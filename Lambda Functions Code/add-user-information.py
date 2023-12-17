import json
import boto3
import urllib3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    #receive information from frontend
    #event = {'resource': '/uploadUser', 'path': '/uploadUser', 'httpMethod': 'POST', 'headers': {'accept': 'application/json', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en-US,en;q=0.9', 'content-type': 'application/json', 'Host': 'yjymyndpu1.execute-api.us-east-1.amazonaws.com', 'origin': 'http://finalproject.signup.s3-website-us-east-1.amazonaws.com', 'referer': 'http://finalproject.signup.s3-website-us-east-1.amazonaws.com/', 'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'cross-site', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36', 'X-Amzn-Trace-Id': 'Root=1-6554e16d-7213299c3c170f222d62ed14', 'X-Forwarded-For': '198.13.90.32', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'}, 'multiValueHeaders': {'accept': ['application/json'], 'accept-encoding': ['gzip, deflate, br'], 'accept-language': ['en-US,en;q=0.9'], 'content-type': ['application/json'], 'Host': ['yjymyndpu1.execute-api.us-east-1.amazonaws.com'], 'origin': ['http://finalproject.signup.s3-website-us-east-1.amazonaws.com'], 'referer': ['http://finalproject.signup.s3-website-us-east-1.amazonaws.com/'], 'sec-ch-ua': ['"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"'], 'sec-ch-ua-mobile': ['?0'], 'sec-ch-ua-platform': ['"Windows"'], 'sec-fetch-dest': ['empty'], 'sec-fetch-mode': ['cors'], 'sec-fetch-site': ['cross-site'], 'User-Agent': ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'], 'X-Amzn-Trace-Id': ['Root=1-6554e16d-7213299c3c170f222d62ed14'], 'X-Forwarded-For': ['198.13.90.32'], 'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https']}, 'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'pathParameters': None, 'stageVariables': None, 'requestContext': {'resourceId': '1smxtk', 'resourcePath': '/uploadUser', 'operationName': 'uploadUser', 'httpMethod': 'POST', 'extendedRequestId': 'OcgpHE1IoAMEuIQ=', 'requestTime': '15/Nov/2023:15:19:09 +0000', 'path': '/test/uploadUser', 'accountId': '936225711085', 'protocol': 'HTTP/1.1', 'stage': 'test', 'domainPrefix': 'yjymyndpu1', 'requestTimeEpoch': 1700061549293, 'requestId': 'c377efad-3bfd-46c2-bb5d-5b8787c2c6d2', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '198.13.90.32', 'principalOrgId': None, 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36', 'user': None}, 'domainName': 'yjymyndpu1.execute-api.us-east-1.amazonaws.com', 'apiId': 'yjymyndpu1'}, 'body': '{"information":"test ,test ,Fort Leonard Wood ,test1 ,1234"}', 'isBase64Encoded': False}
    information_string = event['body']
    cleaned_information_string = information_string.split(':')[1][1:-2]
    information_list = cleaned_information_string.split(',')
    print(information_list)
    #insert username and password into dynamoDB
    data_list = []
    data = {}
    data['username'] = information_list[3]
    data['firstname'] = information_list[0]
    data['lastname'] = information_list[1]
    data['base'] = information_list[2]
    data['password'] = information_list[4]
    data_list.append(data)
    insert_data(data_list)
    
    #return response to frontend
    resp = {
        'headers': { 'Access-Control-Allow-Origin': '*'},
        'statusCode': 200,
        'body': json.dumps({})
        }
    return(resp)


def insert_data(data_list, db=None, table='user-information'):
    if not db:
        db = boto3.resource('dynamodb')
    table = db.Table(table)
    # overwrite if the same index is provided
    for data in data_list:
        response = table.put_item(Item=data)
    print('@insert_data: response', response)
    return response