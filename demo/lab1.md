# Lab1 - Acto

In this lab, we will use Acto to test the operator that you picked.

You would need to have a working environment to run Acto, and the Acto repo cloned to your local disk. Since this lab would require a very long running time, we highly recommend you to use the CloudLab machine. We also provide an [Ansible Playbook](https://github.com/xlab-uiuc/acto/tree/main/scripts/ansible) to setup the environment automatically on CloudLab.

1. [Porting Your Operator to Acto by Writing `config.json`](#1-porting-your-operator-to-acto-by-writing-configjson)
2. [Running Acto](#2-running-acto)
3. [Inspecting Acto’s Test Results](#3-inspecting-actos-test-results)
4. [Deliverables](#deliverables)

## Deadlines
- Submit the test results without inspecting them -- next Friday (02/23)
  - Please finish running Acto and use the test result collection [script](https://github.com/xlab-uiuc/kube-523/blob/main/demo/lab1.md#31-gathering-test-results) to generate the `result.csv` file.
  - Create a PR to the repo to upload the `result.csv` file to the operator directory.
- Submit the inspection results of 10 reports -- next next Tuesday (02/27)
  - Please pick ten alarms from the `result.csv`, follow the instructions in the [deliverables](https://github.com/xlab-uiuc/kube-523/blob/main/demo/lab1.md#deliverables) to write a report analyzing the alarms.
  - Create a PR with your report.
- Submit all the inspection results  -- next next next Tuesday (03/05)
  - Create a PR with all the 100 alarm analysis.

## 1. Porting Your Operator to Acto by Writing `config.json`

Acto requires the following essential information to test an operator:

1. The way to deploy the operator
2. The operation interface

To provide these information to Acto, you would need to write a configuration file.

The configuration file has multiple sections. The first section is to teach Acto to deploy the operator. The configuration interface is abstracted as a sequence of steps.

### 1.1 Steps for Deploying the Operator

As you may have already experienced, deploying the operator involves multiple steps.

In the cass-operator’s case, it involves two main steps. The first step deploys the cert-manager which manages the certificates. We then need to wait for the cert-manager to completely finishes deploying. Afterwards, we then deploy the cass-operator itself, which includes all the resources needed by the operator (e.g. rbac, CRD, operator deployment).

The operator deploy for cass-operator is written in the following format, split into three steps:

```json
"deploy": {
    "steps": [
        {
            "apply": {
                "file": "data/cass-operator/init.yaml",
                "namespace": null
            }
        },
        {
            "wait": {
                "duration": 10
            }
        },
        {
            "apply": {
                "file": "data/cass-operator/bundle.yaml",
                "operator": true
            }
        }
    ]
}
```

**Added 02/20**
In case your operator uses helm to deploy, please check out the `helm template` command to export the helm chart into YAML files:
https://helm.sh/docs/helm/helm_template/

```
helm template --output-dir './yaml' ...
```

### 1.2 Providing the Name of the CRD to be Tested

You would also need to provide the full name of the CRD to be tested (Acto only supports to test one CRD at a time).

```
{
  "crd_name": "**cassandradatacenters.cassandra.datastax.com**"
}
```

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  annotations:
    cert-manager.io/inject-ca-from: cass-operator/cass-operator-serving-cert
    controller-gen.kubebuilder.io/version: v0.7.0
  name: **cassandradatacenters.cassandra.datastax.com**
spec:
```

P.S. Check if your CRD is complete. Check if the schema defined in the CRD is opaque. Some operator developers choose to define the CRD opaquely, using the `x-kubernetes-preserve-unknown-fields: true` keyword in the schema. 

### 1.3 Providing a Seed CR

Provide a sample CR which will be used by Acto as the seed. This can be any valid CR, usually operator repos contain multiple sample CRs. Specify this through the `seed_custom_resource` property in the configuration.

**Added 02/20**
Please specify the `metadata.name` as `test-cluster` in the CR YAML

For example, cass-operator provides a list of sample CRs in their [repo](https://github.com/k8ssandra/cass-operator/tree/master/config/samples)

Copy one CR into the port directory, and specify the path of the copied CR in the `seed_custom_resource` property.

### 1.4 [optional] Extending Acto

Please refer to [https://github.com/xlab-uiuc/acto/blob/main/docs/test_generator.md](https://github.com/xlab-uiuc/acto/blob/main/docs/test_generator.md)

## 2. Running Acto

After you have the config, Acto is ready to roll!

Hold your horses, before launching a full test campaign, you may want to validate that your operator config. You wouldn’t want to run Acto for overnight and realize the operator was crashing all the time.

### 2.1 Run the “learn” phase of Acto

Acto has a pre-flight “learn” phase, which does some first-time information collection and checking.

To only run the “learn” phase:

```bash
python3 -m acto --config CONFIG --learn
```

It does the following tasks:

1. Create a “learn” Kubernetes cluster
2. Parse the Operator deployment steps to figure out which namespace the operator is deployed to.
3. Deploy the Operator according to the Deploy section of the operator config.
4. Get the CRD from the Kubernetes cluster, which should be created at step 3.
5. Deploy the CR.
6. Inspect the Kubernetes nodes to get the list of images being used. These images will be preloaded to the Kubernetes nodes during the test campaign to avoid the Docker’s pull rate limit.
7. Conduct pre-flight checking to make sure the system state is at least healthy. It also checks whether the pods have “IfNotPresent” as the ImagePullPolicy.

At the end, it produces a `context.json` file in the same directory with the seed CR. The context.json file will be used for the actual test campaign, so that the above “learn” phase is only one-time effort.

### 2.2 Kick-off Acto’s Test Campaign

Now you are all set to test your operator!

Run the following command to invoke Acto test your operator:

```bash
python3 -m acto --config CONFIG [--num-workers NUM_WORKERS]
```

Note the `--num-workers` optional flag. Acto is able to parallelize the tests “almost” perfectly, so it is recommended to run Acto with as many workers as your machine can support. However, the bottleneck of Acto is a bit counter-intuitive: it is bottlenecked by your disk’s I/O bandwidth. It is because each worker runs a separate Kubernetes cluster, and they are constantly loading large images from disk into docker’s fs. When you have 4 Kubernetes clusters at the same time, the total image size is at least 40GB not counting the application’s images.

If you are running Acto on your personal computer with an SSD, it is recommended to run Acto with 2-4 workers. You would also need to configure some system parameters according to: [https://github.com/xlab-uiuc/acto/blob/main/docs/FAQ.md](https://github.com/xlab-uiuc/acto/blob/main/docs/FAQ.md)

If you are running Acto on CloudLab, it is recommended to setup the machine using our provided [Ansible Playbook](https://github.com/xlab-uiuc/acto/tree/main/scripts/ansible). Since the machines on CloudLab would have much larger memory, we can play to the trick to mount the docker into a tmpfs(memory-based file system) to remove the image loading bottleneck. Of course now the bottleneck becomes the size of the main memory.

You can experiment a bit to see how much space one Kubernetes cluster takes up. Usually for a machine with 200GB memory, 8 workers is a safe choice.

If you specify too many workers, the machine could be overloaded, and you may be even not able to ssh into it. You can restart the machine by clicking the power cycle button on the CloudLab website in this case.

There are many other useful options when running Acto, the full list is:

```bash
--config CONFIG, -c CONFIG
                        Operator porting config path
--num-workers NUM_WORKERS
                        Number of concurrent workers to run Acto with
--workdir WORKDIR_PATH
                        Working directory
```

### 2.3 Babysitting Acto

Acto is still a research prototype, and it is very likely to have problems when being applied to different operators.

Since the testing usually takes hours, it is recommended to monitor Acto’s log at the beginning to make sure it does not crash (to avoid the bad experience where you waited for one day to check the result, and realize that Acto crashed after 10 mins after starting). When Acto crashes, it dumps the stacktrace with all the local variable values. Acto prints log at `CRTICIAL` level when it crashes. To check whether Acto has crashed, simply do a keyword search of `CRITICAL` in Acto’s log.

Acto writes the test log to `{WORKDIR}/test.log` . If you did not specify the `--workdir` command line argument, `{WORKDIR}` would be `testrun-{TIMESTAMP` in the current directory.

We do not expect you to debug Acto if it crashes. Please raise a question on Piazza or open an issue on Acto’s github and we will fix it ASAP.

## 3. Inspecting Acto’s Test Results

### Regenerating the result.csv

Previously there was a required manual step to specify the regular expressions for the non-deterministic property paths. If not done correctly, Acto’s differential oracle would produce many false alarms.

Fortunately, Acto is splitted into multple phases, and they can be rerun independently. To rerun the differential oracle for the post processing steps, you just need to run the following command to remove the previous results and regenerate the new results:

```bash
git pull

rm -f testrun-{}/post_diff_test/compare-results-*
python3 -m acto.post_process.post_diff_test --config OPERATOR_CONFIG --num-workers 32 --testrun-dir TESTRUN_DIR --workdir {TESTRUN_DIR}/post_diff_test/ --checkonly
```

This command would take 5 mins to 30 mins to run.

Afterwards, you can run the result collection script to generate the result.csv again.

### Interpreting the Result

Acto will first generate a test plan using the operator's CRD and the semantic information. The test plan is serialized at `testrun-cass/testplan.json` (You don't need to manually inspect the `testplan.json`, it is just to give an overview of the tests going to be run). Note that Acto does not run the tests according to the order in the `testplan.json`, the tests are run in a random order at runtime.

Acto then constructs the number of Kubernetes clusters according to the `--num-workers` argument, and start to run tests. Tests are run in parallel in separate Kubernetes clusters. Under the `testrun-cass` directory, Acto creates directories `trial-XX-YYYY`. `XX` corresponds to the worker ID, i.e. `XX` ranges from `0` to `3` if there are 4 workers. `YYYY` starts from `0000`, and Acto increments `YYYY` every time it has to restart the cluster. This means every step inside the same `trial-xx-yyyy` directory runs in the same instance of Kubernetes cluster.

Acto takes steps to run the testcases over the previous CR one by one. One testcase is to change the current CR to provide the next CR to be applied. Acto starts from the sample CR given from the operator configuration.

At each step, Acto applies a test case over the existing CR to produce the next CR. It then uses `kubectl apply` to apply the CR in a declarative fashion. Acto waits for the operator to reconcile the system to match the CR, then collects a "snapshot" of the system state at this point of time. It then runs a collection of oracles(checkers) over the snapshot to detect bugs. Acto serializes the "snapshot" and the runtime result from the oracles in the `trial-xx-yyyy` directory.

The schema of the "snapshot" is defined at [acto/snapshot.py](https://github.com/xlab-uiuc/acto/blob/main/acto/snapshot.py). It is serialized to the following files:

- `mutated-*.yaml`: These files are the inputs Acto submitted to Kubernetes to run the state transitions. Concretely, Acto first applies `mutated-0.yaml`, and wait for the system to converge, and then applies `mutated-1.yaml`, and so on.
- `cli-output-*.log` and `operator-*.log`: These two files contain the command line result and operator log after submitting the input.
- `system-state-*.json`: After each step submitting `mutated-*.yaml`, Acto collects the system state and store it as `system-state-*.json`. This file contains the serialized state objects from Kubernetes.
- `events-*.log`: This file contains the list of detailed Kubernetes event objects happened after each step.
- `not-ready-pod-*.log`: Acto collects the log from pods which are in `unready` state. This information is helpful for debugging the reason the pod crashed or is unhealthy.

The schema of the runtime result is defined at [acto/result.py](https://github.com/xlab-uiuc/acto/blob/main/acto/result.py). It is serialized to the `generation-XXX-runtime.json` files. It mainly includes the result from the oracles:

- `crash`: if any container crashed or not
- `health`: if any StatefulSet or Deployment is unhealthy, by comparing the ready replicas in status and desired replicas in spec
- `consistency`: consistency oracle, checking if the desired system state matches the actual system state
- `operator_log`: if the log indicates invalid input
- `custom`: result of custom oracles, defined by users
- `differential`: if the recovery step is successful after the error state

### Post Differetial Test Results
In the `result.csv`, you may find that some alarms’ `testcase` column is a hash. This means that this alarm is from a postrun differential test, and the alarm is raised by the differential oracle. These alarms are raised by comparing two system states produced by the same CR input. To inspect these alarms, you can take a look at the `Differential` column of the alarm to figure out which two steps are being compared.

The raw alarm file can be found in the `post_diff_test` directory under the `testrun-{}` directory. You should be able to find a list of files named as `compare-results-{HASH}.json` . The `compare-results-{HASH}.json` file contains a list of alarms corresponding to the same input (the hash is in fact computed based on the input CR). Inside each alarm, you can find the computed delta between the two system states, along with the two system states being compared.

The difference in the system states on the same CR is usually caused by different previous existing system state. You can diagnose the alarms by figuring out what is the previous system state, and how does the operator behave differently under different existing system state.

### 3.1 Gathering Test Results

After Acto finishes all the tests, you can use the following script to collect all the test results into a .csv file and inspect them in Google Sheet.

Please upload the csv file as the first part of the lab1, and analyze the results based on it.

**Added 02/17**
Run the following command in the Acto repo, it will produce a csv file under the testrun directory(workdir).
```
python3 -m acto.post_process.collect_test_result --config OPERATOR_CONFIG --testrun-dir TESTRUN_DIR
```

Usage documentation:
```
usage: collect_test_result.py [-h] --config CONFIG --testrun-dir TESTRUN_DIR

Collect all test results into a CSV file for analysis.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the operator config file
  --testrun-dir TESTRUN_DIR
                        Path to the testrun dir which contains the testing result
```

### Example of A True Alarm

Let’s take a look at one example how we analyzed one alarm produced by Acto and found the https://github.com/k8ssandra/cass-operator/issues/330

You can find the trial which produced the result [here](lab1/alarm_examples/true_alarm/), and the alarm is raise inside [this file](lab1/alarm_examples/true_alarm/generation-002-runtime.json)

Inside the [generation-002-runtime.json](lab1/alarm_examples/true_alarm/generation-002-runtime.json), you can find the following the alarm:

```json
"consistency": {
    "message": "Found no matching fields for input",
    "input_diff": {
        "prev": "ACTOKEY",
        "curr": "NotPresent",
        "path": {
            "path": [
                "spec",
                "additionalServiceConfig",
                "seedService",
                "additionalLabels",
                "ACTOKEY"
            ]
        }
    },
    "system_state_diff": null
},
```

This shows that the alarm is raised by Acto’s consistency oracle. In the alarm description, you can see three fields: `message`, `input_diff`, and `system_state_diff`. In the `input_diff`, it shows the following information:

- In this step, Acto changed the property of path `spec.additionalServiceConfig.seedService.additionalLabels.ACTOKEY` from `ACTOKEY` to `NotPresent`. This basically means that Acto deleted the `spec.additionalServiceConfig.seedService.additionalLabels.ACTOKEY` from the CR.
- Acto checked through the system state change, and could not find a matching change.

To look deeper into this alarm, we can check the [delta-002.log](lab1/alarm_examples/true_alarm/delta-002.log) file. The `delta-002.log` file contains two sections: `INPUT DELTA` and `SYSTEM DELTA`. In the `INPUT DELTA`, you can see the diff from the `mutated-001.yaml` to `mutated-002.yaml`. In the `SYSTEM DELTA`, you can see the diff from `system-state-001.json` to `system-state-002.json`. You can also view the `mutated-*.yaml` and `system-state-*.json` files directly to see the full CR or full states.

These files tell us the behavior of the operator when reacting to the CR transition. Next, we need to understand why the operator behaves in this way. We need to look into the operator source code to understand the behavior.

The operator codebase may be large, so we need to pinpoint the subset of the operator source code which is related to the `spec.additionalServiceConfig.seedService.additionalLabels.ACTOKEY` property.

We first need to find the places in the source code which reference the property. 

- We can find the type definition for the property at [https://github.com/k8ssandra/cass-operator/blob/9d320dd1960706adb092541a2dc30f186a76338e/apis/cassandra/v1beta1/cassandradatacenter_types.go#L342.](https://github.com/k8ssandra/cass-operator/blob/53c637c22f0d5f1e2f4c09156591a47f7919e0b5/apis/cassandra/v1beta1/cassandradatacenter_types.go#L299)
- Then we trace through the code to find the uses of this field, and eventually we arrive at this line: [https://github.com/k8ssandra/cass-operator/blob/9d320dd1960706adb092541a2dc30f186a76338e/pkg/reconciliation/construct_service.go#L91.](https://github.com/k8ssandra/cass-operator/blob/53c637c22f0d5f1e2f4c09156591a47f7919e0b5/pkg/reconciliation/construct_service.go#L90)
- Tracing backward to see how the returned values are used, we arrive at this line: https://github.com/k8ssandra/cass-operator/blob/53c637c22f0d5f1e2f4c09156591a47f7919e0b5/pkg/reconciliation/reconcile_services.go#L59.
- We can see that the operator always merge the existing annotations with the annotations specified in the CR. This “merge” behavior causes the old annotations to be never deleted: https://github.com/k8ssandra/cass-operator/blob/53c637c22f0d5f1e2f4c09156591a47f7919e0b5/pkg/reconciliation/reconcile_services.go#L104.

### Example of Misoperation

Let’s take a look at one example of an alarm caused by a misoperation vulnerability in the tidb-operator. A misoperation vulnerability means that the operator failed to reject an erroneous desired state, and caused the system to be in an error state.

You can look at the example alarm [here](lab1/alarm_examples/misoperation/)

Inside the [alarm file](lab1/alarm_examples/misoperation/generation-001-runtime.json), you can find the following alarm message:

```json
"health": {
    "message": "statefulset: test-cluster-tidb replicas [3] ready_replicas [2]"
},
```

This shows the alarm is raised by the health oracle, which checks if the Kubernetes resources have desired number of replicas. In this alarm, Acto found that the StatefulSet object named `test-cluster-tidb` only has two ready replicas, whereas the desired number of replicas is three.

To find out what happened, we can take a look at the [delta-001.log](lab1/alarm_examples/misoperation/delta-001.log) . It tells us that from the previous step, Acto added an Affinity rule to the tidb’s CR. And in the system state, the tidb-2 pod is recreated with the Affinity rule.

Next, we need to figure out why the tidb-2 pod is recreated, but cannot be scheduled. After taking a look at the [events-001.json](lab1/alarm_examples/misoperation/events-001.json) file, we can find an error event issued by the `Pod` with the message: `"0/4 nodes are available: 1 node(s) had untolerated taint {node-role.kubernetes.io/control-plane: }, 3 node(s) didn't match Pod's node affinity/selector. preemption: 0/4 nodes are available: 4 Preemption is not helpful for scheduling.."` indicating that the new Pod cannot be properly scheduled to nodes.

The root cause is because the desired Affinity specified in the TiDB CR cannot be satisfied in the current cluster state. The tidb-operator fails to reject the erroneous desired state, updates the TiDB cluster with the unsatisfiable Affinity rule, causing the cluster to lose one replica.

### Example of False Alarm

Acto’s oracles are not sound, meaning that Acto may report an alarm, but the operator’s behavior is correct. [Here](lab1/alarm_examples/false_alarm/) is an example of false alarms produced by Acto.

Looking at the [generation-002-runtime.json](lab1/alarm_examples/false_alarm/generation-002-runtime.json), you can find the following error message from the consistency oracle: 

```json
"oracle_result": {
    "crash": null,
    "health": null,
    "operator_log": null,
    "consistency": {
        "message": "Found no matching fields for input",
        "input_diff": {
            "prev": "1Gi",
            "curr": "2Gi",
            "path": {
                "path": [
                    "spec",
                    "ephemeral",
                    "emptydirvolumesource",
                    "sizeLimit"
                ]
            }
        },
        "system_state_diff": null
    },
    "differential": null,
    "custom": null
},
```

This indicates that Acto expects a corresponding system state change for the input delta of path `spec.ephemeral.emptydirvolumesource.sizeLimit`. To understand the operator’s behavior, we trace through the operator source. We can see that the property has a control-flow dependency on another property: https://github.com/pravega/zookeeper-operator/blob/9fc6151757018cd99acd7b73c24870dce24ba3d5/pkg/zk/generators.go#L48C1-L52C54. And in the CR generated by Acto, the property `spec.storageType` is set to `persistent` instead of `ephemeral`.

This alarm is thus a false alarm. The operator’s behavior is correct. It did not update the system state because the storageType is not set to `ephemeral`. Acto raised this alarm because it fails to recognize the control-flow dependency among the properties `spec.ephemeral.emptydirvolumesource.sizeLimit` and `spec.storageType`.

## Deliverables

1. Please finish testing the operator using Acto
2. There would be many alarms produced by Acto, and you are expected to inspect at least 100 alarms, and write a report for them. You can use the report template here: https://github.com/xlab-uiuc/kube-523/blob/main/demo/lab1/alarm_report_template.md
    1. For each alarm, you need to determine if this is a True alarm or False alarm
    2. Please describe what is the CR change introduced by Acto in this alarm, and what is the operator’s behavior
    3. If it is a false alarm, please explain why do you think it is a false alarm. Is Acto’s correctness assumption broken?
    4. If it is a true alarm, please explain what exactly the operator did wrong. Please try to trace through the operator’s source code to find out the root cause.
    5. If it is a true alarm, please work with us to send a bug report to the developers to help them improve their reliability!
3. Note that 100 seems a big number, but you will notice that many alarms are duplicated. There is an open question on how to improve the usability of Acto by grouping the duplicated alarms. Can you think of some features which can be used to determine if two alarms are duplicated?
4. Note: this lab would require you to deeply understand the operator’s behavior, and almost certainly you would need to inspect the operator’s source code to understand the behavior. It would be a hard, but rewarding process!
