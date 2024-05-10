# Lab1 Report

netid: kw37


## trial-07-0059/001
Type: True alarm

### What happened
Acto adds a new label with key ACTOKEY to `pvcTemplate.metaData` but it is not shown in the system state.

### Root Cause
According to [this issue](https://github.com/kubernetes/enhancements/issues/661), Kubernetes does not support modification of pvcTemplate currently.

### Expected Behavior
The label should be added to the metadata.
	

## trial-08-0020/001
Type: False alarm

### What happened
Acto adds a new label with key ACTOKEY to `customSolrKubeOptions.nodeServiceOptions.annotations` but it is not shown in the system state.

### Root Cause
The operator will not reconcile the state of NodeService if solrAddressibility.External is not configured correctly. 

```go
if instance.UsesIndividualNodeServices() { // true only when solrAddressibility.External is configured
    for _, nodeName := range solrNodeNames {
        err, ip := r.reconcileNodeService(ctx, logger, instance, nodeName) // reconcile the state of NodeService
    }
}
```

### Expected Behavior
The operator’s behavior is correct.


## trial-03-0033/001
Type: False alarm

### What happened
Acto adds a new label with key ACTOKEY to `customSolrKubeOptions.ingressOptions.labels` but it is not shown in the system state.

### Root Cause
The operator will not reconcile the state of Ingress if `solrAddressibility.External.Method` is not set to `Ingress`.


```go
if extAddressabilityOpts != nil && extAddressabilityOpts.Method == solrv1beta1.Ingress {
    // Generate Ingress
    ingress := util.GenerateIngress(instance, solrNodeNames)
}
```

### Expected Behavior
The operator’s behavior is correct.


## trial-00-0006/001
Type: True alarm

### What happened
Acto changes the values of `customSolrKubeOptions.podOptions.podSecurityContext.{runAsGroup, runAsUser, supplementalGroups}` to 0. And the pod `test-cluster-solrcloud-2` crashed.

### Root Cause
The operator will setup the containers with a non-existed user, which directly crashes the command. 

```go
setupCommands = append(setupCommands, fmt.Sprintf(
    "(%s || chown -R %d:%d %s)",
    testDirCommand,
    solrUser, // this may crash the command!!
    solrFSGroup,
    volumeMount.MountPath)
)
```

### Expected Behavior
The operator should not crash. An alternative is to run as the default user/group if the uid/gid does not exist. 

## trial-08-0030/001
Type: True alarm

### What happened
Acto adds a new item with key ACTOKEY to `zookeeperRef.provided.persistence.spec.resources.limits`, but it is not shown in the system state.

### Root Cause


### Expected Behavior