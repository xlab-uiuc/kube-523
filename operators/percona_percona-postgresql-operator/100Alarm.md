## Alarm -1
- Trial: trial-00-0000
- Type: False Alarm
### What happened
Tried to add `ACTOKEY` to `root['spec']['dataSource'][pgbackrest][options][0]` field.
It leads to unhealthy state of pods.
### Root Cause
The command doesn't allow parameters. ACTOKEY is considered invalid.
### Expected Behavior
`ACTOKEY` shows up in the system state.

## Alarm -2
- Trial: trial-00-0017
- Type: Misoperation
### What happend
Tried to added `ACTOKEY` to `root['spec']['backups'][pgbakrest][jobs][limits]`
Error message is `Found no matching fields for input`.
### Root Cause
`ACTOKEY` is not an valid ephemeral storage. So still this fields is set to tmpDirSizeLimitGTE320 = resouce.MustParse("1.5Gi")
### Expected Behavior
The related fields should show `limits = ACTOKEY` in system state.

## Alarm-3
- Trial: trial 00-0006
- Type: Misoperation
### What happened.
Tried to delete `root['spec']['dataSource']['volumes']['pgWALVolume']`. It leads to pod in unhealthy state.

Error message is "message": "0/4 nodes are available: persistentvolumeclaim \"ACTOKEY\" not found. preemption: 0/4 nodes are available: 4 No preemption victims found for incoming pod..",
### Root Cause
PVC `ACTOKEY` doesn't exists. Only existed Pvcs can be bounded. While no resources are specified for the oracle. Therefor the PV cannot be created.
### Expected Behavior
Storage should be automatically created.

## Alarm-4
- Trial: trial 00-0005
- Type: True Alarm
### What happend 
backup pod crash. backup and restore pods unhealthy.
### Root Cause
back pod and repohost is alligned on different instances. While the ceritificate config is not availble for cross-instance communication, which leads to failure.

The problem is caused by local storage. There are replicated instances but only one local backup in current deployment config. A centralized backup like s3 will work. 

However it is critical that without back up, the cluster will still continue to work. But in this operator, the dependency makes the backup part a must, which is not flexible and leads to unstable behavior of system.
### Expected Behavior
Even there is a mismatch on cluster and backup cluster's replicas, backup can be achieved smoothly. Or without backup the system still needs to run well, instead of a failure in deployment.

## Alarm-5
- Trial: trial 00-0006
- Type: True Alarm
### What happend 
backup pod crash. backup and restore pods unhealthy.
### Root Cause
back pod and repohost is alligned on different instances. While the ceritificate config is not availble for cross-instance communication, which leads to failure.

The problem is caused by local storage. There are replicated instances but only one local backup in current deployment config. A centralized backup like s3 will work. 

However it is critical that without back up, the cluster will still continue to work. But in this operator, the dependency makes the backup part a must, which is not flexible and leads to unstable behavior of system.
### Expected Behavior
Even there is a mismatch on cluster and backup cluster's replicas, backup can be achieved smoothly. Or without backup the system still needs to run well, instead of a failure in deployment.

## Alarm-6
- Trial: trial 00-0007
- Type: True Alarm
### What happend 
Backup restore pod crashed. pgbackrest-restore pods are unhealthy.
### Root Cause
Oracles tried to set stanza value to "". While based on config, it can either be not present or has a valid, non empty string.
```
// The name of an existing pgBackRest stanza to use as the data source for the new PostgresCluster.
    // Defaults to `db` if not provided.
    // +kubebuilder:default="db"
    Stanza string `json:"stanza"`
```
### Expected Behavior
For empty string, it should be treated the same as `stanza` is not present. Therefore, the value still needs to be set to default value, instead of throwing an exception.

## Alarm-7
- Trial: trial-00-0008
- Type: True Alarm
### What happened
Backup restore pod crashed. pgbackrest-restore pods are unhealthy. No backup set found to restore
### Root Cause
Backup on the cluster failed. Backup and assigned repo is host on different nodes. 
Backup is trying to use a UNIX socket communication within same node. While here a cross-instance TCP connection is required.
### Expected Behavior
UNIX socket communication should be replaced. Either they could communicate across intances, or a repo should be hosted within same node along with a backup cluster.

## Alarm-8
- Trial: trial-00-0014
- Type: misoperation
### What happened
Acto tries to set up`root['spec']['backups'['pgbackres']['sidecars'][pgbackrest][resources[limits][ACTOKEY]` to 2000m. But stateful sets shows there are no ready replicas.
### Root Cause
`ACTOKEY` is not a standard resource type nor a qualified resourceEphemeralStorage.
### Expected Behavior

