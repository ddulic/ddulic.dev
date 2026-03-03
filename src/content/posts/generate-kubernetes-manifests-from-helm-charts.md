---
title: "Generate Kubernetes Manifests from Helm Charts"
published: 2022-05-18
description: ""
tags: [Kubernetes, Helm]
category: Kubernetes
draft: false
---

# Introduction

I have stumbled upon many projects that don’t share Kustomize manifests, or even Kubernetes manifests, but do have Helm charts.

Not everyone uses Helm, so I wanted to share a method can be semi-easily automated to generate k8s manifests from Helm charts.

**What is Kustomize**

I need the manifests to use them with Kustomize, which is a templating tool that allows you to “kustomize” the Kubernetes manifests, usually based on environments. As of a few Kubernetes versions ago, kustomize is also built into Kubernetes.

**How does Kustomize Work**

[Introducing kustomize; Template-free Configuration Customization for Kubernetes](https://kubernetes.io/blog/2018/05/29/introducing-kustomize-template-free-configuration-customization-for-kubernetes/#a-new-option-for-configuration-customization)

**Kustomize vs Helm**

Here is some reading material if you are interested in the differences between Kustomize and Helm.

[Comparing Helm vs Kustomize: Kubernetes Templating Tools](https://harness.io/blog/devops/helm-vs-kustomize/)

[K8s Tips : Manifests, Helm, Kustomize](https://itnext.io/k8s-tips-manifests-helm-kustomize-12f72f878022)

# Generate Manifests from Helm Charts

I will be using [cluster-autoscaler](https://github.com/kubernetes/autoscaler) for this example, you can see how the project has [charts](https://github.com/kubernetes/autoscaler/tree/master/charts) but not the manifests ([external-dns](https://github.com/kubernetes-sigs/external-dns/tree/master/kustomize) has manifests, for example)

Let’s dive into it.

---

The first step is to add the autoscaler repository

```bash
helm repo add autoscaler https://kubernetes.github.io/autoscaler
```

Check the latest chart version

```bash
helm search repo autoscaler/cluster-autoscaler
NAME                               	CHART VERSION	APP VERSION	DESCRIPTION
autoscaler/cluster-autoscaler      	9.9.2        	1.20.0     	Scales Kubernetes worker nodes within autoscali...
autoscaler/cluster-autoscaler-chart	2.0.0        	1.18.1     	Scales Kubernetes worker nodes within autoscali...
```

Next, we need to download the latest version

```bash
helm fetch autoscaler/cluster-autoscaler --untar --untardir $PWD/tmp --version 9.9.2
```

I would suggest taking the [values.yaml](https://github.com/kubernetes/autoscaler/blob/master/charts/cluster-autoscaler/values.yaml) and modifying it to suite your needs. `values.yaml` should contain the unique values for the changes in our environment compared to the default values that the helm chart gives us.

```bash
helm template $PWD/tmp/cluster-autoscaler --values values.yaml --namespace cluster-autoscaler --output-dir $PWD/tmp --debug
```

Note that we are hardcoding the namespace above (not required, depends on your deployment strategy), make sure to change/remove it if required.

Once we generate the manifests, we still need to make a few tweaks:

1. (optional) Merge all RBAC related manifests into one. I like to do this as it simplifies the structure

    ```bash
    TMP_LOC=$PWD/tmp/cluster-autoscaler/templates && cd $TMP_LOC && cat clusterrole.yaml clusterrolebinding.yaml role.yaml rolebinding.yaml serviceaccount.yaml > rbac.yaml && cd -
    ```

2. Move the following into the `base` directory from `tmp/cluster-autoscaler/templates`
    - `deployment.yaml`
    - `pdb.yaml` if there are any changes
    - `service.yaml` if there are any changes
    - newly generated `rbac.yaml`
3. There are some values that we can't replace via `values.yaml` as they are built into Helm, so we have to remove them

    ```bash
    sed -i '' '/app.kubernetes.io\/instance/d' base/*.yaml
    sed -i '' 's/RELEASE-NAME-cluster-autoscaler/cluster-autoscaler/g' base/*.yaml
    ```


Now all that is left is to create a kustomize manifest and test locally before adding it to version control.

I hope this has been useful, have a wonderful day.
