import json
import boto3
import urllib3
import random
import os
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    entered_username = event['queryStringParameters']['q']
    print(entered_username)
    username_results = lookup_data({'username': entered_username})
    print(username_results)
    
    if username_results != None:
        username = username_results['username']
        password = username_results['password']
        firstname = username_results['firstname']
        lastname = username_results['lastname']
        base = username_results['base']
        results_entry = {"username" : username, "password": password, "firstname": firstname, "lastname": lastname, "base": base}
    else:
        username = 'None'
        results_entry = {"username" : username}
    
    body = {"results": results_entry}
    
    resp = {
            'headers': { 'Access-Control-Allow-Origin': '*', 'X-Api-Key': 'KVxqSUcSJn5AjNPQlx8f2aaDmq75wksiby98PCE1'},
            'statusCode': 200,
            'body': json.dumps(body)
            }
    
    
    return(resp)
    
    
def lookup_data(key, db=None, table='user-information'):
    if not db:
        db = boto3.resource('dynamodb')
    table = db.Table(table)
    try:
        response = table.get_item(Key=key)
        if "Item" not in response.keys():
            resp = None
        else:
            resp = response["Item"]
    except ClientError as e:
        print('Error', e.response['Error']['Message'])
    else:
        return resp