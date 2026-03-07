---
title: "Using external-dns to Migrate Services between Kubernetes Clusters"
published: 2022-03-20
description: ""
tags: [Kubernetes, AWS, DNS, Migration]
category: Kubernetes
draft: false
---

# Introduction

We live in a world of microservices that are intertwined (kind of the point), usually within a complex network structure. If you utilize AWS and have your service deployed in EKS, you are most likely using AWS Load Balancers to expose said service, making it accessible to the entire world. Your domain name lives in Route53 and you want to map that to your ELB provisioned by an Ingress Controller in Kubernetes. In a non-k8s world, you would manage this from a tool or pipeline, likely utilizing the AWS CLI or SDK that configures the domain in Route53, or worse, you would configure it manually.

What if you have hundreds of services and DNS records that need to be created and managed? What if the Load Balancer Endpoint changes? How do you keep track of hundreds of DNS records? Kubernetes allows us to utilize [external-dns](https://github.com/kubernetes-sigs/external-dns).

> ExternalDNS allows you to control DNS records dynamically via Kubernetes resources in a DNS provider-agnostic way.
>

You can also use external-dns to migrate between clusters, which I will be covering in this post.

# Prerequisites

- Kubernetes Cluster configured in AWS. I will assume both Clusters are in AWS for this example.
- AWS Route53 zone created and configured. For this post, I will assume you are familiar with Route53 and have done this already.
- An Ingress Controller configured in the Kubernetes Cluster. The good thing about external-dns is that it doesn't care about what this is, as long as it uses Ingress or Service k8s objects. If you use an external service, see [kubernetes-sigs/external-dns#deploying-to-a-cluster](https://github.com/kubernetes-sigs/external-dns#deploying-to-a-cluster) for more info.

# Setup

There are two approaches:

- Blue-Green
- Canary

There are pros and cons to both approaches. The choice of the approach will depend on the teams and their requirements.

Blue-Green uses a [Simple Record](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html#routing-policy-simple), something that our services have had configured, so there is no need to change the record type, a huge bonus.

Canary uses a [Weighted Record](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html#routing-policy-weighted), and sadly, in Route53, you can't switch from one policy to another. You have to DELETE the existing record, causing downtime if any service caches the no-response in the time to create the record. To semi-mitigate this, I have reduced the sync time with external-dns to a few seconds instead of the default 60 seconds.

---

For the main external-dns setup, follow the [instructions for AWS](https://github.com/kubernetes-sigs/external-dns/blob/master/docs/tutorials/aws.md).

Below are the specific args you need to configure to make sure the setup works as intended for this use-case, passing the values as env variables

```yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: external-dns
spec:
  template:
    spec:
      containers:
        - name: external-dns
          args:
            - --source=service
            - --source=ingress
            - --provider=aws
            - --zone-id-filter=$(HOSTED_ZONE_ID_FILTER)
            - --policy=sync
            - --aws-zone-type=$(HOSTED_ZONE_TYPE)
            - --registry=txt
            - --txt-owner-id=$(CLUSTER_NAME)
            - --aws-batch-change-size=2
            - --interval=5s
```

Let's go through all the args:

- `--source`; the k8s objects you want to watch.
- `--provider`; self-explanatory.
- `--zone-id-filter`; make sure that only the zone you would like to change is modified.
- `--policy`; modifies how DNS records are synchronized between sources and providers. The default is "sync" but, explicit is always better than implicit.
- `--aws-zone-type`; private or public zone type.
- `--registry`; create a TXT record alongside the ALIAS (A) Record. The TXT Record signifies that the corresponding ALIAS Record is managed by external-dns. This makes external-dns safer for running in environments where there are other records managed via other means.
- `--txt-owner-id`; this is the main component I will take advantage of for our use case. Set this to a unique name for your cluster.
- `--aws-batch-change-size`; tmp fix for the "Blocking Changes" mentioned below in Issues.
- `--interval`; lowering the interval to update Route53 as soon as possible. The lower value is required to reduce downtime when switching between record types. [The default is 1 minute](https://github.com/kubernetes-sigs/external-dns/blob/7f547d23fd70b5c4fe171048e9246638e0295151/pkg/apis/externaldns/types.go#L497). When changing this, note the [Route53 API Request Limits](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/DNSLimitations.html#limits-api-requests-route-53).

---

Now, you need to make the required service-specific configurations for external-dns. Luckily, there are only annotations.

I will assume that you are already using an Ingress object in your "old" cluster and that the service is available in both locations. How you do this is up to you.

## Blue-Green

To use a Blue-Green release method to switch over to the new cluster, you will have to configure your CICD to change the TXT record associated with the hostname extracted from the Ingress object. The TXT Record should have a similar value to

```yaml
"heritage=external-dns,external-dns/owner=old-cluster,external-dns/resource=ingress/namespace-name/ingress-name"
```

You want to modify the `owner` field to say `new-cluster` instead of old-cluster.

Once you do this, the external-dns running in the new-cluster will see that it owns the record. However, the value of the associated A record isn't valid. It will update it to match the hostname in the Ingress object, switching over the traffic to the new cluster.

How you do this update is up to you. Ideally, you would have it hooked into your CICD as part of the application's deployment, running the required checks to make sure you are modifying the correct record, as well as if the record has changed.

## Canary

When utilizing Canary, add a few additional annotations if you don't have them already.

Make sure the Ingress associated with your service in the current "old" cluster has the following annotations:

```yaml
external-dns.alpha.kubernetes.io/hostname: <service-route53-hostname>
external-dns.alpha.kubernetes.io/alias: "true"
external-dns.alpha.kubernetes.io/set-identifier: <service>-<old-cluster>
external-dns.alpha.kubernetes.io/aws-weight: "50"
```

Consider the following when specifying the annotations:

- `hostname`; self-explanatory.
- `alias`; set to true, explicitly set alias targets to Ingress Load Balancers.
- `set-identifier`; a unique name that differentiates among multiple resource record sets that have the same combination of name and type. As I will use Weighted Records, this is applicable because this will be creating two new A/TXT Records for this domain. For simplicity, suffix your service name with `old-cluster` and assign this as a value.
- `aws-weight`; sets the proportion of DNS queries Route53 should respond to using this Record Set. All queries will route to this record set until you deploy the service on the second new cluster. There will be no difference to the service routing until the second Ingress is created in the new cluster.

The config in the cluster you wish to migrate to should include the same annotations, but with the `set-identifier` and `aws-weigh` modified

```yaml
external-dns.alpha.kubernetes.io/hostname: <service-route53-hostname>
external-dns.alpha.kubernetes.io/alias: "true"
external-dns.alpha.kubernetes.io/set-identifier: <service>-<new-cluster>
external-dns.alpha.kubernetes.io/aws-weight: "5"
```

:::warning
Note that if you have a record already set off a different type, you will have to DELETE the previous record “manually”. I say manually in quotes because you can hook this up with your CICD and make the experience seamless for Developers.
:::

**Tweaking the Weighted Routing**

Choose a number between 0 and 255, bearing in mind that you will need to apportion the total weighting (up to 510 altogether) across the old and new clusters to achieve the desired proportion of traffic routed to either service. For example:

- Assign `"5"` as a value in old-cluster for 9% of traffic to be routed to new-cluster
- Assign `"25"` as a value in old-cluster for 33% of traffic to be routed to new-cluster
- Assign `"50"` as a value in old-cluster for 50% of traffic to be routed to new-cluster
- Assign `"100"` as a value in old-cluster for 66% of traffic to be routed to new-cluster
- Assign `"200"` as a value in old-cluster for 80% of traffic to be routed to new-cluster
- Assign `"255"` as a value in old-cluster for 85% of traffic to be routed to new-cluster

When comfortable, decrease the weighting in the old cluster and/or increase the weighting in the new cluster. Do this until the changes are satisfactory, and the migrated service has 100% weighting in the new cluster.

:::warning
Setting a weight of "0" would stop requests going towards the associated cluster.
:::

# Issues

As always, no solution is perfect. There are some issues with Route53 and external-dns. Here are the ones I ran into:

- Lack of TTL using an Alias

    [Choosing between alias and non-alias records](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-choosing-alias-non-alias.html)

    > If an alias record points to an AWS resource, you can't set the time to live (TTL); Route 53 uses the default TTL for the resource. If an alias record points to another record in the same hosted zone, Route 53 uses the TTL of the record that the alias record points to.
    >

    The ELBs in AWS have a TTL of 60 seconds, and you can't change this (at least not that I could find).

    If the address is changed and the old target is unavailable, you will experience downtime.

- Need to delete the Route53 Record if switching record types

    To make the issue worse, it seems that within AWS, resources will still cache the no-response if you remove the record temporarily. Unexpected as AWS states that Route53 uses the TTL of the record that the alias is pointing towards.

- Blocking Changes
    - If something prevents external-dns from creating a record (for example, say you are switching from a Simple to a Weighted Record), the change will be blocking...

        [https://github.com/kubernetes-sigs/external-dns/issues/1517](https://github.com/kubernetes-sigs/external-dns/issues/1517)

        [external-dns/types.go at 7f547d23fd70b5c4fe171048e9246638e0295151 · kubernetes-sigs/external-dns](https://github.com/kubernetes-sigs/external-dns/blob/7f547d23fd70b5c4fe171048e9246638e0295151/pkg/apis/externaldns/types.go#L404)

    - You will want to be alerted on this to be safe. There is an example of a similar message of `msg=InvalidChangeBatch` ([kubernetes-sigs/external-dns/issues/1517](https://github.com/kubernetes-sigs/external-dns/issues/1517)). An easy way of doing this would be to check the logs for `level=error`.

# Conclusion

Migrating services between clusters is always complex. You want to make sure that there is no-to minimal downtime. You don't want your customers don't have a negative experience.

external-dns and Route53 can fulfil such requirements if used correctly. Hopefully, this post helps you along the journey.
