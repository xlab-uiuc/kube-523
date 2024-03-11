# Lab1 10 results inspection
## Yuanzhuo Zhang
## Netid: yz124



### Alarm #1
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



### Alarm #8
In this round of test, pod crashed after applying this specific field value. Basicaaly, acto set the spec.router.bootstrapOptions value to an empty string.
```
  router:
    bootstrapOptions:
    - ''
```
I think this should be consider as a **true alarm**. Since the operator failed to check the input cr.yaml value correctness.
```
"trial_id": "trial-00-0011",
    "duration": 668.207487821579,
    "error": {
        "crash": {
            "message": "Pod test-cluster-router-5bfb5455b5-vm7ht crashed"
        },
        "health": {
            "message": "pod: test-cluster-router-5bfb5455b5-vm7ht container [router] restart_count [6]"
        },
        "operator_log": null,
        "consistency": null,
        "differential": null,
        "custom": null
    }
```

### Alarm #9
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
```
However, in mutated-002.yaml, it does not specify the **backupProfileName or backupProfile**, so this is a False alarm.


### Alarm #10-11
This is a true alarm.
These two alarms basically apply this cr
```
spec:
  backupSchedules:
  - backupProfile:
      dumpInstance:
        storage:
          azure:
            config: ''
            containerName: ajqjrpbyrs
```
and after inspecting the operator log.
The operator failed to apply change based on the random containerName. 

So the operator failed to inspect given cr correctness.


### Alarm #15-17
This are all true alarms, pod got crashed since acto apply invalid field values: **spec.router.options: ACTOKEY**
```
  router:
    instances: 1
    options:
    - ACTOKEY
```

### Alarm #22
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
    image: hdjelzdevb
    monitor: false
    ...
```

only if the spec.metrics.enable is True then operator will update the container properties, so this is a false alarm.

### Alarm #23
This is a True alarm.
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
image field is a random string, which cause the resource not found error. And the operator failed to check the cr value correctness before applying it.

### Alarm #24-25
These are true alarms, based on invalid input. 
```
"message": "Found no matching fields for input",
            "input_diff": {
                "prev": "ACTOKEY",
                "curr": "",
                "path": {
                    "path": [
                        "spec",
                        "backupSchedules",
                        0,
                        "backupProfile",
                        "dumpInstance",
                        "storage",
                        "ociObjectStorage",
                        "prefix"
                    ]
                }
            },
```

the prefix value has not been updated coorectly. However, the operator log

```
"message":"CronJob.batch \"test-cluster-pkmhnbsybn-cb\" is invalid: spec.schedule: Invalid value: \"cigxkfdfzw\": expected exactly 5 fields,
```

in the specif cr
```
spec:
  backupSchedules:
  - backupProfile:
      dumpInstance:
        storage:
          ociObjectStorage:
            bucketName: lahbamraed
            credentials: ttgcxogaqt
            prefix: ''
    enabled: true
    name: pkmhnbsybn
    schedule: cigxkfdfzw
```
the schedule is an invalid string and cause the update fails. So the operator failed to check **spec.backupSchedules.schedule** value correctness.

### Alarm #26

This is a false alarm.
```
"consistency": {
            "message": "Found no matching fields for input",
            "input_diff": {
                "prev": true,
                "curr": false,
                "path": {
                    "path": [
                        "spec",
                        "logs",
                        "error",
                        "collect"
                    ]
                }
            },
            "system_state_diff": null
        },
```
the spec.logs.error.collect has not been updated correctly.
However, in the cr
```
spec:
  initDB:
    dump:
      name: INVALID_NAME
      storage: {}
  instances: 3
  logs:
    error:
      collect: false
```
the spec.initDB.dump.storage is empty and the operator log raise the error that:

 mysqloperator.controller.api_utils.ApiSpecError: One of  must be set in spec.initDB.dump.storage

So acto did not set this property correctly and cause the false alarm.


### Alarm #31
This is a true alarm. The pod has been crashed,
```
"crash": {
            "message": "Pod test-cluster-router-74b6f8c9-hgblq crashed"
        },
        "health": {
            "message": "pod: test-cluster-router-74b6f8c9-hgblq container [router] restart_count [6]"
        },
```
since the spec.router.bootstrapOptions value is invalid(ACTOKEY). and the operator fail to check the correctness.
```
router:
    bootstrapOptions:
    - ACTOKEY
    instances: 1
```

### Alarm #33,36,37
same as alarm #23, a true alarm
```
metrics:
    enable: true
    image: abtteukdwr
    options:
    - ACTOKEY
```
invalid image string cause the exception happened and cause error state.

