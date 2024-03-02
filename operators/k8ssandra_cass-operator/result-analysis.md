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

#### Expected behavior?
It is a false alarm and should be solved by extending the coverage of the learn phase.

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
#### Root Cause
#### Expected behavior?

## 3
trial-01-0033/0001

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
trial-01-0035/0001

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
trial-02-0031/0001

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
trial-02-0039/0001

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