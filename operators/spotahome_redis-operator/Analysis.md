# Lab1: analysis
total inspected alarms:  141

## Incomplete PVC config
**True Alarm?**
True alarm
**CR Change**
Added PVC config
**What Happened**
Acto generated incomplete PVC config, and operator didn't fill with default value or reject the incomplete config. Then the new Pod is unable to be deployed due to error, causing cluster to stuck in wrong state.     

	(create Pod rfr-test-cluster-1 in StatefulSet rfr-test-cluster failed error: Pod "rfr-test-cluster-1" is invalid: [spec.containers[0].volumeMounts[3].name: Required value, spec.containers[0].volumeMounts[3].name: Not found: ""])

Trial ids: (61 in total)
00-0002,00-0004,00-0016,00-0017,00-0032,00-0033,00-0034,01-0000,01-0014,01-0015,01-0030,01-0031,01-0039,01-0040,01-0041,01-0050,01-0051,01-0052,02-0026,02-0027,03-0019,03-0020,03-0028,03-0029,03-0030,03-0034,03-0035,03-0036,03-0043,03-0044,03-0051,03-0050,03-0088,03-0052,04-0024,04-0025,04-0026,04-0027,04-0035,04-0036,04-0047,04-0048,04-0065,04-0066,04-0076,04-0076,04-0076,04-0076,04-0076,04-0076,04-0076,04-0076,04-0076,04-0076,04-0077,05-0022,05-0030,05-0032,05-0033,05-0051,05-0053,

**How to fix**
Operator should either fill blanked fields with default value, or reject incomplete configs 

## Incomplete/erroneous extraContainers config
**True Alarm?**
True alarm
**CR Change**
Added/modified extraContainers config
**What Happened**
Acto generated both incomplete and erroneous extraContainers config, and operator didn't fill with default value or reject the incomplete config. Then the new Pod is unable to be deployed due to error, causing cluster to stuck in wrong state.     

	create Pod rfr-test-cluster-1 in StatefulSet rfr-test-cluster failed error: Pod \"rfr-test-cluster-1\" is invalid: [spec.containers[2].image: Required value, spec.containers[2].env[0].valueFrom.configMapKeyRef.name: Invalid value: \"INVALID_NAME\": a lowercase RFC 1123 subdomain must consist of lower case alphanumeric characters, '-' or '.', and must start and end with an alphanumeric character (e.g. 'example.com', regex used for validation is '[a-z0-9]([-a-z0-9]*[a-z0-9])?(\\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*')]",

Trial ids: (67 in total)
00-0031,01-0010,01-0012,01-0034,01-0057,01-0058,01-0059,01-0080,01-0081,01-0082,01-0083,02-0003,02-0004,02-0005,02-0015,02-0017,02-0018,02-0032,02-0033,02-0040,02-0041,02-0042,02-0044,02-0045,02-0046,02-0050,02-0052,02-0053,02-0054,02-0055,02-0073,02-0074,02-0075,02-0076,02-0077,03-0012,03-0013,03-0021,03-0022,03-0023,03-0031,03-0033,03-0037,03-0038,03-0039,03-0040,03-0042,03-0061,03-0084,04-0002,04-0015,04-0016,04-0017,04-0018,04-0030,04-0031,04-0055,04-0056,04-0057,04-0058,04-0090,05-0001,05-0002,05-0003,05-0004,05-0009,05-0010,05-0019,

**How to fix**
Operator should either fill blanked fields with default value, or reject incomplete configs 

## Invalid topologySpreadConstraints config
**True Alarm?**
True alarm
**CR Change**
Added/modified topologySpreadConstraints config
**What Happened**
True Alarm, Acto generated invalid value on topology spread constraints, operator failed to identify and reject 

	"create Pod rfr-test-cluster-1 in StatefulSet rfr-test-cluster failed error: Pod \"rfr-test-cluster-1\" is invalid: [spec.topologySpreadConstraints[0].whenUnsatisfiable: Unsupported value: \"ACTOKEY\": supported values: \"DoNotSchedule\", \"ScheduleAnyway\", spec.topologySpreadConstraints[0].nodeAffinityPolicy: Unsupported value: \"ACTOKEY\": supported values: \"Honor\", \"Ignore\", spec.topologySpreadConstraints[0].nodeTaintsPolicy: Unsupported value: \"ACTOKEY\": supported values: \"Honor\", \"Ignore\", spec.topologySpreadConstraints[0].matchLabelKeys[0]: Invalid value: \"ACTOKEY\": exists in both matchLabelKeys and labelSelector, spec.topologySpreadConstraints[0].matchLabelKeys[1]: Invalid value: \"ACTOKEY\": exists in both matchLabelKeys and labelSelector]"

