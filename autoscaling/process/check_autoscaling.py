#
import sys
import re
import boto3
from fabric.colors import red, green, yellow, white
# import argparse
# import pprint

VERBOSE = True
#
# parser = argparse.ArgumentParser()
# parser.add_argument("-v", "--verbose", help="increase output verbosity",action="store_true")
# args = parser.parse_args()
# if args.verbose:
#     print("Verbosity turned on")
#     VERBOSE = True


def __get_blocked__processes(aws_ag):
    processes_blocked = ""
    for temp_var in aws_ag['SuspendedProcesses']:
        processes_blocked = processes_blocked + temp_var["ProcessName"] + " "
    return processes_blocked


def __analise(aws_ag):
    if len(aws_ag['SuspendedProcesses']):
        processes_blocked = __get_blocked__processes(aws_ag)
        print("AutoScalingGroupName: " + aws_ag['AutoScalingGroupName'])
        print("LaunchConfigurationName: " + aws_ag['LaunchConfigurationName'] + " || Status: " + red(
            "Blocked " + str(len(aws_ag['SuspendedProcesses'])) + " processes"))
        if VERBOSE:
            print("The following processes are blocked >> " +
                  red(processes_blocked))
    else:
        print("AutoScalingGroupName: " + aws_ag['AutoScalingGroupName'])
        print("LaunchConfigurationName: " +
              aws_ag['LaunchConfigurationName'] + " || Status: " + green("Unblocked"))
    print(yellow(">> aws autoscaling suspend-processes --auto-scaling-group-name=\"" +
                 aws_ag['AutoScalingGroupName'] + "\""))
    print(green(">> aws autoscaling resume-processes --auto-scaling-group-name=\"" +
                aws_ag['AutoScalingGroupName'] + "\""))
    if VERBOSE:
        splitted = str(aws_ag['AutoScalingGroupARN']).split(":")
        region = splitted[3]
        id_with_no_space = re.sub(r"\s+", '+', aws_ag['AutoScalingGroupName'])
        print(white("Link to console: https://console.aws.amazon.com/ec2/autoscaling/home?region=" +
                    region + "#AutoScalingGroups:id=" + id_with_no_space + ";view=details"))
    print("")


def __check_ag(aws_ag, filter_for_ag=False):
    if filter_for_ag:
        if re.search(filter_for_ag, aws_ag['AutoScalingGroupName']):
            __analise(aws_ag)
    else:
        __analise(aws_ag)


def __check(filter_for_ag=False):
    client = boto3.client('autoscaling')
    response = client.describe_auto_scaling_groups()
    print(green("There are " +
                str(len(response['AutoScalingGroups'])) +
                " autoscaling groups"))
    for aws_ag in response['AutoScalingGroups']:
        __check_ag(aws_ag, filter_for_ag)


if len(sys.argv) == 1:
    __check()
if len(sys.argv) == 2:
    AUTOSCALING_GROUP_NAME = sys.argv[1]
    __check(AUTOSCALING_GROUP_NAME)
