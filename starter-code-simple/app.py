import json
import logging
import sqlite3

import bcrypt
from config import Config
from flask import Flask, jsonify, request
from pydantic import ValidationError
from validation_models import UserLogin, UserRegistration

# --- Application Setup ---

app = Flask(__name__)
app.config.from_object(Config)

# Configure logging to avoid printing sensitive data
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# --- Database Helper Functions ---


def get_db_connection():
    """Establishes a connection to the database."""
    conn = sqlite3.connect(app.config["DATABASE_URL"])
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn


def init_db():
    """Initializes the database schema."""
    conn = get_db_connection()
    # In testing mode, ensure clean database by dropping existing table
    if app.config.get("TESTING"):
        conn.execute("DROP TABLE IF EXISTS users")
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()
    logging.info("Database initialized.")


@app.errorhandler(ValidationError)
def handle_validation_error(e):
    errors = json.loads(e.json(include_url=False))
    return jsonify({"errors": errors}), 400


# --- Routes ---


@app.route("/health")
def health_check():
    """
    Secure health check endpoint.
    It confirms the app is running without leaking information.
    """
    conn = None
    try:
        conn = get_db_connection()
        conn.execute("SELECT 1")
        db_status = "ok"
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        db_status = "error"
    finally:
        if conn:
            conn.close()

    return jsonify({"status": "healthy", "database_connection": db_status})


@app.route("/users", methods=["GET"])
def get_users():
    """Gets a list of all usernames."""
    conn = get_db_connection()
    users = conn.execute("SELECT id, username FROM users").fetchall()
    conn.close()
    return jsonify(
        {"users": [{"id": u["id"], "username": u["username"]} for u in users]}
    )


@app.route("/users", methods=["POST"])
def create_user():
    """Creates a new user with a securely hashed password."""
    user_data = UserRegistration(**request.get_json())

    username = user_data.username
    password = user_data.password

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, hashed_password.decode("utf-8")),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "Username already exists"}), 409
    finally:
        conn.close()

    logging.info(f"Created new user: {username}")

    return jsonify({"message": "User created successfully", "username": username}), 201


@app.route("/login", methods=["POST"])
def login():
    """Authenticates a user."""
    user_data = UserLogin(**request.get_json())

    username = user_data.username
    password = user_data.password

    conn = get_db_connection()

    user_row = conn.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()
    conn.close()

    if user_row:
        stored_hash = user_row["password_hash"].encode("utf-8")
        if bcrypt.checkpw(password.encode("utf-8"), stored_hash):
            logging.info(f"User '{username}' logged in successfully.")
            return jsonify({"message": "Login successful", "user_id": user_row["id"]})

    logging.warning(f"Failed login attempt for username: '{username}'")
    return jsonify({"error": "Invalid username or password"}), 401


if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=app.config["DEBUG"])
