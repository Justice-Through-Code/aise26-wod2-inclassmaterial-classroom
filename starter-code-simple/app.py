# Simple Python API - Starting Point for GitHub Classroom Assignment
# This code has intentional security flaws for educational purposes

from flask import Flask, request, jsonify
from dotenv import load_dotenv
import sqlite3
import bcrypt
import os

load_dotenv()  # take environment variables from .env.


app = Flask(__name__)

# Security Issue: Hardcoded secrets
DATABASE_URL = os.getenv("DATABASE_URL")
API_SECRET = os.getenv("API_SECRET")


def get_db_connection():
    return sqlite3.connect("users.db")


@app.route("/health")
def health_check():
    return jsonify({"status": "healthy", "database": DATABASE_URL})


@app.route("/users", methods=["GET"])
def get_users():
    conn = get_db_connection()
    users = conn.execute("SELECT id, username FROM users").fetchall()
    conn.close()
    return jsonify({"users": [{"id": u[0], "username": u[1]} for u in users]})


@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Security Issue: Weak password hashing
    hashed_password = bcrypt.hashpw(
        password.encode(), bcrypt.gensalt(rounds=12)
    ).decode()

    conn = get_db_connection()
    # Security Issue: SQL injection vulnerability
    conn.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, hashed_password),
    )
    conn.commit()
    conn.close()

    # Security Issue: Logging sensitive information
    return jsonify({"message": "User created", "username": username})


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    hashed_password = bcrypt.hashpw(
        password.encode(), bcrypt.gensalt(rounds=12)
    ).decode()

    conn = get_db_connection()
    # Security Issue: SQL injection vulnerability
    user = conn.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, hashed_password),
    ).fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login successful", "user_id": user[0]})
    return jsonify({"message": "Invalid credentials"}), 401


def init_db():
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    app.run()
