# Acto Test Result Report for Prometheus-operator

## Alarm 1

### Test Case Info

Trial number: **trial-02-0008/0007** and **trial-02-0009/0003**

Health oracle reports that the number of ready replicas of the StatefulSet named `prometheus-test-cluster` is 2, while the desired replicas is 3. It also reports that `prometheus-test-cluster-1`` pod crashed.

### Root Cause

Prometheus CRD has a field called `PageTitle`, which is the prometheus web page title. We see in `delta-007.log` that the pageTitle became empty from `ACTOKEY`, which caused error in starting of the pod and hence resulted in `CrashLoopBackOff`` error

### Categorization

This is an example of a misconfiguration


## Alarm 2

### Test Case Info

Trial number: **trial-02-0005/0002**

When Acto adds tolerations `test-key=test-value:INVALID_EFFECT`, pod creation of `prometheus-test-cluster-1` failed

### Root Cause

`spec.tolerations[0].effect` must have been `NoExecute` when `tolerationSeconds` is set. But Acto used `INVALID_EFFECT` which is an unsupported effect and hence resulted in pod creation failure.

### Categorization

This is an example of a misconfiguration


## Alarm 3

### Test Case Info

Trial number: **trial-02-0003/0001**

When Acto changes the restart policy to `Always`, deleting pod `prometheus-k8s-0` failed

### Root Cause

Acto tried to delete a container which did not exist or was in the process of being recreated.

### Categorization

This can be classified as misconfiguration or a false alarm