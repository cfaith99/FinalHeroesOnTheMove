import json
import boto3
import urllib3
import random
import os
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from botocore.exceptions import ClientError
from datauri import DataURI
import zlib
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
import numpy as np
import math
import random

REGION = 'us-east-1'
POST_HOST = 'search-content-posts-2gxv2gmnkmz3jb6ygn4zlu3pqm.us-east-1.es.amazonaws.com'
PHOTO_HOST = 'search-photos-post-3h5gv4mnatvwhr7xfpy3nvcojq.us-east-1.es.amazonaws.com'
POST_INDEX = 'post'
PHOTO_INDEX = 'photos'

lex = boto3.client('lexv2-runtime')
s3 = boto3.client('s3')
username = ""

def lambda_handler(event, context):
    q = event['multiValueQueryStringParameters']['q'][0]
    q_type = q.split(":")[0]
    
    #search for users own posts
    if q_type == 'username':
        username = q.split(":")[1].strip()
        results = query_username(username)
    #get 
    elif q_type == 'home':
        username = q.split(":")[1].strip()
        try:
        #get liked posts
            liked_posts = lookup_data({'username': username}, 'liked-posts')['liked_posts']
            #base = lookup_data({'username': username}, 'user-information')['base']
            #base = base[5:]
            #base_posts = query_base(base)
            all_posts = query_all()
            #get labels of posts
            x = []
            y = []
            length = []
            for like in liked_posts:
                post_info = []
                post = query_username_time(like)[0]
                photo = query_photos_by_user(like)[0]
                post_labels = post['labels'][1:-1].split(',')
                for pst in post_labels:
                    post_info.append( pst.strip()[1:-1])
                post_tags = post['tags'][1:-1].split(',')
                for pst in post_tags:
                    post_info.append( pst.strip()[1:-1])
                photo_labels = photo['lables'][1:-1].split(',')
                for pst in photo_labels:
                    post_info.append( pst.strip()[1:-1])
                print(post_info)
                length.append(len(post_info))
                x.append(post_info)
                y.append(1)
            for post in all_posts:
                post_id = post['username_time']
                if post_id not in liked_posts:
                    post_info = []
                    check_photo = query_photos_by_user(post_id)
                    if check_photo != []:
                        photo = check_photo[0]
                        post_labels = post['labels'][1:-1].split(',')
                        for pst in post_labels:
                            post_info.append( pst.strip()[1:-1])
                        post_tags = post['tags'][1:-1].split(',')
                        for pst in post_tags:
                            post_info.append( pst.strip()[1:-1])
                        photo_labels = photo['lables'][1:-1].split(',')
                        for pst in photo_labels:
                            post_info.append( pst.strip()[1:-1])
                        print(post_info)
                        length.append(len(post_info))
                        x.append(post_info)
                        y.append(-1)

            train_number = math.ceil(len(x)*0.8)
            test_number = len(x) - train_number
            train_indices = []
            min_len = min(length)
    
            while len(train_indices) < train_number:
                index = random.randint(0, len(x)-1)
                if index not in train_indices:
                    train_indices.append(index)

            train_x = []
            train_y = []
            min_length = []
            for index in train_indices:
                vectorizer = CountVectorizer()
                x_post = x[index]
                x_post_stg = ' '.join(x_post)
                trans = vectorizer.fit_transform([x_post_stg])
                arr_trans = trans.toarray()
                print(np.array(arr_trans[0]))
                train_x.append(arr_trans[0])
                min_length.append(len(arr_trans[0]))
                y_value = y[index]
                #y_list = np.array([y_value for i in range(0, len(arr_trans[0]))])
                #print(y_list)
                train_y.append(y_value)
            
            minimum = min(min_length)
            final_train_x = []
            for data in train_x:
                final_train_x.append(data[:minimum])
        
            classifer = SGDClassifier()
            classifer.fit(final_train_x, train_y)
        
            results = []
            for post in all_posts:
                post_id = post['username_time']
                post_info = []
                check_photo = query_photos_by_user(post_id)
                if check_photo != []:
                    photo = check_photo[0]
                    post_labels = post['labels'][1:-1].split(',')
                    for pst in post_labels:
                        post_info.append( pst.strip()[1:-1])
                    post_tags = post['tags'][1:-1].split(',')
                    for pst in post_tags:
                        post_info.append( pst.strip()[1:-1])
                    photo_labels = photo['lables'][1:-1].split(',')
                    for pst in photo_labels:
                        post_info.append( pst.strip()[1:-1])
                    print(post_info)
                    vectorizer = CountVectorizer()
                    post_stg = ' '.join(post_info)
                    trans = vectorizer.fit_transform([post_stg])
                    arr_trans = trans.toarray()
                    adjusted = arr_trans[0][:minimum].reshape(1, -1)
                    y_predict = classifer.predict(adjusted)
                    if y_predict[0] == 1:
                        if post_id not in liked_posts:
                            results.append(post)
            if len(results) <= 5:
                raise Exception("Sorry, no numbers below zero")        
        except Exception as e:
            print(e)
            try:
                print('in compare words')
                results=[]
                like_words = []
                for like in liked_posts:
                    post_info
                    post = query_username_time(like)[0]
                    photo = query_photos_by_user(like)[0]
                    post_labels = post['labels'][1:-1].split(',')
                    for pst in post_labels:
                        post_info.append( pst.strip()[1:-1])
                    post_tags = post['tags'][1:-1].split(',')
                    for pst in post_tags:
                        post_info.append( pst.strip()[1:-1])
                    photo_labels = photo['lables'][1:-1].split(',')
                    for pst in photo_labels:
                        post_info.append( pst.strip()[1:-1])
                    for word in post_info:
                        if word not in like_words:
                            like_words.append(word)
                    print('like words' + str(like_words))
                for post in all_posts:
                    post_id = post['username_time']
                    post_info = []
                    check_photo = query_photos_by_user(post_id)
                    if check_photo != []:
                        photo = check_photo[0]
                        post_labels = post['labels'][1:-1].split(',')
                        for pst in post_labels:
                            post_info.append( pst.strip()[1:-1])
                        post_tags = post['tags'][1:-1].split(',')
                        for pst in post_tags:
                            post_info.append( pst.strip()[1:-1])
                        photo_labels = photo['lables'][1:-1].split(',')
                        for pst in photo_labels:
                            post_info.append( pst.strip()[1:-1])
                        print(post_info)
                    count = 0
                    for word in post_info:
                        if word in like_words:
                            count += 1
                    if count >= len(post_info)*0.6 and post_id not in liked_posts and post['username'] != 'carly':
                        results.append(post)
                if len(results) < 1:
                    raise Exception("Sorry, no numbers below zero")
            except Exception as e:
                print(e)
                print('in base')
                base = lookup_data({'username': username}, 'user-information')['base']
                base = base[5:]
                results = query_base(base)
    #search based on query
    else:
        username = q.split(":")[2].split("=")[1].strip()
        response = lex.recognize_text(
                botId='NV0VVVPCOC',
                botAliasId='TSTALIASID',
                localeId='en_US',
                sessionId='testuser',
                text=q.split(":")[1].strip()
            )
        searchTerms = response['sessionState']['intent']['slots']
        searchTerm1 = searchTerms['searchTerm1']['value']['resolvedValues'][0]
        if searchTerms['searchTerm2'] != None:
            searchTerm2 = searchTerms['searchTerm2']['value']['resolvedValues'][0]
        else:
            searchTerm2 = None
    
        if searchTerm1[-1] == 's':
            searchTerm1 = searchTerm1[:-1]
        if searchTerm2 != None and searchTerm2[-1] == 's':
            searchTerm2 = searchTerm2[:-1]
        q = str(searchTerm1)
        if searchTerm2 != None:
            q = q + ' AND ' + str(searchTerm2)
        #post results
        post_results = query_posts(q)

        #photo results
        photo_results = query_photos(q)
        
        results = []
        used_username_time = []
        for result in post_results:
            username_time = result['username_time']
            if username_time not in used_username_time:
                used_username_time.append(username_time)
                results.append(result)
        for result in photo_results:
            username_time = result['objectKey'].split(".")[0]
            if username_time not in used_username_time:
                used_username_time.append(username_time)
                results.append(result)
        
    innerBody = []
    like_results = []
    try:
        like_results = lookup_data({'username': username},'liked-posts')['liked_posts']
    except Exception as e:
        print(e)
    
    print(like_results)
    for result in results:
        if 'username_time' in result.keys():
            username_time = result['username_time']
        else:
            username_time = result['objectKey'].split(".")[0]
            posts = query_username_time(username_time)
            if posts == []:
                continue
            else:
                result = posts[0]
        photo_results = query_photos_by_user(username_time)
        
        #check if post is liked
        liked = False
        if username_time in like_results:
            liked = True
            
        #post information
        username = result['username']
        base = result['base']
        caption = result['caption']
        tags = result['tags']
        
        if photo_results != []:
            #picture information
            key = photo_results[0]['objectKey']
            bucket = photo_results[0]['bucket']
            
            try:
                url = "https://s3.amazonaws.com/finalproject.postpictures/" + key
            except Exception as e:
                url = ""
                print(e)
        else:
            url = ""
        resultEntry = {"username": username, "base": base, "caption": caption, "tags": tags, "url" : url, "username_time": username_time, 'liked': liked}
        innerBody.append(resultEntry)

    body = {"results": innerBody}
    
    resp = {
            'headers': { 'Access-Control-Allow-Origin': '*'},
            'statusCode': 200,
            'body': json.dumps(body)
            }
    print(resp)
    return(resp)
    
    

