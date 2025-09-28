import pytest
from app import app as flask_app
from app import init_db
from config import TestConfig


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Use the test configuration
    flask_app.config.from_object(TestConfig)

    # Create the database and the database table
    with flask_app.app_context():
        init_db()

    yield flask_app

    # Teardown can go here if needed, but in-memory DB is auto-cleaned


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()
