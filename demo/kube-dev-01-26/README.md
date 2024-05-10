# Kubernetes Operator Tutorial

## Recap

We [learned to use the Kubernetes built-in resources to deploy the ZooKeeper ensemble](https://github.com/xlab-uiuc/kube-523/blob/main/demo/kube-dev-01-24/README.md). We used Pod resources to deploy ZooKeeper container, and PVC resources to deploy storage. We learned that Kubernetes provides the StatefulSet resource, creating a layer of abstraction over Pods and PVCs.

Remember the State-Reconciliation Principle, where the controller reconciles the system state to match the resources declared in the etcd. For the Pod controller, the **system state** managed by the Pod controller is the containers running in the system. For the PVC controller, the system state is the volumes on the disk.

**So what is the system state of StatefulSet?**

The StatefulSet manages Pod resources and PVC resources inside the etcd. It makes sure that there are the exact number of Pods and PVCs matching the desired number of replicas. If we try to manually delete one Pod, the StatefulSet will automatically create a new Pod.

## Managing ZooKeeper Ensemble

What does it mean to manage a system? Don’t we just run it? 

Back to the ZooKeeper ensemble example; we need to manage the ZooKeeper system after we deploy it. What does it mean to manage the ZooKeeper?

What if I found out that my user traffic is getting bigger, and I want to allocate more resources to each ZooKeeper Pod?

What if I want more reliability, and I want to add two more replicas to the ZooKeeper ensemble?

There are a lot of management operations to be done to maintain the ZooKeeper ensemble in production.

Let’s try with the example of adding two replicas.

### Adding two additional replicas to the ZooKeeper ensemble

The StatefulSet resource allows us to change the `replicas` property to add more replicas. Is scaling up the ZooKeeper ensemble as simple as changing the `replicas` property in the StatefulSet?

Let’s try to change an existing StatefulSet deployed with [prev_stateful_set.yaml](prev_stateful_set.yaml).

With an existing statefulSet defined by, we can modify the file to downscale to 1. Here, we changed the `replicas` property and the command line argument of the ZooKeeper container.

Run `kubectl apply -f curr_stateful_set.yaml`

We can see that the StatefulSet controller first creates two new ZooKeeper Pods, both with the new configuration of 3 replicas. So they will contain a membership list of zk-0,1,2. Note that currently the zk-0 still has the old membership list, where it is the only node. Then the StatefulSet controller restarts the zk-0 Pod with the new configuration.

**What could go wrong here?**

The two newly added zk nodes may form a quorum themselves, while the zk-0 still thinks it is the leader. This creates a split-brain scenario.

So what should be the correct procedure to scale a ZooKeeper ensemble?

You can checkout the official ZooKeeper guide on dynamically changing the ensemble size: https://zookeeper.apache.org/doc/r3.5.3-beta/zookeeperReconfig.html#sc_reconfig_modifying

To dynamically add two new replicas to the ZooKeeper ensemble, the two replicas need to be create with special initial membership list: the existing replicas + itself. One should not add two new participants at the same time. After the two new replicas are booted, they will contact the current leader to sync the membership list. In this way, we don’t even need to restart the leader and cause unavailability.

This process shows a lot of challenges in managing ZooKeeper on Kubernetes. There is a lot of manual effort involved, and as we know when humans are extremely unreliable. It also requires very deep domain-specific knowledge. To safely scale up the ZooKeeper ensemble, one needs to understand ZooKeeper very deeply.

## Extending Kubernetes

Can we have another resource in Kubernetes presenting the desired state of the ZooKeeper ensemble, and have a zookeeper-controller to reconcile the system state to match the desired state?

This is where the extensibility of Kubernetes shines and the concept of operator comes in. To abstract out all these tedious, tricky operations, we can extend the Kubernetes interface, to define a new Resource specifically for ZooKeeper, and add a custom controller to Kubernetes to reconcile the ZooKeeper Resource. The zookeeper-controller encodes all the domain-specific knowledge of how to manage ZooKeeper ensembles; and manages the Kubernetes built-in resources, e.g., StatefulSet, Pod, Service, PVC in a composable manner.

The extended new resource is called Custom Resource. Just as Pods, StatefulSet have defined interfaces, we also need to define an interface for the Custom Resource. The interface definition is called CustomResourceDefinition.

The custom controller is usually termed “operator” in Kubernetes. Since most of you have already picked an operator, you probably noticed a large number of open-source operations.

## Operator Definition

If you read the official documentation from Kubernetes, you will find it rather short and leaves readers a lot of space for imagination.

- Operators are software extensions to Kubernetes that make use of [custom resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) to manage applications and their components. Operators follow Kubernetes principles, notably the [control loop](https://kubernetes.io/docs/concepts/architecture/controller).
    
    

To us, operator is basically a custom controller managing an application on top of Kubernetes.

## zookeeper-operator

Let’s take a look at the zookeeper-operator. https://github.com/pravega/zookeeper-operator 

First, let’s take a look at the CustomResourceDefinition managed by the zookeeper-operator, and see what features does this zookeeper-operator support: https://github.com/pravega/zookeeper-operator/blob/master/config/crd/bases/zookeeper.pravega.io_zookeeperclusters.yaml

### Install the ZookeeperCluster CRD and the zookeeper-operator in your cluster

Follow the steps described here: https://github.com/pravega/zookeeper-operator/tree/master?tab=readme-ov-file#install-the-operator

Then, let’s try to deploy a 3-node ZooKeeper cluster using this CR.

Create a yaml file describing the ZookeeperCluster resource like [this one](zk.yaml),
and run `kubectl apply -f zk.yaml`:

```yaml
apiVersion: "zookeeper.pravega.io/v1beta1"
kind: "ZookeeperCluster"
metadata:
  name: "zookeeper"
spec:
  replicas: 3
```

Then monitor the system state using `kubectl` or `k9s` and wait for the system to boot up. You should be able to see three new ZK pods getting created.

Then, modify the ZookeeperCluster resource by changing the replicas from `3` to `5` and monitor the scaling process:
`kubectl apply -f zk-5.yaml`

```yaml
apiVersion: "zookeeper.pravega.io/v1beta1"
kind: "ZookeeperCluster"
metadata:
  name: "zookeeper"
spec:
  replicas: 5
```

**Now try this with the operator you picked!**
