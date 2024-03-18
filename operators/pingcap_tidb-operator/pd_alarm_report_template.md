---
name: Alarm Inspection Report
about: An analysis report for the alarms produced by Acto

---

# Alarm 1


## What happened
In ti-db pd subsystem the value of `['spec']['security_context']['run_as_group']` has gone from NoneType to int in an integer deletion test. The value originates at null and transitions to 4.

## Root Cause
This value seems to be managed by the larger kubernetes api and seems relatively untouched by ti-db directly. This can be seen in `tidb-operator/charts/tidb-operator/values.yaml` where they refer to SecurityContext as just part of the large Kubernetes Security Context. When introduced operator does not have any logic to consider run_as_group.

## Expected behavior?
True alarm, operator should consider run_as_group and reconcile cases where it is set. 

# Alarm 2

## What happened
In ti-db pd subsystem the value of `['spec']['security_context']['run_as_group']` has gone from NoneType to int in an integer change test. The value originates at null and transitions to 2.

## Root Cause
This value seems to be managed by the larger kubernetes api and seems relatively untouched by ti-db directly. This can be seen in `tidb-operator/charts/tidb-operator/values.yaml` where they refer to SecurityContext as just part of the large Kubernetes Security Context. When introduced operator does not have any logic to consider run_as_group after initalization.

## Expected behavior?
True alarm, operator should consider run_as_group and reconcile cases where it is set. 

# Alarm 3


## What happened
In ti-db pd subsystem the value of `['spec']['security_context']['run_as_user']` has gone from NoneType to int in an integer deletion test. The value originates at null and transitions to 1.

## Root Cause
This value seems to be managed by the larger kubernetes api and seems relatively untouched by ti-db directly. This can be seen in `tidb-operator/charts/tidb-operator/values.yaml` where they refer to SecurityContext as just part of the large Kubernetes Security Context. When introduced operator does not have any logic to consider run_as_user.

## Expected behavior?
True alarm, operator should consider run_as_user and reconcile cases where it is set. 

# Alarm 4

## What happened
In ti-db pd subsystem the value of `['spec']['security_context']['run_as_user']` has gone from NoneType to int in an integer change test. The value originates at null and transitions to 2.

## Root Cause
This value seems to be managed by the larger kubernetes api and seems relatively untouched by ti-db directly. This can be seen in `tidb-operator/charts/tidb-operator/values.yaml` where they refer to SecurityContext as just part of the large Kubernetes Security Context. When introduced operator does not have any logic to consider run_as_user after initalization.

## Expected behavior?
True alarm, operator should consider run_as_user and reconcile cases where it is set. 

# Alarm 5

## What happened
After inserting and deleting podAffinityTerm the Controller goes into an unhealthy state and raises an Acto Alarm.

## Root Cause 
The operator causes a PD failover after the state is unreconcilebile after being unable to select for a null label selector. Since no key is found the Operator updates the statefulset and when the pod is accessed again it is unavailable (is not found in set). This creates a loop where the operator keeps trying to select the same null pod which results in nothing.

## Expected behavior?
True Alarm, ti-db needs to be modified to be able to reconcile state after add and deletion of affinity.

# Alarm 6

## What happened
After inserting an empty string into podAffinityTerm the Controller goes into an unhealthy state and raises an Acto Alarm.

## Root Cause 
The operator causes a PD failover after the state is unreconcilebile after being unable to select for a null label selector. Since no key is found the Operator updates the statefulset and when the pod is accessed again it is unavailable (is not found in set). This creates a loop where the operator keeps trying to select the same null pod which results in nothing.

## Expected behavior?
True Alarm, ti-db needs to be modified to be able to reconcile state after the insertion of an empty string.

# Alarm 7

## What happened
After inserting podAffinity and changing weight from 0 to 1 PD health raises a warning causing Acto to raise an alarm

## Root Cause 
The operator causes a PD failover after the state is unreconcilebile after being unable to select for a null label selector. Since no key is found the Operator updates the statefulset and when the pod is accessed again it is unavailable (is not found in set). This creates a loop where the operator keeps trying to select the same null pod which results in nothing.

