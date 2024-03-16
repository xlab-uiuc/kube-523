# Alarms

## Alarm1

0710fa11958d72d457f1bfbf5bbd43b8/0000

### Categorization

Misoperation

### What Happened

Acto changes the imagePullSecrets from NotPresent to INVALID_NAME. But the operator fails to reject the erroneous state.

### Root Cause

The operator copies ImagePullSecrets from cr without checking whether it's valid or not.

```go
Spec: corev1.PodSpec{
    ServiceAccountName: broker.Spec.ServiceAccountName,
    HostNetwork:        broker.Spec.HostNetwork,
    DNSPolicy:          corev1.DNSClusterFirstWithHostNet,
    Affinity:           broker.Spec.Affinity,
    Tolerations:        broker.Spec.Tolerations,
    NodeSelector:       broker.Spec.NodeSelector,
    PriorityClassName:  broker.Spec.PriorityClassName,
    ImagePullSecrets:   broker.Spec.ImagePullSecrets,
}
```

### Expected behavior

The operator should reject the erroneous desired state.

## Alarm2

0a9ca4c73a558f6f82222f93a71fd839/0000

### Categorization

True Alarm

### What Happened

Acto changes the requests in volumeClaimTemplate from NotPresent to 2. But the operator fails to recover to seed state.

### Root Cause

In broker controller, the operator generate a new volumes config when storageMod is defined as EmptyDir, which may not be the same as the orginal state.

``` go
func getVolumes(broker *rocketmqv1alpha1.Broker) []corev1.Volume {
	switch broker.Spec.StorageMode {
	case cons.StorageModeStorageClass:
		return broker.Spec.Volumes
	case cons.StorageModeEmptyDir:
		volumes := broker.Spec.Volumes
		volumes = append(volumes, corev1.Volume{
			Name: broker.Spec.VolumeClaimTemplates[0].Name,
			VolumeSource: corev1.VolumeSource{
				EmptyDir: &corev1.EmptyDirVolumeSource{}},
		})
		return volumes
	case cons.StorageModeHostPath:
		fallthrough
	default:
		volumes := broker.Spec.Volumes
		volumes = append(volumes, corev1.Volume{
			Name: broker.Spec.VolumeClaimTemplates[0].Name,
			VolumeSource: corev1.VolumeSource{
				HostPath: &corev1.HostPathVolumeSource{
					Path: broker.Spec.HostPath,
				}},
		})
		return volumes
	}
}
```

### Expected behavior

The operator should generate the volumes config based on previous defined one.

## Alarm3

0b1b71cc4d26c407b4c222a381ff4816/0000

### Categorization

Misoperation

### What Happened

Acto changes the name in securityContext from NotPresent to INVALID_NAME. But the operator fails to reject the erroneous state.

### Root Cause

Same as Alarm1

## Alarm4

0f15f31d5fc9e841fc1ef023e22add3f/0000

### Categorization

True Alarm

### What Happened

Acto changes the capacity in volumeClaimTemplate from NotPresent to 1. But the operator fails to recover to seed state.

### Root Cause

Same as Alarm2

## Alarm5

1d052c5df117cd9d85c237d3b103ef44/0000

### Categorization

Misoperation

### What Happened

Acto changes the imagePullSecrets from ACTOKEY to []. But the operator fails to reject the erroneous state.

### Root Cause

Same as Alarm1.

## Alarm6

20b8c2f49f384b8af429902aa7a04f31/0000

### Categorization

True Alarm

### What Happened

Acto changes storageClassName in volumes from NotPresent to ACTOKEY. But the operator fails to recover to seed state.

### Root Cause

Same as Alarm2

## Alarm7

2e5e027a9d44a99306ac2b02a896e0d3/0000

### Categorization

True Alarm

### What Happened

Acto changes the scaleIO in volumes. But the operator fails to recover to seed state.

### Root Cause

Same as Alarm2

## Alarm8

32057edb3a82378275d64dfe6692a434/0000

### Categorization

Misoperation

### What Happened

Acto changes the affinity. But the operator fails to reject the erroneous state.

### Root Cause

Same as Alarm1.

## Alarm9

34b29d43f98036d2a505832b565fb501/0000

### Categorization

Ture Alarm

### What Happened

Acto changes the requests in volumeClaimTemplate from NotPresent to {}. But the operator fails to recover to seed state.

### Root Cause

In broker controller, the operator generate a empty volumeClaimTemplate config when storageMod is defined as EmptyDir, which may not be the same as the orginal state.

