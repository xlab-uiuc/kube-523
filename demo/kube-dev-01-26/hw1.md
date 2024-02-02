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

We provide a program to collect the system state from the Kubernetes cluster under a specific namespace(default to `default` namespace), and check if the Kubernetes resources are healthy.

### Environment Setup

1. First, clone the Acto repo to your local disk: `git clone https://github.com/xlab-uiuc/acto.git`
2. Follow the setup steps described in the [Acto’s README](https://github.com/xlab-uiuc/acto?tab=readme-ov-file#prerequisites) to set up the environment.

### Execute the test program to collect the system state

1. Follow the steps in the previous sections to
    1. Create kind cluster
    2. Install the operator and CRD
    3. Deploy an example custom resource
2. Go into Acto’s top-level directory `cd acto`
3. Test the program with the Kubernetes’ control-plane namespace `python3 -m acto.cli.collect_system_state --namespace kube-system`
    
    This step works as a sanity check to validate your environment is correctly setup, and the `collect_system_state` program is working correctly. If there are some errors at this step, it means either the environment is not correctly setup, or there is a bug in the `collect_system_state` program. If you believe there is a bug in the program, please let us know on the piazza. 
    
4. Run the program to collect the system state `python3 -m acto.cli.collect_system_state`
    
    The `collect_system_state` program can be run with the following four arguments:
    
    ```yaml
    usage: collect_system_state.py [-h] [--output OUTPUT] [--kubeconfig KUBECONFIG] [--kubecontext KUBECONTEXT] [--namespace NAMESPACE]
    
    Collect the system state of a Kubernetes cluster under a namespace and dump it to a file. Check the health of the system state.
    
    options:
      -h, --help            show this help message and exit
      --output OUTPUT       Path to dump the system state to
      --kubeconfig KUBECONFIG
                            Path to the kubeconfig file
      --kubecontext KUBECONTEXT
                            Name of the Kubernetes context to use
      --namespace NAMESPACE
                            Namespace to collect the system state under
    ```
    
    All arguments are optional. Note that if your operator and the custom resource are deployed in a non-default namespace, please specify the namespace via the `--namespace` argument. The `--kubeconfig` and `--kubecontext` arguments are for the case where you used non-default kubeconfig and kubecontext to create the kind cluster. If you used `kind create cluster --config config.yaml` to create the cluster, `--kubeconfig` and `--kubecontext` are not needed.
    
    The `collect_system_state` performs some very simple health check to ensure the system resources are healthy. If it terminates with some error message, it means there are some problems with your deployed application. 
    If you believe it is the problem of the `collect_system_state` program, please let us know on piazza.
    
5. Name the dumped system state file to `{netid}-system-state.json`, ~~upload it to the shared Google Drive folder.~~ create a PR to this repo to upload the system state to the corresponding directory under the [operators](../../operators) dir ([example](https://github.com/xlab-uiuc/kube-523/pull/1)). Please first fork the repo and create a separate branch to create the PR.