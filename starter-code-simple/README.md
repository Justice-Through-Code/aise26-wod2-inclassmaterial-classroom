## Overview

A secure Flask-based user management API with best practices for secrets, authentication, and code quality.

## Setup Instructions

1. **Clone the repository**

   ```
   git clone <repo-url>
   cd <repo-directory>
   ```

2. **Create and activate a virtual environment**

   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Create a `.env` file and fill in your secrets.

5. **Run the application**
   ```
   python app.py
   ```

## Team Workflow & Standards

- All changes must be made via pull requests (PRs) to the `main` branch.
- PRs require at least one code review and must pass CI checks.
- Pre-commit hooks and security scans (Bandit, detect-secrets) are required.
- Follow the [Contributing Guidelines](CONTRIBUTING.md).

## Security

- Secrets must never be hardcoded.
- Use strong password hashing (bcrypt).
- All code is scanned for vulnerabilities before merging.

## API Endpoints

### Health Check

```bash
GET /health
```

### Create User

```bash
POST /users
{
    "username": "john_doe",
    "password": "password123"
}
```

### Login

```bash
POST /login
{
    "username": "john_doe",
    "password": "password123"
}
```

### List Users

```bash
GET /users
```
