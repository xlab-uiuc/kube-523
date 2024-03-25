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

## Alarm 4
### What happened
There are two CR, one is the seed state, and one is the modified version of seed state (with `pool.annotations` modified). If we apply the modified version first, the statefulset will have an `Annotation` of `ACTOKEY: ""` and we are unable to delete this annotation by any changes in yaml file. However, if we apply the seed state and then apply the modlified version, the `ACTOKEY : ""` will not be added to the metadata of statefulset. (316c2b7fddfb4bcaeca7d9401bf249d3/0000)

### Root Cause
https://github.com/minio/operator/blob/master/pkg/controller/main-controller.go#L1211 Here, the operator create the `StatefulSet` with the `poolArgs` which adds the `Annotation` to the metadata of statefulset. However, at this loop https://github.com/minio/operator/blob/master/pkg/controller/main-controller.go#L1231C2-L1231C6, the operator tries to reconcile the `StatefulSet` to the updated version but didn't modify the `Annotation` field under the `StatefulSet`'s metadata.

### Expected behavior?
It's a true alarm. The operator should either modify the `Annotaion` during the updating or don't add the `Annotation` when creating the `StatefulSet`. The solution is to change either piece of code to make the operator consistent.

## Alarm 5
### What happened
ACTO applied a CR with invalid `CSR` which caused the operator stuck before creating the Pod and of course failed to recovered to the seed state. (17e42fb34bbdd5114585f32fab680b75)

### Root Cause
https://github.com/minio/operator/blob/master/pkg/controller/csr.go#L204 shows that the operator will keep retrying to fetch the generated certificate from the CSR for `timeout = 20 mins`.

### Expected behavior?
I think it is a misoperation. The operator requires a valid `CSR` for creating a Pod while ACTO provided an invalid one.


## Alarm 6
### What happened
The default value of `requestAutoCert` is `true` which enables TLS. ACTO set it to `false` and the operator updated the services but didn't delete the `tls` secret. However, the operator will not create the `tls` secret if `requestAutoCert` is set to `false` in the beginning which casued the alarm. (3f4243c3740822fbcb3e33a4bd77d853)

### Root Cause
https://github.com/minio/operator/blob/master/pkg/controller/main-controller.go#L710. This is the sync function. In this function, it will only create the `tls` secret if `requestAutoCert` is changed from `false` to `true`. However, it will not delete the `tls` secret if `requestAutoCert` is changed from `true` to `false`. 

### Expected behavior?
If the operator is able to delete the secret mechanically, then I think it is a true alarm. Modifying the `sync` function to delete the `tls` secret if `requestAutoCert` is changed from `true` to `false` will fix the problem.

## Alarm 7
### What happened
The operator failed to create a `service.metadata.labels` which caused the alarm. (6a6200f12a60c3fa8433a26e67f4882f)

### Root Cause
https://github.com/minio/operator/blob/master/pkg/resources/services/service.go#L90C1-L91C1. At this line, `internalLabels` are added to the `labels` only when `Spec.ServiceMetadata.ConsoleServiceLabels != nil`. And later, the variable `labels` is used to create service.

### Expected behavior?
It's a true alarm. The operator should add the `internalLabels` to the `labels` regardless of the `Spec.ServiceMetadata.ConsoleServiceLabels` is `nil` or not. To fix this bug, simply add a else statement. ***

## Alarm 8
### What happened
ACTO set `reclaimStorage` to `true` but the operator failed to add a label to the `pvc` which caused the alarm. (8b2c62e6ffef74d2966e64d34c6ccf08)

### Root Cause
https://github.com/minio/operator/blob/master/pkg/controller/main-controller.go#L1278. This block updates the statefulset. It only updates  `Spec.Template` and `Spec.UpdateStrategy` but it won't update other fields.

### Expected behavior?
It's a true alarm. The operator should update all the fields under the `StatefulSet`. To fix this bug, developers should modify the code to copy all the fields upder spec of expected state to the current state.

## Alarm 9
### What happened
ACTO add a subfield under `sideCars.containers` and the pod failed to start. (trial-00-0006/0005)

### Expected behavior?
It's a misoperation. `sideCars` defines a list of containers that the Operator attaches to each MinIO server pods in the `pool`. Providing an invalid container will cause the pod failed to start. 

## Alarm 10
### What happened
ACTO add a subfield under `externalCertSecret` and the pod failed to start. (trial-04-0000/0005)

