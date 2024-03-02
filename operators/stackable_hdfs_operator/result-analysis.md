# Result analysis for Stackable HDFS Operator
Author: Jiyu Hu (jiyuhu2)

## What happened (#1)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["nameNodes", "roleGroups", "ACTOKEY" "podOverrides" "spec" "initContainers", "0", "env", "0", "valueFrom", "configMapKeyRef", "optional"]` field is not set from `True` to `False`

## Root Cause
In function `pub async fn reconcile_hdfs(hdfs: Arc<HdfsCluster>, ctx: Arc<Ctx>) -> HdfsOperatorResult<Action>`, [`let merged_config = role.merged_config(&hdfs, rolegroup_name).context(ConfigMergeSnafu)?;`](https://github.com/stackabletech/hdfs-operator/blob/0975c361e1db67cf662b8456d34794b4bfbe0e3f/rust/operator-binary/src/hdfs_controller.rs#L340) is called to merge the current spec to new desired spec. As we can see [here](https://github.com/stackabletech/hdfs-operator/blob/0975c361e1db67cf662b8456d34794b4bfbe0e3f/rust/crd/src/lib.rs#L341), priority is to set `role_group` config at higher priority than `spec`, so spec is overwritten.

## Expected behavior?
I do think this is a bug in the controller. It should change the priority they set the config. In fact, all my error reports are related to this. Fields in `roleGroups` are not updated because they have higher priority during `Merge`.

## What happened (#2)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "journalNodes", "config", "resources", "cpu", "max"]` field is not set from `ACTOKEY` to `""`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#3)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "journalNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "initContainers", 0, "stdin"]` field is not set from `True` to `False`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#4)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "dataNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "readinessGates", 0, "conditionType"]` field is not set from `ACTOKEY` to `""`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#5)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["status", "conditions", 0, "lastTransitionTime"]` field is not set from `ACTOKEY` to `""`

## Root Cause
`lastTransitionTime` is set according to time

## Expected behavior?
This is a false alarm as this field should not be modified by Acto