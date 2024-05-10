# Lab1 Report 72 Alarms

netid: kw37

## Alarm-1
- Trial: trial-04-0003/001
- Type: Misoperation

### What happened
Acto sets `zookeeperRef.provided.initContainers[0]` to 
```yaml
- imagePullPolicy: Always
  name: mpeksqgthy
```
and the number of zookeeper replicas change from 3 to 2.

### Root Cause
When the image of the initContainer is not specified, the stateful set controller fails to restart the pod after the termination. As the result, the reconcilation stucks at restarting the first zookeeper pod it tries.

### Expected Behavior
If the image is not specified, the controller should simply bypass that container.

## Alarm-2
- Trial: trial-07-0000/003
- Type: Misoperation

### What happened
Acto sets `customSolrKubeOptions.podOptions.initContainers[0]` to
```yaml
- imagePullPolicy: Always
  name: etsqnsuhab
```
and the number of solr-cloud replicas change from 3 to 2.

### Root Cause
When the image of the initContainer is not specified, the stateful set controller fails to restart the pod after the termination. As the result, the reconcilation stucks at restarting the first solr-cloud pod it tries.

### Expected Behavior
If the image is not specified, the controller should simply bypass that container.

## Alarm-3
- Trial: trial-00-0026/006
- Type: Misoperation

### What happened
Acto sets `zookeeperRef.provided.containers[0]` to
```yaml
- name: gloilyyepf
  resources:
    claims:
    - name: INVALID_NAME
```
and the number of zookeeper replicas change from 3 to 2.

### Root Cause
When the image of the container is not specified, the stateful set controller fails to restart the pod after the termination. As the result, the reconcilation stucks at restarting the first zookeeper pod it tries.

### Expected Behavior
If the image is not specified, the controller should simply bypass that container or find a default image.

## Alarm-4
- Trial: trial-03-0050/001
- Type: Misoperation

### What happened
Acto sets `customSolrKubeOptions.podOptions.initContainers[0]` to
```yaml
- env:
- name: idiuvhrstn
    valueFrom:
    resourceFieldRef:
        divisor: 1000m
        resource: wkdtehvvdl
  name: hgbnaedxvb
```
and the number of solr-cloud replicas change from 3 to 2.

### Root Cause
When the image of the initContainer is not specified, the stateful set controller fails to restart the pod after the termination. As the result, the reconcilation stucks at restarting the first solr-cloud pod it tries.

### Expected Behavior
If the image is not specified, the controller should simply bypass that container.

## Alarm-5
- Trial: trial-01-0032/001
- Type: Misoperation

### What happened
Acto sets `customSolrKubeOptions.podOptions.sideContainers[0]` to
```yaml
- name: vpwttfhttl
  ports:
  - containerPort: 5
    name: INVALID_NAME
```
and the number of solr-cloud replicas change from 3 to 2.

### Root Cause
When the image of the sideContainer is not specified, the stateful set controller fails to restart the pod after the termination. As the result, the reconcilation stucks at restarting the first solr-cloud pod it tries.

### Expected Behavior
If the image is not specified, the controller should simply bypass that container.

## Alarm-6
- Trial: trial-06-0007/001
- Type: Misoperation

### What happened
Acto sets `zookeeperRef.provided.containers[0]` to
```yaml
- name: szurzaxbbn
  readinessProbe:
    exec:
    command:
    - invalid-command
```
and the number of zookeeper replicas change from 3 to 2.

### Root Cause
When the image of the container is not specified, the stateful set controller fails to restart the pod after the termination. As the result, the reconcilation stucks at restarting the first zookeeper pod it tries.

### Expected Behavior
If the image is not specified, the controller should simply bypass that container.

## Alarm-7
- Trial: trial-04-0051/002
- Type: Misoperation

### What happened
Acto sets `customSolrKubeOptions.podOptions.topologySpreadConstraints[0]` to
```yaml
- labelSelector:
  matchExpressions:
    - key: ACTOKEY
      operator: ACTOKEY
      values:
      - ACTOKEY
      - ACTOKEY
      - ACTOKEY
  matchLabels:
    ACTOKEY: ACTOKEY
  matchLabelKeys:
  - ACTOKEY
  - ACTOKEY
  maxSkew: 1
  minDomains: 4
  nodeAffinityPolicy: ACTOKEY
  nodeTaintsPolicy: ACTOKEY
  topologyKey: ACTOKEY
  whenUnsatisfiable: ACTOKEY
```
and the number of solr-cloud replicas change from 3 to 2.

### Root Cause
When `whenUnsatisfiable` is not set to `ScheduleAnyway`, the controller will not schedule the pod onto the node if the contraints are not fulfilled.

### Expected Behavior
The behavior is normal.

## Alarm-8
- Trial: trial-03-0039/001
- Type: Misoperation

### What happened
Acto sets `zookeeperRef.provided.volumns[0]` to
```yaml
- name: ivsiroqqlw
  scaleIO:
    gateway: jxfrdsrvsd
    secretRef:
      name: INVALID_NAME
    system: nkiyntpnka
```
and the number of zookeeper replicas change from 3 to 2.

### Root Cause
The pod cannot be restarted since it cannot find the gateway of scaleIO.

### Expected Behavior
The operator should reject the erroneous desired state.

## Alarm-9
- Trial: trial-06-0000/002
- Type: Misoperation

