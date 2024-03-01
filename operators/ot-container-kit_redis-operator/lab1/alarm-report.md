---
name: Alarm Inspection Report
about: An analysis report for the alarms produced by Acto
---

**ALARM 1**
trial-00-0059/0001

## What happened
When acto adds a sidecar with invalid parameters to the spec, a pod crashes.

## Root Cause
The spec does not specify a valid sidecar. The operator code attempts to update the `SatetfullSet`  with the updated spec in `k8sutils/satefulset.go` without performing any validation on the statefulset spec.

## Expected behavior?
This is a misoperation. The operator should be able to easily reject the new spec as the sidecar spec does not specify a valid container

**ALARM 2**
trial-02-0059/0001

## What happened
Same as ALARM 1 except with an array of invalid sidecars.

## What happened
When acto adds a sidecar with invalid parameters to the spec, a pod crashes.

**ALARM 3**
trial-02-0059/0001

## What happened
When acto adds a TLS configuration with invalid parameters to the spec, a pod crashes.

## Root Cause
The spec does not specify a valid TLS cert. The operator code attempts to update the `SatetfullSet`  with the updated spec in `k8sutils/satefulset.go` without performing any validation on the statefulset spec. When the cluster restarts it repeatedly fails as it is unable to create a pod with the invalid TLS spec

## Expected behavior?
This is a misoperation. The operator should be able to easily reject the new spec as the TLS spec does not specify a valid cert.

**ALARM 4**
trial-01-0042/0001

## What happened
Same as ALARM 3.

**ALARM 5**
trial-02-0040/0001

## What happened
Same as ALARM 3.

**ALARM 6**
trial-00-0051/0001

## What happened
When acto adds a `RedisSecret` with "ACTOKEY" as the key, the pod enters an unhealthy state.

## Root Cause
The operator assumes that the `RedisSecret` field will specify a password for Redis. As such it assumes that the value of key will be "password" and that the name will be a valid password. The operator only checks if `RedisSecret` has been defined and does not check if name as been specified. As such when the operator attempts to create a pod with the new spec, it fails when it tries to get the name that is not specified. For example at: https://github.com/OT-CONTAINER-KIT/redis-operator/blob/891d740293ab27ee8502f212088d05e0b29cb15f/k8sutils/redis.go#L113.

## Expected behavior?
This is a misoperation. The operator should be able to easily reject the spec as the password is not properly specified. 


**ALARM 7**
trial-01-0044/0001

## What happened
Same as ALARM 6.

**ALARM 8**
trial-01-0045/0001

## What happened
Same as ALARM 6.

**ALARM 9**
trial-00-0051/0001

## What happened
When acto adds a `service` with "ClusterIP" as the `serviceType`, the pod enters an unhealthy state.

## Root Cause
The operator assumes that the `service` will specify a valid service, either a load balancer, node port, or cluster IP. However, it does not check if all the fields are specified or if they are valid. In this test case since only the `serviceType` is specified, the operator fails to create a pod with the new spec.

## Expected behavior?
This is a misoperation. The operator should be able to easily reject the spec as the service is not properly defined. 

**ALARM 10**
trial-01-0045/0001

## What happened
Similar to ALARM 9. Only `annotation` is specified within `service`.
