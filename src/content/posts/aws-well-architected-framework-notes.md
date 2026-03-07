---
title: "AWS Well-Architected Framework Notes"
published: 2018-10-28
description: ""
tags: [AWS, Security, Reliability]
category: AWS
draft: false
---

---


# **Introduction**

Hey 👋

This is a collection of all of my notes/quotes from the 5 [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/) books/whitepapers, which cover

- Operational Excellence
- Security
- Reliability
- Performance Efficiency
- Cost Optimization

Let me start of by saying that these notes are for me, these notes are mostly:

- the things I know the least and need to repeat a few times to understand
- the stuff I need to research more to understand
- they represent the most crucial parts of the given white paper

If you also get something out of this or if it helps you in some way as well, then amazing :)

In retrospect, the one thing I noted while reading these white papers is that you are not meant to learn the contents of the papers by heart, you are instead meant to read and practice the recommendations they focus on until you start to think like a Solutions Architect. They are AWS white papers, but there is nothing stopping you from replacing the services in these books with ones from Google Cloud or Azure and applying the principles and strategies there.

Also, don't just do everything that is written in these books, review the services objectively.

"Just because it is managed doesn't mean it is better."

The best white paper in my opinion is the Reliability Pillar.

In addition to reading these books, I would also highly recommend the following as nice fillers:

