#!/usr/bin/env python
# Just to have a look at how the subnets are distribuited
#
# TODO: Remove repetition of code
# TODO: Acced VPC id as parameter
# TODO: Be flexible with number of subnets

import boto3
import pprint

pp = pprint.PrettyPrinter(indent=4)
client = boto3.client('ec2')
json_result = client.describe_subnets(
    DryRun=False,
    Filters=[
        {
            'Name': 'vpc-id',
            'Values': [
                'vpc-xxx',
            ]
        },
    ]
)

all_subnets = []
a = []
b = []
c = []
d = []
e = []

# pp.pprint(json_result['Subnets'])
# exit()

for subnet in json_result['Subnets']:
    all_subnets.append(subnet['CidrBlock']+" "+subnet['AvailabilityZone'])
    if subnet['AvailabilityZone'] == 'us-east-1a':
        toAdd = subnet['CidrBlock']
        tags = subnet['Tags']
        for aTag in tags:
            if aTag['Key'] == 'Name':
                toAdd = toAdd+' '+aTag['Value']+' '+subnet['SubnetId']
        a.append(toAdd)
    if subnet['AvailabilityZone'] == 'us-east-1b':
        toAdd = subnet['CidrBlock']
        tags = subnet['Tags']
        for aTag in tags:
            if aTag['Key'] == 'Name':
                toAdd = toAdd+' '+aTag['Value']+' '+subnet['SubnetId']
        b.append(toAdd)
    if subnet['AvailabilityZone'] == 'us-east-1c':
        toAdd = subnet['CidrBlock']
        tags = subnet['Tags']
        for aTag in tags:
            if aTag['Key'] == 'Name':
                toAdd = toAdd+' '+aTag['Value']+' '+subnet['SubnetId']
        c.append(toAdd)
    if subnet['AvailabilityZone'] == 'us-east-1d':
        toAdd = subnet['CidrBlock']
        tags = subnet['Tags']
        for aTag in tags:
            if aTag['Key'] == 'Name':
                toAdd = toAdd+' '+aTag['Value']+' '+subnet['SubnetId']
        d.append(toAdd)
    if subnet['AvailabilityZone'] == 'us-east-1e':
        toAdd = subnet['CidrBlock']
        tags = subnet['Tags']
        for aTag in tags:
            if aTag['Key'] == 'Name':
                toAdd = toAdd+' '+aTag['Value']+' '+subnet['SubnetId']
        e.append(toAdd)

print 'AZ a: '+str(len(a))
print "\n".join([str(x) for x in a])
print "\n"
# pp.pprint(sorted(a))
print 'AZ b: '+str(len(b))
print "\n".join([str(x) for x in b])
print "\n"
# pp.pprint(sorted(b))
print 'AZ c: '+str(len(c))
print "\n".join([str(x) for x in c])
print "\n"
# pp.pprint(sorted(c))
print 'AZ d: '+str(len(d))
print "\n".join([str(x) for x in d])
print "\n"
# pp.pprint(sorted(d))
print 'AZ e: '+str(len(e))
print "\n".join([str(x) for x in e])
print "\n"
# pp.pprint(sorted(e))
