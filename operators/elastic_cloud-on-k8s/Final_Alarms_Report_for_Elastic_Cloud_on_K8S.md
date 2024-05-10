# Final Alarms Report for Elastic Cloud on K8S

netId: renzhou2

## Overview

### All Alarms

| Alarm    | Name               | Category     |
| -------- | ------------------ | ------------ |
| Alarm 1  | trial-00-0001/0001 | bug          |
| Alarm 2  | trial-00-0003/0008 | misoperation |
| Alarm 3  | trial-00-0004/0003 | misoperation |
| Alarm 4  | trial-00-0005/0002 | misoperation |
| Alarm 5  | trial-00-0006/0003 | misoperation |
| Alarm 6  | trial-00-0010/0009 | misoperation |
| Alarm 7  | trial-00-0011/0003 | misoperation |
| Alarm 8  | trial-00-0014/0002 | false alarm  |
| Alarm 9  | trial-00-0016/0002 | misoperation |
| Alarm 10 | trial-00-0017/0003 | misoperation |
| Alarm 11 | trial-00-0020/0002 | false alarm  |
| Alarm 12 | trial-00-0021/0003 | false alarm  |
| Alarm 13 | trial-01-0006/0002 | false alarm  |
| Alarm 14 | trial-01-0007/0003 | false alarm  |
| Alarm 15 | trial-01-0011/0004 | misoperation |
| Alarm 16 | trial-01-0020/0003 | bug          |
| Alarm 17 | trial-02-0000/0003 | false alarm  |
| Alarm 18 | trial-02-0001/0003 | false alarm  |
| Alarm 19 | trial-02-0005/0001 | misoperation |
| Alarm 20 | trial-02-0006/0001 | misoperation |
| Alarm 21 | trial-02-0008/0001 | misoperation |
| Alarm 22 | trial-02-0009/0001 | misoperation |
| Alarm 23 | trial-02-0015/0010 | false alarm  |
| Alarm 24 | trial-02-0016/0003 | false alarm  |
| Alarm 25 | trial-03-0002/0007 | bug          |
| Alarm 26 | trial-03-0003/0001 | bug          |
| Alarm 27 | trial-03-0005/0001 | misoperation |
| Alarm 28 | trial-03-0010/0002 | false alarm  |
| Alarm 29 | trial-03-0011/0003 | false alarm  |
| Alarm 30 | trial-03-0016/0008 | misoperation |
| Alarm 31 | trial-03-0017/0001 | misoperation |

### Statistical data:

| category  | bug  | misoperation | false alarm | total |
| --------- | ---- | ------------ | ----------- | ----- |
| **count** | 4    | 16           | 11          | 31    |



## Alarm 1

**name**: trial-00-0001/0001

**type**: bug

### What happened
Acto tried to add `ACTOKEY` into path `spec.http.service.metadata.annotations`, however the system state did not add this value.


### Root Cause
```go
UpdateReconciled: func() {
    // override annotations and labels with expected ones
    // don't remove additional values in reconciled that may have been defaulted or
    // manually set by the user on the existing resource
    reconciled.Labels = maps.Merge(reconciled.Labels, expected.Labels)
    reconciled.Annotations = maps.Merge(reconciled.Annotations, expected.Annotations)
    reconciled.Spec = expected.Spec
 },
```

The code shows the old annotations should be merged with the new annotations, however, it seems not work.

### Expected behavior
System state should add `ACTOKEY` to `spec.http.service.metadata.annotations` list.

## Alarm 2

**name**: trial-00-0003/0008

**type**: misoperation

### What happened

Acto tried to update `spec.nodeSets[0].volumeClaimTemplates[0].spec.volumeMode` from `ACTOKEY` to "", but system state did not change.


### Root Cause

```go
const (
	// PersistentVolumeBlock means the volume will not be formatted with a filesystem and will remain a raw block device.
	PersistentVolumeBlock PersistentVolumeMode = "Block"
	// PersistentVolumeFilesystem means the volume will be or is formatted with a filesystem.
	PersistentVolumeFilesystem PersistentVolumeMode = "Filesystem"
)
```

The `volumeMode` should be `Block` or `Filesystem`, "" is not valid.

### Expected behavior

