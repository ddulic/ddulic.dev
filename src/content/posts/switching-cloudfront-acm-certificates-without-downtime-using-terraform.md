---
title: "Switching CloudFront ACM Certificates Without  Downtime Using Terraform"
published: 2023-05-19
description: ""
tags: [Terraform, CloudFront, AWS]
category: Terraform
draft: false
---

If you are looking to switch to a new CloudFront ACM Certificate without any downtime, you are in the right place. In this blog post, I will show you how to do this using Terraform.

---

Changing the ACM Certificate will cause downtime, the downtime can last for about 5–10 minutes while the Certificate is replaced.

You can create a new Certificate with the domains you want while the old one is still attached to the Distribution. When the Certificate is ready, you can update or change the new Certificate on the Distribution, and CloudFront will take a few minutes to redeploy. In the meantime, the Distribution will serve the old Certificate and switch to the new one when the redeployment propagates. Afterward, you can delete the old Certificate when it is no longer being served to users. This way, there will be no downtime.

## Prerequisites

Before we start, we assume that you have the following:

- A CloudFront Distribution that is already deployed.
- Basic knowledge of Terraform and a modularized setup, my module will use the name `module_name`.

# Current Certificate Setup

I will assume you have an [aws_acm_certificate_validation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/acm_certificate_validation) already setup (ACM CloudFront Certificates have to live in us-east-1)

```hcl
resource "aws_acm_certificate_validation" "certificate" {
  certificate_arn         = aws_acm_certificate.certificate.arn
  validation_record_fqdns = [for record in aws_route53_record.certificate_validation : record.fqdn]
}
```

Tip: use [aws_acm_certificate](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/acm_certificate) to keep your ACM record validations in Terraform. Using DNS as a validation method makes it even easier to manage.

```hcl
resource "aws_acm_certificate" "certificate" {
  domain_name = var.domain_name

  options {
    certificate_transparency_logging_preference = "ENABLED"
  }

  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_route53_record" "certificate_validation" {
  for_each = {
    for dvo in aws_acm_certificate.certificate.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
      zone_id = var.zone_id
    }
  }

  name    = each.value.name
  records = [each.value.record]
  ttl     = 300
  type    = each.value.type
  zone_id = each.value.zone_id
}
```

---

This Certificate should be referenced in your [aws_cloudfront_distribution](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudfront_distribution) resource

```hcl
resource "aws_cloudfront_distribution" "distribution" {
  # ...
  viewer_certificate {
    acm_certificate_arn = aws_acm_certificate_validation.certificate.certificate_arn
		cloudfront_default_certificate = "false"
    ssl_support_method   = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }
  # ...
}

```

# Create the New ACM Certificate

This is the easy part, you just have to copy the current certificate block and rename the resource. Isn’t IaC amazing?

```hcl
resource "aws_acm_certificate" "new_certificate" {
  domain_name = var.domain_name

  options {
    certificate_transparency_logging_preference = "ENABLED"
  }

  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}
```

Run your pipeline and make this is `terraform apply`ed.

# Switch to the New ACM Certificate

Because we are using the `aws_acm_certificate_validation.certificate.certificate_arn` in our CloudFront config to reference the Certificate, this is where we have to change it.

Modify the value of `certificate` in the `aws_acm_certificate_validation.certificate` Resource

```hcl
resource "aws_acm_certificate_validation" "certificate" {
  certificate_arn         = aws_acm_certificate.new_certificate.arn
  validation_record_fqdns = [for record in aws_route53_record.certificate_validation : record.fqdn]
}
```

Run your pipeline and make this is `terraform apply`ed.

# Rename Resources

To prevent deletions, we will have to move some items around in the Terraform State. If you are updating the Certificate to add/remove SANs, the validation records will be updated automatically.

```bash
❯ terraform state mv 'module.module_name.aws_acm_certificate.certificate' 'module.module_name.aws_acm_certificate.old_certificate'
Move "module.module_name.aws_acm_certificate.certificate" to "module.module_name.aws_acm_certificate.old_certificate"
Successfully moved 1 object(s).

❯ terraform state mv 'module.module_name.aws_acm_certificate.new_certificate' 'module.module_name.aws_acm_certificate.certificate'
Move "module.module_name.aws_acm_certificate.new_certificate" to "module.module_name.aws_acm_certificate.certificate"
Successfully moved 1 object(s).
Releasing state lock. This may take a few moments...
```

Tip: run `terraform state list` to get a list of all resources in the state.

Update your code to match the above renames, so you are renaming:

- Resource aws_acm_certificate.certificate → aws_acm_certificate.old_certificate
- Value of aws_acm_certificate_validation.certificate.certificate_arn
    - aws_acm_certificate.new_certificate.arn → aws_acm_certificate.certificate.arn
- Resource aws_acm_certificate.new_certificate → aws_acm_certificate.certificate

:::warning
You must modify the state before you plan and apply, make sure to lock the pipeline for this process.
:::

After the resources have been renamed, run your pipeline and make this is `terraform apply`ed. There should be no ACM or CloudFront changes.

# Verify the New ACM Certificate

After Terraform has updated your CloudFront Distribution, you should verify that the new Certificate is being used. You can do this by checking the Certificate information in your browser or with [openssl](https://support.moonpoint.com/security/encryption/openssl/checking-website-certificate.php)

```bash
❯ echo | openssl s_client -connect google.com:443 2>/dev/null | openssl x509 -noout -fingerprint
SHA256 Fingerprint=D5:12:96:35:A0:50:F6:3D:D6:07:FF:A9:27:1E:EF:AA:B5:97:C0:97:58:09:76:5D:AD:25:39:73:FC:55:4D:25
```

# Conclusion

Switching to a new CloudFront ACM Certificate without any downtime is a straightforward process in the UI, not so much using Terraform as we have to fiddle with the State, just so we leave a clean trail.

By following the steps outlined in this post, you can make the switch seamlessly and without any disruptions to your users.

I hope you found this helpful.