``` go
func getVolumeClaimTemplates(broker *rocketmqv1alpha1.Broker) []corev1.PersistentVolumeClaim {
	switch broker.Spec.StorageMode {
	case cons.StorageModeStorageClass:
		return broker.Spec.VolumeClaimTemplates
	case cons.StorageModeEmptyDir, cons.StorageModeHostPath:
		fallthrough
	default:
		return nil
	}
}
```

### Expected behavior

The operator should generate the volumeClaimTemplate config based on previous defined one.

## Alarm10

36af93f8931c71ee3fdaa04407162d47/0000

### Categorization

True Alarm

### What Happened

Acto changes the size in spec from 1 to 0. But the operator fails to reject the erroneous state.

### Root Cause

When both the broker.Status.Size and broker.Spec.Size are 0, the operator will set the groupNum to 0.

```go
if broker.Status.Size == 0 {
    share.GroupNum = broker.Spec.Size
} else {
    share.GroupNum = broker.Status.Size
}
```

### Expected behavior

The operator should reject the erroneous desired state.


## Alarm11

4bf1074effbc3cf6522e0c8680bc3979/0000

### Categorization

True Alarm

### What Happened

Acto changes the limits in volumeClaimTemplate from NotPresent to 5. But the operator fails to recover to seed state.

### Root Cause

Same as Alarm9


## Alarm12

4d09b7797238bff93f05863af4633fe2/0000

### Categorization

Misoperation

### What Happened

Acto changes the name in imagePullSecrets from NotPresent to ACTOKEY. But the operator fails to reject the erroneous state.

### Root Cause

Same as Alarm1

## Alarm13

61668afeb787c507778fc9b14ceb247c/0000

### Categorization

Misoperation

### What Happened

Acto changes the ACTOKEY in resources from NotPresent to 5. But the operator fails to reject the erroneous state.

### Root Cause

Same as Alarm1

## Alarm14

6183bca745aa3c1e08364e4e86d79a15/0000

### Categorization

True Alarm

### What Happened

Acto changes the cinder in volumes from NotPresent to 5. But the operator fails to recover to seed state.

### Root Cause

Same as Alarm2

## Alarm15

678dce2f10f9874f29c390e3d10e87fc/0000

### Categorization

Misoperation

### What Happened

Acto changes the imagePullSecrets from NotPresent to []. But the operator fails to reject the erroneous state.

### Root Cause

Same as Alarm1

## Alarm16

6af5491b81dfc6990e19250df790890c/0000 

### Categorization

True Alarm

### What Happened

Acto changes the ACTOKEY in volumeClaimTemplate from NotPresent to 2. But the operator fails to recover to seed state.

### Root Cause

Same as Alarm2

## Alarm17

6e6985fb0b4aee240163c41878f6f71c/0000

### Categorization

True Alarm

### What Happened

Acto changes the name in volumeClaimTemplates. But the operator fails to recover to seed state.

### Root Cause

Same as Alarm9

## Alarm18

76b04b36ea5caa2fd42f72cc902dbd8e/0000

### Categorization

Misoperation

### What Happened

Acto changes the clusterMode from NotPresent to ACTOKEY. But the operator fails to reject the erroneous state.

### Root Cause

The operator's clusterMode should be configed as "" or "CONTROLLER", but it didn't check non-valid value.

### Expected behavior

The operator should reject the erroneous desired state.

## Alarm19

8b7f62ed8ada93722ee3e2b8de72a485/0000

### What Happened

Acto changes the size in spec from 0 to 2. But the operator fails to recover to seed state.

## Alarm20

False Alarm

### What Happened

Testcase is invalid, resources.requests.ACTOKEY in body must be of type integer,string

## Alarm21

994aee3306115c249a35c7f59e9dbd45/0000

### Categorization

Misoperation

### What Happened

Acto changes the ACTOKEY in resources from NotPresent to 2. But the operator fails to reject the erroneous state.

### Root Cause

Same as Alarm1

## Alarm22

997040cc42df087bd62454ed659baa95/0000

### What Happened

Acto changes the hostNetwork from NotPresent to true. But the operator fails to recover to seed state.

## Alarm23

9f70c83f8bbcd192b11902bf8a1d5d4d/0000

### Categorization

Misoperation

### What Happened

Acto changes the name in env from broker-config to INVALID_NAME. But the operator fails to reject the erroneous state.

### Root Cause

Same as Alarm1

## Alarm24

afd503c19b8848e3f8a2e06fa617dd24/0000

### Categorization

True Alarm

### What Happened

Acto changes the name in volumeClaimTemplates. But the operator fails to recover to seed state.

### Root Cause

Same as Alarm9

## Alarm25

afeddfc6c34ca37ed4e114da011e7f84/0000

### What Happened

Acto changes the hostNetwork from true to false. But the operator fails to recover to seed state.

### Root Cause

Same as Alarm21

## Alarm26

