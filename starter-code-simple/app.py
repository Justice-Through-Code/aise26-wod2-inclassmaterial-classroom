import os
import sqlite3
import logging
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

try:
    from dotenv import load_dotenv  # for local dev
    load_dotenv()
except Exception:
    pass

app = Flask(__name__)

DB_PATH = os.getenv("DATABASE_PATH", "users.db")

# ---------- logging (no secrets) ----------
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(message)s"
)
log = logging.getLogger(__name__)

# ---------- helpers ----------
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

def validate_username(u: str) -> bool:
    return isinstance(u, str) and 3 <= len(u) <= 64

def validate_password(p: str) -> bool:
    return isinstance(p, str) and 8 <= len(p) <= 256

# ---------- routes ----------
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "database": DB_PATH}), 200

@app.route("/users", methods=["GET"])
def get_users():
    with get_conn() as conn:
        rows = conn.execute("SELECT id, username, created_at FROM users ORDER BY id").fetchall()
    # never return password hashes
    return jsonify([dict(r) for r in rows]), 200

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not (validate_username(username) and validate_password(password)):
        return jsonify({"error": "invalid username or password"}), 400

    pwd_hash = generate_password_hash(password)

    try:
        with get_conn() as conn:
            conn.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, pwd_hash)
            )
        log.info("created user '%s'", username)
        return jsonify({"message": "user created", "username": username}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "username already exists"}), 409

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not (validate_username(username) and isinstance(password, str)):
        return jsonify({"error": "invalid credentials"}), 400

    with get_conn() as conn:
        row = conn.execute(
            "SELECT password_hash FROM users WHERE username = ?",
            (username,)
        ).fetchone()

    if not row or not check_password_hash(row["password_hash"], password):
        log.warning("failed login for '%s'", username)
        return jsonify({"error": "invalid credentials"}), 401

    log.info("successful login for '%s'", username)
    # For exercise-just acknowledge-do NOT return secrets/tokens here
    return jsonify({"message": "login ok"}), 200

# ---------- bootstrap ----------
if __name__ == "__main__":
    init_db()
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=debug)
