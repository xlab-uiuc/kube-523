### Kubernetes Core Resource
- additionalPorts
- clientSSLCertSecret
- disruptionBudget
- envs
- headlessServiceEnabled
- oneBrokerPerNode
- propagateLabels
- removeUnusedIngressResources
- rollingUpgradeConfig

### Application-Specific Resource
- alertManagerConfig
- brokerConfigGroups
- brokers
- clusterImage
- clusterMetricsReporterImage
- clusterWideConfig
- cruiseControlConfig
- envoyConfig
- ingressController
- listenersConfig
- monitoringConfig
- rackAwareness
- readOnlyConfig

### External Custom Resource
- istioControlPlane
- istioIngressConfig
- kubernetesClusterDomain
- zkAddresses
- zkPath

### Complexity Score

- **Depth**: Scale the weight of the depth to $$\text{Complexity} = 1.1^{\text{depth}}$$. Something at depth 2 is not twice as complex as something at depth 1, so this only starts punishing heavily at high depth values.

- **Type Multipliers**:
  - **Booleans**: 1x, simple toggles
  - **Integers**: 2x, number of items/replicas
  - **Strings**: 3x, can add lot of variability
  - **Lists/Dictionaries**: 4x, they can add nesting and more complexity

- **Exclude Descriptions**: Things like names, descriptions, and label properties shouldn't be included because they are used to make the document more human-readable.

**Formula**: Calculate the complexity of each type using $$\text{Complexity Score} = (1.1^{\text{depth}}) \times \text{Type Weight}$$, and sum for each property in the file.

The final result is calculated to be **358618.154**