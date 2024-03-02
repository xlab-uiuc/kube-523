---
name: Combined Alarm Inspection Report
about: An analysis report for the alarms produced by Acto due to integer changes on ports `grpcPort`, `httpPort`, and `sqlPort`. and False Alarms

---

## 1)TestCases (3/27)

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

## 2)TestCases (6/27)

| Test Case Identifier                           | Affected Field | Misclassification      |
|------------------------------------------------|----------------|------------------------|
| `testrun-2024-02-21-22-04/trial-01-0000/0009`  | `grpcPort`     | Integer deletion       |
| `testrun-2024-02-21-22-04/trial-06-0005/0001`  | `httpPort`     | Integer deletion       |
| `testrun-2024-02-21-22-04/trial-11-0000/0009`  | `sqlPort`      | Integer deletion       |

## What happened

**Why did Acto raise these alarms?**  
Acto raised alarms for three test cases, each classified as an integer deletion for essential port configurations (`grpcPort`, `httpPort`, and `sqlPort`). However, upon inspection, it was determined that these alarms were misclassified. The actual mutation in these cases involved adding port values rather than deleting them. Despite the misclassification, the alarms were justified based on the reasons outlined in previous test cases involving integer changes.

**Misclassification Issue:**  
The test cases were incorrectly classified as integer deletions in the mutated YAML files, whereas the changes were similar to the previously discussed integer changes, indicating an addition of port values.

**Justification for Raising the Alarm:**  
Although misclassified, the rationale for raising the alarm remains valid as per the analysis provided in the earlier cases. The changes to port configurations, even if added and not deleted, could lead to system crashes due to improper validation and sanitization of port values.

## Root Cause

**Misclassification Analysis:**  
The primary issue here is not with the operator's behavior but with the classification mechanism used by Acto. The system erroneously identified changes in port configurations as deletions.

**Impact of Misclassification:**  
This misclassification could potentially lead to confusion in troubleshooting and addressing the root cause of the alarms. However, the underlying issue remains the same: the failure to validate and sanitize input values for the `grpcPort`, `httpPort`, and `sqlPort` configurations correctly.

## Expected behavior?

**Alarm Classification Correction:**  
Although the alarms were triggered for a valid reason, it is crucial to correct the classification mechanism within Acto to accurately reflect the nature of the mutations. This ensures clarity in understanding the alarms and aids in the precise diagnosis of issues.

**Reaffirmation of the Fix in Operator Code:**  
As previously recommended, the operator code must be updated to incorporate a validation step prior to applying changes to the `grpcPort`, `httpPort`, and `sqlPort` configurations. This includes checks for:

- **Port Availability:** Ensuring new port values do not conflict with allocated resources or system ports.
- **Port Validity:** Verifying the port values are within acceptable ranges and not used by other services.
- **Error Handling:** Applying a default port value or retaining the previous configuration if validation fails, accompanied by clear, actionable error messages.

**Conclusion:**  
This report reaffirms the necessity for the recommended fixes in the operator code to address the root cause of the alarms. Simultaneously, it highlights the need for Acto to improve its classification mechanism to prevent future instances of misclassification, thereby enhancing the system's stability and reliability.

---

## 3)TestCases (12/27)

| Test Case Identifier                          | Description                                   |
|-----------------------------------------------|-----------------------------------------------|
| `testrun-2024-02-21-22-04/trial-04-0000/0000` | No mutation, false alarm                      |
| `testrun-2024-02-21-22-04/trial-06-0000/0000` | No mutation, false alarm                      |
| `testrun-2024-02-21-22-04/trial-07-0004/0000` | No mutation, false alarm                      |
| `testrun-2024-02-21-22-04/trial-07-0006/0000` | No mutation, false alarm                      |
| `testrun-2024-02-21-22-04/trial-09-0003/0000` | No mutation, false alarm                      |
| `testrun-2024-02-21-22-04/trial-10-0000/0000` | No mutation, false alarm                      |

## What happened

**Why were these alarms wrongly classified?**  
Acto flagged these test cases as alarms without any actual configuration changes being applied. The mutations expected or indicated did not occur, and when the YAML files generated during these test cases were deployed in a sandboxed environment, they performed correctly, demonstrating that the system's deployment capabilities were intact.

**Observations from Acto's Reports:**  
Acto attributed the alarms to operational issues, as evidenced by the restart counts of the `cockroach-operator-manager` pods. However, these restarts could be attributed to factors unrelated to the current test cases, such as residuals from previous tests, configuration issues, or improper termination handling of previous test cases.

## Analysis

**Operational Issue Indication:**  
The restart counts suggest intermittent operational issues within Acto or the deployment system itself rather than problems with the test cases or the YAML configurations. This misclassification of alarms points to the necessity for a more refined diagnostic approach within Acto to differentiate between actual configuration issues and operational anomalies.

**Potential Causes for Misclassification:**  
- Residual effects from previous test runs that weren't adequately cleared or reset.
- Configuration issues within the Acto environment that led to false positives.
- Inadequate termination handling for test cases, causing overlapping or residual impacts on subsequent tests.

## Expected behavior?

**Improvements in Acto's Diagnostic Mechanism:**  
To prevent such misclassifications, Acto needs to enhance its diagnostic and monitoring mechanisms. This includes:

- **Clearing Residual States:** Ensuring that the environment is returned to a clean state after each test run to prevent carry-over effects.
- **Refined Monitoring:** Implementing more granular monitoring to accurately identify the root cause of restarts and differentiate between operational issues and actual configuration problems.
- **Enhanced Termination Handling:** Developing robust termination processes for test cases to ensure all components are correctly shutdown and reset before the next test begins.

**Conclusion:**  
While the alarms were triggered due to perceived operational issues, the analysis indicates that these were false alarms resulting from misclassifications by Acto. Corrective measures focusing on improving Acto's diagnostic capabilities and operational handling are recommended to mitigate such occurrences in the future, ensuring that alarms accurately reflect the state of the system and its configurations.

---
