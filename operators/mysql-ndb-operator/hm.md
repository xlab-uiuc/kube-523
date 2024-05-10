# Info
- Name: Chun Chieh (Willy) Chang
- NetID: cc132

# Analyze CRD

## 1. Deployment and Configuration

### Core Deployment Properties

| Properties | Detail |
| --- | --- |
| replicas | Specifies the desired number of MariaDB instances for handling database requests, aiding in read scalability. |
| image | Defines the MariaDB container image and version to be deployed, ensuring consistency across instances.
args, command |
| args, command | Custom startup arguments and commands for the MariaDB container, allowing for tailored initialization procedures. |
| env, envFrom | Environment variables for the MariaDB container, sourced directly or from ConfigMaps/Secrets, to configure runtime behaviors and database settings. |
| imagePullPolicy, imagePullSecrets | Controls how the image is pulled (based on availability or always) and authentication for private registries. |
| initContainers, sidecarContainers | Pre-startup tasks and auxiliary services running alongside the main MariaDB container for extended functionality. |
| volumes, volumeMounts, volumneClaimTemplate | Storage configurations for data persistence, including dynamic provisioning and specific mount paths within the container. |

### Database Configuration

| Properties | Detail |
| --- | --- |
| database, bootstrapFrom | The database name to be created and the source (if any) for initial data loading, crucial for database setup and migrations. |
| myCnf | Custom configuration file (my.cnf) for MariaDB, allowing for detailed database tuning and behavior adjustments. |
| rootPasswordSecretKeyRef, passwordSecretKeyRef, username, rootEmptyPassword | Security and access configurations, including user credentials and root access controls. |

## **2. Networking and Services**

### Networking

| Properties | Detail |
| --- | --- |
| port | Network port configuration and Kubernetes Service definitions for database access, enabling connectivity and service discovery |
| service |  |
| primaryService |  |
| secondaryService |  |
| connection | Templates for configuring database connections, optimizing connectivity for different operational modes (primary, secondary). |
| primaryConnection |  |
| secondaryConnection |  |

### Service Discovery and Load Balancing

| Properties | Detail |
| --- | --- |
| serviceAccountName | Specifies the ServiceAccount under which the MariaDB pods run, aligning with Kubernetes RBAC for access control. |
| metrics | Configures exposure and scraping of database metrics, integrating with monitoring solutions like Prometheus. |

## 3. High Availability and Scaling

### HA and Replication

| Properties | Detail |
| --- | --- |
| galera | Configuration for high-availability setups using Galera Cluster or traditional replication, ensuring database uptime and data consistency. |
| replication |  |
| maxScale | Specifies integration with MaxScale for automatic failover and load balancing, enhancing availability and scalability. |
| maxScaleRef |  |

### Scaling and Resource Management

| Properties | Detail |
| --- | --- |
| resources | Resource requests and limits for CPU and memory, crucial for ensuring performance and efficient resource utilization. |
| ephemeralStorage | Option to use ephemeral storage, useful for temporary data processing or testing environments. |
| updateStrategy | Determines how updates to the MariaDB StatefulSet are applied, managing rollout strategies and minimizing downtime. |

## 4. Security and Compliance

### Scheduling Preferences

| Properties | Detail |
| --- | --- |
| affinity | Scheduling preferences and constraints, influencing pod placement based on node characteristics, priorities, and cluster topology for optimal distribution and resilience. |
| nodeSelector |  |
| priorityClassName |  |
| tolerations |  |
| topologySpreadConstraints |  |

### Operational Resilience

| Properties | Detail |
| --- | --- |
| podDisruptionBudget | Defines the minimum available pods during voluntary disruptions, safeguarding against downtime during maintenance. |
| livenessProbe | Health check configurations to assess container vitality and readiness, crucial for managing service availability and traffic routing. |
| readinessProbe |  |

## **6. Observability and Diagnostics**

### Monitoring and Metrics

| Properties | Detail |
| --- | --- |
| metrics | (Also under Networking and Services) Enables the collection and exposure of metrics for performance monitoring and alerting. |
| liveness Probe |  |
| readinessProbe |  |

## **7. State and Lifecycle**

| Properties | Detail |
| --- | --- |
| status | Reflects the current state of the MariaDB deployment, including operational metrics and health indicators, essential for observability and management. |
| updateStrategy |  |
| initContainers |  |
| sidecarContainers |  |

# CRD Field Analysis
## Estimating Configuration Depth (CD)
The depth is evident in properties like galera, replication, and metrics, which have nested configurations. Assuming the deepest nesting is around 3 levels deep (e.g., spec -> galera -> properties).

## Calculating CID
Let's calculate the CID with the assumed values for CI (10) and the maximum CD (3).

The Configuration Interdependence and Depth (CID) metric for the MariaDB CustomResourceDefinition (CRD) is calculated to be 13. This score reflects not just the number of configurable options within the CRD, but the complexity introduced by the interdependencies between configurations and the depth of the configuration hierarchy. A CID score of 13 suggests a moderately complex CRD, indicating that managing a MariaDB instance with this CRD involves understanding several interconnected properties and navigating through multiple levels of configuration details. 