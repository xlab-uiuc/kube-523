# Analysis of Acto Test Result for grafana-operator

This is based on some acto testruns that were not parsing the grafana-operator's logs correctly, leading to a large number of mis-operations. Therefore, the results contained within should not be used.

## Categorization Summary

The table below lists all the trials reported as True Postives by Acto that were investigated as a part of this study; their categorization into *Bugs*, *Mis-operations*, and *False Alarms*; and any previous trials that had the same or similar root cause.

|           Alarm # | Trial #      | Category           | Dplicate Alarm |
| ----------------: | ------------ | ------------------ | -------------- |
|     [1](#alarm-1) | 01-0000/0008 | Bug                |                |
|     [2](#alarm-2) | 01-0001/0007 | Bug                | Alarm #1       |
|     [3](#alarm-3) | 01-0005/0010 | Mis-operation      |                |
|     [4](#alarm-4) | 01-0006/0003 | Mis-operation      | Alarm #3       |
|     [5](#alarm-5) | 01-0008/0009 | Mis-operation      | Alarm #3       |
|     [6](#alarm-6) | 02-0003/0006 | Bug                | Alarm #1       |
|     [7](#alarm-7) | 02-0009/0001 | Mis-operation      | Alarm #3       |
|     [8](#alarm-8) | 04-0006/0010 | Mis-operation      |                |
|     [9](#alarm-9) | 04-0008/0005 | False Alarm        |                |
|   [10](#alarm-10) | 05-0002/0007 | Mis-operation      | Alarm #3       |
|   [11](#alarm-11) | 05-0003/0003 | Mis-operation      | Alarm #3       |
|   [12](#alarm-12) | 05-0005/0003 | Mis-operation      | Alarm #8       |
|   [13](#alarm-13) | 05-0006/0002 | Bug                |                |
|   [14](#alarm-14) | 07-0003/0009 | Bug                | Alarm #1       |
|   [15](#alarm-15) | 07-0004/0003 | Bug                | Alarm #14      |
|   [16](#alarm-16) | 07-0008/0008 | Bug                |                |
|   [17](#alarm-17) | 07-0009/0006 | Bug                |                |
|   [18](#alarm-18) | 00-0009/0005 | Bug                | Alarm #14      |
|   [19](#alarm-19) | 00-0012/0005 | Mis-operation      | Alarm #3       |
|   [20](#alarm-20) | 00-0013/0001 | Mis-operation      | Alarm #3       |
|   [21](#alarm-21) | 00-0015/0002 | Mis-operation      |                |
|   [22](#alarm-22) | 00-0016/0003 | Mis-operation      | Alarm #21      |
|   [23](#alarm-23) | 00-0017/0008 | Mis-operation      | Alarm #3       |
|   [24](#alarm-24) | 01-0010/0001 | Mis-operation      | Alarm #3       |
|   [25](#alarm-25) | 01-0011/0003 | Mis-operation      | Alarm #3       |
|   [26](#alarm-26) | 01-0012/0002 | Mis-operation      | Alarm #3       |
|   [27](#alarm-27) | 01-0013/0004 | Bug                | Alarm #14      |
|   [28](#alarm-28) | 01-0015/0001 | Bug                | Alarm #17      |
|   [29](#alarm-29) | 01-0016/0001 | Bug                | Alarm #17      |
|   [30](#alarm-30) | 03-0011/0010 | Mis-operation      | Alarm #3       |
|   [31](#alarm-31) | 03-0013/0002 | Bug                | Alarm #1       |
|   [32](#alarm-32) | 04-0009/0005 | Known Bug          |                |
|   [33](#alarm-33) | 04-0011/0003 | Mis-operation      | Alarm #3       |
|   [34](#alarm-34) | 04-0013/0002 | Mis-operation      |                |
|   [35](#alarm-35) | 05-0010/0006 | Bug                | Alarm #16      |
|   [36](#alarm-36) | 05-0012/0003 | Mis-operation      | Alarm #3       |
|   [37](#alarm-37) | 06-0015/0006 | Bug                | Alarm #1       |
|   [38](#alarm-38) | 06-0016/0003 | False Alarm        |                |
|   [39](#alarm-39) | 07-0010/0001 | Bug                |                |
|   [40](#alarm-40) | 00-0019/0005 | Bug                | Alarm #17      |
|   [41](#alarm-41) | 00-0020/0001 | Bug                | Alarm #17      |
|   [42](#alarm-42) | 00-0023/0002 | Bug                | Alarm #1       |
|   [43](#alarm-43) | 00-0025/0004 | Mis-operation      | Alarm #3       |
|   [44](#alarm-44) | 00-0026/0002 | Mis-operation      | Alarm #3       |
|   [45](#alarm-45) | 00-0028/0004 | Bug                | Alarm #1       |
|   [46](#alarm-46) | 01-0019/0006 | False Alarm        | Alarm #38      |
|   [47](#alarm-47) | 01-0020/0002 | False Alarm        | Alarm #38      |
|   [48](#alarm-48) | 02-0023/0001 | Bug? Random crash? | Alarm #17      |
|   [49](#alarm-49) | 02-0024/0001 | Bug? Random crash? | Alarm #17      |
|   [50](#alarm-50) | 02-0025/0001 | Bug? Random crash? | Alarm #17      |
|   [51](#alarm-51) | 03-0020/0010 | False Alarm        | Alarm #38      |
|   [52](#alarm-52) | 03-0021/0002 | False Alarm        | Alarm #38      |
|   [53](#alarm-53) | 03-0022/0002 | False Alarm        | Alarm #38      |
|   [54](#alarm-54) | 04-0014/0010 | Mis-operation      | Alarm #3       |
|   [55](#alarm-55) | 04-0016/0009 | Mis-operation      | Alarm #3       |
|   [56](#alarm-56) | 04-0022/0007 | False Alarm        |                |
|   [57](#alarm-57) | 04-0023/0001 | False Alarm        | Alarm #56      |
|   [58](#alarm-58) | 04-0024/0001 | False Alarm        | Alarm #56      |
|   [59](#alarm-59) | 05-0018/0005 | Mis-operation      | Alarm #21      |
|   [60](#alarm-60) | 05-0019/0003 | Mis-operation      | Alarm #21      |
|   [61](#alarm-61) | 05-0024/0001 | Mis-operation      | Alarm #3       |
|   [62](#alarm-62) | 05-0026/0001 | False Alarm        |                |
|   [63](#alarm-63) | 05-0028/0005 | Mis-operation      | Alarm #3       |
|   [64](#alarm-64) | 05-0029/0003 | Mis-operation      | Alarm #3       |
|   [65](#alarm-65) | 05-0030/0007 | Mis-operation      | Alarm #3       |
|   [66](#alarm-66) | 06-0017/0002 | False Alarm        | Alarm #38      |
|   [67](#alarm-67) | 06-0018/0002 | False Alarm        | Alarm #38      |
|   [68](#alarm-68) | 06-0021/0009 | Mis-operation      | Alarm #21      |
|   [69](#alarm-69) | 06-0023/0009 | False Alarm        | Alarm #62      |
|   [70](#alarm-70) | 06-0024/0008 | Mis-operation      | Alarm #3       |
|   [71](#alarm-71) | 07-0018/0003 | Mis-operation      | Alarm #3       |
|   [72](#alarm-72) | 07-0021/0007 | Mis-operation      | Alarm #3       |
|   [73](#alarm-73) | 07-0022/0003 | Mis-operation      | Alarm #3       |
|   [74](#alarm-74) | 07-0025/0002 | Bug                | Alarm #14      |
|   [75](#alarm-75) | 07-0026/0007 | False Alarm        | Alarm #38      |
|   [76](#alarm-76) | 07-0028/0008 | Mis-operation      | Alarm #21      |
|   [77](#alarm-77) | 00-0030/0002 | Mis-operation      | Alarm #34      |
|   [78](#alarm-78) | 00-0035/0002 | False Alarm        | Alarm #38      |
|   [79](#alarm-79) | 00-0036/0002 | False Alarm        | Alarm #38      |
|   [80](#alarm-80) | 00-0037/0003 | Mis-operation      | Alarm #3       |
|   [81](#alarm-81) | 02-0028/0009 | Bug                | Alarm #17      |
|   [82](#alarm-82) | 02-0031/0003 | Mis-operation      | Alarm #3       |
|   [83](#alarm-83) | 02-0032/0003 | Mis-operation      | Alarm #3       |
|   [84](#alarm-84) | 03-0025/0001 | Bug                | Alarm #17      |
|   [85](#alarm-85) | 03-0026/0001 | Bug                | Alarm #17      |
|   [86](#alarm-86) | 03-0030/0008 | Mis-operation      | Alarm #21      |
|   [87](#alarm-87) | 03-0033/0009 | Bug                | Alarm #1       |
|   [88](#alarm-88) | 04-0027/0007 | Mis-operation      | Alarm #3       |
|   [89](#alarm-89) | 04-0028/0001 | Mis-operation      | Alarm #3       |
|   [90](#alarm-90) | 04-0031/0002 | False Alarm        | Alarm #38      |
|   [91](#alarm-91) | 04-0033/0005 | Mis-operation      | Alarm #3       |
|   [92](#alarm-92) | 04-0034/0002 | Mis-operation      | Alarm #3       |
|   [93](#alarm-93) | 04-0035/0002 | Mis-operation      | Alarm #3       |
|   [94](#alarm-94) | 04-0036/0003 | Mis-operation      | Alarm #3       |
|   [95](#alarm-95) | 04-0038/0003 | Bug                | Alarm #1, #87  |
|   [96](#alarm-96) | 06-0029/0004 | Mis-operation      | Alarm #21      |
|   [97](#alarm-97) | 06-0030/0002 | Mis-operation      | Alarm #96      |
|   [98](#alarm-98) | 06-0033/0002 | False Alarm        |                |
|   [99](#alarm-99) | 06-0035/0001 | Bug                | Alarm #17      |
| [100](#alarm-100) | 07-0029/0002 | Mis-operation      | Alarm #21      |


The next table provides a breakdown of the unique issues identified here and the related alarms. Alarms sharing a common issue description in this table may have been triggered by different modifications to the CR, but are the result of the same or similar bugs.

| Issue # | Category            | Issue Description                                                                                    | Alarms                                                                                                 |
| ------: | ------------------- | ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
|       1 | Bug                 | Various metadata fields are not reconciled properly, possibly due to the controller-runtime package. | 1, 2, 6, 14, 15, 18, 27, 31, 37, 42, 45, 74, 87, 95                                                    |
|       2 | Mis-operation       | The `spec.route` field is not valid for the test system's configuration, but no error is reported.   | 3-5, 7, 10, 11, 19, 20, 23-26, 30, 33, 36, 43, 44, 54, 55, 61, 63-65, 70-73, 80, 82, 83, 88, 89, 91-94 |
|       3 | Mis-operation       | A deprecated API is not reported as such when used at runtime.                                       | 8, 12                                                                                                  |
|       4 | False Alarm         | The system crashes when many more nodes are requested than are available.                            | 9                                                                                                      |
|       5 | Bug                 | The ingress reconciler does not reconcile its fields if `spec.ingress.spec.rules` is not set.        | 13                                                                                                     |
|       6 | Mis-operation / bug | When configured for an external instance, most fields are not reconciled.                            | 16, 35                                                                                                 |
|       7 | Bug                 | Null-pointer dereference.                                                                            | 17, 28, 29, 39, 40, 41, 48-50, 81, 84, 85, 99                                                          |
|       8 | Mis-operation       | An alpha, feature-gated field is ignored without warning.                                            | 21, 22, 59, 60, 68, 76, 86, 96, 97, 100                                                                |
|       9 | Known Bug           | [Old API not marked deprecated.](https://github.com/grafana/grafana-operator/issues/1292)            | 32                                                                                                     |
|      10 | Mis-operation       | When an invalid container image is provided, the pod can crash.                                      | 34, 77                                                                                                 |
|      11 | False Alarm         | An unsatisfiable affinity requirement causes the pod to hang.                                        | 38, 46, 47, 51-53, 66, 67, 75, 78, 79, 90, 98                                                          |
|      12 | False Alarm         | Pausing the deployment causes the pod to hang, which is expected behavior.                           | 56-58                                                                                                  |
|      13 | False Alarm         | Acto does not properly identify the error reported in the operator log.                              | 62, 69                                                                                                 |


## Alarm 1

Trial 01-0000/0008

### Acto's Action

Delete the field `spec.service.metadata.annotations.ACTOKEY`, which previously contained the value `"ACTOKEY"`.

### Alarm Details & Root Cause

Despite the resource specification no longer containing the fields `spec.service.metadata.annotations.ACTOKEY` and `spec.service.metadata.labels.ACTOKEY`,
these fields are still found in the system state.

I believe that this is because the reconciliation process that updates the `spec.service` object uses the `CreateOrUpdate` function as below:
```go
  service := model.GetGrafanaService(cr, scheme)

	_, err := controllerutil.CreateOrUpdate(ctx, r.client, service, func() error {
		service.Spec = v1.ServiceSpec{
			Ports: getServicePorts(cr),
			Selector: map[string]string{
				"app": cr.Name,
			},
			Type: v1.ServiceTypeClusterIP,
		}
		return v1beta1.Merge(service, cr.Spec.Service)
	})
	if err != nil {
		return v1beta1.OperatorStageResultFailed, err
	}
```

The `CreateOrUpdate` function appears to not properly delete metadata fields when they are removed from the object being updated. This is likely due to the treatment of the metadata in the `Update` function found [here](https://github.com/kubernetes-sigs/controller-runtime/blob/d273bae064626b96912127e5a2a6fd1642865d5a/pkg/client/unstructured_client.go#L65-92).



## Alarm 2

Trial 01-0001/0007

### Acto's Action

Delete the field `spec.service.metadata.labels.ACTOKEY`, which previously contained the value `"ACTOKEY"`.

### Alarm Details & Root Cause

Despite the resource specification no longer containing the field `spec.service.metadata.labels.ACTOKEY`,
this field is still found in the system state.

Duplicate of [Alarm 1](#alarm-1).



## Alarm 3

Trial 01-0005/0010

### Acto's Action

Change `spec.route.spec.tls.termination` from `"ACTOKEY"` to `""`.

### Alarm Details & Root Cause

The prior value of `spec.route.spec.tls.termination` does not appear to have ever entered the system
state, so changing the value has no effect either.

According to the grafana-operator API reference, the `spec.route` object "only works in Openshift."
Because we are evaluating in Kind and not using Openshift, we should not expect this configuration to
work.

Thus, we classify this as a *mis-operation*, since the operator does not flag it as an invalid configuration
for our system.



## Alarm 4

Trial 01-0006/0003

### Acto's Action

Change `spec.route.spec.tls.termination` from `"ACTOKEY"` to `""`.

### Alarm Details & Root Cause

Duplicate of [Alarm 3](#alarm-3).



## Alarm 5

Trial 01-0008/0009

### Acto's Action

Add the field `spec.route.metadata.annotations.ACTOKEY` with value `"ACTOKEY"`.

### Alarm Details & Root Cause

Duplicate of [Alarm 3](#alarm-3).



## Alarm 6

Trial 02-0003/0006

### Acto's Action

Delete the field `spec.deployment.metadata.labels.ACTOKEY`, which previously contained the value `"ACTOKEY"`.

### Alarm Details & Root Cause

The system state still contains the deleted field, for the same reason as [Alarm 1](#alarm-1): the reconciler for the `spec.deployment`
object uses a merge operation which does not remove deleted fields.



## Alarm 7

Trial 02-0009/0001

### Acto's Action

Add the field `spec.route.metadata.annotations.ACTOKEY` with value `"ACTOKEY"`.

### Alarm Details & Root Cause

Duplicate of [Alarm 5](#alarm-3).



## Alarm 8

Trial 04-0006/0010

### Acto's Action

Change the field `spec.deployment.spec.template.spec.serviceAccount` from `"ACTOKEY"` to `""`.

### Alarm Details & Root Cause

The grafana-operator API reference defines the `spec.deployment.spec.template.spec.serviceAccount` field as:
> ServiceAccount is a depreciated alias for ServiceAccountName. Deprecated: Use serviceAccountName instead.

Thus, we classify this as a mis-operation, since the grafana-operator does not report this issue at run-time.



## Alarm 9

Trial 04-0008/0005

### Acto's Actions

Change the field `spec.deployment.spec.replicas` from `3` to `1000`.

### Alarm Details & Root Cause

The health oracle reports:
> deployment: test-cluster-deployment replicas [1000] ready_replicas [323], test-cluster-deployment condition [Available] status [False] message [Deployment does not have minimum availability.]

This seems expected, so classifying as a false alarm.



## Alarm 10

Trial 05-0002/0007

### Acto's Actions

Change the field `spec.route.spec.to.kind` from `"ACTOKEY"` to `""`.

### Alarm Details & Root Cause

Duplicate of [Alarm 3](#alarm-3).



## Alarm 11

Trial 05-0003/0003

### Acto's Actions

Change the field `spec.route.spec.to.kind` from `"ACTOKEY"` to `""`.

### Alarm Details & Root Cause

Duplicate of [Alarm 3](#alarm-3).



## Alarm 12

Trial 05-0005/0003

### Acto's Actions

Change the field `spec.deployment.spec.template.spec.serviceAccount` from `"ACTOKEY"` to `""`.

### Alarm Details & Root Cause

Duplicate of [Alarm 8](#alarm-8).



## Alarm 13

Trial 05-0006/0002

### Acto's Actions

Change the field `spec.ingress.spec.tls[0].hosts[0]` from `"test.com"` to `"example.com"`.

### Alarm Details & Root Cause

The `spec.ingress` state is not updated. This is because in `ingress_reconciler.go`, the reconciler only reconciles its fields if the `spec.ingress.spec.rules` field is non-null, using the following check:
```go
  if cr.Spec.Ingress == nil || len(cr.Spec.Ingress.Spec.Rules) == 0 {
		return v1beta1.OperatorStageResultSuccess, nil
	}
```

I'm classifying this as a bug, although it could also potentially by classified as a mis-operation.





## Alarm 14

Trial 07-0003/0009

### Acto's Actions

Delete the field `spec.serviceAccount.imagePullSecrets[0].name`, which previously contained the value `"ACTOKEY"`.

### Alarm Details & Root Cause

In `service_account_reconciler.go`, we can see that the ServiceAccount state is updated via a merge operation:

```go
  sa := model.GetGrafanaServiceAccount(cr, scheme)

	_, err := controllerutil.CreateOrUpdate(ctx, r.client, sa, func() error {
		return v1beta1.Merge(sa, cr.Spec.ServiceAccount)
	})
	if err != nil {
		return v1beta1.OperatorStageResultFailed, err
	}

	return v1beta1.OperatorStageResultSuccess, nil
```

Because the update is merged, deleted fields are not removed from the system's state.

Related to [Alarm 1](#alarm-1).



## Alarm 15

Trial 07-0004/0003

### Acto's Actions

Delete the field `spec.serviceAccount.imagePullSecrets[0].name`, which previously contained the value `"ACTOKEY"`.

### Alarm Details & Root Cause

Duplicate of [Alarm 14](#alarm-14).



## Alarm 16

Trial 07-0008/0008

### Acto's Actions

Add the field `spec.serviceAccount.metadata.annotations.ACTOKEY` with value `"ACTOKEY"`.

### Alarm Details & Root Cause

In this trial, an earlier generation had set the following fields:
```yaml
spec:
  external:
    adminPassword:
      key: ACTOKEY
      name: ACTOKEY
      optional: null
    adminUser:
      key: ACTOKEY
      name: ACTOKEY
      optional: true
    apiKey:
      key: ACTOKEY
      name: ACTOKEY
      optional: false
    url: ACTOKEY
```

Because, in this case, the grafana-operator is set up to connect to an external instance, it skips any reconciliation process that doesn't
affect the `spec.external` configuration. See `grafana_controller.go`.

[The documentation](https://grafana.github.io/grafana-operator/docs/grafana/) states that in external-mode, the fields under `grafana.spec.config` have no affect,
but I'm not certain whether other fields should be considered. It seems potentially problematic that the deployment fields are not reconciled. 

This is either a mis-operation or a bug, but I'm not sure which.

## Alarm 17

Trial 07-0009/0006

### Acto's Actions

Add the field `spec.ingress.metadata.annotations.ACTOKEY` with value `"ACTOKEY"`.

### Alarm Details & Root Cause

The crash oracle reports:
> Pod grafana-operator-controller-manager-867b655778-wzm4s crashed

The health oracle reports:
> deployment: grafana-operator-controller-manager replicas [1] ready_replicas [None], grafana-operator-controller-manager condition [Available] status [False] message [Deployment does not have minimum availability.]\npod: grafana-operator-controller-manager-867b655778-wzm4s container [manager] restart_count [6]

And the consistency oracle reports:
> Found no matching fields for input

The root cause is a null-pointer dereference in the following code snippet from `ingress_reconciler.go`:
```go
  if cr.Spec.Ingress == nil || len(cr.Spec.Ingress.Spec.Rules) == 0 { // Null-pointer dreference here
		return v1beta1.OperatorStageResultSuccess, nil
	}
```
Here, the code checks whether the object `cr.Spec.Ingress` is `nil`, but fails to check whether `cr.Spec.Ingress.Spec` is `nil`. Because our test case does not include a definition of `spec.ingress.spec`, this causes an error.

This is a bug.


## Alarm 18

Trial 00-0009/0005

### Acto's Actions

Delete the field `spec.serviceAccount.metadata.annotations.ACTOKEY`, which contained the value `"ACTOKEY"`.

### Alarm Details & Root Cause

Duplicate of [Alarm 14](#alarm-14).



## Alarm 19

Trial 00-0012/0005

### Acto's Actions

Add the field `spec.route.metadata.annotations.ACTOKEY` with value `"ACTOKEY"`.

### Alarm Details & Root Cause

Duplicate of [Alarm 3](#alarm-3).



## Alarm 20

Trial 00-0013/0001

### Acto's Actions

Add the field `spec.route.metadata.annotations.ACTOKEY` with value `"ACTOKEY"`.

### Alarm Details & Root Cause

Duplicate of [Alarm 3](#alarm-3).



## Alarm 21

Trial 00-0015/0002

### Acto's Actions

Change the field `spec.deployment.spec.template.spec.volumes[0].projected.sources[0].clusterTrustBundle.path` from `"ACTOKEY"` to `""`.

### Alarm Details & Root Cause

The `clusterTrustBundle` is in alpha and [feature-gated](https://kubernetes.io/docs/reference/command-line-tools-reference/feature-gates/).

It is unclear to me whether it should be the grafana-operator's job to report this as a mis-operation, but classifying it as such regardless. 



## Alarm 22

Trial 00-0016/0003

### Acto's Actions

Change the field `spec.deployment.spec.tempalte.spec.volumes[0].projects.sources[0].clusterTrustBundle.path` from `"ACTOKEY"` to `""`.

### Alarm Details & Root Cause

Duplicate of [Alarm 21](#alarm-21).



## Alarm 23

Trial 00-0017/0008

### Acto's Actions

Add the field `spec.route.metadata.labels.ACTOKEY` with value `"ACTOKEY"`.

### Alarm Details & Root Cause

Duplicate of [Alarm 3](#alarm-3)



## Alarm 24

Trial 01-0010/0001

### Acto's Actions

Add the field `spec.route.metadata.annotations.ACTOKEY` with value `"ACTOKEY"`.

### Alarm Details & Root Cause

Duplicate of [Alarm 3](#alarm-3).



## Alarm 25

Trial 01-0011/0003

### Acto's Actions

Change the field `spec.route.spec.alternateBackends[0].weight` from `3` to `0`.

### Alarm Details & Root Cause

Duplicate of [Alarm 3](#alarm-3).



## Alarm 26

Trial 01-0012/0002

### Acto's Actions

Change the field `spec.route.spec.alternateBackends[0].weight` from `2` to `4`.

### Alarm Details & Root Cause

Duplicate of [Alarm 3](#alarm-3).



## Alarm 27

Trial 01-0013/0004

### Acto's Actions

Delete the field `spec.serviceAccount.metadata.annotations.ACTOKEY`, which previously contained the value `"ACTOKEY"`.

### Alarm Details & Root Cause

Duplicate of [Alarm 14](#alarm-14).



## Alarm 28

Trial 01-0015/0001

### Acto's Actions

Add the field `spec.ingress.metadata.annotations.ACTOKEY` with the value `"ACTOKEY"`.

### Alarm Details & Root Cause

Duplicate of [Alarm 17](#alarm-17)



## Alarm 29

Trial 01-0016/0001

### Acto's Actions

Add the field `spec.ingress.metadata` with the value `{}`.

### Alarm Details & Root Cause

Duplicate of [Alarm 17](#alarm-17)



## Alarm 30

Trial 03-0011/0010

### Acto's Actions

Change the value of `spec.route.spec.tls.caCertificate` from `"ACTOKEY"` to `""`.

### Alarm Details & Root Cause

Duplicate of [Alarm 3](#alarm-3).



## Alarm 31

Trial 03-0013/0002

### Acto's Actions

Delete the field `spec.deployment.metadata.annotations.ACTOKEY`, which previously contained the value `"ACTOKEY"`.

### Alarm Details & Root Cause

Duplicate of [Alarm 6](#alarm-6).



## Alarm 32

Trial 04-0009/0005

### Acto's Actions

Add the field `spec.jsonnet.libraryLabelSelector.matchLabels.ACTOKEY` with the value `"ACTOKEY"` (and add several other `spec.jsonnet` fields).

### Alarm Details & Root Cause

A [currently-open GitHub Issue](https://github.com/grafana/grafana-operator/issues/1292) seems to suggest that support for `spec.jsonnet.libraryLabelSelector` (and possibly all of `spec.jsonnet`) was broken in the most recent version of grafana-operator. Therefore, we can classifythis as a known bug.



## Alarm 33

Trial 04-0011/0003

### Acto's Actions

Change the value of `spec.route.spec.tls.caCertificate` from `"ACTOKEY"` to `""`.

### Alarm Details & Root Cause

Duplicate of [Alarm 3](#alarm-3).



## Alarm 34

Trial 04-0013/0002

### Acto's Actions

Add the field `spec.deployment.spec.template.spec.initContainers[0].image` with the value `ACTOKEY`.

### Alarm Details & Root Cause

The health oracle reports:
> deployment: test-cluster-deployment condition [Progressing] status [False] message [ReplicaSet \"test-cluster-deployment-c7bd84bfb\" has timed out progressing.]

Thus, we can mark this as a mis-operation, since the invalid image name causes a crash. This could possibly be addressed in `deployment_reconciler.go`, which currently
does very few checks.



## Alarm 35

Trial 05-0010/0006

### Acto's Actions

Add the field `spec.deployment.spec.template.spec.affinity.podAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.labelSelector.matchLabels.ACTOKEY` with the value `"ACTOKEY"`.

### Alarm Details & Root Cause

Duplicate of [Alarm 16](#alarm-16).



## Alarm 36 

Trial 05-0012/0003

### Acto's Actions

Change the value of `spec.route.spec.tls.destinationCACertificate` from `"ACTOKEY"` to `""`.

### Alarm Details & Root Cause

Duplicate of [Alarm 3](#alarm-3).



## Alarm 37

Trial 06-0015/0006

### Acto's Actions

Delete the field `spec.service.metadata.annotations.ACTOKEY`, which previously contained the value `"ACTOKEY"`.

### Alarm Details & Root Cause

Duplicate of [Alarm 1](#alarm-1).



## Alarm 38

Trial 06-0016/0003

### Acto's Actions

Set the following field accordingly:
```yaml
spec:
  deployment:
    spec:
      template:
        spec:
          affinity:
            podAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
              - matchLabelKeys:
                - ACTOKEY
                topologyKey: exzptsgjrs
```
and then modify to:
```yaml
spec:
  deployment:
    spec:
      template:
        spec:
          affinity:
            podAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
              - matchLabelKeys: []
                topologyKey: exzptsgjrs
```

### Alarm Details & Root Cause

The health oracle reports:
> deployment: test-cluster-deployment condition [Progressing] status [False] message [ReplicaSet \"test-cluster-deployment-8487f8659d\" has timed out progressing.]

Additionally, the operator logs report:
> 2024-03-06T18:22:24Z	INFO	KubeAPIWarningLogger	spec.template.spec.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[0].labelSelector: a null labelSelector results in matching no pod

My understanding of this is: since the affinity requirement cannot be satisfied, the pod is not scheduled at all, and therefore fails to progress.

Classifying as a false alarm, since this is what would be expected from an unsatisfiable affinity requirement.



## Alarm 39

Trial 07-0010/0001

### Acto's Actions

Add the field `spec.ingress.metadata.annotations` with value `{}`.

### Alarm Details & Root Cause

Duplicate of [Alarm 17](#alarm-17).



## Alarm 40

Trial 00-0019/0005

### Acto's Actions

Add the field `spec.ingress.metadata.labels.ACTOKEY` with the value `"ACTOKEY"`.

### Alarm Details & Root Cause

Likely duplicate of [Alarm 17](#alarm-17).



## Alarm 41

Trial 00-0020/0001

### Acto's Actions

Add the field `spec.ingress.metadata.labels` with value `{}`.

### Alarm Details & Root Cause

Likely duplicate of [Alarm 17](#alarm-17).



## Alarm 42

Trial 00-0023/0002

### Acto's Actions

Delete `spec.service.metadata.labels.ACTOKEY`, which previously contained the value `"ACTOKEY"`.

### Alarm Details & Root Cause

Duplicate of [Alarm 1](#alarm-1).



## Alarm 43

Trial 00-0025/0004

### Acto's Actions

Change the value of `spec.route.spec.to.weight` from `1` to `0`.

### Alarm Details & Root Cause

Duplicate of [Alarm 3](#alarm-3).



## Alarm 44

Trial 00-0026/0002

### Acto's Actions

Change the value of `spec.route.spec.to.weight` from `2` to `4`.

### Alarm Details & Root Cause

Duplicate of [Alarm 3](#alarm-3).



## Alarm 45

Trial 00-0028/0004

### Acto's Actions

Delete the field `spec.deployment.metadata.annotations.ACTOKEY`, which previously contained the value `"ACTOKEY"`.

### Alarm Details & Root Cause

Duplicate of [Alarm 1](#alarm-1).



## Alarm 46

Trial 01-0019/0006

### Acto's Actions

Set the following fields accordingly:
```yaml
spec:
  deployment:
    spec:
      template:
        spec:
          affinity:
            podAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
              - matchLabelKeys:
                - ACTOKEY
                topologyKey: lqdtlbktca
```
then modify:
```yaml
spec:
  deployment:
    spec:
      template:
        spec:
          affinity:
            podAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
              - matchLabelKeys:
                - ''
                topologyKey: lqdtlbktca
```

### Alarm Details & Root Cause

Duplicate of [Alarm 38](#alarm-38).



## Alarm 47

Trial 01-0020/0002

### Acto's Actions

Set the following fields accordingly:
```yaml
spec:
  deployment:
    spec:
      template:
        spec:
          affinity:
            podAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
              - matchLabelKeys:
                - ACTOKEY
                topologyKey: bmfyjowfnu
```

### Alarm Details & Root Cause

Duplicate of [Alarm 38](#alarm-38).



## Alarm 48

Trial 02-0023/0001

### Acto's Actions

Add the field `spec.ingress.metadata.annotations.ACTOKEY` with value `"ACTOKEY"`.

### Alarm Details & Root Cause

Duplicate of [Alarm 17](#alarm-17).



## Alarm 49

Trial 02-0024/0001

### Acto's Actions

Add the field `spec.ingress.metadata.annotations.ACTOKEY` with value `"ACTOKEY"`.

### Alarm Details & Root Cause

Duplicate of [Alarm 17](#alarm-17).



## Alarm 50

Trial 02-0025/0001

### Acto's Actions

Add the field `spec.ingress.metadata.annotations.ACTOKEY` with value `''`.

### Alarm Details & Root Cause

Likely duplicate of [Alarm 17](#alarm-17).



## Alarm 51

Trial 03-0020/0010

### Acto's Actions

Set the following fields accordingly:
```yaml
spec:
  deployment:
    spec:
      template:
        spec:
          affinity:
            podAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
              - matchLabelKeys:
                - ACTOKEY
                topologyKey: ycmkczawae
```
then modify:
```yaml
spec:
  deployment:
    spec:
      template:
        spec:
          affinity:
            podAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
              - matchLabelKeys: []
                topologyKey: ycmkczawae
```

### Alarm Details & Root Cause

Duplicate of [Alarm 38](#alarm-38).



## Alarm 52

Trial 03-0021/0002

### Acto's Actions

Set the following fields accordingly:
```yaml
spec:
  deployment:
    spec:
      template:
        spec:
          affinity:
            podAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
              - mismatchLabelKeys: []
                topologyKey: wpbzrwxhix
```
then modify:
```yaml
spec:
  deployment:
    spec:
      template:
        spec:
          affinity:
            podAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
              - mismatchLabelKeys:
                - ACTOKEY
                topologyKey: wpbzrwxhix
```

### Alarm Details & Root Cause

Duplicate of [Alarm 38](#alarm-38).



## Alarm 53

Trial 03-0022/0002

### Acto's Actions

Set the following fields accordingly:
```yaml
spec:
  deployment:
    spec:
      template:
        spec:
          affinity:
            podAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
              - mismatchLabelKeys:
                - ACTOKEY
                topologyKey: xfrxtuxbyl
```
then modify:
```yaml
spec:
  deployment:
    spec:
      template:
        spec:
          affinity:
            podAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
              - mismatchLabelKeys: []
                topologyKey: xfrxtuxbyl
```

### Alarm Details & Root Cause

Duplicate of [Alarm 38](#alarm-38).



## Alarm 54

Trial 04-0014/0010

### Acto's Actions

Change the value of `spec.route.spec.tls.destinationCACertificate` from `"ACTOKEY"` to `""`.

### Alarm Details & Root Cause

Duplicate of [Alarm 3](#alarm-3).



## Alarm 55

Trial 04-0016/0009

### Acto's Actions

Add the field `spec.route.metadata.annotations.ACTOKEY` with value `"ACTOKEY"`.

### Alarm Details & Root Cause

Duplicate of [Alarm 3](#alarm-3).



## Alarm 56

Trial 04-0022/0007

### Acto's Actions

Add the field `spec.deployment.spec.paused` with value `true`.

### Alarm Detail & Root Cause

The health oracle reports:
> deployment: test-cluster-deployment condition [Progressing] status [Unknown] message [Deployment is paused]

This is expected behavior, given the configuration. This is a False Alarm.



## Alarm 57

Trial 04-0023/0001

### Acto's Actions

Add the field `spec.deployment.spec.paused` with value `true`.

### Alarm Detail & Root Cause

Duplicate of [Alarm 56](#alarm-56).



## Alarm 58

Trial 04-0024/0001

### Acto's Actions

Add the field `spec.deployment.spec.paused` with value `true`.

### Alarm Detail & Root Cause

Duplicate of [Alarm 56](#alarm-56).



## Alarm 59

Trial 05-0018/0005

### Acto's Actions

Change the value of `spec.deployment.spec.template.spec.volumes[0].projected.sources[0].clusterTrustBundle.signerName` from `"ACTOKEY"` to `""`.

### Alarm Detail & Root Cause

Duplicate of [Alarm 21](#alarm-21).



## Alarm 60

Trial 05-0019/0003

### Acto's Actions

Change the value of `spec.deployment.spec.template.spec.volumes[0].projected.sources[0].clusterTrustBundle.signerName` from `"ACTOKEY"` to `""`.

### Alarm Detail & Root Cause

Duplicate of [Alarm 21](#alarm-21).



## Alarm 61

Trial 05-0024/0001

### Acto's Actions

Add the field `spec.route.metadata.labels.ACTOKEY` with value `""`.

### Alarm Detail & Root Cause

Duplicate of [Alarm 3](#alarm-3).



## Alarm 62

Trial 05-0026/0001

### Acto's Actions

Add the field `spec.persistentVolumeClaim.spec.resources.limits.ACTOKEY` with the value `".8883269e.8"`.

### Alarm Detail & Root Cause

The operator log reports:
```
E0306 20:21:09.933172       1 reflector.go:147] k8s.io/client-go@v0.29.1/tools/cache/reflector.go:229: Failed to watch *v1beta1.Grafana: failed to list *v1beta1.Grafana: quantities must match the regular expression '^([+-]?[0-9.]+)([eEinumkKMGTP]*[-+]?[0-9]*)$'
```

Note that this is a different format than the grafana-operator's standard error logging, which is presumably why it was not classified as a reported error by acto (the regex to match the error format is different). The regex used to validate this field does not match numbers with fractional exponents, hence the error. I do not know whether this is intended behavior, but since the error was properly reported by the operator, I'm marking this as a false alarm.



## Alarm 63

Trial 05-0028/0005

### Acto's Actions

Change the value of `spec.route.spec.wildcardPolicy` from `"ACTOKEY"` to `""`.

### Alarm Detail & Root Cause

Duplicate of [Alarm 3](#alarm-3).



## Alarm 64

Trial 05-0029/0003

### Acto's Actions

Change the value of `spec.route.spec.wildcardPolicy` from `"ACTOKEY"` to `""`.

### Alarm Detail & Root Cause

Duplicate of [Alarm 3](#alarm-3).



## Alarm 65

Trial 05-0030/0007

### Acto's Actions

Change the value of `spec.route.spec.alternateBackends[0].kind` from `"ACTOKEY"` to `""`.

### Alarm Detail & Root Cause

Duplicate of [Alarm 3](#alarm-3).



## Alarm 66

Trial 06-0017/0002

### Acto's Actions

Set the following fields accordingly:
```yaml
spec:
  deployment:
    spec:
      template:
        spec:
          affinity:
            podAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
              - matchLabelKeys: []
                topologyKey: gacolgmnbc
```
then modify:
```yaml
spec:
  deployment:
    spec:
      template:
        spec:
          affinity:
            podAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
              - matchLabelKeys:
                - ACTOKEY
                topologyKey: gacolgmnbc
```

### Alarm Detail & Root Cause

Duplicate of [Alarm 38](#alarm-38).



## Alarm 67

Trial 06-0018/0002

### Acto's Actions

Set the following fields accordingly:
```yaml
spec:
  deployment:
    spec:
      template:
        spec:
          affinity:
            podAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
              - matchLabelKeys:
                - ACTOKEY
                topologyKey: artcnlovbn
```
then modify:
```yaml
spec:
  deployment:
    spec:
      template:
        spec:
          affinity:
            podAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
              - matchLabelKeys: []
                topologyKey: artcnlovbn
```

### Alarm Detail & Root Cause

Duplicate of [Alarm 38](#alarm-38).



## Alarm 68

Trial 06-0021/0009

### Acto's Actions

Add the field `spec.deployment.spec.template.spec.volumes[0].projected.sources[0].clusterTrustBundle.labelSelector.matchLabels.ACTOKEY` with the value `"ACTOKEY"`.

### Alarm Detail & Root Cause

Duplicate of [Alarm 21](#alarm-21).



## Alarm 69

Trial 06-0023/0009

### Acto's Actions

Add the field `spec.deployment.spec.template.spec.overhead.ACTOKEY` with the value `"-.9816492600E.7955886961"`.

### Alarm Details

Duplicate of [Alarm 62](#alarm-62).



## Alarm 70

Trial 06-0024/0008

### Acto's Actions

Change the value of `spec.route.spec.tls.insecureEdgeTerminationPolicy` from `"ACTOKEY"` to `""`.

### Alarm Details

Duplicate of [Alarm 3](#alarm-3).



## Alarm 71 

Trial 07-0018/0003

### Acto's Actions

Change the value of `spec.route.spec.tls.insecureEdgeTerminationPolicy` from `"ACTOKEY"` to `""`.

### Alarm Details

Duplicate of [Alarm 3](#alarm-3).



## Alarm 72

Trial 07-0021/0007

### Acto's Actions

Change the value of `spec.route.spec.tls.certificate` from `"ACTOKEY"` to `""`.

### Alarm Details

Duplicate of [Alarm 3](#alarm-3).



## Alarm 73

Trial 07-0022/0003

### Acto's Actions

Change the value of `spec.route.spec.tls.certificate` from `"ACTOKEY"` to `""`.

### Alarm Details

Duplicate of [Alarm 3](#alarm-3).



## Alarm 74

Trial 07-0025/0002

### Acto's Actions

Delete the field `spec.serviceAccount.metadata.annotations.ACTOKEY`, which previously contained the value `"ACTOKEY"`.

### Alarm Details

Duplicate of [Alarm 14](#alarm-14).



## Alarm 75

Trial 07-0026/0007

### Acto's Actions

Set the following fields accordingly:
```yaml
spec:
  deployment:
    spec:
      template:
        spec:
          affinity:
            podAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
              - mismatchLabelKeys:
                - ACTOKEY
                topologyKey: ukvrohlcjd
```
then modify:
```yaml
spec:
  deployment:
    spec:
      template:
        spec:
          affinity:
            podAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
              - mismatchLabelKeys:
                - ''
                topologyKey: ukvrohlcjd

```

### Alarm Details & Root Cause

Duplicate of [Alarm 38](#alarm-38).



## Alarm 76

Trial 07-0028/0008

### Acto's Actions

Change the value of `spec.deployment.spec.template.spec.volumes[0].projected.sources[0].clusterTrustBundle.optional` from `true` to `false`.

### Alarm Details & Root Cause

Duplicate of [Alarm 21](#alarm-21).



## Alarm 77

Trial 00-0030/0002

### Acto's Actions

Add the field `spec.deployment.spec.template.spec.containers[0].image` with value `ACTOKEY`.

### Alarm Details & Root Cause

Duplicate of [Alarm 34](#alarm-34).



## Alarm 78

Trial 00-0035/0002

### Acto's Actions

Set the following fields accordingly:
```yaml
spec:
  deployment:
    spec:
      template:
        spec:
          affinity:
            podAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
              - mismatchLabelKeys:
                - ACTOKEY
                topologyKey: rxttgdylen
```

### Alarm Details & Root Cause

Duplicate of [Alarm 38](#alarm-38).



## Alarm 79

Trial 00-0036/0002

### Acto's Actions

Set the following fields accordingly:
```yaml
spec:
  deployment:
    spec:
      template:
        spec:
          affinity:
            podAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
              - mismatchLabelKeys:
                - ''
                topologyKey: rbgvykjzsg
```

### Alarm Details & Root Cause

Duplicate of [Alarm 38](#alarm-38).



## Alarm 80

Trial 00-0037/0003

### Acto's Actions

Change the field `spec.route.spec.path` from `"ACTOKEY"` to `""`.

### Alarm Details & Root Cause

Duplicate of [Alarm 3](#alarm-3)



## Alarm 81

Trial 02-0028/0009

### Acto's Actions

Add the field `spec.ingress.metadata.labels.ACTOKEY` with the value `"ACTOKEY"`.

Likely duplicate of [Alarm 17](#alarm-17).



## Alarm 82

Trial 02-0031/0003

### Acto's Actions

Delete the field `spec.route.spec.alternateBackends[0].kind`, which previously contained the value `"ACTOKEY"`.

### Alarm Details & Root Cause

Duplicate of [Alarm 3](#alarm-3).



## Alarm 83

Trial 02-0032/0003

### Acto's Actions

Delete the field `spec.route.spec.alternateBackends[0].kind`, which previously contained the value `"ACTOKEY"`.

### Alarm Details & Root Cause

Duplicate of [Alarm 3](#alarm-3).



## Alarm 84

Trial 03-0025/0001

### Acto's Actions

Add the field `spec.ingress.metadata.labels.ACTOKEY` with value `"ACTOKEY"`.

### Alarm Details & Root Cause

Likely duplicate of [Alarm 17](#alarm-17).



## Alarm 85

Trial 03-0026/0001

### Acto's Actions

Add the field `spec.ingress.metadata.labels.ACTOKEY` with value `''`.

### Alarm Details & Root Cause

Likely duplicate of [Alarm 17](#alarm-17).



## Alarm 86

Trial 03-0030/0008

### Acto's Actions

Add the field `spec.deployment.spec.template.spec.volumes[0].projected.sources[0].clusterTrustBundle.labelSelector.matchLabels.ACTOKEY` with value `"ACTOKEY"`.

### Alarm Details & Root Cause

Likely duplicate of [Alarm 21](#alarm-21).



## Alarm 87

Trial 03-0033/0009

### Acto's Actions

Delete the field `spec.serviceAccount.secrets[0].apiVersion`, which previously contained `"ACTOKEY"`.

### Alarm Details & Root Cause

Duplicate of [Alarm 14](#alarm-14).



## Alarm 88

Trial 04-0027/0007

### Acto's Actions

Add the field `spec.route.metadata.labels.ACTOKEY` with the value `"ACTOKEY"`.

### Alarm Details & Root Cause

Duplicate of [Alarm 3](#alarm-3).



## Alarm 89

Trial 04-0028/0001

### Acto's Actions

Add the field `spec.route.metadata.labels.ACTOKEY` with the value `"ACTOKEY"`.

### Alarm Details & Root Cause

Duplicate of [Alarm 3](#alarm-3).



## Alarm 90

Trial 04-0031/0002

### Acto's Actions

Set the following fields accordingly:
```yaml
spec:
  deployment:
    spec:
      template:
        spec:
          affinity:
            podAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
              - topologyKey: ACTOKEY
```

### Alarm Details & Root Cause

Duplicate of [Alarm 38](#alarm-38).



## Alarm 91

Trial 04-0033/0005

### Acto's Actions

Change the value of `spec.route.spec.port.targetPort` from `3` to `0`.

### Alarm Details & Root Cause

Duplicate of [Alarm 3](#alarm-3).



## Alarm 92

Trial 04-0034/0002

### Acto's Actions

Change the value of `spec.route.spec.port.targetPort` from `2` to `4`.

### Alarm Details & Root Cause

Duplicate of [Alarm 3](#alarm-3).



## Alarm 93

Trial 04-0035/0002

### Acto's Actions

Change the value of `spec.route.spec.port.targetPort` from `"ACTOKEY"` to `""`.

### Alarm Details & Root Cause

Duplicate of [Alarm 3](#alarm-3).



## Alarm 94

Trial 04-0036/0003

### Acto's Actions

Change the value of `spec.route.spec.port.targetPort` from `"ACTOKEY"` to `""`.

### Alarm Details & Root Cause

Duplicate of [Alarm 3](#alarm-3).



## Alarm 95

Trial 04-0038/0003

### Acto's Actions

Delete `spec.serviceAccount.secrets[0].apiVersion`, which previously contained the value `"ACTOKEY"`.

### Alarm Details & Root Cause

Duplicate of [Alarm 87](#alarm-87). See also [Alarm 1](#alarm-1).



## Alarm 96

Trial 06-0029/0004

### Acto's Actions

Change the value of `spec.deployment.spec.template.spec.hostUsers` from `true` to `false`.

### Alarm Details & Root Cause

The API documentation notes:
> This field is alpha-level and is only honored by servers that enable the UserNamespacesSupport feature.

Because this feature is not enabled on our server, this is not a bug. It might be considered a mis-operation.



## Alarm 97

Trial 06-0030/0002

### Acto's Actions

Change the value of `spec.deployment.spec.template.spec.hostUsers` from `true` to `false`.

### Alarm Details & Root Cause

Duplicate of [Alarm 96](#alarm-96).



## Alarm 98

Trial 06-0033/0002

### Acto's Actions

Add the field `spec.deployment.spec.template.spec.nodeSelector.ACTOKEY` with value `"ACTOKEY"`.

### Alarm Details & Root Cause

Because the `nodeSelector` does not match the labels on any node in the system, the operator cannot be scheduled and ceases to progress, with the following message from the health oracle:
> deployment: test-cluster-deployment condition [Progressing] status [False] message [ReplicaSet \"test-cluster-deployment-7d8978868d\" has timed out progressing.]

False Alarm. Realted to [Alarm 38](#alarm-38).



## Alarm 99

Trial 06-0035/0001

### Acto's Actions

Add the field `spec.ingress` with the value `{}`.

### Alarm Details & Root Cause

Duplicate of [Alarm 17](#alarm-17).



## Alarm 100

Trial 07-0029/0002

### Acto's Actions

Change the value of `spec.deployment.spec.template.spec.volumes[0].projected.sources[0].clusterTrustBundle.optional` from `true` to `false`.

### Alarm Details & Root Cause

Duplicate of [Alarm 21](#alarm-21).