### Alarm #45,46,47
These are false alarms.


message='Found no matching fields for input' input_diff=Diff(prev=True, curr=False, path=["spec", "backupSchedules", 0, "deleteBackupData"]) system_state_diff=None


However, the operator log shows that: 

mysqloperator.controller.api_utils.ApiSpecError: One of backupProfileName or backupProfile must be set in spec.backupSchedules

but the acto's cr did not provide the required properties, and causing the operator error.
```
spec:
  backupSchedules:
  - deleteBackupData: false
    enabled: true
    name: cblvnegone
    schedule: ljfukxzxnm
```



### Alarm #54
This is a false alarm
The cli.log 
```
"stderr": "The InnoDBCluster \"test-cluster\" is invalid: spec.router.version: Invalid value: \"\": spec.router.version in body should match '^\\d+\\.\\d+\\.\\d+(-.+)?'"
```

but the cr specified version did not satisfy the regex expression and cause the error.
```
spec:
  instances: 3
  router:
    instances: 1
    version: ''
```

### Alarm #2-7
### Alarm #12-14
### Alarm #18-21
### Alarm #27-30
### Alarm #32,34,35,38-44
### Alarm #48-53

All of the following alarms are raised for the same reason as **Alarm #1**.

<ul>
<li>message='Found no matching fields for input' input_diff=Diff(prev='ACTOKEY', curr='', path=["spec", "backupProfiles", 0, "dumpInstance", "storage", "s3", "prefix"]) system_state_diff=None
<li>message='Found no matching fields for input' input_diff=Diff(prev='ACTOKEY', curr='', path=["spec", "backupProfiles", 0, "dumpInstance", "storage", "s3", "prefix"]) system_state_diff=None
<li>message='Found no matching fields for input' input_diff=Diff(prev='ACTOKEY', curr='', path=["spec", "initDB", "dump", "storage", "s3", "endpoint"]) system_state_diff=None
<li>message='Found no matching fields for input' input_diff=Diff(prev='ACTOKEY', curr='', path=["spec", "initDB", "dump", "storage", "s3", "endpoint"]) system_state_diff=None
<li>message='Found no matching fields for input' input_diff=Diff(prev='ACTOKEY', curr='', path=["spec", "backupProfiles", 0, "snapshot", "storage", "azure", "prefix"]) system_state_diff=None
<li>message='Found no matching fields for input' input_diff=Diff(prev='ACTOKEY', curr='', path=["spec", "initDB", "dump", "storage", "azure", "containerName"]) system_state_diff=None
<li>message='Found no matching fields for input' input_diff=Diff(prev='ACTOKEY', curr='', path=["spec", "initDB", "dump", "storage", "azure", "containerName"]) system_state_diff=None
<li>message='Found no matching fields for input' input_diff=Diff(prev='ACTOKEY', curr='', path=["spec", "initDB", "dump", "storage", "azure", "config"]) system_state_diff=None
<li>message='Found no matching fields for input' input_diff=Diff(prev='ACTOKEY', curr='', path=["spec", "keyring", "file", "fileName"]) system_state_diff=None
<li>message='Found no matching fields for input' input_diff=Diff(prev='ACTOKEY', curr='', path=["spec", "keyring", "file", "fileName"]) system_state_diff=None
<li>message='Found no matching fields for input' input_diff=Diff(prev='ACTOKEY', curr='', path=["spec", "backupProfiles", 0, "dumpInstance", "storage", "s3", "endpoint"]) system_state_diff=None
<li>message='Found no matching fields for input' input_diff=Diff(prev='ACTOKEY', curr='', path=["spec", "backupProfiles", 0, "dumpInstance", "storage", "s3", "endpoint"]) system_state_diff=None
<li>message='Found no matching fields for input' input_diff=Diff(prev='ACTOKEY', curr='', path=["spec", "backupProfiles", 0, "snapshot", "storage", "s3", "prefix"]) system_state_diff=None
<li>message='Found no matching fields for input' input_diff=Diff(prev='ACTOKEY', curr='', path=["spec", "backupProfiles", 0, "snapshot", "storage", "s3", "prefix"]) system_state_diff=None
<li>message='Found no matching fields for input' input_diff=Diff(prev='mypwds', curr='', path=["spec", "secretName"]) system_state_diff=None
<li>message='Found no matching fields for input' input_diff=Diff(prev='mypwds', curr='ACTOKEY', path=["spec", "secretName"]) system_state_diff=None
<li>message='Found no matching fields for input' input_diff=Diff(prev='mypwds', curr='', path=["spec", "secretName"]) system_state_diff=None
<li>message='Found no matching fields for input' input_diff=Diff(prev='ACTOKEY', curr='', path=["spec", "backupProfiles", 0, "snapshot", "storage", "azure", "prefix"]) system_state_diff=None
<li>message='Found no matching fields for input' input_diff=Diff(prev='ACTOKEY', curr='', path=["spec", "initDB", "dump", "storage", "ociObjectStorage", "bucketName"]) system_state_diff=None
<li>message='Found no matching fields for input' input_diff=Diff(prev='ACTOKEY', curr='', path=["spec", "initDB", "dump", "storage", "s3", "profile"]) system_state_diff=None
<li>message='Found no matching fields for input' input_diff=Diff(prev='ACTOKEY', curr='', path=["spec", "initDB", "dump", "storage", "s3", "profile"]) system_state_diff=None
<li>message='Found no matching fields for input' input_diff=Diff(prev=True, curr=False, path=["spec", "keyring", "file", "readOnly"]) system_state_diff=None
<li>message='Found no matching fields for input' input_diff=Diff(prev=True, curr=False, path=["spec", "keyring", "file", "readOnly"]) system_state_diff=None
<li>message='Found no matching fields for input' input_diff=Diff(prev='ACTOKEY', curr='', path=["spec", "initDB", "dump", "storage", "ociObjectStorage", "prefix"]) system_state_diff=None
<li>message='Found no matching fields for input' input_diff=Diff(prev='ACTOKEY', curr='', path=["spec", "initDB", "dump", "storage", "ociObjectStorage", "prefix"]) system_state_diff=None
<li>message='Found no matching fields for input' input_diff=Diff(prev='ACTOKEY', curr='', path=["spec", "backupProfiles", 0, "snapshot", "storage", "s3", "profile"]) system_state_diff=None
<li>message='Found no matching fields for input' input_diff=Diff(prev='ACTOKEY', curr='', path=["spec", "backupProfiles", 0, "snapshot", "storage", "s3", "profile"]) system_state_diff=None
<li>message='Found no matching fields for input' input_diff=Diff(prev='ACTOKEY', curr='', path=["spec", "initDB", "dump", "storage", "azure", "config"]) system_state_diff=None
<li>message='Found no matching fields for input' input_diff=Diff(prev='ACTOKEY', curr='', path=["spec", "mycnf"]) system_state_diff=None
<li>message='Found no matching fields for input' input_diff=Diff(prev='ACTOKEY', curr='', path=["spec", "mycnf"]) system_state_diff=None
<li>message='Found no matching fields for input' input_diff=Diff(prev='ACTOKEY', curr='', path=["spec", "keyring", "oci", "keySecret"]) system_state_diff=None
<li>message='Found no matching fields for input' input_diff=Diff(prev='ACTOKEY', curr='', path=["spec", "keyring", "oci", "keySecret"]) system_state_diff=None
<li>message='Found no matching fields for input' input_diff=Diff(prev='ACTOKEY', curr='', path=["spec", "backupProfiles", 0, "snapshot", "storage", "ociObjectStorage", "bucketName"]) system_state_diff=None
<li>message='Found no matching fields for input' input_diff=Diff(prev='ACTOKEY', curr='', path=["spec", "backupProfiles", 0, "snapshot", "storage", "ociObjectStorage", "bucketName"]) system_state_diff=None
</ul>





