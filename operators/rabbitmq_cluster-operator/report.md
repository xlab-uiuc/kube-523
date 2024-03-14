---
name: Alarm Inspection Report
about: An analysis report for the alarms produced by Acto
---


**ALARM 1**

trial-00-0000/0001

**Categorization**

Alarm

**Root Cause**

The activeDeadlineSeconds in StatefulSet is not Supported. This is a bug. Specified in this bug raised in 
rabbitmq(https://github.com/kedacore/keda/issues/630). The job spun  should get deleted after time interval specified in ttlSecondsAfterFinish. But the job is kept
and not deleted.

**ALARM 2**

trial-00-0000/0002

**Categorization**

False Alarm

**Root Cause**

Just False Alarm due to waiting for the consumer to be created before binding the testcases.

**ALARM 3**

trial-00-0000/0003

**Categorization**

False Alarm

**Root Cause**

Same as Alarm 2

**ALARM 4**

trial-00-0000/0004

**Categorization**

Alarm

**Root Cause**

Same as Alarm 1

**ALARM 5**

trial-00-0001/0002

**Categorization**

Alarm

**Root Cause**

"Invalid input determined from status message: The service has no endpoints available" was the error given by ACTO. 
It seems it can be a docker problem. It is not able to connect to the correct endpoints on the system. A similar problem
was found here https://github.com/devmentors/DNC-DShop/issues/8. 



**ALARM 6**

trial-00-0004/0003

**Categorization**

Misoperation

**Root Cause**

"Container image \"rabbitmqoperator/cluster-operator:2.7.0\" already present on machine" This shows that it tried to construct a container already on the machine.

**ALARM 7**

trial-00-0005/0002

**Categorization**

Misoperation

**Root Cause**

same as Alarm 6

**ALARM 8**

trial-00-0006/0004

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 9**

trial-00-0007/0002

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 10**

trial-00-0008/0001

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 11**

trial-00-0009/0001

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 12**

trial-00-0011/0003

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 13**

trial-00-0012/0002

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 14**

trial-00-0013/0002

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 15**

trial-00-0014/0008

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 16**

trial-00-0016/0001

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

