---
name: Alarm Inspection Report
about: An analysis report for the alarms produced by Acto

---
netid：wendifu2

## Alarm 1
trial-00-0000/0001

#### oracle:
```
"[\"spec\", \"podTemplateSpec\", \"spec\", \"containers\", 0, \"resources\", \"requests\", \"ACTOKEY\"]"
```
#### What happened
The cluster is unhealthy. Received:
```
"kind": null,
"last_timestamp": "2024-03-11T07:56:43+00:00",
"message": "Readiness probe failed: HTTP probe failed with statuscode: 500",
```
And in the alarm we have:
```
message='statefulset: cluster1-test-cluster-default-sts replicas [0] ready_replicas [None]'
```

#### Root Cause

This is an misoperation. The events show that the cluster did not start successfully or returns error in the healthcheck path. 
```
"create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.containers[0].image: Required value, spec.containers[0].resources.requests[ACTOKEY]: Invalid value: ACTOKEY: must be a standard resource type or fully qualified, spec.containers[0].resources.requests[ACTOKEY]: Invalid value: ACTOKEY: must be a standard resource for containers]"
```
It shows that the ACTO misconfigured the cluster by providing an invalid ACTOKEY as a standard resource for containers and causes the issue.

#### Expected behavior?
It is an misoperation and is also something evitable.


## Alarm 2

trial-00-0001/0001

#### What happened


```
message='statefulset: cluster1-test-cluster-default-sts replicas [0] ready_replicas [None]'
```

#### Root Cause

This is an misoperation. The events show that the cluster did not start successfully or returns error in the healthcheck path. 
```
create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.volumes[4].ephemeral.volumeClaimTemplate.spec.accessModes: Required value: at least 1 access mode is required, spec.volumes[4].ephemeral.volumeClaimTemplate.spec.resources[storage]: Required value, spec.containers[0].volumeMounts[0].name: Not found: \"4\", spec.containers[1].volumeMounts[0].name: Not found: \"4\"]
```
It shows that the ACTO misconfigured the cluster by not providing the accessModes. This is an expected behavior from the cluster. And the cluster reports its unhealthy state.

#### Expected behavior?
It is an misoperation.

## Alarm 3
trial-00-0002/0001

#### What happened

The cluster is unhealthy.
```
message='statefulset: cluster1-test-cluster-default-sts replicas [1] ready_replicas [None]'
```

#### Root Cause

In CR, the ACTO sets the pulsarServiceUrl into this
```
pulsarServiceUrl: rirafhxnwf
```
which is unreachable as an configuration for the Pulsar service. It causes the cluster creation failure, and subsequent deletion failure. 

#### Expected behavior?
False Alarm

## Alarm 4
trial-00-0003/0001

#### What happened
The cluster is unhealthy.
```
message='statefulset: cluster1-test-cluster-default-sts replicas [1] ready_replicas [None]'
```
#### Root Cause
In CR, the ACTO sets the pulsarServiceUrl into this
```
pulsarServiceUrl: iizdulqrzc
```
which is unreachable as an configuration for the Pulsar service. It causes the cluster creation failure, and subsequent deletion failure. 

#### Expected behavior?
Misopertion

## Alarm 5
trial-00-0005/0004

#### oracle:

#### What happened

The cluster is unhealthy.
```
message='statefulset: cluster1-test-cluster-default-sts replicas [1] ready_replicas [None]\npod: cluster1-test-cluster-default-sts-0'
```

#### Root Cause
From the events we can find:
```
0/4 nodes are available: 1 node(s) didn't match pod affinity rules. preemption: 0/4 nodes are available: 1 Preemption is not helpful for scheduling, 3 No preemption victims found for incoming pod.
```
This is caused by the ACTO accidentally set non-matching topoogyKey for the affinity requirements as follows:
```
requiredDuringSchedulingIgnoredDuringExecution:
    - topologyKey: ACTOKEY
```
It needs to matches that of any node on which any of the selected pods is running. It causes the clusters goes unhealthy. 

#### Expected behavior?
False Alarm

## Alarm 6
trial-00-0006/0001

#### What happened
The cluster is unhealthy:
```
"statefulset: cluster1-test-cluster-default-sts replicas [1] ready_replicas [None]\npod: cluster1-test-cluster-default-sts-0"
```

#### Root Cause
Similar to the previous one:
It is caused by the ACTO accidentally set non-matching topoogyKey for the affinity requirements as follows:
```
requiredDuringSchedulingIgnoredDuringExecution:
    - topologyKey: ACTOKEY
```
It needs to matches that of any node on which any of the selected pods is running. It causes the clusters goes unhealthy. 
#### Expected behavior?
False Alarm


## Alarm 7
trial-00-0007/0001

#### What happened
The cluster is unhealthy:
```
"statefulset: cluster1-test-cluster-default-sts replicas [1] ready_replicas [None]\npod: cluster1-test-cluster-default-sts-0"
```

#### Root Cause
Similar to the previous one; the ACTO sets the topoogyKey for the affinity requirements as follows:
```
    requiredDuringSchedulingIgnoredDuringExecution:
    - topologyKey: ''
```
And it violates the requirement for the topologyKey, as it should not be empty. This raises the following events:
```
"message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[0].topologyKey: Required value: can not be empty, spec.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[0].topologyKey: Invalid value: \"\": name part must be non-empty, spec.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[0].topologyKey: Invalid value: \"\": name part must consist of alphanumeric characters, '-', '_' or '.', and must start and end with an alphanumeric character (e.g. 'MyName',  or 'my.name',  or '123-abc', regex used for validation is '([A-Za-z0-9][-A-Za-z0-9_.]*)?[A-Za-z0-9]')]",
```
And causes the cluster to crush inevitably.

#### Expected behavior?
False Alarm

## Alarm 8
trial-00-0008/0001

#### What happened

The cluster is unhealthy.
```
message='statefulset: cluster1-test-cluster-default-sts replicas [0] ready_replicas [None]'
```

#### Root Cause

It misconfigured the additionaVolume as follows.
```
    additionalVolumes:
    - mountPath: kvgdwjltbd
      name: '2'
      pvcSpec:
        resources:
          requests:
            ACTOKEY: 2000m
```
It does not provide valid nmountPath and request for the additionalVolumes to the Cassandra clusters.

#### Expected behavior?
False Alarm

## Alarm 9
trial-00-0009/0001

#### What happened

The cluster is unhealthy.
```
message='statefulset: cluster1-test-cluster-default-sts replicas [0] ready_replicas [None]'
```

#### Root Cause
It is the same as the previous one.

It misconfigured the additionaVolume as follows.
```
    additionalVolumes:
    - mountPath: rvukalacop
      name: a
      pvcSpec:
        resources:
          requests:
            ACTOKEY: 1000m
```
It does not provide valid nmountPath and request for the additionalVolumes to the Cassandra clusters.

#### Expected behavior?
False Alarm. Probably add the detection for the mountpoint/paths and generate pseudo/generally used path instead.

## Alarm 10
trial-00-0010/0001

#### What happened

The cluster is unhealthy.
```
message='statefulset: cluster1-test-cluster-default-sts replicas [0] ready_replicas [None]'
```

#### Root Cause

It misconfigured the spec.ephemeralContainers:
```
"create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.ephemeralContainers[0].image: Required value, spec.ephemeralContainers[0].startupProbe: Forbidden: cannot be set for an Ephemeral Container, spec.ephemeralContainers: Forbidden: cannot be set on create]",
```
And the INVALID_NAME did not acts here. The cluster was unhealthy since the misconfiguration of spec.ephemeralContainers[0].image, spec.ephemeralContainers[0].startupProbe, and  spec.ephemeralContainers.

#### Expected behavior?
False Alarm. It is not caused by setting the invalid name, but is caused by inproperly setting spec.ephemeralContainers[0].image and  spec.ephemeralContainers[0].startupProbe.

## Alarm 11
trial-00-0011/0001

#### What happened
The cluster is unhealthy.
```
message='statefulset: cluster1-test-cluster-default-sts replicas [0] ready_replicas [None]'
```
#### Root Cause
It caused by the invalid configuartion of the podTemplateSpec. The use of podTemplateSpec is unrecommended by the developer due to its suspectible behavior. 
```
  podTemplateSpec:
    spec:
      containers: []
      initContainers:
      - env:
        - name: zvnzrpdinl
          valueFrom:
            resourceFieldRef:
              divisor: 2000m
              resource: zlymlynvia
        name: wimgctlmey
```
This leads to :
```
"message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.initContainers[0].image: Required value, spec.initContainers[0].env[0].valueFrom.resourceFieldRef.resource: Unsupported value: \"zlymlynvia\": supported values: \"limits.cpu\", \"limits.ephemeral-storage\", \"limits.memory\", \"requests.cpu\", \"requests.ephemeral-storage\", \"requests.memory\"]",
```
#### Expected behavior?
False Alarm. 

