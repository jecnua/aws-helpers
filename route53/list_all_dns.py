'''
This script can be used to dump all the recordset inside a specific aws account
'''
import boto3


def get_all_hosted_zones(boto_client):
    '''
    TODO
    '''
    response = boto_client.list_hosted_zones()
    return list(map(lambda x: x['Id'], response['HostedZones']))


def filter_by_type(entry):
    '''
    TODO
    '''
    return bool(entry['Type'] in ['CNAME', 'A']) and (bool('ResourceRecords' in entry) or bool('AliasTarget' in entry))


def get_value(data):
    '''
    TODO
    '''
    value = ''
    if 'ResourceRecords' in data:
        value = str(data['ResourceRecords'][0]['Value'])
    if 'AliasTarget' in data:
        value = str(data['AliasTarget']['DNSName'])
    return str(data['Name']) + ' || ' + value


def get_all_recordset(boto_client, identifier):
    '''
    TODO
    '''
    paginator = boto_client.get_paginator('list_resource_record_sets')
    response = paginator.paginate(HostedZoneId=identifier)
    all_result = []
    for record in response:
        filtered = list(filter(filter_by_type, record['ResourceRecordSets']))
        all_result.extend(list(map(get_value, filtered)))
    return all_result


def main():
    '''
    TODO
    '''
    client = boto3.client('route53')
    results = list(map(lambda x: get_all_recordset(client, x), get_all_hosted_zones(client)))
    list(map(lambda x: print('\n'.join(x)), results))

main()
