Lambda Code README

search-user-information.py
 - about: is triggered when when the API GET call /searchUsers is made to search for user information
 - input: event from the frontend containing username
 - features: searches the DynamoDB table called user-information based on the provided username
 - returns: a dictonary of user information such as username, password, firstname, lastname, and base

search-posts.py
 - about: is triggered when when the API GET call /searchPosts is made to search for post information
 - input: event from the frontend containing query
 - features: searches both OpenSearch indicies, posts and photos, to find posts that have descriptions matching the query. If this is called from a users feed, the query is based on the username of the user. Based on this username, the DynamoDB table called liked-posts is searched to obtain liked posts, and recommended posts based on a machine learning algorithm or text similarity are returned. If this is called from a users search query, the query is disseminated using lex and posts and photos in OpenSearch are returned that have a matching terms to the query. If this is called when a user views their profile posts are returned that were created by that user's username.
- functions:
	query_username(username): queries the OpenSearch index posts and returns all posts with that username in the username field
	query_all(): returns all posts in the OpenSearch index posts
	query_base(base): queries the OpenSearch index posts and returns all posts with that base in the base field
	query_username_time(username_time): queries the OpenSearch index posts and returns all posts with that username_time in the username_time field *username_time is used as a key in this index
	query_posts(term): queries the OpenSearch index posts and returns all posts with that term in the labels or tags field
	query_photos_by_user(username_time): queries the OpenSearch index photos and returns all photos with the provided username_time as a key
	query_photos(term): queries the OpenSearch index photos and returns all posts with the term in the labels field
	lookup_data(key, table, db=None): queries the provided DynamoDB table and returns the item with the associated key 
 - returns: a dictonary of post information such as username, base, caption, tags, photo url, username_time, and liked

add-user-information.py
 - about: is triggered when when the API POST call /uploadUser is made to upload a user's information
 - input: event from the frontend
 - features: obtains all required information sent from the frontend and adds it to the DynamoDB table called user-information
 - returns: a status 200 code

add-post-photo.py
 - about: is triggered when when the API POST call /uploadPhoto/{bucket}/{key} uploads a photo to the S3 bucket
 - features: gets the photo from the S3 bucket, sends it to Amazon Rekognition to get labels, and adds it to the OpenSearch index photos

add-post-content.py
 - about: is triggered when when the API POST call /uploadPostContent is made to upload a post's information
 - input: event from the frontend
 - features: obtains all required information sent from the frontend and adds it to the OpenSearch index called photos
 - returns: a status 200 code

add-like.py
 - about: is triggered when when the API POST call /uploadLike is made to upload a like that a user made
 - input: event from the frontend
 - features: obtains all required information sent from the frontend about the user and the post that they liked and updates the DynamoDB table called liked-posts to reflect the new post that they liked
 - returns: a status 200 code