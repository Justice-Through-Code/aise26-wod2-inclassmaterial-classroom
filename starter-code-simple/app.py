# Simple Python API - Starting Point for GitHub Classroom Assignment
# This code has intentional security flaws for educational purposes

# import os added to read .env variables in app rather than hardcoding sensitive data
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import sqlite3
import hashlib

# This reads from the .env file
load_dotenv()  

app = Flask(__name__)

# Hardcoded sensitive data presents a security issue
# Resolved by setting `os.getenv` to read from environment
DATABASE_URL = os.getenv("DATABASE_URL")   
API_SECRET   = os.getenv("API_SECRET")         
DATABASE_PATH = os.getenv("DATABASE_PATH", "users.db")

def get_db_connection():
    return sqlite3.connect('users.db')

@app.route('/health')
def health_check():
    # Health check exposed DB URl, which included sensitive password
    # Changed health check so it only checks if the app is running and the DB is connected   
    try:
        # Try to connect to the database using path defined in .env 
        conn = sqlite3.connect(DATABASE_PATH)

        # Run a query ("SELECT 1") to verify the DB is responsive
        conn.execute("SELECT 1")

        # Close the connection to avoid leaks
        conn.close()

        # If no errors, return a simple OK response
        return jsonify({"status": "ok", "db_ok": True})
    except Exception:
        # If anything fails return degraded status and a 503 Service Unavailable
        return jsonify({"status": "degraded", "db_ok": False}), 503

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    users = conn.execute('SELECT id, username FROM users').fetchall()
    conn.close()
    return jsonify({"users": [{"id": u[0], "username": u[1]} for u in users]})

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Security Issue: Weak password hashing
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    
    conn = get_db_connection()
    # Security Issue: SQL injection vulnerability
    conn.execute(
        f"INSERT INTO users (username, password) VALUES ('{username}', '{hashed_password}')"
    )
    conn.commit()
    conn.close()
    
    # Security Issue: Logging sensitive information
    print(f"Created user: {username} with password: {password}")
    return jsonify({"message": "User created", "username": username})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    
    conn = get_db_connection()
    # Security Issue: SQL injection vulnerability
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{hashed_password}'"
    user = conn.execute(query).fetchone()
    conn.close()
    
    if user:
        return jsonify({"message": "Login successful", "user_id": user[0]})
    return jsonify({"message": "Invalid credentials"}), 401

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)