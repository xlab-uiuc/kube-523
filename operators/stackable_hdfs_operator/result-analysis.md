# Result analysis for Stackable HDFS Operator
Author: Jiyu Hu (jiyuhu2)

## What happened (#1)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["nameNodes", "roleGroups", "ACTOKEY" "podOverrides" "spec" "initContainers", "0", "env", "0", "valueFrom", "configMapKeyRef", "optional"]` field is not set from `True` to `False`

## Root Cause
In function `pub async fn reconcile_hdfs(hdfs: Arc<HdfsCluster>, ctx: Arc<Ctx>) -> HdfsOperatorResult<Action>`, [`let merged_config = role.merged_config(&hdfs, rolegroup_name).context(ConfigMergeSnafu)?;`](https://github.com/stackabletech/hdfs-operator/blob/0975c361e1db67cf662b8456d34794b4bfbe0e3f/rust/operator-binary/src/hdfs_controller.rs#L340) is called to merge the current spec to new desired spec. As we can see [here](https://github.com/stackabletech/hdfs-operator/blob/0975c361e1db67cf662b8456d34794b4bfbe0e3f/rust/crd/src/lib.rs#L341), priority is to set `role_group` config at higher priority than `spec`, so spec is overwritten.

## Expected behavior?
I do think this is a bug in the controller. It should change the priority they set the config. In fact, all my error reports are related to this. Fields in `roleGroups` are not updated because they have higher priority during `Merge`.

## What happened (#2)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "journalNodes", "config", "resources", "cpu", "max"]` field is not set from `ACTOKEY` to `""`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#3)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "journalNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "initContainers", 0, "stdin"]` field is not set from `True` to `False`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#4)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "dataNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "readinessGates", 0, "conditionType"]` field is not set from `ACTOKEY` to `""`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#5)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["status", "conditions", 0, "lastTransitionTime"]` field is not set from `ACTOKEY` to `""`

## Root Cause
`lastTransitionTime` is set according to time

## Expected behavior?
This is a false alarm as this field should not be modified by Acto

## What happened (#6)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "nameNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "affinity", "podAffinity", "preferredDuringSchedulingIgnoredDuringExecution", 0, "podAffinityTerm", "namespaceSelector", "matchLabels", "ACTOKEY"]` field is not set from `NotPresent` to `""`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#7)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "nameNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "volumes", 0, "downwardAPI", "items", 0, "resourceFieldRef", "divisor"]` field is not set from `ACTOKEY` to `""`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#8)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "nameNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "containers", 0, "securityContext", "windowsOptions", "gmsaCredentialSpec"]` field is not set from `ACTOKEY` to `""`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#9)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "dataNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "affinity", "podAffinity", "preferredDuringSchedulingIgnoredDuringExecution", 0, "podAffinityTerm", "namespaceSelector", "matchLabels", "ACTOKEY"]` field is not set from `NotPresent` to `""`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#10)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "journalNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "volumes", 0, "quobyte", "readOnly"]` field is not set from `True` to `False`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#11)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "journalNodes", "podOverrides", "spec", "serviceAccountName"]` field is not set from `INVALID_SERVICE_ACCOUNT_NAME` to `default`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#12)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "journalNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "containers", 0, "stdinOnce"]` field is not set from `True` to `False`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#13)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "journalNodes", "podOverrides", "spec", "initContainers", 0, "imagePullPolicy"]` field is not set from `Always` to `INVALID_IMAGE_PULL_POLICY`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#14)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "nameNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "initContainers", 0, "securityContext", "windowsOptions", "gmsaCredentialSpecName"]` field is not set from `ACTOKEY` to `""`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#15)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "nameNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "volumes", 0, "projected", "sources", 0, "secret", "items", 0, "mode"]` field is not set from `1` to `"NotPresent"`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#16)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "dataNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "hostPID"]` field is not set from `True` to `"False"`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#17)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "journalNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "containers", 0, "ports", 0, "containerPort"]` field is not set from `1` to `"NotPresent"`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#18)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "journalNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "volumes", 0, "secret", "defaultMode"]` field is not set from `5` to `0`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#19)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "journalNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "securityContext", "fsGroupChangePolicy"]` field is not set from `ACTOKEY` to `""`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#20)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "journalNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "securityContext", "fsGroupChangePolicy"]` field is not set from `ACTOKEY` to `""`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#21)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "dataNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "containers", 0, "lifecycle", "preStop", "httpGet", "scheme"]` field is not set from `ACTOKEY` to `""`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#22)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "journalNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "volumes", 0, "iscsi", "iscsiInterface"]` field is not set from `ACTOKEY` to `""`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#23)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["status", "conditions", 0, "lastUpdateTime"]` field is not set from `ACTOKEY` to `""`

## Root Cause
Same as 5

## Expected behavior?
Same as 5

## What happened (#24)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "journalNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "containers", 0, "image"]` field is not set from `ACTOKEY` to `""`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#25)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "journalNodes", "config", "resources", "storage", "data", "selectors", "matchLabels", "ACTOKEY"]` field is not set from `NotPresent` to `ACTOKEY`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#26)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "nameNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "initContainers", 0, "resizePolicy", 0, "resourceName"]` field is not set from `ACTOKEY` to `NotPresent`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#27)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "journalNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "volumes", 0, "vsphereVolume", "volumePath"]` field is not set from `ACTOKEY` to `"`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#28)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "nameNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "topologySpreadConstraints", 0, "minDomains"]` field is not set from `2` to `0`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#29)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "nameNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "topologySpreadConstraints", 0, "minDomains"]` field is not set from `2` to `0`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#30)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "nameNodes", "roleGroups", "ACTOKEY", "config", "affinity", "podAntiAffinity", "preferredDuringSchedulingIgnoredDuringExecution", 0, "podAffinityTerm", "namespaceSelector", "matchLabels", "ACTOKEY"]` field is not set from `NotPresent` to `ACTOKEY`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#31)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "dataNodes", "cliOverrides", "ACTOKEY"]` field is not set from `NotPresent` to `"`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#32)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "dataNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "containers", 0, "securityContext", "seLinuxOptions", "role"]` field is not set from `ACTOKEY` to `"`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#33)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "nameNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "volumes", 0, "projected", "sources", 0, "downwardAPI", "items", 0, "mode"]` field is not set from `4` to `0`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#34)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "nameNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "containers", 0, "lifecycle", "postStart", "httpGet", "port"]` field is not set from `ACTOKEY` to `"`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#35)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "dataNodes", "config", "resources", "cpu", "min"]` field is not set from `ACTOKEY` to `"`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#36)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "nameNodes", "roleGroups", "ACTOKEY", "envOverrides", "ACTOKEY"]` field is not set from `NotPresent` to `ACTOKEY`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#37)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "nameNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "initContainers", 0, "lifecycle", "postStart", "tcpSocket", "port"]` field is not set from `ACTOKEY` to `"`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#38)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "nameNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "volumes", 0, "quobyte", "readOnly"]` field is not set from `True` to `False`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#39)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "nameNodes", "roleGroups", "ACTOKEY", "config", "affinity", "podAffinity", "preferredDuringSchedulingIgnoredDuringExecution", 0, "podAffinityTerm", "labelSelector", "matchLabels", "ACTOKEY"]` field is not set from `NotPresent` to `ACTOKEY`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#40)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "dataNodes", "roleGroups", "ACTOKEY", "config", "affinity", "podAntiAffinity", "requiredDuringSchedulingIgnoredDuringExecution", 0, "topologyKey"]` field is not set from `ACTOKEY` to `"`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#41)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "journalNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "volumes", 0, "flexVolume", "readOnly"]` field is not set from `True` to `False`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#42)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "dataNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "initContainers", 0, "env", 0, "value"]` field is not set from `ACTOKEY` to `NotPresent`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#43)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "nameNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "volumes", 0, "quobyte", "registry"]` field is not set from `ACTOKEY` to `"`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#44)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "nameNodes", "roleGroups", "ACTOKEY", "cliOverrides", "ACTOKEY"]` field is not set from `NotPresent` to `ACTOKEY`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#45)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "nameNodes", "roleGroups", "ACTOKEY", "cliOverrides", "ACTOKEY"]` field is not set from `NotPresent` to `"`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#46)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "nameNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "volumes", 0, "rbd", "readOnly"]` field is not set from `True` to `False`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#47)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "dataNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "shareProcessNamespace"]` field is not set from `True` to `False`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#48)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "journalNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "volumes", 0, "secret", "optional"]` field is not set from `True` to `False`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#49)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "dataNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "containers", 0, "env", 0, "valueFrom", "resourceFieldRef", "resource"]` field is not set from `ACTOKEY` to `"`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#50)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "nameNodes", "roleGroups", "ACTOKEY", "config", "affinity", "podAffinity", "requiredDuringSchedulingIgnoredDuringExecution", 0, "namespaceSelector", "matchLabels", "ACTOKEY"]` field is not set from `NotPresent` to `ACTOKEY`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#51)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "nameNodes", "roleGroups", "ACTOKEY", "config", "affinity", "podAffinity", "requiredDuringSchedulingIgnoredDuringExecution", 0, "namespaceSelector", "matchLabels", "ACTOKEY"]` field is not set from `NotPresent` to `ACTOKEY`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#52)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "journalNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "initContainers", 0, "lifecycle", "postStart", "httpGet", "httpHeaders", 0, "value"]` field is not set from `ACTOKEY` to `"`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#53)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "journalNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "containers", 0, "stdinOnce"]` field is not set from `True` to `False`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#54)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "journalNodes", "roleGroups", "ACTOKEY", "podOverrides", "metadata", "generateName"]` field is not set from `ACTOKEY` to `"`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#55)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "nameNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "affinity", "podAffinity", "requiredDuringSchedulingIgnoredDuringExecution", 0, "namespaceSelector", "matchLabels", "ACTOKEY"]` field is not set from `NotPresent` to `ACTOKEY`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#56)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "dataNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "initContainers", 0, "livenessProbe", "httpGet", "httpHeaders", 0, "value"]` field is not set from `ACTOKEY` to `NotPresent`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#57)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "dataNodes", "roleGroups", "ACTOKEY", "config", "affinity", "podAntiAffinity", "requiredDuringSchedulingIgnoredDuringExecution", 0, "namespaceSelector", "matchLabels", "ACTOKEY"]` field is not set from `NotPresent` to `ACTOKEY`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#58)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "nameNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "initContainers", 0, "securityContext", "seLinuxOptions", "user"]` field is not set from `ACTOKEY` to `"`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#59)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "journalNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "volumes", 0, "portworxVolume", "fsType"]` field is not set from `ACTOKEY` to `"`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#60)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "journalNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "initContainers", 0, "volumeMounts", 0, "mountPath"]` field is not set from `ACTOKEY` to `"`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#61)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "dataNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "initContainers", 0, "startupProbe", "initialDelaySeconds"]` field is not set from `4` to `0`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#62)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "dataNodes", "config", "resources", "storage", "ACTOKEY", "selectors", "matchLabels", "ACTOKEY"]` field is not set from `NotPresnet` to `ACTOKEY`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#63)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "journalNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "volumes", 0, "ephemeral", "volumeClaimTemplate", "spec", "dataSourceRef", "kind"]` field is not set from `ACTOKEY` to `"`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#64)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["status", "conditions", 0, "status"]` field is not set from `ACTOKEY` to `"`

## Root Cause
From the [`pub fn compute_conditions`](https://github.com/stackabletech/operator-rs/blob/8092fd4ab7be5e48f3d50f805c05a35df3e9309d/src/status/condition/mod.rs#L71), we can see the new and old conditions are merged, from [`merge`](https://github.com/stackabletech/operator-rs/blob/8092fd4ab7be5e48f3d50f805c05a35df3e9309d/src/status/condition/mod.rs#L303), we can see that if new and old conditions both exists, they are concatenated.

## Expected behavior?
This is a false alarm because the behavior is correct, The concatenated result does not change.

## What happened (#64)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "dataNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "containers", 0, "readinessProbe", "successThreshold"]` field is not set from `5` to `0`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#65)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "dataNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "initContainers", 0, "resizePolicy", 0, "resourceName"]` field is not set from `ACTOKEY` to `"`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#66)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "dataNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "tolerations", 0, "value"]` field is not set from `ACTOKEY` to `"`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#67)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "dataNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "volumes", 0, "nfs", "path"]` field is not set from `ACTOKEY` to `"`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#68)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "nameNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "initContainers", 0, "envFrom", 0, "prefix"]` field is not set from `ACTOKEY` to `NotPresent`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#69)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "journalNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "initContainers", 0, "securityContext", "seLinuxOptions", "user"]` field is not set from `ACTOKEY` to `"`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#70)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "nameNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "affinity", "podAffinity", "requiredDuringSchedulingIgnoredDuringExecution", 0, "namespaceSelector", "matchLabels", "ACTOKEY"]` field is not set from `NotPresent` to `ACTOKEY`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#71)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "nameNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "affinity", "podAffinity", "requiredDuringSchedulingIgnoredDuringExecution", 0, "namespaceSelector", "matchLabels", "ACTOKEY"]` field is not set from `NotPresent` to `"`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#72)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "nameNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "affinity", "podAffinity", "requiredDuringSchedulingIgnoredDuringExecution", 0, "namespaceSelector", "matchLabels", "ACTOKEY"]` field is not set from `NotPresent` to `"`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#73)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "dataNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "volumes", 0, "iscsi", "chapAuthDiscovery"]` field is not set from `True` to `False`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#74)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "dataNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "initContainers", 0, "env", 0, "valueFrom", "resourceFieldRef", "containerName"]` field is not set from `ACTOKEY` to `"`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#78)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "nameNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "initContainers", 0, "resources", "requests", "ACTOKEY"]` field is not set from `NotPresent` to `ACTOKEY`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#79)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "journalNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "containers", 0, "startupProbe", "initialDelaySeconds"]` field is not set from `2` to `0`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#80)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "dataNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "containers", 0, "startupProbe", "grpc", "service"]` field is not set from `ACTOKEY` to `"`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#81)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "nameNodes", "roleGroups", "ACTOKEY", "config", "affinity", "podAntiAffinity", "requiredDuringSchedulingIgnoredDuringExecution", 0, "labelSelector", "matchLabels", "ACTOKEY"]` field is not set from `NotPresnet` to `ACTOKEY`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#82)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "nameNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "volumes", 0, "secret", "optional"]` field is not set from `True` to `False`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#84)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "dataNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "tolerations", 0, "tolerationSeconds"]` field is not set from `4` to `0`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#85)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "journalNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "volumes", 0, "iscsi", "lun"]` field is not set from `2` to `0`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#86)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "nameNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "containers", 0, "resources", "limits", "ACTOKEY"]` field is not set from `NotPresent` to `ACTOKEY`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#87)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "dataNodes", "config", "logging", "enableVectorAgent"]` field is not set from `True` to `False`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#88)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "journalNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "containers", 0, "securityContext", "privileged"]` field is not set from `True` to `False`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#89)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "journalNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "initContainers", 0, "startupProbe", "httpGet", "path"]` field is not set from `ACTOKEY` to `"`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#90)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "nameNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "initContainers", 0, "livenessProbe", "failureThreshold"]` field is not set from `5` to `0`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#91)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "nameNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "initContainers", 0, "startupProbe", "httpGet", "httpHeaders", 0, "value"]` field is not set from `ACTOKEY` to `"`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#93)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "dataNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "initContainers", 0, "terminationMessagePolicy"]` field is not set from `ACTOKEY` to `"`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#94)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "nameNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "volumes", 0, "secret", "items", 0, "mode"]` field is not set from `4` to `0`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#95)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "nameNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "containers", 0, "lifecycle", "postStart", "httpGet", "scheme"]` field is not set from `ACTOKEY` to `"`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#96)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "dataNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "volumes", 0, "projected", "defaultMode"]` field is not set from `2` to `4`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#97)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "journalNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "initContainers", 0, "startupProbe", "httpGet", "httpHeaders", 0, "value"]` field is not set from `ACTOKEY` to `"`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#98)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "journalNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "containers", 0, "readinessProbe", "terminationGracePeriodSeconds"]` field is not set from `4` to `0`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#99)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "journalNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "volumes", 0, "cephfs", "path"]` field is not set from `ACTOKEY` to `"`

## Root Cause
Same as 1

## Expected behavior?
Same as 1

## What happened (#100)
Why did Acto raise this alarm?\
Consistency issue in state transition\
What happened in the state transition?\
System state transition does not match the desired state specified by Acto\
Why Acto’s oracles raised an alarm?\
`["spec", "nameNodes", "roleGroups", "ACTOKEY", "podOverrides", "spec", "volumes", 0, "configMap", "defaultMode"]` field is not set from `2` to `4`

## Root Cause
Same as 1

## Expected behavior?
Same as 1