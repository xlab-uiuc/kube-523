# HW1

## Overview

In this homework, you will create a Kind cluster, deploy the operator you picked on the Kind cluster, and deploy an example managed system.

## Learning Objective

This homework is meant to get you familiar with the operator you pick, and prepare for the Lab 1. This also gives you the opportunity to find potential problems with the operator you picked, and change to another operator.

## Creating Kind Cluster

First, install the Kind tool:

- Install Golang https://go.dev/doc/install
- Install Kind
    - `go install [sigs.k8s.io/kind@v0.20.0](http://sigs.k8s.io/kind@v0.20.0)`
- Create a Kubernetes cluster with 3 workers and 1 control-plane
    - Create a Kubernetes Configuration file and name it as `kind.yaml`:
    
    ```yaml
    apiVersion: kind.x-k8s.io/v1alpha4
    kind: Cluster
    nodes:
    - role: worker
    - role: worker
    - role: worker
    - role: control-plane
    ```
    
    - Use Kind to create the Kubernetes cluster
        - `kind create cluster --config kind.yaml`
- Then you should be able to interact with the Kubernetes cluster with `kubectl`. (Try out the `k9s`!)

## Go Through the Installation Instructions from Your Operator

**[Note] This section provides you the example installation instructions. For this homework, please install the operator you picked**

**[Note] In some cases, the operator is built against an older version of Kubernetes. Thus you may need to ask Kind to deploy an older version of Kubernetes. To deploy a Kubernetes cluster of version v1.29.0, run `kind create cluster --config kind.yaml --image kindest/node:v1.29.0` You can find the list of Kind node images at https://hub.docker.com/r/kindest/node/tags**

Taking the zookeeper-operator as the example, the operator developers wrote down the detailed installation instructions [here](https://github.com/pravega/zookeeper-operator/tree/master?tab=readme-ov-file#install-the-operator)

To keep dependencies minimum, I followed the manual deployment steps. I pulled the operator source code to my machine, and ran the following command:

- `kubectl create -f config/crd/bases`
- `kubectl create -f config/rbac/all_ns_rbac.yaml`
- `kubectl create -f config/manager/manager.yaml`

### [optional] From the lecture, we know `config/crd/bases` defines the CustomResourceDefinition for the ZooKeeperCluster. But what is the second and third commands doing?

### [optional] In the lecture, Tyler always used `kubectl apply` to create the resources. In this guide provided by the zookeeper-operator, they use `kubectl create`, what is the difference between these two?

## Deploy the Managed Application (Custom Resource)

**[Note] This is the example for the zookeeper-operator. For this homework, please use your operator to deploy the application it manages.**

The zookeeper-operator developers also listed a number of examples for deploying the ZooKeeperCluster [here](https://github.com/pravega/zookeeper-operator/tree/master?tab=readme-ov-file#deploy-a-sample-zookeeper-cluster).

The only thing we need to do is to run the command `kubectl create -f zk.yaml`. Where the `zk.yaml` file contains the example CR:

```jsx
apiVersion: "zookeeper.pravega.io/v1beta1"
kind: "ZookeeperCluster"
metadata:
  name: "zookeeper"
spec:
  replicas: 3
```

Run `kubectl get all -l app=zookeeper` to get all resources related to the ZookeeperCluster.

## Validate the deployed application by collecting the system state

We will provide a program later to collect the system state and do some validation.