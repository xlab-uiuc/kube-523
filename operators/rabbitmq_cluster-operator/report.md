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

**ALARM 17**

trial-00-0017/0001

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 18**

trial-00-0018/0001

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 19**

trial-00-0019/0001

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 20**

trial-00-0019/0002

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 21**

trial-00-0019/0003

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 22**

trial-00-0020/0001

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 23**

trial-00-0020/0002

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 24**

trial-00-0021/0001

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 25**

trial-00-0021/0002

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 26**

trial-00-0023/0005

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 27**

trial-00-0024/0002

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 28**

trial-00-0025/0001

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 29**

trial-00-0027/0002

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 30**

trial-00-0028/0002

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 31**

trial-00-0029/0002

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 32**

trial-00-0030/0003

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 33**

trial-00-0031/0001

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 34**

trial-00-0032/0002

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 35**

trial-00-0034/0002

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 36**

trial-00-0035/0001

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 37**

trial-00-0036/0006

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 38**

trial-00-0038/0006

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 39**

trial-00-0039/0003

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 40**

trial-00-0040/0002

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 41**

trial-00-0042/0003

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 42**

trial-00-0043/0006

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 43**

trial-00-0045/0005

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 44**

trial-00-0046/0007

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 45**

trial-00-0047/0002

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 46**

trial-00-0049/0004

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 47**

trial-00-0050/0002

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 48**

trial-00-0051/0001

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 49**

trial-00-0052/0001

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 50**

trial-00-0053/0002

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 51**

trial-00-0055/0002

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 52**

trial-00-0056/0003

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 53**

trial-00-0056/0004

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 54**

trial-00-0057/0003

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 55**

trial-00-0057/0005

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 56**

trial-00-0059/0001

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 57**

trial-00-0060/0002

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 58**

trial-00-0061/0002

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 59**

trial-00-0062/0002

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 60**

trial-00-0063/0001

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 61**

trial-00-0065/0002

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 62**

trial-00-0066/0001

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 63**

trial-00-0067/0001

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 64**

trial-00-0068/0002

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 65**

trial-00-0069/0002

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 66**

trial-00-0070/0002

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 67**

trial-00-0071/0003

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 68**

trial-00-0073/0001

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 69**

trial-00-0074/0001

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 70**

trial-00-0075/0001

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 71**

trial-00-0076/0002

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 72**

trial-00-0000/0005

**Categorization**

Misoperation

**Root Cause**

Same as Alarm 6

**ALARM 73**

trial-00-0064/0004

**Categorization**

False Alarm

**Root Cause**

The right kubernetes API was not specified.

**ALARM 74**

trial-00-0064/0005

**Categorization**

False Alarm

**Root Cause**

Same as alarm 73

**ALARM 75**

trial-00-0064/0006

**Categorization**

False Alarm

**Root Cause**

Same as alarm 73

**ALARM 76**

trial-00-0064/0007

**Categorization**

False Alarm

**Root Cause**

Same as alarm 73

**ALARM 77**

trial-00-0065/0000

**Categorization**

False Alarm

**Root Cause**

Same as alarm 73

**ALARM 78**

trial-00-0065/0001

**Categorization**

False Alarm

**Root Cause**

Same as alarm 73

**ALARM 79**

trial-00-0066/0000

**Categorization**

False Alarm

**Root Cause**

Same as alarm 73

**ALARM 80**

trial-00-0067/0000

**Categorization**

False Alarm

**Root Cause**

Same as alarm 73

**ALARM 81**

trial-00-0068/0000

**Categorization**

False Alarm

**Root Cause**

Same as alarm 73

**ALARM 82**

trial-00-0069/0000

**Categorization**

False Alarm

**Root Cause**

Same as alarm 73

**ALARM 83**

trial-00-0070/0000

**Categorization**

False Alarm

**Root Cause**

Same as alarm 73

**ALARM 84**

trial-00-0071/0000

**Categorization**

False Alarm

**Root Cause**

Same as alarm 73

**ALARM 85**

trial-00-0072/0000

**Categorization**

False Alarm

**Root Cause**

Same as alarm 73

**ALARM 86**

trial-00-0073/0000

**Categorization**

False Alarm

**Root Cause**

Same as alarm 73

**ALARM 87**

trial-00-0074/0000

**Categorization**

False Alarm

**Root Cause**

Same as alarm 73

**ALARM 88**

trial-00-0075/0000

**Categorization**

False Alarm

**Root Cause**

Same as alarm 73

**ALARM 89**

trial-00-0076/0000

**Categorization**

False Alarm

**Root Cause**

Same as alarm 73

**ALARM 90**

trial-00-0077/0000

**Categorization**

False Alarm

**Root Cause**

Same as alarm 73

**ALARM 91**

trial-00-0000/0000

**Categorization**

False Alarm

**Root Cause**

Same as alarm 73

**ALARM 92**

trial-00-0001/0000

**Categorization**

False Alarm

**Root Cause**

Same as alarm 73

**ALARM 93**

trial-00-0001/0000

**Categorization**

False Alarm

**Root Cause**

Same as alarm 73

**ALARM 94**

trial-00-0003/0000

**Categorization**

False Alarm

**Root Cause**

Same as alarm 73

**ALARM 95**

trial-00-0004/0000

**Categorization**

False Alarm

**Root Cause**

Same as alarm 73

**ALARM 96**

trial-00-0005/0000

**Categorization**

False Alarm

**Root Cause**

Same as alarm 73

**ALARM 97**

trial-00-0006/0000

**Categorization**

False Alarm

**Root Cause**

Same as alarm 73

**ALARM 98**

trial-00-0007/0000

**Categorization**

False Alarm

**Root Cause**

Same as alarm 73

**ALARM 99**

trial-00-0008/0000

**Categorization**

False Alarm

**Root Cause**

Same as alarm 73

**ALARM 100**

trial-00-0009/0000

**Categorization**

False Alarm

**Root Cause**

Same as alarm 73
