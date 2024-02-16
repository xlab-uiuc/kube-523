### Info

netid: qhng2  
name: Quan Hao Ng  
operator: kubeblocks for mysql  

### Chosen CRD

The chosen CRD is called `apps.kubeblocks.io_clusters.yaml`. It is taken from the `kubeblocks/config/crd/bases` directory of the kubeblocks project repo. I chose this CRD because it is the one that is used when I first installed and setup a simple cluster using the kubeblocks operator for MySQL. 

In the setup process, I has to write a simply yaml file for this Custom Resource and then use `kubectl apply -f` to apply this Custom Resource.

### The fields of the CRD 

In the CRD, I focused on the fields defined in `spec.versions.schema.openAPIV3Schema.properties.spec.properties`.

I initially considered splitting by what fields are required, as a measurement of how much effort it takes for a minimal setup. However, the only required field is `terminationPolicy`, which describes what happens when the cluster terminates.

These are the categorisations I now use:

Cluster description
- `componentSpecs`
- `clusterVersionRef`
- `clusterDefinitionRef`

Policies
- `tolerations`
- `terminationPolicy`
- `monitor`
- `availabilityPolicy`

Pods distribution
- `tenancy`
- `affinity`

Storage related
- `storage`
- `shardingSpecs`
- `resources`
- `replicas`
- `backup`

Networking
- `services`
- `network`

### Complexity metric

For complexity, I decided to analyze the `spec.versions.schema.openAPIV3Schema.properties.spec.properties.componentSpecs` and `spec.versions.schema.openAPIV3Schema.properties.spec.properties.shardingSpecs` in greater detail because this is the core portion that dictates how we want the cluster to eventually look like. One of the 2 has to be defined. 

The complexity metric that I'm using is the greatest depth. I think this is the one that causes the most confusion for me when I was analyzing through the CRD. The depth of these 2 fields is also interesting because they seem to have a recursive structure that mirror the parent (Something like components of components). 

I realised I could not find a simple utility to get the depths of a YAML file so I wrote a short python utility to help me get the depth of a particular node I'm interested in.

This is the depth for the primary fields listed above:  
`[('affinity', 5), ('availabilityPolicy', 3), ('backup', 4), ('clusterDefinitionRef', 4), ('clusterVersionRef', 2), ('componentSpecs', 15), ('monitor', 6), ('network', 4), ('replicas', 2), ('resources', 6), ('services', 12), ('shardingSpecs', 17), ('storage', 6), ('tenancy', 3), ('terminationPolicy', 3), ('tolerations', 5)]`

As expected, the componentSpecs and shardingSpecs have the greatest depth.

This is the depth for `componentSpecs`:  
`[('description', 1), ('items', 14), ('maxItems', 1), ('minItems', 1), ('type', 1), ('x-kubernetes-validations', 3)]`

This is the depth for `shardingSpecs`:  
`[('description', 1), ('items', 16), ('maxItems', 1), ('minItems', 1), ('type', 1), ('x-kubernetes-list-map-keys', 2), ('x-kubernetes-list-type', 1)]`

For both: `items` is the subtree with the highest depth and is the one that seems to mirror the parent structure.