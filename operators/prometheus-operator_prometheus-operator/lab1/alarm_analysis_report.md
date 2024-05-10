# Acto Test Result Report for Prometheus-operator

## Alarm 1

### Test Case Info

Trial number: **trial-02-0008/0007** and **trial-02-0009/0003**

Health oracle reports that the number of ready replicas of the StatefulSet named `prometheus-test-cluster` is 2, while the desired replicas is 3. It also reports that `prometheus-test-cluster-1`` pod crashed.

### Root Cause

Prometheus CRD has a field called `PageTitle`, which is the prometheus web page title. We see in `delta-007.log` that the pageTitle became empty from `ACTOKEY`, which caused error in starting of the pod and hence resulted in `CrashLoopBackOff`` error

### Categorization

This is an example of a misconfiguration


## Alarm 2

### Test Case Info

Trial number: **trial-02-0005/0002**

When Acto adds tolerations `test-key=test-value:INVALID_EFFECT`, pod creation of `prometheus-test-cluster-1` failed

### Root Cause

`spec.tolerations[0].effect` must have been `NoExecute` when `tolerationSeconds` is set. But Acto used `INVALID_EFFECT` which is an unsupported effect and hence resulted in pod creation failure.

### Categorization

This is an example of a misconfiguration


## Alarm 3

### Test Case Info

Trial number: **trial-02-0003/0001** **trial-02-0002/0004**

When Acto changes the restart policy to `Always`, deleting pod `prometheus-k8s-0` failed

### Root Cause

Acto tried to delete a container which did not exist or was in the process of being recreated.

### Categorization

This can be classified as misconfiguration or a false alarm


## Alarm 4

### Test Case Info

Trial number: **trial-02-0001/0001** and **trial-02-0000/0001**

When Acto adds TCP port to the readiness probe field of `initContainers`, pod creation of `prometheus-test-cluster-1` failed

### Root Cause

`spec.initContainers[1].readinessProbe` is not allowed for init container unless `restartPolicy` is set to Always

### Categorization

This is an example of a misconfiguration



## Alarm 5

### Test Case Info

Trial number: **ttrial-02-0012/0007**

Pod creation of `prometheus-test-cluster-1` failed when `spec.volumes[6].ephemeral.volumeClaimTemplate.spec.dataSourceRef` was changed by Acto in the input data.

### Root Cause
Atleast 1 access mode is required in the field `spec.volumes[6].ephemeral.volumeClaimTemplate.spec.accessModes` but Acto did not provide any. Also, invalid value of "gbybqzcwoh" was provided for `spec.volumes[6].ephemeral.volumeClaimTemplate.spec.dataSourceRef.kind`, which must be 'PersistentVolumeClaim'.


### Categorization

This is an example of a misconfiguration



## Alarm 6

### Test Case Info

Trial number: **trial-02-0010/0001**

