import json
import urllib.parse
import boto3
from requests_aws4auth import AWS4Auth
import urllib3
from opensearchpy import OpenSearch, RequestsHttpConnection
import base64
from string import punctuation
from collections import Counter

opensearch = boto3.client('opensearch')

region = 'us-east-1'
host = 'search-content-posts-2gxv2gmnkmz3jb6ygn4zlu3pqm.us-east-1.es.amazonaws.com'

def lambda_handler(event, context):
    #receive information from frontend
    #event = {'resource': '/uploadUser', 'path': '/uploadUser', 'httpMethod': 'POST', 'headers': {'accept': 'application/json', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en-US,en;q=0.9', 'content-type': 'application/json', 'Host': 'yjymyndpu1.execute-api.us-east-1.amazonaws.com', 'origin': 'http://finalproject.signup.s3-website-us-east-1.amazonaws.com', 'referer': 'http://finalproject.signup.s3-website-us-east-1.amazonaws.com/', 'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'cross-site', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36', 'X-Amzn-Trace-Id': 'Root=1-6554e16d-7213299c3c170f222d62ed14', 'X-Forwarded-For': '198.13.90.32', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'}, 'multiValueHeaders': {'accept': ['application/json'], 'accept-encoding': ['gzip, deflate, br'], 'accept-language': ['en-US,en;q=0.9'], 'content-type': ['application/json'], 'Host': ['yjymyndpu1.execute-api.us-east-1.amazonaws.com'], 'origin': ['http://finalproject.signup.s3-website-us-east-1.amazonaws.com'], 'referer': ['http://finalproject.signup.s3-website-us-east-1.amazonaws.com/'], 'sec-ch-ua': ['"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"'], 'sec-ch-ua-mobile': ['?0'], 'sec-ch-ua-platform': ['"Windows"'], 'sec-fetch-dest': ['empty'], 'sec-fetch-mode': ['cors'], 'sec-fetch-site': ['cross-site'], 'User-Agent': ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'], 'X-Amzn-Trace-Id': ['Root=1-6554e16d-7213299c3c170f222d62ed14'], 'X-Forwarded-For': ['198.13.90.32'], 'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https']}, 'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'pathParameters': None, 'stageVariables': None, 'requestContext': {'resourceId': '1smxtk', 'resourcePath': '/uploadUser', 'operationName': 'uploadUser', 'httpMethod': 'POST', 'extendedRequestId': 'OcgpHE1IoAMEuIQ=', 'requestTime': '15/Nov/2023:15:19:09 +0000', 'path': '/test/uploadUser', 'accountId': '936225711085', 'protocol': 'HTTP/1.1', 'stage': 'test', 'domainPrefix': 'yjymyndpu1', 'requestTimeEpoch': 1700061549293, 'requestId': 'c377efad-3bfd-46c2-bb5d-5b8787c2c6d2', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '198.13.90.32', 'principalOrgId': None, 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36', 'user': None}, 'domainName': 'yjymyndpu1.execute-api.us-east-1.amazonaws.com', 'apiId': 'yjymyndpu1'}, 'body': '{"information":"test ,test ,Fort Leonard Wood ,test1 ,1234"}', 'isBase64Encoded': False}
    information_string = event['body']
    cleaned_information_string = information_string.split(':')[1][1:-2]
    information_list = cleaned_information_string.split(',')
    #information_list = ['"carly1700434112876"', '"carly"', '"elephant.png"', '"wow* this trip to the zoo was amazing. The elephant was so big!"', '"Fort Knox"', '"#zoo/ #elephant"']
    print(information_list)
    
    #insert username and password into dynamoDB
    username_time = information_list[0][1:-1]
    username = information_list[1][1:-1]
    caption = information_list[3][1:-1].replace("*", ",")
    base = information_list[4][1:-1]
    sent_tags = information_list[5][1:-1].split("/")
    tags = []
    for tag in sent_tags:
        tag = tag.strip()
        if tag[0] == '#':
            tags.append(tag[1:])
        else:
            tags.append(tag)
    
    #get caption labels
    labels = get_labels(caption)
    print(labels)
    
    #add to opensearch
    add_data(username_time, username, base, caption, tags, labels)
    
    #return response to frontend
    resp = {
        'headers': { 'Access-Control-Allow-Origin': '*'},
        'statusCode': 200,
        'body': json.dumps({})
        }
    return(resp)
    
def get_labels(caption):
    # Stop words
    STOP_WORDS = set(
        """
    a about above across after afterwards again against all almost alone along
    already also although always am among amongst amount an and another any anyhow
    anyone anything anyway anywhere are around as at
    
    back be became because become becomes becoming been before beforehand behind
    being below beside besides between beyond both bottom but by
    
    call can cannot ca could
    
    did do does doing done down due during
    
    each eight either eleven else elsewhere empty enough even ever every
    everyone everything everywhere except
    
    few fifteen fifty first five for former formerly forty four from front full
    further
    
    get give go
    
    had has have he hence her here hereafter hereby herein hereupon hers herself
    him himself his how however hundred
    
    i if in indeed into is it its itself
    
    keep
    
    last latter latterly least less
    
    just
    
    made make many may me meanwhile might mine more moreover most mostly move much
    must my myself
    
    name namely neither never nevertheless next nine no nobody none noone nor not
    nothing now nowhere
    
    of off often on once one only onto or other others otherwise our ours ourselves
    out over own
    
    part per perhaps please put
    
    quite
    
    rather re really regarding
    
    same say see seem seemed seeming seems serious several she should show side
    since six sixty so some somehow someone something sometime sometimes somewhere
    still such
    
    take ten than that the their them themselves then thence there thereafter
    thereby therefore therein thereupon these they third this those though three
    through throughout thru thus to together too top toward towards twelve twenty
    two
    
    under until up unless upon us used using
    
    various very very via was we well were what whatever when whence whenever where
    whereafter whereas whereby wherein whereupon wherever whether which while
    whither who whoever whole whom whose why will with within without would
    
    yet you your yours yourself yourselves
    """.split()
    )

    contractions = ["n't", "'d", "'ll", "'m", "'re", "'s", "'ve"]
    STOP_WORDS.update(contractions)
    caption_text = caption.split(" ")
    
    for apostrophe in ["‘", "’"]:
        for stopword in contractions:
            STOP_WORDS.add(stopword.replace("'", apostrophe))
    
    keyword = []
    stopwords = list(STOP_WORDS)
    for word in caption_text:
        if word[-1] in punctuation:
            word = word[:-1]
        if(word.lower() in stopwords or word in punctuation):
            continue
        else:
            keyword.append(word.lower())
    freq_word = Counter(keyword)
    labels = []
    for word in freq_word.most_common(5):
        labels.append(word[0])
    return labels

def add_data(username_time, username, base, caption, tags, labels):
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
        #response3 = client.indices.create('post')
        #print('\nCreating index:')
        #print(response3)
    
        # Add a document to the index.
        response4 = client.index(
            index='post',
            body={
                'username_time': str(username_time),
                'username': str(username),
                'base': str(base),
                'caption': str(caption),
                'tags': str(tags),
                'labels': str(labels)
                },
            id=str(username_time),
        )
        print('added')
        print(response4)
    except Exception as e:
        print(e)
        raise(e)
        
def get_awsauth(region, service):
    cred = boto3.Session().get_credentials()
    return AWS4Auth(cred.access_key,
                    cred.secret_key,
                    region,
                    service,
                    session_token=cred.token)
    