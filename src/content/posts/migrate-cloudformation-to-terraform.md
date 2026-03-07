---
title: "Migrate CloudFormation to Terraform"
published: 2023-03-28
description: ""
tags: [Terraform, AWS, Migration, IaC]
category: Terraform
draft: false
---

This guide will show you how to migrate resources managed by AWS [CloudFormation](https://aws.amazon.com/cloudformation/) to [Terraform](https://www.terraform.io/) without destroying the resources and creating them again.

You need to keep in mind that deprecating CloudFormation is a delicate process that manipulates existing resources on your account. Always make sure to triple-check before running any change.

The process involves a couple of steps:

1. Check CloudFormation managed resources
2. Add `DeletionPolicy` to the resources
3. Terraform Import Local
4. Terraform Import Remote
5. Terraform Apply
6. Delete CloudFormation Stack

Let’s take an example that we will migrate a CloudFront Distribution Stack that is consistent of the following Resource Types:

- AWS::CertificateManager::Certificate
- AWS::Route53::RecordSetGroup
- AWS::CloudFront::Distribution
- AWS::CloudFront::CloudFrontOriginAccessIdentity
- AWS::CloudFront::Function
- AWS::S3::Bucket
- AWS::S3::BucketPolicy

According to the AWS CloudFormation Documentation, if we want to keep resources when the Stack is deleted, we have to add `DeletionPolicy: Retain` all resources under the stack.

However, when I deleted a test stack that I had created, everything got deleted regardless? 😕

I couldn’t really find anything online, luckily [cfn-lint](https://github.com/aws-cloudformation/cfn-lint) was useful, it listed the below for all resources where I added the `DeletionPolicy`.

```bash
W3011 Both UpdateReplacePolicy and DeletionPolicy are needed to protect Resources/FrontendOriginAccessIdentity from deletion
infrastructure.yaml:16:3
```

Why wouldn’t you mention this somewhere in the [DeletionPolicy attribute - AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-deletionpolicy.html) Documentation?

Finally, after adding the `UpdateReplacePolicy: Retain` I got what I wanted. When I now deleted the test Stack, I can see the Deletion is being skipped.

The next stage will be the longest one… writing Terraform code and making sure when you import that there are no changes, meaning that Terraform Infra Code matches the CloudFormation Infra Code.

To write Terraform code for our example, I found it useful to create a list based on the resources in the CloudFormation stack. This list includes everything we need.

- [x]  Generate TF for Route53
- [x]  Generate TF for CloudFront
- [x]  Generate TF for CloudFrontOriginAccessIdentity
- [x]  Generate TF for Buckets
- [x]  Generate TF for CloudFront Functions
- [x]  Generate TF for Bucket Policies
- [x]  Generate TF for ACM

Below was the process that allowed me to do it in less than 1 working day.

The biggest issue when importing is getting an initial state, I use [terraformer](https://github.com/GoogleCloudPlatform/terraformer) to assist me with that.

I first [planned](https://github.com/GoogleCloudPlatform/terraformer#planning) all the valid sections that I cared about

```bash
terraformer plan aws --resources=acm --regions=us-east-1
terraformer plan aws --resources=cloudfront
terraformer plan aws --resources=route53
terraformer plan aws --resources=s3
```

I had issues with the `filter` syntax, so I manually edited the generated json to only include the elements that I care about. The list of available resources is listed [here](https://github.com/GoogleCloudPlatform/terraformer/blob/master/docs/aws.md).

I then imported them

```bash
terraformer import plan generated/aws/terraformer/acm.json
terraformer import plan generated/aws/terraformer/cloudfront.json
terraformer import plan generated/aws/terraformer/route53.json
terraformer import plan generated/aws/terraformer/s3.json
```

As can be seen from the previous link, not all resources were supported, I had to write some Terraform manually (the inhumanity) and import the CloudFront Origin Access Identities and CloudFront Functions.

```bash
terraform import aws_cloudfront_origin_access_identity.FrontendOAI EXAMPLEXXXXXXX
terraform import aws_cloudfront_origin_access_identity.OAITwo EXAMPLEXXXXXXX
terraform import aws_cloudfront_function.AppFunction app-function
terraform import aws_cloudfront_function.FunctionTwo function-two
```

The `terraformer import` also generates a valid state file, but it is scattered all over the place, so I used [jordiprats/tfstate-merge](https://github.com/jordiprats/tfstate-merge) to merge them all into one. I used the S3 state as the starting point and merged the rest into it

```bash
python ~/Documents/tfstate-merge/mergestates.py generated/aws/acm generated/aws/route53 generated/aws/cloudfront .
```

Terraformer generates a state file with an old provider (at least at the date I ran it), so I had to replace it

```bash
terraform state replace-provider registry.terraform.io/-/aws hashicorp/aws
```

The S3 buckets also weren’t fully up to date. I had to split out the policy, metrics and access policy and manually import them. Example for `frontend-app`

```bash
terraform import aws_s3_bucket_metric.frontend_app frontend-app:EntireBucket
terraform import aws_s3_bucket_public_access_block.frontend_ap frontend-app
terraform import aws_s3_bucket_policy.frontend_app frontend-app
```

I skipped `AccessControl: "BucketOwnerFullControl"` as AWS [ignores it by default](https://docs.aws.amazon.com/AmazonS3/latest/userguide/acl-overview.html#canned-acl).

---

The next order of business is to get this packaged up into a module. This will depend on how you want to structure the module and what would work for your project, but it will involve running a lot of `terraform state mv` to make everything work.

Hopefully, this helps someone. Have a wonderful day.
