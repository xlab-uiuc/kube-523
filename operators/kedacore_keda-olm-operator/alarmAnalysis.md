
Based on my analysis, I don’t feel this Acto is super useful for this operator. However, for a sanity check, I will run Acto again and check everything.

# Alarm 1: Trial 00-0000
## What happened:
System states show empty JSON files, but it should show the system state with the updated number of replicas. This System state should be updated to the CRD when the `horizontalPodAutoscalerConfig` sets the replicas to a higher or lower value. I also see in the mutated-001.yaml that it tried to set the `horizontalPodAutoscalerConfig` to `INVALID_NAME`, which isn’t the right way to use this property (and it is not assigning the other required properties here). I also see on some of the operator logs that an exception occurred. What this tells us is that this alarm is a misoperation because this tried to access `horizontalPodAutoscalerConfig` such that it tried to set it to a different setting as opposed to a number, which is a misoperation. It’s also not putting the required fields

Also, looking at the CLI outputs, it is running into the error where Acto is not able to validate the trial run.

## Root cause:
Look at the `horizontalPodAutoscalerConfig` part of the `scaledJobs` crd. This requires the behavior (which takes behavior as a policy, and in that policy is the period (in second, int), the type (string), and the value (amount of change) (int)), and Acto was not passing an integer.  

## Expected behavior:
This should pass in a behavior (which takes behavior as a policy, and in that policy is the period (in second, int), the type (string), and the value (amount of change) (int)), and Acto was not passing an integer. Based on this, Keda should run these policies for the specified period and then autoscale based on those policies, and then Acto would check.

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

## Root cause:
Look at the `health` property of the `scaledObjects` `CRD` (under spec).

## Expected Behavior:
Acto should simulate the desired number of failures by creating a large number of pods and crashing them equal to the desired number of failures. The health property should take care of the rest.

## Classification:
False Alarm


Based on my analysis, I don’t feel this Acto is super useful for this operator. However, for a sanity check, I will run Acto again and check everything.

# Alarm 11: trial-00-0005
## What happened:
This tries to toggle the `scaleUp` behavior for `horizontalPodAutoscalerConfig` by setting the period, type, and value of the policies of `scaleUp`. However, y, but the system state still shows nothing. Looking at all the mutated values, it seems that it is assigning the field values correctly here, but appears to crash when it shouldn’t. Looking at the operator logs, an exception is raised when waiting for convergence.


## Root Cause:
Look at the `scaleUp` property of `horizontalPodAutoscalerConfig` of the `scaledObjects` `CRD` (under spec).


## Expected Behavior:
Acto should simulate the scaling-up property by simulating machines using many resources and then keda assigning more resources.


## Classification:
False Alarm


# Alarm 12: trial-00-0006
## What happened:
This tries to toggle the `originalReplicaCount` field. However,, the system state still shows nothing. Looking at the operator logs, an exception is raised when waiting for convergence. This is similar to Alarm 11


## Root Cause:
Look at the `originalReplicaCount` property of the `scaledObjects` `CRD` (under spec).


## Expected Behavior:
Acto should simulate the `originalReplicaCount` by starting off with the specified replicas when running an autoscaler.


## Classification:
False Alarm


# Alarm 13: trial-00-0007
## What happened:
This tries to toggle the `scaleTargetGVKR` field. However, the system state still shows nothing. Looking at the operator logs, an exception is raised when waiting for convergence. This is similar to Alarm 2


## Root Cause:
Look at the scaleTargetGVKR part of the `scaledJobs` crd. This requires the exact parameters as what was provided, but it appears this crashed due to the empty state.

Expected behavior: 




## Expected Behavior:
This should provide a unified structure for the schema.GroupVersionKind and Resource according to description.


## Classification:
False Alarm


# Alarm 14: trial-00-0008
## What happened:
This tries to toggle the `scaleDown` field of `horizontalPodAutoscalerConfig`. However, the system state still shows nothing. Looking at the operator logs, an exception is raised when waiting for convergence. This is similar to Alarm 11


## Root Cause:
Look at the `scaleDown` property of `horizontalPodAutoscalerConfig` of the `scaledObjects` `CRD` (under spec).


