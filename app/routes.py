from flask import request
from . import app
from fakeData.posts import post_data


# Define a route
@app.route("/")
def index():
    first_name = 'Garren'
    age = 123
    return 'Hello ' + first_name + ' who is ' + str(age) + ' years old'

# post endpoints

# get all posts
@app.route('/posts')
def getposts():
    # get the posts from storage (fake data -> tomorrow will be db)
    posts = post_data
    return posts


# get single post by ID
@app.route('/posts/<int:post_id>')
def getpost(post_id):
    posts = post_data
    # for each dict in the list of post dicts
    for post in posts:
        # if the key of id matches the post id from the url
        if post['id'] == post_id:
            # return that post from the dict
            return post
    # if we loop through all the posts without returning the post with that id does not exist

    return {'Error': f'post of {post_id} does not exist'}, 404

# create a post
@app.route('/posts', methods=['POST'])
def create_post():
    # Check to see if the request body is JSON
    if not request.is_json:
        return {'error': 'Your content-type must be application/json'}, 400
    # Get the data from the request body
    data = request.json
    # Validate the incoming data
    required_fields = ['title', 'body']
    missing_fields = []
    # For each of the required fields
    for field in required_fields:
        # If the field is not in the request body dictionary
        if field not in data:
            # Add that field to the list of missing fields
            missing_fields.append(field)
    # If there are any missing fields, return 400 status code with the missin
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400
   
    # Get data values
    title = data.get('title')
    body = data.get('body')

    # Create a new post dictionary with data
    newpost = {
        'id': len(post_data) + 1,
        'title': title,
        'body': body,
        'userId': 1,
        'dateCreated': '2024-03-25T15:21:35',
        'likes': 0
    }

    # Add the new post to storage (post_data -> will be db tomorrow)
    post_data.append(newpost)
    
    # Return the newly created post dictionary with a 201 Created Status Code
    return newpost, 201

