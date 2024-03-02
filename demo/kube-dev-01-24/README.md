# Kubernetes Tutorial

## Learning Outcome

After this tutorial, you will learn
1. Basic concepts in Kubernetes.
2. How to deploy an application (ZooKeeper) on Kubernetes using Pod and PVC
3. How to deploy a replicated application(ZooKeeper ensemble) on Kubernetes using StatefulSet.

## **Setting up local Kubernetes cluster**

We will first go through a tutorial to set up a Kubernetes cluster on a local machine.

Kind is a tool built by the Kubernetes community for local development and easy testing of Kubernetes.
We will use it to create a local Kubernetes cluster to play with.

**"All problems in computer science can be solved by another level of indirection." — David J. Wheeler**

What Kind does is to create Kubernetes "node" containers that behave like a machine in a cluster. Each node runs a Kubernetes daemon and joins together to form a Kubernetes cluster. 

- Install [Golang](https://go.dev/doc/install)
- Install [Docker](https://docs.docker.com/engine/install/)
- Install Kind
    - `go install sigs.k8s.io/kind@v0.20.0`
- Create a Kubernetes cluster with 3 workers and 1 control-plane
    - Create the following Kubernetes Configuration file `kind.yaml`:
    
    ```yaml
    apiVersion: kind.x-k8s.io/v1alpha4
    kind: Cluster
    nodes:
    - role: worker
    - role: worker
    - role: worker
    - role: control-plane
    ```
    
    - Use Kind to create the Kubernetes cluster with the configuration
        - `kind create cluster --config kind.yaml`

### **Kubectl tool — Interacting with Kubernetes**

Next, we will learn the command line tool to interact with the Kubernetes cluster

- Install [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
- Inspect the current Pod resource: `kubectl get pods -A -o wide`
    - We will be able to see all the Pods currently running in the cluster. Since we haven't deployed anything, currently there are only the Kubernetes core controllers running.

## **Pod — Deploying Containers on Kubernetes**

OK, now we have a Kubernetes cluster. Let’s try to ask Kubernetes to deploy and manage an application for us.

### State-Reconciliation Principle

Remember in Kubernetes, there is a centralized data store(etcd) that stores the desired state of all resources.
The controllers in Kubernetes monitor the resources' specifications stored in the etcd, and reconcile the system state to match the desired state.

Kubernetes has many native resources, and Pod is the smallest unit of computing resources.
A Pod can be considered as a collection of co-located containers.
When we create a Pod specification in etcd, the Pod controller will realize that the current system state (system containers) does not match the desired state in etcd. Specifically, there is one Pod in the etcd, but there is currently no container corresponding to that.
Then the Pod controller creates a new container according to Pod specification so that the system state matches the desired state.

Another important resource in Kubernetes is PersistentVolumeClaim(PVC).
The PersistentVolumeClaim controller will create volumes that can be used as storage according to the PVC specification.

### **Writing the Pod/PersistentVolumeClaim Resource Spec to Run a Standalone ZooKeeper**

Let’s take the ZooKeeper as an example, and deploy it on Kubernetes using the Pod and PVC resources.

We can describe the Pod resources as YAML files.

In the following YAML file, it specifies two resources required to deploy the standalone ZooKeeper: the Pod resource to deploy the ZooKeeper container, and the PersistentVolumeClaim to hold the data for the ZooKeeper.

You can see in the Pod spec, it references the PersistentVolumeClaim to use it as a volume (zk-data), and that volume gets mounted into the zk container on the path `/var/lib/zookeeper`

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: zk-0
spec:
  containers:
  - name: zk
    image: "registry.k8s.io/kubernetes-zookeeper:1.0-3.4.10"
    ports:
    - containerPort: 2181
      name: client
    - containerPort: 2888
      name: server
    - containerPort: 3888
      name: leader-election
    command:
    - sh
    - -c
    - "start-zookeeper \
      --servers=1 \
      --data_dir=/var/lib/zookeeper/data \
      --data_log_dir=/var/lib/zookeeper/data/log \
      --conf_dir=/opt/zookeeper/conf \
      --client_port=2181 \
      --election_port=3888 \
      --server_port=2888 \
      --tick_time=2000 \
      --init_limit=10 \
      --sync_limit=5 \
      --heap=512M \
      --max_client_cnxns=60 \
      --snap_retain_count=3 \
      --purge_interval=12 \
      --max_session_timeout=40000 \
      --min_session_timeout=4000 \
      --log_level=INFO"
    volumeMounts:
    - name: datadir
      mountPath: /var/lib/zookeeper
  volumes:
  - name: datadir
    persistentVolumeClaim:
      claimName: zk-data
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: zk-data
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

To create this Pod and PVC in Kubernetes, use `kubectl`:
```kubectl apply -f standalone/pvc.yaml```
```kubectl apply -f standalone/zk-pod.yaml```

Note: how do I know what properties to write in these YAML files?
You can find the resource definitions from the official Kubernetes API reference

[**Pod**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.25/#pod-v1-core)

[**PVC**](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.25/#persistentvolumeclaim-v1-core)

### Try out this deployed application [optional]

This ZooKeeper Pod exposes client service on port 2181. You can try to establish a client connection on that port to use the service.

Or you can try to use the ZooKeeper CLI inside the ZooKeeper container.

To run an exec command inside the ZooKeeper container, you can make use of the `kubectl` CLI, by running `kubectl exec {POD} -- {CMD}`

To perform a write using the ZooKeeper CLI, run `kubectl exec zk-0 -- zkCli.sh create /hello world`

## **Deploying 3-node ZooKeeper ensemble**

### Manually creating 3 Pods, and joining them as an ensemble

We can manually replicate the resource definitions we wrote for the Pod and PVC three times.
You can find the resource definitions in the repo: [3-node/zk-pods.yaml](3-node/zk-pods.yaml) [3-node/pvc.yaml](3-node/pvc.yaml)

Pay attention to the changed fields in the Pods and PVCs.

You will notice that we added an additional Service resource when creating 3 Pods.
This Service resource provides an FQDN for each Pod we create so that they know how to communicate with each other and form an ensemble.

### Introducing StatefulSet

Manually creating 3 Pods requires a lot of manual effort, and does not scale well if you want more replicas.
Let's look at another resource, `StatefulSet``, defined by Kubernetes, which can simplify the management process.

The StatefulSet resource allows templating the Pod resources and PVC resources,
and automatically creating multiple Pods and PVCs according to the specified replica number.

Let's try to deploy the same 3-replica ZooKeeper ensemble with the StatefulSet resource.
You can find the StatefulSet resource definition [stateful_set/stateful_set.yaml](stateful_set/stateful_set.yaml).

Run `kubectl apply -f stateful_set/stateful_set.yaml` to create the StatefulSet resource in etcd.
And run `kubectl get pods` to wait for all Pods to get ready.

After all Pods are fully started, let’s test out this ZooKeeper ensemble we just deployed.

Since it is a distributed system for replication data, let's try to write a data on the zk-0, and read the data on zk-1.

To create a path `/hello` with data `world` on `zk-0`, run:
`kubectl exec zk-0 -- zkCli.sh create /hello world`

After the create is completed, try to read the data from the path `/hello`,
and you will see the command returns `world` along with a bunch of metadata.
`kubectl exec zk-1 -- zkCli.sh get /hello`

## If you want to explore more, there are some optional tasks for you to try:
- Creating a Service resource in Kubernetes to expose this application as a service
- What if we want to scale a 3-replica existing ZooKeeper ensemble to 5 replicas.
- Deploy the ZooKeeper cluster by using the [zookeeper-operator](https://github.com/pravega/zookeeper-operator)
