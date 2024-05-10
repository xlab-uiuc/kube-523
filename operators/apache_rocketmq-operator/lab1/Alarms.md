# Alarms

## Alarm1

trial-00-0003

### Categorization

False Alarm

### What Happened

Acto changes the capacity in VolumeClaimTemplates from NotPresent to 68967M. But there’s no matching change in the system state.

### Root Cause

In the Broker CRD file, VolumeClaimTemplates defines the StorageClass, the operator will use VolumeClaimTemplates defined in cr.yaml only if storageMod is defined as StorageClass.

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

## Alarm2

trial-00-0013/0009

### Categorization

False Alarm

### What Happened

Acto changes the requests in volumes from NotPresent to 3. But there’s no matching change in the system state.

### Root Cause

In broker controller, the operator will use volumes defined in cr.yaml only if storageMod is defined as StorageClass, otherwise it will generate a new volumes config.

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

## Alarm3

trial-00-0014/0001

### Categorization

False Alarm

### What Happened

Acto changes the requests in volumes from NotPresent to 2. But there’s no matching change in the system state.

### Root Cause

Same as Alarm2

## Alarm4

trial-00-0016/0001

### Categorization

False Alarm

### What Happened

Acto changes the requests in volumes from NotPresent to .971785510. But there’s no matching change in the system state.

### Root Cause

Same as Alarm2

## Alarm5

trial-01-0012/0006

### Categorization

False Alarm

### What Happened

Acto changes the nodeSelector in spec from NotPresent to ACTOKEY. But there’s no matching change in the system state.

### Root Cause

The labels for selecting the resources should belongs to the given broker CR name, otherwise it won't match.

``` go
func labelsForBroker(name string) map[string]string {
	return map[string]string{"app": "broker", "broker_cr": name}
}
```

## Alarm6

trial-02-0012/0003

### Categorization

False Alarm

### What Happened

Acto changes the limits in spec from NotPresent to 4. But there’s no matching change in the system state.

### Root Cause

It looks that the every time the operator reconcile will generator a new statefulset config and use the latest cr. Maybe it's becase it sleeps for 30 seconds. 

```go
func (r *ReconcileBroker) Reconcile(ctx context.Context, request reconcile.Request) (reconcile.Result, error) {
    for brokerGroupIndex := 0; brokerGroupIndex < broker.Spec.Size; brokerGroupIndex++ {
        brokerName := getBrokerName(broker, brokerGroupIndex)
        // Update master broker
        reqLogger.Info("Update Master Broker NAMESRV_ADDR of " + brokerName)
        dep := r.getBrokerStatefulSet(broker, brokerGroupIndex, 0)
        found := &appsv1.StatefulSet{}
        err = r.client.Get(context.TODO(), types.NamespacedName{Name: dep.Name, Namespace: dep.Namespace}, found)
        if err != nil {
            reqLogger.Error(err, "Failed to get broker master StatefulSet of "+brokerName)
        } else {
            found.Spec.Template.Spec.Containers[0].Env[0].Value = share.NameServersStr
            err = r.client.Update(context.TODO(), found)
            if err != nil {
                reqLogger.Error(err, "Failed to update NAMESRV_ADDR of master broker "+brokerName, "StatefulSet.Namespace", found.Namespace, "StatefulSet.Name", found.Name)
            } else {
                reqLogger.Info("Successfully updated NAMESRV_ADDR of master broker "+brokerName, "StatefulSet.Namespace", found.Namespace, "StatefulSet.Name", found.Name)
            }
            time.Sleep(time.Duration(cons.RestartBrokerPodIntervalInSecond) * time.Second)
        }
    }
}

func (r *ReconcileBroker) getBrokerStatefulSet() {
    dep := &appsv1.StatefulSet{
        Containers: []corev1.Container{{
            Resources: broker.Spec.Resources,
            Image:     broker.Spec.BrokerImage,
            Name:      cons.BrokerContainerName,
            Lifecycle: &corev1.Lifecycle{
                PostStart: &corev1.Handler{
                    Exec: &corev1.ExecAction{
                        Command: cmd,
                    },
                },
            },
        }}
    }
    return dep
}
```

## Alarm7

trial-02-0013/0001

### Categorization

False Alarm

### What Happened

Acto changes the limits in spec from NotPresent to 2. But there’s no matching change in the system state.

### Root Cause

Same as Alarm6.

## Alarm8

trial-02-0014/0001

### Categorization

False Alarm

### What Happened

Acto changes the limits in spec from NotPresent to +.80342954e-4635221.06. But there’s no matching change in the system state.

### Root Cause

Same as Alarm6.

## Alarm9

trial-03-0007/0002

### Categorization

Ture Alarm

### What Happened

Acto changes the runAsGroup in securityContext from 0 to 1000. But there’s no matching change in the system state.

### Root Cause

In the Broker CRD file, ecurityContext defines the Pod Security Context. However, in the actual code of broker types/controller, it uses podSecurityContext as the field name for the Pod Security Context. 

``` go
type BrokerSpec struct {
    PodSecurityContext *corev1.PodSecurityContext `json:"securityContext,omitempty"`
}

func getPodSecurityContext(broker *rocketmqv1alpha1.Broker) *corev1.PodSecurityContext {
	var securityContext = corev1.PodSecurityContext{}
	if broker.Spec.PodSecurityContext != nil {
		securityContext = *broker.Spec.PodSecurityContext
	}
	return &securityContext
}
```

## Alarm10

trial-03-0008/0009

### Categorization

False Alarm

### What Happened

Acto changes the limits from NotPresent to 3. But there’s no matching change in the system state.

### Root Cause

Same as Alarm2