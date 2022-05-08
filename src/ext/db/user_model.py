import datetime
from marshmallow import fields, Schema

from src.ext.db import db
from src.ext.schema import ma
from src.ext.db.blogpost_model import BlogPostSchema

class UserModel(db.Model):
    """
    User Model
    """

    # table name
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    blogposts = db.relationship('BlogPostModel', backref='users', lazy=True)

    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.name = data.get('name')
        self.email = data.get('email')
        self.birth_date = data.get('birth_date')
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        pass

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_users():
        return UserModel.query.all()

    @staticmethod
    def get_one_user(id: int):
        return UserModel.query.get(id)

    @staticmethod
    def get_user_by_email(email: str):
        return UserModel.query.filter_by(email=email).first()

    def __repr__(self):
        return '<id {}>'.format(self.id)

class UserSchema(ma.Schema):
    class Meta:
        """Fields to expose"""
        model = UserModel
        fields = ('id', 'name', 'email', 'birth_date', 'created_at', 'blogposts')