def query_username(username):
    q = {'query': {'query_string': {'query': username, 'fields': ['username']}}}
    client = OpenSearch(hosts=[{
        'host': POST_HOST,
        'port': 443
    }],
        http_auth=get_awsauth(REGION, 'es'),
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection)

    res = client.search(index=POST_INDEX, body=q)

    hits = res['hits']['hits']
    results = []
    for hit in hits:
        results.append(hit['_source'])

    return results

def query_all():
    q = {'query': {'match_all':{}}}
    client = OpenSearch(hosts=[{
        'host': POST_HOST,
        'port': 443
    }],
        http_auth=get_awsauth(REGION, 'es'),
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection)

    res = client.search(index=POST_INDEX, body=q)

    hits = res['hits']['hits']
    results = []
    for hit in hits:
        results.append(hit['_source'])

    return results

def query_base(base):
    q = {'query': {'query_string': {'query': base, 'fields': ['base']}}}
    client = OpenSearch(hosts=[{
        'host': POST_HOST,
        'port': 443
    }],
        http_auth=get_awsauth(REGION, 'es'),
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection)

    res = client.search(index=POST_INDEX, body=q)

    hits = res['hits']['hits']
    results = []
    for hit in hits:
        results.append(hit['_source'])

    return results

def query_username_time(username_time):
    q = {'query': {'query_string': {'query': username_time, 'fields': ['username_time']}}}
    client = OpenSearch(hosts=[{
        'host': POST_HOST,
        'port': 443
    }],
        http_auth=get_awsauth(REGION, 'es'),
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection)

    res = client.search(index=POST_INDEX, body=q)

    hits = res['hits']['hits']
    results = []
    for hit in hits:
        results.append(hit['_source'])

    return results

