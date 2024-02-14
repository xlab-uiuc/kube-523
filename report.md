## Custom Resource Definition

### Kubernetes Basic Resources
`description`,`metadata`,`replicas`,`proxy`,`backup`,`pmm`
These fields specify the high-level deployment resources of the operator.

### Deployment Resources
`image`,`imagePullPolicy`,`imagePullSecrets`,`port`,`instance`,`Affinity`,`podAntiAffinity`,`customTLSSecret`,
`topologyKey`,`requiredDuringSchedulingIgnoredDuringExecution`,`openshift`,`tolerations`,`expose`,`extension`,`grpc`,`sidecars`,


These fields are more specific and related to the cluster. It defines how to deploy the operator.

### Volume/Data Related Resources
General : `dataSourceRef`,` dataSource`,`storage`,`restore`,`manual`,`repos`,`repoHost`,`restore`,`global`,`Configuration`,`dataVolumeClaimSpec`,`users`,`databaseInitSQL`,`volumeMounts`,
`

Since Percona-Postgres Operator will connect to database and need to have backup. It will have some fields related to these kinds of resources.
