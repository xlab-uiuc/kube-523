---
name: Alarm Inspection Report
about: An analysis report for the first 10 alarms produced by Acto

---
# Alarm1
trial-00-0007/0005
## What happened
Operator identified this transition as invalid. This transition added a random port number in order to test for integer deletion.

## Root Cause
Operator implicitly checks the validity of zookeeper port. In this test Acto generates an invalid port (port 24614).

## Expected behavior?
Misoperation-Misconfiguration. 

# Alarm2
00-0007/0007

## What happened
Operator identified this transition as invalid. This transition used a random generated port number for zookeeper.

## Root Cause
Operator implicitly checks the validity of zookeeper port. In this test Acto generates an invalid port (port 2).

## Expected behavior?
Misoperation-Misconfiguration.

# Alarm3
00-0007/0009

## What happened
Operator identified this transition as invalid. This testcase removed the whole zookeeper field away from the cr and is rejected by the operator.

## Root Cause
Operator implicitly checks the existence of zookeeper because it's part of the mandatory environment. It rejects the operation of removing zookeeper config.

## Expected behavior?
Misoperation-Misconfiguration.

# Alarm4
00-0007/0009

## What happened
Operator identified this transition as invalid. This testcase assigned an empty string to field insecure.

## Root Cause
Operator checks the input of insecure field. Empty string is not a valid boolean string, thus, the transition is rejected.

## Expected behavior?
Misoperation-Misconfiguration.

# Alarm5
06-0005/0002

## What happened
Operator identified this transition as invalid. This testcase removes the template field in cluster configuration.

## Root Cause
Cluster config without template field is considered invalid by the operator and is rejected.

## Expected behavior?
Misoperation-Misconfiguration.

# Alarm6
05-0004/0002
## What happened
Operator complained about the input.

## Root Cause
Acto captures a word 'no' in the log, but the operator is working fine.

## Expected behavior?
False alarm.


# Alarm7
Fixed at https://github.com/Altinity/clickhouse-operator/issues/1319.

# Alarm8-12
testrun-2024-02-29-00-59/trial-05-0008/0004 -> 008a89a30b03d59501e4793efc9d37f4/0000
testrun-2024-02-29-00-59/trial-06-0004/0001 -> 0277fca72f289cb0953d2549c129b040/0000
testrun-2024-02-29-00-59/trial-05-0006/0001 -> 02aadf0389a0c2c33f69330cf3c273e8/0000
testrun-2024-02-29-00-59/trial-05-0009/0004 -> 03ca0b17a4acbba496ce96e7fee19e04/0000

Differential Oracle reported an alarm but only non-deterministic fields changed.

# Alarm 13
testrun-2024-03-14-09-03/trial-03-0004/0006

## What happened
PreviousTailAffinity breaks the reconilation.

## Root causes
Not 100% sure. Seems this affinity rule requires some nodes topology that cannot be satisfied? The stateful set failed to be updated.

## Expected behavior
Reported [here](https://github.com/Altinity/clickhouse-operator/issues/1378). I feel it's a true alarm.

# Alarm 14
testrun-2024-03-14-09-03/trial-03-0005/0002

## What happened
Acto modify the status field in the cr.

## Root causes
Stateful set failed to be reconsiled due to mismatched status.

## Expected behavior
Misoperation

# Alarm 15
testrun-2024-03-14-09-03/trial-07-0015/0005

## What happened
Acto detected an consistency issue of removing an item in array replicas.

## Root causes
This crd structure of spec.configuration.clusters.layout is very special. It allows fine-grained definition of cluster layout and vague definition with only required replicas and shard number. The normalizer will normalize such configuration. In the normalization process,the file field (which is a dictionary) is merged into new value (which is an empty dictionary as it's removed). Therefore it appears there are no changes in the system state but it is still the expected bahavior.

## Expected behavior
False alarm

# Not Alarm 16-18
testrun-2024-03-14-09-03/trial-07-0012/0002
testrun-2024-03-14-09-03/trial-07-0013/0001
testrun-2024-03-14-09-03/trial-07-0007/0004
## What happened
Managed system crushed and partial invalid input detected. Note Acot did not raise an alarm in these cases, I just found them interesting to look into.

## Root causes
The generated cr is not semantically valid that causes the deployment failed.

## Expected bahavior
A misoperation (if doing something wrong is considerred misoperation) with dire consequences. Or a bug for operator is it doesn't handle this case well. Personally I feel the cr is too wierd to blame for operator bugs.

# Not Alarm 19-27
testrun-2024-03-14-09-03/trial-07-0016/0002
testrun-2024-03-14-09-03/trial-03-0006/0003
testrun-2024-03-14-09-03/trial-07-0006/0005
testrun-2024-03-14-09-03/trial-07-0006/0007
testrun-2024-03-14-09-03/trial-07-0009/0001
testrun-2024-03-14-09-03/trial-07-0015/0003
testrun-2024-03-14-09-03/trial-02-0001/0002
testrun-2024-03-14-09-03/trial-04-0003/0002
testrun-2024-03-14-09-03/trial-05-0002/0001
## What happened
These are not raised as alarm but acto reports some operator input warnings
## Root Causes
Mostly caused by the difficulties to generate some valid 'port', 'host', 'namespace' value.
## Expected behaviour
Handled misoperations.