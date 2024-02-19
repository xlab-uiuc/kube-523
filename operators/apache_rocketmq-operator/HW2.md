netid: cw110
operator: https://github.com/apache/rocketmq-operator

## CRD Analysis

The fields in the CRD can be categorized in the following groups:

Kubernetes core resource:
- affinity: the pod's scheduling preferences.
- allowRestart: defines whether allow pod restart.
- imagePullPolicy: defines how the image is pulled.
- imagePullSecrets: The secrets used to pull image from private registry.
- nodeSelector: must be true for the pod to fit on a node.
- priorityClassName: Priority indication for pod scheduling.
- resources: Compute resource requirements (CPU, memory).
- scalePodName: The name of pod where the metadata from
- securityContext: Pod-level security attributes.
- serviceAccountName: Service account to attach to the pod.
- tolerations: Pod's tolerations.

Application-specific resource:
- brokerImage: customized docker image repo of the RocketMQ broker
- containerSecurityContext: Container Security Context
- clusterMode: defines the way to be a broker cluster.
- env: defines custom env, e.g. BROKER_MEM
- nameServers: defines the name service list
- replicaPerGroup: each broker cluster's replica number
- size: size of broker cluster
- volumes: define the broker.conf

External custom resource:
- storageMode: StorageMode can be EmptyDir, HostPath, or external StorageClass
- volumeClaimTemplates: defines the StorageClass

## Complexity Measurement

The complexity can be measured by the type of each attribute in the CRD since the complex type(object, array) of the attribute indicates the complex configuration of the system, which leads to a complex system. 
The compute rule can be defined as follows:

- boolean: 1
- integer: 1
- string: 3
- object: the sum of complexity of the object
- array: the sum of complexity of each array item

Therefore, we can measure the complexity using the following pseudocode:

```
function calculate_complexity(propertites):
    complexity = 0;
    for propertiy in properties:
        if property.type == boolean:
            complexity += 1;
        if property.type == integer:
            complexity += 1;
        if property.type == string:
            complexity += 3;
        if property.type == object:
            complexity += calculate_complexity(property.properties);
        if property.type == array:
            complexity += calculate_complexity(property.items.properties);
    return complexity
```