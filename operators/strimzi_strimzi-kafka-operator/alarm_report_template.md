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

# Alarm 11

## What happened
kafka.storage.volume.class attribute is added however no change in the system state is observed.

## Root Cause
This operation is not allowed by the operator. Warning messages were logged pointing out the allowed actions.

## Expected behavior?
True Alarm. The operator should not accept the mutation and throw an error on applying the CRD.

# Alarm 12
Exactly the same as Alarm 11

# Alarm 13
Invalid topology key is generated for the CRD similar to Alarm 1

# Alarm 15
## What happened
Topic operator restarted once when the seed CR is created.

## Root Cause
I compared the logs and system states with other runs; however, I could not find any difference. This seems like a very rare bug potentially caused by race conditions 
because it is undeterministic.

## Expected behavior?
True alarm. The operator should not restart on creating the seed CR. However, it is difficult to reproduce the issue.

# Alarm 16
## What happened
Acto did not observe change to system state caused by mutation of `kafkaExporter.logging` attribute.

## Root Cause
The attribute only supports three values: `info`, `debug`, `trace`. Any other value is not allowed. The problem is that the operator does not throw an error for invalid values nor does it log a warning.

## Expected behavior?
True alarm. The operator should throw an error for invalid values.

# Alarm 19
## What happened
Acto test `bad-security-context` crashed kafka cluster node. The recovery differential oracle observed inconsistent system state.

## Root Cause
The change in security context caused the permission denied error when reading from an
existing log file created by the pod previously.

## Expected behavior?
True alarm. Idealy, the operator should reject this misoperation or at least given a warning.

# Alarm 24
## What happened
Acto set a value in the status of CRD which is ignored by the operator, therefore triggering the consistency oracle.

## Root Cause
Acto mutating the status of CRD.

## Expected behavior?
False alarm. Acto should not mutate the status of CRD.

# Alarm 26
## What happened
Acto generated a invalid image value for `entityOperator.tlsSidecar.image` attribute.

## Root Cause
Acto is unable to generate valid image value for `entityOperator.tlsSidecar.image` attribute.

## Expected behavior?
False alarm. Acto should be able to generate valid image attributes from examples.

# Alarm 37

## What happened
`zookeeper.jvmOptions.gcLoggingEnabled` attribute is added and caused socket disconnection.
Error: `ClientCnxn:1300 - Session 0x0 for server test-cluster-zookeeper-0.test-cluster-zookeeper-nodes.kafka.svc/10.244.2.5:2181, Closing socket connection. Attempting reconnect except it is a SessionExpiredException.`

## Root Cause
I manually tested deploying the CR with the attributes on and off. The error occurs when
the attribute is changed after the initial deployment. 

## Expected behavior?
True alarm. The operator should either reject this operation or correctly handle the change in the attribute.

# Alarm 41

## What happened
Setting `clusterCa.generateCertificateAuthority` to `false` triggered consistency oracle.

## Root Cause
This is a configuration for the operator and does not cause any system state change.

## Expected behavior?
False alarm. Acto should ignore this configuration.

# Alarm 43

## What happened
Setting `kafka.authorization.type` to `custom` without setting `kafka.authorization.authorizerClass` caused the operator to fail on startup. The error message indicates that
the operator is unable to find a class for the authorizer.

## Root Cause
Kafka operator does not have enough schema validation for the `kafka.authorization` attribute.

## Expected behavior?
True alarm. The operator should throw an error for invalid values.

# Alarm 44

## What happened
The operator set a value in the CRD that does not introduce any system state change.
The attribute `kafka.storage.volumes.0.overides.0.broker` is set to `4` which means
that the the operator would override the config for broker 4. However, there is no broker 4 in the kafka cluster.

## Root Cause
The operator does not throw an error for invalid values.

## Expected behavior?
True alarm. The operator should throw an error for misoperation.

# Alarm 46

## What happened
Acto generated a invalid value for `hostAlias.ITEM.ip` attribute.

## Root Cause
Acto is did not automatically generate valid ip address for `hostAlias.ITEM.ip` attribute.

## Expected behavior?
False alarm. Acto should be able to generate valid ip address for `hostAlias.ITEM.ip` attribute.

# Alarm 51

## What happened
Acto generated a invalid value for `template.pod.schedulerName` attribute.

## Root Cause
Acto is did not automatically generate valid scheduler name for `template.pod.schedulerName` attribute.

## Expected behavior?
False alarm. Acto should be able to generate valid scheduler name for `template.pod.schedulerName` attribute.

# Alarm 57

## What happened
The operator logs error message `Resource Kafka(kafka/test-cluster) contains object at path spec.kafka.listeners.auth with an unknown property: tlsTrustedCertificates` when `tlsTrustedCertificates` is part of the CRD.

## Root Cause
Acto generated an invalid value for `tlsTrustedCertificates.certificate` attribute.

## Expected behavior?
True alarm. The operator should throw an error for invalid values.

# Alarm 59

## What happened
Consistency oracle is triggered by attribute mutation `kafka.authorization.grantsRefreshPoolSize`.

## Root Cause
Acto did not observe the reconciliation failure of the previous mutation caused by
invalid topology spread constraints.

## Expected behavior?
False alarm. Acto should wait for the system to reconcile the previous mutation.

# Alarm 63

## What happened
Acto's consistency oracle is triggered due to mutating the value `entityOperator.template.deployment.deploymentStrategy` which does not cause any system state change.

## Root Cause
The value change is not reflected in the system state.

## Expected behavior?
False alarm. The system change is not expeced to change.

# Alarm 64

## What happened
When `kafka.authentication.type` is set to `scram-sha-512` without accompanying values
of username and password, the operator timeout on updating pod resource in the kafka cluster.

## Root Cause
The operator does not check for invalid input for `scram-sha-512` authentication type.

## Expected behavior?
True alarm. The operator should throw an error for invalid values.

# Alarm 70

## What happened
The testcase `k8s-normal_security_context` cause the pod to crash.
Error: `"/opt/kafka/zookeeper_run.sh: line 32: /var/lib/zookeeper/data/myid: Permission denied"`

## Root Cause
The testcase is not properly configured.

## Expected behavior?
False alarm. The managed system depends on the default security context to function properly.

# Alarm 74

## What happened
`kafka.listener.authentication.type` is set to `custom` without setting `kafka.listener.listenerConfig` caused the operator to throw null pointer exception.

## Root Cause
The operator does not have enough schema validation for the `kafka.listener` attribute.

## Expected behavior?
True alarm. The operator should throw an error for invalid values. This bug is [reported](https://github.com/strimzi/strimzi-kafka-operator/issues/9398)

# Alarm 80

## What happened
Acto differential oracle detected inconsistency in the number of secrets in the system
state. 

## Root Cause
Kafka takes longer than Acto's timeout to reconcile the secrets.

## Expected behavior?
False alarm. Acto should wait for the system to reconcile the secrets.

# Alarm 81 - 100

## What happened
Acto is unable to detect the strimzi-kafka's cluster- operator failure to reconcile the system state because the operator only logs the error message and does not throw an error on
CRD apply. This means that Acto often continues to apply CRD mutations even when the operator is not functioning properly. This causes Acto to raise false alarms. Especially for differential oracles, there would almost always be a state difference because the latest CRD mutation is not applied properly and reconciled.

## Root Cause
The operator does not throw an error for invalid CRD mutations.

## Expected behavior?
True alarm. The operator should throw an error for invalid CRD mutations. Acto should also be able to detect the operator's failure to reconcile the system state by inspecting logs.

---

The alarms that I skipped in this report are duplicates of the alarms that I have already analyzed.