def query_posts(term):
    q = {'query': {'query_string': {'query': term, 'fields': ['labels', 'tags']}}}
    client = OpenSearch(hosts=[{
        'host': POST_HOST,
        'port': 443
    }],
        http_auth=get_awsauth(REGION, 'es'),
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection)

    res = client.search(index=POST_INDEX, body=q)

    hits = res['hits']['hits']
    results = []
    for hit in hits:
        results.append(hit['_source'])

    return results
    
def query_photos_by_user(username_time):
    q = {'query': {'query_string': {'query': username_time, 'fields': ['objectKey']}}}
    client = OpenSearch(hosts=[{
        'host': PHOTO_HOST,
        'port': 443
    }],
        http_auth=get_awsauth(REGION, 'es'),
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection)

    res = client.search(index=PHOTO_INDEX, body=q)

    hits = res['hits']['hits']
    results = []
    for hit in hits:
        results.append(hit['_source'])

    return results
    
def query_photos(term):
    q = {'query': {'query_string': {'query': term, 'fields': ['lables']}}}
    client = OpenSearch(hosts=[{
        'host': PHOTO_HOST,
        'port': 443
    }],
        http_auth=get_awsauth(REGION, 'es'),
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection)

    res = client.search(index=PHOTO_INDEX, body=q)

    hits = res['hits']['hits']
    results = []
    for hit in hits:
        results.append(hit['_source'])

    return results

def get_awsauth(region, service):
    cred = boto3.Session().get_credentials()
    return AWS4Auth(cred.access_key,
        cred.secret_key,
        region,
        service,
        session_token=cred.token)

def lookup_data(key, table, db=None):
    if not db:
        db = boto3.resource('dynamodb')
    table = db.Table(table)
    try:
        print(table)
        response = table.get_item(Key=key)
    except ClientError as e:
        print('Error', e.response['Error']['Message'])
    else:
        print(response['Item'])
        return response['Item']
    