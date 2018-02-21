#

import boto3
import pprint
import datetime
from operator import itemgetter, attrgetter
from fabric.colors import red, green, yellow, white

PP = pprint.PrettyPrinter(indent=4)
EC2_CLIENT = boto3.client('ec2')
RESULT = {}


def _search_old_nodes(age_in_days=30, region='us-east-1'):
    print('Age in days: ' + str(age_in_days))
    print('Region: ' + region)
    all_servers = EC2_CLIENT.describe_instances()
    # PP.pprint(all_servers['Reservations'])
    for reservation in all_servers['Reservations']:
        for instance in reservation['Instances']:
            state = instance['State']['Name']
            # PP.pprint(instance['State']['Name'])
            lunch_time = instance['LaunchTime']
            # print(type(lunch_time))
            now = datetime.datetime.now(datetime.timezone.utc)
            delta = now - lunch_time
            name = 'NO NAME'
            if 'Tags' in instance:
                for tag in instance['Tags']:
                    if tag['Key'] == 'Name':
                        name = tag['Value']
            RESULT.update(
                {instance['InstanceId'] + ' ' + name + ' ' + state : delta.days}
            )
            # diff_in_time = datetime.datetime.now() - lunch_time
            # PP.pprint(instance['InstanceType'] + ' ' + str(instance['LaunchTime']))
    # PP.pprint(sorted(RESULT, key=itemgetter(2), reverse=True))
    PP.pprint(sorted(RESULT.items(), key=itemgetter(1), reverse=True))
    # PP.pprint(sorted(RESULT.values()))


_search_old_nodes(age_in_days=30, region='us-east-1')