## Expected Behavior:
Acto should simulate the scaling-down property by simulating machines using lesser resources and then keda reducing the number of pods.


## Classification:
False Alarm


# Alarm 15: trial-00-0009
## What happened:
This tries to toggle the `horizontalPodAutoscalerConfig` fields and `fallback` fields. However, the system state still shows nothing. Additionally, this doesn’t toggle the required fields for `horizontalPodAutoscalerConfig` 


## Root Cause:
Look at `horizontalPodAutoscalerConfig` of the `scaledObjects` `CRD` (under spec).


## Expected Behavior:
Acto should toggle the `horizontalPodAutoscalerConfig` behavior by toggling all the required fields.


## Classification:
Misoperations


# Alarm 16: trial-00-0010
## What happened:
This tries to toggle the `maxReplicaCount` field. However, the system state still shows nothing. 


## Root Cause:
Look at `maxReplicaCount` field of the `scaledObjects` `CRD` (under spec).


## Expected Behavior:
Acto should try to raise the number of replicas after setting the `maxReplicaCount` and then see if keda limits this.


## Classification:
False Alarm


# Alarm 17: trial-01-0001
## What happened:
This tries to toggle the `minReplicaCount`, `triggers`, and then the `conditions` fields. However, the system state still shows nothing. Furthermore, when running `triggers`, the other required field must also be triggered. Also, looking at the logs, it appears that an exception has occurred when trying to toggle the field 


## Root Cause:
Look at `minReplicaCount` field of the `scaledObjects` `CRD` (under spec). Also see the `triggers` field in `spec` of the `scaledObjects` `CRD`.


## Expected Behavior:
Acto should try to decrease the number of replicas below and see if the number of replicas falls below that of the `minReplicaCount` and if it does, then KEDA has failed.


## Classification:
Misoperation or Bug on Acto’s end.


# Alarm 18: trial-01-0002
## What happened:
This did not toggle any mutations, but we got an empty system state. Looking at the operator logs, Acto found “Bug! Exception raised when waiting for converge.”, meaning an exception occurred when performing such a mutation on the operator. What I do think is missing though is the required fields from the spec.
  


## Root Cause:
Look at the `spec` in the `scaledObjects` `CRD`.


## Expected Behavior:
Acto should toggle and/or initialize the required fields of the spec or in general of the operator CRD


## Classification:
Misoperation




# Alarm 19: trial-01-0003
## What happened:
This tries to toggle the `externalMetricNames` of the `status` of the `schema`. However, the system state still is empty.


## Root Cause:
Look at the `externalMetricNames` in the `scaledObjects` `CRD`.


## Expected Behavior:
Acto should add items to `externalMetricNames` and then perform the analysis and see what was received with the `externalMetricNames`.


## Classification:
False Alarm


# Alarm 20: trial-01-0004
## What happened:
This tries to toggle the `triggers` field of the CRD and provides metadata to it. However, the other required field ( `scaleTargetRef`) was not triggered.


## Root Cause:
Look at the ` `scaleTargetRef`` in the `scaledObjects` `CRD`. However, 


## Classification:
Misoperation


# Alarm 21: trial-01-0005
## What happened:
Similar to Alarm 18, this did not toggle any mutations, but we got an empty system state. Looking at the operator logs, Acto found “Bug! Exception raised when waiting for converge.”, meaning an exception occurred when performing such a mutation on the operator. What I do think is missing though is the required fields from the spec.


## Root Cause:
Look at the `spec` in the `scaledObjects` `CRD`.


## Expected Behavior:
Acto should toggle and/or initialize the required fields of the spec or in general of the operator CRD


## Classification:
Misoperation


# Alarm 22: trial-01-0006
## What happened:
Similar to Alarm 2, System states here also show empty JSON files, but it should show the system state with the updated replicas. I see that in mutated-005, it assigns the values of scaleTargetGVKR field correctly, but the system state still shows nothing. Looking at all the mutated values, it seems that it is assigning the field values correctly here, but appears to crash when it shouldn’t.


## Root Cause:
Look at the scaleTargetGVKR part of the `scaledJobs` crd. This requires the exact parameters as what was provided, but it appears this crashed due to the empty state


## Expected Behavior:
This should provide a unified structure for the schema.GroupVersionKind and Resource according to description. 




