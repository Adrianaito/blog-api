from flask import request, Blueprint, json, Response
from firebase_admin import auth
from flask_cors import cross_origin
from flask import current_app

from src.ext.auth import Auth
from src.ext.db import UserModel, BlogPostModel, UserSchema, BlogPostSchema

blogpost_bp = Blueprint('blogpost', __name__)



@cross_origin()
@blogpost_bp.route('/blogpost', methods=['POST'])
# @limiter.limit("5 per day")
@Auth.check_token
def create():
  """
  Takes in title and contents fields from the request and
  creates a blog post.
  Title and contents are required fields.
  """
  req_data = request.get_json()
  jwt_token = request.headers.get('Authorization')
  decoded_token = auth.verify_id_token(jwt_token)
  email = decoded_token['email']
  user = UserModel.get_user_by_email(email)
  req_data['owner_id'] = user.id

  blogpost_schema = BlogPostSchema()
  data = blogpost_schema.load(req_data)

  post = BlogPostModel(data)
  post.save()
  data = blogpost_schema.dump(post)
  return custom_response(data, 201)


@cross_origin()
@blogpost_bp.route('/blogposts', methods=['GET'])
# @limiter.limit("5 per day")
def get_all():
  """
  Get All Blogposts
  """
  posts = BlogPostModel.get_all_blogposts()
  blogposts_schema = BlogPostSchema(many=True)
  data = blogposts_schema.dump(posts)
  return custom_response(data, 200)


@cross_origin()
@blogpost_bp.route('/blogposts/<int:blogpost_id>', methods=['GET'])
# @limiter.limit("5 per day")
def get_one(blogpost_id):
  """
  Get A Blogpost
  """
  post = BlogPostModel.get_one_blogpost(blogpost_id)
  if not post:
    return custom_response({'error': 'post not found'}, 404)
  blogpost_schema = BlogPostSchema()
  data = blogpost_schema.dump(post)
  return custom_response(data, 200)


@cross_origin()
@blogpost_bp.route('/blogposts/<int:blogpost_id>', methods=['PUT'])
# @limiter.limit("2 per day")
@Auth.check_token
def update(blogpost_id):
  """
  Update A Blogpost.
  """
  req_data = request.get_json()
  post = BlogPostModel.get_one_blogpost(blogpost_id)

  jwt_token = request.headers.get('Authorization')
  decoded_token = auth.verify_id_token(jwt_token)
  email = decoded_token['email']
  user = UserModel.get_user_by_email(email)
  req_data['owner_id'] = user.id
  blogpost_schema = BlogPostSchema()

  if not post:
    return custom_response({'error': 'post not found'}, 404)
  data = blogpost_schema.dump(post)
  if data.get('owner_id') != user.id:
    return custom_response({'error': 'permission denied'}, 400)

  data = blogpost_schema.load(req_data, partial=True)

  post.update(data)

  data = blogpost_schema.dump(post)
  return custom_response(data, 200)


@cross_origin()
@blogpost_bp.route('/blogposts/<int:blogpost_id>', methods=['DELETE'])
# @limiter.limit("2 per day")
@Auth.check_token
def delete(blogpost_id):
  """
  Delete A Blogpost
  """
  jwt_token = request.headers.get('Authorization')
  decoded_token = auth.verify_id_token(jwt_token)
  email = decoded_token['email']
  user = UserModel.get_user_by_email(email)
  post = BlogPostModel.get_one_blogpost(blogpost_id)

  blogpost_schema = BlogPostSchema()

  if not post:
    return custom_response({'error': 'post not found'}, 404)
  data = blogpost_schema.dump(post)
  if data.get('owner_id') != user.id:
    return custom_response({'error': 'permission denied'}, 400)
  try:
    post.delete()
    return custom_response({'message': 'Post deleted!'}, 204)
  except Exception as e:
    return custom_response({'message': 'Something went wrong!'}, 400)


def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
      mimetype="application/json",
      response=json.dumps(res),
      status=status_code
  )
