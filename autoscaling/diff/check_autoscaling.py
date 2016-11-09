#
import sys
import boto3
import pprint
from fabric.colors import red, yellow

AUTOSCALING_GROUP_NAME = sys.argv[1]

#
def date2str(dt):
    return(dt.strftime("%Y %m %d %H:%M:%S GMT"))

#
def check():
    client = boto3.client('autoscaling')
    ec2_client = boto3.client('ec2')
    # pp = pprint.PrettyPrinter(indent=4)

    print(AUTOSCALING_GROUP_NAME)

    response = client.describe_auto_scaling_groups(
        AutoScalingGroupNames=[
            AUTOSCALING_GROUP_NAME,
        ],
        MaxRecords=1
    )

    # print (response)

    print("LaunchConfigurationName: ")
    print(response['AutoScalingGroups'][0]['LaunchConfigurationName'])

    instances = response['AutoScalingGroups'][0]['Instances']

    # print (response['AutoScalingGroups'][0]['Instances'])
    for instance in instances:
        test = ""
        if instance['LaunchConfigurationName'] != response['AutoScalingGroups'][0]['LaunchConfigurationName']:
            an_instance = ec2_client.describe_instances(
                InstanceIds=[
                    instance['InstanceId'],
                ],
            )
            # pp.pprint(instance['Reservations'][0]['Instances'][0]['LaunchTime'])
            date = date2str(an_instance['Reservations'][0]['Instances'][0]['LaunchTime'])
            test = red(" == DIFFERENT == " + date)
        print(instance['InstanceId'] + ": " + instance['LaunchConfigurationName'] + test)
        if instance['LaunchConfigurationName'] != response['AutoScalingGroups'][0]['LaunchConfigurationName']:
            print("To terminate the instance:")
            print(yellow("aws autoscaling terminate-instance-in-auto-scaling-group --instance-id " + instance['InstanceId'] + " --no-should-decrement-desired-capacity"))
            print("")

    #https://docs.aws.amazon.com/cli/latest/reference/autoscaling/terminate-instance-in-auto-scaling-group.html

check()