## Classification:
False Alarm


# Alarm 23: trial-01-0007
## What happened:
This toggled with the `scaleTargetRef`, but this toggling it’s `apiVersion` and `envSourceContainerName` fields. This though is getting similar results to the previous alarms (empty state, exceptions in operator logs).  




## Root Cause:
Look at the `scaleTargetRef` part of the `scaledJobs` crd. This requires the exact parameters as what was provided, but it appears this crashed due to the empty state


## Expected Behavior:
This should hold the reference to the scale target Object. 


## Classification:
False Alarm

# Alarm 24: trial-01-0008
## What happened:
Similar to Alarm 18, this did not toggle any mutations, but we got an empty system state. Looking at the operator logs, Acto found “Bug! Exception raised when waiting for converge.”, meaning an exception occurred when performing such a mutation on the operator. What I do think is missing though is the required fields from the spec.


## Root Cause:
Look at the `spec` in the `scaledObjects` `CRD`.


## Expected Behavior:
Acto should toggle and/or initialize the required fields of the spec or in general of the operator CRD


## Classification:
Misoperation


# Alarm 25: trial-01-0009
## What happened:
This tries to toggle the `externalMetricNames` of the `status` of the `schema`. However, this does not assign an array to the `externalMetricNames`. System state is also empty for a lot of these cases


## Root Cause:
Look at the `externalMetricNames` in the `scaledObjects` `CRD`.


## Expected Behavior:
Acto should add items to `externalMetricNames` and then perform the analysis and see what was received with the `externalMetricNames`.


## Classification:
Misoperation


# Alarm 26: trial-01-0010
## What happened:
This tries to toggle the `triggers` field of the CRD and provides metadata to it. However, the other required field was not triggered.


## Root Cause:
Look at the `scaleTargetRef` in the `scaledObjects` CRD.


## Expected Behavior:
Acto should also trigger the `scaleTargetRef` property as that is also required


## Classification:
Misoperation


# Alarm 27: trial-02-0001
## What happened:
This tries to toggle the `authenticationRef` specifically of the `triggers` field of the CRD and provides metadata to it. However, the other required field was still not triggered.


## Root Cause:
Look at the `scaleTargetRef` in the `scaledObjects` CRD.


## Expected Behavior:
Acto should also trigger the `scaleTargetRef` property as that is also required


## Classification:
Misoperation


# Alarm 28: trial-02-0002
## What happened:
This tries to toggle the behavior of the `horizontalPodAutoscalerConfig` by playing around with the field. However, like the other alarms, this was still leading into an exception and still getting an empty state. 


## Root Cause:
Look at `horizontalPodAutoscalerConfig` of the `scaledObjects` `CRD` (under spec).


## Expected Behavior:
Based on these 


## Classification:
False Alarm


# Alarm 29: trial-02-0002
## What happened:
This tries to toggle the behavior of the `horizontalPodAutoscalerConfig` by playing around with the field. However, like the other alarms, this was still leading to an exception and still getting an empty state. 


## Root Cause:
Look at `horizontalPodAutoscalerConfig` of the `scaledObjects` `CRD` (under spec).


## Expected Behavior:
Based on these configurations, Acto should test for when these scenarios hold (i.e when setting `periodSeconds`, it should check for if the `scaleUp` policy held within the window).


## Classification:
False Alarm


# Alarm 30: trial-02-0003
## What happened:
This tries to toggle the behavior of `resourceMetricNames` and `scaleTargetKind`. However, like the other alarms, this was still leading to an exception and still getting an empty state. 


## Root Cause:
Look at `status` of the `scaledObjects` `CRD`, especially `resourceMetricNames` and `scaleTargetKind`.


## Expected Behavior:
Based on these configurations, Acto should test for when these kinds of resource metrics will be considered and what kind of target to scale to.


## Classification:
False Alarm


# Alarm 31: trial-02-0004
## What happened:
This tries to toggle `cooldownPeriod` in `specs` along with the properties in `status`. However, like the other alarms, this was still leading to an exception and still getting an empty state. 


## Root Cause:
Look at `status` of the `scaledObjects` `CRD`. Also look at `cooldownPeriod` in the `specs` of the `scaledObjects` `CRD`.


