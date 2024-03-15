---
name: Alarm Inspection Report for Foundation DB
netid: bothra2
total alarms: 270

---

# Class of Alarms 1
266 such alarms

## What happened
### Why did Acto raise this alarm?
All the alarms have the message `message='Found no matching fields for input'`, followed by the value that was being modified during that iteration. This suggests that Acto checked through the system state change, and could not find a matching change.
### What happened in the state transition?
Acto was modifying values within the `spec/processes/ACTOKEY` object.

## Root Cause
### Why did the operator behave in this way? Please find the exact block in the operator source code resulting in the behavior.
In all these alarms, Acto had added an object in `spec/processes` with the key `ACTOKEY`, but the key can only have the following names - (`log`, `storage`, `transaction`, `stateless`, `cluster_controller`, `test`, `coordinator`, `proxy`, `commit_proxy`, `grv_proxy`, `general`). All the alarms were raised because Acto was modifying values within the `ACTOKEY` object itself.
Here is the code block in the operator that explains this - [foundationdb_process_class.go#L28](https://github.com/FoundationDB/fdb-kubernetes-operator/blob/4116a24230fa12f083cfbe1d738ae96dba606922/api/v1beta2/foundationdb_process_class.go#L28)


## Expected behavior?
### If it is a true alarm, how to fix it in the operator code? 
It is a true alarm since the operator should have,
  1. Written the yaml files such that it defines all the acceptable keys instead of allowing an arbitrary value.
  2. Throw an error! Currently no erorr was displayed in any of the logs, which made it slightly hard to debug.

### If it is a false alarm, how to fix it in Acto code?
Acto raised 266 alarms for the same issue, but it can use reasonable heusistics to group these alarms together. A way to do this is to look at all the modifications made as a large decision tree, the leaves of which indicate if the value of `ALARM` is `true` or `false`. Then, it can do a breadth first search on all the nodes of the tree and check if all the leaves of a node result as `true`. If it does, then all the test cases of that node. It should be a reasonable assumption that the alarm is likely caused by the same reason.