## Alarm 12
trial-00-0012/0001

#### What happened
The cluster is unhealthy.
```
message='statefulset: cluster1-test-cluster-default-sts replicas [0] ready_replicas [None]'
```

#### Root Cause
Same as the previous one:

It caused by the invalid configuartion of the podTemplateSpec. The use of podTemplateSpec is unrecommended by the developer due to its suspectible behavior. 
```
  podTemplateSpec:
    spec:
      containers: []
      initContainers:
      - env:
        - name: kdagujcgjc
          valueFrom:
            resourceFieldRef:
              divisor: 1000m
              resource: gfhswynukj
        name: snhuuxwuvn
```
This leads to :
```
"message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.initContainers[0].image: Required value, spec.initContainers[0].env[0].valueFrom.resourceFieldRef.resource: Unsupported value: \"gfhswynukj\": supported values: \"limits.cpu\", \"limits.ephemeral-storage\", \"limits.memory\", \"requests.cpu\", \"requests.ephemeral-storage\", \"requests.memory\"]",
```
#### Expected behavior?
False Alarm

## Alarm 13
trial-00-0014/0001
Duplicated...
#### What happened
The cluster is unhealthy.
```
message='statefulset: cluster1-test-cluster-default-sts replicas [0] ready_replicas [None]'
```
#### Root Cause
In CR, the ACTO sets the pulsarServiceUrl into this
```
pulsarServiceUrl: bnbegjcvga
```
which is unreachable as an configuration for the Pulsar service. It causes the cluster creation failure, and subsequent deletion failure. 
#### Expected behavior?
False Alarm

## Alarm 14
trial-00-0015/0001
Duplicated...
#### What happened
The cluster is unhealthy.
```
message='statefulset: cluster1-test-cluster-default-sts replicas [0] ready_replicas [None]'
```
#### Root Cause

In CR, the ACTO sets the pulsarServiceUrl into this
```
pulsarServiceUrl: iugzfooohs
```
which is unreachable as an configuration for the Pulsar service. It causes the cluster creation failure, and subsequent deletion failure. 

#### Expected behavior?
False Alarm

## Alarm 15
trial-00-0016/0002
Duplicated...
#### What happened
The cluster is unhealthy.
```
message='statefulset: cluster1-test-cluster-default-sts replicas [0] ready_replicas [None]'
```
#### Root Cause
The ACTO sets the topoogyKey for the affinity requirements as follows:
```
    requiredDuringSchedulingIgnoredDuringExecution:
    - topologyKey: ''
```
And it violates the requirement for the topologyKey, as it should not be empty. This raises the following events:
```
"message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[0].topologyKey: Required value: can not be empty, spec.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[0].topologyKey: Invalid value: \"\": name part must be non-empty, spec.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[0].topologyKey: Invalid value: \"\": name part must consist of alphanumeric characters, '-', '_' or '.', and must start and end with an alphanumeric character (e.g. 'MyName',  or 'my.name',  or '123-abc', regex used for validation is '([A-Za-z0-9][-A-Za-z0-9_.]*)?[A-Za-z0-9]')]",
```
And causes the cluster to crush inevitably.
#### Expected behavior?
False Alarm

## Alarm 16
trial-00-0017/0003

#### What happened
The cluster is unhealthy.
```
message='statefulset: cluster1-test-cluster-default-sts replicas [0] ready_replicas [None]'
```
#### Root Cause
Similar to Alarm 7
The ACTO sets the topoogyKey for the affinity requirements as follows:
```
    requiredDuringSchedulingIgnoredDuringExecution:
    - topologyKey: ''
```
And it violates the requirement for the topologyKey, as it should not be empty. This raises the following events:
```
"message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[0].topologyKey: Required value: can not be empty, spec.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[0].topologyKey: Invalid value: \"\": name part must be non-empty, spec.affinity.podAffinity.requiredDuringSchedulingIgnoredDuringExecution[0].topologyKey: Invalid value: \"\": name part must consist of alphanumeric characters, '-', '_' or '.', and must start and end with an alphanumeric character (e.g. 'MyName',  or 'my.name',  or '123-abc', regex used for validation is '([A-Za-z0-9][-A-Za-z0-9_.]*)?[A-Za-z0-9]')]",
```
And causes the cluster to crush inevitably.

#### Expected behavior?
False Alarm


## Alarm 17
trial-00-0018/0001

#### What happened
The cluster is unhealthy.
```
message='statefulset: cluster1-test-cluster-default-sts replicas [0] ready_replicas [None]'
```
#### Root Cause

The ACTO sets the host IP of the container to ACTO key, which is not satisfy the cass-operator CR.
```
  managementApiAuth:
    insecure: {}
  podTemplateSpec:
    spec:
      containers:
      - name: vtxpxmjtah
        ports:
        - containerPort: 3
          hostIP: ACTOKEY
          hostPort: 1
          name: ACTOKEY
          protocol: ACTOKEY
```
  
#### Expected behavior?
False Alarm

## Alarm 18
trial-00-0019/0001

#### What happened
The cluster is unhealthy.
```
message='statefulset: cluster1-test-cluster-default-sts replicas [0] ready_replicas [None]'
```
#### Root Cause
In the mutated CRD, the ACTO didn't specify the spec.containers[0].image's value, and caused the creation of a failed pod. 
```
"message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: spec.containers[0].image: Required value",
```

#### Expected behavior?
False Alarm

## Alarm 19
trial-00-0020/0001

#### What happened
The cluster is unhealthy.
```
message='statefulset: cluster1-test-cluster-default-sts replicas [0] ready_replicas [None]'
```
#### Root Cause
Similar to Alarm 17
```
  podTemplateSpec:
    spec:
      containers:
      - name: ouowtyngyr
        ports:
        - containerPort: 3
          hostIP: null
          hostPort: 4
          name: ACTOKEY
          protocol: ACTOKEY
```
The ACTO doesn;t set the host IP of the container to ACTO key, which is not satisfy the cass-operator CR. And the pod creation fails.
#### Expected behavior?
False Alarm

## Alarm 20
trial-01-0000/0001

#### What happened
The cluster is unhealthy.
```
message='statefulset: cluster1-test-cluster-default-sts replicas [0] ready_replicas [None]'
```
#### Root Cause
Similar to Alarm 8
It misconfigured the additionaVolume as follows.
```
  storageConfig:
    additionalVolumes:
    - mountPath: hibtkzmudr
      name: d
      volumeSource:
        ephemeral:
          volumeClaimTemplate:
            spec:
              resources:
                requests:
                  ACTOKEY: 2000m
```
It does not provide valid nmountPath and request for the additionalVolumes to the Cassandra clusters.
#### Expected behavior?
False Alarm

## Alarm 21
trial-01-0001/0001

#### What happened
Like the previous one, it tries to mount the additionalVolume to invalid path hibtkzmudr. 
And it does not contains the required values for the spec.volumes[4].ephemeral.volumeClaimTemplate.spec.accessModes.
```
 "message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.volumes[4].ephemeral.volumeClaimTemplate.spec.accessModes: Required value: at least 1 access mode is required, spec.volumes[4].ephemeral.volumeClaimTemplate.spec.resources[storage]: Required value, spec.containers[0].volumeMounts[0].name: Not found: \"4\", spec.containers[1].volumeMounts[0].name: Not found: \"4\"]",
 ```
Causing the cluster to fail. 
```
additionalVolumes:
    - mountPath: hibtkzmudr
      name: d
      volumeSource:
        ephemeral:
          volumeClaimTemplate:
            spec:
              resources:
                requests:
                  ACTOKEY: 2000m
```

#### Root Cause
ACTO doesn't define the access modes, causing the pod creation to fail. This results in an unhealthy cluster. 

#### Expected behavior?
False Alarm

## Alarm 22
trial-01-0002/0001

#### What happened
The pod creation failed and cass-operator fails to reject this state. This leads to unhealthy cluster. 

