#
import sys
import boto3
import pprint
from fabric.colors import red, yellow, green

VERBOSE=False

#
def __date2str(dt):
    return(dt.strftime("%Y %m %d %H:%M:%S GMT"))

#
def __check_ag(ag):
    ec2_client = boto3.client('ec2')
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(ag)
    print("Checking "+ag['AutoScalingGroupName'])
    if VERBOSE:
        print("LaunchConfigurationName: " + ag['LaunchConfigurationName'])
    instances = ag['Instances']
    for instance in instances:
        test = ""
        if instance['LaunchConfigurationName'] != ag['LaunchConfigurationName']:
            an_instance = ec2_client.describe_instances(
                InstanceIds=[
                    instance['InstanceId'],
                ],
            )
            date = __date2str(an_instance['Reservations'][0]['Instances'][0]['LaunchTime'])
            test = red(" == DIFFERENT == " + date)
        if instance['LaunchConfigurationName'] != ag['LaunchConfigurationName']:
            print(instance['InstanceId'] + ": " + instance['LaunchConfigurationName'] + test)
            print("To terminate the instance:")
            print(yellow("aws autoscaling terminate-instance-in-auto-scaling-group --instance-id " + instance['InstanceId'] + " --no-should-decrement-desired-capacity"))
            print("# https://docs.aws.amazon.com/cli/latest/reference/autoscaling/terminate-instance-in-auto-scaling-group.html")
        else:
            if VERBOSE:
                print(instance['InstanceId'] + ": " + instance['LaunchConfigurationName'] + test)
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
    print(green("Checking " + str(len(response['AutoScalingGroups'])) + " autoscaling roups"))
    for ag in response['AutoScalingGroups']:
        __check_ag(ag)

if len(sys.argv) == 1:
    check_all()
if len(sys.argv) == 2:
    AUTOSCALING_GROUP_NAME = sys.argv[1]
    print(green("Checking 1 autoscaling roups"))
    check_single(AUTOSCALING_GROUP_NAME)
