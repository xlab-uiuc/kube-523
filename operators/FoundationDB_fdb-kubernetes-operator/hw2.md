# Analysis of the Foundation DB CRD
We analyze the 55 fields in `apps.foundationdb.org_foundationdbclusters.yaml`, and classify them in the following categories - 

### FoundationDB Specific
`automationOptions`, `version`, `useUnifiedImage`, `useExplicitListenAddress`, `storageClass`, `skip`, `services`, `replaceInstancesWhenResourcesChange`, `processes`, `processGroupsToRemoveWithoutExclusion`, `processGroupsToRemove`, `processGroupIDPrefix`, `processCounts`, `pendingRemovals`, `nextInstanceID`, `minimumUpTimeSecondsForBounce`, `logGroup`, `labels`, `lockOptions`, `instanceIDPrefix`, `instanceToRemoveWithoutExclusion`, `instancesToRemove`, `faultDomain`, `ignoreUpgradabilityChecks`, `databaseConfiguration`, `dataHall`, `configMap`, `configured`, `coordinatorSelection`, `customParameters`, `dataCenter`, `buggify`

### Kubernetes Specific or more General properties
`containers`, `volumes`, `volumeSize`, `volumeClaim`, `updatePodsByReplacement`, `storageServersPerPod`, `sideCarVersions`, `sideCarVersions`, `sidecarVariables`, `sidecarContainer`, `resources`, `podTemplate`, `podSecurityContext`, `podLabels`, `podTemplate`, `podSecurityContext`, `mainContainer`

### External Properties
While they are required by FoundationDB, so they are much closer to being FoundationDB specific, they are specifically required while interaction with external resources (internet, or even to other containers)
`trustedCAs`, `seedConnectionString`, `connectionString`, `routing`, `partialConnectionString`

### Deployment Specific
This overlaps with the previous three categories, which were exhaustive in themselves. These are the properties which are required only at the time of deployment, as opposed to during the entire time the cluster is running (or at specific points of time, but it could be anytime throughout the lifecycle of the cluster).
`version`, `seedConnectionString`, `configured`, `dataCenter`, `instanceIDPrefix`, `trustedCAs`, `labels`


# Complexity metric
A lot of the properties are labels or IDs, which are useful (but not interesting?) but do not add significantly to the complexity of the CRD. On the other hand, there are properties which have subproperties which are particularly interesting (such as `routing`, `containers`, `faultDomain`). Based on these observations, a possible choice of weights could be,
Labels: 1
Booleans: 2
ConnectionStrings/Commands: 3
Integers: 5
Properties (with subproperties): 7

A property with subproperties should ideally get the sum of all it's data types, but for the sake of simplicity, I have chosen a weight of 7 based on a cursory evaluation of all the properties. I attempted going into each of the subproperties and coming up with a better evaluating scheme, but it was taking too long. 

The complexity of the CRD can be calculated as the weighted average of all properties,
$$
\frac{1 \times 7 + 2 \times 8 + 3 \times 10 + 5 \times 2 + 7 \times 28}{55} = 4.70
$$