#!/usr/bin/env python
import boto3

'''
Will list all ELB and ALB listener with SSL cert arn
Python3
'''

def _find_certs_elb(region_name='us-east-1'):
    client = boto3.client('elb', region_name=region_name)
    response = client.describe_load_balancers(
        PageSize=400
    )
    all_elb = response['LoadBalancerDescriptions']
    for single_elb in all_elb:
        for a_listener in single_elb["ListenerDescriptions"]:
            if 'SSLCertificateId' in a_listener["Listener"]:
                # print(a_listener)
                # exit(0)
                padded_name = '{:<32}'.format(single_elb["LoadBalancerName"])
                print("ELB : " + padded_name + " : (" + str(a_listener["Listener"]["LoadBalancerPort"]) + ") " +
                      a_listener["Listener"]["SSLCertificateId"])

# http://boto3.readthedocs.io/en/latest/reference/services/elbv2.html
def _find_cers_alb(region_name='us-east-1'):
    client = boto3.client('elbv2', region_name=region_name)
    response = client.describe_load_balancers(
        PageSize=400
    )
    for lb in response['LoadBalancers']:
        arn = lb['LoadBalancerArn']
        name = lb['LoadBalancerName']
        listeners = client.describe_listeners(LoadBalancerArn=arn)
        for a_listener in listeners['Listeners']:
            if 'Certificates' in a_listener:
                for a_cert in a_listener['Certificates']:
                    cert_arn = a_cert['CertificateArn']
                    prot = a_listener['Port']
                    print("ALB : " + name + " : (" + str(prot) + ") " + cert_arn)


_find_certs_elb()
print("==============================")
_find_certs_elb(region_name='eu-west-1')
print("==============================")
_find_cers_alb()
print("==============================")
_find_cers_alb(region_name='eu-west-1')
