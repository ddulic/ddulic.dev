---
title: "2018 Website Continuous Deployment Pipeline"
published: 2018-02-17
description: ""
tags: [CI/CD, AWS, S3, CloudFront]
category: DevOps
draft: false
---

---


New year, new website... again. But this one may be here to stay.

Solving a series of problems starting from an idea to a fully working system is why I love my work. It makes me happy.

“To be happy we need something to solve. Happiness is therefore a form of action;” ― Mark Manson, The Subtle Art of Not Giving a F*ck: A Counterintuitive Approach to Living a Good Life

If you haven't read the book, I highly recommend you do.

Moving on...

# **Intro**

This time the setup is a whole new beast. Everything is fully automated in a Continuous Deployment pipeline and every component can be found on my GitHub profile.

I had a few issues with the last platform I used, and I wanted them addressed.

I also wanted to learn something new. The solution was to somehow set up a CI/CD pipeline for my website, host it on AWS and make it in such a way so that it doesn't backstab my wallet.

# **Solution**

Since [Ghost](https://github.com/ddulic/damir.tech/blob/master/posts/i-switched-to-markdown/#Ghost-Setup) doesn't support static file hosting, I required a new platform.

After some research and testing, I ended up on [hexo](https://hexo.io/) because:

- it's fast
- uses markdown
- extendable via plugins
- has numerous themes to choose from
- supports static file hosting

Took me a while to configure Hexo to the way I wanted and once I did, it wasn't hard to figure out to put it as a static website on S3. AWS's [official guide](https://docs.aws.amazon.com/AmazonS3/latest/dev/website-hosting-custom-domain-walkthrough.html) was sufficient in giving me all the needed information.

# **Flow**

So sum up the general workflow of adding a new post

- `git push` locally edited files to a remote GitHub repo
- Travis CI is set up to watch the repo and on a commit execute the build details in `.tavis.yaml` in the root of the project
- travis generates the static files and pushes them to the designated AWS S3 Bucket

# **Setup**

Like I said, everything is open and can be found on my GitHub, along with the basic understanding of how everything works which is explained in this post you should have no problem 1:1 copying and modifying to fit your needs.

## **AWS**

The AWS part might be the only one which requires additional information.

S3 does the job, but only if we want to use the AWS's S3 endpoint. If we would like to use a custom name, we have to point our Domain Name to the AWS's S3 endpoint, but this method doesn't allow us to use https directly on AWS.

To use TLS, we have to use CloudFront and attach a certificate to our CF ID, for which a guide can be found [here](https://docs.aws.amazon.com/AmazonS3/latest/dev/website-hosting-cloudfront-walkthrough.html).

~~Once we have set up our CloudFront and pointed it to S3, there is a tool which can setup `https` via [Let's Encrypt](https://letsencrypt.org/) automagically for us - [certbot-s3front](https://github.com/dlapiduz/certbot-s3front); just follow their README :)~~

Update: I ditched LE in favor of [AWS Certificate Manager](https://aws.amazon.com/certificate-manager/pricing/) just so I don't have to think about constantly renewing. They offer free public certificates.

So, in the end, it looks something like this:

S3 files → S3 endpoint → CloudFront ID ~~(With LE Cert)~~ → Route 53 Alias

Note: Due to the way CloudFront works in caching our content, your changes won't be visible immediately upon the file's updating in S3 (it can take up to 24h). If you want to circumvent this, you need to trigger an invalidation on CloudFront, more info [here](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Invalidation.html).

# **Cost $$$**

This is nice and all, but how much will this cost me? -- Well, it will cost you almost nothing compared to other hosting providers. AWS does an estimation [here](https://aws.amazon.com/getting-started/projects/host-static-website/) which says:

The total cost of hosting your static website on AWS will vary depending on your usage. Typically, it will cost \$1-3/month if you are outside the AWS Free Tier limits. If you qualify for AWS Free Tier and are within the limits, hosting your static website will cost around \$0.50/month.

In my case, so far, it is costing just as they said, \$0.50/month since I am still in the free tier.

# **Final Thoughts**

All in all, it was a pleasant learning experience for me, I got to research in depth multiple AWS services as well as get some hands-on experience and in doing so, I got to update my website.

I still have some ideas for possible improvements, like:

- cache invalidation via a Lambda
- ~~let's encrypt certificate renew via a Lambda~~

Time to start playing with lambda :)