## Expected Behavior:
Based on these configurations, based on the `cooldownPeriod`, Acto should test for whether the system was able to cool down after that period after autoscaling. Acto should also test for when each of these scenarios in `status` behave when set (i.e when `numberOfFailures` is 4 and `originalReplicaCount` is 5, then test for when the number of failures can go beyond 4 from the original replica count).


## Classification:
False Alarm
# Alarm 32: trial-02-0005
## What happened:
Similar to Alarm 11. This tries to toggle the `scaleUp` behavior for `horizontalPodAutoscalerConfig` by setting the period, type, and value of the policies of `scaleUp`. However, y, but the system state still shows nothing. Looking at all the mutated values, it seems that it is assigning the field values correctly here, but appears to crash when it shouldn’t. Looking at the operator logs, an exception is raised when waiting for convergence.


## Root Cause:
Look at the `scaleUp` property of `horizontalPodAutoscalerConfig` of the `scaledObjects` `CRD` (under spec).


## Expected Behavior:
Acto should simulate the scaling-up property by simulating machines using many resources and then keda assigning more resources.


## Classification:
False Alarm


# Alarm 33: trial-02-0006
## What happened:
This tries to manipulate the `lastActiveTime` and `pausedReplicaCount` for the status, but like with the other alarms, the system state is empty and looking at the operator logs, we ran into an exception. 


## Root Cause:
Look at the `lastActiveTime` and `pausedReplicaCount` properties of `status` of the `scaledObjects` `CRD` (under spec).


## Expected Behavior:
First off, `lastActiveTime` should be sent in date-time format according to CRD. Also, this should be set whenever KEDA performs the autoscaling. Second, for `pausedReplicaCount`, this should test for when the replica count decreases/increases to that value and stop there.


## Classification:
Misoperation (incorrect way to set lastActiveTime)


# Alarm 34: trial-02-0007
## What happened:
This tries to manipulate the `scalingModifiers` in `advanced` in `spec`. However, this does not set all the properties, only the `target` property. But none of the properties are required, so only setting `target` should be fine. However, this appears to still have an empty state.


## Root Cause:
Look at the `scalingModifiers` in `advanced` in `spec` of the `scaledObjects` `CRD` (under spec).


## Expected Behavior:
This should basically do nothing as only the `target` has changed, that’s it.


## Classification:
False Alarm


# Alarm 35: trial-02-0008
## What happened:
This did not toggle any mutations, but we got an empty system state. Looking at the operator logs, Acto found “Bug! Exception raised when waiting for converge.”, meaning an exception occurred when performing such a mutation on the operator. What I do think is missing though is the required fields from the spec.
  


## Root Cause:
Look at the `spec` in the `scaledObjects` `CRD`.


## Expected Behavior:
Acto should toggle and/or initialize the required fields of the spec or in general of the operator CRD


## Classification:
Misoperation


# Alarm 36: trial-02-0009
## What happened:
This toggles with the `pollingInterval` in `spec`. However, like all the alarms, this leads to an empty system state.
  


## Root Cause:
Look at the `spec` in the `scaledObjects` `CRD` (particularly `pollingInterval`).


## Expected Behavior:
Keda should check every trigger source every period specified by the polling interval, and Acto should verify that Keda checked each trigger source


## Classification:
False Alarm


# Alarm 37: trial-02-0010
## What happened:
This toggles with the `pollingInterval` in `spec`. However, like all the alarms, the system states are empty. Looking at the operator logs, Acto found “Bug! Exception raised when waiting for converge.”, meaning an exception occurred when performing such a mutation on the operator.


## Root Cause:
Look at the `pollingInterval` in `spec` in the `scaledObjects` `CRD`.


## Expected Behavior:
When setting the Polling Interval, Acto should check for each trigger on during the interval specified by the polling interval. 


## Classification:
False Alarm


# Alarm 38: trial-03-0003
## What happened:
This toggles with the `restoreToOriginalReplicaCount` in `advanced` in `spec`. However, like all the alarms, the system states are empty. Looking at the operator logs, Acto found “Bug! Exception raised when waiting for converge.”, meaning an exception occurred when performing such a mutation on the operator.


