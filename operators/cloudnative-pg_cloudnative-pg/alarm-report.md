# Acto Test Result Report for CloudNative-PG (CNPG)

CNPG commit hash: `2b1b0e9563aeb40dbbd1f2d6f276a6671a0a1832`

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

When Acto adds `ACTOKEY:ACTOKEY` to `affinity.nodeSelector`, a pod becomes unhealthy.

### Categorization

This is classified as a misoperation.

### Root Cause

Since the newly added node affinity rule does not match any node, it is impossible to reconcile the system to the desired state. CNPG could have inspected all nodes in the cluster, determined that the new spec cannot be fulfilled, and rejected it therefore.

## Alarm 3

### Test Case Info

Trial number: **trial-01-0019/0001** and **trial-01-0020/0001** (these are actually the same test case)

When Acto sets `schedulerName` to `ACTOKEY`, a pod becomes unhealthy.

### Categorization

These are classified as misoperations.

### Root Cause

The specified scheduler does not exist, so CNPG is unable to schedule the pods. CNPG could have easily rejected this new spec by checking whether the scheduler exists.

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