### Rest Alarm
The rest true alarms are raised by the differential oracle.
Basically can be classified into 3 catogories.

#### First kind of the alarm
This is basiclly first kind of alarm diff message
```
"values_changed": {
                "root['pod']['test-cluster-0']['metadata']['finalizers'][0]": {
                    "new_value": "kopf.zalando.org/KopfFinalizerMarker",
                    "old_value": "mysql.oracle.com/membership"
                },
                "root['pod']['test-cluster-1']['metadata']['finalizers'][0]": {
                    "new_value": "kopf.zalando.org/KopfFinalizerMarker",
                    "old_value": "mysql.oracle.com/membership"
                },
                "root['pod']['test-cluster-2']['metadata']['finalizers'][0]": {
                    "new_value": "kopf.zalando.org/KopfFinalizerMarker",
                    "old_value": "mysql.oracle.com/membership"
                },
                "root['deployment']['test-cluster-router']['spec']['replicas']": {
                    "new_value": 0,
                    "old_value": 1
                },
                "root['config_map']['test-cluster-componentconf']['data']['mysqld.my']": {
                    "new_value": "{\n    \"components\": \"file://component_keyring_oci\"\n}",
                    "old_value": "{}",
                    "diff": "--- \n+++ \n@@ -1 +1,3 @@\n-{}\n+{\n+    \"components\": \"file://component_keyring_oci\"\n+}"
                }
            },
```

