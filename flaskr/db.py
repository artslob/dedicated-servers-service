import click
from flask.cli import with_appcontext
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('sqlite:///instance/flaskr.sqlite', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def close_db(exp=None):
    db_session.remove()


def init_db():
    from . import models
    Base.metadata.create_all(bind=engine)
    rack = models.Rack(capacity=10)
    db_session.add(rack)
    db_session.commit()
    for i in range(5):
        db_session.add(models.Server(rack_id=rack.id))
        rack.size = models.Rack.size + 1
        db_session.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