#### Root Cause
The ACTO misdefining the spec.ephemeralContainers[0].env[0].valueFrom.resourceFieldRef.resource as 'bnfmqmgmrq', which caused the behavior above. 
```
"message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.ephemeralContainers[0].image: Required value, spec.ephemeralContainers[0].env[0].valueFrom.resourceFieldRef.resource: Unsupported value: \"bnfmqmgmrq\": supported values: \"limits.cpu\", \"limits.ephemeral-storage\", \"limits.memory\", \"requests.cpu\", \"requests.ephemeral-storage\", \"requests.memory\", spec.ephemeralContainers: Forbidden: cannot be set on create]",
```
#### Expected behavior?
False Alarm

## Alarm 23
trial-01-0003/0001

#### What happened
The same as the previous one (Alarm 22). The pod creation failed and cass-operator fails to reject this state. This leads to unhealthy cluster. 
#### Root Cause
The same as the previous one (Alarm 22). 
```
"message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.ephemeralContainers[0].image: Required value, spec.ephemeralContainers[0].env[0].valueFrom.resourceFieldRef.resource: Unsupported value: \"shgngiqfqe\": supported values: \"limits.cpu\", \"limits.ephemeral-storage\", \"limits.memory\", \"requests.cpu\", \"requests.ephemeral-storage\", \"requests.memory\", spec.ephemeralContainers: Forbidden: cannot be set on create]",
```
#### Expected behavior?
False Alarm

## Alarm 24
trial-01-0004/0001

#### What happened

The pod creation failed and cass-operator reject this state. This leads to unhealthy cluster. 
```
"message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The ACTO falsefully set the valid values for spec.containers[0].volumeDevices[0] as ACTOKEY, which cannot be found.
```
"message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.containers[0].image: Required value, spec.containers[0].volumeDevices[0].name: Not found: \"ACTOKEY\"]",
```
#### Expected behavior?
False Alarm

## Alarm 25
trial-01-0005/0001

#### What happened
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```

#### Root Cause
The mutated CRD does not provide the required key-value for the spec.containers[0].image. The causes the failure of pod creation.
```
"message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: spec.containers[0].image: Required value",
```

#### Expected behavior?
False Alarm

## Alarm 26
trial-01-0006/0001

#### What happened
The same as the previous one (Alarm 25)
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The mutated CRD does not provide the required key-value for the spec.containers[0].image. The causes the failure of pod creation.
```
"message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: spec.containers[0].image: Required value",
```
#### Expected behavior?
False Alarm

## Alarm 27
trial-01-0008/0003

#### What happened
The pod creation failed, and causes the cluster stays in an unhealthy state. 
```
"message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The ACTO gives invalid volumeMounts.name. It was rejected by the operator as the updated state cannot satisfy the CR. 
```
"message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.containers[0].volumeMounts[0].name: Not found: \"9wo9f\", spec.containers[1].volumeMounts[0].name: Not found: \"9wo9f\"]",
```
#### Expected behavior?
False Alarm

## Alarm 28
trial-01-0011/0001

#### What happened
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The ACTO fails to configure the spec.initContainers fields. The mutated states cannot satisify the cass-operator CR. The fieldPath is invalid. 
```
"message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.initContainers[0].image: Required value, spec.initContainers[0].env[0].valueFrom.fieldRef.fieldPath: Invalid value: \"nhiiystxvx\": error converting fieldPath: unsupported pod version: v2]",
```
#### Expected behavior?
False Alarm

## Alarm 29
trial-01-0013/0001

#### What happened
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The ACTO fails to provide a valid name for spec.containers[0].volumeMounts[0].name. The mutated states cannot satisify the cass-operator CR.
```
  "message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.containers[0].volumeMounts[0].name: Not found: \"u1h3\", spec.containers[1].volumeMounts[0].name: Not found: \"u1h3\"]",
```

#### Expected behavior?
False Alarm

## Alarm 30
trial-01-0014/0001

#### What happened
It is the same duplicated alarm as previous one (Alarm 29)
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The ACTO fails to provide a valid name for spec.containers[0].volumeMounts[0].name. The mutated states cannot satisify the cass-operator CR.
```
 "message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.containers[0].volumeMounts[0].name: Not found: \"wt\", spec.containers[1].volumeMounts[0].name: Not found: \"wt\"]",
```

#### Expected behavior?
False Alarm


## Alarm 31
trial-01-0016/0001

#### What happened
This is the duplicated alarm as (Alarm 5)
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```

#### Root Cause

his is caused by the ACTO accidentally set non-matching topoogyKey for the affinity requirements as follows:
```
requiredDuringSchedulingIgnoredDuringExecution:
    - topologyKey: ACTOKEY
```
It needs to matches that of any node on which any of the selected pods is running. It causes the clusters goes unhealthy, also producing the following warnning.
```
  "message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: spec.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[1].namespace: Invalid value: \"ACTOKEY\": a lowercase RFC 1123 label must consist of lower case alphanumeric characters or '-', and must start and end with an alphanumeric character (e.g. 'my-name',  or '123-abc', regex used for validation is '[a-z0-9]([-a-z0-9]*[a-z0-9])?')",
```
#### Expected behavior?
False Alarm

## Alarm 32
trial-01-0017/0001

#### What happened
This is a duplicated alarm as the previous one-(Alarm 31)
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```

#### Root Cause
This is caused by the ACTO accidentally set non-matching topoogyKey for the affinity requirements as follows:
```
requiredDuringSchedulingIgnoredDuringExecution:
    - topologyKey: ACTOKEY
```
It needs to matches that of any node on which any of the selected pods is running. It causes the clusters goes unhealthy, also producing the following warnning in the events.
```
  "message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: spec.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[1].namespace: Invalid value: \"ACTOKEY\": a lowercase RFC 1123 label must consist of lower case alphanumeric characters or '-', and must start and end with an alphanumeric character (e.g. 'my-name',  or '123-abc', regex used for validation is '[a-z0-9]([-a-z0-9]*[a-z0-9])?')",
```

#### Expected behavior?
False Alarm

## Alarm 33
trial-01-0018/0001

#### What happened
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```

#### Root Cause
This is caused by the ACTO accidentally set invalid spec.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[1].namespace for the affinity requirements as follows:
```
podAntiAffinity:
  requiredDuringSchedulingIgnoredDuringExecution:
  - namespaces:
    - ''
```
This causes:
```
"message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: spec.affinity.podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution[1].namespace: Invalid value: \"\": a lowercase RFC 1123 label must consist of lower case alphanumeric characters or '-', and must start and end with an alphanumeric character (e.g. 'my-name',  or '123-abc', regex used for validation is '[a-z0-9]([-a-z0-9]*[a-z0-9])?')",
```

#### Expected behavior?

## Alarm 34
trial-01-0019/0005

#### What happened
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The pod creation failure was partly expected as the ACTO provides the invalid name to the operator. The operator's CR cannot be satisfied and the this leads to an unhealthy state.
But it also fails to provide the spec.initContainers[0].image. This should be categorized as an false alarm.
```
"message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.initContainers[0].image: Required value, spec.initContainers[0].volumeMounts[0].name: Not found: \"INVALID_NAME\"]",
```

#### Expected behavior?
False Alarm

## Alarm 35
trial-01-0020/0001

#### What happened
This is a duplicated alarm as the alarm 29
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The ACTO fails to provide a valid name for spec.containers[0].volumeMounts[0].name. The mutated states cannot satisify the cass-operator CR. It also fails to provide valid spec.volumes[4].ephemeral.volumeClaimTemplate.spec.accessModes. Which leads the operation fails.
```
  "message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.volumes[4].ephemeral.volumeClaimTemplate.spec.accessModes: Unsupported value: \"ACTOKEY\": supported values: \"ReadOnlyMany\", \"ReadWriteMany\", \"ReadWriteOnce\", \"ReadWriteOncePod\", spec.volumes[4].ephemeral.volumeClaimTemplate.spec.resources[storage]: Required value, spec.containers[0].volumeMounts[0].name: Not found: \"cmoltag\", spec.containers[1].volumeMounts[0].name: Not found: \"cmoltag\"]",
```
#### Expected behavior?
False Alarm

## Alarm 36
trial-01-0022/0008

#### What happened
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
It misconfigured the spec.ephemeralContainers:
```
  "message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.ephemeralContainers[0].image: Required value, spec.ephemeralContainers: Forbidden: cannot be set on create]",
```
And the INVALID_NAME did not acts here. The cluster was unhealthy since the misconfiguration of spec.ephemeralContainers[0].image, spec.ephemeralContainers[0].startupProbe, and  spec.ephemeralContainers.
#### Expected behavior?
Misopeation

