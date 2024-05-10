# MongoDB Operator Lab 1 Alarm Inspection Report

Acto raised only 3 alarms in total and they are from the same source.

## Alarm 1-3
alarm1:
```
trial-00-0023/0007,
{"field": "[\"spec\", \"statefulSet\", \"metadata\", \"labels\", \"ACTOKEY\"]", "testcase": "string-deletion"}
message='Found no matching fields for input' input_diff=Diff(prev='NotPresent', curr='ACTOKEY', path=["spec", "statefulSet", "metadata", "labels", "ACTOKEY"]) system_state_diff=None
```
alarm2:
```
trial-00-0024/0001,
"{""field"": ""[\""spec\"", \""statefulSet\"", \""metadata\"", \""labels\"", \""ACTOKEY\""]"", ""testcase"": ""string-change""}",True,,,,"message='Found no matching fields for input' input_diff=Diff(prev='NotPresent', curr='ACTOKEY', path=[""spec"", ""statefulSet"", ""metadata"", ""labels"", ""ACTOKEY""]) system_state_diff=None",None,
testrun-2024-02-21-08-40/trial-00-0025/0000,{},False,,,,,None
```
alarm3:
```
trial-00-0025/0001,
"{""field"": ""[\""spec\"", \""statefulSet\"", \""metadata\"", \""labels\"", \""ACTOKEY\""]"", ""testcase"": ""string-empty""}",True,,,,"message='Found no matching fields for input' input_diff=Diff(prev='NotPresent', curr='', path=[""spec"", ""statefulSet"", ""metadata"", ""labels"", ""ACTOKEY""]) system_state_diff=None",None,
testrun-2024-02-21-08-40/trial-00-0026/0000,{},False,,,,,None,
```

### What happened
Acto raise this alarm because there is no matching fields for change stateful set spec after apply this change. Check the mutated yaml file, there is an insertion of `spec, statefulset, metadata, labels, ACTOKEY` in the yaml file. However, the current state didn't change after that insertion.

### Root Cause
The root cause of this change is because the `spec, statefulset` field in mongodb operator use a merge policy, which is annotated in the [crd](https://github.com/mongodb/mongodb-kubernetes-operator/blob/c81c05ccfd9436bcb04059a8f390cc2ace0318a3/config/crd/bases/mongodbcommunity.mongodb.com_mongodbcommunity.yaml) :
```yaml
statefulSet:
    description: StatefulSetConfiguration holds the optional custom StatefulSet
      that should be merged into the operator created one.
```
And we can find the source code of merging statefulset configuration [in this file](https://github.com/mongodb/mongodb-kubernetes-operator/blob/c81c05ccfd9436bcb04059a8f390cc2ace0318a3/pkg/util/merge/merge_statefulset.go#L28)
```go
// StatefulSets merges two StatefulSets together.
func StatefulSets(defaultStatefulSet, overrideStatefulSet appsv1.StatefulSet) appsv1.StatefulSet {
	mergedSts := defaultStatefulSet
	mergedSts.Labels = StringToStringMap(defaultStatefulSet.Labels, overrideStatefulSet.Labels)
	if overrideStatefulSet.Namespace != "" {
		mergedSts.Namespace = overrideStatefulSet.Namespace
	}
	if overrideStatefulSet.Name != "" {
		mergedSts.Name = overrideStatefulSet.Name
	}
	mergedSts.Spec = StatefulSetSpecs(defaultStatefulSet.Spec, overrideStatefulSet.Spec)
	return mergedSts
}
```
It merges the spec field inside the statefulset field, but in this case we leave spec filed an empty object. So the statefulSet field will be deleted after merging.
```yaml
statefulSet:
  metadata:
    labels:
    ACTOKEY: ACTOKEY
  spec: {}
```

### Expected behavior?
In conclusion, it is a false alarm. From Acto's perspective, Acto can never know these things except understand the operator's code. So I think this kind of false positive is inevitable.