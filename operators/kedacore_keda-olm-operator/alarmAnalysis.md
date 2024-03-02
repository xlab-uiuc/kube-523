
Based on my analysis, I don’t feel this Acto is super useful for this operator. However, for a sanity check, I will run Acto again and check everything.

# Alarm 1: Trial 00-0000
## What happened:
System states show empty JSON files, but it should show the system state with the updated number of replicas. This System state should be updated to the CRD when the `horizontalPodAutoscalerConfig` sets the replicas to a higher or lower value. I also see in the mutated-001.yaml that it tried to set the `horizontalPodAutoscalerConfig` to `INVALID_NAME`, which isn’t the right way to use this property (and it is not assigning the other required properties here). I also see on some of the operator logs that an exception occurred. What this tells us is that this alarm is a misoperation because this tried to access `horizontalPodAutoscalerConfig` such that it tried to set it to a different setting as opposed to a number, which is a misoperation. It’s also not putting the required fields

Also, looking at the CLI outputs, it is running into the error where Acto is not able to validate the trial run.

## Root cause:
Look at the `horizontalPodAutoscalerConfig` part of the `scaledJobs` crd. This requires the behavior (which takes behavior as a policy, and in that policy is the period (in second, int), the type (string), and the value (amount of change) (int)), and Acto was not passing an integer.  

## Expected behavior:
This should pass 

## Classification: 
Misoperation (or invalid input from Acto)

# Alarm 2: Trial 00-0001
## What Happened:
System states here also show empty JSON files, but it should show the system state with the updated replicas. I see that in `mutated-005`, it assigns the values of `scaleTargetGVKR` field correctly, but the system state still shows nothing. Looking at all the mutated values, it seems that it is assigning the field values correctly here, but appears to crash when it shouldn’t.

## Root cause:
Look at the `scaleTargetGVKR` part of the `scaledJobs` crd. This requires the exact parameters as what was provided, but it appears this crashed.

## Classification: 
False Alarm

## Expected behavior: 
This should provide a unified structure for the `schema.GroupVersionKind` and `Resource` according to description. 

# Alarm 3: Trial 00-0002
System states here also show empty JSON files, but it should show the system state with the updated replicas. Here, it tried to only set the `logLevel` of `metricsServer`.

## Root cause:
Look at the `metricsServer` part of the crd. This requires the exact parameters as what were provided, but it appears this crashed.

## Expected behavior:
`logLevel` of 0 means for info, and that was the only thing it, so it should not have crashed (should have functioned regularly).

## Classification: 
False Alarm

# Alarm 4: Trial 00-0004
## What happened:
This tried to set the message, status, and type of the conditions of scaledobjects schema, and this apparently raised an exception on the operator.

## Root cause: 
Look at the `conditions:` member variable under `status` of scaledobjects crd. 

## Classification: 
False Alarm

## Expected behavior: 
This should provide a unified structure for the `schema.GroupVersionKind` and `Resource` according to description. 


# Alarm 5: Trial 01--0000
## What happened:
This tried to set the `scalingModifiers` to the required values in the crd in part 003. This also tried to set the required values of triggers of the spec for `scaledObjects` crd, but is missing `scaleTargetRef`, which is also required property of the spec. This is a misoperation.

## Root cause: 
Look at the spec of the `scaledObjects` crd. You will see that `scaleTargetRef` and `triggers` are required

## Expected Behavior:
Acto should also toggle the `triggers` field.

# Classification: 
Misoperation (I feel that Acto should account for other required properties too. Maybe it is just a thing with this operator). 

# Alarm 6: Trial 01–0001
## What happened:
This tried to toggle with the min replica count `minReplicaCount` for the `scaledObjects` CRD. This also tried to toggle the conditions for status. However, this is still getting an exception according to the operator logs when it shouldn’t. This also doesn’t account for the required fields (particularly `scaleTargetRef`)

## Root cause: 
Look at `minReplicaCount` in `scaledObjects` CRD.

## Expected behavior: 
Toggle the minimum number of pods we scale down to. 

## Classification: 
False alarm for wrong behavior when toggling replicas (but going deeper, this is a misoperation for forgetting the other required fields).

# Alarm 7: Trial 02–0000
## What Happened: 
Similar behavior to the previous alarms, system state is an empty state. This is accounted for `scaleTargetRef`, but they didn’t provide the other required field.

## Root cause: 
Look at the `triggers` field of the `scaledObjects` crd.

## Expected behavior:
Hold reference to the scale target Object according to the description

## Classification: 
Misoperation (or bug in Acto for not accounting for other required fields)

# Alarm 8: Trial 03-0000
## What Happened: 
Similar behavior to the previous alarms (particularly Alarm 7), system state is an empty state. This is accounted for `scaleTargetRef`, but they didn’t provide the other required field.

## Root cause: 
Look at the `triggers` field of the `scaledObjects` crd.

## Expected behavior:
Hold reference to the scale target Object according to the description

## Classification: 
Misoperation

# Alarm 8: Trial 03-0000
## What Happened: 
Similar behavior to the previous alarms (particularly Alarm 7), system state is an empty state. This is accounted for `scaleTargetRef` (toggle different optional variable this time), but they didn’t provide the other required field.

## Root cause: 
Look at the `triggers` field of the `scaledObjects` CRD. This is a required CRD

## Expected behavior:
Hold reference to the scale target Object according to the description

## Classification: 
Misoperation

# Alarm 9: trial-03-0001
## What happened: 
This tries to account for pod failure when autoscaling by toggling `failureThreshold` and `replicas` for the `fallback` (which is the spec for fallback options according to the description). Acto is supposed to simulate the behavior of the pods failing, so the `failureThreshold` accounts for that, but it appears that it ran into another exception. The system states are also empty. 

## Root cause:
Look at the `fallback` property of the `scaledObjects` `CRD` (under spec). What this does is that it decides how many failures it tolerates and then decides how many replicas to go to.

## Expected Behavior:
Acto should simulate the pods failing and then see how the fallback property is accounting for those rather than crashing and giving an empty state.

## Classification:
False Alarm

# Alarm 10: trial-03-0001
## What happened: 
This tries to account for the health of `ScaledObject` by toggling the `health` spec in `ScaledObject` CRD. However, the system states were empty and didn’t produce the desired value. 

# Root cause:
Look at the `health` property of the `scaledObjects` `CRD` (under spec).

# Expected Behavior:
Acto should simulate the desired number of failures by creating a large number of pods and crashing them equal to the desired number of failures. The health property should take care of the rest.

# Classification:
False Alarm

