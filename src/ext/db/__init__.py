from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)

from .blogpost_model import BlogPostModel, BlogPostSchema
from .user_model import UserModel, UserSchema
