## Summary
ALL ALARM ANALYSIS RAISED BY ACTO. Most of the alarms are false alarms with no real bug in the operator code.

Although, the alarms raised due to deleted/depreciated property, the property from the CRD should be removed. This can/should be reported to the developers.

## ALARM 1
trial-00-0000/0002

## What happened
When acto expected the value at the specified path in the input to be 5, but it found that the actual value was 0.

## Root Cause
acto tries to modify the property ‘periodSeconds’ from 5 to 0, but the minimum value of this property is 1. 

## Expected behavior?
This is a false alarm. The operator should be able to easily reject the new spec as it is less than the minimum value. 

## ALARM 2
trial-00-0002/0001

## What happened
It is a string-deletion / string-change / string-empty error raised by ACTO. 

## Root Cause
acto tries to modify the property ‘accessModes’, to something which is not a valid value!

## Expected behavior?
This is a false alarm. The operator should be able to easily reject the new spec as it is a garbage value and not a part of default values.
accessModes contains the desired access modes the volume should have. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#access-modes-1'

## ALARM 3
trial-00-0000/0001 ( SAME AS 1 ) 

## ALARM 4
trial-00-0001/0001 ( SAME AS 1 ) 

## ALARM 5
trial-00-0001/0002 ( SAME AS 1 )

## ALARM 6
trial-00-0002/0002 ( SAME AS 2 )
## ALARM 7
trial-00-0002/0003 ( SAME AS 2 )

## ALARM 8
trial-00-0002/0004 ( SAME AS 2 )

## ALARM 9 ( SAME AS 2, on property: matchExpressions )
trial-00-0002/0005 

## ALARM 10 ( SAME AS 2, on property: matchExpressions )
trial-00-0002/0006

## ALARM 11 ( SAME AS 2, on property: matchExpressions )
trial-00-0002/0007 ( FALSE ALARM AS SPECIFIED BY ACTO )

## ALARM 12 ( SAME AS 2, on property: matchExpressions )
trial-00-0002/0008 ( FALSE ALARM AS SPECIFIED BY ACTO )

## ALARM 13
trial-00-0002/0009 ( FALSE ALARM AS SPECIFIED BY ACTO )

## What happened
It is a string-deletion error raised by ACTO. 

## Root Cause
acto tries to delete the property image. To “ACTOKEY” ( Specifies, Image of the additional container.)

## Expected behavior?
This is a false alarm. It is an invalid request.

## ALARM 14 ( Same as 13 ) ( FALSE ALARM AS SPECIFIED BY ACTO )

## ALARM 15 
trial-00-0003/0001 ( Same as 13 ) ( FALSE ALARM AS SPECIFIED BY ACTO )

## ALARM 16
trial-00-0003/0002 ( Same as 13 ) ( FALSE ALARM AS SPECIFIED BY ACTO )

## ALARM 17
trial-00-0004/0001 ( Same as 13 ) ( FALSE ALARM AS SPECIFIED BY ACTO )

## ALARM 18
trial-00-0004/0002 ( Same as 13 ) ( FALSE ALARM AS SPECIFIED BY ACTO )
## ALARM 19, 20, 21
trial-00-0004/0003, trial-00-0004/0004, trial-00-0004/0005 

livenessProbe:
                description: LivenessProbe Port is set to `druid.port` if not specified
                  with httpGet handler.


## ALARM 22, 23, 24, 25
trial-00-0004/0006, trial-00-0004/0007, trial-00-0005/0001, trial-00-0005/0002

REASON:
Trying to modify a depreciated property here:
As per docs, Kubernetes 1.29 does not include a gcePersistentDisk volume type.
The gcePersistentDisk in-tree storage driver was deprecated in the Kubernetes v1.17 release and then removed entirely in the v1.28 release. The Kubernetes project suggests that you use the Google Compute Engine Persistent Disk CSI third party storage driver instead. This change should reflect in the CR. Can be reported to the devs.
## ALARM 26, 27, 28, 29
trial-00-0006/0002, trial-00-0006/0001, trial-00-0007/0001, trial-00-0007/0002
## What happened
When acto expected the value at the specified path in the input to be 0, but it found no matching fields for input. livenessProbe.timeoutSeconds to 0

## Root Cause
acto tries to modify the property livenessProbe.timeoutSeconds from 3 to 0, but the minimum value of this property is 1. 

## Expected behavior?
FALSE ALARM, AS STATED BY ACTO.

## ALARM 30, 31, 32, 33
trial-00-0009/0009, trial-00-0009/0008, trial-00-0010/0001, trial-00-0010/0002. 

## What happened
This is an integer-deletion, integer-change / integer-updation alarm. 

## Root Cause
Acto tried to update a depreciated property ‘awsElasticBlockStore’. Operator should reject it. Operator source code should remove this from CR. 

## Expected behavior?
False Alarm, as stated by acto. Operator CR should be updated.

## ALARM 34, 35, 36, 37, 38, 39
trial-00-0011/0001, trial-00-0011/0002, trial-00-0011/0003, trial-00-0011/0004, trial-00-0012/000,  trial-00-0012/0001

## What happened

Expected property ‘replicaCount’ to be 0, found 2 instead. 

## Root Cause

In the operator code, ‘replicaCount’ is set to 2, this is for the testing environment. In actual production environment, this value will be determined based on the number of factors.

## Expected behavior?

False alarm, as stated by acto. 

## ALARM 40, 41, 42, 43, 44, 45, 46, 47, 48

## What happened

Mismatch of the property: ‘volumeClaimTemplates.resources’ 

## Root Cause

In the operator code, volumeClaimTemplates.resources is set to “NOT PRESENT”, but found to be 1. As, NOT PRESENT, is not a valid value for this property, the operator rejects it.

## Expected behavior?

This is a False Alarm as raised by ACTO.

############################################################################





Scope for Future Improvements:

Try to understand the reason for the alarm:

testrun-2024-02-22-21-35/trial-00-0015/0002
{"field": "[\"spec\", \"nodes\", \"ACTOKEY\", \"hpAutoscaler\", \"metrics\", 0, \"pods\", \"target\", \"averageValue\"]", "testcase": "integer-change"}
message='Found no matching fields for input' input_diff=Diff(prev=2, curr=4, path=["spec", "nodes", "ACTOKEY", "hpAutoscaler", "metrics", 0, "pods", "target", "averageValue"]) system_state_diff=None



Possible Reason:


The operator ignores any change of this property, as this is a metric. 