### What happened
Acto sets `zookeeperRef.provided.initContainers[0]` to
```yaml
- name: telvlljquw
  resizePolicy:
  - resourceName: ieapzxgtmk
    restartPolicy: INVALID_RESTART_POLICY
```
and the number of zookeeper replicas change from 3 to 2.

### Root Cause
When the image of the container is not specified, the stateful set controller fails to restart the pod after the termination. As the result, the reconcilation stucks at restarting the first zookeeper pod it tries.

### Expected Behavior
If the image is not specified, the controller should simply bypass that container.

## Alarm-10
- Trial: trial-01-0016/001
- Type: False alarm

### What happened
Acto sets `zookeeperRef.provided.persistence` to
```yaml
spec:
  resources:
    requests:
      ACTOKEY: 2000m
```
but it is not shown in the system state.

### Root Cause
This is actually a behavior from zookeeper operator. When the `volumeReclaimPolicy` is not equal to `Delete`, the operator simply returns `nil`.
```go
func (r *ZookeeperClusterReconciler) reconcileFinalizers(instance *zookeeperv1beta1.ZookeeperCluster) (err error) {
	if instance.Spec.Persistence != nil && instance.Spec.Persistence.VolumeReclaimPolicy != zookeeperv1beta1.VolumeReclaimPolicyDelete {
		return nil
	}
}
```

### Expected Behavior
The operator's behavior is correct.

## Alarm-11
- Trial: trial-03-0032/004
- Type: True alarm

### What happened
Acto removes the annotation with key ACTOKEY in `customSolrKubeOptions.statefulSetOptions.annotations` but it is not deleted in the system state.

### Root Cause
When the operator merges the original annotations and the new ones, it fails to remove the annotations that are not existed in the new configuration.
```go
func MergeLabelsOrAnnotations(base, additional map[string]string) map[string]string {
  // will not remove a key
	merged := DuplicateLabelsOrAnnotations(base)
	for k, v := range additional {
		if _, alreadyExists := merged[k]; !alreadyExists {
			merged[k] = v
		}
	}
	return merged
}
```

### Expected Behavior
The annotation should be removed from the system state.

## Alarm-12
- Trial: trial-0107-0050/001
- Type: False alarm

### What happened
Acto adds a new label with key ACTOKEY to `customSolrKubeOptions.nodeServiceOptions` but it is not shown in the system state.

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

## Alarm-13
- Trial: trial-01-0030/001
- Type: False alarm

### What happened
Acto adds a new annotation with key ACTOKEY to `zookeeperRef.provided.persistence` but it is not shown in the system state.

### Root Cause
This is actually a behavior from zookeeper operator. When the `volumeReclaimPolicy` is not equal to `Delete`, the operator simply returns `nil`.
```go
func (r *ZookeeperClusterReconciler) reconcileFinalizers(instance *zookeeperv1beta1.ZookeeperCluster) (err error) {
	if instance.Spec.Persistence != nil && instance.Spec.Persistence.VolumeReclaimPolicy != zookeeperv1beta1.VolumeReclaimPolicyDelete {
		return nil
	}
}
```

### Expected Behavior
The operator’s behavior is correct.

## Alarm-14
- Trial: trial-00-0045/003
- Type: False alarm

### What happened
Acto removes the element from `zookeeperRef.provided.zookeeperPodPolicy.imagePullsecrets` but it not updated in the system state.

### Root Cause
The operator will not update `ImagePullSecrets` if `ImagePullSecret` is not set.
```go
if zkSpec.Image.ImagePullSecret != "" {
    if len(zkSpec.ZookeeperPod.ImagePullSecrets) > 0 {
        zkCluster.Spec.Pod.ImagePullSecrets = append(zkCluster.Spec.Pod.ImagePullSecrets, corev1.LocalObjectReference{Name: zkSpec.Image.ImagePullSecret})
    } else {
        zkCluster.Spec.Pod.ImagePullSecrets = []corev1.LocalObjectReference{{Name: zkSpec.Image.ImagePullSecret}}
    }
}
```

### Expected Behavior
The operator's behavior is correct.

## Alarm-15
- Trial: trial-09-0036/002
- Type: Misoperation

### What happened
Acto changes the values of `customSolrKubeOptions.podOptions.podSecurityContext.{runAsGroup, runAsUser, supplementalGroups}` to 500. And the pod `test-cluster-solrcloud-2` crashed.

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

## Alarm-16
- Trial: trial-05-0030/006
- Type: Misoperation

### What happened
Acto removes the element in `customSolrKubeOptions.podOptions.tolerations` but the change is not shown in the system state.

