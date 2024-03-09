___

## Ingress Annotations Inconsistency
Alarms: `trial-00-0002/0002`, `trial-00-0007/0003`, `trial-00-0036/0005`, `trial-01-0001/0007`, `trial-01-0002/0003`, `trial-02-0000/0003`, `trial-03-0027/0010`, `trial-03-0028/0003`, `trial-03-0045/0009`, `trial-03-0068/0005`, `trial-03-0070/0009`, `trial-03-0071/0003`, `trial-04-0042/0003`, `trial-04-0043/0003`
- ### What happened
  > Why did Acto raise this alarm? What happened in the state transition? Why Acto’s oracles raised an alarm?
  
  Consistency oracle "Found no matching fields for input". In all of these test cases, Acto either changed or removed the annotation `spec.grafana.ingress.annotations` or `spec.server.grpc.ingress.annotations` but found no matching system state change.

- ### Root Cause
  > Why did the operator behave in this way? Please find the exact block in the operator source code resulting in the behavior.
  
  The following code is responsible for this behavior. [ArgoCD Operator Ingress Reconciliation](https://github.com/Gisaldjo/argocd-setup/blob/df6454b64ebe13a5390abf9690f39e0e87bcaa30/argocd-operator-0.8.0/controllers/argocd/ingress.go#L92-L101)
  
  The operator creates a new Ingress object from the CR and checks if that object already exists in the cluster. If it does, and the CR still wants to keep it enabled, it returns. 
  I believe this doesn't account for annotations because even though the Ingress Go object is created from the CR, it doesn't actually set the annotations in the Go object: [Ingress object creation](https://github.com/Gisaldjo/argocd-setup/blob/df6454b64ebe13a5390abf9690f39e0e87bcaa30/argocd-operator-0.8.0/controllers/argocd/ingress.go#L39-L65).
  
  The annotations are only added when the ingress object is first created in the cluster ([here](https://github.com/Gisaldjo/argocd-setup/blob/df6454b64ebe13a5390abf9690f39e0e87bcaa30/argocd-operator-0.8.0/controllers/argocd/ingress.go#L107-L117)) but that code block is not reached when the ingress object already exists in the cluster (even the CR wants to change the annotations).
  
  This behavior is replicated in several other ingress related functions for different properties (i.e. grpc, prometheus, etc.) which result in the other alarms mentioned in the title. [Code Pointer](https://github.com/Gisaldjo/argocd-setup/blob/df6454b64ebe13a5390abf9690f39e0e87bcaa30/argocd-operator-0.8.0/controllers/argocd/ingress.go#L67-L90)

- ### Expected behavior?
  > If it is a true alarm, how to fix it in the operator code? If it is a false alarm, how to fix it in Acto code?
  
  This is a true alarm because a change in the CR did not result in a corresponding system state change. The fix could be to compare the annotations of the existing Ingress object with the ones specified by the CR instead of returning immediately on an existence check.
___