### Expected behavior?
It's a misoperation. `externalCertSecret` defines a k8s secret containing the tls certificate. Providing this field enables `TLS` and the operator will copy the specified certificate to every MinIO pod in the tenant which will cause pods failed to start.


## Alarm 11
### What happened
ACTO add a value to the subfield under `topologySpreadConstraints` and the pod failed to start. (trial-04-0004/0001)

### Expected behavior?
It's a misoperation. `topologySpreadConstraints` specify one or more Kubernetes Topology Spread Constraints to apply to pods deployed in the MinIO pool. Providing an invalid value will cause the pod failed to start and it's hard for the operator to detect whether the `topologySpreadConstraint` is valid or not.


## Alarm 12
### What happened
ACTO deleted a user but the operator didn't delete an existing user. (trial-00-0014/0001)

### Root Cause
https://github.com/minio/operator/blob/798825dd0a9071875e89f0af321dc671a4e995f8/pkg/controller/main-controller.go#L1329. This block controls the user creation. It will only create the user once and after that, the operator will not modify users.

### Expected behavior?
I think it is a misoperation. The initial design of the operator is to create the minio `Users` once and after that it has no control over the `Users` 

## Alarm 13
### What happened
ACTO provided an invalid `PriorityClassName` and there is no corresponding `PriorityClass` created in the cluster which makes the pod crashes. (trial-01-0003/0001)

### Expected behavior?
It is a true alarm. The operator should check the whether there is `PriorityClass` related with `PriorityClassName` provided in the cluster and then update the statefulset and pod.

## Alarm 14
### What happened
ACTO provided an invalid `env` variable and the operator failed to deploy the `Tenant` resource under this invalid environment. (trial-01-0006/0008)

### Expected behavior?
It is a misoperation. It is hard for the operator to check whether the `env` variable is a valid environment or not.

## Alarm 15
### What happened
ACTO provided an invalid `Probe` to the operator and the operator failed to deploy the pods. (trial-03-0008/0001)

### Expected behavior?
It is a misoperation. The pod crashed due to the invalid `Probe` provided by ACTO and It is hard for the operator the check whether the `Probe` provided is valid or not.

## Alarm 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27
### What happened
Same as Alarm 1. Acto changes some subfields of `kes` which caused the tenant pods to crash.
(trial-00-0001/0001, trial-00-0002/0001, trial-00-0003/0001, trial-03-0000/0002, trial-03-0001/0001, trial-03-0011/0004, trial-03-0015/0001, trial-03-0016/0001, trial-03-0017/0001, trial-05-0000/0005, trial-06-0000/0001, trial-07-0000/0002)

## Alarm 28, 29, 30
### What happened
Same as Alarm 5. (3e9f8dc9f51f70593d2d66ee9587b0c5, 6de500572bf208eba78a850beeb2c143, a65765c4376fdf2ddaded577eab07132)

## Alarm 31, 32, 33
### What happened
Same as Alarm 7. (9327decb3d6490646a42ee94ae3a4c8c, a3f72c8ea289fac43f8e50ce25326625, aadcb34b4ede0602258a374cb87ceba8)

## Alarm 34, 35
### What happened
Same as Alarm 8. (eb5786a9b462d1f7155ee2f2b4baf150, trial-03-0012/0003)

## Alarm 36, 37
### What happened
Same as Alarm 3. (fed06192f9cd1a0331ef35652b5b6b0a, trial-00-0009/0002)

## Alarm 38, 39, 40, 41, 42, 43, 44, 45, 46
### What happened
Same as Alarm 2. (trial-00-0012/0005, trial-00-0013/0006, trial-02-0000/0001, trial-03-0004/0001, trial-03-0009/0001, trial-03-0005/0001, trial-03-0014/0001, trial-04-0007/0003, trial-04-0008/0001)

## Alarm  47, 48, 49, 50, 51, 52, 53, 54, 55
### What happened
Same as Alarm 9. (trial-00-0007/0003, trial-00-0008/0001, trial-00-0010/0001, trial-01-0000/0007, trial-01-0001/0001, trial-01-0002/0001, trial-01-0005/0001, trial-03-0002/0001, trial-03-0003/0001)

## Alarm  56, 57
### What happened
Same as Alarm 10. (trial-04-0001/0001, trial-04-0002/0001)

## Alarm  58, 59
### What happened
Same as Alarm 11. (trial-04-0005/0001, trial-04-0006/0001)