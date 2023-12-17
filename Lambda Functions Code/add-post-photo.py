import json
import urllib.parse
import boto3
from requests_aws4auth import AWS4Auth
import urllib3
from opensearchpy import OpenSearch, RequestsHttpConnection
import base64
from datauri import DataURI

http = urllib3.PoolManager()

s3 = boto3.client('s3')
rek = boto3.client('rekognition')
opensearch = boto3.client('opensearch')

region = 'us-east-1'
host = 'search-photos-post-3h5gv4mnatvwhr7xfpy3nvcojq.us-east-1.es.amazonaws.com'

def lambda_handler(event, context):
    # Get the object from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    labels = []
    
    try:
        response3 = s3.get_object(Bucket=bucket, Key=key)
        picture64 = response3['Body'].read().decode('utf-8')
        print(picture64)
        #picture = base64.b64decode(picture64 + b'==')
        #picture_data = picture64.decode('utf-8')
        #picture_data = base64.b64decode(bytes(picture64,'utf-8'), validate=True)
        picture_data = DataURI(picture64)
        picture_data = picture_data.data
        
        detect_response = rek.detect_labels(Image = {'Bytes': picture_data}, MaxLabels= 5, Features=['GENERAL_LABELS'])
        for label in detect_response['Labels']:
            labels.append(label['Name'].lower())
    except Exception as e:
        print(e)
        raise(e)
    
    json_string = '{"objectKey": "' + str(key) + '", "bucket": "' + str(bucket) + '", "labels": ' + str(labels) + '}'
    print(json_string)
    try:
        # Build the OpenSearch client
        client = OpenSearch(
            hosts=[{'host': host, 'port': 443}],
            http_auth=get_awsauth(region, 'es'),
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection
        )
        # It can take up to a minute for data access rules to be enforced
        #time.sleep(45)

        # Create index
        #response3 = client.indices.create('photos')
        #print('\nCreating index:')
        #print(response3)
    
        # Add a document to the index.
        response4 = client.index(
            index='photos',
            body={
                'objectKey': str(key),
                'bucket': str(bucket),
                'lables': str(labels)
                },
            id=str(key),
        )
        print('add picture')
        print(response4)
    except Exception as e:
        print(e)
        raise(e)
    return

#def detect_labels(bucket, key):
 #   response = rek.detect_labels(
  #  Image={
   #     'S3Object': {
    #        'Bucket': bucket,
     #       'Name': key
      #  }},
    #MaxLabels=5,
    #Features=[
    #    'GENERAL_LABELS'
    #])
    #return response
    
def get_awsauth(region, service):
    cred = boto3.Session().get_credentials()
    return AWS4Auth(cred.access_key,
                    cred.secret_key,
                    region,
                    service,
                    session_token=cred.token)
