| Acto Alarm Inspection Report: (Operator Tested) | About: |
| --- | --- |
| Splunk Operator | An analysis report for the alarms produced by Acto when analyzing the Splunk Operator with an indexer CR applied. |

# Summary



| Alarm Number: | What happened: | Root cause: | Expected behavior: | 
| --- | --- | --- | --- |
| [Alarm #01](##Alarm-#01 ), [Alarm #03](##Alarm-#03 ), [Alarm #37](##Alarm-#37 )  | Acto consistency oracle detected controller state not changing with the new configuration.    | Acto requested configuration value is below minimum acceptable value according to the documentation but not explicitly listed in the CRD.    | False Alarm    |
| [Alarm #02](##Alarm-#02 ), [Alarm #04](##Alarm-#04 ), [Alarm #08](##Alarm-#08 ), [Alarm #09](##Alarm-#09 ), [Alarm #18](##Alarm-#18 ), [Alarm #22](##Alarm-#22 ), [Alarm #23](##Alarm-#23 ), [Alarm #38](##Alarm-#38 ), [Alarm #06](##Alarm-#06 ), [Alarm #07](##Alarm-#07 ), [Alarm #10](##Alarm-#10 ), [Alarm #11](##Alarm-#11 ), [Alarm #30](##Alarm-#30 ), [Alarm #43](##Alarm-#43 ), [Alarm #44](##Alarm-#44 ), [Alarm #05](##Alarm-#05 ), ...  | Acto consistency oracle detected system state does not align with requested configuration.    | Splunk indexer configuration (CR) spec needed to reference the deployed cluster manager causing the operator to reject changes.    | False Alarm    |

# Alarms

## Alarm #01 
testrun-2024-03-14-00-28/trial-00-0002/0004

### Alarm #01 - What happened?

Acto tried to configure the `"failureThreshold": 0` but according to the [kubernetes documentation](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#configure-probes) the minimum value should be `1` . The system state did not change.


Input Delta:
```
{
      "values_changed": {
            "root['spec']['readinessProbe']['failureThreshold']": {
                  "prev": 4,
                  "curr": 0,
                  "path": {
                        "path": [
                              "spec",
                              "readinessProbe",
                              "failureThreshold"
                        ]
                  }
            }
      }
}
```


### Alarm #01 - Root Cause

The operator rejected the change `"failureThreshold": 0` as the configuration is below the minimum value.


***trial-00-0002/operator-004.log:***
```
ERROR	Reconciler error	{"controller": "indexercluster", "controllerGroup": "enterprise.splunk.com", "controllerKind": "IndexerCluster", "IndexerCluster": {"name":"test-cluster","namespace":"splunk-operator"}, "namespace": "splunk-operator", "name": "test-cluster", "reconcileID": "c091ebe4-c378-4624-865b-3432b560df88", "error": "IndexerCluster spec should refer to ClusterManager via clusterManagerRef"}
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).reconcileHandler
	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.14.5/pkg/internal/controller/controller.go:329
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).processNextWorkItem
	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.14.5/pkg/internal/controller/controller.go:274
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2.2
	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.14.5/pkg/internal/controller/controller.go:235
```

***indexercluster_controller.go***
```go
func (r *IndexerClusterReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
	reconcileCounters.With(getPrometheusLabels(req, "IndexerCluster")).Inc()
	defer recordInstrumentionData(time.Now(), req, "controller", "IndexerCluster")

	reqLogger := log.FromContext(ctx)
	reqLogger = reqLogger.WithValues("indexercluster", req.NamespacedName)

	// Fetch the IndexerCluster
	instance := &enterpriseApi.IndexerCluster{}
	err := r.Get(ctx, req.NamespacedName, instance)
	if err != nil {
		if k8serrors.IsNotFound(err) {
			// Request object not found, could have been deleted after
			// reconcile request.  Owned objects are automatically
			// garbage collected. For additional cleanup logic use
			// finalizers.  Return and don't requeue
			return ctrl.Result{}, nil
		}
		// Error reading the object - requeue the request.
		return ctrl.Result{}, errors.Wrap(err, "could not load indexer cluster data")
	}

	// If the reconciliation is paused, requeue
	annotations := instance.GetAnnotations()
	if annotations != nil {
		if _, ok := annotations[enterpriseApi.IndexerClusterPausedAnnotation]; ok {
			return ctrl.Result{Requeue: true, RequeueAfter: pauseRetryDelay}, nil
		}
	}

	reqLogger.Info("start", "CR version", instance.GetResourceVersion())

	result, err := ApplyIndexerCluster(ctx, r.Client, instance)
	if result.Requeue && result.RequeueAfter != 0 {
		reqLogger.Info("Requeued", "period(seconds)", int(result.RequeueAfter/time.Second))
	}

	return result, err
}
```


### Alarm #01 - Expected behavior?
This was a false alarm. The `failureThreshold` configures the minimum consecutive failures for the probe to be considered failed after having succeeded. A value of `0` for minimum consecutive failures would mean even with no consecutive failures, the probe would be considered a failure. Intuitively this doesn't make sense and functionally the controller did not change the controller state for that configuration.

The CRD property for `failureThreshold` doesn't explicitly list the minimum value as `0` which explains why Acto tried to change the configuration value to `0`. It might be worth exploring changes to Acto where Acto is aware of [probe configuration](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#configure-probes).

## Alarm #02
testrun-2024-03-14-00-28/trial-00-0003/0002

### Alarm #02 - What happened?
Acto tried to configure the `"failureThreshold": 4` but the system state did not change.

### Alarm #02 - Root Cause
`failureThreshold` cannot be set because the configuration is dependant on the proper configuration of `custerManagerRef` to point to the deployed cluster manager by modifying the CR spec.

***trial-00-0003/operator-0002.log:***
```
ERROR	Reconciler error	{"controller": "indexercluster", "controllerGroup": "enterprise.splunk.com", "controllerKind": "IndexerCluster", "IndexerCluster": {"name":"test-cluster","namespace":"splunk-operator"}, "namespace": "splunk-operator", "name": "test-cluster", "reconcileID": "f09b9d9b-3e01-43a6-8375-1769e7881a1e", "error": "IndexerCluster spec should refer to ClusterManager via clusterManagerRef"}
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).reconcileHandler
	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.14.5/pkg/internal/controller/controller.go:329
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).processNextWorkItem
	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.14.5/pkg/internal/controller/controller.go:274
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2.2
	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.14.5/pkg/internal/controller/controller.go:235

```

### Alarm #02 - Expected behavior?
False alarm. The system did not change state for the `failureThreshold` because the `custerManagerRef:` in the CR needs to be configured properly to point to the correct clusterManager object deployed in the same namespace. This can be fixed by changing the default custerManagerRef parameter to point to the name of the deployed clusterManager within the same namespace.

## Alarm #03
testrun-2024-03-14-00-28/trial-00-0004/0003

### Alarm #03 - What happened?

Input Delta:
```
{
      "values_changed": {
            "root['spec']['livenessProbe']['failureThreshold']": {
                  "prev": 5,
                  "curr": 0,
                  "path": {
                        "path": [
                              "spec",
                              "livenessProbe",
                              "failureThreshold"
                        ]
                  }
            }
      }
}
```

Similar issue to Alarm #01 with setting `"failureThreshold": 0`. See [Alarm #01](##Alarm-#01) for more details.


### Alarm #03 - Root Cause
See [Alarm #01](##Alarm-#01).

### Alarm #03 - Expected behavior?
See [Alarm #01](##Alarm-#01).

## Alarm #04
testrun-2024-03-14-00-28/trial-00-0005/0002

### Alarm #04 - What happened?
Acto tried to configure the `"failureThreshold": 4` but the system state did not change.
See [Alarm #02](##Alarm-#02).

### Alarm #04 - Root Cause
See [Alarm #02](##Alarm-#02).

### Alarm #04 - Expected behavior?
See [Alarm #02](##Alarm-#02).

## Alarm #05
testrun-2024-03-14-00-28/trial-01-0000/0002

### Alarm #05 - What happened?
Acto tried to change configuration of `"tolerations": 'node-role.kubernetes.io/control-plane'` but state did not change from `'test-key'`. Tolerations describe a pod's tolerance for a node's taint.
```yaml
  tolerations:
  - effect: NoExecute
    key: node-role.kubernetes.io/control-plane
    operator: Exists
    tolerationSeconds: 3600
```

See [Alarm #02](##Alarm-#02).

### Alarm #05 - Root Cause
See [Alarm #02](##Alarm-#02).

### Alarm #05 - Expected behavior?
See [Alarm #02](##Alarm-#02).

## Alarm #06
testrun-2024-03-14-00-28/trial-01-0001/0004

### Alarm #06 - What happened?
Acto tried to set `"sizeLimit": 4` but the system state did not change from `2000m`.


Input Delta:
```
{
      "values_changed": {
            "root['spec']['volumes'][0]['emptyDir']['sizeLimit']": {
                  "prev": "2000m",
                  "curr": "4",
                  "path": {
                        "path": [
                              "spec",
                              "volumes",
                              0,
                              "emptyDir",
                              "sizeLimit"
                        ]
                  }
            }
      }
}
```

See [Alarm #02](##Alarm-#02).

### Alarm #06 - Root Cause
See [Alarm #02](##Alarm-#02).


### Alarm #06 - Expected behavior?
See [Alarm #02](##Alarm-#02).

Note: The documentation link used in the latest Splunk CRD for `sizeLimit` is broken and needs an update.

## Alarm #07
testrun-2024-03-14-00-28/trial-01-0002/0002
### Alarm #07 - What happened?
Acto tried to set `"sizeLimit": 0.5000` but the system state did not change from `1000m`.

See [Alarm #06](##Alarm-#06).

### Alarm #07 - Root Cause
See [Alarm #06](##Alarm-#06).

### Alarm #07 - Expected behavior?
See [Alarm #06](##Alarm-#06).

## Alarm #08
testrun-2024-03-14-00-28/trial-01-0003/0002
### Alarm #08 - What happened?
Acto tried to set `"initialDelaySeconds": 0` under the livenessProbe but the system state did not change from `1`.

See [Alarm #02](##Alarm-#02).

### Alarm #08 - Root Cause
See [Alarm #02](##Alarm-#02).

### Alarm #08 - Expected behavior?
See [Alarm #02](##Alarm-#02).

## Alarm #09
testrun-2024-03-14-00-28/trial-01-0004/0002
### Alarm #09 - What happened?
Acto tried to set `"initialDelaySeconds": 4` under the livenessProbe but the system state did not change from `2`.

See [Alarm #02](##Alarm-#02).

### Alarm #09 - Root Cause
See [Alarm #02](##Alarm-#02).

### Alarm #09 - Expected behavior?
See [Alarm #02](##Alarm-#02).

## Alarm #10
testrun-2024-03-14-00-28/trial-01-0005/0002
### Alarm #10 - What happened?
Acto tried to configure a volumeClaim with `"ACTOKEY": 2000m` under a `VolumeClaimTemplate` but the system state did not change to satisfy the volume claim request.

```
        "consistency": {
            "message": "Found no matching fields for input",
            "input_diff": {
                "prev": "NotPresent",
                "curr": "2000m",
                "path": {
                    "path": [
                        "spec",
                        "volumes",
                        0,
                        "ephemeral",
                        "volumeClaimTemplate",
                        "spec",
                        "resources",
                        "limits",
                        "ACTOKEY"
                    ]
                }
            },
            "system_state_diff": null
        },
```

```yaml
  volumes:
  - ephemeral:
      volumeClaimTemplate:
        spec:
          resources:
            limits:
              ACTOKEY: 2000m
```

See [Alarm #06](##Alarm-#06).

### Alarm #10 - Root Cause
See [Alarm #06](##Alarm-#06).

### Alarm #10 - Expected behavior?
See [Alarm #06](##Alarm-#06).

## Alarm #11
testrun-2024-03-14-00-28/trial-02-0000/0001
### Alarm #11 - What happened?
Acto tried to configure a volumeClaim with `"ACTOKEY": 1000m` under a `VolumeClaimTemplate` but the system state did not change to satisfy the volume claim request.

```yaml
  volumes:
  - ephemeral:
      volumeClaimTemplate:
        spec:
          resources:
            limits:
              ACTOKEY: 1000m
```

See [Alarm #06](##Alarm-#06).

### Alarm #11 - Root Cause
See [Alarm #06](##Alarm-#06).

### Alarm #11 - Expected behavior?
See [Alarm #06](##Alarm-#06).

## Alarm #12
testrun-2024-03-14-00-28/trial-03-0000/0002
### Alarm #12 - What happened?
Acto tried to set `"periodSeconds": 0` under the startupProbe but the system state did not change from `1`.

See [Alarm #02](##Alarm-#02).

### Alarm #12 - Root Cause
See [Alarm #02](##Alarm-#02).

### Alarm #12 - Expected behavior?
See [Alarm #02](##Alarm-#02).

## Alarm #13
testrun-2024-03-14-00-28/trial-03-0001/0002
### Alarm #13 - What happened?
Acto tried to set `"periodSeconds": 4` under the startupProbe but the system state did not change from `1`.

See [Alarm #02](##Alarm-#02).

### Alarm #13 - Root Cause
See [Alarm #02](##Alarm-#02).

### Alarm #13 - Expected behavior?
See [Alarm #02](##Alarm-#02).

## Alarm #14
testrun-2024-03-14-00-28/trial-03-0002/0002
### Alarm #14 - What happened?
Acto attempts a delete operation for `"imagePullSecrets"` but the system state did not change from `ACTOKEY`.

See [Alarm #02](##Alarm-#02).

### Alarm #14 - Root Cause
See [Alarm #02](##Alarm-#02).

### Alarm #14 - Expected behavior?
See [Alarm #02](##Alarm-#02).

## Alarm #15
testrun-2024-03-14-00-28/trial-03-0003/0003
### Alarm #15 - What happened?
Acto attempts an array pop operation for `"imagePullSecrets"` but the system state did not change from `ACTOKEY`.

See [Alarm #02](##Alarm-#02).

### Alarm #15 - Root Cause
See [Alarm #02](##Alarm-#02).

### Alarm #15 - Expected behavior?
See [Alarm #02](##Alarm-#02).

## Alarm #16
testrun-2024-03-14-00-28/trial-03-0004/0002
### Alarm #16 - What happened?
Acto tried to set `"divisor": 4` under the downwardAPI but the system state did not change from `2000m`.

See [Alarm #02](##Alarm-#02).

### Alarm #16 - Root Cause
See [Alarm #02](##Alarm-#02).

### Alarm #16 - Expected behavior?
See [Alarm #02](##Alarm-#02).

## Alarm #17
testrun-2024-03-14-00-28/trial-03-0005/0001
### Alarm #17 - What happened?
Acto tried to set `"divisor": 0.5` under the downwardAPI but the system state did not change from `1000m`.

See [Alarm #02](##Alarm-#02).

### Alarm #17 - Root Cause
See [Alarm #02](##Alarm-#02).

### Alarm #17 - Expected behavior?
See [Alarm #02](##Alarm-#02).


## Alarm #18
testrun-2024-03-14-00-28/trial-03-0007/0002
### Alarm #18 - What happened?
Acto tried to set `"initialDelaySeconds": 4` under the startupProbe but the system state did not change from `2`.

See [Alarm #02](##Alarm-#02).

### Alarm #18 - Root Cause
See [Alarm #02](##Alarm-#02).

### Alarm #18 - Expected behavior?
See [Alarm #02](##Alarm-#02).

## Alarm #19
testrun-2024-03-14-00-28/trial-04-0000/0006
### Alarm #19 - What happened?
Acto attempts a delete operation for `"extraEnv"` but the system state did not change from `ADDITIONAL_ENV_VAR_1`.

See [Alarm #02](##Alarm-#02).

### Alarm #19 - Root Cause
See [Alarm #02](##Alarm-#02).

### Alarm #19 - Expected behavior?
See [Alarm #02](##Alarm-#02).

## Alarm #20
testrun-2024-03-14-00-28/trial-04-0001/0002
### Alarm #20 - What happened?
Acto attempts a delete operation for `"extraEnv"` but the system state did not change from `ACTOKEY`.

See [Alarm #02](##Alarm-#02).

### Alarm #20 - Root Cause
See [Alarm #02](##Alarm-#02).

### Alarm #20 - Expected behavior?
See [Alarm #02](##Alarm-#02).

## Alarm #21
testrun-2024-03-14-00-28/trial-04-0002/0001
### Alarm #21 - What happened?
Acto attempts a delete operation for `"extraEnv"` but the system state did not change from `ADDITIONAL_ENV_VAR_1`.

See [Alarm #02](##Alarm-#02).

### Alarm #21 - Root Cause
See [Alarm #02](##Alarm-#02).

### Alarm #21 - Expected behavior?
See [Alarm #02](##Alarm-#02).

## Alarm #22
testrun-2024-03-14-00-28/trial-06-0000/0003
### Alarm #22 - What happened?
Acto tried to set `"initialDelaySeconds": 0` under the readinessProbe but the system state did not change from `2`.

See [Alarm #02](##Alarm-#02).

### Alarm #22 - Root Cause
See [Alarm #02](##Alarm-#02).

### Alarm #22 - Expected behavior?
See [Alarm #02](##Alarm-#02).

## Alarm #23
testrun-2024-03-14-00-28/trial-06-0001/0002
### Alarm #23 - What happened?
Acto tried to set `"initialDelaySeconds": 4` under the readinessProbe but the system state did not change from `2`.

See [Alarm #02](##Alarm-#02).

### Alarm #23 - Root Cause
See [Alarm #02](##Alarm-#02).

### Alarm #23 - Expected behavior?
See [Alarm #02](##Alarm-#02).

## Alarm #24
testrun-2024-03-14-00-28/trial-07-0000/0003
### Alarm #24 - What happened?
Acto tried to set `"periodSeconds": 0` under the livenessProbe but the system state did not change from `1`.

See [Alarm #02](##Alarm-#02).

### Alarm #24 - Root Cause
See [Alarm #02](##Alarm-#02).

### Alarm #24 - Expected behavior?
See [Alarm #02](##Alarm-#02).

## Alarm #25
testrun-2024-03-14-00-28/trial-07-0001/0002
### Alarm #25 - What happened?
Acto tried to set `"periodSeconds": 4` under the livenessProbe but the system state did not change from `2`.

See [Alarm #02](##Alarm-#02).

### Alarm #25 - Root Cause
See [Alarm #02](##Alarm-#02).

### Alarm #25 - Expected behavior?
See [Alarm #02](##Alarm-#02).

## Alarm #26
testrun-2024-03-14-00-28/trial-08-0000/0005
### Alarm #26 - What happened?
Acto tried to set `"divisor": 4` under the downwardAPI but the system state did not change from `2000m`.

See [Alarm #02](##Alarm-#02).

### Alarm #26 - Root Cause
See [Alarm #02](##Alarm-#02).

### Alarm #26 - Expected behavior?
See [Alarm #02](##Alarm-#02).

## Alarm #27
testrun-2024-03-14-00-28/trial-08-0001/0002
### Alarm #27 - What happened?
Acto tried to set `"divisor": 0.5` under the downwardAPI but the system state did not change from `1000m`.

See [Alarm #02](##Alarm-#02).

### Alarm #27 - Root Cause
See [Alarm #02](##Alarm-#02).

### Alarm #27 - Expected behavior?
See [Alarm #02](##Alarm-#02).

## Alarm #28
testrun-2024-03-14-00-28/trial-08-0002/0002
### Alarm #28 - What happened?
Acto tried to set `"periodSeconds": 0` under the readinessProbe but the system state did not change from `4`.

See [Alarm #02](##Alarm-#02).

### Alarm #28 - Root Cause
See [Alarm #02](##Alarm-#02).

### Alarm #28 - Expected behavior?
See [Alarm #02](##Alarm-#02).

## Alarm #29
testrun-2024-03-14-00-28/trial-08-0003/0002
### Alarm #29 - What happened?
Acto tried to set `"periodSeconds": 4` under the readinessProbe but the system state did not change from `2`.

See [Alarm #02](##Alarm-#02).

### Alarm #29 - Root Cause
See [Alarm #02](##Alarm-#02).

### Alarm #29 - Expected behavior?
See [Alarm #02](##Alarm-#02).

## Alarm #30
testrun-2024-03-14-00-28/trial-08-0004/0003
### Alarm #30 - What happened?
Acto tried to configure a volumeClaim with `"accessModes": ReadWriteMany` under a `VolumeClaimTemplate` but the system state did not change from `InvalidAccessMode`.

```yaml
  volumes:
  - ephemeral:
      volumeClaimTemplate:
        spec:
          accessModes:
          - ReadWriteMany
```

See [Alarm #06](##Alarm-#06).

### Alarm #30 - Root Cause
See [Alarm #06](##Alarm-#06).

### Alarm #30 - Expected behavior?
See [Alarm #06](##Alarm-#06).

## Alarm #31
testrun-2024-03-14-00-28/trial-09-0000/0004
### Alarm #31 - What happened?
Acto tried to set `"whenUnsatisfiable": INVALID_WHEN_UNSATISFIABLE` under `maxSkew` but the system state did not change from `DoNotSchedule`. `whenUnsatisfiable` describes how to deal with pod scheduling differences in global topology that deviates from the maximum permitted deviation. 

See [Alarm #02](##Alarm-#02).

### Alarm #31 - Root Cause
See [Alarm #02](##Alarm-#02).

### Alarm #31 - Expected behavior?
See [Alarm #02](##Alarm-#02).

## Alarm #32
testrun-2024-03-14-00-28/trial-09-0001/0001
### Alarm #32 - What happened?
Acto tried to set `"whenUnsatisfiable": INVALID_WHEN_UNSATISFIABLE` under `maxSkew` but the system state did not change from `DoNotSchedule`. `whenUnsatisfiable` describes how to deal with pod scheduling differences in global topology that deviates from the maximum permitted deviation. 

See [Alarm #02](##Alarm-#02).

### Alarm #32 - Root Cause
See [Alarm #02](##Alarm-#02).

### Alarm #32 - Expected behavior?
See [Alarm #02](##Alarm-#02).

## Alarm #33
testrun-2024-03-14-00-28/trial-09-0002/0002
### Alarm #33 - What happened?
Acto tried to set `"timeoutSeconds": 0` under the livenessProbe but the system state did not change from `1`.

See [Alarm #02](##Alarm-#02).

### Alarm #33 - Root Cause
See [Alarm #02](##Alarm-#02).

### Alarm #33 - Expected behavior?
See [Alarm #02](##Alarm-#02).

## Alarm #34
testrun-2024-03-14-00-28/trial-09-0003/0002
### Alarm #34 - What happened?
Acto tried to set `"timeoutSeconds": 4` under the livenessProbe but the system state did not change from `2`.

See [Alarm #02](##Alarm-#02).

### Alarm #34 - Root Cause
See [Alarm #02](##Alarm-#02).

### Alarm #34 - Expected behavior?
See [Alarm #02](##Alarm-#02).

## Alarm #35
testrun-2024-03-14-00-28/trial-11-0000/0002
### Alarm #35 - What happened?
Acto tried to set `"timeoutSeconds": 0` under the livenessProbe but the system state did not change from `1`.

See [Alarm #02](##Alarm-#02).

### Alarm #35 - Root Cause
See [Alarm #02](##Alarm-#02).

### Alarm #35 - Expected behavior?
See [Alarm #02](##Alarm-#02).

## Alarm #36
testrun-2024-03-14-00-28/trial-11-0001/0002
### Alarm #36 - What happened?
Acto tried to set `"timeoutSeconds": 4` under the livenessProbe but the system state did not change from `2`.

See [Alarm #02](##Alarm-#02).

### Alarm #36 - Root Cause
See [Alarm #02](##Alarm-#02).

### Alarm #36 - Expected behavior?
See [Alarm #02](##Alarm-#02).

## Alarm #37
testrun-2024-03-14-00-28/trial-12-0000/0003

### Alarm #37 - What happened?

Similar issue to Alarm #01 with setting `"failureThreshold": 0`. See [Alarm #01](##Alarm-#01) for more details.


### Alarm #37 - Root Cause
See [Alarm #01](##Alarm-#01).

### Alarm #37 - Expected behavior?
See [Alarm #01](##Alarm-#01).

## Alarm #38
testrun-2024-03-14-00-28/trial-12-0001/0002
### Alarm #38 - What happened?
Acto tried to set `"failureThreshold": 4` under the startupProbe but the system state did not change from `2`.

See [Alarm #02](##Alarm-#02).

### Alarm #38 - Root Cause
See [Alarm #02](##Alarm-#02).

### Alarm #38 - Expected behavior?
See [Alarm #02](##Alarm-#02).

## Alarm #39
testrun-2024-03-14-00-28/trial-12-0002/0003
### Alarm #39 - What happened?
Acto tried to configure a volumeClaim with `"ACTOKEY": 2000m` under a `requests` but the system state did not change to satisfy the volume claim request.

See [Alarm #06](##Alarm-#06).

### Alarm #39 - Root Cause
See [Alarm #06](##Alarm-#06).

### Alarm #39 - Expected behavior?
See [Alarm #06](##Alarm-#06).

## Alarm #40
testrun-2024-03-14-00-28/trial-12-0003/0001
### Alarm #40 - What happened?
Acto tried to configure a volumeClaim with `"ACTOKEY": 2000m` under a `requests` but the system state did not change to satisfy the volume claim request.

See [Alarm #06](##Alarm-#06).

### Alarm #40 - Root Cause
See [Alarm #06](##Alarm-#06).

### Alarm #40 - Expected behavior?
See [Alarm #06](##Alarm-#06).

## Alarm #41
testrun-2024-03-14-00-28/trial-12-0004/0003

### Alarm #41 - What happened?
See [Alarm #05](##Alarm-#05).

### Alarm #41 - Root Cause
See [Alarm #05](##Alarm-#05).

### Alarm #41 - Expected behavior?
See [Alarm #05](##Alarm-#05).

## Alarm #42
testrun-2024-03-14-00-28/trial-13-0000/0002

### Alarm #42 - What happened?
See [Alarm #05](##Alarm-#05).

### Alarm #42 - Root Cause
See [Alarm #05](##Alarm-#05).

### Alarm #42 - Expected behavior?
See [Alarm #05](##Alarm-#05).

## Alarm #43
testrun-2024-03-14-00-28/trial-13-0001/0006
### Alarm #43 - What happened?
Acto tried to configure a volumeClaim with `"ACTOKEY": 2000m` under a `VolumeClaimTemplate` but the system state did not change to satisfy the volume claim request.

```yaml
  volumes:
  - ephemeral:
      volumeClaimTemplate:
        spec:
          resources:
            limits:
              ACTOKEY: 2000m
```

See [Alarm #06](##Alarm-#06).

### Alarm #43 - Root Cause
See [Alarm #06](##Alarm-#06).

### Alarm #43 - Expected behavior?
See [Alarm #06](##Alarm-#06).

## Alarm #44
testrun-2024-03-14-00-28/trial-13-0002/0001
### Alarm #44 - What happened?
Acto tried to configure a volumeClaim with `"ACTOKEY": 1000m` under a `VolumeClaimTemplate` but the system state did not change to satisfy the volume claim request.

```yaml
  volumes:
  - ephemeral:
      volumeClaimTemplate:
        spec:
          resources:
            limits:
              ACTOKEY: 1000m
```

See [Alarm #06](##Alarm-#06).

### Alarm #44 - Root Cause
See [Alarm #06](##Alarm-#06).

### Alarm #44 - Expected behavior?
See [Alarm #06](##Alarm-#06).

## Alarm #45
testrun-2024-03-14-00-28/trial-14-0000/0004
### Alarm #45 - What happened?
Acto tried to set `"timeoutSeconds": 0` under the readinessProbe but the system state did not change from `4`.

See [Alarm #02](##Alarm-#02).

### Alarm #45 - Root Cause
See [Alarm #02](##Alarm-#02).

### Alarm #45 - Expected behavior?
See [Alarm #02](##Alarm-#02).


## Alarm #46
testrun-2024-03-14-00-28/trial-15-0000/0008
### Alarm #46 - What happened?
Acto tried to set `"divisor": 4` under the downwardAPI but the system state did not change from `2000m`.

See [Alarm #02](##Alarm-#02).

### Alarm #46 - Root Cause
See [Alarm #02](##Alarm-#02).

### Alarm #46 - Expected behavior?
See [Alarm #02](##Alarm-#02).

## Alarm #47
testrun-2024-03-14-00-28/trial-15-0001/0002
### Alarm #47 - What happened?
Acto tried to set `"divisor": 0.5` under the downwardAPI but the system state did not change from `1000m`.

See [Alarm #02](##Alarm-#02).

### Alarm #47 - Root Cause
See [Alarm #02](##Alarm-#02).

### Alarm #47 - Expected behavior?
See [Alarm #02](##Alarm-#02).




# Template
## Alarm #XX
### Alarm #XX - What happened?
Why did Acto raise this alarm?
What happened in the state transition?
Why Acto’s oracles raised an alarm?

### Alarm #XX - Root Cause
Why did the operator behave in this way? Please find the exact block in the operator source code resulting in the behavior.

### Alarm #XX - Expected behavior?
If it is a true alarm, how to fix it in the operator code? 
If it is a false alarm, how to fix it in Acto code?