## Root Cause:
Look at the `restoreToOriginalReplicaCount` in `advanced` in `spec` in the `scaledObjects` `CRD`.


## Expected Behavior:
When the flag is toggled, Acto should restore the `replicaCount` to what it was originally.


## Classification:
False Alarm


# Alarm 39: trial-03-0004
## What happened:
This toggles with the `restoreToOriginalReplicaCount` in `advanced` in `spec`. However, like all the alarms, the system states are empty. Looking at the operator logs, Acto found “Bug! Exception raised when waiting for converge.”, meaning an exception occurred when performing such a mutation on the operator.


## Root Cause:
Look at the `restoreToOriginalReplicaCount` in `advanced` in `spec` in the `scaledObjects` `CRD`.


## Expected Behavior:
When setting the Polling Interval, Acto should check for each trigger on during the interval specified by the polling interval. 


## Classification:
False Alarm


# Alarm 40: trial-03-0005
## What happened:
This toggles with the `restoreToOriginalReplicaCount` in `advanced` in `spec`. However, like all the alarms, the system states are empty. Looking at the operator logs, Acto found “Bug! Exception raised when waiting for converge.”, meaning an exception occurred when performing such a mutation on the operator.


## Root Cause:
Look at the `restoreToOriginalReplicaCount` in `advanced` in `spec` in the `scaledObjects` `CRD`.


## Expected Behavior:
When this is triggered, Keda should bring the number of pods to the original replica count. 


## Classification:
False Alarm


# Alarm 41: trial-03-0006
## What happened:
This tries to toggle the `triggers` field (particularly the use of `useCachedMetrics`) of the CRD and provides metadata to it. However, the other required field was not triggered.


## Root Cause:
Look at the `triggers` in the `scaledObjects` `CRD`. However, 


## Classification:
Misoperation


# Alarm 42: trial-03-0007
## What happened:
This tries to toggle the `conditions` of `status` field of the CRD. However system state is still empty like all alarms.


## Root Cause:
Look at the `conditions` of `status` in the `scaledObjects` `CRD`.


## Expected Behavior:
Acto is supposed to store the Conditions an array representation to store multiple Conditions


## Classification:
False Alarm


# Alarm 43: trial-03-0008
## What happened: 
This tries to account for pod failure when autoscaling by toggling `failureThreshold` and `replicas` for the `fallback` (which is the spec for fallback options according to the description). Acto is supposed to simulate the behavior of the pods failing, so the `failureThreshold` accounts for that, but it appears that it ran into another exception. The system states are also empty. 

## Root Cause:
Look at the `fallback` property of the `scaledObjects` `CRD` (under spec). What this does is that it decides how many failures it tolerates and then decides how many replicas to go to.

## Expected Behavior:
Acto should simulate the pods failing and then see how the fallback property is accounting for those rather than crashing and giving an empty state.


## Classification:
False Alarm


# Alarm 44: trial-03-0009
## What happened:
This tries to toggle the `triggers` field (particularly the use of `useCachedMetrics`) of the CRD and provides metadata to it. However, the other required field was not triggered.


## Root Cause:
Look at the `triggers` in the `scaledObjects` `CRD`. However, 


## Classification:
Misoperation


# Alarm 45: trial-03-0009
## What happened:
This tries to toggle the `triggers` field (particularly the use of `useCachedMetrics`) of the CRD and provides metadata to it. However, the other required field was not triggered.


## Root Cause:
Look at the `triggers` in the `scaledObjects` `CRD`. However, 


## Classification:
Misoperation


# Alarm 46: trial-04-0000
## What happened:
This tries to toggle the `status` fields (particularly `health` and `conditions`) of the CRD and provides metadata to it. However, like the rest of the alarms, this returns an empty state. 


## Root Cause:
Look at the `conditions` and `health` of `status` in the `scaledObjects` `CRD`.


## Expected Behavior
Acto should simulate the desired number of failures by creating a large number of pods and crashing them equal to the desired number of failures. The health property should take care of the rest.


## Classification:
False Alarm


# Alarm 47: trial-04-0001
## What happened:
This tries to toggle the `status` fields (particularly `health` and `conditions`) of the CRD and provides metadata to it. However, like the rest of the alarms, this returns an empty state. 


