from flask import Flask

from src.ext import config # using dynaconf

def create_app():
    app = Flask(__name__)
    config.init_app(app)

    return app
