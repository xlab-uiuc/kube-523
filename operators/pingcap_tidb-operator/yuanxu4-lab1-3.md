# Alarm 1 
## What happened
Why did Acto raise this alarm? What happened in the state transition? Why Acto’s oracles raised an alarm?
## Root Cause
Why did the operator behave in this way? Please find the exact block in the operator source code resulting in the behavior.
## Expected behavior?
If it is a true alarm, how to fix it in the operator code? If it is a false alarm, how to fix it in Acto code?

# Alarm 1-25 
## What happened
false alarm OR misoperation 

1. testrun-2024-03-08-21-48/trial-00-0005/0001
2. testrun-2024-03-08-21-48/trial-00-0006/0002
3. testrun-2024-03-08-21-48/trial-00-0007/0001
4. testrun-2024-03-08-21-48/trial-01-0003/0001
5. testrun-2024-03-08-21-48/trial-01-0004/0002
6. testrun-2024-03-08-21-48/trial-01-0005/0001
7. testrun-2024-03-08-21-48/trial-01-0042/0001
8. testrun-2024-03-08-21-48/trial-01-0076/0001
9. testrun-2024-03-08-21-48/trial-01-0077/0001
10. testrun-2024-03-08-21-48/trial-01-0078/0001
11. testrun-2024-03-08-21-48/trial-01-0081/0001
12. testrun-2024-03-08-21-48/trial-01-0082/0001
13. testrun-2024-03-08-21-48/trial-01-0083/0001
14. testrun-2024-03-08-21-48/trial-02-0004/0001
15. testrun-2024-03-08-21-48/trial-02-0005/0001
16. testrun-2024-03-08-21-48/trial-02-0006/0001
17. testrun-2024-03-08-21-48/trial-02-0043/0007
18. testrun-2024-03-08-21-48/trial-02-0044/0002
19. testrun-2024-03-08-21-48/trial-02-0045/0001
20. testrun-2024-03-08-21-48/trial-02-0057/0001
20. testrun-2024-03-08-21-48/trial-02-0059/0007
21. testrun-2024-03-08-21-48/trial-02-0060/0003
22. testrun-2024-03-08-21-48/trial-05-0003/0002
23. testrun-2024-03-08-21-48/trial-05-0032/0001
24. testrun-2024-03-08-21-48/trial-05-0033/0001
25. testrun-2024-03-08-21-48/trial-05-0034/0001

add key `ACTOKEY` in `spec.tikv.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution` 
## Root Cause
In the message, it says `ACTOKEY` is not a valid selector operator for the `spec.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[0].labelSelector.matchExpressions[0].operator`. 
```
"message": "create Pod test-cluster-tikv-0 in StatefulSet test-cluster-tikv failed error: Pod \"test-cluster-tikv-0\" is invalid: [spec.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[0].labelSelector.matchExpressions[0].operator: Invalid value: \"ACTOKEY\": not a valid selector operator, spec.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[0].labelSelector.matchExpressions[1].operator: Invalid value: \"ACTOKEY\": not a valid selector operator, spec.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[0].labelSelector.matchExpressions[2].operator: Invalid value: \"ACTOKEY\": not a valid selector operator, spec.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[0].labelSelector.matchExpressions[3].operator: Invalid value: \"ACTOKEY\": not a valid selector operator, spec.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[0].namespace: Invalid value: \"ACTOKEY\": a lowercase RFC 1123 label must consist of lower case alphanumeric characters or '-', and must start and end with an alphanumeric character (e.g. 'my-name',  or '123-abc', regex used for validation is '[a-z0-9]([-a-z0-9]*[a-z0-9])?')]",
```
## Expected behavior?
It can be both false alarm or misoperation, for `ACTOKEY` should not be set in that key OR tidb operator should not accept this CR.
If it's a false alarm, fix it by changing the `ACTOKEY` consist with the "a lowercase RFC 1123 label must consist of lower case alphanumeric characters or '-', and must start and end with an alphanumeric character (e.g. 'my-name',  or '123-abc', regex used for validation is '[a-z0-9]([-a-z0-9]*[a-z0-9])?')".

