## CRD Analysis

> NETID: tianyih5

I notices that there are five CRD yaml in the [GitHub Action Runner Controller CRDS folder](https://github.com/actions/actions-runner-controller/tree/master/charts/actions-runner-controller/crds). I briefly summarize each via reading the description in each CRD:

1. **HorizontalRunnerAutoscalers (`actions.summerwind.dev_horizontalrunnerautoscalers.yaml`)**: Defines a resource for automatically scaling the number of runners based on demand, similar to how Horizontal Pod Autoscalers work in Kubernetes. It allows the scaling of runner pods based on workload, such as the number of pending GitHub Actions jobs.
2. **RunnerDeployments (`actions.summerwind.dev_runnerdeployments.yaml`)**: Defines a resource for managing the deployment of a set of runners. It's similar to a Deployment resource in Kubernetes but tailored for GitHub Actions runners. It helps in maintaining a desired state and updating runners.
3. **RunnerReplicaSets (`actions.summerwind.dev_runnerreplicasets.yaml`)**: Defines a resource that acts similarly to a ReplicaSet in Kubernetes, ensuring that a specified number of runner replicas are running at any given time. It provides redundancy and scalability for runners.
4. **Runners (`actions.summerwind.dev_runners.yaml`)**: Defines individual runner instances. This resource allows for the management of individual GitHub Actions runners, including their registration, deregistration, and lifecycle management.
5. **RunnerSets (`actions.summerwind.dev_runnersets.yaml`)**: Defines a resource for managing sets of runners that are not necessarily identical but share a common configuration. This could be used for managing different types of runners within the same cluster, each optimized for different kinds of workloads or jobs.

To conduct an analysis, I will focus on the most intricate and critical Custom Resource Definition provided by the `actions.summerwind.dev` group, specifically `actions.summerwind.dev_runners.yaml`. I intend to categorize the fields within this CRD into three distinct groups: **Kubernetes Core Resources, Application-Specific Resources, and External Custom Resources**. This tripartite classification is beneficial because it delineates how Kubernetes interacts with different types of configurations.

**Kubernetes Core Resources** are handled directly by the Kubernetes system, which endeavors to reconcile the desired state defined by these resources with the actual state of the system. The modifications in these resources are typically designed to *have a minimal impact on the complexity of measuring an operator's intricacies, as they adhere to well-defined Kubernetes behaviors*.

**Application-Specific Resources**, on the other hand, are configurations that the application itself responds to. *Changes in these resources may introduce additional variables and complexities, due to their direct impact on the application's behavior*. This layer adds a significant dimension to the overall complexity as the system must account for the application's internal logic and potential state changes.

Lastly, **External Custom Resources** encapsulate the interaction with systems outside of Kubernetes, such as cloud services like Amazon S3. *These resources contribute an even greater level of uncertainty and complexity because they depend on the behavior and availability of external systems*, which are beyond the control of Kubernetes. This dependency introduces potential variables that can significantly affect both the system's stability and the predictability of its operations.

#### Kubernetes core resource

- **affinity**: Controls pod scheduling preferences.
- **autoMountServiceAccountToken**: A boolean that controls whether a service account token is automatically mounted into the pod's file system.
- **containers**: Container specifications for the pod.
- **dnsConfig**: Custom DNS settings for the pod.
- **dnsPolicy**: DNS policy for the pod.
- **hostAliases**: Hostname to IP mappings to add to a pod's `/etc/hosts` file.
- **imagePullPolicy**: Policy for pulling images.
- **imagePullSecrets**: Secrets for authenticating to a private registry.
- **initContainers**: Special containers that run before app containers.
- **labels**: Key-value pairs that are used to organize and select groups of objects.
- **nodeSelector**: Label queries to select nodes for pod scheduling.
- **priorityClassName**: Priority indication for pod scheduling.
- **resources**: Compute resource requirements (CPU, memory).
- **runtimeClassName**: Runtime class for selecting container runtime configuration.
- **securityContext**: Pod-level security attributes.
- **serviceAccountName**: Service account to attach to the pod.
- **sidecarContainers**: Additional containers that run alongside the main container.
- **terminationGracePeriodSeconds**: Duration in seconds to wait before terminating a pod.
- **tolerations**: Tolerations for node taints.
- **topologySpreadConstraints**: Rules for pod spreading across topology domains.
- **volumeMounts**: Mount paths for volumes inside containers.
- **volumes**: Volume specifications for data persistence.

#### Application-specific resource

- **containerMode**: Likely specifies how the runner operates within a container.
- **dockerEnabled**: Enable Docker within the runner environment.
- **dockerEnv**: Environment variables for Docker.
- **dockerMTU**: MTU setting for Docker networking.
- **dockerRegistryMirror**: Mirror configuration for Docker image registry.
- **dockerVarRunVolumeSizeLimit**: Size limit for the Docker `var/run` volume.
- **dockerVolumeMounts**: Mount paths for Docker-specific volumes.
- **dockerdContainerResources**: Resource limits for the Docker daemon container.
- **dockerdWithinRunnerContainer**: Specifies if the Docker daemon runs within the runner container.
- **enableServiceLabels**: Whether to enable Kubernetes service links.
- **enterprise**: Enterprise account for the runner to register.
- **env**: Environment variables for the runner.
- **envFrom**: Environment variables from other sources, such as ConfigMaps.
- **ephemeral**: If the runner is ephemeral.
- **ephemeralContainers**: Special temporary containers.
- **githubAPICredentialsFrom**: Source of GitHub API credentials.
- **group**: Runner group.
- **organization**: GitHub organization for the runner.
- **repository**: GitHub repository for the runner.
- **workDir**: Working directory for the runner.

#### External custom resource

- **volumeStorageMedium**: The storage medium of volumes, which could refer to an external storage class or provisioner.
- **workVolumeClaimTemplate**: template for the runner's working directory, which might use external storage resources.

### Complexity Metric

As previously discussed, Kubernetes Core Resources generally contribute less to the overall complexity of the system. In contrast, Application-Specific Resources and, most notably, External Custom Resources significantly add to the complexity. The latter's complexity stems from its dependency on the intricacies of "unknown" external systems (the term "unknown" is used here because the specifics of the external Custom Resources utilized by the system are not always transparent). Consequently, for quantifying complexity, we assign different weights to each category:
$$
C = 0.1\cdot C_k + 0.4 \cdot C_a + 0.5 \cdot C_e
$$
$C_k, C_a, C_e$ denote the complexity contributions from Kubernetes core resources, application-specific resources, and external custom resources, respectively. To assess the complexity of each component, we employ information entropy. Given that a YAML file structurally resembles a tree, we can calculate the complexity of each node as follows:
$$
C_{node} = C_{children} + H_{node}
$$

$$
H_{node} = -\sum{p(x)log(p(x))}
$$

For instance, a boolean, with two states, has an entropy of:
$$
H_{bool}= -((1/2)log₂(1/2) + (1/2)log₂(1/2)) = 1
$$
For an enum with 7 elements, the entropy is:
$$
H_{enum7} = -7 \cdot (1/7)log₂(1/7) ≈ 2.8074 bits.
$$
For data types with potentially infinite states, like strings, calculating entropy precisely is challenging. In such cases, we estimate:
$$
H_{unknown} = 1.5bit
$$
This estimation is based on the rationale that for many unknown data types (e.g., strings, arrays), errors are less likely because users often copy/paste values (such as secret keys or URLs). Thus, the state is essentially binary—correct or incorrect—similar to a boolean's entropy of 1 bit. To account for additional uncertainty and complexity, we slightly increase this value to 1.5 bits.

To traverse the YAML tree and apply the designated algorithm, recursion serves as a straightforward method. In my analysis of the YAML file, dividing the fields into three distinct categories proved to be exceedingly time-intensive. Consequently, I've decided to bypass the initial step of the algorithm. Moreover, for certain data types, I've opted for a simplified approach by assigning predetermined values rather than computing their entropies, as shown below:

```python
entropy_values = {
    "bool": 1.0,
    "enum": 2.5,
    "string": 1.5,
    "unknown": 1.5,
}
```

The entirety of the code is accessible in [complexity.py](./complexity.py). Utilizing my algorithm yielded a complexity score of `2029.5`. 

