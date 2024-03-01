# Analysis of Acto Test Result for grafana-operator

## Categorization Summary

| Alarm # | Trial #      | Category      | Previous Occurance? |
| ------: | ------------ | ------------- | ------------------- |
|       1 | 00-0000/0010 | Mis-operation |                     |
|       2 | 00-0001/0003 | Mis-operation | See Alarm #1.       |
|       3 | 00-0005/0002 | Bug           |                     |
|       4 | 00-0006/0002 | Bug           | See Alarm #3.       |
|       5 | 00-0009/0003 | Bug           |                     |
|       6 | 00-0010/0002 | False Alarm   |                     |
|       7 | 00-0011/0002 | False Alarm   | See Alarm #6.       |
|       8 | 00-0012/0002 | False Alarm   | See Alarm #6.       |
|       9 | 00-0013/0003 | False Alarm   | See Alarm #6.       |
|      10 | 00-0014/0001 | Bug           |                     |

## Alarm 1

In Trial 00-0000/0010, Acto changed the `deployment.spec.template.spec.containers[0].ports[0].protocol` field from `"ACTOKEY"` to `""`. This appears to b an invalid configuration for two reasons:
 1. The protocol should be restricted to one of `"UDP"`, `"TCP"`, or `"STCP"`.
 2. The `containerPort` field is set to `0`, which is invalid.

## Alarm 2

In Trial 00-0001/0003, we encounter the same issue identified in [Alarm 1](#alarm-1).

## Alarm 3

In Trial 00-0005/0002, Acto changes the `deployment.spec.template.spec.hostPID` field from `true` to `false`. As far as I can tell, this field is never accessed by the reconcilers.

Classifying this as a bug.

## Alarm 4 

In Trial 00-0006/0002, we encounter the same issue identified in [Alarm 3](#alarm-3).

## Alarm 5

In Trial 00-0009/0003, Acto changed the `deployment.spec.template.spec.initContainers[0].readinessProbe.httpGet.path` field from `"ACTOKEY"` to `""`. From what I can tell, the grafana-operator currently ignores this field in favor of a hardcoded value in `deployment_reconciler.go`. This does not appear to be documented anywhere.

Therefore, we will (at least momentarily) classify this as a bug in grafana-operator.

## Alarm 6

In Trial 00-0010/0002, Acto modifies the `deployment.spec.template.spec.containers[index].lifecycle.postStart.tcpSocket.port` field. Since the `tcpSocket` field is [now deprecated](https://grafana.github.io/grafana-operator/docs/api/#grafanaspecdeploymentspectemplatespeccontainersindexlifecyclepoststarttcpsocket), we can consider this a false alarm.

## Alarm 7

In Trial 00-0011/0002, we encounter the same false alarm as in [Alarm 6](#alarm-6).

## Alarm 8

In Trial 00-0012/0002, we encounter the same false alarm as in [Alarm 6](#alarm-6).

## Alarm 9

In Trial 00-0013/0003, we encounter the same false alarm as in [Alarm 6](#alarm-6).

## Alarm 10

In Trial 00-0014/0001, Acto changes the `jsonnet.libraryLabelSelector.matchLabels.ACTOKEY` field from `"NotPresent"` to `"ACTOKEY"`. As far as I can tell, the `jsonnet.libraryLabelSelector` is never used by the operator.

Classifying this as a bug.