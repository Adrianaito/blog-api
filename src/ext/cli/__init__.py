import click
from src.ext.db import db
from src.ext.db import models # noqa

def init_app(app):

    @app.cli.command()
    def create_db():
        """This command will create the database."""
        db.create_all()
        click.echo('Database created.')