Pod creation of `prometheus-test-cluster-1` failed when `spec.initContainers[1].env[0].valueFrom.secretKeyRef was included in the input data.

### Root Cause

`spec.initContainers[1].env[0].valueFrom.secretKeyRef.name` with value "INVALID_NAME" is invalid, since a lowercase RFC 1123 subdomain must consist of lower case alphanumeric characters, '-' or '.', and must start and end with an alphanumeric character

### Categorization

This is an example of a misconfiguration



## Alarm 7

### Test Case Info

Trial number: **trial-02-0013/0001**

When Acto adds HTTP port to the liveness probe field of `initContainers`, pod creation of `prometheus-test-cluster-1` failed

### Root Cause

`spec.initContainers[1].livenessProbe` is not allowed for init container unless `restartPolicy` is set to Always

### Categorization

This is an example of a misconfiguration


## Alarm 8

### Test Case Info

Trial number: **trial-02-0014/0005**

When Acto adds HTTP port to the `lifecycle` field of `initContainers`, pod creation of `prometheus-test-cluster-1` failed

### Root Cause

`spec.initContainers[1].lifecycle` is not allowed for init container unless `restartPolicy` is set to Always

### Categorization

This is an example of a misconfiguration



## Alarm 9

### Test Case Info

Trial number: **trial-00-0003/0009**

When Acto adds `VolumeClaimTemplate` to the input specification, pod creation of `prometheus-test-cluster-1` failed

### Root Cause

Atleast 1 access mode is required in the field `spec.volumes[6].ephemeral.volumeClaimTemplate.spec.accessModes` but Acto did not provide any.

### Categorization

This is an example of a misconfiguration



## Alarm 10

### Test Case Info

Trial number: **trial-00-0008/0005** and **trial-00-0009/0001**

Pod creation failed when `spec.topologySpreadConstraints` specification were modified by Acto in the input data

### Root Cause

Acto used unsupported value (random string) for `spec.topologySpreadConstraints[0].whenUnsatisfiable`, whereas the supported values are "DoNotSchedule" and "ScheduleAnyway". Furthermore, Acto specified wrong value for `spec.topologySpreadConstraints[0].minDomains`, a field which can be only used if `whenUnsatisfiable=DoNotSchedule`

### Categorization

This is an example of a misconfiguration


## Alarm 11

### Test Case Info

Trial number: **trial-00-0000/0003**

When Acto adds HTTP port to the `startupProbe` field of `initContainers`, pod creation of `prometheus-test-cluster-1` failed

### Root Cause

`spec.initContainers[1].startupProbe` is not allowed for init container unless `restartPolicy` is set to Always

### Categorization

This is an example of a misconfiguration


## Alarm 12

### Test Case Info

Trial number: **17ccfec57832ed1280e4312c1944ac0c**, **31e3906856b1b1784cdca98a996f8659**, **350a1f98495c2c4858a1ba3ea0a34503**, **3f3b81814702c7790c2570b9764e74be**, **f9bc6bfceaea89f5e2d6f27f3ec8239e**, **5891bc3189edae22c9a7e460f006830e**, **f3c4a64af362143eef991f352962f99e**, **e7592e2c3542efa9639d578e9af6041a**, **e55f4d953354360eda4caedcc1ebdf01**, **e55be9aad3dd67e24362ad3a88c50431**, **d282b6dd541f96a71c8679897e6bca2d**, **ca82863459a5f9b7f4a6be0fcf06c6c2**, **beb6bc35f03bc0cecada30301c0f282b**, **6c4ff8ffd2da1d02a174c764c57ba557**, **70e55602697a86d7a86bd6081802a572**, **78f72886c5fe5aab4cd3c85fe509b3c4**, **87ec6c0bc8a61835532996d2b7b92aa5**, **8971e2175e0d91f9c90a98277669bda3**

Differential oracle flags an error that the total number of secrets is not matching between the old state and the new state

### Root Cause

On digging deep, three secrets required for a specific pod `prometheus-test-cluster` was not present, since the pod creation had failed. Acto returns an error that the StatefulSet `acto-namespace/prometheus-test-cluster` was not found. Along with that, an error message saying `creating config failed: remote write 0: must provide Azure Managed Identity or Azure OAuth in the Azure AD config` was printed. The error is reported because the config file did not have or had wrong Azure AD/OAuth2 authentication specification (client id, url, secret, etc.) to enable Prometheus to perform remote write to Azure datastore. 

### Categorization

This is an example of misconfiguration



## Alarm 13

### Test Case Info

Trail number: **06a788116a12f6eb6aeaabacf5e9f56b**, **21b5aba7fc328dfacb8cc0c8063d4f78**, **572f9a248ad419f3385d37bc1a826d64**, **a6d45cd9ffef5aecc60dbfb38f2cc6a6**, **167d5b212ec0e50863a246629e93afd5**, **1b166613a4516abc3e95051d1a2f6b66**, **2177078ffb71d415354e721ac63da48d**, **239c449c613e9e4d315efd5a5c2f84ef**, **309b3aed3619800f6b30f292b9b32ca8**, **311124934f543564df26884dafdf8f7c**, **422d19c0b47839af32d7564d16b8e969**, **427cb20b0bcbe6ab5e526de8217c096c**, **4a277a20958f730739a2050fce4d9edb**, **4ba9da13506556187ed7198e90f07c45**, **4c80db14556c1abf81d5dd7938d393ce**, **4ca99f41d1780e6d4cea628be455242e**, **5392fb085528ead3d710e027ccf59f87**, **5577e7563cd3654f046d87537ed14da2** and the remaining differential oracle testcases

Differential oracle flags an error which occurred due to a mismatch in `prometheus-operator-input-hash`

### Root Cause

Since input CRs are different for each step in the Acto testing pipeline, the `prometheus-operator-input-hash` is automatically different. Hence, differential oracle flagged it as an alarm, which it should not have.

### Categorization

This is an example of false alarm