## Root Cause:
Look at the `conditions` and `health` of `status` in the `scaledObjects` `CRD`.


## Expected Behavior:
Acto should simulate the desired number of failures by creating a large number of pods and crashing them equal to the desired number of failures. The health property should take care of the rest.


## Classification:
False Alarm


# Alarm 48: trial-05-0000
## What happened:
This tries to toggle the `externalMetricNames` of the `status` of the `schema`. However, the system state still is empty.


## Root Cause:
Look at the `externalMetricNames` in the `scaledObjects` `CRD`.


## Expected Behavior:
Acto should add items to `externalMetricNames` and then perform the analysis and see what was received with the `externalMetricNames`.


## Classification:
False Alarm


# Alarm 49: trial-05-0001
## What happened:
This tries to toggle the `triggers`. However, when running `triggers`, the other required field must also be triggered. Also, looking at the logs, it appears that an exception has occurred when trying to toggle the field 


## Root Cause:
 Look at the spec of the scaledObjects crd. You will see that scaleTargetRef and triggers are required


## Classification:
Misoperation or Bug on Acto’s end.


# Alarm 50: trial-06-0000
## What happened:
This tries to toggle the `resourceMetricNames` in `status`. However, like with all the alarms, the system states are empty.  


## Root Cause:
Look at `status` of the `scaledObjects` `CRD`, especially `resourceMetricNames`.


## Expected Behavior:
Based on these configurations, Acto should test for when these kinds of resource metrics will be considered and how exactly will they be.


## Classification:
False Alarm


# Alarm 51: trial-07-0000
## What happened:
This tries to toggle the `resourceMetricNames` in `status`. However, like with all the alarms, the system states are empty.  


## Root Cause:
Look at `status` of the `scaledObjects` `CRD`, especially `resourceMetricNames`.


## Expected Behavior:
Based on these configurations, Acto should test for when these kinds of resource metrics will be considered and how exactly will they be.


## Classification:
False Alarm


# Alarm 52: trial-07-0001
## What happened:
This tried to do multiple mutations, once changing the `restoreToOriginalReplicaCount`, then changing `scaleTargetGVKR` (most of the time), and also getting an empty mutation. As usual, the system states are very much empty  


## Root Cause:
Look at the `restoreToOriginalReplicaCount` in `advanced` in `spec` in the `scaledObjects` `CRD`. Also look at the scaleTargetGVKR part of the `scaledJobs` crd. This requires the exact parameters as what was provided, but it appears this crashed due to the empty state.


## Expected Behavior:
Based on these configurations, Keda should bring the number of replicas to the original count.


## Classification:
False Alarm


# Alarm 53: trial-08-0000
## What happened:
This tries to toggle the `originalReplicaCount` field. However,, the system state still shows nothing. Looking at the operator logs, an exception is raised when waiting for convergence. This is similar to Alarm 11


## Root Cause:
Look at the `originalReplicaCount` property of the `scaledObjects` `CRD` (under spec).


## Expected Behavior:
Acto should simulate the `originalReplicaCount` by starting off with the specified replicas when running an autoscaler.


## Classification:
False Alarm


# Alarm 54: trial-09-0000
## What happened:
This tries to toggle the `scalingModifiers` field and the `conditions` and `status`. However, the system state still shows nothing. Looking at the operator logs, an exception is raised when waiting for convergence. 


## Root Cause:
Look at the `scalingModifiers` in `specs` and `conditions` in `status` property of the `scaledObjects` `CRD` (under spec).


## Expected Behavior:
Acto should simulate the `scalingModifiers` by first specifying a scaling logic and then performing the scaling based on that logic (i.e when resource utilization reaches a point, how is that logic used).


## Classification:
False Alarm


# Alarm 55: trial-09-0001
What happened:
This tried to set the scalingModifiers to the required values in the crd in part 003. This also tried to set the required values of triggers of the spec for scaledObjects crd, but is missing scaleTargetRef, which is also required property of the spec. This is a misoperation.

Root cause: Look at the spec of the scaledObjects crd. You will see that scaleTargetRef and triggers are required

Classification: Misoperation (I feel that Acto should account for other required properties too. Maybe it is just a thing with this operator).