- [The Open Guide to Amazon Web Services](https://github.com/open-guides/og-aws)
- [aws-mindmap](https://github.com/gitvani/aws-mindmap)

---

PS the best way to copy and paste notes from Kindle is to attach a Goodreads account and grab the notes from there since it's fiddly to copy from the mobile app, and they disabled copy from the web client :/

# **Operational Excellence Pillar**

- The operational excellence pillar includes the ability to run and monitor systems to deliver business value and to continually improve supporting processes and procedures.
- In the cloud, you can automate the creation of annotated documentation after every build.
- Make frequent, small, reversible changes.
- Refine operations procedures frequently.
- Set up regular Game Days to review and validate that all procedures are effective and that teams are familiar with them.
- Anticipate failure: Perform “pre-mortem” exercises to identify potential sources of failure so that they can be removed or mitigated.
- You will have runbooks that document your routine activities and playbooks that guide your processes for issue resolution.
- The key AWS service that supports operational readiness is AWS Lambda, which enables the definition of operational procedures as code that can be triggered by events within your environment.
- In AWS, you can improve recovery time by replacing failed components with known good versions, rather than trying to repair them. You can then carry out analysis on the failed resource out of band.

# **Security Pillar**

- The security pillar encompasses the ability to protect information, systems, and assets while delivering business value through risk assessments and mitigation strategies.
- Using federation reduces the need to create users in IAM while leveraging the existing identities, credentials, and role-based access you might already have established in your organization.
- Take extra care to avoid storing access and secret keys in improperly secured locations or inadvertently committing them to source code repositories.
- AWS STS lets you request temporary, limited-privilege credentials for authentication with other AWS APIs.
- IAM instance profiles for EC2 instances allow you to leverage the Amazon EC2 metadata service and managed, temporary credentials for accessing other AWS APIs.
- AWS Organizations should be used to centrally manage accounts. This service allows grouping accounts into organizational units (OUs). Service control policies (SCPs) can be used to centrally control AWS services across multiple AWS accounts.
- You can use native, API-driven services to collect, filter, and analyze logs instead of maintaining and scaling the logging backend yourself.
- You can direct CloudTrail logs to Amazon CloudWatch Logs or other endpoints so that you can obtain events in a consistent format across compute, storage, and applications.
- A best practice for building a mature security operations team is to deeply integrate the flow of security events and findings into a notification and workflow system such as a ticketing system, a bug/issue system, or other security information and event management (SIEM) system. This takes the workflow out of email and static reports, allowing you to route, escalate, and manage events or findings. Many DevOps organizations are now integrating security alerts into their chat/collaboration and developer productivity platforms.
- In AWS, routing events of interest and information reflecting potentially unwanted changes into a proper workflow is done using Amazon CloudWatch Events.
- Using Amazon Inspector, you can perform configuration assessments for known common vulnerabilities and exposures (CVEs), assess your instances against security benchmarks, and fully automate the notification of defects.
- In AWS, there are a number of different approaches to consider when addressing data protection. The following section describes how to use these approaches:
    - Data classification
    - Encryption/tokenization
    - Protecting data at rest
    - Protecting data in transit
    - Data backup/replication/recovery.
- Consider storing backups in a different account with a different set of credentials to protect against human error or a compromise of the primary account.

# **Reliability Pillar**

- The reliability pillar encompasses the ability of a system to recover from infrastructure or service disruptions, dynamically acquire computing resources to meet demand, and mitigate disruptions such as misconfigurations or transient network issues.
- Service availability is commonly defined as the percentage of time that an application is operating normally.
- Designing applications for higher levels of availability typically comes with increased costs, so it’s appropriate to identify the true availability needs before embarking on application design.
- In general, you should plan on deploying large VPC CIDR blocks. Note that VPC CIDR blocks can be changed after they are deployed, but if you allocate large CIDR ranges for your VPC, it will be easier to manage in the long term.
- Critically evaluate the unique aspects to your applications and, where appropriate, differentiate the availability design goals to reflect the needs of your business.
- In the years that we’ve operated Amazon.com and AWS, we’ve gathered deep experience in designing applications for availability. While there are many lessons to be learned, the five most common practices we apply to improve availability are following:
    - Fault Isolation Zones
    - Redundant components
    - Micro-service architecture
    - Recovery Oriented Computing
    - Distributed systems best practices
- When building a system that relies on redundant components, it’s important to ensure the components operate independently, and in the case of AWS Regions, autonomously. Theoretical availability calculations are only valid if this holds true.
- A pattern to avoid is developing recovery paths that are rarely executed.
- Our experience has shown that the only error recovery that works is the path you test frequently.
- Retry with exponential fallback: This is the invoking side of the throttling pattern we just discussed. AWS SDKs implement this by default, and can be configured. The pattern is to pause and then retry at a later time. If it fails again, pause longer and retry. This increase in pause time is often called “backing off.” After a configured number of attempts or elapsed time, it will quit retrying and return failure.
- Be very mindful of places where queues exist (they often hide in workflows or in work that’s recorded to a database).
- We refer to this as “bi-modal” behavior, because the system has different behavior under normal and failure modes.
- One of the most important rules AWS has established for its own deployments is to avoid touching multiple Availability Zones within a Region at the same time.
- Monitoring at AWS consists of five distinct phases:
    - Generation
    - Aggregation
    - Real-time processing and alarming
    - Storage
    - Analytics

# **Performance Efficiency Pillar**

- Performance efficiency in the cloud is composed of four areas:
    - Selection
    - Review
    - Monitoring
    - Trade-offs Take a data-driven approach to building a high-performance architecture.
- In AWS, compute is available in three forms: instances, containers, and functions.
- Containers are a method of operating system virtualization that allow you to run an application and its dependencies in resource-isolated processes.
- The optimal storage solution for a particular system varies based on the kind of access method (block, file, or object) you use, patterns of access (random or sequential), throughput required, frequency of access (online, offline, archival), frequency of update (WORM, dynamic), and availability and durability constraints.
- When you select a storage solution, you should consider the different characteristics that you require, such as ability to share, file size, cache size, latency, throughput, and persistence of data. Then match the requirements you want to the AWS service that best fits your needs: Amazon S3, Amazon Glacier, Amazon Elastic Block Store (Amazon EBS), Amazon Elastic File System (Amazon EFS), or Amazon EC2 instance store.
- SSD-backed storage for transactional workloads, such as databases and boot volumes (performance depends primarily on IOPS), and HDD-backed storage for throughput-intensive workloads such as MapReduce and log processing (performance depends primarily on MB/s).
- Consider using RAID 0 when I/O performance is more important than fault tolerance.
- The optimal database solution for a particular system can vary based on your requirements for availability, consistency, partition tolerance, latency, durability, scalability, and query capability.
- Although a workload’s database approach (for example, relational database management system or RDBMS, NoSQL, etc.) has significant impact on performance efficiency, it is often an area that is chosen according to organizational defaults rather than through using a data-driven approach.
- Amazon EC2 provides placement groups for networking. A placement group is a logical grouping of instances within a single Availability Zone. Using placement groups with supported instance types enables applications to participate in a low-latency, 20-gigabits-per-second (Gbps) network. Placement groups are recommended for applications that benefit from low network latency, high network throughput, or both. Using placement groups has the benefit of lowering jitter in network communications.
- AWS Direct Connect provides dedicated connectivity to the AWS environment, from 50 Mbps up to 10 Gbps.
- Network Load Balancer is best suited for load balancing of TCP traffic where extreme performance is required. It is capable of handling millions of requests per second while maintaining ultra-low latencies, and it is also optimized to handle sudden and volatile traffic patterns.
- Benchmarking should be used in conjunction with load testing because load testing will tell you how your whole workload will perform in production.
- The location of your load test clients should reflect the geographic spread of your end users.
- Partitioning or sharding provides a way to scale write-heavy workloads, but requires that data is evenly distributed and evenly accessed across all partitions or shards. It can introduce complexity in relational database solutions, while NoSQL solutions generally trade consistency to deliver this.
- When architecting with a buffer keep in mind two key considerations. First, what is the acceptable delay between producing the work and consuming the work? Second, how do you plan to handle duplicate requests for work?

# **Cost Optimization Pillar**

- A cost-optimized system will fully utilize all resources, achieve an outcome at the lowest possible price point, and meet your functional requirements.
- Cost optimization in the cloud is composed of four areas:
    - Cost-effective resources
    - Matching supply with demand
    - Expenditure awareness
    - Optimizing over time
- Right sizing is using the lowest cost resource that still meets the technical specifications of a specific workload.
- AWS Trusted Advisor performs analysis of resources and reports on any under- or over-utilized resources.
- On-Demand Instances are recommended for applications with short-term workloads (such as a four-month project) that spike periodically, or unpredictable workloads that can’t be interrupted.
- Spot Instances are ideal for use cases such as batch processing, scientific research, image or video processing, financial analysis, and testing.
- Standard Reserved Instances provide both a billing benefit and capacity reservation when the instance family, size, and Availability Zone are specified. Convertible Reserved Instances are provided for a one-year or three-year term and allow conversion to different families, new pricing, different instance sizes, different platforms, or tenancy during the period.
- The economic benefits of just-in-time supply needs to be balanced against the need to provision to account for resource failures, high availability, and provision time.
- In AWS, you can use a number of different approaches to match supply with demand. The following sections describe how to use these approaches:
    - Demand-based
    - Buffer-based
    - Time-based
- Amazon SQS provides a queue that allows a single consumer to read individual messages. Amazon Kinesis provides a stream that allows many consumers to read the same messages.
- When architecting with a buffer-based approach keep in mind two key considerations. First, what is the acceptable delay between producing the work and consuming the work? Second, how do you plan to handle duplicate requests for work?
- Idempotence is an application logic pattern that allows a consumer to process a message multiple times, but when a message is subsequently processed it has no effect on downstream systems or storage.
