## Info
Name : Sally Rong

Netid: chenyan7

## Custom Resource Definition

### Kubernetes Basic Resources
`description`,`metadata`,`replicas`,`proxy`,`backup`,`pmm`
These fields specify the high-level deployment resources of the operator.

### Deployment Resources
`image`,`imagePullPolicy`,`imagePullSecrets`,`port`,`instance`,`Affinity`,`podAntiAffinity`,`customTLSSecret`,
`topologyKey`,`requiredDuringSchedulingIgnoredDuringExecution`,`openshift`,`tolerations`,`expose`,`extension`,`grpc`,`sidecars`


These fields are more specific and related to the cluster. It defines how to deploy the operator.

### Volume/Data Related Resources
General : `dataSourceRef`,` dataSource`,`storage`,`restore`,`manual`,`repos`,`repoHost`,`restore`,`global`,`Configuration`,`dataVolumeClaimSpec`,`users`,`databaseInitSQL`,`volumeMounts`
Since Percona-Postgres Operator will connect to database and need to have backup. It will have some fields related to these kinds of resources.

## Complexity Metric
Standing on the point of a Database related operator, I may think how the system can effectively manage resources. I think the complexity comes from the automated process. I may investigate it from a **Powerful Database**'s pespective. 

1. Volume
   
Data volumn and PVC is of priority for a database.
`spec.volume.dataVolumeClaimSpec.{accessModes,resources}`, `spec.dataSource`,`spec.volumes` 

2. High Availability and scalability
   
Multiple replicas can contribute to high availablity. Also it allows instances up and down to adjust for workload requirements. 

`instances` in level 1 has 3 `replicas`. 

`pgBouncer` in level 2 has 3 `replicas`.  

Affinity and anti-affinity rules play a critical role in defining how pods are scheduled and distributed. 

`spec.repoHost.affinity`, `spec.affinity.podAffinity`, `spec.affinity.pod-antiAffinity`

3. Backup and Recovery
   
`spec.backups.pgbackrest` configures automated backups using pgBackRest. 

`spec.backups.pgbackrest.repos.schedules` specifies automative backup schedule. 

`spec.backups.pgbackrest.repos.volume` specifies storage. 

`spec.backups.pgbackrest.restore` specifies configuration for restoration.

4. Monitoring and Logging 

`spec.pmm.enabled` enables integration with Percona Monitoring and Management service.

5. Extension
   
A lot of options are open to enable users to host the operator on different platforms, along with different backup options. 

`openshift` for deploying with openshift.   

`spec.backups.pgbackrest.repos.s3`, `spec.backups.pgbackrest.repos.azure`,`spec.backups.pgbackrest.repos.gcs` are offered for backup on different clouds.   

`spec.backups.pgbackrest.configuration.secret` ensures safety access.

6. Safety
   
TLS configuration is required for secure communication.  

`sshConfigMap` `sshSecret` `secretKeyRef` ensures safety connection with pods. 

`spec.proxy.pgBouncer.customTLSSecret` to encrypt connection with pgBouncer. 

`spec.backups.pgbackrest.configuration.secret` ensures safety access to backup space`. 

`spec.pmm.secret` ensures safety access to monitor.