There is a similar issue: https://github.com/kubernetes/kubernetes/issues/94088

# Alarm 26 
## What happened
false alarm OR misoperation 

testrun-2024-03-08-21-48/trial-00-0010/0001

add key `ACTOKEY` in `spec.containers[0].envFrom[0].configMapRef` 
## Root Cause
In the message, it says `spec.containers[0].envFrom[0].configMapRef.name`is not set, this CR is invalid. 

Why did the operator behave in this way? Please find the exact block in the operator source code resulting in the behavior.
```
"message": "create Pod test-cluster-tikv-0 in StatefulSet test-cluster-tikv failed error: Pod \"test-cluster-tikv-0\" is invalid: spec.containers[0].envFrom[0].configMapRef.name: Required value",
```

## Expected behavior?
It can be both false alarm or misoperation, for acto should set the name of `configMapRef` because other value of `configMapRef` have dependency with the name OR tidb operator should not accept this invalid CR.
If it's a false alarm, fix it by changing the `ACTOKEY` consist with the "a lowercase RFC 1123 label must consist of lower case alphanumeric characters or '-', and must start and end with an alphanumeric character (e.g. 'my-name',  or '123-abc', regex used for validation is '[a-z0-9]([-a-z0-9]*[a-z0-9])?')".

# Alarm 27-55 
## What happened
false alarm OR misoperation 

1. testrun-2024-03-08-21-48/trial-00-0013/0001
2. testrun-2024-03-08-21-48/trial-00-0023/0006
3. testrun-2024-03-08-21-48/trial-00-0024/0002
4. testrun-2024-03-08-21-48/trial-00-0025/0001
5. testrun-2024-03-08-21-48/trial-00-0053/0003
6. testrun-2024-03-08-21-48/trial-00-0061/0001
7. testrun-2024-03-08-21-48/trial-00-0062/0002
8. testrun-2024-03-08-21-48/trial-00-0063/0001
9. testrun-2024-03-08-21-48/trial-00-0067/0002
10. testrun-2024-03-08-21-48/trial-01-0065/0001
11. testrun-2024-03-08-21-48/trial-01-0066/0001
12. testrun-2024-03-08-21-48/trial-02-0001/0003
13. testrun-2024-03-08-21-48/trial-02-0002/0001
14. testrun-2024-03-08-21-48/trial-02-0003/0001
15. testrun-2024-03-08-21-48/trial-02-0028/0002
16. testrun-2024-03-08-21-48/trial-02-0029/0003
17. testrun-2024-03-08-21-48/trial-02-0034/0010
18. testrun-2024-03-08-21-48/trial-03-0007/0005
19. testrun-2024-03-08-21-48/trial-03-0008/0003
20. testrun-2024-03-08-21-48/trial-03-0017/0001
21. testrun-2024-03-08-21-48/trial-03-0018/0002
22. testrun-2024-03-08-21-48/trial-03-0019/0001
23. testrun-2024-03-08-21-48/trial-03-0023/0004
24. testrun-2024-03-08-21-48/trial-05-0000/0001
25. testrun-2024-03-08-21-48/trial-05-0001/0002
26. testrun-2024-03-08-21-48/trial-05-0002/0001
27. testrun-2024-03-08-21-48/trial-05-0014/0002
28. testrun-2024-03-08-21-48/trial-05-0043/0001

add key `ACTOKEY` in `spec.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution` 

## Root Cause
In the message, it says `ACTOKEY` is not a valid selector operator for the `spec.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.labelSelector.matchExpressions[0].operator`. 