affa9ed3c45bfb6fb38356264ae2bb57/0000

### What Happened

Acto changes the driver in volumes. But the operator fails to recover to seed state.

### Root Cause

Same as Alarm2

## Alarm27

c7c0522e8edf05df3d0b83d094675f89/0000

### What Happened

Acto changes the name in imagePullSecrets from NotPresent to ACTOKEY. But the operator fails to reject the erroneous state.

### Root Cause

Same as Alarm1

## Alarm28

ce15ac7f52ee9208cc6d0d3439a3ec18/0000

### What Happened

Acto changes the storageClassName in volumes. But the operator fails to recover to seed state.

### Root Cause

Same as Alarm2

## Alarm29

dc265d95c37e6744d713b3fed5744eb0/0000

### What Happened

Acto changes the name in volumeClaimTemplates. But the operator fails to recover to seed state.

### Root Cause

Same as Alarm9

## Alarm30

e214d02df0568e0a9f92282a7a6747f0/0000

### What Happened

Acto changes the clusterMode from ACTOKEY to "". But the operator fails to reject the erroneous state.

### Root Cause

Same as Alarm18

## Alarm31

testrun-2024-03-15-11-08/trial-00-0000/0002

### What Happened

Acto changes the storageClassName in Volumes from ACTOKEY to "". But there’s no matching change in the system state.

### Root Cause

Same as Alarm2

## Alarm32

testrun-2024-03-15-11-08/trial-00-0001/0003

### What Happened

Acto changes the storageClassName in Volumes from ACTOKEY to "". But there’s no matching change in the system state.

### Root Cause

Same as Alarm2

## Alarm33

testrun-2024-03-15-11-08/trial-00-0002/0001

### What Happened

Acto changes the limits in volumeClaimTemplates. But there’s no matching change in the system state.

### Root Cause

Same as Alarm9

## Alarm34

testrun-2024-03-15-11-08/trial-00-0003/0001

### What Happened

Acto changes the limits in volumeClaimTemplates. But there’s no matching change in the system state.

### Root Cause

Same as Alarm9

## Alarm35

testrun-2024-03-15-11-08/trial-01-0001/0001

### What Happened

Acto changes the capacity in volumeClaimTemplates. But there’s no matching change in the system state.

### Root Cause

Same as Alarm9

## Alarm36

testrun-2024-03-15-11-08/trial-01-0003/0005 

### What Happened

Acto changes the imagePullSecrets. But there’s no matching change in the system state.

### Root Cause

Same as Alarm1

## Alarm37

testrun-2024-03-15-11-08/trial-01-0004/0003

### What Happened

Acto changes the imagePullSecrets. But there’s no matching change in the system state.

### Root Cause

Same as Alarm1

## Alarm38

testrun-2024-03-15-11-08/trial-01-0005/0002 

### What Happened

Acto changes the name in env from broker-config to INVALID_NAME. But there’s no matching change in the system state.

### Root Cause

Same as Alarm1

## Alarm39

testrun-2024-03-15-11-08/trial-02-0000/0001 

### What Happened

Acto changes the name in volumeClaimTemplates. But there’s no matching change in the system state.

### Root Cause

Same as Alarm9

## Alarm40

testrun-2024-03-15-11-08/trial-02-0001/0006 

### What Happened

Acto changes volumeClaimTemplates. But there’s no matching change in the system state.

### Root Cause

Same as Alarm9

## Alarm41

testrun-2024-03-15-11-08/trial-02-0002/0003 

### What Happened

Acto changes volumeClaimTemplates. But there’s no matching change in the system state.

### Root Cause

Same as Alarm9

## Alarm42

testrun-2024-03-15-11-08/trial-02-0003/0001 

### What Happened

Acto changes volumeClaimTemplates. But there’s no matching change in the system state.

### Root Cause

Same as Alarm9

## Alarm43

testrun-2024-03-15-11-08/trial-02-0005/0005 

### What Happened

Acto changes volumes. But there’s no matching change in the system state.

### Root Cause

Same as Alarm2

## Alarm44

testrun-2024-03-15-11-08/trial-02-0006/0001 

### What Happened

Acto changes volumes. But there’s no matching change in the system state.

### Root Cause

Same as Alarm2

## Alarm45

testrun-2024-03-15-11-08/trial-03-0000/0001 

### What Happened

Acto changes the ACTOKEY in resources from NotPresent to 5. But there’s no matching change in the system state.

### Root Cause

Same as Alarm1

## Alarm46

testrun-2024-03-15-11-08/trial-03-0001/0001 

### What Happened

Acto changes the ACTOKEY in resources from NotPresent to 2. But there’s no matching change in the system state.

### Root Cause

Same as Alarm1
