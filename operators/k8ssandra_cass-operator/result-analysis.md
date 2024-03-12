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
Misoperation

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
Misoperation

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
Misoperation


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
Misoperation

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
Misoperation

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
Misoperation. Probably add the detection for the mountpoint/paths and generate pseudo/generally used path instead.

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
Misoperation. It is not caused by setting the invalid name, but is caused by inproperly setting spec.ephemeralContainers[0].image and  spec.ephemeralContainers[0].startupProbe.

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
Misoperation. 

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
Misoperation

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
Misoperation

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
Misoperation

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
Misoperation

## Alarm 16
trial-00-0017/0003

#### What happened
#### Root Cause
#### Expected behavior?

## Alarm 17
trial-00-0018/0001

#### What happened
#### Root Cause
#### Expected behavior?

## Alarm 18
trial-00-0019/0001

#### What happened
#### Root Cause
#### Expected behavior?

## Alarm 19
trial-00-0020/0001

#### What happened
#### Root Cause
#### Expected behavior?

## Alarm 20
trial-01-0000/0001

#### What happened
#### Root Cause
#### Expected behavior?