After inspecting the operator log
```
 File "/usr/lib/mysqlsh/python-packages/mysqloperator/controller/innodbcluster/operator_cluster.py", line 932, in <dictcomp>
    patch = {field[0]: new for op, field, old, new in diff }
IndexError: tuple index out of range
```
The problematic code is a dictionary comprehension that tries to create a dictionary where keys are derived from the first element of the field tuple and values are the new values from the diff. The error suggests that at least one of the field tuples is empty.

And inspect the cr
```
spec:
  instances: 3
  podLabels: {}
```
podLabels is empty and cause the error. This is a True alarm since in the operator_cluster.py line932 fails to process the structure of the 'diff' object before processing.


#### Second kind of the alarm
Diff message:

```
"diff": {
            "values_changed": {
                "root['secret_number']": {
                    "new_value": 1,
                    "old_value": 4
                }
            }
        },
```

This diff message is created based upon various invalid input parameters:
here are the operator log for them:
```
1. 
mysqloperator.controller.api_utils.ApiSpecError: One of dumpInstance or snapshot must be set in a spec.backupSchedules.backupProfile.
2.
mysqloperator.controller.api_utils.ApiSpecError: Only one of ociObjectStorage, s3, azure must be set in spec.backupProfiles.gtutqdiwxt.snapshot.storage
3.
mysqloperator.controller.api_utils.ApiSpecError: One of  must be set in spec.backupProfiles.gtutqdiwxt.snapshot.storage
4.
HTTP response body: {"kind":"Status","apiVersion":"v1","metadata":{},"status":"Failure","message":"secrets \"ACTOKEY\" not found","reason":"NotFound","details":{"name":"ACTOKEY","kind":"secrets"},"code":404}
  raise ApiSpecError(f"Secret {secret_name} is missing")
mysqloperator.controller.api_utils.ApiSpecError: Secret ACTOKEY is missing
```
For the first three error, those are true alarm for invalid param checking in cr.

The last error is intriguing, which shows that it was raised for trying to find a kubernetes Secret named 'ACTOKEY' and fail to find that.

in the cr
```
 keyring:
    encryptedFile:
      fileName: ACTOKEY
      password: ACTOKEY
      readOnly: true
      storage: {}
```
the operator trying to fetch that secret but fail to find. So this is also a true alarm.

#### Third kind of the alarm
```
  "diff": {
            "values_changed": {
                "root['pod']['test-cluster-0']['metadata']['annotations']['kopf.zalando.org/last-handled-configuration']": {
                    "new_value": ...,{\"name\":\"kube-api-access-lvjg8\"...
                    "old_value": ...,{\"name\":\"kube-api-access-sz9n9\"...
                "root['pod']['test-cluster-0']['metadata']['annotations']['mysql.oracle.com/membership-info']": {
                    "new_value": "{\"memberId\": \"e500e7be-d204-11ee-847c-ce0acd628b0b\", \"lastTransitionTime\": \"2024-02-23T04:35:27Z\", \"lastProbeTime\": \"2024-02-23T04:35:27Z\", \"groupViewId\": \"17086629261895130:1\", \"status\": \"ONLINE\", \"version\": \"8.3.0\", \"role\": \"PRIMARY\", \"joinTime\": \"2024-02-23T04:35:27Z\"}",
                    "old_value": "{\"memberId\": \"04480154-d1e5-11ee-84e4-aaad66a5f925\", \"lastTransitionTime\": \"2024-02-23T00:47:05Z\", \"lastProbeTime\": \"2024-02-23T00:47:05Z\", \"groupViewId\": \"17086492238845076:1\", \"status\": \"ONLINE\", \"version\": \"8.3.0\", \"role\": \"PRIMARY\", \"joinTime\": \"2024-02-23T00:47:05Z\"}"
                },
```
Key Points from the Diff:
Last Handled Configuration Annotation Change:

Annotation Key: kopf.zalando.org/last-handled-configuration
The diff shows a change in the configuration of the pod, including volume definitions, init containers, and main containers configurations. The notable change is in the kube-api-access volume name (kube-api-access-lvjg8 to kube-api-access-sz9n9), indicating a potential refresh or update in the Kubernetes API access setup.
Membership Info Annotation Change:

Annotation Key: mysql.oracle.com/membership-info
This diff represents a change in the cluster membership information. Specifically, the memberId, lastTransitionTime, lastProbeTime, and groupViewId values have changed, indicating an update in the cluster's state or topology. This might reflect the addition, removal, or state change of a cluster member.