## Alarm-9
- Trial: trial-00-0015
- Type: misoperation
### What happened
Acto tries to set up`root['spec']['backups'['pgbackres']['sidecars'][pgbackrest][resources[limits][ACTOKEY]` to 2000m. But stateful sets shows there are no ready replicas.
### Root Cause
`ACTOKEY` is not a standard resource type nor a qualified resourceEphemeralStorage.
### Expected Behavior

## Alarm-10
- Trial: trial-00-0017
- Type: misoperation
### What happened
Acto tries to set up`root['spec']['backups']['pgbackrest']['jobs'][pgbackrest][resources][limits][ACTOKEY]` to 2000m. But found no matching.
### Root Cause
`ACTOKEY` is not a standard resource type nor a qualified resourceEphemeralStorage.
### Expected Behavior


## Alarm-11
- Trial: trial-00-0011
- Type: Misoperation
### What happened
Created 1000 replicas failed. System crashed and tried to recover. While it failed to coverage within 480 seconds.
### Root Cause
Each instance asks for 1Gi. Due to resource limit(CPU/resources/etc), kind cluster failed to initialize. It's an overloaded behavior.
### Expected Behavior

## Alarm-12
- Trial: trial-00-0018
- Type: Misoperation
### What happened
pod: test-cluster-move unhealthy.  HTTP probe failed with statuscode: 503.
### Root Cause
pvcName `ACTOKEY` is not a existed pvc nor a valid resource name.
### Expected Behavior

## Alarm-13
- Trial: trial-00-0020
- Type: Misoperation
### What happened
Backup restore pod crashed. pgbackrest-restore pods are unhealthy. No backup set found to restore
### Root Cause
ACTOKEY is an invalid resource/storage type. Thus stanza is failed to create.
### Expected Behavior
Create dataSource with storage 2000m.


## Alarm-14
- Trial: trial-00-0023
- Type: False Alarm
### What happened
PgBouncer's replicaSet has timeout progressing.
### Root Cause
An invalid sidecar container is added to proxy's config without an valid image, incuring the error.
### Expected Behavior
Create an valid sidecar.

## Alarm-15
- Trial: trial-00-0024
- Type: Misoperation
### What happened
Replica of repo host not reday. Backup pods are in unhealthy state.
### Root Cause
Tolerations are set with invalid config like ['effect'] = ACTOKEY. It causes repo-host failed to initalize.
### Expected Behavior
For such kind of value, a enumeration should be provided to avoid this kind of error.



## Alarm-16
- Trial: trial-00-0024
- Type: Misoperation
### What happened
Replica of repo host not reday. Backup pods are in unhealthy state.
### Root Cause
Tolerations are set with invalid config like ['effect'] = ACTOKEY. It causes repo-host failed to initalize.
### Expected Behavior
For such kind of value, a enumeration should be provided in CRD to avoid this kind of error.

## Alarm-17
- Trial: trial-00-0025
- Type: Misoperation
### What happened
Replica of repo host not reday. Backup pods are in unhealthy state.
### Root Cause
Tolerations are set with invalid config like ['effect'] = ACTOKEY. It causes repo-host failed to initalize.
### Expected Behavior
For such kind of value, a enumeration should be provided in CRD to avoid this kind of error.

## Alarm-18
- Trial: trial-00-0026
- Type: Misoperation
### What happened
Replica of repo host not reday. Backup pods are in unhealthy state.
### Root Cause
Tolerations are set with invalid config like ['effect'] = ACTOKEY. It causes repo-host failed to initalize.
### Expected Behavior
For such kind of value, a enumeration should be provided in CRD to avoid this kind of error.


## Alarm-19
- Trial: trial-00-0028
- Type: False Alarm
### What happened
Restart pod in cluster failed. Cluster crashed.
### Root Cause
Container cannot be initialized without image provided.

## Alarm-20
- Trial: trial-00-0030
- Type: misoperation
### What happened
Acto tries to set up`root['spec']['backups'['pgbackres']['sidecars'][pgbackrest][resources][request][ACTOKEY]` to 2000m. Replicas not ready.
### Root Cause
`ACTOKEY` is not a standard resource type nor a qualified resourceEphemeralStorage.
### Expected Behavior


