#!/usr/bin/env python
import boto3
import pprint

'''
TODO: Expand to support elbv2
'''

pp = pprint.PrettyPrinter(indent=4)
client = boto3.client('elb', region_name='us-east-1')
response = client.describe_load_balancers(
    PageSize=400
)
all_elb = response['LoadBalancerDescriptions']
for single_elb in all_elb:
    for a_listener in single_elb["ListenerDescriptions"]:
        if 'SSLCertificateId' in a_listener["Listener"]:
            print(single_elb["LoadBalancerName"] + "\t\t" +
                  a_listener["Listener"]["SSLCertificateId"])
