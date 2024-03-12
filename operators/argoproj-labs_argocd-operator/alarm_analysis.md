___

## Ingress Annotations Inconsistency
Alarms: (9) `trial-00-0002/0002`, `trial-00-0007/0003`, `trial-01-0001/0007`, `trial-01-0002/0003`, `trial-02-0000/0003`, `trial-03-0027/0010`, `trial-03-0028/0003`, `trial-03-0071/0003`, `trial-04-0043/0003`
- ### What happened
  > Why did Acto raise this alarm? What happened in the state transition? Why Acto’s oracles raised an alarm?
  
  Consistency oracle "Found no matching fields for input". In all of these test cases, Acto either changed or removed the annotation `spec.grafana.ingress.annotations`, `spec.server.grpc.ingress.annotations` or `spec.prometheus.ingress.annotations` but found no matching system state change.

- ### Root Cause
  > Why did the operator behave in this way? Please find the exact block in the operator source code resulting in the behavior.
  
  The following code is responsible for this behavior. [ArgoCD Operator Ingress Reconciliation](https://github.com/Gisaldjo/argocd-setup/blob/df6454b64ebe13a5390abf9690f39e0e87bcaa30/argocd-operator-0.8.0/controllers/argocd/ingress.go#L92-L101)
  
  The operator creates a new Ingress object from the CR and checks if that object already exists in the cluster. If it does, and the CR still wants to keep it enabled, it returns. 
  I believe this doesn't account for annotations because even though the Ingress Go object is created from the CR, it doesn't actually set the annotations in the Go object: [Ingress object creation](https://github.com/Gisaldjo/argocd-setup/blob/df6454b64ebe13a5390abf9690f39e0e87bcaa30/argocd-operator-0.8.0/controllers/argocd/ingress.go#L39-L65).
  
  The annotations are only added when the ingress object is first created in the cluster ([here](https://github.com/Gisaldjo/argocd-setup/blob/df6454b64ebe13a5390abf9690f39e0e87bcaa30/argocd-operator-0.8.0/controllers/argocd/ingress.go#L107-L117)) but that code block is not reached when the ingress object already exists in the cluster (even if the CR wants to change the annotations).
  
  This behavior is replicated in several other ingress related functions for different properties (i.e. grpc, prometheus, etc.) which result in the other alarms mentioned in the title. [Code Pointer](https://github.com/Gisaldjo/argocd-setup/blob/df6454b64ebe13a5390abf9690f39e0e87bcaa30/argocd-operator-0.8.0/controllers/argocd/ingress.go#L67-L90)

- ### Expected behavior?
  > If it is a true alarm, how to fix it in the operator code? If it is a false alarm, how to fix it in Acto code?
  
  This is a true alarm because a change in the CR did not result in a corresponding system state change. The fix could be to compare the annotations of the existing cluster Ingress object with the ones specified by the CR instead of returning immediately on an existence check.
___
Alarms: (12) `trial-03-0012/0002`, `trial-00-0036/0005`, `trial-01-0004/0002`, `trial-01-0066/0004`, `trial-03-0021/0001`, `trial-03-0045/0009`, `trial-03-0068/0005`, `trial-03-0070/0009`, `trial-04-0024/0005`, `trial-04-0042/0003`, `trial-04-0048/0006`, `trial-04-0056/0004`
- ### What happened
  > Why did Acto raise this alarm? What happened in the state transition? Why Acto’s oracles raised an alarm?
  
  Consistency oracle "Found no matching fields for input". While still affecting the test cases for `ingress.annotations`, the issue in this case is due to a validation error when the operator tries to apply the new CR.

- ### Root Cause
  > Why did the operator behave in this way? Please find the exact block in the operator source code resulting in the behavior.
  
  Upon digging in the operator logs I found the following reconciler error for `trial-03-0012/0002`:
  ```
  2024-03-06T21:48:05Z	ERROR	Reconciler error	{"controller": "argocd", "controllerGroup": "argoproj.io", "controllerKind": "ArgoCD", "ArgoCD": {"name":"test-cluster","namespace":"argocd-operator-system"}, "namespace": "argocd-operator-system", "name": "test-cluster", "reconcileID": "4b76696c-7114-49f3-bfbe-3f26832a7263", "error": "Deployment.apps \"test-cluster-repo-server\" is invalid: [spec.template.spec.containers[1].image: Required value, spec.template.spec.containers[1].readinessProbe.httpGet.httpHeaders: Invalid value: \"INVALID_NAME\": a valid HTTP header must consist of alphanumeric characters or '-' (e.g. 'X-Header-Name', regex used for validation is '[-A-Za-z0-9]+')]"}
  ```
  
  Similar validation errors appear on the other tests listed in this section.
  
  This seems to be a similar situation to one previously discussed in class. The application of the new CR seemingly succeeds (as noted by the cli-output files), however, when the operator tried to process the new CR it throws a validation error. The end user is not aware that the change failed unless they manually confirm or check the operator logs. 

- ### Expected behavior?
  > If it is a true alarm, how to fix it in the operator code? If it is a false alarm, how to fix it in Acto code?
  
  This is a true alarm because a "successful" CR change should result in a system state change too. If there is a validation error, the user needs to be made aware at the moment when they apply the new CR. This could be fixed by creating a webhook that performs validation at the moment that the new CR is applied.
___

___

## Route Annotations Inconsistency
Alarms: (3) `trial-01-0070/0003`, `trial-03-0024/0005`, `trial-03-0025/0003`
- ### What happened
  > Why did Acto raise this alarm? What happened in the state transition? Why Acto’s oracles raised an alarm?
  
  Consistency oracle "Found no matching fields for input". Similar to `ingress.annotations` above, in all of these test cases, Acto either changed or removed the annotation `spec.grafana.route.annotations` but found no matching system state change. This applies for all other `*route.annotations` properties.

- ### Root Cause
  > Why did the operator behave in this way? Please find the exact block in the operator source code resulting in the behavior.
  
  The following code is responsible for this behavior. [ArgoCD Operator Route Reconciliation](https://github.com/Gisaldjo/argocd-setup/blob/df6454b64ebe13a5390abf9690f39e0e87bcaa30/argocd-operator-0.8.0/controllers/argocd/route.go#L98-L106)
  
  The operator creates a new Route object from the CR and checks if that object already exists in the cluster. If it does, and the CR still wants to keep it enabled, it returns right away. 
  I believe this doesn't account for annotations because even though the Route Go object is created from the CR, it doesn't actually set the annotations in the Go object: [Route object creation](https://github.com/Gisaldjo/argocd-setup/blob/df6454b64ebe13a5390abf9690f39e0e87bcaa30/argocd-operator-0.8.0/controllers/argocd/route.go#L60-L74).
  
  The annotations are only added after the route object is first created in the cluster ([here](https://github.com/Gisaldjo/argocd-setup/blob/df6454b64ebe13a5390abf9690f39e0e87bcaa30/argocd-operator-0.8.0/controllers/argocd/route.go#L112-L115)) but that code block is not reached when the route object already exists in the cluster (even if the CR wants to change the annotations).
  
  This behavior is replicated in several other route reconciliation related functions for different properties (i.e. server, prometheus, etc.) which result in the other alarms mentioned in the title. [Code Pointer](https://github.com/Gisaldjo/argocd-setup/blob/df6454b64ebe13a5390abf9690f39e0e87bcaa30/argocd-operator-0.8.0/controllers/argocd/route.go#L76-L95)

- ### Expected behavior?
  > If it is a true alarm, how to fix it in the operator code? If it is a false alarm, how to fix it in Acto code?
  
  This is a true alarm because a change in the CR did not result in a corresponding system state change. The fix could be to compare the annotations of the existing cluster Route object with the ones specified by the CR instead of returning immediately on an existence check.
___

___

## Validation Error
resources.limits alarms: (25) `trial-00-0003/0002`, `trial-00-0004/0001`, `trial-00-0042/0005`, `trial-00-0043/0002`, `trial-00-0059/0007`, `trial-01-0010/0008`, `trial-01-0011/0002`, `trial-01-0060/0006`, `trial-01-0061/0002`, `trial-02-0006/0001`, `trial-02-0007/0001`, `trial-02-0010/0006`, `trial-03-0006/0002`, `trial-03-0008/0001`, `trial-03-0009/0002`, `trial-03-0010/0002`, `trial-03-0033/0001`, `trial-03-0059/0001`, `trial-03-0060/0001`, `trial-03-0074/0009`, `trial-04-0004/0001`, `trial-04-0005/0001`, `trial-04-0007/0001`, `trial-04-0021/0006`, `trial-04-0022/0001`  

resources.requests alarms: (19) `trial-01-0007/0008`, `trial-01-0008/0001`, `trial-01-0014/0006`, `trial-01-0015/0001`, `trial-01-0040/0009`, `trial-01-0046/0004`, `trial-01-0053/0001`, `trial-01-0054/0001`, `trial-02-0003/0009`, `trial-02-0004/0002`, `trial-03-0013/0002`, `trial-03-0014/0001`, `trial-03-0047/0004`, `trial-03-0048/0002`, `trial-03-0049/0001`, `trial-03-0072/0002`, `trial-04-0002/0005`, `trial-04-0003/0001`, `trial-04-0055/0002`

resourceFieldRef.divisor: (14) `trial-01-0027/0005`, `trial-01-0028/0002`, `trial-01-0041/0004`, `trial-01-0042/0002`, `trial-01-0044/0007`, `trial-01-0045/0002`, `trial-03-0016/0003`, `trial-03-0017/0002`, `trial-03-0038/0008`, `trial-03-0039/0002`, `trial-03-0041/0002`, `trial-03-0042/0002`, `trial-04-0000/0003`, `trial-04-0001/0002`

route.labels: (3) `trial-00-0022/0002`, `trial-02-0015/0009`, `trial-03-0043/0009`

- ### What happened
  > Why did Acto raise this alarm? What happened in the state transition? Why Acto’s oracles raised an alarm?
  
  Consistency oracle "Found no matching fields for input". In all of these test cases, Acto either changed or added the property `*resources.limits`, `*resources.requests`, `*resourceFieldRef.divisor` but found no matching system state change.

- ### Root Cause
  > Why did the operator behave in this way? Please find the exact block in the operator source code resulting in the behavior.
  
  The property changes generated by Acto did not pass the validation checks. The most common one states that `ACTOKEY` is not a valid resource type. The cli output indicates that the CR was applied correctly but later the operator finds that the CR does not pass the validation checks.

- ### Expected behavior?
  > If it is a true alarm, how to fix it in the operator code? If it is a false alarm, how to fix it in Acto code?
  
  This is a true alarm because a "successful" CR change should result in a system state change too. While Acto should ideally generate correct types of values for the properties it tests, if there is a validation error, the user needs to be made aware at the moment when they apply the new CR. This could be fixed by creating a webhook that performs validation at the moment that the new CR is applied.
___
___

## Route Labels Inconsistency
route.labels: (3) `trial-01-0023/0007`, `trial-01-0024/0003`, `trial-01-0068/0007`

- ### What happened
  > Why did Acto raise this alarm? What happened in the state transition? Why Acto’s oracles raised an alarm?
  
  Consistency oracle "Found no matching fields for input". In all of these test cases, Acto either changed or removed the annotation `*route.labels` but found no matching system state change.

- ### Root Cause
  > Why did the operator behave in this way? Please find the exact block in the operator source code resulting in the behavior.
  
  The following code is responsible for this behavior. [ArgoCD Operator Route Reconciliation](https://github.com/Gisaldjo/argocd-setup/blob/df6454b64ebe13a5390abf9690f39e0e87bcaa30/argocd-operator-0.8.0/controllers/argocd/route.go#L98-L106)
  
  The operator creates a new Route object from the CR and checks if that object already exists in the cluster. If it does, and the CR still wants to keep it enabled, it returns right away. 
  I believe this doesn't account for labels because even though the Route Go object is created from the CR, it doesn't actually set the labels in the Go object: [Route object creation](https://github.com/Gisaldjo/argocd-setup/blob/df6454b64ebe13a5390abf9690f39e0e87bcaa30/argocd-operator-0.8.0/controllers/argocd/route.go#L60-L74).
  
  The labels are only added after the route object is first created in the cluster ([here](https://github.com/Gisaldjo/argocd-setup/blob/df6454b64ebe13a5390abf9690f39e0e87bcaa30/argocd-operator-0.8.0/controllers/argocd/route.go#L117-L124)) but that code block is not reached when the route object already exists in the cluster (even if the CR wants to change the labels).
  
  This behavior is replicated in several other route reconciliation related functions for different properties (i.e. server, prometheus, etc.) which result in the other alarms. [Code Pointer](https://github.com/Gisaldjo/argocd-setup/blob/df6454b64ebe13a5390abf9690f39e0e87bcaa30/argocd-operator-0.8.0/controllers/argocd/route.go#L76-L95)

- ### Expected behavior?
  > If it is a true alarm, how to fix it in the operator code? If it is a false alarm, how to fix it in Acto code?
  
  This is a true alarm because a change in the CR did not result in a corresponding system state change. The fix could be to compare the labels of the existing cluster Route object with the ones specified by the CR instead of returning immediately on an existence check.
___
___

## Ingress Tls Inconsistency
ingress.tls: (8) `trial-00-0058/0002`, `trial-01-0012/0006`, `trial-01-0037/0004`, `trial-01-0038/0003`, `trial-02-0012/0002`, `trial-03-0075/0003`, `trial-04-0058/0002`, `trial-04-0060/0003`

- ### What happened
  > Why did Acto raise this alarm? What happened in the state transition? Why Acto’s oracles raised an alarm?
  
  Consistency oracle "Found no matching fields for input". In all of these test cases, Acto either changed or removed the annotation `*ingress.tls` but found no matching system state change. This stems from the same issue as the `ingress.annotations` tests mentioned above.

- ### Root Cause
  > Why did the operator behave in this way? Please find the exact block in the operator source code resulting in the behavior.
  
  The following code is responsible for this behavior. [ArgoCD Operator Ingress Reconciliation](https://github.com/Gisaldjo/argocd-setup/blob/df6454b64ebe13a5390abf9690f39e0e87bcaa30/argocd-operator-0.8.0/controllers/argocd/ingress.go#L92-L101)
  
  The operator creates a new Ingress object from the CR and checks if that object already exists in the cluster. If it does, and the CR still wants to keep it enabled, it returns. 
  This doesn't account for labels because even though the Ingress Go object is created from the CR, it doesn't actually set the labels in the Go object: [Ingress object creation](https://github.com/Gisaldjo/argocd-setup/blob/df6454b64ebe13a5390abf9690f39e0e87bcaa30/argocd-operator-0.8.0/controllers/argocd/ingress.go#L39-L65).
  
  The CR labels are only added when the ingress object is first created in the cluster ([here](https://github.com/Gisaldjo/argocd-setup/blob/df6454b64ebe13a5390abf9690f39e0e87bcaa30/argocd-operator-0.8.0/controllers/argocd/ingress.go#L157-L160)) but that code block is not reached when the ingress object already exists in the cluster (even if the CR wants to change the tls options).
  
  This behavior is replicated in several other ingress related functions for different properties (i.e. grpc, prometheus, etc.) which result in the other alarms mentioned in the title. [Code Pointer](https://github.com/Gisaldjo/argocd-setup/blob/df6454b64ebe13a5390abf9690f39e0e87bcaa30/argocd-operator-0.8.0/controllers/argocd/ingress.go#L67-L90)

- ### Expected behavior?
  > If it is a true alarm, how to fix it in the operator code? If it is a false alarm, how to fix it in Acto code?
  
  This is a true alarm because a change in the CR did not result in a corresponding system state change. The fix could be to compare the labels of the existing cluster Route object with the ones specified by the CR instead of returning immediately on an existence check.
___
___

## Server extraCommandArgs crash loop
server.extraCommandArgs: (5) `trial-00-0017/0001`, `trial-00-0018/0002`, `trial-00-0019/0001`, `trial-04-0019/0002`, `trial-04-0020/0001`

- ### What happened
  > Why did Acto raise this alarm? What happened in the state transition? Why Acto’s oracles raised an alarm?
  
  The pods did not reach ready state due to crash looping. `"pod: test-cluster-server-574dddff8b-x4hfl container [argocd-server] restart_count [6]"`
  Both the crash and the health oracle were triggered.

- ### Root Cause
  > Why did the operator behave in this way? Please find the exact block in the operator source code resulting in the behavior.
  
  The `server.extraCommandArgs` property allows the user provide additional arguments to the `argocd-server` binary that is executed in these pods. However, the argument that was generated by Acto is not a valid `argocd-server` argument. i.e. > "Error: unknown command \"ACTOKEY\" for \"argocd-server\"", "Run 'argocd-server --help' for usage."

- ### Expected behavior?
  > If it is a true alarm, how to fix it in the operator code? If it is a false alarm, how to fix it in Acto code?
  
  This is a true alarm because a "successful" change in the CR did not result in a corresponding system state change. While the situation is a bit tricky since the operator needs to have knowledge of the commands and args supported by `argocd-server` which can easily go out of sync, it is possible to perform validation on the values passed in as extraCommandArgs. This validation could be done through a webhook as previously mentioned cases to provide the user with immediate information when they apply the invalid CR.
___
