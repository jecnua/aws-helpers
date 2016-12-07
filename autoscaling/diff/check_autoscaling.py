#
import pprint
import boto3
from fabric.colors import red, yellow, green
import pprint
import argparse

VERBOSE = False

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity",action="store_true")
parser.add_argument("ag",help="autoscaling group",nargs='?')
args = parser.parse_args()
if args.verbose:
    print("Verbosity turned on")
    VERBOSE = True

def __date2str(dts):
    return dts.strftime("%Y %m %d %H:%M:%S GMT")

def __check_ag(aws_ag):
    ec2_client = boto3.client('ec2')
    pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(aws_ag)
    if VERBOSE:
        print("Checking " + aws_ag['AutoScalingGroupName'])
        print("LaunchConfigurationName: " + aws_ag['LaunchConfigurationName'])
    instances = aws_ag['Instances']
    for instance in instances:
        test = ""
        if 'LaunchConfigurationName' not in instance:
            print(red("=========="))
            pp.pprint(instance)
            print(red("No autoscaling group name"))
            print(red("If you are using terraform it may have been deleted. Destroy this node if possible"))
            print("To terminate the instance:")
            print(
                yellow(
                    "aws autoscaling terminate-instance-in-auto-scaling-group --instance-id " +
                    instance['InstanceId'] +
                    " --no-should-decrement-desired-capacity"))
            print(red("=========="))
        else:
            if instance['LaunchConfigurationName'] != aws_ag[
                    'LaunchConfigurationName']:
                an_instance = ec2_client.describe_instances(
                    InstanceIds=[
                        instance['InstanceId'],
                    ],
                )
                date = __date2str(an_instance['Reservations'][0][
                                  'Instances'][0]['LaunchTime'])
                test = red(" == DIFFERENT == " + date)
            if instance['LaunchConfigurationName'] != aws_ag[
                    'LaunchConfigurationName']:
                print(
                    instance['InstanceId'] +
                    ": " +
                    instance['LaunchConfigurationName'] +
                    test)
                print("To terminate the instance:")
                print(
                    yellow(
                        "aws autoscaling terminate-instance-in-auto-scaling-group --instance-id " +
                        instance['InstanceId'] +
                        " --no-should-decrement-desired-capacity"))
                print("# https://docs.aws.amazon.com/cli/latest/reference/autoscaling/terminate-instance-in-auto-scaling-group.html")
            else:
                if VERBOSE:
                    print(
                        instance['InstanceId'] +
                        ": " +
                        instance['LaunchConfigurationName'] +
                        test)
#


def check_single(ag_name):
    client = boto3.client('autoscaling')
    response = client.describe_auto_scaling_groups(
        AutoScalingGroupNames=[
            ag_name,
        ],
        MaxRecords=1
    )
    __check_ag(response['AutoScalingGroups'][0])

#

def check_all():
    client = boto3.client('autoscaling')
    response = client.describe_auto_scaling_groups()
    if VERBOSE:
        print(green("Checking " +
                    str(len(response['AutoScalingGroups'])) +
                    " autoscaling roups"))
    for aws_ag in response['AutoScalingGroups']:
        __check_ag(aws_ag)

if args.ag:
    AUTOSCALING_GROUP_NAME = args.ag
    if VERBOSE:
        print(green("Checking 1 autoscaling roups"))
    check_single(AUTOSCALING_GROUP_NAME)
else:
    check_all()
