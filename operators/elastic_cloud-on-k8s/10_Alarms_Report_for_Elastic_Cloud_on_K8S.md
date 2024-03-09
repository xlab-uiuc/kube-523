# 10 Alarms Report for Elastic Cloud on K8S

netId: renzhou2

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

**name**: trial-00-0010/0009

**type**: misoperation

### What happened

Acto tried to update `spec.auth.roles[0].secretName` from `ActoKey` to "", but system state did not change.


### Root Cause

```go
func (tto TransportTLSOptions) UserDefinedCA() bool {
	return tto.Certificate.SecretName != ""
}
```

The `SecretName` field should not be a "" value.

### Expected behavior

System state should reject this change.

## Alarm 5

**name**: trial-00-0011/0003

**type**: misoperation

This alarm is same as **Alarm 4**.

## Alarm 6

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

## Alarm 7

**name**: trial-00-0016/0002

**type**: misoperation

This alarm is same as **Alarm 4**.

## Alarm 8

**name**: trial-00-0017/0003

**type**: misoperation

This alarm is same as **Alarm 4**.

## Alarm 9

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

## Alarm 10

**name**: trial-01-0020/0003

**type**: bug

### What happened

Acto tried to remove `spec.nodeSets[0].volumeClaimTemplates[0].spec.volumeName` , but system state did not remove this value.

### Root Cause

I did not find any reference where to change the value of `volumeName`, so the system state seems not to be able to change this value.

### Expected behavior

The system state should remove the value `volumeName`.
