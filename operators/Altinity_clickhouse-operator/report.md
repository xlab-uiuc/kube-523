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