## Alarm-21
- Trial: trial-00-0031
- Type: misoperation
### What happened
Acto tries to set up`root['spec']['backups'['pgbackres']['sidecars'][pgbackrest][resources][request][ACTOKEY]` to 2000m. Replicas not ready.
### Root Cause
`ACTOKEY` is not a standard resource type nor a qualified resourceEphemeralStorage.
### Expected Behavior

## Alarm-22
- Trial: trial-00-0035
- Type: false alarm
### What happened
Replicas not ready.
### Root Cause
The prompt tries to set invalid-service for gprc, leading to cluster failed to initialize.
### Expected Behavior

## Alarm-22
- Trial: trial-00-0036
- Type: false alarm
### What happened
Replicas not ready.
### Root Cause
The prompt tries to set invalid-name for config, leading to cluster failed to initialize.
### Expected Behavior


## Alarm-23
- Trial: trial-01-0001
- Type: false alarm
### What happened
Pod crashes when tried to set invalid-name for DataSourceRef
### Root Cause
DataSourceRef preserves all values, and generates an error if a disallowed value is specified.
### Expected Behavior

## Alarm-23
- Trial: trial-01-0002
- Type: Misoperation
### What happened
Replicas not ready when tring to add config to initContainers.
### Root Cause
Image must be provided when intializing containers.
### Expected Behavior

## Alarm-23
- Trial: trial-01-0003
- Type: Misoperation
### What happened
Replicas not ready when tring to add config to initContainers.
### Root Cause
Image must be provided when intializing containers.
### Expected Behavior

## Alarm-23
- Trial: trial-01-0004
- Type: False Alarm
### What happened
Pod crashes when tring to set configMapRef to invalid-name in init-containers section.
### Root Cause
Image must be provided when intializing containers. Invalid-name is invalid value for the field.
### Expected Behavior

## Alarm-24
- Trial: trial-01-0005
- Type: False Alarm
### What happened
Replicas not ready when tring to set ['volumeMounts']['name'] to invalid-name.
### Root Cause
Mount path is not provided thus failed to find the resources.
### Expected Behavior

## Alarm-25
- Trial: trial-02-0001
- Type: misoperation
### What happened
Acto tries to set up`root['spec']['backups'['pgbackres']['sidecars'][pgbackrest][resources][request][ACTOKEY]` to 2000m. Replicas not ready and pod crashes.
### Root Cause
`ACTOKEY` is not a standard resource type nor a qualified resourceEphemeralStorage.
### Expected Behavior

## Alarm-26
- Trial: trial-02-0002
- Type: misoperation
### What happened
Acto tries to decrease quantity in `root['spec']['backups'['pgbackres']['sidecars'][pgbackrest][resources][request][ACTOKEY]`. Replicas not ready and pod crashes.
### Root Cause
`ACTOKEY` is not a standard resource type nor a qualified resourceEphemeralStorage.
### Expected Behavior

## Alarm-27
- Trial: trial-02-0004
- Type: True Alarm
### What happened
Enabled pmm. Pod crashed and replica sets not found.
### Root Cause
Backup on the cluster failed. Backup and assigned repo is host on different nodes. 
Backup is trying to use a UNIX socket communication within same node. While here a cross-instance TCP connection is required.
### Expected Behavior
UNIX socket communication should be replaced. Either they could communicate across intances, or a repo should be hosted within same node along with a backup cluster.

## Alarm-28
- Trial: trial-02-0005
- Type: True Alarm
### What happened
Enabled pmm. Pod crashed and replica sets not found.
### Root Cause
Backup on the cluster failed. Backup and assigned repo is host on different nodes. 
Backup is trying to use a UNIX socket communication within same node. While here a cross-instance TCP connection is required.
### Expected Behavior
UNIX socket communication should be replaced. Either they could communicate across intances, or a repo should be hosted within same node along with a backup cluster.

## Alarm-29
- Trial: trial-02-0006
- Type: True Alarm
### What happened
Enabled pmm. Pod crashed and replica sets not found.
### Root Cause
Backup on the cluster failed. Backup and assigned repo is host on different nodes. 
Backup is trying to use a UNIX socket communication within same node. While here a cross-instance TCP connection is required.
### Expected Behavior
UNIX socket communication should be replaced. Either they could communicate across intances, or a repo should be hosted within same node along with a backup cluster.

## Alarm-30
- Trial: trial-02-0008
- Type: Misoperation
### What happened
Acto tries to set up`root['spec']['backups'['pgbackres']['sidecars'][pgbackrest][resources][request][ACTOKEY]` to 2000m. Replicas not ready.
### Root Cause
`ACTOKEY` is not a standard resource type nor a qualified resourceEphemeralStorage.
### Expected Behavior

