import pytest
from src import create_app


@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app("flask_test.cfg")

    with flask_app.test_client() as test_client:
        with flask_app.app_context():
            yield test_client