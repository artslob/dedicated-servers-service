import os
import tempfile

import pytest

from flaskr import create_app


@pytest.fixture(scope='session')
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        import flaskr.db as db
        db.init_app(app)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def default_data(app):
    from flaskr import models
    from flaskr.db import db_session
    models.Rack.query.delete()
    models.Server.query.delete()
    db_session.commit()
    rack = models.Rack(capacity=models.RackCapacities.ten)
    db_session.add(rack)
    db_session.commit()
    for i in range(5):
        db_session.add(models.Server(rack_id=rack.id))
        rack.size = models.Rack.size + 1
        db_session.commit()

    rack = models.Rack(capacity=models.RackCapacities.twenty)
    db_session.add(rack)
    db_session.commit()
    for i in range(20):
        db_session.add(models.Server(rack_id=rack.id))
        rack.size = models.Rack.size + 1
        db_session.commit()