# Alarm 56: trial-10-0000
## What happened:
This tried to set the `lastActiveTime` and the `pausedReplicaCount`, but `lastActiveTime` is not set in date-time format. This is a misoperation.

## Root Cause:
Look at the `lastActiveTime` and `pausedReplicaCount` properties of `status` of the `scaledObjects` `CRD` (under spec).


## Expected Behavior:
First off, `lastActiveTime` should be sent in date-time format according to CRD. Also, this should be set whenever KEDA performs the autoscaling. Second, for `pausedReplicaCount`, this should test for when the replica count decreases/increases to that value and stop there.


## Classification:
Misoperation (incorrect way to set lastActiveTime)


# Alarm 57: trial-10-0001
## What Happened: 
Similar behavior to the previous alarms, system state is an empty state. This is accounted for `scaleTargetRef`, but they didn’t provide the other required field.

### Root Cause: 
Look at the `triggers` field of the `scaledObjects` crd.

### Expected Behavior:
Hold reference to the scale target Object according to the description

### Classification: 
Misoperation

# Alarm 57: trial-12-0000
## What Happened: 
Toggled `horizontalPodAutoscalerConfig` such that now there are many policies for scaling down and scaling up. However, like all the alarms, the system states are empty. Looking at the operator logs, Acto found “Bug! Exception raised when waiting for converge.”, meaning an exception occurred when performing such a mutation on the operator. 

### Root Cause: 
Look at the `horizontalPodAutoscalerConfig` field of the `scaledObjects` crd.

### Expected Behavior:
Keda should decide how to do the scaling up and scaling down based on the values telling the resource utilization (which Acto should simulate).

### Classification: 
False Alarm


# Alarm 58: trial-12-0001
## What happened:
This tries to toggle the `maxReplicaCount` field. However, the system state still shows nothing. 


## Root Cause:
Look at `maxReplicaCount` field of the `scaledObjects` `CRD` (under spec).


## Expected Behavior:
Acto should try to raise the number of replicas after setting the `maxReplicaCount` and then see if keda limits this.


## Classification:
False Alarm


# Alarm 59: trial-14-0000
## What happened:
This toggles with the `pollingInterval` in `spec`. However, like all the alarms, this leads to an empty system state.
  


## Root Cause:
Look at the `spec` in the `scaledObjects` `CRD` (particularly `pollingInterval`).


## Expected Behavior:
Keda should check every trigger source every period specified by the polling interval, and Acto should verify that Keda checked each trigger source


## Classification:
False Alarm


# Alarm 60: trial-14-0001
## What happened:
This tries to toggle the `status` fields (particularly `health` and `conditions`) of the CRD and provides metadata to it. However, like the rest of the alarms, this returns an empty state. 


## Root Cause:
Look at the `conditions` and `health` of `status` in the `scaledObjects` `CRD`.


## Expected Behavior:
Acto should simulate the desired number of failures by creating a large number of pods and crashing them equal to the desired number of failures. The health property should take care of the rest.


## Classification:
False Alarm


# Alarm 61: trial-15-0000
## What happened: 
This tries to account for pod failure when autoscaling by toggling `failureThreshold` and `replicas` for the `fallback` (which is the spec for fallback options according to the description). Acto is supposed to simulate the behavior of the pods failing, so the `failureThreshold` accounts for that, but it appears that it ran into another exception. The system states are also empty. 

## Root Cause:
Look at the `fallback` property of the `scaledObjects` `CRD` (under spec). What this does is that it decides how many failures it tolerates and then decides how many replicas to go to.

## Expected Behavior:
Acto should simulate the pods failing and then see how the fallback property is accounting for those rather than crashing and giving an empty state.

Classification:
False Alarm


# Alarm 62: trial-15-0001
## What happened:
This tries to toggle the `triggers` field of the CRD and provides metadata to it. However, the other required field ( `scaleTargetRef`) was not triggered.


## Root Cause:
Look at the ` `scaleTargetRef`` in the `scaledObjects` `CRD`. However, 


## Classification:
Misoperation


Based on this analysis, I don’t think this operator is suitable for Acto due to how this operator was structured. If the operator crashes for a few cases, then it’s probably scalable, but since this is happening in all the places. 
