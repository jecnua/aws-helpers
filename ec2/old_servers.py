#!/usr/bin/env python

import boto3
import pprint
import datetime
import argparse
from operator import itemgetter

pp = pprint.PrettyPrinter(indent=4)
ec2_client = boto3.client('ec2')
results = []
ignored = 0
total_servers = 0

parser = argparse.ArgumentParser("")
parser.add_argument('-m', '--max-results', type=int,
                    default=-1, help='The max number of results')
parser.add_argument('-o', '--older-than', type=int,
                    default=0, help='Number of days you want the all_servers to \
                    be older too')
args = parser.parse_args()


def _search_old_nodes():
    global ignored
    global total_servers
    all_servers = ec2_client.describe_instances()
    for reservation in all_servers['Reservations']:
        for instance in reservation['Instances']:
            total_servers += 1
            state = instance['State']['Name']
            lunch_time = instance['LaunchTime']
            now = datetime.datetime.now(datetime.timezone.utc)
            delta = now - lunch_time
            if int(delta.days) > args.older_than:
                name = 'NO NAME'
                if 'Tags' in instance:
                    for tag in instance['Tags']:
                        if tag['Key'] == 'Name':
                            name = tag['Value']
                results.append((instance['InstanceId'], name,
                                delta.days, state))
            else:
                ignored += 1


print("Gathering the data... This can take a while (AWS is slow)")
print("FYI: Filters won't speed it up :D")
_search_old_nodes()
results.sort(key=itemgetter(2), reverse=True)
pp.pprint(results[:args.max_results:])
showing = 0
if args.max_results == -1:
    showing = 'all'
else:
    showing = args.max_results
print(f"Found {len(results)} servers that respect the search criteria \
(showing {showing} results)")
print(f"Ignoring {ignored} servers because they are younger than give age")
print(f"Found {total_servers} servers in total")