Trial ids: (4 in total)
00-0020, 01-0017, 01-0018, 05-0044

**How to fix**
Operator should either fill blanked fields with default value, or reject incomplete configs 

## Invalid extraVolumes config
**True Alarm?**
False alarm
**CR Change**
Added/modified extraVolumes config
**What Happened**
Acto generated invalid value 47016u for field sizeLimit, which got rejected by operator and didn't reflect in real state. Then Acto's consistency oracle not met, raised an false alarm (these are not invalid value tests)

	W0306 11:25:21.729498  1  reflector.go:533] pkg/mod/k8s.io/client-go@v0.27.3/tools/cache/reflector.go:231: failed to list <unspecified>: quantities must match the regular expression '^([+-]?[0-9.]+)([eEinumkKMGTP]*[-+]?[0-9]*)$'

	E0306 11:25:21.731269  1  reflector.go:148] pkg/mod/k8s.io/client-go@v0.27.3/tools/cache/reflector.go:231: Failed to watch <unspecified>: failed to list <unspecified>: quantities must match the regular expression '^([+-]?[0-9.]+)([eEinumkKMGTP]*[-+]?[0-9]*)$'

Trial ids: (1 in total)
01-0028

**How to fix**
Acto might improve rules to follow the regex expression for stoage size related field 


## Invalid initContainers config
**True Alarm?**
True and False alarm (true for health oracle and false for consistency oracle)
**CR Change**
Added/modified initContainers config
**What Happened**
Acto generated value +.7e+.01620577 that don't match the regex ^([+-]?[0-9.]+)([eEinumkKMGTP]*[-+]?[0-9]*)$, which is rejected (this is a array-pop case), then generated incomplete config, like cases above

	create Pod rfr-test-cluster-1 in StatefulSet rfr-test-cluster failed error: Pod "rfr-test-cluster-1" is invalid: spec.initContainers[0].image: Required value


Trial ids: (1 in total)
02-0061

**How to fix**
Acto should generate more accurate testcase; Second part is similar to 00-0015, developer shoud add webhook to check.

## Misoperation in command config
**True Alarm?**
Misoperation
**CR Change**
Acto added command "ACTOKEY" in spec/redis/command
**What Happened**
The "ACTOKEY" command replaced the starting command "redis-server", causing redis unable to start, but this is probably a misoperation due to the disign. User should add command "redis-server" first, then add other command.

	//generator.go:1061
	func getRedisCommand(rf *redisfailoverv1.RedisFailover) []string {  
	    if len(rf.Spec.Redis.Command) > 0 {  
	       return rf.Spec.Redis.Command  
	    }  
	    return []string{  
	       "redis-server",  
	       fmt.Sprintf("/redis/%s", redisConfigFileName),  
	    }  
	}


Trial ids: (6 in total)
02-0036, 02-0038, 02-0039, 03-0005, 03-0006, 03-0007

**How to fix**
Acto should generate more accurate testcase; Second part is similar to 00-0015, developer shoud add webhook to check.

## k8s-overload
**True Alarm?**
True alarm
**CR Change**
Acto changed replica to 1000 replicas
**What Happened**
Operator didn't reject the overloaded config and tried to deploy 1000 pods and caused cluster to crash. 

	//validate.go:48
	if r.Spec.Sentinel.Replicas <= 0 {  
	    r.Spec.Sentinel.Replicas = defaultSentinelNumber  
	}
	//only checked if replicas <= 0


Trial ids: (1 in total)
00-0036

**How to fix**
Developer should add more check on this field to ensure replicas don't exhaust all resources. 