## Expected behavior?
True Alarm, ti-db needs to be modified to be able to reconcile state after weight is set 0 in podAffinity

# Alarm 8

## What happened
ti-db cluster was not proerply initalized since an invalid configuration was used

## Root Cause
The yaml file used in testing used an invalid name which caused the operator to fail on application. The invalid case comes from an invalid `additionalContainers` parameter.

## Expected behavior?
False Alarm, when an invalid configuration is used a cluster should fail.

# Alarm 9

## What happened
An invalid parameter was tested in `initContainers` causing a PD failover marking the pod as unhealthy. 

## Root Cause
In the unhealthy state the pod is unable to reconcile with the invalid paramter and the pod is removed from the healthy set causing it to constantly try to find the work cluster.

## Expected behavior?
True alarm, the operater should be able to reconcile with an invalid initContainer if it was in a valid state prior. 

# Alarm 10

## What happened
During the attempt to scale the operator to overload levels the operator reachs an unhealthy unrecoverable state.

## Root Cause
Changing the state to 1000 replicas causes a case were multiple writes are attempted `test-cluster-pd` causing an indeterminate state where two writers are present.

## Expected behavior?
True alarm, some modification should be made to allow for only one writer to exist to modifying `test-cluster-pd`

# Alarm 11

## What happened 
After inserting the `requiredDuringSchedulingIgnoredDuringExecution` in `podAffinity` a PD failover is caused marking the pod as unhealthy.

## Root Cause
After being put into an unhealthy state from the PD failover the pod attempted to correct the unhealthy pod but fail to find the pod contiously trying to upgrade.

## Expected behavior?
True alarm, some modification should be made to allow for a change in podAffinity member tags without the operater reaching an unreconcilable state.

# Alarm 12

## What happened 
After inserting the `preferedDuringSchedulingIgnoredDuringExecution` in `podAntiAffinity` and then deleting the contents of `topologyKey` a PD failover is caused marking the pod as unhealthy.

## Root Cause
After being put into an unhealthy state from the PD failover the pod attempted to correct the unhealthy pod but fail to find the pod contiously trying to upgrade. The pod is initally elected leader but transfers leadership after trying to sync after updating with its new contents.

## Expected behavior?
True alarm, some modification should be made to allow for a change in podAntiAffinity member tags without the operater reaching an unreconcilable state.

# Alarm 13 

## What happened 
After inserting the `requiredDuringSchedulingIgnoredDuringExecution` in `podAntiAffinity` and putting a random string for `namespace` a PD failover is caused marking the pod as unhealthy.

## Root Cause
After being put into an unhealthy state the pod becomes unselectable from the operator with a null label selector causing no pod matches.

## Expected behavior?
True alarm, some modification should be made to allow for a change in podAntiAffinity member tags without the operater reaching an unreconcilable state.

# Alarm 14

## What happened 
After inserting the `requiredDuringSchedulingIgnoredDuringExecution` in `podAntiAffinity` and then deleting the contents of `namespace` a PD failover is caused marking the pod as unhealthy.

## Root Cause
After being put into an unhealthy state the pod becomes unselectable from the operator with a null label selector causing no pod matches.

## Expected behavior?
True alarm, some modification should be made to allow for a change in podAntiAffinity member tags without the operater reaching an unreconcilable state.

# Alarm 15

## What happened 
After inserting the `requiredDuringSchedulingIgnoredDuringExecution` in `podAntiAffinity` and putting an empty string for `namespace` a PD failover is caused marking the pod as unhealthy.

## Root Cause
After being put into an unhealthy state the pod becomes unselectable from the operator with a null label selector causing no pod matches.

## Expected behavior?
True alarm, some modification should be made to allow for a change in podAntiAffinity member tags without the operater reaching an unreconcilable state.

# Alarm 16

## What happened 
After inserting the `requiredDuringSchedulingIgnoredDuringExecution` in `podAffinity` and testing the deletion of an object a PD failover is caused.

## Root Cause
After being put into an unhealthy state from the PD failover the pod attempted to correct the unhealthy pod but fail to find the pod contiously trying to upgrade.

## Expected behavior?
True alarm, some modification should be made to allow for a change in podAffinity member tags without the operater reaching an unreconcilable state.








