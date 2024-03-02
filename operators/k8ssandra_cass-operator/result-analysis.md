---
name: Alarm Inspection Report
about: An analysis report for the alarms produced by Acto

---
netid：wendifu2

## 1
trial-01-0001/0002
trial-01-0001/0004
trial-02-0045/0004
trial-02-0045/0002
trial-02-0045/0006
trial-02-0045/0008

#### oracle:
```
{"field": "", "testcase": "revert"}
```
#### What happened
Acto instructs the cluster to revert to the previous state

#### Root Cause
cass-operator is not healthy and restarts.
```
E0223 21:06:49.056700       1 reflector.go:138] pkg/mod/k8s.io/client-go@v0.22.2/tools/cache/reflector.go:167: Failed to watch *v1.Service: failed to list *v1.Service: services is forbidden: User "system:serviceaccount:cass-operator:cass-operator-controller-manager" cannot list resource "services" in API group "" at the cluster scope: RBAC: clusterrole.rbac.authorization.k8s.io "cass-operator-manager-crrole" not found
```

#### Expected behavior?
True Alarm

Need to check as the ACTO pass through the learn stage, and doesn't produce error readings during the run.

## 2
trial-01-0032/0001

#### oracle:
```
{"field": "[\"spec\", \"additionalServiceConfig\", \"allpodsService\", \"additionalLabels\", \"ACTOKEY\"]", "testcase": "string-deletion"}
```
#### consistency
```
message='Found no matching fields for input' input_diff=Diff(prev='NotPresent', curr='ACTOKEY', path=["spec", "additionalServiceConfig", "allpodsService", "additionalLabels", "ACTOKEY"]) system_state_diff=None
```
#### What happened

```
E0223 21:06:49.056700       1 reflector.go:138] pkg/mod/k8s.io/client-go@v0.22.2/tools/cache/reflector.go:167: Failed to watch *v1.Service: failed to list *v1.Service: services is forbidden: User "system:serviceaccount:cass-operator:cass-operator-controller-manager" cannot list resource "services" in API group "" at the cluster scope: RBAC: clusterrole.rbac.authorization.k8s.io "cass-operator-manager-crrole" not found
```

#### Root Cause

The Cass operator's CRrole is not found during the enumeration

#### Expected behavior?
It is not an expected behavior...


## 3
trial-01-0033/0001 - WIP

#### oracle:

```
{"field": "[\"spec\", \"additionalServiceConfig\", \"allpodsService\", \"additionalLabels\", \"ACTOKEY\"]", "testcase": "string-change"}
```
#### consistency
```
message='Found no matching fields for input' input_diff=Diff(prev='NotPresent', curr='ACTOKEY', path=["spec", "additionalServiceConfig", "allpodsService", "additionalLabels", "ACTOKEY"]) system_state_diff=None
```
#### What happened
#### Root Cause
#### Expected behavior?

## 4
trial-01-0035/0001 - WIP

#### oracle:

```
{"field": "[\"spec\", \"podTemplateSpec\", \"spec\", \"nodeSelector\"]", "testcase": "object-deletion"}
```
#### consistency
```
message='Found no matching fields for input' input_diff=Diff(prev='NotPresent', curr='ACTOKEY', path=["spec", "podTemplateSpec", "spec", "nodeSelector", "ACTOKEY"]) system_state_diff=None
```
#### What happened
#### Root Cause
#### Expected behavior?

## 5
trial-02-0031/0001 - WIP

#### oracle:
```
{"field": "[\"spec\", \"podTemplateSpec\", \"spec\", \"affinity\", \"podAffinity\"]", "testcase": "object-deletion"}
```
#### consistency
```
message='Found no matching fields for input' input_diff=Diff(prev='NotPresent', curr='ACTOKEY', path=["spec", "podTemplateSpec", "spec", "affinity", "podAffinity", "preferredDuringSchedulingIgnoredDuringExecution", 0, "podAffinityTerm", "labelSelector", "matchLabels", "ACTOKEY"]) system_state_diff=None
```
#### What happened
#### Root Cause
#### Expected behavior?

## 6
trial-02-0039/0001 - WIP

#### oracle:
```
{"field": "[\"spec\", \"podTemplateSpec\", \"spec\", \"volumes\", 0, \"ephemeral\", \"volumeClaimTemplate\", \"spec\", \"resources\", \"limits\", \"ACTOKEY\"]", "testcase": "k8s-quantity_increase"}
```
#### consistency
```
message='Found no matching fields for input' input_diff=Diff(prev='NotPresent', curr='2000m', path=["spec", "podTemplateSpec", "spec", "volumes", 0, "ephemeral", "volumeClaimTemplate", "spec", "resources", "limits", "ACTOKEY"]) system_state_diff=None
```
#### What happened
#### Root Cause
#### Expected behavior?