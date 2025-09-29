# app.py — Secure Flask User Management API
# Notes:
# - Uses environment variables for secrets/config
# - Parameterized SQL everywhere (no string formatting)
# - bcrypt for password hashing (with constant-time verification)
# - Minimal health output (no infra leakage)
# - Input validation + structured error responses
# - Safe logging (no secrets, no PII like passwords)
# - Context-managed DB connections

import os
import re
import json
import logging
import sqlite3
from typing import Tuple, Optional

from flask import Flask, request, jsonify
import bcrypt

# -------------------------
# Config
# -------------------------
APP_ENV = os.getenv("APP_ENV", "development")               # development | test | production
DB_PATH = os.getenv("SQLITE_PATH", "users.db")              # keep sqlite for the assignment
# Example: API_SECRET used for future features (JWT signing, etc.)
API_SECRET = os.getenv("API_SECRET", None)                  # DO NOT hardcode; may be None in dev

# -------------------------
# App & Logging
# -------------------------
app = Flask(__name__)

class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            "level": record.levelname,
            "msg": record.getMessage(),
            "logger": record.name,
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload)

handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
app.logger.setLevel(logging.INFO if APP_ENV != "development" else logging.DEBUG)
app.logger.addHandler(handler)

# -------------------------
# Helpers
# -------------------------
def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

USERNAME_RE = re.compile(r"^[A-Za-z0-9_]{3,32}$")

def validate_credentials(username: Optional[str], password: Optional[str]) -> Tuple[bool, str]:
    if not isinstance(username, str) or not USERNAME_RE.fullmatch(username or ""):
        return False, "Username must be 3–32 chars (letters, numbers, underscore)."
    if not isinstance(password, str) or len(password) < 8:
        return False, "Password must be at least 8 characters."
    return True, ""

def hash_password(password: str) -> str:
    # bcrypt returns bytes like b'$2b$12$...'; store as utf-8 string
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        # In case legacy/invalid hashes exist, fail closed without leaking detail
        return False

def json_error(message: str, status: int = 400):
    return jsonify({"error": message}), status

# -------------------------
# DB Init (idempotent)
# -------------------------
def init_db():
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                is_admin INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        conn.commit()

# -------------------------
# Routes
# -------------------------
@app.route("/health", methods=["GET"])
def health():
    # Intentionally minimal to avoid leaking config
    return jsonify({"status": "healthy", "env": APP_ENV})

@app.route("/users", methods=["GET"])
def list_users():
    with get_conn() as conn:
        rows = conn.execute("SELECT id, username FROM users ORDER BY id ASC").fetchall()
        users = [{"id": row["id"], "username": row["username"]} for row in rows]
    return jsonify({"users": users})

@app.route("/users", methods=["POST"])
def create_user():
    try:
        data = request.get_json(force=True, silent=False)
    except Exception:
        return json_error("Invalid JSON body.", 400)

    username = (data or {}).get("username")
    password = (data or {}).get("password")

    ok, msg = validate_credentials(username, password)
    if not ok:
        return json_error(msg, 400)

    pw_hash = hash_password(password)

    try:
        with get_conn() as conn:
            conn.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, pw_hash),
            )
            conn.commit()
    except sqlite3.IntegrityError:
        return json_error("Username already exists.", 409)

    app.logger.info(f"user_created username={username}")  # safe: no password
    return jsonify({"message": "User created", "username": username}), 201

@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json(force=True, silent=False)
    except Exception:
        return json_error("Invalid JSON body.", 400)

    username = (data or {}).get("username")
    password = (data or {}).get("password")

    if not isinstance(username, str) or not isinstance(password, str):
        return json_error("Username and password are required.", 400)

    with get_conn() as conn:
        row = conn.execute(
            "SELECT id, username, password_hash FROM users WHERE username = ?",
            (username,),
        ).fetchone()

    if not row or not verify_password(password, row["password_hash"]):
        # Don’t reveal which field failed
        app.logger.info(f"login_failed username={username}")
        return json_error("Invalid credentials.", 401)

    app.logger.info(f"login_success username={username} user_id={row['id']}")
    # For the assignment we return a simple payload. In production, issue a JWT/session cookie.
    return jsonify({"message": "Login successful", "user_id": row["id"]})

# -------------------------
# Error Handling
# -------------------------
@app.errorhandler(404)
def not_found(_):
    return json_error("Route not found.", 404)

@app.errorhandler(405)
def method_not_allowed(_):
    return json_error("Method not allowed.", 405)

@app.errorhandler(500)
def internal_error(e):
    app.logger.error("internal_error", exc_info=e)
    return json_error("Internal server error.", 500)

# -------------------------
# Entrypoint
# -------------------------
if __name__ == "__main__":
    init_db()
    # Never force debug=True; respect env
    debug = APP_ENV == "development"
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=debug)
