# Alarms

# Alarm1

Test info: trial-05-0044/0004

## What happened

Acto changes the flinkVersion from v1_17 to v1_13. But there’s no change in the system state.

## Categorization

False alarm.

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

So operator will not change the Flink version below 1.15. The transaction from 1.17 to 1.18, 1.16, 1.15 tested in other trails behave well. 

---

# Alarm2

Test info: trial-06-0046/0001

## What happened

Acto changes the flinkVersion from v1_17 to v1_14. But there’s no change in the system state.

## Categorization

False alarm

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

---

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

---

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

---

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