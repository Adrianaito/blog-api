from flask import request
from functools import wraps
from firebase_admin import auth
from functools import wraps


class Auth():
  """
  Auth Class
  """
  @staticmethod
  def check_token(f):
    '''
    Firebase Authentication
    '''
    @wraps(f)
    def wrap(*args, **kwargs):
        if not request.headers.get('authorization'):
            return {'message': 'No token provided'}, 400
        try:
            user = auth.verify_id_token(request.headers['authorization'])
            request.user = user
        except:
            return {'message': 'Invalid token provided.'}, 400
        return f(*args, **kwargs)
    return wrap