## Alarm 37
trial-01-0023/0006

#### What happened
#### Root Cause

"message": "delete Pod cluster1-test-cluster-nuzsteswew-sts-0 in StatefulSet cluster1-test-cluster-nuzsteswew-sts failed error: pods \"cluster1-test-cluster-nuzsteswew-sts-0\" not found",

#### Expected behavior?
WIP!!!

## Alarm 38
trial-01-0024/0001

#### What happened
It a duplicated alarm as alarm 36.
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
It misconfigured the spec.ephemeralContainers:
```
  "message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.ephemeralContainers[0].image: Required value, spec.ephemeralContainers: Forbidden: cannot be set on create]",
```
And the INVALID_NAME did not acts here. The cluster was unhealthy since the misconfiguration of spec.ephemeralContainers[0].image, spec.ephemeralContainers[0].startupProbe, and  spec.ephemeralContainers.
#### Expected behavior?
False Alarm

## Alarm 39
trial-01-0025/0001

#### What happened
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
#### Root Cause
It misconfigured the spec.volumes[1].ephemeral.volumeClaimTemplate.spec.accessModes:
```
"message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.volumes[1].ephemeral.volumeClaimTemplate.spec.accessModes: Required value: at least 1 access mode is required, spec.volumes[1].ephemeral.volumeClaimTemplate.spec.resources[storage]: Required value, spec.volumes[1].ephemeral.volumeClaimTemplate.spec.volumeMode: Unsupported value: \"ACTOKEY\": supported values: \"Block\", \"Filesystem\"]",
```
The ACTO does not provide the specific keys to the entires, and causes the pod to fail. 
#### Expected behavior?
False Alarm

## Alarm 40
trial-01-0027/0004

#### What happened
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The alarm is caused by the cluster has no ready replicas
```
message='statefulset: cluster1-test-cluster-default-sts replicas [0] ready_replicas [None]'
```
This is actually expected as there's only one replica in the cluster. The deletion was successfully handled by the oeprator. 
#### Expected behavior?
False alarm. 

## Alarm 41
trial-01-0028/0001

#### What happened
This is a duplicated alarm as Alarm 25.
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True. 
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The mutated CRD does not provide the required key-value for the spec.containers[0].image. The causes the failure of pod creation.
```
"message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: spec.containers[0].image: Required value",
```

#### Expected behavior?
False Alarm

## Alarm 42
trial-01-0029/0001

#### What happened
This is a duplicated alarm as Alarm 25.
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True. 
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The mutated CRD does not provide the required key-value for the spec.containers[0].image. The causes the failure of pod creation.
```
"message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: spec.containers[0].image: Required value",
```
#### Expected behavior?
False Alarm

## Alarm 43
trial-01-0030/0001

#### What happened
This is a duplicated alarm as Alarm 43.
The system is unhealthy, since the recreation of the pod failures as the affinity rule cannot satisfy the operator's CR.
```
 "message": "0/4 nodes are available: 1 node(s) didn't match Pod's node affinity/selector. preemption: 0/4 nodes are available: 1 Preemption is not helpful for scheduling, 3 No preemption victims found for incoming pod.",
```
#### Root Cause
There is no node matches the pod's affinity selector:
  nodeSelector:
    ACTOKEY: ACTOKEY
This operation is not detected as rejected by the operator.
#### Expected behavior?
Misoperation

## Alarm 44
trial-01-0031/0001

#### What happened
This is a duplicated alarm as Alarm 43.
The system is unhealthy, since the recreation of the pod failures as the affinity rule cannot satisfy the operator's CR.
```
 "message": "0/4 nodes are available: 1 node(s) didn't match Pod's node affinity/selector. preemption: 0/4 nodes are available: 1 Preemption is not helpful for scheduling, 3 No preemption victims found for incoming pod.",
```
#### Root Cause
There is no node matches the pod's affinity selector:
  nodeSelector:
    ACTOKEY: ACTOKEY
This operation is not detected as not rejected by the operator. 
#### Expected behavior?
Misoperation

## Alarm 45
trial-01-0032/0001

#### What happened
This is a duplicated alarm as Alarm 43.
The system is unhealthy, since the recreation of the pod failures as the affinity rule cannot satisfy the operator's CR.
```
 "message": "0/4 nodes are available: 1 node(s) didn't match Pod's node affinity/selector. preemption: 0/4 nodes are available: 1 Preemption is not helpful for scheduling, 3 No preemption victims found for incoming pod.",
```
#### Root Cause
There is no node matches the pod's affinity selector:
  nodeSelector:
    ACTOKEY: ''
This operation is not detected as not rejected by the operator.
#### Expected behavior?
Misoperation

## Alarm 46
trial-01-0033/0001

#### What happened
This is a duplicated alarm as Alarm 36.
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
It misconfigured the spec.ephemeralContainers:
```
  "message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.ephemeralContainers[0].image: Required value, spec.ephemeralContainers: Forbidden: cannot be set on create]",
```
And the INVALID_NAME did not acts here. The cluster was unhealthy since the misconfiguration of spec.ephemeralContainers[0].image, spec.ephemeralContainers[0].startupProbe, and  spec.ephemeralContainers.
#### Expected behavior?
Misopeation

## Alarm 47
trial-01-0034/0001

#### What happened
This is a duplicated alarm as Alarm 36.
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
It misconfigured the spec.ephemeralContainers:
```
  "message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.ephemeralContainers[0].image: Required value, spec.ephemeralContainers: Forbidden: cannot be set on create]",
```
And the INVALID_NAME did not acts here. The cluster was unhealthy since the misconfiguration of spec.ephemeralContainers[0].image, spec.ephemeralContainers[0].startupProbe, and  spec.ephemeralContainers.
#### Expected behavior?
Misopeation

## Alarm 48
trial-01-0036/0002

#### What happened
This is a duplicated alarm as Alarm 27.
The pod creation failed, and causes the cluster stays in an unhealthy state. 
```
"message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The ACTO gives invalid volumeMounts.name. It was rejected by the operator as the updated state cannot satisfy the CR. 
```
"message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.containers[0].volumeMounts[0].name: Not found: \"9wo9f\", spec.containers[1].volumeMounts[0].name: Not found: \"9wo9f\"]",
```
#### Expected behavior?
False Alarm

## Alarm 49
trial-01-0037/0001

#### What happened
This is a duplicated alarm as Alarm 27.
The pod creation failed, and causes the cluster stays in an unhealthy state. 
```
"message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The ACTO gives invalid volumeMounts.name. It was rejected by the operator as the updated state cannot satisfy the CR. 
```
"message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.containers[0].volumeMounts[0].name: Not found: \"9wo9f\", spec.containers[1].volumeMounts[0].name: Not found: \"9wo9f\"]",
```
#### Expected behavior?
False Alarm

## Alarm 50
trial-01-0038/0001

#### What happened
This is a duplicated alarm as Alarm 27.
The pod creation failed, and causes the cluster stays in an unhealthy state. 
```
"message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The ACTO gives invalid volumeMounts.name. It was rejected by the operator as the updated state cannot satisfy the CR. 
```
"message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.containers[0].volumeMounts[0].name: Not found: \"9wo9f\", spec.containers[1].volumeMounts[0].name: Not found: \"9wo9f\"]",
```
#### Expected behavior?
False Alarm

## Alarm 51
trial-01-0039/0002

#### What happened
#### Root Cause
#### Expected behavior?
WIP

## Alarm 52
trial-01-0040/0002

#### What happened
This is a duplicated alarm as Alarm 34.
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The pod creation failure was partly expected as the ACTO provides the invalid name to the operator. The operator's CR cannot be satisfied and the this leads to an unhealthy state.
Which is expected as the last available pod was impaired by the invalid name. The operator acts normally.
```
 "message": "create Pod cluster1-test-cluster-rwqfyawdap-sts-0 in StatefulSet cluster1-test-cluster-rwqfyawdap-sts failed error: Pod \"cluster1-test-cluster-rwqfyawdap-sts-0\" is invalid: [spec.initContainers[0].image: Required value, spec.initContainers[0].envFrom[0].configMapRef.name: Invalid value: \"INVALID_NAME\": a lowercase RFC 1123 subdomain must consist of lower case alphanumeric characters, '-' or '.', and must start and end with an alphanumeric character (e.g. 'example.com', regex used for validation is '[a-z0-9]([-a-z0-9]*[a-z0-9])?(\\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*')]"
