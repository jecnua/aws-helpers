import boto3
import pprint
from fabric.colors import red, green, yellow, white

client = boto3.client('autoscaling')
pp = pprint.PrettyPrinter(indent=4)
response = client.describe_auto_scaling_groups()
# pp.pprint(len(response)) # 2
# pp.pprint(response.keys())
# pp.pprint(response['AutoScalingGroups'])
print white("Found " + str(len(response['AutoScalingGroups'])) + " autoscaling groups\n")

countDisabled = 0
countEnabled = 0
countPartial = 0
for anAutoscaling in response['AutoScalingGroups']:
    # pp.pprint(anAutoscaling.keys())
    # print anAutoscaling['AutoScalingGroupName']
    # print "%60s" % (anAutoscaling['AutoScalingGroupName'])
    if len(anAutoscaling['EnabledMetrics']) == 0:
        print anAutoscaling['AutoScalingGroupName']  + red(" DISABLED")
        countDisabled = countDisabled + 1
    else:
        result = len(anAutoscaling['EnabledMetrics'])
        # for metric in anAutoscaling['EnabledMetrics']:
            # result = result + metric['Metric'] + ' '
        if result < 8:
            result = yellow("PARTIALLY DISABLED - ACTIVE: ") + red(str(result), bold=False)
            countPartial = countPartial + 1
        else:
            result = green(str(result))
            countEnabled = countEnabled + 1
        print green(anAutoscaling['AutoScalingGroupName']) + " " + result

print "\nRecap:"
print "> ENABLED: " + str(countEnabled)
print "> PARTIALLY-ENABLED: " + str(countPartial)
print "> DISABLED: " + str(countDisabled)
