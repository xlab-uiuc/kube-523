# Lab1 10 results inspection
## Yuanzhuo Zhang
## Netid: yz124


### First alarm
<p>
This alarm in results.csv is a True alarm.

In the generation-002-runtime.json file

```
 "oracle_result": {
        "crash": null,
        "health": null,
        "operator_log": null,
        "consistency": {
            "message": "Found no matching fields for input",
            "input_diff": {
                "prev": "INVALID_SERVICE_ACCOUNT_NAME",
                "curr": "default",
                "path": {
                    "path": [
                        "spec",
                        "serviceAccountName"
                    ]
                }
            },
            "system_state_diff": null
        },
        "differential": null,
        "custom": null
    },
```
This shows that Acto change **spec.serviceAccountName** from **INVALID_SERVICE_ACCOUNT_NAME** to **default**

To look up the operator source code about how this field being defined:


in /mysql-operator/mysqloperator/controller/cluster_api.py:
the code define an abstract class to initialize the value read from the cr.yaml file.
Specifically:
```
class AbstractServerSetSpec(abc.ABC):
    ...
    serviceAccountName: Optional[str] = None
    ...

    def _load(self, spec_root: dict, spec_specific: dict, where_specific: str) -> None:
    ...
     self.serviceAccountName = dget_str(spec_root, "serviceAccountName", "spec", default_value=f"{self.name}-sidecar-sa")
    ...
```
In order to check how **spec_root** object being created, I trace through the code and find that 



in /mysql-operator/mysqloperator/controller/innodbcluster/operator_cluster.py

```
@kopf.on.create(consts.GROUP, consts.VERSION,
                consts.INNODBCLUSTER_PLURAL)  # type: ignore
def on_innodbcluster_create(name: str, namespace: Optional[str], body: Body,
                            logger: Logger, **kwargs) -> None:
    ...
    cluster = InnoDBCluster(body)
    icspec = cluster.parsed_spec
    print("5. Cluster ServiceAccount")
            existing_sa = ignore_404(lambda: cluster.get_service_account(icspec))
            if not existing_sa:
                print("\tPreparing...")
                sa = cluster_objects.prepare_service_account(icspec)

```
the code use kpof.on.create to create the cluster 

in the original cr.yaml, when we want to update the specific field like **spec.tlsCASecretName**, there could be:
```
@kopf.on.field(consts.GROUP, consts.VERSION, consts.INNODBCLUSTER_PLURAL,
               field="spec.tlsCASecretName")  # type: ignore
def on_innodbcluster_field_tls_ca_secret_name(body: Body,
                                              logger: Logger, **kwargs):
    logger.info("on_innodbcluster_field_tls_ca_secret_name")
    on_sts_field_update(body, "spec.tlsCASecretName", logger)
```
However, there is no specific function to handle the **spec.serviceAccountName** field change request, so this is a True alarm.



</p>


### Second alarm
This alarm is a False alarm.
In the results.json
```
 "consistency": {
            "message": "Found no matching fields for input",
            "input_diff": {
                "prev": "InvalidSchedule",
                "curr": "1 * * * *",
                "path": {
                    "path": [
                        "spec",
                        "backupSchedules",
                        0,
                        "schedule"
                    ]
                }
            },
            "system_state_diff": null
        }
```

It shows that cluster fails to change the **spec.backupSchedules.schedule** field.

However, in the operator.log, it shows following error:
```
One of backupProfileName or backupProfile must be set in spec.backupSchedules
[2024-02-22 20:33:38,836] kopf.objects         [ERROR   ] Handler 'on_innodbcluster_field_backup_schedules/spec.backupSchedules' failed with an exception. Will retry.
Traceback (most recent call last):
  File "/usr/lib/mysqlsh/python-packages/kopf/_core/actions/execution.py", line 279, in execute_handler_once
    result = await invoke_handler(
  File "/usr/lib/mysqlsh/python-packages/kopf/_core/actions/execution.py", line 374, in invoke_handler
    result = await invocation.invoke(
  File "/usr/lib/mysqlsh/python-packages/kopf/_core/actions/invocation.py", line 139, in invoke
    await asyncio.shield(future)  # slightly expensive: creates tasks
  File "/usr/lib64/python3.9/concurrent/futures/thread.py", line 58, in run
    result = self.fn(*self.args, **self.kwargs)
    ...
```
However, in mutated-002.yaml, it does not specify the **backupProfileName or backupProfile**, so this is a False alarm.

### Third alarm
This is a False alarm.
in generatiion-001-runtime.json:
```
 "health": {
            "message": "statefulset: test-cluster replicas [3] ready_replicas [2]\npod: test-cluster-2"
        }
```
The health result shows that pos number is not consistent with the cr.
```
[2024-02-23 02:45:57,272] kopf.objects         [ERROR   ] Handler 'on_innodbcluster_field_metrics/spec.metrics' failed with an exception. Will retry.
Traceback (most recent call last):
...
kubernetes.client.exceptions.ApiException: (404)
Reason: Not Found
```
operator fail to find the required resource
in mutated-001.yaml
```
  metrics:
    enable: true
    image: srgabmrwyt
    monitor: true
```
image field is a random string, which cause the resource not found error.


### Fourth alarm
This is a False Alarm.
in the generatiion-002-runtime.json:
```
"oracle_result": {
        "crash": {
            "message": "Pod test-cluster-router-84c46fd95f-zjmvc crashed"
        },
        "health": {
            "message": "deployment: test-cluster-router replicas [1] ready_replicas [None], test-cluster-router condition [Available] status [False] message [Deployment does not have minimum availability.]\npod: test-cluster-router-84c46fd95f-zjmvc container [router] restart_count [6]"
        },
        "operator_log": null,
        "consistency": null,
        "differential": null,
        "custom": null
    },
```

However, in the mutated-002.yaml
```
  router:
    instances: 1
    options:
    - ACTOKEY
  secretName: mypwds
  tlsUseSelfSigned: true
```
in not-ready-pods-002.json:
```
{
    "test-cluster-router-84c46fd95f-zjmvc": [
        ...
    "[Entrypoint] Starting mysql-router.",
        "Error: invalid argument 'ACTOKEY'."
```
Basically, the wrong field value crash the pod.

### Fifth alarm
This is a False Alarm.
in the generatiion-003-runtime.json:
```
"consistency": {
            "message": "Found no matching fields for input",
            "input_diff": {
                "prev": "ACTOKEY",
                "curr": "",
                "path": {
                    "path": [
                        "spec",
                        "metrics",
                        "image"
                    ]
                }
            },
            "system_state_diff": null
        },
```

the **spec.metrics.image** files is not updated correctly
in the operator source code, I trace through it to find that:
```
def update_metrics(sts: api_client.V1StatefulSet,
                   service: api_client.V1Service,
                   cluster: InnoDBCluster, logger: Logger) -> None:
    spec = cluster.parsed_spec
    ...
    if spec.metrics and spec.metrics.enable:
        sts.spec.template.spec.containers += yaml.safe_load(spec.metrics_sidecar)
        if spec.metrics_volumes:
            sts.spec.template.spec.volumes += yaml.safe_load(spec.metrics_volumes)
``` 
and this is the mutated-003.yaml
```
metrics:
    enable: false
    image: ''
```

only if the spec.metrics.enable is True then operator will update the container properties, so this is a false alarm.