## Alarm-31
- Trial: trial-02-0009
- Type: Misoperation
### What happened
Acto tries to decrease quantity in `root['spec']['backups'['pgbackres']['sidecars'][pgbackrest][resources][request][ACTOKEY]`. Replicas not ready and pod crashes.
### Root Cause
`ACTOKEY` is not a standard resource type nor a qualified resourceEphemeralStorage.
### Expected Behavior

## Alarm-32
- Trial: trial-02-0011
- Type: False Alarm
### What happened
Acto tries to set root['spec']['backups']['pgbakrest']['image'] from a valid image into 'ACTOKEY'
### Root Cause
`ACTOKEY` is not an invalid image value.
### Expected Behavior

## Alarm-33
- Trial: trial-03-0006
- Type: True Alarm
### What happened
Backup restore pod crashed because of resourceVersion mismatch. pgbackrest-restore pods are unhealthy. 
### Root Cause
Backup on the cluster failed. Backup and assigned repo is host on different nodes. 
Backup is trying to use a UNIX socket communication within same node. While here a cross-instance TCP connection is required.
### Expected Behavior
UNIX socket communication should be replaced. Either they could communicate across intances, or a repo should be hosted within same node along with a backup cluster.

## Alarm-34
- Trial: trial-03-0007
- Type: True Alarm
### What happened
Backup restore pod crashed because of resourceVersion mismatch. pgbackrest-restore pods are unhealthy. 
### Root Cause
Backup on the cluster failed. Backup and assigned repo is host on different nodes. 
Backup is trying to use a UNIX socket communication within same node. While here a cross-instance TCP connection is required.
### Expected Behavior
UNIX socket communication should be replaced. Either they could communicate across intances, or a repo should be hosted within same node along with a backup cluster.

## Alarm-35
- Trial: trial-03-0008
- Type: True Alarm
### What happened
Backup restore pod crashed because of resourceVersion mismatch. pgbackrest-restore pods are unhealthy. 
### Root Cause
Backup on the cluster failed. Backup and assigned repo is host on different nodes. 
Backup is trying to use a UNIX socket communication within same node. While here a cross-instance TCP connection is required.
### Expected Behavior
UNIX socket communication should be replaced. Either they could communicate across intances, or a repo should be hosted within same node along with a backup cluster.


## Alarm-36
- Trial: trial-03-0011
- Type: True Alarm
### What happened
Backup restore pod crashed because of resourceVersion mismatch. pgbackrest-restore pods are unhealthy. 
### Root Cause
Backup on the cluster failed. Backup and assigned repo is host on different nodes. 
Backup is trying to use a UNIX socket communication within same node. While here a cross-instance TCP connection is required.
### Expected Behavior
UNIX socket communication should be replaced. Either they could communicate across intances, or a repo should be hosted within same node along with a backup cluster.

