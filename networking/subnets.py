#!/usr/bin/env python
# Just to have a look at how the subnets are distribuited

import boto3

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

for an_az in results:
    print(f"================== {an_az}")
    for subnet in results[an_az]:
        print(subnet)
    print("==================")
