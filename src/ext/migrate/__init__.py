from flask_migrate import Migrate
from src.ext.db import  db
from src.ext.db import blogpost_model,user_model # noqa

migrate = Migrate()

def init_app(app):
    migrate.init_app(app, db)
