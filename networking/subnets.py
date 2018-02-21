#!/usr/bin/env python
# Just to have a look at how the subnets are distribuited

import boto3
import re
import argparse

parser = argparse.ArgumentParser("")
parser.add_argument('-a', '--available', action='store_true',
                    help='List the available CIDR')
args = parser.parse_args()

client = boto3.client('ec2')
json_result = client.describe_subnets(
    DryRun=False,
    # Filters=[
    #     {
    #         'Name': 'vpc-id',
    #         # 'Values': [
    #         #     'vpc-xxx',
    #         # ]
    #     },
    # ]
)

results = {}
for subnet in json_result['Subnets']:
    az = subnet['AvailabilityZone']
    subnet_name = 'No name'
    cidr_block = subnet['CidrBlock']
    subnet_id = subnet['SubnetId']
    if 'Tags' in subnet:
        for aTag in subnet['Tags']:
            if aTag['Key'] == 'Name':
                subnet_name = aTag['Value']
    toAdd = (cidr_block, subnet_name, subnet_id)
    if az not in results:
        results[az] = []
    results[az].append(toAdd)

range_ip = []
for an_az in results:
    for subnet in results[an_az]:
        range_ip.append(re.split('/', subnet[0])[0])
if args.available:
    cidrs = [int(re.split('\.', range)[2]) for range in range_ip]
    available_cidr = list(set(range(1, 255)).difference(cidrs))
    used = sum([len(results[an_az]) for an_az in results])
    print(f"Found {len(available_cidr)} available ({used} used)")
    print(available_cidr)
else:
    for an_az in results:
        print(f"================== {an_az}: {len(results[an_az])} subnets")
        for subnet in results[an_az]:
            print(subnet)
        print("==================")
    print(f"Found {sum([len(results[an_az]) for an_az in results])} subnets")