### Root Cause
According to the [document](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/#example-use-cases), since the specified tolerations cannot be matched, the pod is not executed.

### Expected Behavior
The operator should reject erroneous desired states.

## Alarm-17
- Trial: trial-05-0025/001
- Type: Misoperation

### What happened
Acto sets `dataStorage.persistent` to 
```yaml
pvcTemplate:
  spec:
    resources:
    limits:
        ACTOKEY: 1000m
    requests:
        storage: 5Gi
  reclaimPolicy: Delete
```
but it is not shown in the system state.

### Root Cause
According to [this issue](https://github.com/kubernetes/enhancements/issues/661), Kubernetes does not support modification of pvcTemplate currently.

### Expected Behavior
The operator should specify this property as immutable in CRD.

## Alarm-18
- Trial: trial-01-0046/003
- Type: False alarm

### What happened
Acto removes the element from `zookeeperRef.provided.zookeeperPodPolicy.imagePullsecrets` but it not updated in the system state.

### Root Cause
The operator will not update `ImagePullSecrets` if `ImagePullSecret` is not set.
```go
if zkSpec.Image.ImagePullSecret != "" {
    if len(zkSpec.ZookeeperPod.ImagePullSecrets) > 0 {
        zkCluster.Spec.Pod.ImagePullSecrets = append(zkCluster.Spec.Pod.ImagePullSecrets, corev1.LocalObjectReference{Name: zkSpec.Image.ImagePullSecret})
    } else {
        zkCluster.Spec.Pod.ImagePullSecrets = []corev1.LocalObjectReference{{Name: zkSpec.Image.ImagePullSecret}}
    }
}
```

### Expected Behavior
The operator's behavior is correct.

## Alarm-19
- Trial: trial-08-0004/003
- Type: Misoperation

### What happened
Acto changes `dataStorage.persistent.pvcTemplate.spec.accessModes` from `InvalidAccessMode` to `ReadWriteMany`, but the change is not shown in the system state.

### Root Cause
According to [this issue](https://github.com/kubernetes/enhancements/issues/661), Kubernetes does not support modification of pvcTemplate currently.

### Expected Behavior
The operator should specify this property as immutable in CRD.

## Alarm-20
- Trial: trial-05-0006/006
- Type: True alarm

### What happened
Acto removes the label in `customSolrKubeOptions` but it is not updated in the system state.

### Root Cause
When the operator merges the new configuration, it fails to remove the label due to the defect in the merging logic.
```go
func MergeLabelsOrAnnotations(base, additional map[string]string) map[string]string {
	merged := DuplicateLabelsOrAnnotations(base)
	for k, v := range additional {
		if _, alreadyExists := merged[k]; !alreadyExists {
			merged[k] = v
		}
	}
	return merged
}
```

### Expected Behavior
The label should be removed correctly.

## Alarm-21
- Trial: trial-09-0037/001
- Type: Misoperation

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

## Alarm-22
- Trial: trial-01-0017/001
- Type: False alarm

### What happened
Acto sets `zookeeperRef.provided.persistence` to
```yaml
spec:
  resources:
    requests:
      ACTOKEY: 1000m
```
but it is not shown in the system state.

### Root Cause
This is actually a behavior from zookeeper operator. When the `volumeReclaimPolicy` is not equal to `Delete`, the operator simply returns `nil`.
```go
func (r *ZookeeperClusterReconciler) reconcileFinalizers(instance *zookeeperv1beta1.ZookeeperCluster) (err error) {
	if instance.Spec.Persistence != nil && instance.Spec.Persistence.VolumeReclaimPolicy != zookeeperv1beta1.VolumeReclaimPolicyDelete {
		return nil
	}
}
```

### Expected Behavior
The operator's behavior is correct.

## Alarm-23
- Trial: trial-06-0030/001
- Type: False alarm

### What happened
Acto adds a new label with key ACTOKEY to `customSolrKubeOptions.nodeServiceOptions` but it is not shown in the system state.

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
The operator's behavior is correct.

## Alarm-24
- Trial: trial-07-0026/002
- Type: True alarm

### What happened
Acto removes all the elements in `customSolrKubeOptions.podOptions.envVars` but it is not updated in the system.

### Root Cause
The operator simply appends the new envVars to the original one. Thus, it fails to remove the existing variables.
```go
if nil != customPodOptions {
		envVars = append(envVars, customPodOptions.EnvVariables...)
}
```

### Expected Behavior
The environment variables should be removed.

## Alarm-25
- Trial: trial-09-0021/009
- Type: Misoperation

### What happened
Acto changes the property `downwardAPI.resourceFieldRef` from 2000m to 4, but it is not updated in the system state.

### Root Cause
According to the [documentation](https://kubernetes.io/docs/concepts/workloads/pods/downward-api/#downwardapi-resourceFieldRef), the `resource` has a certain format and cannot be an arbitrary string.

### Expected Behavior
The operator should reject the erroneous desired state.

## Alarm-26
- Trial: trial-03-0009/006
- Type: True alarm

### What happened
Acto adds a new label with key ACTOKEY to `customSolrKubeOptions.commonServiceOptions` but it is not shown in the system state.

### Root Cause
When the operator merges the original annotations with the new ones, it fails to remove the annotations that are not existed in the new configuration.
```go
func MergeLabelsOrAnnotations(base, additional map[string]string) map[string]string {
	merged := DuplicateLabelsOrAnnotations(base)
	for k, v := range additional {
		if _, alreadyExists := merged[k]; !alreadyExists {
			merged[k] = v
		}
	}
	return merged
}
```

### Expected Behavior
The label should be removed correctly.

## Alarm-27
- Trial: trial-05-0061/001
- Type: Misoperation

### What happened
Acto adds a new annotation with key ACTOKEY to `pvcTemplate.metaData` but it is not shown in the system state.

### Root Cause
According to [this issue](https://github.com/kubernetes/enhancements/issues/661), Kubernetes does not support modification of pvcTemplate currently.

### Expected Behavior
The annotation should be specified as immutable.

## Alarm-28
- Trial: trial-05-0060/001
- Type: Misoperation

### What happened
Acto adds a new annotation with key ACTOKEY to `pvcTemplate.metaData` but it is not shown in the system state.

### Root Cause
According to [this issue](https://github.com/kubernetes/enhancements/issues/661), Kubernetes does not support modification of pvcTemplate currently.

### Expected Behavior
The annotation should be specified as immutable.

## Alarm-29
- Trial: trial-06-0045/002
- Type: True alarm

### What happened
Acto removes the elements in `customSolrKubeOptions.headlessServiceOptions` but the change is not shown in the system state.

### Root Cause
When the operator merges the original annotations with the new ones, it fails to remove the annotations that are not existed in the new configuration.
```go
func MergeLabelsOrAnnotations(base, additional map[string]string) map[string]string {
	merged := DuplicateLabelsOrAnnotations(base)
	for k, v := range additional {
		if _, alreadyExists := merged[k]; !alreadyExists {
			merged[k] = v
		}
	}
	return merged
}
```

### Expected Behavior
The labels and annotations should be removed correctly.

## Alarm-30
- Trial: trial-00-0023/002
- Type: True alarm

### What happened
Acto sets `solrAddressability.podPort` to 1 and the pod `test-cluster-solrcloud-0` crashed.

### Root Cause
The underlying container crashed with an error. Since it crashes every it tries to bind the port 1, the operator fails to reconcile.
```java
Caused by: java.io.IOException: Failed to bind to 0.0.0.0/0.0.0.0:1
```

### Expected Behavior
The pod should not crash.

## Alarm-31
- Trial: trial-04-0043/006
- Type: True alarm

### What happened
Acto sets `solrJavaMem` to ACTOKEY and the pod `test-cluster-solrcloud-2` crashed.

### Root Cause
The underlying container crashed with an error. Since it crashes every it tries to set JavaMem to ACTOKEY, the operator fails to reconcile.
```java
Caused by: java.lang.ClassNotFoundException: ACTOKEY
```

### Expected Behavior
The pod should not crash. One alternative is falling back to the default value.

## Alarm-32
- Trial: trial-01-0057/002
- Type: True alarm

### What happened
Acto sets `solrGCTune` to ACTOKEY and the pod `test-cluster-solrcloud-1` crashed.

### Root Cause
The underlying container crashed with an error. Since it crashes every it tries to set JavaMem to ACTOKEY, the operator fails to reconcile.
```java
Caused by: java.lang.ClassNotFoundException: ACTOKEY
```

### Expected Behavior
The pod should not crash. One alternative is falling back to the default value.

## Alarm-33
- Trial: trial-03-0012/003
- Type: False alarm

### What happened
Acto adds a new label with key ACTOKEY to `customSolrKubeOptions.ingressOptions` but it is not shown in the system state.

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

## Alarm-34
- Trial: trial-06-0031/001
- Type: False alarm

### What happened
Acto adds a new label with key ACTOKEY to `customSolrKubeOptions.nodeServiceOptions` but it is not shown in the system state.

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

## Alarm-35
- Trial: trial-02-0015/003
- Type: Misoperation

### What happened
Acto sets `customSolrKubeOptions.podOptions.initContainers[0]` to
```yaml
- name: rhfogslyib
  resources:
    limits:
      ACTOKEY: 2000m
```
but it is not shown in the system state.

### Root Cause
The operator fails to start the pod since there is no image provided in `initContainer`.

### Expected Behavior
The operator should still run the pod as without the initContainers set.

## Alarm-36
- Trial: trial-04-0021/001
- Type: False alarm

### What happened
Acto sets `zookeeper.provided.persistence` to
```yaml
annotations:
  ACTOKEY: ACTOKEY
```
but it is not shown in the system state.

### Root Cause
This is actually a behavior from zookeeper operator. When the `volumeReclaimPolicy` is not equal to `Delete`, the operator simply returns `nil`.
```go
func (r *ZookeeperClusterReconciler) reconcileFinalizers(instance *zookeeperv1beta1.ZookeeperCluster) (err error) {
	if instance.Spec.Persistence != nil && instance.Spec.Persistence.VolumeReclaimPolicy != zookeeperv1beta1.VolumeReclaimPolicyDelete {
		return nil
	}
}
```

### Expected Behavior
The operator's behavior is correct.

## Alarm-37
- Trial: trial-05-0024/001
- Type: Misoperation

### What happened
Acto adds a new resource `limits.ACTOKEY` to `dataStorage.pvcTemplate` but it is not shown in the system state.

### Root Cause
According to [this issue](https://github.com/kubernetes/enhancements/issues/661), Kubernetes does not support modification of pvcTemplate currently.

### Expected Behavior
The operator should mark the properity as immutable.

## Alarm-38
- Trial: trial-00-0022/001
- Type: True alarm

### What happened
Acto sets `solrZkOpts` to ACTOKEY and the pod `test-cluster-solrcloud-2` crashed.

### Root Cause
```java
Caused by: java.lang.ClassNotFoundException: ACTOKEY
```

### Expected Behavior
The operator should not crash. One alternative is falling back to the default value.

## Alarm-39
- Trial: trial-03-0001/002
- Type: False alarm

### What happened
Acto sets `zookeeperRef.provided` to
```yaml
zookeeperPodPolicy:
  nodeSelector:
    ACTOKEY: ACTOKEY
```
and it is not shown in the system state.

### Root Cause
The operator will not reconcile `zookeeperRef.provided` if the `connectionInfo` is set.
```go
func (r *SolrCloudReconciler) reconcileZk(ctx context.Context, logger logr.Logger, instance *solrv1beta1.SolrCloud, newStatus *solrv1beta1.SolrCloudStatus) error {
	zkRef := instance.Spec.ZookeeperRef

	if zkRef.ConnectionInfo != nil {
		newStatus.ZookeeperConnectionInfo = *zkRef.ConnectionInfo
	} else if zkRef.ProvidedZookeeper != nil {
    // reconcile provided
		pzk := zkRef.ProvidedZookeeper
  }
}
```

### Expected Behavior
The operator's behavior is correct.

## Alarm-40
- Trial: trial-02-0005/009
- Type: False alarm

### What happened
Acto sets `zookeeperRef.provided.persistence` to
```yaml
spec:
  resources:
    limits:
      ACTOKEY: 2000m
```
and it is not shown in the system state.

### Root Cause
This is actually a behavior from zookeeper operator. When the `volumeReclaimPolicy` is not equal to `Delete`, the operator simply returns `nil`.
```go
func (r *ZookeeperClusterReconciler) reconcileFinalizers(instance *zookeeperv1beta1.ZookeeperCluster) (err error) {
	if instance.Spec.Persistence != nil && instance.Spec.Persistence.VolumeReclaimPolicy != zookeeperv1beta1.VolumeReclaimPolicyDelete {
		return nil
	}
}
```

### Expected Behavior
The operator's behavior is correct.

## Alarm-41
- Trial: trial-01-0024/002
- Type: Misoperation

### What happened
Acto changes `zookeeperRef.provided.probes.livenessProbe.successThreshold` from 2 to 4 but it is not updated in the system state.

### Root Cause
The operator does not use the value read from the configuration.
```go
LivenessProbe: &v1.Probe{
  InitialDelaySeconds: z.Spec.Probes.LivenessProbe.InitialDelaySeconds,
  PeriodSeconds:       z.Spec.Probes.LivenessProbe.PeriodSeconds,
  TimeoutSeconds:      z.Spec.Probes.LivenessProbe.TimeoutSeconds,
  FailureThreshold:    z.Spec.Probes.LivenessProbe.FailureThreshold,

  ProbeHandler: v1.ProbeHandler{
    Exec: &v1.ExecAction{Command: []string{"zookeeperLive.sh"}},
  },
},
```

### Expected Behavior
The operator should simply disable that property.

## Alarm-42
- Trial: trial-09-0006/003
- Type: True alarm

### What happened
Acto removes an annotation from `customSolrKubeOptions.headlessService.Options` but the system state is not updated.

### Root Cause
When the operator merges the original annotations with the new ones, it fails to remove the annotations that are not existed in the new configuration.
```go
func MergeLabelsOrAnnotations(base, additional map[string]string) map[string]string {
  // will not remove a key
	merged := DuplicateLabelsOrAnnotations(base)
	for k, v := range additional {
		if _, alreadyExists := merged[k]; !alreadyExists {
			merged[k] = v
		}
	}
	return merged
}
```

### Expected Behavior
The operator should remove the annotation correctly.

## Alarm-43
- Trial: trial-03-0013/001
- Type: False alarm

### What happened
Acto adds a new label with key ACTOKEY to `customSolrKubeOptions.ingressOptions` but it is not shown in the system state.

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

## Alarm-44
- Trial: trial-01-0023/002
- Type: Misoperation

### What happened
Acto changes `zookeeperRef.provided.probes.livenessProbe.successThreshold` from 4 to 0 but it is not updated in the system state.

### Root Cause
The operator does not use the value read from the configuration.
```go
LivenessProbe: &v1.Probe{
  InitialDelaySeconds: z.Spec.Probes.LivenessProbe.InitialDelaySeconds,
  PeriodSeconds:       z.Spec.Probes.LivenessProbe.PeriodSeconds,
  TimeoutSeconds:      z.Spec.Probes.LivenessProbe.TimeoutSeconds,
  FailureThreshold:    z.Spec.Probes.LivenessProbe.FailureThreshold,

  ProbeHandler: v1.ProbeHandler{
    Exec: &v1.ExecAction{Command: []string{"zookeeperLive.sh"}},
  },
},
```

### Expected Behavior
The operator should simply disable that property.

## Alarm-45
- Trial: trial-00-0047/001
- Type: Misoperation

### What happened
Acto changes the values of `customSolrKubeOptions.podOptions.podSecurityContext.{runAsGroup, runAsUser, supplementalGroups}` to 1000. And the pod `test-cluster-solrcloud-2` crashed.

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

## Alarm-46
- Trial: trial-09-0017/009
- Type: False alarm

### What happened
Acto adds a new annotation with key ACTOKEY to `customSolrKubeOptions.nodeServiceOptions` but it is not shown in the system state.

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

## Alarm-47
- Trial: trial-09-0018/001
- Type: False alarm

### What happened
Acto adds a new annotation with key ACTOKEY to `customSolrKubeOptions.nodeServiceOptions` but it is not shown in the system state.

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

## Alarm-48
- Trial: trial-08-0006/005
- Type: Misoperation

### What happened
Acto adds a new volume in `zookeeperRef.provided.volumes` with the properties:
```yaml
- ephemeral:
    volumeClaimTemplate:
      metadata: {}
      spec:
        accessModes: []
        dataSource:
          apiGroup: ACTOKEY
          kind: ACTOKEY
          name: ACTOKEY
        dataSourceRef:
          apiGroup: ACTOKEY
          kind: ACTOKEY
          name: ACTOKEY
          namespace: ACTOKEY
        resources:
          claims: null
          limits:
            ACTOKEY: 5548379390u
          requests:
            ACTOKEY: 3
        selector:
          matchExpressions: []
          matchLabels:
            ACTOKEY: ACTOKEY
        storageClassName: ACTOKEY
        volumeMode: ACTOKEY
        volumeName: null
  name: ebcbulgnsw
```
The number of zookeeper replicas changes from 3 to 2 nd the change above is not shown in the system state.

### Root Cause
The operator fails to start the pod due to the misconfiguration. E.g., `volumeClaimTemplate.dataSource.kind` should be set to a valid data kind.

### Expected Behavior
The operator should reject the erroneous desired state.

## Alarm-49
- Trial: trial-05-0046/006
- Type: False alarm

### What happened
Acto adds a new label with key ACTOKEY to `customSolrKubeOptions.ingressOptions` but it is not shown in the system state.

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

## Alarm-50
- Trial: trial-02-0007/001
- Type: False alarm

### What happened
Acto sets `zookeeperRef.provided.persistence` to
```yaml
spec:
  resources:
    requests:
      ACTOKEY: 1000m
```
but it is not shown in the system state.

### Root Cause
This is actually a behavior from zookeeper operator. When the `volumeReclaimPolicy` is not equal to `Delete`, the operator simply returns `nil`.
```go
func (r *ZookeeperClusterReconciler) reconcileFinalizers(instance *zookeeperv1beta1.ZookeeperCluster) (err error) {
	if instance.Spec.Persistence != nil && instance.Spec.Persistence.VolumeReclaimPolicy != zookeeperv1beta1.VolumeReclaimPolicyDelete {
		return nil
	}
}
```

### Expected Behavior
The operator's behavior is correct. But it is also possible that the operator should set `VolumeReclaimPolicy` in zookeeper spec as the same in its own spec.


## Alarm-51
- Trial: trial-02-0041/003
- Type: True alarm

### What happened
Acto changes `zookeeperRef.provided.replicas` from 3 to 1000 and the pod `test-cluster-solrcloud-zookeeper-3` crashed.

### Root Cause
I actually could not reproduce the crash. But when the controller is trying to create the 96th replica, the status of that replica stays pending and the replica cannot be created. I think the root cause is the hardware limitations of the machine.

### Expected Behavior
The operator should not crash. But I think it is fine to stay in the pending state. When the resources are increases, the operator can keep creating more replicas.


## Alarm-52
- Trial: trial-05-0052/002
- Type: True alarm

### What happened
Acto removes the annotation with key ACTOKEY in `customSolrKubeOptions.statefulSetOptions` but it is not deleted in the system state.

### Root Cause
When the operator merges the original annotations with the new ones, it fails to remove the annotations that are not existed in the new configuration.
```go
func MergeLabelsOrAnnotations(base, additional map[string]string) map[string]string {
  // will not remove a key
	merged := DuplicateLabelsOrAnnotations(base)
	for k, v := range additional {
		if _, alreadyExists := merged[k]; !alreadyExists {
			merged[k] = v
		}
	}
	return merged
}
```

### Expected Behavior
The annotation should be removed from the system state.

## Alarm-53
- Trial: trial-00-0021/001
- Type: True alarm

### What happened
Acto sets `solrZkOpts` to ACTOKEY and the pod `test-cluster-solrcloud-2` crashed.

### Root Cause
```java
Caused by: java.lang.ClassNotFoundException: ACTOKEY
```

### Expected Behavior
The operator should not crash. One alternative is falling back to the default value.

## Alarm-54
- Trial: trial-00-0000/009
- Type: False alarm

### What happened
Acto sets `zookeeperRef.provided.containers[0]` to
```yaml
- env:
  - name: vyzdsydfxp
    valueFrom:
      resourceFieldRef:
        divisor: '4'
        resource: jvxdvyniiz
  name: mmsmwqjvys
```
but the change is not shown in the system state.

### Root Cause
The operator will not reconcile `zookeeperRef.provided` if the `connectionInfo` is set.
```go
func (r *SolrCloudReconciler) reconcileZk(ctx context.Context, logger logr.Logger, instance *solrv1beta1.SolrCloud, newStatus *solrv1beta1.SolrCloudStatus) error {
	zkRef := instance.Spec.ZookeeperRef

	if zkRef.ConnectionInfo != nil {
		newStatus.ZookeeperConnectionInfo = *zkRef.ConnectionInfo
	} else if zkRef.ProvidedZookeeper != nil {
    // reconcile provided
		pzk := zkRef.ProvidedZookeeper
  }
}
```

### Expected Behavior
The operator's behavior is correct.

## Alarm-55
- Trial: trial-05-0049/002
- Type: True alarm

### What happened
Acto removes all the elements in `customSolrKubeOptions.commonServiceOptions` but the change is not shown in the system state.

### Root Cause
When the operator merges the original annotations with the new ones, it fails to remove the annotations that are not existed in the new configuration. Same for the labels.
```go
func MergeLabelsOrAnnotations(base, additional map[string]string) map[string]string {
  // will not remove a key
	merged := DuplicateLabelsOrAnnotations(base)
	for k, v := range additional {
		if _, alreadyExists := merged[k]; !alreadyExists {
			merged[k] = v
		}
	}
	return merged
}
```
### Expected Behavior
The elements should be removed correctly.

## Alarm-56
- Trial: trial-04-0022/001
- Type: False alarm

### What happened
Acto sets `zookeeperRef.provided.persistence` to 
```yaml
annotations:
  ACTOKEY: ACTOKEY
```
but it is not shown in the system state.

### Root Cause
This is actually a behavior from zookeeper operator. When the `volumeReclaimPolicy` is not equal to `Delete`, the operator simply returns `nil`.
```go
func (r *ZookeeperClusterReconciler) reconcileFinalizers(instance *zookeeperv1beta1.ZookeeperCluster) (err error) {
	if instance.Spec.Persistence != nil && instance.Spec.Persistence.VolumeReclaimPolicy != zookeeperv1beta1.VolumeReclaimPolicyDelete {
		return nil
	}
}
```

### Expected Behavior
The operator's behavior is correct. But in my opinion the operator should set `VolumeReclaimPolicy` of the zookeeper spec as the same of itself.

## Alarm-57
- Trial: trial-06-0003/002
- Type: True alarm

### What happened
Acto removes all the elements in `customSolrKubeOptions.commonServiceOptions` but the change is not shown in the system state.

### Root Cause
When the operator merges the original annotations with the new ones, it fails to remove the annotations that are not existed in the new configuration. Same for the labels.
```go
func MergeLabelsOrAnnotations(base, additional map[string]string) map[string]string {
  // will not remove a key
	merged := DuplicateLabelsOrAnnotations(base)
	for k, v := range additional {
		if _, alreadyExists := merged[k]; !alreadyExists {
			merged[k] = v
		}
	}
	return merged
}
```
### Expected Behavior
The elements should be removed correctly.

## Alarm-58
- Trial: trial-05-0010/005
- Type: Misoperation

### What happened
Acto adds a new label with key ACTOKEY to `customSolrKubeOptions.podOptions` but it is now shown in the system state.

### Root Cause
Based on the log of the controller,
```log
INFO    Will not create/update the StatefulSet because the zookeeperConnectionString has no host
```
the pods are not updated due to the erroneous desired state.

### Expected Behavior
The operator should reject the erroneous desired state at the first place. So the misconfigured properties are not passed to the stateful set controller.

## Alarm-59
- Trial: trial-05-0039/001
- Type: False alarm

### What happened
Acto sets `zookeeperRef.provided.persistence` but it is not shown in the system state.

### Root Cause
This is actually a behavior from zookeeper operator. When the `volumeReclaimPolicy` is not equal to `Delete`, the operator simply returns `nil`.
```go
func (r *ZookeeperClusterReconciler) reconcileFinalizers(instance *zookeeperv1beta1.ZookeeperCluster) (err error) {
	if instance.Spec.Persistence != nil && instance.Spec.Persistence.VolumeReclaimPolicy != zookeeperv1beta1.VolumeReclaimPolicyDelete {
		return nil
	}
}
```

### Expected Behavior
The operator's behavior is correct. But in my opinion the operator should set `VolumeReclaimPolicy` of the zookeeper spec as the same of itself.

## Alarm-60
- Trial: trial-01-0059/002
- Type: False alarm

### What happened
Acto changes `dataStorage.ephemeral.emptyDir.sizeLimit` from 1000m to '0.5' but this change is not shown in the system state.

### Root Cause
The operator will not reconcile the ephemeral storage if the persistent storage is specified.
```go
if solrCloud.UsesPersistentStorage() {
  // set persistent storage
  pvcs = []corev1.PersistentVolumeClaim{
    {
      ObjectMeta: metav1.ObjectMeta{
        Name:        pvc.ObjectMeta.Name,
        Labels:      pvc.ObjectMeta.Labels,
        Annotations: pvc.ObjectMeta.Annotations,
      },
      Spec: pvc.Spec,
    },
  }
} else {
  // set ephemeral storage
  ephemeralVolume := corev1.Volume{
    Name:         solrDataVolumeName,
    VolumeSource: corev1.VolumeSource{},
  }
}
```

### Expected Behavior
The operator's behavior is correct.

## Alarm-61
- Trial: trial-02-0040/004
- Type: True alarm

### What happened
Acto changes `zookeeperRef.provided.replicas` from 1 to 3 and the pod `test-cluster-solrcloud-zookeeper-1` crashed.

### Root Cause
When the number of zookeeper replicas is 1 (from the previous generation), the operator fails to bring any solr-cloud pods to the ready state. As a result, the operator cannot reconcile due to the property `maxPodsUnavailable`.
```go
// this is always failed and the operator will keep retrying later
additionalPodsToUpdate, retryLater =
				util.DeterminePodsSafeToUpdate(instance, int(*statefulSet.Spec.Replicas), outOfDatePods, state, availableUpdatedPodCount, updateLogger)
if !retryLater {
  podsToUpdate = append(podsToUpdate, additionalPodsToUpdate...)
}
```

### Expected Behavior
THe operator should bring all the solr-cloud pods to the ready states even though there is only one zookeeper replica.

## Alarm-62
- Trial: trial-04-0024/004
- Type: Misoperation

### What happened
Actos adds the metadata to `dataStorage.persistent.pvcTemplate` but it is not shown in the system state.
```yaml
metadata:
  annotations:
    ACTOKEY: ACTOKEY
```

### Root Cause
According to [this issue](https://github.com/kubernetes/enhancements/issues/661), Kubernetes does not support modification of pvcTemplate currently.

### Expected Behavior
The operator should specify this property as immutable in CRD.

## Alarm-63
- Trial: trial-08-0003/002
- Type: True alarm

### What happened
Acto removes the label in `customSolrKubeOptions.statefulSetOptions` but it is not deleted in the system state.

### Root Cause
When the operator merges the original annotations and the new ones, it fails to remove the annotations that are not existed in the new configuration.
```go
func MergeLabelsOrAnnotations(base, additional map[string]string) map[string]string {
  // will not remove a key
	merged := DuplicateLabelsOrAnnotations(base)
	for k, v := range additional {
		if _, alreadyExists := merged[k]; !alreadyExists {
			merged[k] = v
		}
	}
	return merged
}
```

### Expected Behavior
The annotation should be removed from the system state.

## Alarm-64
- Trial: trial-01-0048/006
- Type: False alarm

### What happened
Acto adds a new annotation with key ACTOKEY to `customSolrKubeOptions.nodeServiceOptions` but it is not shown in the system state.

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

## Alarm-65
- Trial: trial-07-0030/001
- Type: False alarm

### What happened
Acto adds a new label with key ACTOKEY to `customSolrKubeOptions.ingressOptions` but it is not shown in the system state.

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

## Alarm-66
- Trial: trial-03-0041/004
- Type: Misoperation

### What happened
Acto sets `zookeeperRef.connectionInfo.externalConnectionString` to ACTOKEY and the pod `test-cluster-solrcloud-2` crashed.

### Root Cause
The underlying container raises the following error when it tries to connect to the zookeeper cluster.
```java
java.lang.IllegalArgumentException: Unable to canonicalize address ACTOKEY
```
and the operator cannot reconcile the pod to the ready state.

### Expected Behavior
The operator should reject the erroneous desired state.

## Alarm-67
- Trial: trial-03-0010/003
- Type: True alarm

### What happened
Acto removes the annotation in `customSolrKubeOptions.configMapOptions` but the change is not shown in the system state.

### Root Cause
When the operator merges the original annotations and the new ones, it fails to remove the annotations that are not existed in the new configuration.
```go
func MergeLabelsOrAnnotations(base, additional map[string]string) map[string]string {
  // will not remove a key
	merged := DuplicateLabelsOrAnnotations(base)
	for k, v := range additional {
		if _, alreadyExists := merged[k]; !alreadyExists {
			merged[k] = v
		}
	}
	return merged
}
```

### Expected Behavior
The annotation should be removed from the system state.

## Alarm-68
- Trial: trial-00-0024/001
- Type: Misoperation

### What happened
Acto sets `solrAddressability.podPort` to 2 and the pod `test-cluster-solrcloud-2` crashed.

### Root Cause
The underlying container crashed with an error. Since it crashes every it tries to bind the port 2, the operator fails to reconcile.
```java
Caused by: java.io.IOException: Failed to bind to 0.0.0.0/0.0.0.0:2
```

### Expected Behavior
The pod should not crash.

## Alarm-69
- Trial: trial-05-0047/001
- Type: False alarm

### What happened
Acto adds a new label with key ACTOKEY to `customSolrKubeOptions.ingressOptions` but it is not shown in the system state.

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

## Alarm-70
- Trial: trial-06-0050/001
- Type: Misoperation

### What happened
Actos adds the metadata to `dataStorage.persistent.pvcTemplate` but it is not shown in the system state.
```yaml
metadata:
  labels:
    ACTOKEY: ACTOKEY
```

### Root Cause
According to [this issue](https://github.com/kubernetes/enhancements/issues/661), Kubernetes does not support modification of pvcTemplate currently.

### Expected Behavior
The operator should specify this property as immutable in CRD.

## Alarm-71
- Trial: trial-07-0047/001
- Type: False alarm

### What happened
Acto adds a new annotation with key ACTOKEY to `customSolrKubeOptions.ingressOptions` but it is not shown in the system state.

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

## Alarm-72
- Trial: trial-02-0038/002
- Type: True alarm

### What happened
Acto changes `zookeeperRef.provided.persistence.spec.accessModes` from `InvalidAccessMode` to `ReadWriteMany` but the change is not shown in the system state.

### Root Cause
When the accessModes is `InvalidAccessMode` (from the previous generation), the operator fails to bring any solr-cloud pods to the ready state. As a result, the operator cannot reconcile due to the property `maxPodsUnavailable`.
```go
// this is always failed and the operator will keep retrying later
additionalPodsToUpdate, retryLater =
				util.DeterminePodsSafeToUpdate(instance, int(*statefulSet.Spec.Replicas), outOfDatePods, state, availableUpdatedPodCount, updateLogger)
if !retryLater {
  podsToUpdate = append(podsToUpdate, additionalPodsToUpdate...)
}
```

### Expected Behavior
The operator should bring all the solr-cloud pods to the ready state even though the accessMode is not set correctly. Alternatively, the operator should reject the erroneous desired state at the first place.