```

#### Expected behavior?
Misoperation

## Alarm 53
trial-01-0041/0001

#### What happened
The pod crashed.
```
message='Pod cluster1-test-cluster-default-sts-0 crashed'
```
as the ACTO tries to set the security context. 
#### Root Cause
The back-off restarting failed as the security context is bad. And the in this case the operator should reject in the system state and thus the pod creation. The pod crush was expected.
```
"message": "Back-off restarting failed container cassandra in pod cluster1-test-cluster-default-sts-0_acto-namespace(f86533d8-027a-4b2f-9537-d1b43fd05416)"
```
#### Expected behavior?
False Alarm

## Alarm 54
trial-01-0042/0002

#### What happened
It is the duplicated alarm as the previous one(Alarm 53). 
The pod crashed.
```
message='Pod cluster1-test-cluster-default-sts-0 crashed'
```
as the ACTO tries to set the security context. 
#### Root Cause
The back-off restarting failed as the security context is bad. And the in this case the operator should reject in the system state and thus the pod creation. The pod crush was expected.
```
"message": "Back-off restarting failed container cassandra in pod cluster1-test-cluster-default-sts-0_acto-namespace(f86533d8-027a-4b2f-9537-d1b43fd05416)"
```
#### Expected behavior?
False Alarm

## Alarm 55
trial-01-0044/0003

#### What happened
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
 ```
#### Root Cause
It misconfigured the spec.initContainers without giving the valid image. The TCP probe does not happen here as the cluster goes unhealthy by this unrejected misconfiguration.
 ```
"message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.initContainers[0].image: Required value, spec.initContainers[0].startupProbe: Forbidden: may not be set for init containers without restartPolicy=Always]",
 ```
#### Expected behavior?
Misoperation

## Alarm 56
trial-01-0045/0001

#### What happened
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
 ```
#### Root Cause
It misconfigured the spec.initContainers without giving the valid image. The TCP probe does not happen here as the cluster goes unhealthy by this unrejected misconfiguration.
```
"message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.initContainers[0].image: Required value, spec.initContainers[0].startupProbe: Forbidden: may not be set for init containers without restartPolicy=Always]",
```
#### Expected behavior?
Misoperation

## Alarm 57
trial-01-0046/0009

#### What happened
The cluster was not healthy. Tracking down the events logs it says the image cannot be pulled and the subsequent steps are failing.
#### Root Cause
The ACTO misconfigured the cass-management-api to some unresolvable reference as follows:
```
 "message": "Failed to pull image \"cr.k8ssandra.io/k8ssandra/cass-management-api:5.532412050.181\": rpc error: code = NotFound desc = failed to pull and unpack image \"cr.k8ssandra.io/k8ssandra/cass-management-api:5.532412050.181\": failed to resolve reference \"cr.k8ssandra.io/k8ssandra/cass-management-api:5.532412050.181\": cr.k8ssandra.io/k8ssandra/cass-management-api:5.532412050.181: not found",
```
This causes the dedicated image cannot be found, and all failed operation afterwards. The Failure was expected as the configuration was rejected by the operator.
#### Expected behavior?
False Alarm

## Alarm 58
trial-01-0047/0003

#### What happened
This is a duplicated alarm as Alarm 36.
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
It misconfigured the spec.ephemeralContainers:
```
  "message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.ephemeralContainers[0].image: Required value, spec.ephemeralContainers: Forbidden: cannot be set on create]",
```
And the changed pull policy did not acts here. The cluster was unhealthy since the misconfiguration of spec.ephemeralContainers[0].image and spec.ephemeralContainers[0]
#### Expected behavior?
Misopeation

## Alarm 59
trial-01-0049/0006

#### What happened
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
  "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The acto misconfigured the spec.ephemeralContainers:
```
  "message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: spec.volumes[1].downwardAPI.resourceFieldRef.containerName: Required value",
```
And the quantity increase did not acts here. The cluster was unhealthy since the misconfiguration of spec.volumes[1].downwardAPI.resourceFieldRef.containerName. The operator failed to reject the value and leads to create a failed pod.
#### Expected behavior?
Misopeation


## Alarm 60
trial-01-0050/0001

#### What happened
This is a duplicated alarm as Alarm 59.
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
  "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
```
    "message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: spec.volumes[1].downwardAPI.resourceFieldRef.containerName: Required value",
```
And the quantity decrease did not acts here. The cluster was unhealthy since the misconfiguration of spec.volumes[1].downwardAPI.resourceFieldRef.containerName. The operator failed to reject the value and leads to create a failed pod.
#### Expected behavior?
Misopeation

## Alarm 61
trial-01-0051/0001

#### What happened
This is a duplicated alarm as Alarm 36.
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
It misconfigured the spec.ephemeralContainers:
```
  "message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.ephemeralContainers[0].image: Required value, spec.ephemeralContainers: Forbidden: cannot be set on create]",
```
And the changed pull policy did not acts here. The cluster was unhealthy since the misconfiguration of spec.ephemeralContainers[0].image and spec.ephemeralContainers[0]
#### Expected behavior?
Misopeation

## Alarm 62
trial-01-0052/0001

#### What happened
This is a duplicated alarm as Alarm 36.
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
It misconfigured the spec.ephemeralContainers:
```
  "message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.ephemeralContainers[0].image: Required value, spec.ephemeralContainers: Forbidden: cannot be set on create]",
```
And the changed pull policy did not acts here. The cluster was unhealthy since the misconfiguration of spec.ephemeralContainers[0].image and spec.ephemeralContainers[0]
#### Expected behavior?
Misopeation

## Alarm 63
trial-01-0053/0001

#### What happened
This is a duplicated alarm as Alarm 36.
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
It misconfigured the spec.ephemeralContainers:
```
  "message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.ephemeralContainers[0].image: Required value, spec.ephemeralContainers: Forbidden: cannot be set on create]",
```
And the changed pull policy did not acts here. The cluster was unhealthy since the misconfiguration of spec.ephemeralContainers[0].image and spec.ephemeralContainers[0]
#### Expected behavior?
Misopeation

## Alarm 64
trial-01-0054/0001

#### What happened
This is a duplicated alarm as Alarm 34.
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The pod creation failure was partly expected as the ACTO provides the invalid name to the operator. The operator's CR cannot be satisfied and the this leads to an unhealthy state.
But it also fails to provide the spec.initContainers[0].image. This should be categorized as an false alarm.
```
"message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.initContainers[0].image: Required value, spec.initContainers[0].volumeMounts[0].name: Not found: \"INVALID_NAME\"]",
```

#### Expected behavior?
False Alarm

## Alarm 65
trial-01-0055/0001

#### What happened
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The pod creation failure was casued by the misconfiguration of the spec.volumes. The deletion does not play its role here. The failure of node creation was expected per the behavior of the operator. 
```
  "message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.volumes[1].projected: Invalid value: \"ACTOKEY\": conflicting duplicate paths, spec.volumes[1].projected.sources[0].downwardAPI.fieldRef.fieldPath: Invalid value: \"ACTOKEY\": error converting fieldPath: unsupported pod version: ACTOKEY, spec.volumes[1].projected.sources[0].downwardAPI: Invalid value: \"resource\": fieldRef and resourceFieldRef can not be specified simultaneously, spec.volumes[1].projected.sources[0].serviceAccountToken.expirationSeconds: Invalid value: 3: may not specify a duration less than 10 minutes, spec.volumes[1].projected.sources[0]: Forbidden: may not specify more than 1 volume type]"
```
#### Expected behavior?
False Alarm


## Alarm 66
trial-01-0057/0002

#### What happened
This is a duplicated alarm as Alarm 43.
The system is unhealthy, since the recreation of the pod failures as the affinity rule cannot satisfy the operator's CR.
```
 "message": "0/4 nodes are available: 1 node(s) didn't match Pod's node affinity/selector. preemption: 0/4 nodes are available: 1 Preemption is not helpful for scheduling, 3 No preemption victims found for incoming pod.",
```
#### Root Cause
The nodeSelector fails here. It fails to select the matching node and cause the cluster to fail.
```
  podTemplateSpec:
    spec:
      containers: []
      nodeSelector:
        ACTOKEY: ACTOKEY
