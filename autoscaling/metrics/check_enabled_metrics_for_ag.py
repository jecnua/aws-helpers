import boto3
import pprint
import re
import argparse
from fabric.colors import red, green, yellow, white

VERBOSE = False

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity",action="store_true")
args = parser.parse_args()
if args.verbose:
    print("Verbosity turned on")
    VERBOSE = True

client = boto3.client('autoscaling')
pp = pprint.PrettyPrinter(indent=4)
response = client.describe_auto_scaling_groups()
if VERBOSE:
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
            if VERBOSE:
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

if VERBOSE:
    print(white("\nRecap:"))
    print(green("> ENABLED: " + str(countEnabled)))
    print(red("> PARTIALLY-ENABLED: " + str(countPartial)))
    print(red("> DISABLED: " + str(countDisabled)))
    print(yellow("> IGNORED: " + str(countIgnored)))
