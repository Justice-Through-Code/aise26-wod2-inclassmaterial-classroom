# Simple Python API - Starting Point for GitHub Classroom Assignment

import os
import sqlite3

import bcrypt
from dotenv import load_dotenv
from flask import Flask, jsonify, request

app = Flask(__name__)
load_dotenv()  # Load environment variables from .env file

# Load secrets from environment variables
DATABASE_URL = os.environ.get("DATABASE_URL")
API_SECRET = os.environ.get("API_SECRET")


def get_db_connection():
    return sqlite3.connect("users.db")


@app.route("/health")
def health_check():
    # Do not expose secrets in health check
    return jsonify({"status": "healthy", "database": bool(DATABASE_URL)})


@app.route("/users", methods=["GET"])
def get_users():
    conn = get_db_connection()
    users = conn.execute("SELECT id, username FROM users").fetchall()
    conn.close()
    return jsonify({"users": [{"id": u[0], "username": u[1]} for u in users]})


@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    # Basic input validation
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Invalid input"}), 400

    username = data.get("username")
    password = data.get("password")

    # Strong password hashing
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    conn = get_db_connection()
    # Use parameterized query to prevent SQL injection
    conn.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, hashed_password),
    )
    conn.commit()
    conn.close()

    # Do not log sensitive information
    print(f"Created user: {username}")
    return jsonify({"message": "User created", "username": username})


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    conn = get_db_connection()
    # Use parameterized query to prevent SQL injection
    user = conn.execute(
        "SELECT id, password FROM users WHERE username=?", (username,)
    ).fetchone()
    conn.close()

    if user and bcrypt.checkpw(password.encode(), user[1].encode()):
        return jsonify({"message": "Login successful", "user_id": user[0]})
    return jsonify({"message": "Invalid credentials"}), 401


def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