## Alarm-37
- Trial: trial-03-0012
- Type: misoperation
### What happened
Acto tries to set `root[spec][secrets][customTLSSecret][name] to invalid name Replicas not ready and pod crashes.
### Root Cause
CusomTLSSecret fields encrypts connections to PgBouncer. Being an invalid value will lead to crash.
### Expected Behavior

## Alarm-38
- Trial: trial-03-0013
- Type: Misoperation
### What happened
Acto tries to set up`root['spec'][proxy][pgBouncer][sidecars][resources][requests][ACTOKEY]` to 2000m. Replicas not ready.
### Root Cause
`ACTOKEY` is not a standard resource type nor a qualified resourceEphemeralStorage.
### Expected Behavior

## Alarm-39
- Trial: trial-03-0014
- Type: Misoperation
### What happened
Acto tries to decrease quantity in `root['spec'][proxy][pgBouncer][sidecars][resources][requests][ACTOKEY]`. Replicas not ready and pod crashes.
### Root Cause
`ACTOKEY` is not a standard resource type nor a qualified resourceEphemeralStorage.
### Expected Behavior

## Alarm-40
- Trial: trial-03-0015
- Type: false alarm
### What happened
Replicas not ready.
### Root Cause
The prompt tries to set invalid grpc action for grpc field, which will lead to crash.
### Expected Behavior

## Alarm-41
- Trial: trial-03-0019
- Type: True Alarm
### What happened
Pod crash when tries to set repo schedule.
### Root Cause
Backup on the cluster failed. Backup and assigned repo is host on different nodes. 
Backup is trying to use a UNIX socket communication within same node. While here a cross-instance TCP connection is required. When creating stanza, db-backup.lock cannot be acquired.
### Expected Behavior
UNIX socket communication should be replaced. Either they could communicate across intances, or a repo should be hosted within same node along with a backup cluster.


## Alarm-42
- Trial: trial-03-0020
- Type: True Alarm
### What happened
Pod crash when tries to set repo schedule.
### Root Cause
Backup on the cluster failed. Backup and assigned repo is host on different nodes. 
Backup is trying to use a UNIX socket communication within same node. While here a cross-instance TCP connection is required. When creating stanza, db-backup.lock cannot be acquired.
### Expected Behavior
UNIX socket communication should be replaced. Either they could communicate across intances, or a repo should be hosted within same node along with a backup cluster.


## Alarm-43
- Trial: trial-03-0023
- Type: True Alarm
### What happened
Pod crash when initalizing.
### Root Cause
Backup on the cluster failed. Backup and assigned repo is host on different nodes. 
Backup is trying to use a UNIX socket communication within same node. While here a cross-instance TCP connection is required. When creating stanza, db-backup.lock cannot be acquired.
### Expected Behavior
UNIX socket communication should be replaced. Either they could communicate across intances, or a repo should be hosted within same node along with a backup cluster.


## Alarm-44
- Trial: trial-03-0027
- Type: False Alarm
### What happened
Acto tries to set root['spec']['backups']['pgbakrest']['image'] from a valid image into 'ACTOKEY'
### Root Cause
`ACTOKEY` is not an invalid image value.
### Expected Behavior


## Alarm-45
- Trial: trial-03-0029
- Type: Misoperation
### What happened
Replica of repo host not reday. Backup pods are in unhealthy state.
### Root Cause
Tolerations are set with invalid config like ['effect'] = ACTOKEY. It causes repo-host failed to initalize.
### Expected Behavior
For such kind of value, a enumeration should be provided to avoid this kind of error.

## Alarm-46
- Trial: trial-03-0030
- Type: Misoperation
### What happened
Replica of repo host not reday. Backup pods are in unhealthy state.
### Root Cause
dataSource's repo must be existed, valid repo with storage source clarified.
### Expected Behavior

## Alarm-47
- Trial: trial-03-0031
- Type: Misoperation
### What happened
Replica of repo host not reday. Backup pods are in unhealthy state.
### Root Cause
dataSource's repo must be existed, valid repo with storage source clarified.
### Expected Behavior

## Alarm-48
- Trial: trial-03-0032
- Type: Misoperation
### What happened
Replica of repo host not reday. Backup pods are in unhealthy state.
### Root Cause
dataSource's repo must be existed, valid repo with storage source clarified.
### Expected Behavior

## Alarm-49
- Trial: trial-03-0038
- Type: False Alarm
### What happened
Replica of repo host not reday. Backup pods are in unhealthy state. ['topologySpreadConstraint']['whenUnsatisfiable'] is trying to set to `invalid-name`
### Root Cause
The field ['topologySpreadConstraint']['whenUnsatisfiable'] must follow K8S's contraint on it, where only `Do not schedule` or `Schedule Anyway` is allowed.
### Expected Behavior

## Alarm-50
- Trial: trial-03-0039
- Type: False Alarm
### What happened
Replica of repo host not reday. Backup pods are in unhealthy state. ['topologySpreadConstraint']['whenUnsatisfiable'] is trying to set to `invalid-name`
### Root Cause
The field ['topologySpreadConstraint']['whenUnsatisfiable'] must follow K8S's contraint on it, where only `Do not schedule` or `Schedule Anyway` is allowed.
### Expected Behavior


## Alarm-51
- Trial: trial-03-0039
- Type: True Alarm
### What happened
Pod crash when tries to set repo schedule.
### Root Cause
Backup on the cluster failed. Backup and assigned repo is host on different nodes. 
Backup is trying to use a UNIX socket communication within same node. While here a cross-instance TCP connection is required. When creating stanza, db-backup.lock cannot be acquired.
### Expected Behavior
UNIX socket communication should be replaced. Either they could communicate across intances, or a repo should be hosted within same node along with a backup cluster.

## Alarm-51
- Trial: trial-03-0040
- Type: False Alarm
### What happened
Replica of repo host not reday. Backup pods are in unhealthy state. [`resizePolicy`][`restartPolicy`] tries to set to `k8s-invalid-policy`
### Root Cause
The field [`resizePolicy`][`restartPolicy`]must follow K8S's contraint on it, where only `Do not schedule` or `Schedule Anyway` is allowed.
### Expected Behavior

## Alarm-52
- Trial: trial-03-0042
- Type: False Alarm
### What happened
Replica of repo host not reday. Backup pods are in unhealthy state. [`spec`][`instances`][`sidecars`][`lifecycle`][`postStart`][`httpGet`][`httpHeaders`][`name`] tries to set to `k8s-invalid-name`
### Root Cause
The field [`resizePolicy`][`restartPolicy`]must follow K8S's contraint on it, where only `Do not schedule` or `Schedule Anyway` is allowed.
### Expected Behavior

## Alarm-53
- Trial: trial-03-0046
- Type: False Alarm
### What happened
Replica of repo host not reday. Backup pods are in unhealthy state. [`spec`][`instances`][`initContainers`][`lifecycle`][`postStart`][`httpGet`][`httpHeaders`][`name`] tries to set to `k8s-invalid-name`
### Root Cause
The field [`resizePolicy`][`restartPolicy`]must follow K8S's contraint on it, where only `Do not schedule` or `Schedule Anyway` is allowed.
### Expected Behavior

## Alarm-54
- Trial: trial-03-0049
- Type: False Alarm
### What happened
Replica of repo host not reday. Backup pods are in unhealthy state. [`spec`][`instances`][`initContainers`][`lifecycle`][`postStart`][`httpGet`][`httpHeaders`][`name`] tries to set to `k8s-invalid-name`
### Root Cause
The field [`resizePolicy`][`restartPolicy`]must follow K8S's contraint on it, where only `Do not schedule` or `Schedule Anyway` is allowed.
### Expected Behavior


## Alarm-55
- Trial: trial-03-0051
- Type: False Alarm
### What happened
Replica of repo host not reday. Backup pods are in unhealthy state. ['topologySpreadConstraint']['whenUnsatisfiable'] is trying to set to `invalid-name`
### Root Cause
The field ['topologySpreadConstraint']['whenUnsatisfiable'] must follow K8S's contraint on it, where only `Do not schedule` or `Schedule Anyway` is allowed.
### Expected Behavior

## Alarm-56
- Trial: trial-03-0052
- Type: True Alarm
### What happened
Pod crash when tries to set repo schedule.
### Root Cause
Backup on the cluster failed. Backup and assigned repo is host on different nodes. 
Backup is trying to use a UNIX socket communication within same node. While here a cross-instance TCP connection is required. When creating stanza, db-backup.lock cannot be acquired.
### Expected Behavior
UNIX socket communication should be replaced. Either they could communicate across intances, or a repo should be hosted within same node along with a backup cluster.

## Alarm-57
- Trial: trial-03-0056
- Type: Misoperation
### What happened
Replica of repo host not reday. Backup pods are in unhealthy state.
### Root Cause
dataSource must be set to invalid resource with storage/volume clarified.
### Expected Behavior

## Alarm-58
- Trial: trial-03-0055
- Type: False Alarm
### What happened
Replica of repo host not reday. Backup pods are in unhealthy state. [`spec`][`instances`][`initContainers`][`lifecycle`][`preStop`][`httpGet`][`httpHeaders`][`name`] tries to set to `k8s-invalid-name`
### Root Cause
The field [`resizePolicy`][`restartPolicy`]must follow K8S's contraint on it, where only `Do not schedule` or `Schedule Anyway` is allowed.
### Expected Behavior


## Alarm-59
- Trial: trial-03-0055
- Type: Misoperation
### What happened
Replica of repo host not reday. Backup pods are in unhealthy state.  Tries to add new backup repo with azure.
### Root Cause
Azure related config like account/secret must be provided in order to backup on cloud.
### Expected Behavior

## Alarm-60
- Trial: trial-03-0060
- Type: misoperation
### What happened
Acto tries to set up`root['spec']['backups'['pgbackres']['repo'][volume][volumeClamSpec][resources][limits][ACTOKEY]` to 2000m. But stateful sets shows there are no ready replicas.
### Root Cause
`ACTOKEY` is not a standard resource type nor a qualified resourceEphemeralStorage.
### Expected Behavior

## Alarm-61
- Trial: trial-03-0061
- Type: misoperation
### What happened
Acto tries to decrease `root['spec']['backups'['pgbackres']['repo'][volume][volumeClamSpec][resources][limits][ACTOKEY]` . But stateful sets shows there are no ready replicas.
### Root Cause
`ACTOKEY` is not a standard resource type nor a qualified resourceEphemeralStorage.
### Expected Behavior

## Alarm-62
- Trial: trial-03-0072
- Type: Misoperation
### What happened
Replica of repo host not reday. Backup pods are in unhealthy state.  Tries to add new backup repo with s3.
### Root Cause
S3 related config like key/secret must be provided in order to backup on cloud.
### Expected Behavior

## Alarm-63
- Trial: trial-03-0073
- Type: Misoperation
### What happened
Replica of repo host not reday. Backup pods are in unhealthy state.  Tries to add new backup repo with s3.
### Root Cause
S3 related config like key/secret must be provided in order to backup on cloud.
### Expected Behavior

## Alarm-64
- Trial: trial-03-0074
- Type: Misoperation
### What happened
Replica of repo host not reday. Backup pods are in unhealthy state.  Tries to add new backup repo with s3.
### Root Cause
S3 related config like key/secret must be provided in order to backup on cloud.
### Expected Behavior

## Alarm-65
- Trial: trial-03-0076
- Type: Misoperation
### What happened
Replica of repo host not reday. Backup pods are in unhealthy state.  Tries to add new backup repo with s3.
### Root Cause
S3 bucket must be provided with non-empty value to achieve successful connection
### Expected Behavior


## Alarm-66
- Trial: trial-03-0078
- Type: misoperation
### What happened
Acto tries to set[`spec`][`dataSource`][`pgbackrest`][`options`] to ACTOKEY
### Root Cause
It should be any valid pgBackRest options.
### Expected Behavior


## Alarm-67
- Trial: trial-03-0079
- Type: Misoperation
### What happened
Replica of repo host not reday. Backup pods are in unhealthy state.
### Root Cause
dataSource's repo must be existed, valid repo with storage source clarified.
### Expected Behavior

## Alarm-67
- Trial: trial-03-0080
- Type: misoperation
### What happened
Acto tries to set[`spec`][`Instances`][`sidecars`][`env`] [`name`] to Invalid-name. Pod crash and is in unhealthy state.
### Root Cause
ENV should be valid environment variables that invoke PostgreSQL utilities.
### Expected Behavior

## Alarm-68
- Trial: trial-03-00084
- Type: misoperation
### What happened
Acto tries to increase quantity in `root['spec']['instances'][dataVolumeClaimSpec][resources][request][ACTOKEY]`. Replicas not ready and pod crashes.
### Root Cause
`ACTOKEY` is not a standard resource type nor a qualified resourceEphemeralStorage.
### Expected Behavior

## Alarm-69
- Trial: trial-03-00085
- Type: misoperation
### What happened
Acto tries to decrease quantity in `root['spec']['instances'][dataVolumeClaimSpec][resources][request][ACTOKEY]`. Replicas not ready and pod crashes.
### Root Cause
`ACTOKEY` is not a standard resource type nor a qualified resourceEphemeralStorage.
### Expected Behavior

## Alarm-70
- Trial: trial-03-00086
- Type: misoperation
### What happened
Pod is in unhealthy state and is not ready. Acto tries to changes the directory and pvc that pgDataVolume points to.
### Root Cause
Only existed Pvcs can be bounded. While no resources are specified for the oracle. Therefor the PV cannot be created.
### Expected Behavior

## Alarm-71
- Trial: trial-03-00088
- Type: misoperation
### What happened
Pod is in unhealthy state and is not ready. Acto tries to changes the directory and pvc that pgDataVolume points to.
### Root Cause
Only existed Pvcs can be bounded. While no resources are specified for the oracle. Therefor the PV cannot be created.
### Expected Behavior

## Alarm-72
- Trial: trial-03-0090
- Type: True Alarm
### What happened
Backup restore pod crashed. pgbackrest-restore pods are unhealthy. No backup set found to restore
### Root Cause
Backup on the cluster failed. Backup and assigned repo is host on different nodes. 
Backup is trying to use a UNIX socket communication within same node. While here a cross-instance TCP connection is required.
### Expected Behavior
UNIX socket communication should be replaced. Either they could communicate across intances, or a repo should be hosted within same node along with a backup cluster.

## Alarm-71
- Trial: trial-03-00091
- Type: misoperation
### What happened
Acto tries to increase quantity in `root['spec']['instances'][dataVolumeClaimSpec][resources][request][ACTOKEY]`. Replicas not ready and pod crashes.
### Root Cause
`ACTOKEY` is not a standard resource type nor a qualified resourceEphemeralStorage.
### Expected Behavior

## Alarm-72
- Trial: trial-03-00093
- Type: misoperation
### What happened
Acto tries to decrease quantity in `root['spec']['instances'][dataVolumeClaimSpec][resources][request][ACTOKEY]`. Replicas not ready and pod crashes.
### Root Cause
`ACTOKEY` is not a standard resource type nor a qualified resourceEphemeralStorage.
### Expected Behavior

## Alarm-73
- Trial: trial-03-00104
- Type: misoperation
### What happened
Acto tries to increase quantity in `root['spec']['instances'][dataVolumeClaimSpec][resources][request][ACTOKEY]`. Replicas not ready and pod crashes.
### Root Cause
`ACTOKEY` is not a standard resource type nor a qualified resourceEphemeralStorage.
### Expected Behavior

## Alarm-74
- Trial: trial-03-00105
- Type: misoperation
### What happened
Acto tries to decrease quantity in `root['spec']['instances'][dataVolumeClaimSpec][resources][request][ACTOKEY]`. Replicas not ready and pod crashes.
### Root Cause
`ACTOKEY` is not a standard resource type nor a qualified resourceEphemeralStorage.
### Expected Behavior

## Alarm-75
- Trial: trial-03-0094
- Type: misoperation
### What happened
 Replicas not ready and pod crashes when trying to initalize Containers.
### Root Cause
Valid port and port name must be provided to initalization, or it will cause pod to crash.
### Expected Behavior

## Alarm-76
- Trial: trial-03-0095
- Type: False Alarm
### What happened
Replicas not ready when initializing containers.
### Root Cause
An invalid sidecar container is added to proxy's config without an valid image, incuring the error. Also for hugepages, cpu memory must be provided.
### Expected Behavior


## Alarm-77
- Trial: trial-03-0096
- Type: False Alarm
### What happened
Replicas not ready when initializing containers.
### Root Cause
An invalid sidecar container is added to proxy's config without an valid image, incuring the error. 
### Expected Behavior

## Alarm-78
- Trial: trial-03-0098
- Type: True Alarm
### What happened
Pod crash when tring to set repo schedule.
### Root Cause
Backup on the cluster failed. Backup and assigned repo is host on different nodes. 
Backup is trying to use a UNIX socket communication within same node. While here a cross-instance TCP connection is required. When creating stanza, db-backup.lock cannot be acquired.
### Expected Behavior
UNIX socket communication should be replaced. Either they could communicate across intances, or a repo should be hosted within same node along with a backup cluster.

## Alarm-79
- Trial: trial-03-0101
- Type: True Alarm
### What happened
Pod crash when tring to enable openshift.
### Root Cause
Backup on the cluster failed. Backup and assigned repo is host on different nodes. 
Backup is trying to use a UNIX socket communication within same node. While here a cross-instance TCP connection is required. When creating stanza, db-backup.lock cannot be acquired.
### Expected Behavior
"Optionally, you can add PostgreSQL Users secrets and TLS certificates to OpenShift. If you don’t, the Operator will create the needed users and certificates automatically, when you create the database cluster."

## Alarm-80
- Trial: trial-03-0102
- Type: True Alarm
### What happened
Pod crash when tring to enable openshift.
### Root Cause
Backup on the cluster failed. Backup and assigned repo is host on different nodes. 
Backup is trying to use a UNIX socket communication within same node. While here a cross-instance TCP connection is required. When creating stanza, db-backup.lock cannot be acquired.
### Expected Behavior
"Optionally, you can add PostgreSQL Users secrets and TLS certificates to OpenShift. If you don’t, the Operator will create the needed users and certificates automatically, when you create the database cluster."

## Alarm-81
- Trial: trial-03-00106
- Type: misoperation
### What happened
Acto tries to set `root['spec']['backups']['pgbackrest']['jobs']['tolerations'][0][effect]` to ACTOKEY and pod crashed.
### Root Cause
`ACTOKEY` is not an valid effect.
### Expected Behavior

## Alarm-82
- Trial: trial-03-00107
- Type: misoperation
### What happened
Acto tries to set `root['spec']['backups']['pgbackrest']['jobs']['tolerations'][0][effect]` to ACTOKEY and pod crashed.
### Root Cause
`ACTOKEY` is not an valid effect.
### Expected Behavior

