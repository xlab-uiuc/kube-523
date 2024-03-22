## Alarm 1

Test case:
{"field": "[\"spec\", \"clusterMetricsReporterImage\"]", "testcase": "string-deletion"}


### What Happened
Health issues are reported

message='pod: test-cluster-0-6pjp6'

Seems like one of the pods is no longer healthy after the changes.


The zookeeper-server node is being reconfigured, but it ends up crashing and being unable to be restored by the kafka koperator.

### Root Cause

If we look at `events.json` for either test case, we see that the zookeeper node ended up failing. 
```json
[{"message": "StatefulSet kafka/zookeeper-server is recreating failed Pod zookeeper-server-0"},
{"message": "delete Pod zookeeper-server-0 in StatefulSet zookeeper-server failed error: pods \"zookeeper-server-0\" not found"}]
```

Let's have a look at what the test case added. For some reason, even though the test is named `string-deletion` it adds this field to the `mutated.yaml`
```yaml
clusterMetricsReporterImage: ACTOKEY
```

There's actually no [documentation](https://banzaicloud.github.io/koperator-docs/docs/configurations/crd/kafkaclusters.kafka.banzaicloud.io/#v1beta1-.spec.clusterMetricsReporterImage) for this field, but from the name we can assume that it is trying to load an image. However, ACTOKEY is not a valid image name, so we can assume this is why the pods crash.


### Expected Behavior

Since the name of the image is not valid, it should reject the new state instead of crashing the cluster. Therefore, this is a misoperation.

## Alarm 2

Test case:
{"field": "[\"spec\", \"clusterMetricsReporterImage\"]", "testcase": "string-change"}


### What Happened
Health issues are reported

message='pod: test-cluster-0-5d85w'

Seems like one of the pods is no longer healthy after the changes.


The zookeeper-server node is being reconfigured, but it ends up crashing and being unable to be restored by the kafka koperator.

### Root Cause

If we look at `events.json` for either test case, we see that the zookeeper node ended up failing. 
```json
[{"message": "StatefulSet kafka/zookeeper-server is recreating failed Pod zookeeper-server-0"},
{"message": "delete Pod zookeeper-server-0 in StatefulSet zookeeper-server failed error: pods \"zookeeper-server-0\" not found"}]
```

Let's have a look at what the test case added. For some reason, even though the test is named `string-change` it adds this field to the `mutated.yaml`
```yaml
clusterMetricsReporterImage: ACTOKEY
```

There's actually no [documentation](https://banzaicloud.github.io/koperator-docs/docs/configurations/crd/kafkaclusters.kafka.banzaicloud.io/#v1beta1-.spec.clusterMetricsReporterImage) for this field, but from the name we can assume that it is trying to load an image. However, ACTOKEY is not a valid image name, so we can assume this is why the pods crash.


### Expected Behavior

Since the name of the image is not valid, it should reject the new state instead of crashing the cluster. Therefore, this is a misoperation.

## Alarm 3

{"field": "[\"spec\", \"brokerConfigGroups\", \"ACTOKEY\", \"containers\", 0, \"image\"]", "testcase": "string-deletion"}

### What Happended

```json
"health": {
    "message": "pod: test-cluster-1-5f8vx"
},
```

### Root Cause

Let's have a look at what the test case added. For some reason, even though the test is named `string-deletion` it adds this field to the `mutated.yaml`
```yaml
ACTOKEY:
  containers:
  - image: ''
    name: gcnipnvpme
```

Looking at the source code and the yaml file, we would expect everything to be fine. The operator has comprehensive valiation for the broker including a check to make sure that a profile exists (shown below)

```go
	if brokerNew.BrokerConfigGroup != "" {
					if _, exists := kafkaClusterSpecNew.BrokerConfigGroups[brokerNew.BrokerConfigGroup]; !exists {
						return field.Invalid(field.NewPath("spec").Child("brokers").Index(int(brokerNew.Id)).Child("brokerConfigGroup"), brokerNew.BrokerConfigGroup, unsupportedRemovingStorageMsg+", provided brokerConfigGroup not found"), nil
					}
	}
```
Even though acto added a new group called "ACTOKEY", it never actually changed any of the brokers to use this new group, therefore the cause of this alarm is very puzzling.

If we look at `events.json` for the test case, we see that the issue was. 

The issue with `test-cluster-1-5f8vx` is that it's in a "Pending" phase because its init containers, `cruise-control-reporter` and `jmx-exporter`, haven't completed their tasks. This status indicates that the pod is still setting up, possibly due to image pulling or configuration setups, delaying the main containers from starting. The pod is waiting for initialization processes to finish.

### Expected Behavior

The behavior is exactly as expected. It seems like there is a bug in acto or it somehow didn't wait enough before collecting the system state. We can classify this as a false alarm.


## Alarm 4-5

{"field": "[\"spec\", \"brokerConfigGroups\", \"ACTOKEY\", \"podSecurityContext\"]", "testcase": "object-deletion"}
{"field": "[\"spec\", \"brokerConfigGroups\", \"ACTOKEY\", \"podSecurityContext\"]", "testcase": "object-empty"}

### What Happended

```json
"health": {
    "message": "pod: test-cluster-0-9wpp6"
},
```

### Root Cause

Let's have a look at what the test case added. In this case it both test cases removed all the properties in the podSecurityContext for the ACTOKEY broker group. 