System state should reject this change.

## Alarm 3

**name**: trial-00-0004/0003

**type**: misoperation

This alarm is same as **Alarm 2**.

## Alarm 4

**name**: trial-00-0005/0002

**type**: misoperation

### What happened

Acto tried to update `status.conditions[0].lastTransitionTime` from `ACTOKEY` to "", but system state did not change.


### Root Cause

```go
type Condition struct {
	Type   ConditionType          `json:"type"`
	Status corev1.ConditionStatus `json:"status"`
	// +optional
	LastTransitionTime metav1.Time `json:"lastTransitionTime,omitempty"`
	// +optional
	Message string `json:"message,omitempty"`
}
```

The `lastTransitionTime` should be `time.Time`, "" is not valid. And in reconciling process, the `lastTransitionTime` field is always be set as `now`, which is not be able to set manually.

### Expected behavior

System state should reject the change of `lastTransitionTime`.

## Alarm 5

**name**: trial-00-0006/0003

**type**: misoperation

This alarm is same as **Alarm 4**.

## Alarm 6

**name**: trial-00-0010/0009

**type**: false alarm

### What happened

Acto tried to update `spec.auth.roles[0].secretName` from `ActoKey` to "", but system state did not change.


### Root Cause

```go
func (tto TransportTLSOptions) UserDefinedCA() bool {
	return tto.Certificate.SecretName != ""
}

if !b.Elasticsearch.Spec.Transport.TLS.UserDefinedCA() && !b.GlobalCA {
    expected = append(expected, test.ExpectedSecret{
        Name: esName + "-es-transport-ca-internal",
        Keys: []string{"tls.crt", "tls.key"},
        Labels: map[string]string{
            "common.k8s.elastic.co/type":                "elasticsearch",
            "elasticsearch.k8s.elastic.co/cluster-name": esName,
        },
    })
}
```

If `SecretName` field was set as "", then `ExpectedSecret`will be set as a default value.

### Expected behavior

The `secretName` in System state should not be changed to "".

## Alarm 7

**name**: trial-00-0011/0003

**type**: false alarm

This alarm is same as **Alarm 6**.

## Alarm 8

**name**: trial-00-0014/0002

**type**: false alarm

### What happened

Acto tried to update `status.inProgressOperations.upgrade.nodes[0].message` from `ActoKey` to "", but system state did not change.

### Root Cause

```go
for _, node := range nodes {
    upgradedNode := u.nodes[node]
    upgradedNode.Name = node
    upgradedNode.Status = status
    if len(message) > 0 {
        upgradedNode.Message = ptr.To[string](message)
    }
    u.nodes[node] = upgradedNode
}
```

If the string is "", the length is zero then its value will not be changed. 

### Expected behavior

System state will skip the branch of this change.

## Alarm 9

**name**: trial-00-0016/0002

**type**: false alarm

This alarm is same as **Alarm 6**.

## Alarm 10

**name**: trial-00-0017/0003

**type**: false alarm

This alarm is same as **Alarm 6**.

## Alarm 11

**name**: trial-00-0020/0002

**type**: false alarm

This alarm is same as **Alarm 8**.

## Alarm 12

**name**: trial-00-0021/0003

**type**: false alarm

This alarm is same as **Alarm 8**.

## Alarm 13

**name**: trial-01-0006/0002

**type**: false alarm

This alarm is same as **Alarm 8**.

## Alarm 14

**name**: trial-01-0007/0003

**type**: false alarm

This alarm is same as **Alarm 8**.

## Alarm 15

**name**: trial-01-0011/0004

**type**: misoperation

### What happened

Acto tried to add `ActoKey` to path`status.monitoringAssociationStatus` , but system state did not add this value.

### Root Cause

```go
AssociationUnknown     AssociationStatus = ""
AssociationPending     AssociationStatus = "Pending"
AssociationEstablished AssociationStatus = "Established"
AssociationFailed      AssociationStatus = "Failed"
```

The `AssociationStatus` type is enumerated and did not accept `ActoKey`

### Expected behavior

The system state should reject this adding operation.

## Alarm 16

**name**: trial-01-0020/0003

**type**: bug

### What happened

Acto tried to remove `spec.nodeSets[0].volumeClaimTemplates[0].spec.volumeName` , but system state did not remove this value.

