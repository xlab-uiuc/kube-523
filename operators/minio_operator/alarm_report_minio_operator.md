---
name: Alarm Inspection Report
about: An analysis report for the alarms produced by Acto

---
## Alarm 1 
### What happened
Acto changes the `kes` section of the Tenant. It set the `kes.replica` to `0`. The corresponding pods were crashed and acto detected it as an alarm. (trial-00-0000/0008)

### Root Cause
The reason is that once the `kes` section is turned on, the operator requires `kes.kesSecret` field. Acto did not provide that field. I think the block of source code resulting in the behavior is https://github.com/minio/operator/blob/master/pkg/apis/minio.min.io/v2/helper.go#L540 and https://github.com/minio/operator/blob/master/pkg/controller/kes.go#L184.


### Expected behavior?
I'd like to say it is a true alarm. Although this alarm was caused by misoperation (didn't provide `kes.kesSecret` field), the tenat pods crashed which makes it a true alarm. I think this can be easily fixed by modifying https://github.com/minio/operator/blob/master/pkg/apis/minio.min.io/v2/helper.go#L540 to check whether the required field is provided instead of just checking whether there is a `kes` section.


## Alarm 2
### What happened
Acto add a init container to the tenant with a invalid `httpheader` `name`. The pod failed to start and acto detected it as an alarm. (trial-00-0004/0001)

### Root Cause
Acto add an invalid init container. For MinIO Tenant, `initContainer` failures prevent Operator pods from starting.


### Expected behavior?
It's a misoperation. It is hard for operator to detect whether the init container is valid. What's more, MinIO allows users to add multiple init containers under the `Spec.InitContainers` field which makes it even harder.

## Alarm 3
### What happened
Acto deleted a label of metadata (`spec.serviceMetadata.consoleServiceLabels`). The operator failed to delete the corresponding label and acto detected it as an alarm. (trial-003-0007/0009)

### Root Cause
https://github.com/minio/operator/blob/master/pkg/controller/console.go#L69 and 
https://github.com/minio/operator/blob/master/pkg/controller/minio-services.go#L92.
The `checkConsoleSvc` method will update any changes of console service. It calls `minioSvcMatchesSpecification` function which checks the whether there are changes made for the console service. It iterate through the desire state and check whether there is a corrsponding item in the current state. Therefore if the current state contains all the items in the desire state and some extra items, it will still return `true` (there are no changes).


### Expected behavior?
It's a true alarm. Simply modifying the `minioSvcMatchesSpecification` function to return `false` if there are extra items in the current state will fix the problem.

## Alarm 4, 5, 6, 7, 8, 9, 10
### What happened
Same as Alarm 1. Acto changes some subfields of `kes` which caused the tenant pods to crash.
(trial-00-0001/0001, trial-00-0002/0001, trial-00-0003/0001, trial-03-0000/0002, trial-03-0001/0001, trial-03-0011/0004, trial-06-0000/0001)


