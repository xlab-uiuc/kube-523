# Alarms

# Alarm1

Test info: trial-00-0002/0000

## What happened
Connection failed, pod is requested to restart.
In generation.json we can observe:
```json
"health": {
    "message": "pod: stackgres-74f48b87d8-trzxp container [stackgres] restart_count [1]"
},
```
In event.json we can observe:
```json
"message": "Readiness probe failed: Get \"http://10.244.3.2:8080/q/health/ready\": dial tcp 10.244.3.2:8080: connect: connection refused",
```

## Categorization

Misoperation.

## **Root Cause**

Stackgres Operator website said:

```java
            .withReadinessProbe(new ProbeBuilder()
                .withNewHttpGet()
                .withPath("/q/health/ready")
                .withPort(new IntOrString(8080))
                .withScheme("HTTP")
                .endHttpGet()
                .withInitialDelaySeconds(0)
                .withPeriodSeconds(2)
                .withTimeoutSeconds(1)
                .build())
```

The root cause of this problem is that Kubernetes is unable to establish a connection to the specified IP address and port during the readiness probe. This issue typically arises due to either the application not being fully started or not listening on the specified IP and port, causing Kubernetes to refuse the connection.

## Expected Behavior

The expected behavior is for the readiness probe to successfully establish a connection to the specified IP address and port, confirming that the application within the Kubernetes pod is ready to receive traffic. 

---

# Alarm2

Test info: trial-00-0008/0000

## What happened
Connection failed, pod is requested to restart.
In generation.json we can observe:
```json
"health": {
    "message": "pod: stackgres-74f48b87d8-dkhvz container [stackgres] restart_count [1]"
},
```
In event.json we can observe:
```json
"message": "Readiness probe failed: Get \"http://10.244.3.2:8080/q/health/ready\": dial tcp 10.244.3.2:8080: connect: connection refused",
```

## Categorization

Misoperation.

## **Root Cause**

Same as Alarm1

## Expected Behavior

Same as Alarm1.

---

# Alarm3

Test info: trial-00-0011/0000

## What happened
Connection failed, pod is requested to restart.
In generation.json we can observe:
```json
"health": {
    "message": "pod: stackgres-74f48b87d8-lffk7 container [stackgres] restart_count [1]"
},
```
In event.json we can observe:
```json
"message": "Readiness probe failed: Get \"http://10.244.3.2:8080/q/health/ready\": dial tcp 10.244.3.2:8080: connect: connection refused",
```

## Categorization

Misoperation.

## **Root Cause**

Same as Alarm1.

## Expected Behavior

Same as Alarm1.

---

# Alarm4

est info: trial-00-0024/0000

## What happened
Connection failed, pod is requested to restart.
In generation.json we can observe:
```json
"health": {
    "message": "pod: stackgres-74f48b87d8-m8tzg container [stackgres] restart_count [1]"
},
```
In event.json we can observe:
```json
"message": "Readiness probe failed: Get \"http://10.244.1.2:8080/q/health/ready\": dial tcp 10.244.1.2:8080: connect: connection refused",
```

## Categorization

Misoperation

## **Root Cause**

Same as Alarm1.

## Expected Behavior

Same as Alarm1.

---

# Alarm5

Test info: trial-00-0025/0000

## What happened
Connection failed, pod is requested to restart.
In generation.json we can observe:
```json
"health": {
    "message": "pod: stackgres-74f48b87d8-cztg5 container [stackgres] restart_count [1]"
},
```
In event.json we can observe:
```json
"message": "Readiness probe failed: Get \"http://10.244.2.2:8080/q/health/ready\": dial tcp 10.244.2.2:8080: connect: connection refused",
```

## Categorization

Misoperation

## **Root Cause**

Same as Alarm1.

## Expected Behavior

Same as Alarm1.

---

# Alarm6
Connection failed, pod is requested to restart.
Test info: trial-00-0026/0000

## What happened

In the generation.json, we can see:

In generation.json we can observe:
```json
"health": {
    "message": "pod: stackgres-74f48b87d8-sgf5v container [stackgres] restart_count [1]"
},
```
In event.json we can observe:
```json
"message": "Readiness probe failed: Get \"http://10.244.3.2:8080/q/health/ready\": dial tcp 10.244.3.2:8080: connect: connection refused",
```

## Categorization

Misoperation

## **Root Cause**

Same as Alarm1.

## Expected Behavior

Same as Alarm1.

---

# Alarm7
Connection failed, pod is requested to restart.
Test info: trial-00-0028/0000

## What happened

In the generation.json, we can see:

In generation.json we can observe:
```json
"health": {
    "message": "pod: stackgres-74f48b87d8-hf7x8 container [stackgres] restart_count [1]"
},
```
In event.json we can observe:
```json
"message": "Readiness probe failed: Get \"http://10.244.3.2:8080/q/health/ready\": dial tcp 10.244.3.2:8080: connect: connection refused",
```

## Categorization

Misoperation

## **Root Cause**

Same as Alarm1.

## Expected Behavior

Same as Alarm1.

---

# Alarm8
Connection failed, pod is requested to restart.
Test info: trial-00-0032/0000

## What happened

In the generation.json, we can see:

In generation.json we can observe:
```json
"health": {
    "message": "pod: stackgres-74f48b87d8-b7zqt container [stackgres] restart_count [1]"
},
```
In event.json we can observe:
```json
"message": "Readiness probe failed: Get \"http://10.244.3.2:8080/q/health/ready\": dial tcp 10.244.3.2:8080: connect: connection refused",
```

## Categorization

Misoperation

## **Root Cause**

Same as Alarm1.

## Expected Behavior

Same as Alarm1.

---

# Alarm9
Connection failed, pod is requested to restart.
Test info: trial-02-0005/0000

## What happened

In the generation.json, we can see:

In generation.json we can observe:
```json
"health": {
    "message": "pod: stackgres-74f48b87d8-9gdsk container [stackgres] restart_count [1]"
},
```
In event.json we can observe:
```json
"message": "Readiness probe failed: Get \"http://10.244.3.2:8080/q/health/ready\": dial tcp 10.244.3.2:8080: connect: connection refused",
```

## Categorization

Misoperation

## **Root Cause**

Same as Alarm1.

## Expected Behavior

Same as Alarm1.

---

# Alarm10

Test info: trial-02-0017/0000

## What happened
Connection failed, pod is requested to restart.
In the generation.json, we can see:

In generation.json we can observe:
```json
"health": {
    "message": "pod: stackgres-74f48b87d8-mspmk container [stackgres] restart_count [1]"
},
```
In event.json we can observe:
```json
"message": "Readiness probe failed: Get \"http://10.244.2.2:8080/q/health/ready\": dial tcp 10.244.2.2:8080: connect: connection refused",
```

## Categorization

Misoperation

## **Root Cause**

Same as Alarm1.

## Expected Behavior

Same as Alarm1.

