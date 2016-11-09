import boto3
import pprint
import re
from fabric.colors import red, green, yellow, white

client = boto3.client('autoscaling')
pp = pprint.PrettyPrinter(indent=4)
response = client.describe_auto_scaling_groups()
print(white("Found " +
            str(len(response['AutoScalingGroups'])) +
            " autoscaling groups\n"))

countDisabled = 0
countEnabled = 0
countPartial = 0
countIgnored = 0
for anAutoscalingGroup in response['AutoScalingGroups']:
    if len(anAutoscalingGroup['EnabledMetrics']) == 0:
        if re.search('awseb-e', anAutoscalingGroup['AutoScalingGroupName']):
            print(
                anAutoscalingGroup['AutoScalingGroupName'] +
                yellow(" BEANSTALK - IGNORING"))
            countIgnored = countIgnored + 1
        else:
            print(
                anAutoscalingGroup['AutoScalingGroupName'] +
                red(" DISABLED"))
            countDisabled = countDisabled + 1
    else:
        resultString = len(anAutoscalingGroup['EnabledMetrics'])
        if resultString < 8:
            resultString = yellow(
                "PARTIALLY DISABLED - ACTIVE: ") + red(str(resultString), bold=False)
            countPartial = countPartial + 1
        else:
            resultString = green(str(resultString))
            countEnabled = countEnabled + 1
        print(
            green(
                anAutoscalingGroup['AutoScalingGroupName']) +
            " " +
            resultString)

print(white("\nRecap:"))
print(green("> ENABLED: " + str(countEnabled)))
print(red("> PARTIALLY-ENABLED: " + str(countPartial)))
print(red("> DISABLED: " + str(countDisabled)))
print(yellow("> IGNORED: " + str(countIgnored)))
