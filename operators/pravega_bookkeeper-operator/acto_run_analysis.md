---
name: Alarm Inspection Report
about: An analysis report for some alarms produced by Acto
netid: sgbhat3
operator: [bookkeeper-operator](https://github.com/pravega/bookkeeper-operator?tab=readme-ov-file)

---

## Summary:

### Consistency Alarms
- Total True Alarms: 21
- Analyzed Alarms: 21

### Differential Alarms
- Total True Alarms: 38
- Analyzed Alarms: 27

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

## Toleration Related Mis-configuration

- `trial-01-0006/0001`
- `trial-01-0007/0002`
- `trial-01-0008/0001`

### What happened
Acto raised these alarms when performing some state transitions where some of the sub-properties under the `tolerations` property such as `effect` and `operator` are changed to `ACTOKEY` which causes one of the replicas to crash. 

### Root Cause
The CRD for bookkeeper specifies that `effect` and `operator` sub-properties need to be of a specific type. For example, for the `effet` property, the CRD specifies that 
```
Effect indicates the taint effect to match. Empty means match all taint effects. When specified, allowed values are NoSchedule, PreferNoSchedule and NoExecute.
```
The string `ACTOKEY` clearly does not match any of the acceptable patterns causing the system to crash. 

### Expected Behaviour
The operator must ideally perform the required sanity checks on the strings provided if they have to be of a specific type and reject the CR as a mis-configuration. 


## Empty/Zero initialization for `readinessProbe` 
- `trial-00-0000/0002`
- `trial-00-0001/0001`
- `trial-04-0004/0001`

## What happened

In these testcases, acto changes some/all of the sub-properties in `readinessProbe` to 0. This causes one of the replicas to show as not ready, thereby triggering an alarm. 

## Root Cause
According to the CRD for the bookkeeper operator, the `readinessProbe` property has a bunch of sub-properties specifying various threshold and time related values such as 
`failureThreshold`, `initialDelaySeconds`, `periodSeconds`, `successThreshold` and `timeoutSeconds`. These have some default values specified within the operator. However, these default values are assigned only when the specification in the CR specifies a value of `nil`. This can be seen in the `Probes.withDefaults` function. So setting them to an empty array (`{}`) **does not** set default values, and instead sets it to 0 for all the integer values within the structure. While typically kubernetes probes have some non-zero minimum values (see [here](https://arc.net/l/quote/qjytsihm)), in this case, bookkeeper specifies a minimum value 0 for all fields. So setting probes to 0 is not a misconfiguration. But how exactly the probe should behave when some values are 0 is not clear. For example, if the `periodSeconds` sub-field is 0 as in this case, the frequency of the readiness probe makes no semantic sense. Similarly, setting `failureThreshold` (which is the number of probe failures after which kubernetes considers the overall check as failed i.e. the container is not ready) to 0 also makes no sense.

## Expected Behaviour
Ideally, 0 default values makes no sense for some of these fields, therefore the condition in the function should be changed to set the default values even if any of the fields are 0. This way the readiness probe will not malfunction and the pod shows up as ready. 

```
func (s *Probes) withDefaults() (changed bool) {
	if s.ReadinessProbe == nil {
		changed = true
		s.ReadinessProbe = &Probe{}
		s.ReadinessProbe.InitialDelaySeconds = DefaultReadinessProbeInitialDelaySeconds
		s.ReadinessProbe.PeriodSeconds = DefaultReadinessProbePeriodSeconds
		s.ReadinessProbe.FailureThreshold = DefaultReadinessProbeFailureThreshold
		s.ReadinessProbe.SuccessThreshold = DefaultReadinessProbeSuccessThreshold
		s.ReadinessProbe.TimeoutSeconds = DefaultReadinessProbeTimeoutSeconds
	}

    ...
    return changed;
}
```

## Incorrect acto behaviour 
- `trial-04-0000/0002`
- `trial-04-0009/0006`
- `trial-04-0010/0003`

### What happened
In these test cases, acto tries to modify the `storageClassName` sub property for the PVCs used by bookkeeper. However, actos behaviour is not consistent with the logs. For example, acto tries to add ACTOKEY as a storage class name, and when viewing the system state clearly there is no change that reflects this, however none of actos oracles raise an alarm. Later when removing this ACTOKEY and modifying it to `''`, acto correctly raises an alarm that no corresponding state change exists. I will look into acto's code to see why this behaviour happens in the future.

In either case, these testcases are misoperations as changing the storage class name to something that does not exist is not okay. However, setting the storage class name as an empty string is a valid operation as in such a case the default storage class will be picked. 


## False Differential Alarms Type 1
- `071a184e0a9b9b0ad9013bb830799308/0000`
- `1094ed6d0287238b7ee8624653c601cc/0000`
- `16d076153462749f349fe4f2a9f0af63/0000`
- `1fec2bc37cf073186c66c154004946d1/0000`
- `401f67dc2e681ba4a1684c97a605efc1/0000`
- `46c0b5fe2ca4758510a42db87bcb2563/0000`
- `4ac730b42e81843ef582ee37134eb0fe/0000`
- `710112cf3d8551c136855d5f18d2f736/0000`
- `733d9cd65ee520cb936a6b92f560c6b0/0000`
- `74943d9794c181be98b524d82ca69cf7/0000`
- `7bbbae820494d03357175d8408991bc8/0000`
- `7dfaa1d73e1bd880c794fe38dc0ab560/0000`
- `95bf2fb470ced14b7ed181ed4db2f837/0000`
- `9ba273691592873af0ea2d84750cf4a2/0000`
- `a9c2f9b123a0abcd79be955bba030385/0000`
- `c156b090d35281bb459e94d53b9c0052/0000`
- `cfbd2432d249a1aebac3ba776af6b00d/0000`
- `d247e38f59a81260669b71f62f4a0be1/0000`
- `d2e51a6bb44175f2294ebbc51089aa3c/0000`
- `d4e3651966f1ea51d436528dc006eb70/0000`
- `dc46f1c253244823149ef555c120b549/0000`
- `e1b87dbceefb4d28f8fe669074d3df09/0000`
- `e4291a712cd98c315adf28f5af1f46be/0000`

### Explanation
Each of these testcases resulted in a post-run differential test alarm. But on inspection, all the system state diffs are actually NULL. This is possibly a bug in acto that causes it to raise alarms despite no difference in the states. 

## False Differential Alarms Type 2
- `0d47bf1fca482818462603832b01b220/0000` 
- `2a5d4b85e67b163e3192a03ce383a325/0000`
- `b9a52fbcbcf1b7bd875173b26cee0cc0/0000`
- `e5281586d3b4c749857baaea81343229/0000`

### Explanation
Each of these testcases resulted in a post-run differential test alarm. But on inspection, all the system state diffs are actually only `type_changes` in the specification part of the system state. More specifically, there is no difference in the actual system state. This is possibly a bug in acto that causes it to raise alarms despite no difference in the actual system states. 

## General note on a possible reason differential oracle alarms
I did not find sufficient time to analyze all the differential oracle alarms. However, I have a possible reason why there are so many alarms for this operator. From my reading of the bookkeeper operator code, currently, in the reconciliation step, the operator **does not** make use of the input state in any of the reconcilation decisions. This is clearly visible in the structure of the code as well as in a comment in the main reconcile function [here](https://github.com/pravega/bookkeeper-operator/blob/14583ce9fea41a847758ddb933818c1860507c18/controllers/bookkeepercluster_controller.go#L63-L69). This indicates that the operator does not distinguish between input states at all when taking reconcilation decisions. Essentially, the operator looks at the spec specified by the user and blindly applies the changes without looking at the current cluster state. This shows that the bookkeeper operator is still in its nascent stages of developement and hasn't matured enough to handle all possible cases. It works well for the common use cases but does not work well in corner cases and is not good at recovering from error states. It might make sense to analyze the operator with acto again as the operator development evolves over the coming months or years as the repository matures. 