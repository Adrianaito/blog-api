from flask import Flask
from flask_cors import CORS

from src.ext import config # using dynaconf

def create_app():
    app = Flask(__name__)
    CORS(app)
    config.init_app(app)

    return app

app = create_app()
