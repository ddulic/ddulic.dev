---
title: "Terraform Cloud External Data Source"
published: 2022-10-17
description: ""
tags: [Terraform, AWS, CloudFront]
category: Terraform
draft: false
---

I had the pleasure of working with Terraform Cloud recently, and I had to use the [External Data Source](https://registry.terraform.io/providers/hashicorp/external/latest/docs/data-sources/data_source), something Terraform only wants you to use a last resort.

For those who don't know what Terraform Cloud is, it “removes many of the complexities in trying to maintain your own Terraform state files in a multi-team, collaborative Terraform environment.” TLDR; it is Terraforms SaaS offering.

Before you all start yelling, that you really shouldn’t be using an External Data Source, well, I HAD NO OTHER OPTION, OK?

I wanted to enable [Additional CloudFront Metrics](https://aws.amazon.com/about-aws/whats-new/2019/12/cloudfront-realtime-metrics/), but AWS doesn’t offer you a way to do this via CloudFront (and thus CDK).

There has been an [open issue on GitHub](https://github.com/aws-cloudformation/cloudformation-coverage-roadmap/issues/545) since mid-2020.

Note that I am aware of a way to do it via a [Lambda](https://github.com/aws-cloudformation/cloudformation-coverage-roadmap/issues/545#issuecomment-962584689), but that approach has multiple drawbacks and I refuse to confront to AWS’s answer of “you can do it via a Lambda”.

---

Decided to go down the Terraform route, and luckily, there is a resource available that I can use - [aws_cloudfront_monitoring_subscription](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudfront_monitoring_subscription), however, due to our use-case I want to enable it for all Distributions and there isn’t anything in Terraform that would allow you to do that.

My first idea was to just use the AWS CLI

```hcl
data "external" "json" {
  program = ["sh", "-c", "aws cloudfront list-distributions | jq '.DistributionList.Items[].Id'"]
}
```

I tried both `bash` and `python`, but no matter what I try, I can’t seem to pass it the map of strings it expects...

Some version of the below error is always present...

```bash
Result Error: json: cannot unmarshal string into Go value of type map[string]string
```

I poked around quite a bit trying to make it work with `jq`, attempting to generate the output that Terraform wants, but failed...

The main issue was that Terraform expects a dictionary object of a specific make, the structure of which is nowhere documented.

I also had the idea that I could possibly create a dictionary of the `.DomainName` and `.Id` from the output. I managed to do it in the end effortlessly with Python.

```python
#!/usr/bin/env python3
# coding: utf-8

import sys
import json
import boto3

def list_distributions():
    client = boto3.client('cloudfront')
    try:
        response = client.list_distributions()
        distributions = {}
        for each in response['DistributionList']['Items']:
            distributions[each['DomainName']] = each['Id']
        output = json.dumps(distributions)
        sys.stdout.write(output)
    except ValueError as e:
        sys.exit(e)

if __name__ == "__main__":
    list_distributions()
```

The question is will this work with Terraform Cloud, which is what I want to use to apply this change, so every time a new Distribution gets added an empty PR will have to be created to trigger the change.

Moving on with the Python idea… the next issue was that it didn’t like the fact that there was a package dependency of `boto3` in my Python script...

```bash
Error: External Program Execution Failed
with data.external.distribution_ids
on data.tf line 2, in data "external" "distribution_ids":
  program = ["python3", "${path.module}/list-distributions.py"]
The data source received an unexpected error while attempting to execute the program.

Program: /usr/bin/python3
Error Message: Traceback (most recent call last):
  File "./list-distributions.py", line 6, in <module>
    import boto3
ModuleNotFoundError: No module named 'boto3'

State: exit status 1
```

Look at their documentation there wasn’t a way to add packages to the runner, so I turned to creating a single package with all the dependencies included, I tried the following and failed with all of them for various reasons...

- [cx_freeze](https://cx-freeze.readthedocs.io/en/latest/)

    Doesn’t provide a single file, I wanted to avoid adding multiple libraries to the repo...

- [pyinstaller](https://pyinstaller.org/en/stable/)

  ```bash
  ❯ docker run -v "$(pwd)"/scripts:/home/scripts python /bin/bash -c "cd /home/scripts && pip install -r ./requirements.txt && pyinstaller --target-architecture x86_64 -F ./list-distributions.py"
  ```

    However, that produced an arm binary due to my Mac being M1...

  ```bash
  ❯ file ./scripts/dist/list-distributions
  ./scripts/dist/list-distributions: ELF 64-bit LSB executable, ARM aarch64, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux-aarch64.so.1, BuildID[sha1]=8cd3bd5a35e6e5119702441ea72b8e4c66888bf9, for GNU/Linux 3.7.0, stripped
  ```

    Once I passed `--platform linux/amd64` it built the correct binary, however Terraform wasn’t happy and complained how `glibc_2.29'` is not found in Terraform Cloud.

    I thought it maybe wasn’t happy that I built it with Python 3.10 (I saw somewhere that Terraform Cloud has 3.6), but after building the binary with 3.6 it also wasn’t happy - [https://app.terraform.io/app/qualio-incubating/air-lab-cloudfront-monitoring-sandbox/runs/run-WscFcWAHDsq8RZjk](https://app.terraform.io/app/qualio-incubating/air-lab-cloudfront-monitoring-sandbox/runs/run-WscFcWAHDsq8RZjk)

    In the end, I ditched pyinstaller...

- [pex](https://pex.readthedocs.io/en/v2.1.92/)

  ```bash
  ❯ docker run --platform linux/amd64 -v "$(pwd)"/scripts:/home/scripts python:3.6 /bin/bash -c "cd /home/scripts && pip install -r ./requirements.txt && pex . boto3 -c ./list-distributions.py -o ./list-distributions.pex"
  ```

    But no matter what I tried, the build always failed for, to be unknown, errors - [https://app.terraform.io/app/qualio-incubating/workspaces/air-lab-cloudfront-monitoring-sandbox/runs/run-GgjfySPBJyJCTu3U](https://app.terraform.io/app/qualio-incubating/workspaces/air-lab-cloudfront-monitoring-sandbox/runs/run-GgjfySPBJyJCTu3U)


Why is it so hard to build a binary in python?

I briefly thought about dusting off my golang as binaries are made easy, but didn’t want to go down that rabbit hole...

---

In the end I just ended up with the hack to install boto3 with pip before running my script (something I tried before but didn’t work), but this time I explicitly declared `python3` as the executable, and it worked... O Terraform Cloud... why thou not alias `python` to `python3`...

```hcl
data "external" "distribution_ids" {
  program = ["bash", "-c", "pip3 install boto3 > /dev/null 2>&1 && python3 ${path.module}/list-distributions.py"]
}

resource "aws_cloudfront_monitoring_subscription" "cf_enable_subscription" {
  for_each = data.external.distribution_ids.result
  distribution_id = each.value

  monitoring_subscription {
    realtime_metrics_subscription_config {
      realtime_metrics_subscription_status = "Enabled"
    }
  }
}
```

---

As for how to update when a Distribution gets added, I tried creating an empty PR, but that didn’t trigger a build, instead I added a `VERSION` file that will have to be incremented every time a Distribution is added.

I tested removing a Distribution, bumping the version, and it didn’t trigger a plan change. The Terraform Cloud UI still showed that the resource was managed.

When I disabled the Advanced Monitoring in the AWS Console for a Distribution and triggered a Plan in the UI, it correctly saw the drift, corrected it for the said Distribution and removed the old deleted one from the Terraform Cloud UI.

Have a wonderful day and happy Terraforming!
