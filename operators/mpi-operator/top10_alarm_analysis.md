# Alarm 1
trial_id: trial-00-0001/0003
## What happened
Acto deletes the apiVersion, but the system state dose not change.

Nothing happened in the state transition?

Acto’s oracles raised an alarm because Acto expects the system state should have been changed.

## Categorization
False Alarm

## Root Cause
Acto delete the apiVersion, then the apiVersion is set to its default value. Therefore the operator don't change the system state. https://github.com/kubeflow/mpi-operator/blob/master/deploy/v2beta1/mpi-operator.yaml#L6705

## Expected behavior?
It would be hard for Acto to **understand** the meaning of each field. So no need to fix Acto.

---
# Alarm 2
trial_id: trial-00-0002/0003
## What happened
Acto deletes the items in downwardAPI. However, the system state is not changed.
## Categorization
Misoperation
## Root Cause
In trial-00-0002/mutated-003.yaml we can see that Acto delete the item of downwardAPI in the `ACTOKEY` field. Since the operator operates `Worker` and `Launcher`, the operator's behavior on `ACTOKEY` is **undefined** and in this case deleting the item of downwardAPI don't change the system state. And the mpi-operator should reject this desired state.

---
# Alarm 3
trial_id: trial-00-0004/0002
## Categorization
Misoperation

*same as Alarm 2*

---
# Alarm 4
trial_id: trial-00-0005/0002
## Categorization
Misoperation

*same as Alarm 2*

---
# Alarm 5
trial_id: trial-00-0006/0003
## Categorization
Misoperation

*same as Alarm 2*

---
# Alarm 6
trial_id: trial-00-0007/0003
## Categorization
Misoperation

*same as Alarm 2*

---
# Alarm 7
trial_id: trial-00-0009/0005
## Categorization
Misoperation

*same as Alarm 2*

---
# Alarm 8
trial_id: trial-00-0010/0002
## Categorization
Misoperation

*same as Alarm 2*

---
# Alarm 9
trial_id: trial-00-0011/0002
## Categorization
Misoperation

*same as Alarm 2*

---
# Alarm 10
trial_id: trial-00-0012/0007
## Categorization
Misoperation

*same as Alarm 2*