```
"message": "create Pod test-cluster-tikv-0 in StatefulSet test-cluster-tikv failed error: Pod \"test-cluster-tikv-0\" is invalid: [spec.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.labelSelector.matchExpressions[0].operator: Invalid value: \"ACTOKEY\": not a valid selector operator, spec.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.labelSelector.matchExpressions[1].operator: Invalid value: \"ACTOKEY\": not a valid selector operator, spec.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.labelSelector.matchExpressions[2].operator: Invalid value: \"ACTOKEY\": not a valid selector operator]",
```
## Expected behavior?
It can be both false alarm or misoperation, for `ACTOKEY` should not be set in that key OR tidb operator should not accept this CR.
If it's a false alarm, fix it by changing the `ACTOKEY` consist with the "a lowercase RFC 1123 label must consist of lower case alphanumeric characters or '-', and must start and end with an alphanumeric character (e.g. 'my-name',  or '123-abc', regex used for validation is '[a-z0-9]([-a-z0-9]*[a-z0-9])?')".

There is a similar issue: https://github.com/kubernetes/kubernetes/issues/94088

# Alarm 56-57 
## What happened
misoperation 

testrun-2024-03-08-21-48/trial-00-0038/0006
testrun-2024-03-08-21-48/trial-00-0039/0001

set `spec.tikv.podSecurityContext.runAsUser` value 2.
## Root Cause
Because CR set tikv pod run as user, but rocksdb's log need root to initialize.
```
"test-cluster-tikv-0": [
        "starting tikv-server ...",
        "/tikv-server --pd=http://test-cluster-pd:2379 --advertise-addr=test-cluster-tikv-0.test-cluster-tikv-peer.acto-namespace.svc:20160 --addr=0.0.0.0:20160 --status-addr=0.0.0.0:20180 --advertise-status-addr=test-cluster-tikv-0.test-cluster-tikv-peer.acto-namespace.svc:20180 --data-dir=/var/lib/tikv --capacity=0 --config=/etc/tikv/tikv.toml",
        "",
        "failed to initialize rocksdb log with file /var/lib/tikv/rocksdb.info: Permission denied (os error 13)"
    ],
```
## Expected behavior?
It is a misoperation, tidb operator should reject this invalid CR.

# Alarm 58-59 
## What happened
misoperation

1. testrun-2024-03-08-21-48/trial-00-0041/0001
2. testrun-2024-03-08-21-48/trial-05-0038/0001

set the `spec.tikv.baseimage` to `ACTOKEY`
## Root Cause
`ACTOKEY` is not a valid `spec.tikv.baseimage`

```
"message": "Failed to apply default image tag \"ACTOKEY:v7.1.1\": couldn't parse image name \"ACTOKEY:v7.1.1\": invalid reference format: repository name must be lowercase",
```
## Expected behavior?
It is a misoperation, operator should reject the invalid CR.

# Alarm 60-66 
## What happened
misoperation 

1. testrun-2024-03-08-21-48/trial-00-0042/0002
2. testrun-2024-03-08-21-48/trial-00-0043/0002
3. testrun-2024-03-08-21-48/trial-00-0044/0001
4. testrun-2024-03-08-21-48/trial-01-0054/0002
5. testrun-2024-03-08-21-48/trial-03-0043/0007
7. testrun-2024-03-08-21-48/trial-03-0044/0001

set `spec.tikv.topologySpreadConstraints.topologyKey` to `ACTOKEY`
## Root Cause
`topologyKey` is set to `ACTOKEY`, so new pod cannot be properly scheduling. There is no node have the node label key as `ACTOKEY`, so `missing required label`.
```
"message": "0/4 nodes are available: 1 node(s) didn't match pod topology spread constraints (missing required label). preemption: 0/4 nodes are available: 1 Preemption is not helpful for scheduling, 3 No preemption victims found for incoming pod..",
```
## Expected behavior?
It's a misoperation, the tidb operator fails to reject the erroneous desired state, causing the cluster cannot be scheduled.


# Alarm 67 
## What happened
misoperation 

testrun-2024-03-08-21-48/trial-03-0045/0001

set `spec.tikv.topologySpreadConstraints.topologyKey` to ``(empty).
## Root Cause
`topologyKey` is set to ``, it can not be set to empty.
```
"message": "create Pod test-cluster-tikv-0 in StatefulSet test-cluster-tikv failed error: Pod \"test-cluster-tikv-0\" is invalid: spec.topologySpreadConstraints[0].topologyKey: Required value: can not be empty",
```
## Expected behavior?
It's a misoperation, the tidb operator fails to reject the erroneous CR, causing the cluster cannot be scheduled.


