# Alarms

# Alarm1

Test info: trial-05-0044/0004

## What happened

Acto changes the flinkVersion from v1_17 to v1_13. But there’s no change in the system state.

## Categorization

true alarm.

## **Root Cause**

Flink Operator website said:

> Starting from 1.7.0 the operator will only support the last 4 Flink minor versions corresponding to the date of the operator release. For 1.7.0 this translates to: 1.18, 1.17, 1.16, 1.15
> 

code can be found: flink-kubernetes-operator/flink-kubernetes-operator-api/src/main/java/org/apache/flink/kubernetes/operator/api/spec/FlinkVersion.java

```bash
public static boolean isSupported(FlinkVersion version) {
        return version != null && version.isNewerVersionThan(FlinkVersion.v1_14);
}
```

So operator will not change the Flink version below 1.15. The transitions from 1.17 to 1.18, 1.16, 1.15 tested in other trials behave well. 

# Alarm2

Test info: trial-06-0046/0001

## What happened

Acto changes the flinkVersion from v1_17 to v1_14. But there’s no change in the system state.

## Categorization

true alarm

## **Root Cause**

Same as Alarm1

---

# Alarm3

Test info: trial-04-0005/0003

## What happened

Acto changes the spec.job.initialSavepointPath from “ACTOKEY” to “” . But there’s no change in the system state.

## Categorization

False alarm

## **Root Cause**

This is actually correct, cause Flink Operator use `savepointRedeployNonce` and `initialSavepointPath` together to redeploy Flink jobs. When changing the `savepointRedeployNonce` the operator will redeploy the job to the savepoint defined in the `initialSavepointPath`. There’s no sense only changing the `initialSavepointPath` .

# Alarm4

est info: trial-03-0007/0001

## What happened

Acto changes spec.job.args[0] from "NotPresent" to "ACTOKEY", the the pods in the system restarts. 

In the generation.json, we can see:

```json
"health": {
    "message": "pod: test-cluster-6868546578-llxsk container [flink-main-container] restart_count [4]"
},
```

Further in the event.json, we can see:

```json
"message": "back-off 20s restarting failed container=flink-main-container pod=test-cluster-6868546578-llxsk_default(5c0cdf51-b882-44d2-b11a-2adedd3a1d20)",
```

## Categorization

Misoperation

## **Root Cause**

the spec.job.args is used to specify the the argument for the job, so this field has a dependency on the actually job, the system fails to reject an invalid argument. Instead, it just restart the pods.

# Alarm5

Test info: trial-07-0035/0004

## What happened

Acto changes spec.serviceAccount from "flink" to "", the the pods in the system restarts. 

In the generation.json, we can see:

```json
"health": {
   "message": "deployment: test-cluster replicas [1] ready_replicas [None], test-cluster condition [Available] status [False] message [Deployment does not have minimum availability.]\npod: test-cluster-f44855bd9-bj8f7 container [flink-main-container] restart_count [6]"
},
```

Further in the event.json, we can see:

```json
"message": "back-off 10s restarting failed container=flink-main-container pod=test-cluster-f44855bd9-bj8f7_default(102124e7-7c1e-4e88-bb9e-349e5a1eebf2)",
```

## Categorization

Misoperation

## **Root Cause**

The serviceAccount cannot be empty or null. We can verify from the code below:

```java
private Optional<String> validateServiceAccount(String serviceAccount) {
        if (serviceAccount == null) {
            return Optional.of(
                    "spec.serviceAccount must be defined. If you use helm, its value should be the same with the name of jobServiceAccount.");
        }
        return Optional.empty();
    }
```

 So if user specify a null or empty serviceAccount, the operator fails to reject it, instead, it just restarts the pods.

# Alarm6

Test info: trial-07-0036/0002

## What happened

Acto changes spec.serviceAccount from "ACTOKEY" to "", the the pods in the system restarts. 

In the generation.json, we can see:

```json
"crash": {
   "message": "Pod test-cluster-64b6599fcf-z44zt crashed"
},
"health": {
    "message": "deployment: test-cluster replicas [1] ready_replicas [None], test-cluster condition [Available] status [False] message [Deployment does not have minimum availability.]\npod: test-cluster-64b6599fcf-z44zt container [flink-main-container] restart_count [6]"
}
```

