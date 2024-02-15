## `metadata.yaml`
```
apiVersion: "v1"
kind: "HWSubmission"
metadata: 
    author_metadata:
        netid: "sgbhat3"
        health: ok
    operator: "bookkeeper-operator" 
    operator_name: "bookkeeperclusters.bookkeeper.pravega.io"
```

## CRD categorization
The bookkeeper operator has the following properties

`affinity`, `annotations`, `autorecovery`, `blockOwnerDeletions`, `envVars`, `headlessSvcNameSuffix`, `image`, `initContainers`, `jvmOptions`, `labels`,   `maxUnavailableBookkeeperReplicas`, `options`, `probes`, `replicas`, `resources`, `runAsPrivilegedUser`, `serviceAccountName`, `storage`, `tolerations`, `upgradeTimeout`, `version`, `zookeeperUri`

We can categorize these as follows

### Maintained Properties
These are fields, properties and/or constraints of the cluster that must be maintained throughout the cluster lifecyle by the operator. This can further be divided into general or bookkeeper specific parameters

#### Bookkeeper Specific 
These represent bookkeeper specific properties

`maxUnavailableBookkeeperReplicas`, `version`, `replicas`

#### General
These are generic properties that pertain to scheduling and resource allocation 

`affinity`, `tolerations`, `resources`

### Deployment Configurations
These are configurations that are provided at deployment time and mostly unchanged throughout the cluster lifecycle. These are further classified into bookkeeper specific (where the sub-fields or the field itself have bookkeeper specific terminology) and general properties

#### Bookkeeper Specific 
`zookeeperUri`, `upgradeTimeout`, `storage`, `headlessSvcNameSuffix`, `jvmOptions`, `options`, `autoRecovery`, `blockOwnerDeletions`

#### General
`annotations`, `labels`, `envVars`, `image`, `runAsPrivilegedUser`, `serviceAccountName`, `probes`, `initContainers`


## Complexity Metric
From a cursory reading of the CRD, it is evident that not each string type or integer type is not equivalent and hence assigning equal importance to these fields is not fair. For example, some strings represents execution commands that must be run whereas others are mere names and labels. Keeping this in mind, a coarse categorization of these types could be as follows, 

commands/env variable strings > integers > other strings > booleans

Assigning weights of 10, 5, 2, 1 respectively, we can computed a weighted average complexity score as

$$ \frac{10 \times \text{commands/env variables} + 3 \times \text{integers} + 2 \times \text{other strings} + 1 \times \text{booleans}}{\text{total number of parameters}} = \frac{ 10 \times 8  + 5 \times 174 + 2 \times 266  + 1 \times 16}{8 + 174 + 266 + 16} = 3.22$$

Of course, one can further split the integers up into classes of importance as some integer types represent important bookkeeper specific properties such as #replicas, whereas others represent less important parameters such as timeouts for various probes. Another improvement would be to take defaulted/compulsory parameters into account. I believe such a weighted metric with different classes of importance is the most interpretable metric.
