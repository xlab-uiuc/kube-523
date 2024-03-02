---
name: Alarm Inspection Report
about: An analysis report for some alarms produced by Acto
netid: sgbhat3
operator: [bookkeeper-operator](https://github.com/pravega/bookkeeper-operator?tab=readme-ov-file)

---

## Summary

- Total True Alarms: 21
- Analyzed Alarms: 12

## JVM Related Mis-configurations

- `trial-04-0002/0001`
- `trial-04-0008/0001`
- `trial-04-0007/0004`

### What happened

Acto raised an alarm due to a state transition that led to an explicit system crash. During this transition, Acto attempted to modify or add a mis-configured string (`ACTOKEY`) to a subproperty of `jvmOptions` (e.g., `gcOpts` or `gcLoggingOpts`), resulting in the system crash.

### Root Cause

The `MakeBookieConfigMap` function, responsible for translating `jvmOptions` to a config map, lacks sanity checks to catch malformed options. The `reconcileConfigMap` function, invoked by the bookkeeper operator during reconciliation, updates the config map without checking the validity of the provided options. As a result, the JVM crashes when receiving a malformed option argument.

### Expected Behavior
This is a mis-operation where the operator is expected to detect and reject such mis-configured strings. To prevent such misoperations, it is crucial to enhance the `MakeBookieConfigMap` function with sanity checks. While this might involve JVM-specific checks, it is essential for long-term stability. Alternatively, if the JVM exposes a simple API to check configuration options, leveraging it would be a more sustainable approach.

## Modifications to Non-updateable Parameters

- `trial-01-0000/0004`
- `trial-01-0001/0001`
- `trial-01-0002/0001`
- `trial-01-0003/0001`
- `trial-01-0004/0003`
- `trial-02-0000/0001`
- `trial-02-0001/0001`
- `trial-04-0014/0001`
- `trial-05-0000/0001`

### What happened
Acto raised alarms during various state transitions that attempt to modify sub-properties within `initContainers` that have explicitly been labelled as non-updateable in the CRD

### Root Cause
The operator code is not written defensively, and does not cleanly reject modifications to non-updateable properties. 

### Expected Behavior
Do not blame users for misconfigurations. Ideally, given how operator developers know exactly which properties are not to be updated, it is their responsibility to write defensive code that handles these cases cleanly. 
Another argument one could make here is that these test-cases are not interesting enough for acto to test, and therefore acto could provide a way to exclude such properties when testing. 