# Alarm 68-71 
## What happened
misoperation

1. testrun-2024-03-08-21-48/trial-00-0045/0004
2. testrun-2024-03-08-21-48/trial-00-0046/0001
3. testrun-2024-03-08-21-48/trial-00-0047/0001
4. testrun-2024-03-08-21-48/trial-04-0020/0007

set `spec.tikv.nodeSelector` to `ACTOKEY`.
## Root Cause
`nodeSelector` is set to `ACTOKEY`, so new pod cannot be properly scheduling. There is no node have the node label key as `ACTOKEY`, so `didn't match Pod's node affinity/selector`.
```
"message": "0/4 nodes are available: 1 node(s) didn't match Pod's node affinity/selector. preemption: 0/4 nodes are available: 1 Preemption is not helpful for scheduling, 3 No preemption victims found for incoming pod..",
```
## Expected behavior?
It's a misoperation, the tidb operator fails to reject the erroneous CR, causing the cluster cannot be scheduled.

# Alarm 72-75
## What happened
misoperation

1. testrun-2024-03-08-21-48/trial-01-0033/0005
2. testrun-2024-03-08-21-48/trial-03-0055/0001
3. testrun-2024-03-08-21-48/trial-03-0056/0001
4. testrun-2024-03-08-21-48/trial-03-0057/0003


set `spec.tikv.limits.ACTOKEY` to 3.
## Root Cause
`limits.ACTOKEY` is set to 3, `ACTOKEY` is not valid for limits, it should be a standard resource type or fully qualified.
```
"message": "create Pod test-cluster-tikv-0 in StatefulSet test-cluster-tikv failed error: Pod \"test-cluster-tikv-0\" is invalid: [spec.containers[0].resources.limits[ACTOKEY]: Invalid value: \"ACTOKEY\": must be a standard resource type or fully qualified, spec.containers[0].resources.limits[ACTOKEY]: Invalid value: \"ACTOKEY\": must be a standard resource for containers, spec.containers[0].resources.requests[ACTOKEY]: Invalid value: \"ACTOKEY\": must be a standard resource type or fully qualified, spec.containers[0].resources.requests[ACTOKEY]: Invalid value: \"ACTOKEY\": must be a standard resource for containers]",
```
## Expected behavior?
It's a misoperation, the tidb operator fails to reject the erroneous CR.

# Alarm 76-80 
## What happened
misoperation

1. testrun-2024-03-08-21-48/trial-01-0036/0002
2. testrun-2024-03-08-21-48/trial-01-0037/0003
3. testrun-2024-03-08-21-48/trial-04-0062/0001
4. testrun-2024-03-08-21-48/trial-04-0063/0001
5. testrun-2024-03-08-21-48/trial-04-0064/0001

set `spec.tikv.podSecurityContext.windowsOptions.gmsaCredentialSpec` to ``.
## Root Cause
gmsaCredentialSpec is set to an empty string, it is invalid.
```
"message": "create Pod test-cluster-tikv-0 in StatefulSet test-cluster-tikv failed error: Pod \"test-cluster-tikv-0\" is invalid: spec.securityContext.windowsOptions.gmsaCredentialSpec: Invalid value: \"\": gmsaCredentialSpec cannot be an empty string",
```
## Expected behavior?
It's a misoperation, the tidb operator fails to reject the erroneous CR.

# Alarm 81 
## What happened
false alarm OR misoperation 

testrun-2024-03-08-21-48/trial-01-0055/0003

dd key `ACTOKEY` in `spec.securityContext.windowsOptions.gmsaCredentialSpecName` 
## Root Cause
In the message, it says `ACTOKEY` is not a valid selector operator for the `sspec.securityContext.windowsOptions.gmsaCredentialSpecName`. 

