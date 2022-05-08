from flask import request, json, Response, Blueprint, jsonify
from flask_cors import cross_origin
from flask import current_app
from firebase_admin import credentials, auth
import firebase_admin
import pyrebase

from src.ext.auth import Auth
from src.ext.db import UserModel, BlogPostModel,  BlogPostSchema, UserSchema


user_bp = Blueprint('user', __name__)


cred = credentials.Certificate('fbAdminConfig.json')
firebase = firebase_admin.initialize_app(cred)
pb = pyrebase.initialize_app(json.load(open('fbconfig.json')))


@user_bp.route('/', methods=['POST'])
# @limiter.limit("2 per day")
def create():
  """
  Create User Function
  Saves User to db
  Returns JWT token from firebase
  """
  req_data = request.get_json()
#   data = user_schema.load(req_data)
  password = req_data.get('password')
  email = req_data.get('email')

  # check if user already exist in the db
  user_in_db = UserModel.get_user_by_email(email)
  if user_in_db:
    return custom_response({'error': 'User already exist, please supply another email address'}, 400)
  try:
    user = auth.create_user(
        email=email,
        password=password
    )
    user = UserModel(req_data)
    user.save()
    print("saving user")
  except Exception as error:
    print(error, type(error))
    return custom_response({'message': "Email already exists"}, 400)

#   user_data = user_schema.dump(user)
  user_pb = pb.auth().sign_in_with_email_and_password(email, password)
  jwt = user_pb['idToken']

  return custom_response({'jwt_token': jwt}, 201)


@cross_origin()
@user_bp.route('/', methods=['GET'])
# @limiter.limit("2 per day")
@Auth.check_token
def get_all():
  '''
  Gets all users from the database
  '''
  users = UserModel.get_all_users()
  print(users)
  user_schema = UserSchema(many=True)
  all_users = user_schema.dump(users)
  print("all users",all_users)
  return jsonify(all_users, 200)


@cross_origin()
@user_bp.route('/login', methods=['POST'])
# @limiter.limit("2 per day")
def login():
  '''
  Takes in email and password and returns a JWT token
  '''
  req_data = request.get_json()
#   data = user_schema.load(req_data, partial=True)
  password = req_data.get('password')
  email = req_data.get('email')

  if not req_data.get('email') or not req_data.get('password'):
    return custom_response({'error': 'you need email and password to sign in'}, 400)
  user = UserModel.get_user_by_email(req_data.get('email'))

  if not user:
    return custom_response({'error': 'email not found'}, 400)

#   user_data = user_schema.dump(user)
  try:
    user_pb = pb.auth().sign_in_with_email_and_password(email, password)
    jwt = user_pb['idToken']
  except:
    return custom_response({'error': 'invalid credentials'}, 400)

  return custom_response({'jwt_token': jwt}, 200)


@cross_origin()
@user_bp.route('/<int:user_id>', methods=['GET'])
# @limiter.limit("2 per day")
@Auth.check_token
def get_a_user(user_id):
  """
  Get a single user
  """
  user = UserModel.get_one_user(user_id)
  if not user:
    return custom_response({'error': 'user not found'}, 404)
  user_schema = UserSchema()
  one_user = user_schema.dump(user)
  return custom_response(one_user, 200)

@cross_origin()
@user_bp.route('/me', methods=['DELETE'])
# @limiter.limit("2 per day")
@Auth.check_token
def delete():
  """
  Delete a user
  """
  jwt_token = request.headers.get('Authorization')
  decoded_token = auth.verify_id_token(jwt_token)
  email = decoded_token['email']
  user = UserModel.get_user_by_email(email)
  user.delete()
  return custom_response({'message': 'User deleted successfully!'}, 204)


@cross_origin()
@user_bp.route('/me', methods=['GET'])
# @limiter.limit("2 per day")
@Auth.check_token
def get_me():
  """
  Get me
  """
  jwt_token = request.headers.get('Authorization')
  decoded_token = auth.verify_id_token(jwt_token)
  email = decoded_token['email']

  user = UserModel.get_user_by_email(email)
  user_schema = UserSchema()
  me_user = user_schema.dump(user)
  return custom_response(me_user, 200)


def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
      mimetype="application/json",
      response=json.dumps(res),
      status=status_code
  )
