import pytest
from src import create_app
from src import db as _db
from setup_test_db import init_db

@pytest.fixture(scope="function")
def test_client():
    flask_app = create_app("flask_test.cfg")


    with flask_app.test_client() as test_client:
        with flask_app.app_context():
            _db.drop_all()
            _db.create_all()
            init_db(_db)
            yield test_client


############
# FOR DB TESTING
############

@pytest.fixture(scope="function")
def app():
    _app = create_app("flask_test.cfg")

    with _app.app_context():
        yield _app


@pytest.fixture(scope="function")
def db(app):
    _db.drop_all()
    _db.create_all()

    init_db(_db)

    return _db


@pytest.fixture(scope="function")
def session(db):
    db.session.begin_nested()

    yield db.session

    db.session.rollback()