```
"message": "create Pod test-cluster-tikv-0 in StatefulSet test-cluster-tikv failed error: Pod \"test-cluster-tikv-0\" is invalid: spec.securityContext.windowsOptions.gmsaCredentialSpecName: Invalid value: \"ACTOKEY\": a lowercase RFC 1123 subdomain must consist of lower case alphanumeric characters, '-' or '.', and must start and end with an alphanumeric character (e.g. 'example.com', regex used for validation is '[a-z0-9]([-a-z0-9]*[a-z0-9])?(\\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*')",
```

## Expected behavior?
It can be both false alarm or misoperation, for `ACTOKEY` should not be set in that key OR tidb operator should not accept this CR.
If it's a false alarm, fix it by changing the `ACTOKEY` consist with the "a lowercase RFC 1123 label must consist of lower case alphanumeric characters or '-', and must start and end with an alphanumeric character (e.g. 'my-name',  or '123-abc', regex used for validation is '[a-z0-9]([-a-z0-9]*[a-z0-9])?')".

# Alarm 82-92 
## What happened
false alarm

1. testrun-2024-03-08-21-48/trial-01-0047/0001
2. testrun-2024-03-08-21-48/trial-01-0057/0001
3. testrun-2024-03-08-21-48/trial-02-0008/0001
4. testrun-2024-03-08-21-48/trial-03-0000/0001
5. testrun-2024-03-08-21-48/trial-03-0001/0001
6. testrun-2024-03-08-21-48/trial-03-0002/0001
7. testrun-2024-03-08-21-48/trial-03-0066/0001
8. testrun-2024-03-08-21-48/trial-04-0056/0007
9. testrun-2024-03-08-21-48/trial-04-0057/0001
10. testrun-2024-03-08-21-48/trial-04-0058/0001
11. testrun-2024-03-08-21-48/trial-04-0059/0001


set `spec.tikv.logTailer.requests.ACTOKEY` to `92403k`
## Root Cause
When looking the code, LogTailer have the type of `ResourceRequirements`. 
```
// LogTailerSpec represents an optional log tailer sidecar container
// +k8s:openapi-gen=true
type LogTailerSpec struct {
	corev1.ResourceRequirements `json:",inline"`
}
```
Accroding to this website https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/, the Resource can only be set as `cpu` `memory` `hugepage`, could not be `ACTOKEY`. So the change on the `ACTOKEY` will not change the system state.
## Expected behavior?
It's a false alarm, `ACTOKEY` is not a `ResourceRequirements`.

# Alarm 93-95 
## What happened
misoperation 

1. testrun-2024-03-08-21-48/trial-03-0034/0003
2. testrun-2024-03-08-21-48/trial-03-0035/0001
3. testrun-2024-03-08-21-48/trial-03-0036/0001

set `spec.tikv.podSecurityContext.runAsNonRoot`
## Root Cause
the container image, will run as root, but the CR set `runAsNonRoot`.

```
"message": "Error: container has runAsNonRoot and image will run as root (pod: \"test-cluster-tikv-0_acto-namespace(3a618527-7ace-474f-b511-9075b78b8bdb)\", container: tikv)",
```
## Expected behavior?
It is misoperation, because the image have to run as root, so it should reject this error CR.



# Alarm 96-100 
## What happened
misoperation

1. testrun-2024-03-08-21-48/trial-05-0008/0001
2. testrun-2024-03-08-21-48/trial-05-0009/0001
3. testrun-2024-03-08-21-48/trial-05-0010/0001
4. testrun-2024-03-08-21-48/trial-05-0011/0001
5. testrun-2024-03-08-21-48/trial-05-0013/0001

set `spec.tikv.requests.ACTOKEY` to 5
## Root Cause
`ACTOKEY` is not a valid value for requests, it should be a resource value like `cpu`, `memory`...

```
"message": "create Pod test-cluster-tikv-0 in StatefulSet test-cluster-tikv failed error: Pod \"test-cluster-tikv-0\" is invalid: [spec.containers[0].resources.requests[ACTOKEY]: Invalid value: \"ACTOKEY\": must be a standard resource type or fully qualified, spec.containers[0].resources.requests[ACTOKEY]: Invalid value: \"ACTOKEY\": must be a standard resource for containers]",
```
## Expected behavior?
It's a misoperation, the operator should reject the CR.