```
This operation is not detected as not rejected by the operator. 
#### Expected behavior?
Misoperation

## Alarm 67
trial-01-0058/0001

#### What happened
This is a duplicated alarm as Alarm 43.
The system is unhealthy, since the recreation of the pod failures as the affinity rule cannot satisfy the operator's CR.
```
 "message": "0/4 nodes are available: 1 node(s) didn't match Pod's node affinity/selector. preemption: 0/4 nodes are available: 1 Preemption is not helpful for scheduling, 3 No preemption victims found for incoming pod.",
```
#### Root Cause
The nodeSelector fails here. It fails to select the matching node and cause the cluster to fail.
```
  podTemplateSpec:
    spec:
      containers: []
      nodeSelector:
        ACTOKEY: ACTOKEY
```
This operation is not detected as not rejected by the operator. 
#### Expected behavior?
Misoperation

## Alarm 68
trial-01-0059/0001

#### What happened
This is a duplicated alarm as Alarm 43.
The system is unhealthy, since the recreation of the pod failures as the affinity rule cannot satisfy the operator's CR.
```
 "message": "0/4 nodes are available: 1 node(s) didn't match Pod's node affinity/selector. preemption: 0/4 nodes are available: 1 Preemption is not helpful for scheduling, 3 No preemption victims found for incoming pod.",
```
#### Root Cause
The nodeSelector fails here. It fails to select the matching node and cause the cluster to fail.
```
  podTemplateSpec:
    spec:
      containers: []
      nodeSelector:
        ACTOKEY: ''
```
This operation is not detected as not rejected by the operator. 
#### Expected behavior?
Misoperation


## Alarm 69
trial-01-0060/0001

#### What happened
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The pod creation failure was casued by the misconfiguration of the spec.volumes.ephemeral.volumeClaimTemplate.spec.selector. The deletion does not play its role here. The failure of node creation was expected per the behavior of the operator. 
```
  "message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.volumes[1].ephemeral.volumeClaimTemplate.spec.selector.matchExpressions[0].operator: Invalid value: \"ACTOKEY\": not a valid selector operator, spec.volumes[1].ephemeral.volumeClaimTemplate.spec.selector.matchExpressions[1].operator: Invalid value: \"ACTOKEY\": not a valid selector operator, spec.volumes[1].ephemeral.volumeClaimTemplate.spec.selector.matchExpressions[2].operator: Invalid value: \"ACTOKEY\": not a valid selector operator, spec.volumes[1].ephemeral.volumeClaimTemplate.spec.selector.matchExpressions[3].operator: Invalid value: \"ACTOKEY\": not a valid selector operator, spec.volumes[1].ephemeral.volumeClaimTemplate.spec.selector.matchExpressions[4].operator: Invalid value: \"ACTOKEY\": not a valid selector operator, spec.volumes[1].ephemeral.volumeClaimTemplate.spec.accessModes: Unsupported value: \"ACTOKEY\": supported values: \"ReadOnlyMany\", \"ReadWriteMany\", \"ReadWriteOnce\", \"ReadWriteOncePod\", spec.volumes[1].ephemeral.volumeClaimTemplate.spec.resources[storage]: Required value, spec.volumes[1].ephemeral.volumeClaimTemplate.spec.storageClassName: Invalid value: \"ACTOKEY\": a lowercase RFC 1123 subdomain must consist of lower case alphanumeric characters, '-' or '.', and must start and end with an alphanumeric character (e.g. 'example.com', regex used for validation is '[a-z0-9]([-a-z0-9]*[a-z0-9])?(\\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*'), spec.volumes[1].ephemeral.volumeClaimTemplate.spec.volumeMode: Unsupported value: \"ACTOKEY\": supported values: \"Block\", \"Filesystem\", spec.volumes[1].ephemeral.volumeClaimTemplate.spec.dataSource.apiGroup: Invalid value: \"ACTOKEY\": a lowercase RFC 1123 subdomain must consist of lower case alphanumeric characters, '-' or '.', and must start and end with an alphanumeric character (e.g. 'example.com', regex used for validation is '[a-z0-9]([-a-z0-9]*[a-z0-9])?(\\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*'), spec.volumes[1].ephemeral.volumeClaimTemplate.spec.dataSourceRef.apiGroup: Invalid value: \"ACTOKEY\": a lowercase RFC 1123 subdomain must consist of lower case alphanumeric characters, '-' or '.', and must start and end with an alphanumeric character (e.g. 'example.com', regex used for validation is '[a-z0-9]([-a-z0-9]*[a-z0-9])?(\\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*'), spec.volumes[1].ephemeral.volumeClaimTemplate.spec.dataSourceRef.namespace: Invalid value: \"ACTOKEY\": a lowercase RFC 1123 label must consist of lower case alphanumeric characters or '-', and must start and end with an alphanumeric character (e.g. 'my-name',  or '123-abc', regex used for validation is '[a-z0-9]([-a-z0-9]*[a-z0-9])?'), spec.volumes[1].ephemeral.volumeClaimTemplate.spec: Invalid value: field.Path{name:\"dataSource\", index:\"\", parent:(*field.Path)(0xc00c9873e0)}: may not be specified when dataSourceRef.namespace is specified]"
```
#### Expected behavior?
False Alarm

## Alarm 70
trial-01-0061/0001

#### What happened
This is a duplicated alarm as the alarm 29
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The ACTO fails to provide a valid value for spec.volumes[4].ephemeral.volumeClaimTemplate.spec.accessModes. The mutated states cannot satisify the cass-operator CR. It also fails to provide valid spec.volumes[4].ephemeral.volumeClaimTemplate.spec.resources[storage]. Which leads the operation fails.
```
  "message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.volumes[4].ephemeral.volumeClaimTemplate.spec.accessModes: Required value: at least 1 access mode is required, spec.volumes[4].ephemeral.volumeClaimTemplate.spec.resources[storage]: Required value, spec.containers[0].volumeMounts[0].name: Not found: \"b\", spec.containers[1].volumeMounts[0].name: Not found: \"b\"]",
```
#### Expected behavior?
False Alarm

## Alarm 71
trial-01-0062/0001

#### What happened
This is a duplicated alarm as the alarm 29
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The ACTO fails to provide a valid value for spec.volumes[4].ephemeral.volumeClaimTemplate.spec.accessModes. The mutated states cannot satisify the cass-operator CR. It also fails to provide valid spec.volumes[4].ephemeral.volumeClaimTemplate.spec.resources[storage]. Which leads the operation fails.
```
  "message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.volumes[4].ephemeral.volumeClaimTemplate.spec.accessModes: Required value: at least 1 access mode is required, spec.volumes[4].ephemeral.volumeClaimTemplate.spec.resources[storage]: Required value, spec.containers[0].volumeMounts[0].name: Not found: \"b\", spec.containers[1].volumeMounts[0].name: Not found: \"b\"]",
```
#### Expected behavior?
False Alarm


## Alarm 72
trial-01-0063/0001

#### What happened
This is a duplicated alarm as the alarm 29
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The ACTO fails to provide a valid value for spec.volumes[4].ephemeral.volumeClaimTemplate.spec.accessModes. The mutated states cannot satisify the cass-operator CR. It also fails to provide valid spec.volumes[4].ephemeral.volumeClaimTemplate.spec.resources[storage]. Which leads the operation fails.
```
  "message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.volumes[4].ephemeral.volumeClaimTemplate.spec.accessModes: Required value: at least 1 access mode is required, spec.volumes[4].ephemeral.volumeClaimTemplate.spec.resources[storage]: Required value, spec.containers[0].volumeMounts[0].name: Not found: \"30px\", spec.containers[1].volumeMounts[0].name: Not found: \"30px\"]",
```
#### Expected behavior?
False Alarm

## Alarm 73
trial-01-0065/0007

#### What happened
This is a duplicated alarm as the alarm 29
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The ACTO fails to provide a valid value for spec.volumes[4].ephemeral.volumeClaimTemplate.spec.accessModes. The mutated states cannot satisify the cass-operator CR. It also fails to provide valid spec.volumes[4].ephemeral.volumeClaimTemplate.spec.resources[storage]. Which leads the operation fails.
```
  "message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.volumes[4].ephemeral.volumeClaimTemplate.spec.accessModes: Required value: at least 1 access mode is required, spec.volumes[4].ephemeral.volumeClaimTemplate.spec.resources[storage]: Required value, spec.volumes[4].ephemeral.volumeClaimTemplate.spec.storageClassName: Invalid value: \"ACTOKEY\": a lowercase RFC 1123 subdomain must consist of lower case alphanumeric characters, '-' or '.', and must start and end with an alphanumeric character (e.g. 'example.com', regex used for validation is '[a-z0-9]([-a-z0-9]*[a-z0-9])?(\\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*'), spec.containers[0].volumeMounts[0].name: Not found: \"e\", spec.containers[1].volumeMounts[0].name: Not found: \"e\"]"

