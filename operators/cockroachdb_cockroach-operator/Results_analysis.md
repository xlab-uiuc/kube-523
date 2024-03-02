---
name: Combined Alarm Inspection Report - Integer Change on Ports
about: An analysis report for the alarms produced by Acto due to integer changes on ports `grpcPort`, `httpPort`, and `sqlPort`.

---

## TestCases (3/27)

| Test Case Identifier                           | Affected Field | Test Case Description |
|------------------------------------------------|----------------|-----------------------|
| `testrun-2024-02-21-22-04/trial-01-0001/0001`  | `grpcPort`     | Integer change        |
| `testrun-2024-02-21-22-04/trial-06-0006/0001`  | `httpPort`     | Integer change        |
| `testrun-2024-02-21-22-04/trial-11-0001/0001`  | `sqlPort`      | Integer change        |


## What happened

**Why did Acto raise these alarms?**  
Acto triggered alarms for three distinct test cases involving changes to the integer values of essential port configurations (`grpcPort`, `httpPort`, and `sqlPort`). Each modification threatened the system's communication infrastructure and, by extension, its operational integrity. 
These changes let to the pods to crash.




**What happened in the state transition?**  
The alteration in integer values for these ports led to configurations that were either invalid or caused resource conflicts. This, in turn, prevented the server from initiating correctly, affecting its ability to handle gRPC, HTTP, and SQL communications effectively.
Pods crashed as they did not have permission to connect to these ports and the Service failed to init leading to the crash.

**Why Acto’s oracles raised an alarm?**  
The oracles identified the changes as significant threats to the node's functionality. Given that these ports are foundational for the operation of the system, any misconfiguration could result in severe operational failures, justifying the alarms.

## Root Cause

**Why did the operator behave in this way?**  
The root cause of the issue is the operator's failure to validate and sanitize the input values for the `grpcPort`, `httpPort`, and `sqlPort` configurations. When changes were applied to these fields, the operator did not verify the new port values' availability or appropriateness, leading to problematic configurations being set.

Pods crashed as they did not have permission to connect to these ports and the Service failed to init leading to the crash. Failure to check for the port correctness on the oparator's side lead to this issue, as they are expected to reject incorrect ports.

**Exact block in the operator source code:**  
The issue originates from the `cockroach-operator/pkg/resource/discovery_service.go` file, within the build function responsible for configuring service specifications:
```go
service.Spec = corev1.ServiceSpec{
    ClusterIP: "None",
    PublishNotReadyAddresses: true,
    Ports: []corev1.ServicePort{
        {Name: "grpc", Port: *b.Cluster.Spec().GRPCPort},
        {Name: "http", Port: *b.Cluster.Spec().HTTPPort},
        {Name: "sql", Port: *b.Cluster.Spec().SQLPort}
    }
}
```
This snippet demonstrates the direct assignment of port values from the cluster specification to the service ports without conducting necessary pre-assignment checks for port validity and availability.

## Expected behavior?

This is a **TRUE** Alarm as the Pods actually crashed during the runs.

**Fix in the operator code:**  
To resolve this issue, the operator code must be updated to incorporate a validation step prior to applying changes to the `grpcPort`, `httpPort`, and `sqlPort` configurations. The validation should ensure that:

- **Port Availability:** The new port values do not conflict with already allocated resources or reserved system ports. This could entail querying Kubernetes or the underlying system to check port availability.

- **Port Validity:** The port values are within a permissible range and not commonly used by other critical services or protocols, minimizing the risk of conflicts.

- **Error Handling:** In case the validation fails, the operator should either keep the previous functional configuration or apply a default, known-good port value. It should also provide clear and actionable error messages that describe the reason for the failure and suggest possible fixes.

The implementation of these changes would enhance the build function with a robust mechanism for port validation, potentially involving additional utility functions or external API interactions to ascertain the status of the specified ports. By ensuring the new port values are validated for both availability and suitability, the operator can prevent configuration-related errors, thereby improving the system's stability and reliability.

---

## TestCases (6/27)

| Test Case Identifier                           | Affected Field | Test Case Description |
|------------------------------------------------|----------------|-----------------------|
| `testrun-2024-02-21-22-04/trial-01-0001/0001`  | `grpcPort`     | Integer change        |
| `testrun-2024-02-21-22-04/trial-06-0006/0001`  | `httpPort`     | Integer change        |
| `testrun-2024-02-21-22-04/trial-11-0001/0001`  | `sqlPort`      | Integer change        |