```json
{
      "dictionary_item_removed": {
            "root['spec']['brokerConfigGroups']['ACTOKEY']['podSecurityContext']['fsGroup']": {
                  "prev": 4,
                  "curr": "NotPresent",
                  "path": {
                        "path": [
                              "spec",
                              "brokerConfigGroups",
                              "ACTOKEY",
                              "podSecurityContext",
                              "fsGroup"
                        ]
                  }
            },
            "root['spec']['brokerConfigGroups']['ACTOKEY']['podSecurityContext']['fsGroupChangePolicy']": {
                  "prev": "ACTOKEY",
                  "curr": "NotPresent",
                  "path": {
                        "path": [
                              "spec",
                              "brokerConfigGroups",
                              "ACTOKEY",
                              "podSecurityContext",
                              "fsGroupChangePolicy"
                        ]
                  }
            },
      }
}
```
(there are more things removed)


Looking at the source code and the yaml file, we would expect everything to be fine. The operator has comprehensive valiation for the broker including a check to make sure that a profile exists (shown below)

```go
	if brokerNew.BrokerConfigGroup != "" {
					if _, exists := kafkaClusterSpecNew.BrokerConfigGroups[brokerNew.BrokerConfigGroup]; !exists {
						return field.Invalid(field.NewPath("spec").Child("brokers").Index(int(brokerNew.Id)).Child("brokerConfigGroup"), brokerNew.BrokerConfigGroup, unsupportedRemovingStorageMsg+", provided brokerConfigGroup not found"), nil
					}
	}
```

Acto didn't even add a new group, it simple modified a group that was never used by any of the brokers, which shouldn't have caused any issues.

If we look at `events.json` for the test case, we see what the issue was. 

The issue is that the zookeeper-server pod is in a "Pending" phase because its init containers, `cruise-control-reporter` and `jmx-exporter`, haven't completed their tasks. This status indicates that the pod is still setting up, possibly due to image pulling or configuration setups, delaying the main containers from starting. The pod is waiting for initialization processes to finish.

### Expected Behavior

The behavior is exactly as expected. It seems like there is a bug in acto or it somehow didn't wait enough before collecting the system state. We can classify this as a false alarm.

### Alarm 6:
{"field": "[\"spec\", \"listenersConfig\", \"externalListeners\", 0, \"config\", \"ingressConfig\", \"ACTOKEY\", \"envoyConfig\", \"envoyCommandLineArgs\", \"concurrency\"]", "testcase": "integer-change"}

### What Happened

```json
"consistency": {
            "message": "Found no matching fields for input",
            "input_diff": {
                "prev": 2,
                "curr": 4,
                "path": {
                    "path": [
                        "spec",
                        "listenersConfig",
                        "externalListeners",
                        0,
                        "config",
                        "ingressConfig",
                        "ACTOKEY",
                        "envoyConfig",
                        "envoyCommandLineArgs",
                        "concurrency"
                    ]
                }
            }
```


### Root Cause

Let's have a look at what the test case changed. It seems that it modified the concurrency value from 2 to 4 in for the envoy configuration. We can see, however, that this change was not reflected in the system state.

Let's look at the source code and make sure the concurrency value gets updated

```go
arguments := []string{"-c", "/etc/envoy/envoy.yaml"}
	if ingressConfig.EnvoyConfig.GetConcurrency() > 0 {
		arguments = append(arguments, "--concurrency", strconv.Itoa(int(ingressConfig.EnvoyConfig.GetConcurrency())))
	}

```

We can see that the value is passed in via command line to envoy, so everything looks good on the operator end. However, envoy is not managed by koperator, so there is likely a bug in their code which caused the concurrency value to not change.

### Expected Behavior
The concurrency value should have been updated in the envoy, so this is a true alarm. However, a fix would likely fall on the envoy developers rather than the koperator team to fix this issue.

### Alarm 7-14:
{"field": "", "testcase": "revert"}

### What Happened
An alarm was triggered subsequent to a test case with an invalid configuration input. This followed a previous test case which failed due to an invalid input detected in the system configuration.

### Root Cause
The root cause of the alarm was identified as a false alarm. The system operator correctly rejected a configuration that contained invalid input, in line with the expected behavior of the system's safeguards against erroneous configurations. 

The alarm was a result of the system's response to the following error message from a previous test case:
`message='Invalid input detected' responsible_property=["spec", "listenersConfig", "externalListeners", 0, "config", "ingressConfig", "ACTOKEY", "envoyConfig", "topologySpreadConstraints", 0, "labelSelector", "matchExpressions", 0, "operator"]`

### Expected Behavior
The expected behavior of the system upon encountering an invalid input is to reject the configuration to prevent system instability or crashes. This mechanism worked correctly, and the system did not allow the invalid configuration to affect the operational status of the system components.

The alarm should be classified as a false alarm as it does not indicate an actual fault in the system.

### Alarm 15-18:
Testcase: {}

### What Happened
During system initialization, `zookeeper-server` experienced a failure with the message "StatefulSet kafka/zookeeper-server is recreating failed Pod zookeeper-server-0". Acto raised an alarm possibly due to this failure detected on startup.

### Root Cause
The failure was likely an Acto glitch during the initialization phase, as no persistent issues were evident in subsequent tests. The specific cause is unclear, but it seems to be related to pod creation timing within the StatefulSet management.

### Expected Behavior
This appears to be a false alarm. If similar issues arise in the future, an adjustment to Acto's timing for state collection may be necessary to allow for pod initialization to complete before state assessment.