```
#### Expected behavior?
False Alarm


## Alarm 74
trial-01-0066/0003

#### What happened
This is a duplicated alarm as the alarm 29
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The ACTO fails to provide a valid value for spec.volumes[4].ephemeral.volumeClaimTemplate.spec.accessModes. The mutated states cannot satisify the cass-operator CR. It also fails to provide valid spec.volumes[4].ephemeral.volumeClaimTemplate.spec.resources[storage]. Which leads the operation fails.
```
  "message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.volumes[4].ephemeral.volumeClaimTemplate.spec.accessModes: Required value: at least 1 access mode is required, spec.volumes[4].ephemeral.volumeClaimTemplate.spec.resources[storage]: Required value, spec.containers[0].volumeMounts[0].name: Not found: \"r\", spec.containers[1].volumeMounts[0].name: Not found: \"r\"]",
```
#### Expected behavior?
False Alarm

## Alarm 75
trial-01-0067/0001

#### What happened
This is a duplicated alarm as Alarm 25.
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True. 
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The mutated CRD does not provide the required key-value for the spec.containers[0].image. The causes the failure of pod creation.
```
"message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: spec.containers[0].image: Required value",
```
#### Expected behavior?
False Alarm

## Alarm 76
trial-01-0068/0002

#### What happened
The array deletion causing non-matching state derived from inputs.  
#### Root Cause
The deletion of the affinty role here in all stages are making no effects since there is only 1 non-matching pod here. The ACTOKEY will not have matching node. The NotPresent is expected result and this alarm is a false alarm. 
#### Expected behavior?
False Alarm

## Alarm 77
trial-01-0069/0002

#### What happened
This is a duplicated alarm as Alarm 76.
The array deletion causing non-matching state derived from inputs. 
#### Root Cause
The deletion of the affinty role here in all stages are making no effects since there is only 1 non-matching pod here. The ACTOKEY will not have matching node. The NotPresent is expected result and this alarm is a false alarm. 
#### Expected behavior?
False Alarm

## Alarm 78
trial-01-0071/0003

#### What happened
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True. 
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The ACTO gives bad value for spec.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.topologyKey violates the requirement for the topologyKey, as it should not be empty. This raises the following events:
```
  "message": "create Pod cluster1-test-cluster-vqywbgfcwk-sts-0 in StatefulSet cluster1-test-cluster-vqywbgfcwk-sts failed error: Pod \"cluster1-test-cluster-vqywbgfcwk-sts-0\" is invalid: [spec.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.: Required value: can not be empty, spec.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.topologyKey: Invalid value: \"\": name part must be non-empty, spec.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].podAffinityTerm.topologyKey: Invalid value: \"\": name part must consist of alphanumeric characters, '-', '_' or '.', and must start and end with an alphanumeric character (e.g. 'MyName',  or 'my.name',  or '123-abc', regex used for validation is '([A-Za-z0-9][-A-Za-z0-9_.]*)?[A-Za-z0-9]')]"
```
#### Expected behavior?
False Alarm

## Alarm 79
trial-01-0072/0001

#### What happened
This is a duplicated alarm as Alarm 34.
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The pod creation failure was partly expected as the ACTO provides the invalid name to the operator. The operator's CR cannot be satisfied and the this leads to an unhealthy state.
But it also fails to provide the spec.initContainers[0].image. This should be categorized as an false alarm.
```
"message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.initContainers[0].image: Required value, spec.initContainers[0].volumeMounts[0].name: Not found: \"INVALID_NAME\"]",
```

#### Expected behavior?
False Alarm

## Alarm 80
trial-01-0073/0005

#### What happened
The ACTO provides invalid image name and the pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The ACTO provides invalid image name that violates the CR requirements. The rejection was expected and should not be considered as an alarm.
  "message": "Failed to apply default image tag \"ACTOKEY\": couldn't parse image name \"ACTOKEY\": invalid reference format: repository name (library/ACTOKEY) must be lowercase",
#### Expected behavior?
False Alarm

## Alarm 81
trial-01-0074/0001

#### What happened
This is a duplicated alarm as Alarm 80.
The ACTO provides invalid image name and the pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The ACTO provides invalid image name that violates the CR requirements. The rejection was expected and should not be considered as an alarm.
  "message": "Failed to apply default image tag \"ACTOKEY\": couldn't parse image name \"ACTOKEY\": invalid reference format: repository name (library/ACTOKEY) must be lowercase",
#### Expected behavior?
False Alarm

## Alarm 82
trial-01-0075/0001

## Alarm 79
trial-01-0072/0001

#### What happened
This is a duplicated alarm as Alarm 34.
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The pod creation failure was expected as the ACTO provides the invalid name to the operator. The operator's CR cannot be satisfied and the this leads to an unhealthy state.
This should be categorized as an false alarm.
```
  "message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: spec.initContainers[0].image: Required value"
```

#### Expected behavior?
False Alarm

## Alarm 83
trial-01-0076/0002

#### What happened
This is a duplicated alarm as Alarm 56.
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
 ```
#### Root Cause
It misconfigured the spec.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].weight without giving the valid value. The CR cannot be satisfied and thus the rejection causes the creation was failed.
```
  "message": "create Pod cluster1-test-cluster-bgfrwagcer-sts-0 in StatefulSet cluster1-test-cluster-bgfrwagcer-sts failed error: Pod \"cluster1-test-cluster-bgfrwagcer-sts-0\" is invalid: spec.affinity.podAntiAffinity.preferredDuringSchedulingIgnoredDuringExecution[0].weight: Invalid value: 0: must be in the range 1-100"
```
#### Expected behavior?
False Alarm

## Alarm 84
trial-01-0098/0002

#### What happened
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
 ```
#### Root Cause
It misconfigured the spec.topologySpreadConstraints[0].whenUnsatisfiable without giving the valid value. The CR cannot be satisfied and thus the rejection causes the creation was failed.
```
  "message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.topologySpreadConstraints[0].whenUnsatisfiable: Unsupported value: \"ACTOKEY\": supported values: \"DoNotSchedule\", \"ScheduleAnyway\", spec.topologySpreadConstraints[0].minDomains: Invalid value: 1: can only use minDomains if whenUnsatisfiable=DoNotSchedule, not ACTOKEY, spec.topologySpreadConstraints[0].nodeAffinityPolicy: Unsupported value: \"ACTOKEY\": supported values: \"Honor\", \"Ignore\", spec.topologySpreadConstraints[0].labelSelector.matchExpressions[0].operator: Invalid value: \"ACTOKEY\": not a valid selector operator, spec.topologySpreadConstraints[0].labelSelector.matchExpressions[1].operator: Invalid value: \"ACTOKEY\": not a valid selector operator, spec.topologySpreadConstraints[0].labelSelector.matchExpressions[2].operator: Invalid value: \"ACTOKEY\": not a valid selector operator]",
```
#### Expected behavior?
False Alarm

## Alarm 85
trial-01-0079/0004

#### What happened
This is a duplicated alarm as Alarm 34.
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The pod creation failure was expected as the ACTO provides the invalid name to the operator. The operator's CR cannot be satisfied and the this leads to an unhealthy state.
This should be categorized as an false alarm.
```
  "message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: spec.initContainers[0].image: Required value"
```

#### Expected behavior?
False Alarm

## Alarm 86
trial-01-0080/0001

#### What happened
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
It misconfigured the spec.ephemeralContainers with INVALID_NAME
```
  "message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.ephemeralContainers[0].image: Required value, spec.ephemeralContainers[0].envFrom[0].secretRef.name: Invalid value: \"INVALID_NAME\": a lowercase RFC 1123 subdomain must consist of lower case alphanumeric characters, '-' or '.', and must start and end with an alphanumeric character (e.g. 'example.com', regex used for validation is '[a-z0-9]([-a-z0-9]*[a-z0-9])?(\\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*'), spec.ephemeralContainers: Forbidden: cannot be set on create]",
