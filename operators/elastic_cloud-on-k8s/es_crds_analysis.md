# Elastic Search CRDS Analysis

## CRDS Category

**Pod Resources**

1. nodeSets: NodeSets allow specifying groups of Elasticsearch nodes sharing the same configuration and Pod templates.
2. podDisruptionBudget: PodDisruptionBudget provides access to the default Pod disruption budget for the Elasticsearch cluster.
3. image: Image is the Elasticsearch Docker image to deploy.

**Network**

1. remoteClusters: RemoteClusters enables you to establish uni-directional connections to a remote Elasticsearch cluster.
2. http: HTTP holds HTTP layer settings for Elasticsearch.
3. transport: Transport holds transport layer settings for Elasticsearch.

**Security**

1. auth: Auth contains user authentication and authorization security settings for Elasticsearch
2. secureSettings: SecureSettings is a list of references to Kubernetes secrets containing sensitive configuration options for Elasticsearch.

**Policies**

1. updateStrategy: UpdateStrategy specifies how updates to the cluster should be performed.
2. volumeClaimDeletePolicy: VolumeClaimDeletePolicy sets the policy for handling deletion of PersistentVolumeClaims for all NodeSets.
3. revisionHistoryLimit: RevisionHistoryLimit is the number of revisions to retain to allow rollback in the underlying StatefulSets.

**Monitors**

1. monitoring: Monitoring enables you to collect and ship log and monitoring data of this Elasticsearch cluster.

**Others**

1. serviceAccountName: ServiceAccountName is used to check access from the current resource to a resource.
2. version: Version of Elasticsearch.

## Complexity Metrics

Regard the CRD yaml file as a tree structure. Consider when the tree has a deeper width and height, the complexity of this tree will be higher. Another intuition is that when a node is far from the root of the tree, we think that the complexity of this node adds less to the complexity of the root node. This is well understood because the number of nodes in a tree may grow exponentially by level, so increasing number of nodes near the root will make this increase faster. 

Take these factors into consideration, we set a attenuation coefficient $\alpha$ for each layer, $0 < \alpha < 1$.  Denote the heigh of tree as $h$, and $n_i$ is the number of nodes for level $i$, then the complexity $C$ is defined as $C = \sum_i^h \alpha^i \cdot n_i$. For each node, we can apply this formula to calculate its complexity metric.
