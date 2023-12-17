APIGateway Swagger File

Main Paths:
- searchPosts: is a GET call to search posts based on a user defined query and returns a status 200 code upon success

- searchUsers: is a GET call to search users based on a user defiend query and returns a status 200 code upon success

- uploadLike: is a POST call that sends a list of information about the liked post and returns a status 200 code upon success

- uploadPhoto/{bucket}/{key}: is a PUT call that uploads the provided photo to the specifed S3 bucket with the given key and returns a status 200 code upon success

- uploadPostContent: is a POST call that sends a list of information about a post and returns a status 200 code upon success

- uploadUser: is a POST call that sends a list of information about a user and returns a status 200 code upon success