# Lab1 - Acto

In this lab, we will use Acto to test the operator that you picked.

You would need to have a working environment to run Acto, and the Acto repo cloned to your local disk. Since this lab would require a very long running time, we highly recommend you to use the CloudLab machine. We also provide an [Ansible Playbook](https://github.com/xlab-uiuc/acto/tree/main/scripts/ansible) to setup the environment automatically on CloudLab.

1. [Porting Your Operator to Acto by Writing `config.json`](#1-porting-your-operator-to-acto-by-writing-configjson)
2. [Running Acto](#2-running-acto)
3. [Inspecting Acto’s Test Results](#3-inspecting-actos-test-results)
4. [Deliverables](#deliverables)

## Deadlines
- Submit the test results without inspecting them -- next Thursday (02/22)
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

### 3.1 Gathering Test Results

After Acto finishes all the tests, you can use the following script to collect all the test results into a .xlsx file and inspect them in Google Sheet.

**We will release the collection script soon.**

## Deliverables

1. Please finish testing the operator using Acto
2. There would be many alarms produced by Acto, and you are expected to inspect at least 100 alarms, and write a report for them.
    1. For each alarm, you need to determine if this is a True alarm or False alarm
    2. Please describe what is the CR change introduced by Acto in this alarm, and what is the operator’s behavior
    3. If it is a false alarm, please explain why do you think it is a false alarm. Is Acto’s correctness assumption broken?
    4. If it is a true alarm, please explain what exactly the operator did wrong. Please try to trace through the operator’s source code to find out the root cause.
    5. If it is a true alarm, please work with us to send a bug report to the developers to help them improve their reliability!
3. Note that 100 seems a big number, but you will notice that many alarms are duplicated. There is an open question on how to improve the usability of Acto by grouping the duplicated alarms. Can you think of some features which can be used to determine if two alarms are duplicated?
4. Note: this lab would require you to deeply understand the operator’s behavior, and almost certainly you would need to inspect the operator’s source code to understand the behavior. It would be a hard, but rewarding process!