## Categorization

Misoperation

## **Root Cause**

Same as Alarm5.

# Alarm7-30

Test info: trial-04-0011/002, trial-04-0010/002, trial-01-0053/0002, trial-01-0052/0005, trial-05-0006/0002, trial-05-0005/0004, trial-02-0050/0002, trial-02-0049/0007, trial-02-0056/0002, trial-01-0065/0004, trial-00-0046/0002, trial-00-0045/0003, trial-02-0032/0002, trial-02-0031/0003, trial-01-0008/0002, trial-01-0007/0004, trial-05-0075/0002, trial-05-0074/0002, trial-03-0026/0002, trial-03-0025/0007, trial-01-0061/0002, trial-00-0055/0002, trial-01-0026/0002, trial-01-0025/0002

## What happened

Acto changes ['spec']['jobManager']['podTemplate']['spec']['containers'][0]['env'][0]['valueFrom']['resourceFieldRef']['divisor'] from "1000m" to "0.5000", and from “2000m” to “4”

From the even.json for trial-04-0010/002, we can see:

```json
"message": "UPGRADE change(s) detected (Diff: FlinkDeploymentSpec[jobManager.podTemplate.spec.containers.0.env.0.valueFrom.resourceFieldRef.divisor : 2000m -> 4, job.state : suspended -> running]), starting reconciliation.",
```

```json
"message": "UPGRADE change(s) detected (Diff: FlinkDeploymentSpec[jobManager.podTemplate : null -> {\"apiVersion\":\"v1\",\"kind\":\"Pod\",\"spec\":{\"containers\":[{\"env\":[{\"valueFrom\":{\"resourceFieldRef\":{\"divisor\":\"2000m\"}}}]}]}}]), starting reconciliation.",
```

Which means, the system detected the value and start reconciliation, but somehow, it rolls back to the previous state.

## Categorization

False Alarm

## **Root Cause**

The value is invalid, The fields in ResourceFieldSelector are `containerName` to specify the name of a container, `resource` to specify the type of a resource (cpu or memory), and `divisor` to specify the output format of values of exposed resources. The default value of divisor is `1` which means cores for cpu and bytes for memory. For cpu, divisor's valid values are `1m` (millicores), `1`(cores), and for memory, the valid values in fixed point integer (decimal) are `1`(bytes), `1k`(kilobytes), `1M`(megabytes), `1G`(gigabytes), `1T`(terabytes), `1P`(petabytes), `1E`(exabytes), and in their power-of-two equivalents `1Ki(kilobytes)`, `1Mi`(megabytes), `1Gi`(gigabytes), `1Ti`(terabytes), `1Pi`(petabytes), `1Ei`(exabytes).

So the system is actually rejecting the invalid value.

# Alarm31-54

Test info: trial-06-0070/0001, trial-06-0069/0003, trial-01-0036/0001, trial-01-0035/0003, trial-05-0013/0001, trial-05-0012/0002, trial-04-0073/0001, trial-04-0072/0008, trial-06-0072/0001, trial-06-0071/0001, trial-05-0057/0001, trial-04-0068/0002, trial-05-0055/0001, trial-05-0054/0006, trial-05-0059/0001, trial-05-0058/0001, trial-00-0042/0002, trial-07-0045/0002, trial-03-0051/0002, trial-03-0050/0002, trial-04-0001/0002, trial-04-0000/0004, trial-04-0025/0002, trial-04-0024/0006

## What happened

Acto changes:

- root['spec']['jobManager']['podTemplate'][spec][containers][0][resources][**limits**][ACTOKEY] from “NotPresent” to 1000m/2000m
- root['spec']['jobManager']['podTemplate'][spec][containers][0][resources][**requests**][ACTOKEY] from “NotPresent” to 1000m/2000m

From the event.json, we can see: spec.template.spec.containers[0].resources.requests[ACTOKEY]: Invalid value: \"ACTOKEY\": must be a standard resource type or fully qualified

spec.template.spec.containers[0].resources.limits[ACTOKEY]: Invalid value: \"ACTOKEY\": must be a standard resource type or fully qualified

## Categorization

True alarm

## **Root Cause(invalid value for the field)**

