# Acto Test Result Report for CloudNative-PG (CNPG)

## Summary

Acto raised 19 alarms exposing 8 potential bugs, among which one is a true bug, 4 are misoperations (including one that can also be viewed as a bug), and 3 are false alarms.

Analysis on CNPG uses commit `2b1b0e9563aeb40dbbd1f2d6f276a6671a0a1832`.

## Alarm 1

### Test Case Info

Trial number: **trial-00-0002/0003**

CNPG uses `serviceAccountTemplate` as the template to create a service account from. When the service account is created with a custom label in `metadata.labels` and the label is later removed from `serviceAccountTemplate.metadata.labels`, CNPG does not correctly remove the label from the service account.

### Categorization

This is classified as a bug in CNPG.

### Root Cause

In `controllers/cluster_create.go`, the function `createOrPatchServiceAccount()` uses the function `MergeMetadata()` (line 488) to update the existing service account. `MergeMetadata()` essentially *merges* `serviceAccountTemplate.metadata.labels` into `metadata.labels` of the actual service account. Thus, existing values will never be deleted because the merge operation only handles updates and insertions.

## Alarm 2

### Test Case Info

Trial number: **trial-01-0010/0009**

When Acto adds `ACTOKEY:ACTOKEY` to `affinity.nodeSelector`, a Pod becomes unhealthy.

### Categorization

This is classified as a misoperation.

### Root Cause

Since the newly added node affinity rule does not match any node, it is impossible to reconcile the system to the desired state. CNPG could have inspected all nodes in the cluster, determined that the new spec cannot be fulfilled, and rejected it therefore.

## Alarm 3

### Test Case Info

Trial number: **trial-01-0019/0001** and **trial-01-0020/0001** (these are actually the same test case)

When Acto sets `schedulerName` to `ACTOKEY`, a Pod becomes unhealthy.

### Categorization

Trial number: **trial-00-0002/0003**

This is classified as a misoperation.

### Root Cause

The specified scheduler does not exist, so CNPG is unable to schedule the Pods. CNPG could have easily rejected this new spec by checking whether the scheduler exists.

## Alarm 4

### Test Case Info

Trial number: **trial-02-0000/0005**

When Acto adds a `backup.volumeSnapshot` object to the cluster spec, nothing changes.

### Categorization

This is classified as a false alarm.

### Root Cause

According to CNPG documentation, `backup.volumeSnapshot` configures the execution of volume snapshot backups. `backup` is another CR defined by CNPG and needs to be created on-demand when a database backup is desired. Here no `backup` is being created yet, so nothing is expected to happen.

## Alarm 5

### Test Case Info

Trial number: **trial-02-0001/0002** and **trial-02-0012/0003**

When Acto creates an object in `externalClusters` in the cluster spec (**trial-02-0001/0002**) or modifies it (**trial-02-0012/0003**), nothing changes.

### Categorization

These are classified as false alarms.

### Root Cause

According to CNPG documentation, items in `externalClusters` are the "connection parameters to an external cluster which is used in the other sections of the configuration". Here, there is no other section referring to this newly specified external cluster, so nothing is expected to happen.

In **trial-02-0012/0003**, the step to create an item in `externalClusters` did not raise an alarm. Rather, an alarm was raised when this item was later modified. This is because the creation step happened to set the `s3Credentials` field and CNPG created a corresponding resource. However, the later modification step did not introduce any immediately visible changes to the cluster.

## Alarm 6

## Test Case Info

Trial number: **trial-02-0008/0004** and **trial-02-0009/0002**

When Acto modifies `postgresql.shared_preload_libraries` to include `ACTOKEY`, a Pod crashes.

## Categorization

These are classified as misoperations.

## Root Cause

According to CNPG documentation, `postgresql.shared_preload_libraries` specifies shared libraries to be preloaded when launching PostgreSQL. This is needed for loading certain extensions.

This value is directly passed through to PostgreSQL in the form of PostgreSQL configuration `shared_preload_libraries`. Since `ACTOKEY` is not a valid shared library, PostgreSQL cannot start successfully.

CNPG could not do much to handle this type of failures. Even if it checks the presence of all files specified, the files could be invalid.

## Alarm 7

### Test Case Info

Trial number: **trial-05-0017/0006**

When Acto specifies `INVALID_NAME` as `bootstrap.initdb.secret.name`, a Pod becomes unhealthy.

## Categorization

This alarm is hard to classify. It is essentially a misoperation, but also has an aspect of a bug. 

## Root Cause

First and foremost, a system administrator is not supposed to edit `bootstrap` after creating the cluster. This section specifies how to initialize the cluster, and any modifications to it will simply be ignored by CNPG (see below). This behavior is undocumented.

In CNPG's source code, the `reconcile()` method in `ClusterReconciler` (line 156 in `cluster_controller.go`) calls invokes `reconcileResources()` at the very end. `reconcileResources()` in turn calls `reconcilePods()` which, as is name suggests, reconciles Pods.

`reconcilePods()` checks if there is no pod in the managed cluster. If so, it initializes the primary instance. Only during this initialization are options specified in `bootstrap` used. After the primary instance becomes alive, CNPG joins other nodes by invoking `/controller/manager join`, which clones data from the primary instance rather than initializing on its own.

Thus, we can confirm that CNPG is designed to never look at `bootstrap` again after the cluster is bootstrapped. If CNPG had strictly followed this design, nothing should happen anyway, even if `bootstrap` is updated to contain invalid data.

After done with bootstrapping, upscaling and downscaling operations, `reconcilePods()` invokes `handleRollingUpdate()` to update existing Pods one by one. CNPG does not always restart Pods though. It uses `isPodNeedingRollout()` to check if any Pod needs to be recreated. In this case, CNPG reports the reason for re-creating Pods as "original and target PodSpec differ in volumes".

This is because when determining whether re-creation of Pods is needed, CNPG constructs `targetPodSpec` using the function `CreateClusterPodSpec()` (line 600 in `cluster_upgrade.go`), then compares the target Pod spec with the current Pod spec. `CreateClusterPodSpec()` ends up calling `createPostgresVolumes()` to construct the value for `volumes` in the new Pod spec, where the user-specified Secret is added as a `volume` mounted into the new Pods.

Thus, CNPG thinks it is necessary to recreate Pods because new volumes are added.  However, when later the Pod controller attempts to create the new Pod requested by CNPG, it fails due to an invalid mount. The Pod will be indefinitely stuck in the `PodInitializing` state, thus unhealthy.

Thanks to the way CNPG handles Pod rollouts, only one Pod will be affected because CNPG does not continue reconcilation until the current rollout operation is finished.

While a system administrator should not make this happen, CNPG could have done better in this scenario, by explicitly and completely ignoring the `bootstrap` section when updating existing Pods.

## Alarm 8

## Test Case Info

Trial number: **trial-05-0025/0001**, **trial-05-0026/0001**, **trial-05-0027/0001** and **trial-05-0039/0001**

When Acto adds `postgresql.parameters`, nothing changes.

## Categorization

These are classified as false alarms.

## Root Cause

This field is for constructing extra parameters that CNPG should append to `postgresql.conf`. Changes will not be reflected on the cluster level as it only affects PostgreSQL's behavior.