### Root Cause

I did not find any reference where to change the value of `volumeName`, so the system state seems not to be able to change this value.

### Expected behavior

The system state should remove the value `volumeName`.

## Alarm 17

**name**: trial-02-0000/0003

**type**: false alarm

This alarm is same as **Alarm 6**.

## Alarm 18

**name**: trial-02-0001/0003

**type**: false alarm

This alarm is same as **Alarm 6**.

## Alarm 19

**name**: trial-02-0005/0001

**type**: misoperation

### What happened

Acto tried to add a k-v item `ActoKey:2000m` into path `spec.nodeSets[0].volumeClaimTemplates[0].spec.resources.limit` , but system state did not add this value.

### Root Cause

```go
const (
	// CPU, in cores. (500m = .5 cores)
	ResourceCPU ResourceName = "cpu"
	// Memory, in bytes. (500Gi = 500GiB = 500 * 1024 * 1024 * 1024)
	ResourceMemory ResourceName = "memory"
	// Volume size, in bytes (e,g. 5Gi = 5GiB = 5 * 1024 * 1024 * 1024)
	ResourceStorage ResourceName = "storage"
	// Local ephemeral storage, in bytes. (500Gi = 500GiB = 500 * 1024 * 1024 * 1024)
	// The resource name for ResourceEphemeralStorage is alpha and it can change across releases.
	ResourceEphemeralStorage ResourceName = "ephemeral-storage"
)
```

The key of the map should be in the above enumerate types, `ActoKey` is not in it.  

### Expected behavior

The system state should reject adding the `ActoKey: 2000m` k-v item.

## Alarm 20

**name**: trial-02-0006/0001

**type**: misoperation

This alarm is same as **Alarm 19**.

## Alarm 21

**name**: trial-02-0008/0001

**type**: misoperation

This alarm is same as **Alarm 15**.

## Alarm 22

**name**: trial-02-0009/0001

**type**: misoperation

This alarm is same as **Alarm 15**.

## Alarm 23

**name**: trial-02-0015/0010

**type**: false alarm

### What happened

Acto tried to update  `spec.nodeSets[0].volumeClaimTemplates[0].spec.storageClassName` , but system state did not update this value.

### Root Cause

```go
if claim.Spec.StorageClassName == nil || *claim.Spec.StorageClassName == "" {
    return getDefaultStorageClass(k8sClient)
}
```

If the expected updating value is "", system state will use default `StorageClassName`

### Expected behavior

System state will change `StorageClassName` to default value.

## Alarm 24

**name**: trial-02-0016/0003

**type**: false alarm

This alarm is same as **Alarm 23**.

## Alarm 25

**name**: trial-03-0002/0007

**type**: bug

### What happened

Acto tried to add a k-v item `ActoKey:ActoKey`  into `spec.nodeSets[0].volumeClaimTemplates[0].metadata.labels` , but system state did not add this item.

### Root Cause

There is no code in reconciling process to change the key or values in labels, so the system state won't update.

### Expected behavior

System state should add the k-v into labels.

## Alarm 26

**name**: trial-03-0003/0001

**type**: bug

This alarm is same as **Alarm 25**.

## Alarm 27

**name**: trial-03-0005/0001

**type**: misoperation

This alarm is same as **Alarm 15**.

## Alarm 28

**name**: trial-03-0010/0002

**type**: false alarm

This alarm is same as **Alarm 6**.

## Alarm 29

**name**: trial-03-0011/0003

**type**: false alarm

This alarm is same as **Alarm 6**.

## Alarm 30

**name**: trial-03-0016/0008

**type**: misoperation

### What happened

Acto tried to apply default image tag: `ActoKey`, and it failed to parse this image name `ActoKey` and then caused the recreating of Pod test-cluster-es-default-2 failure.

### Root Cause

The desired image specified in the elastic search CR cannot be satisfied in the current cluster state. The es operator tried to update the es cluster with the unsatisfiable image and cause the loss of one replica.

### Expected behavior

Operator should reject to update clusters with an invalid image.

## Alarm 31

**name**: trial-03-0017/0001

**type**: misoperation

This alarm is same as **Alarm 30**.
