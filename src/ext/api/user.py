from flask import Blueprint, render_template
from flask_cors import cross_origin
from flask import current_app

user_bp = Blueprint('user', __name__)
