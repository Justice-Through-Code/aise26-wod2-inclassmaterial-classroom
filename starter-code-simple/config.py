# config.py
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG = os.environ.get("FLASK_DEBUG", "False").lower() in ("true", "1", "t")
    DATABASE_URL = os.environ.get("DATABASE_URL")


class TestConfig(Config):
    TESTING = True
    # Use an in-memory SQLite database for tests
    # This is fast and automatically discarded when the connection is closed
    DATABASE_URL = "test_users.db"
    DEBUG = True
