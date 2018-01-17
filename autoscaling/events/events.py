#
import pprint
import boto3
from datetime import date
from datetime import timedelta
from datetime import datetime
from datetime import timezone

PP = pprint.PrettyPrinter(indent=4)
AG_CLIENT = boto3.client('autoscaling')

def _check_events():
    all_ags = AG_CLIENT.describe_auto_scaling_groups(
        # AutoScalingGroupNames=[
        #     'string',
        # ],
        # NextToken='string',
        # MaxRecords=123
    )
    # PP.pprint(all_ags)
    for single_ag in all_ags['AutoScalingGroups']:
        ag_group_name = single_ag['AutoScalingGroupName']
        # PP.pprint(ag['AutoScalingGroupName'])
        response = AG_CLIENT.describe_scaling_activities(
            AutoScalingGroupName=ag_group_name,
            MaxRecords=50,
        )
        # PP.pprint(response)
        print(ag_group_name + ' : ' + str(len(response['Activities'])))
        # exit(1)
        if len(response['Activities']) > 10:
            # PP.pprint("    " + str(response['Activities']['StartTime']))
            for activitie in response['Activities']:
                this_date = activitie['StartTime']
                time_difference = datetime.now(timezone.utc) - this_date
                PP.pprint(time_difference.days())
                PP.pprint(time_difference.seconds())
                # datetime.isocalendar()
                # PP.pprint(datetime.isocalendar())
                exit(1)
                # PP.pprint(activitie['StartTime'])
            exit(1)
        # exit()
    print("bye")

_check_events()
