---
name: Strimzi Alarm Inspection Report
about: An analysis report for the alarms produced by Acto

---

# Alarm 1

## What happened
Misconfiguration of topology key causes services to not be scheduled.

## Root Cause
Acto is unable to generate valid topology key for the CRD

## Expected behavior?
Acto should be able to generate valid topology key for the CRD

# Alarm 2

## What happened
<!-- Why did Acto raise this alarm? -->
<!-- What happened in the state transition? -->
<!-- Why Acto’s oracles raised an alarm? -->
The property `kafka.listeners.ITEM.authentication.jwksIgnoreKeyUse` changed is not included in the custom resource status which triggers the consistency oracle.

## Root Cause
Property not represented in custom resource status.
<!-- Why did the operator behave in this way? Please find the exact block in the operator source code resulting in the behavior. -->

## Expected behavior?
<!-- If it is a true alarm, how to fix it in the operator code? 
If it is a false alarm, how to fix it in Acto code? -->
False alarm. Should ignore the property `kafka.listeners.ITEM.authentication.jwksIgnoreKeyUse` in the consistency oracle.

# Alarm 3

## What happened
Expected system state change caused by property `spec.jmxTrans.image` change is not found.

## Root Cause
The property `spec.jmxTrans` is deprecated the resource would not be created.

## Expected behavior?
False alarm. Should ignore the property `jmxTrans.*`.

# Alarm 4

## What happened
Expected system state change caused by property `spec.jmxTrans.kafkaQueries.ITEM.targetMBean` change is not found.

## Root Cause
The property `spec.jmxTrans` is deprecated the resource would not be created.

## Expected behavior?
False alarm. Should ignore the property `jmxTrans.*`.

# Alarm 5

Extactly the same as Alarm 4

# Alarm 6

Similar to Alarm 4

# Alarm 7

Similar to Alarm 4

# Alarm 8

Similar to Alarm 4

# Alarm 9

## What happened
Error `Cruise Control cannot be deployed with a Kafka cluster which has only one broker. It requires at least two Kafka brokers.` is raised.

## Root Cause
Misconfiguration for `cruiseControl.

## Expected behavior?
False alarm. Should add semantic testcases for `cruiseControl`.

# Alarm 10

## What happened
Error was thrown for invalid affinity match expression rules.

## Root Cause
Acto is unable to match Affinity rules for strimzi-kafka-operator by default and have generated invalid Affinity rules.

## Expected behavior?
False alarm. Should add semantic testcases for Affinity rules or add schema tagging.