the key for “limit” and “request” field must be a standard resource type or fully qualified, ACTOKEY is a invalid value. But the system doesn’t exhibit any information to remind the user of that.

# Alarm54-58

Test Info:  trial-05-0037/0008, trial-05-0077/0004, trial-03-0021/0009, trial-05-0037/0008, trial-03-0021/0009

## What happened

Acto changes:

- "root['spec']['jobManager']['podTemplate']['spec']['overhead']['ACTOKEY']" from 2 to "ACTOKEY".

No system state change.

## Categorization

True alarm

## **Root Cause**

From the operator.log, we can see:

```bash
Character A is neither a decimal digit number, decimal point, nor "e" notation exponential mark.
```

This means, “ACTOKEY” is an invalid value for this field. But the system doesn’t exhibit any information to remind the user of that.

# Alarm59-75

Test Info: trial-03-0056/0001, trial-03-0055/0002, trial-05-0035/0001, trial-05-0034/0003, trial-06-0007/0002, trial-06-0006/0006, 06-0023/0001, 06-0022/0004, trial-06-0029/0006, 06-0030/0002, trial-05-0018/0002, trial-05-0017/0002, trial-04-0045/0001, trial-04-0046/0001, trial-01-0054/0007, trial-01-0004/0002, trial-01-0003/0005

## What happened

Acto changes:

- root['spec']['jobManager']['podTemplate'][spec][volumes][0][ephemeral][volumeClaimTemplate][spec][resources][limits][ACTOKEY] from "NotPresent" to "1000m".

No system state change.

## Categorization

Misoperation alarm

## **Root Cause - Missing required values**

From operation log:

- spec.template.spec.volumes[0].ephemeral.volumeClaimTemplate.spec.accessModes: Required value: at least 1 access mode is required
- spec.template.spec.volumes[0].ephemeral.volumeClaimTemplate.spec.resources[storage]: Required value
- spec.template.spec.volumes[0].name: Required value

Which indicates us the customer resources specification is missing those required values, it’s a misoperation.

# Alarm76-78

Test Info: trial-01-0019/0001, trial-07-0033/0001, trial-07-0032/0002, trial-00-0018/0003

## What happened

Acto changes:

- root['spec']['jobManager']['podTemplate'][spec][preemptionPolicy] from “notPresent” to “Never”.

From the generation.json, we see:

```json
"message": "deployment: test-cluster replicas [None] ready_replicas [None], test-cluster condition [Available] status [False] message [Deployment does not have minimum availability.]"
        
```

## Categorization

Misoperation alarm

## **Root Cause**

From the event.json, we can see:

- the string value of PreemptionPolicy (Never) must not be provided in pod spec; priority admission controller computed PreemptLowerPriority from the given PriorityClass name"

or

- the integer value of priority (2) must not be provided in pod spec; priority admission controller computed 0 from the given PriorityClass name",

That is, the PreemptionPolicy value is calculated and configured internal the system, users don’t need to configure it explicitly. 
            

# Alarm79

Test info: trial-06-0027/0001

## What happened

Acto changes 

root['spec']['podTemplate'][spec][affinity][podAffinity [requiredDuringSchedulingIgnoredDuringExecution][0][labelSelector][matchExpressions][0][key] from NotPresent to "app.kubernetes.io/name".

"message": "0/4 nodes are available: 1 node(s) had untolerated taint {node-role.kubernetes.io/control-plane: }, 3 node(s) didn't match pod affinity rules. preemption: 0/4 nodes are available: 4 Preemption is not helpful for scheduling..".

## Categorization

Misoperation alarm

## Root Cause

The desired Affinity cannot be satisfied in the current cluster state. The operator fails to reject the erroneous desired state.

# Alarm 80-81

Test info: trial-02-0008/0001, trial-04-0060/0001

## What happened

Acto changed root['spec']['podTemplate'][spec][nodeSelector][ACTOKEY] from NotPresent to "", or from NotPresent to"ACTOKEY".

The system reports message='deployment: test-cluster replicas [1] ready_replicas [None], test-cluster condition [Available] status [False] message [Deployment does not have minimum availability.]’

## Categorization

Misoperation alarm

## **Root Cause**

The cluster should have nodes with certain labels then the user can specify the label in the nodeSelector field. In this case, the cluster doesn’t have a node with “ACTOKEY” as the label.