```
And the INVALID_NAME did not acts here. The cluster was unhealthy since the misconfiguration of spec.ephemeralContainers[0].image. There's no valid value for the key image provided. And the pod creation was expected as the operator rejects the invalid condiguration.
#### Expected behavior?
False Alarm

## Alarm 87
trial-01-0082/0002

#### What happened
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The ACTO sets the readinessGates.conditionType to ACTOKEY, which is not in the pod's condition list with matching type.. This configuration cannot satisfy the CR and the recreation was thus failed.                          
#### Expected behavior?
Misoepration. The operator does not explicitly reject this states and it fails silently with unhealthy states.

## Alarm 88
trial-01-0083/0002

#### What happened
This is a duplicated alarm as the Alarm 87.
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The ACTO sets the readinessGates.conditionType to ACTOKEY, which is not in the pod's condition list with matching type.. This configuration cannot satisfy the CR and the recreation was thus failed.         
#### Expected behavior?
Misoepration. The operator does not explicitly reject this states and it fails silently with unhealthy states.

## Alarm 89
trial-01-0084/0001

#### What happened
This is a duplicated alarm as the Alarm 87.
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The ACTO sets the readinessGates.conditionType to ACTOKEY, which is not in the pod's condition list with matching type.. This configuration cannot satisfy the CR and the recreation was thus failed.         
#### Expected behavior?
Misoepration. The operator does not explicitly reject this states and it fails silently with unhealthy states.

## Alarm 90
trial-01-0085/0002

#### What happened
This is a duplicated alarm as the alarm 29
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The ACTO fails to provide a valid value for spec.containers[0].volumeMounts[0].name. The mutated states cannot satisify the cass-operator CR, which leads the operation fails.
```
  "message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.containers[0].volumeMounts[0].name: Not found: \"t0qrhaoi\", spec.containers[1].volumeMounts[0].name: Not found: \"t0qrhaoi\"]"
```
#### Expected behavior?
False Alarm

## Alarm 91
trial-01-0086/0001

#### What happened
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The ACTO provides some invalid configuration for 
```
spec:
  cdc:
    cdcWorkingDir: ACTOKEY
    pulsarServiceUrl: vrpbawxtdv
```
The cdcWorkingDir and the pulsarServiceUrl are both unreachable. There is not detailed description in CR for the config in cdc fields so the categorization is hard. The operator was unhealthy, but fails/unable to reject the incorrect configurations. So I propose it is a misoperation.
#### Expected behavior?
Misoperation

## Alarm 92
trial-01-0087/0001

#### What happened
This is a duplicated alarm as Alarm 91
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The ACTO provides some invalid configuration for 
```
spec:
  cdc:
    cdcWorkingDir: ACTOKEY
    pulsarServiceUrl: vrpbawxtdv
```
The cdcWorkingDir and the pulsarServiceUrl are both unreachable. There is not detailed description in CR for the config in cdc fields so the categorization is hard. The operator was unhealthy, but fails/unable to reject the incorrect configurations. So I propose it is a misoperation.
#### Expected behavior?
Misoperation

## Alarm 93
trial-01-0088/0001

#### What happened
This is a duplicated alarm as Alarm 91
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The ACTO provides some invalid configuration for 
```
spec:
  cdc:
    cdcWorkingDir: ACTOKEY
    pulsarServiceUrl: vrpbawxtdv
```
The cdcWorkingDir and the pulsarServiceUrl are both unreachable. There is not detailed description in CR for the config in cdc fields so the categorization is hard. The operator was unhealthy, but fails/unable to reject the incorrect configurations. So I propose it is a misoperation.
#### Expected behavior?
Misoperation

## Alarm 94
trial-01-0089/0001

#### What happened
This is a duplicated alarm as Alarm 25.
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True. 
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The mutated CRD does not provide the required key-value for the spec.containers[0].image. The causes the failure of pod creation. The INVALID_NAME does not act its role here. 
```
  "message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.containers[0].image: Required value, spec.containers[0].ports[0].name: Invalid value: \"INVALID_NAME\": must contain only alpha-numeric characters (a-z, 0-9), and hyphens (-), spec.containers[0].ports[0].name: Invalid value: \"INVALID_NAME\": must contain at least one letter (a-z)]",
```
#### Expected behavior?
False Alarm

## Alarm 95
trial-01-0091/0001

#### What happened
This is a duplicated alarm as Alarm 36.
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
It misconfigured the spec.ephemeralContainers:
```
  "message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.ephemeralContainers[0].image: Required value, spec.ephemeralContainers: Forbidden: cannot be set on create]",
```
And the boolean toggle did not acts here. The cluster was unhealthy since the misconfiguration of spec.ephemeralContainers[0].image and spec.ephemeralContainers[0]
#### Expected behavior?
False Alarm

## Alarm 96
trial-01-0092/0001

#### What happened
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The INVALID NAME acts here. The pod fails since the invalid value for configmap. This operator behavior is expected. The unhealthy state is also expected as there will not be any ready node available. 
```
 "message": "MountVolume.SetUp failed for volume \"e7mavy\" : configmap \"INVALID_NAME\" not found",
```
#### Expected behavior?
False Alarm

## Alarm 97
trial-01-0093/0005

#### What happened
This is a duplicated alarm as Alarm 34.
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The pod creation failure was expected as the ACTO provides the invalid name to the operator. Also the spec.initContainers[0].lifecycle was incorrectly set. Thus, the operator's CR cannot be satisfied and the this leads to an unhealthy state. This should be categorized as an false alarm.
```
  "message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.initContainers[0].image: Required value, spec.initContainers[0].lifecycle: Forbidden: may not be set for init containers without restartPolicy=Always]",  
```

#### Expected behavior?
False Alarm

## Alarm 98
trial-01-0094/0001

#### What happened
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The pod creation failure was expected as the ACTO provides the invalid spec.dnsPolicy to the operator. Thus, the operator's CR cannot be satisfied and the this leads to an unhealthy state. This should be categorized as an false alarm.
 "message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: spec.dnsPolicy: Unsupported value: \"ACTOKEY\": supported values: \"ClusterFirstWithHostNet\", \"ClusterFirst\", \"Default\", \"None\"",
#### Expected behavior?
False Alarm

## Alarm 99
trial-01-0095/0001

#### What happened
This is a duplicated alarm as Alarm 98.
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The pod creation failure was expected as the ACTO provides the invalid spec.dnsPolicy to the operator. Thus, the operator's CR cannot be satisfied and the this leads to an unhealthy state. This should be categorized as an false alarm.
```
 "message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: spec.dnsPolicy: Unsupported value: \"ACTOKEY\": supported values: \"ClusterFirstWithHostNet\", \"ClusterFirst\", \"Default\", \"None\"",
 ```
#### Expected behavior?
False Alarm

## Alarm 100
trial-01-0098/0002

#### What happened
This is a duplicated alarm as Alarm 98.
Pod creation failed. This results in a unhealthy cluster and sets the Alarm to True.
```
 "message": "StatefulSet acto-namespace/cluster1-test-cluster-default-sts is recreating failed Pod cluster1-test-cluster-default-sts-0",
```
#### Root Cause
The pod creation failure was expected as the ACTO provides the invalid spec.topologySpreadConstraints to the operator. Thus, the operator's CR cannot be satisfied and the this leads to an unhealthy state. This should be categorized as an false alarm.
```
  "message": "create Pod cluster1-test-cluster-default-sts-0 in StatefulSet cluster1-test-cluster-default-sts failed error: Pod \"cluster1-test-cluster-default-sts-0\" is invalid: [spec.topologySpreadConstraints[0].whenUnsatisfiable: Unsupported value: \"ACTOKEY\": supported values: \"DoNotSchedule\", \"ScheduleAnyway\", spec.topologySpreadConstraints[0].minDomains: Invalid value: 1: can only use minDomains if whenUnsatisfiable=DoNotSchedule, not ACTOKEY, spec.topologySpreadConstraints[0].nodeAffinityPolicy: Unsupported value: \"ACTOKEY\": supported values: \"Honor\", \"Ignore\", spec.topologySpreadConstraints[0].labelSelector.matchExpressions[0].operator: Invalid value: \"ACTOKEY\": not a valid selector operator, spec.topologySpreadConstraints[0].labelSelector.matchExpressions[1].operator: Invalid value: \"ACTOKEY\": not a valid selector operator, spec.topologySpreadConstraints[0].labelSelector.matchExpressions[2].operator: Invalid value: \"ACTOKEY\": not a valid selector operator]",
```
#### Expected behavior?
False Alarm

