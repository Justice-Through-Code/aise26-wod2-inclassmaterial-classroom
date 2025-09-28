# User Management API

A secure Flask-based REST API for user management with robust authentication, password hashing, and comprehensive security practices.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Development Workflow](#development-workflow)
- [Security Considerations](#security-considerations)
- [Contributing](#contributing)
- [License](#license)

## Features

- **User Registration**: Secure user account creation with strong password requirements
- **User Authentication**: Secure login with bcrypt password hashing
- **User Management**: View user listings
- **Health Check**: API status monitoring with database connectivity verification
- **Input Validation**: Pydantic-based request validation
- **Secure Configuration**: Environment variable-based configuration management
- **Comprehensive Testing**: Pytest test suite with fixtures
- **Code Quality**: Pre-commit hooks for linting, formatting, and security scanning
- **CI/CD Pipeline**: Automated testing and quality checks via GitHub Actions

## Prerequisites

- Python 3.13 or higher
- Git (for version control and pre-commit hooks)
- Virtual environment management (venv recommended)

## Installation

1. **Clone and navigate to the project directory**:
   ```bash
   git clone <repository-url>
   cd starter-code-simple
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env  # Copy example environment file if provided
   # Edit .env with your configuration values
   ```

5. **Install pre-commit hooks** (for development):
   ```bash
   pip install pre-commit
   pre-commit install
   ```

## Configuration

The application uses environment variables for configuration. Create a `.env` file in the project root:

```env
# Flask Configuration
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here

# Database Configuration
DATABASE_URL=users.db
```

### Configuration Options

- `FLASK_DEBUG`: Enables debug mode (default: False)
- `SECRET_KEY`: Secret key for Flask sessions (required for production)
- `DATABASE_URL`: Path to SQLite database file (default: users.db)

## Usage

1. **Initialize the database and run the application**:
   ```bash
   python app.py
   ```

   The application will start on `http://localhost:5000` (or port 5000 in production).

2. **Verify the API is running**:
   ```bash
   curl http://localhost:5000/health
   ```

## API Documentation

### Base URL
```
http://localhost:5000
```

### Endpoints

#### Health Check
- **GET** `/health`
- **Description**: Checks API and database connectivity
- **Response**: JSON status object

**Example**:
```bash
curl http://localhost:5000/health
```
```json
{
  "status": "healthy",
  "database_connection": "ok"
}
```

#### Create User (Registration)
- **POST** `/users`
- **Description**: Registers a new user account
- **Content-Type**: `application/json`

**Request Body**:
```json
{
  "username": "johndoe",
  "password": "StrongPass123!"
}
```

**Success Response (201)**:
```json
{
  "message": "User created successfully",
  "username": "johndoe"
}
```

**Error Response (400)**:
```json
{
  "error": "Validation error details"
}
```

**Error Response (409)**:
```json
{
  "error": "Username already exists"
}
```

#### User Login
- **POST** `/login`
- **Description**: Authenticates a user
- **Content-Type**: `application/json`

**Request Body**:
```json
{
  "username": "johndoe",
  "password": "StrongPass123!"
}
```

**Success Response (200)**:
```json
{
  "message": "Login successful",
  "user_id": 1
}
```

**Error Response (401)**:
```json
{
  "error": "Invalid username or password"
}
```

#### List Users
- **GET** `/users`
- **Description**: Retrieves all usernames and IDs

**Response**:
```json
{
  "users": [
    {
      "id": 1,
      "username": "johndoe"
    }
  ]
}
```

### Validation Rules

#### Username Requirements
- 3-20 characters
- Only letters, numbers, and underscores
- Must be unique

#### Password Requirements
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit
- At least one special character (!@#$%^&*(),.?":{}|<>)

## Testing

### Running Tests
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_app.py
```

### Pre-commit Hooks
```bash
# Run all hooks on all files
pre-commit run --all-files

# Run specific hook (e.g., flake8)
pre-commit run flake8 --all-files
```

## Development Workflow

### GitHub Flow
1. Create a feature branch from `main`
2. Make changes and commit (pre-commit hooks will run automatically)
3. Push branch and create pull request
4. CI pipeline runs automatically
5. Code review and approval
6. Merge to `main`

### Code Standards
- **Formatting**: Black (88 character line length)
- **Imports**: isort (compatible with Black)
- **Linting**: flake8 with Black/isort integration
- **Type Checking**: mypy
- **Security**: bandit, detect-secrets
- **Testing**: 100% branch coverage target

### Commit Guidelines
- Use clear, descriptive commit messages
- Keep commits atomic and focused
- Reference issue numbers when applicable

### Pull Request Requirements
- All CI checks must pass
- Code review required
- Include tests for new features
- Update documentation as needed
- Follow security checklist (see Contributing)

## Security Considerations

### Password Security
- Passwords are hashed using bcrypt (12 rounds)
- Strong password requirements enforced
- No password logging or storage in plain text

### Input Validation
- All requests validated using Pydantic models
- SQL injection prevention through parameterized queries
- Username uniqueness constraints

### Secure Configuration
- Secrets loaded from environment variables
- No hardcoded credentials in code
- Debug mode disabled in production

### Logging Security
- Sensitive data not logged
- Authentication failures logged without details

### Security Scanning
- Automated scans with bandit and detect-secrets
- Pre-commit hooks prevent secret commits
- CI pipeline includes security checks

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Quick Start
1. Fork the repository
2. Set up development environment (see Installation)
3. Create feature branch: `git checkout -b feature/your-feature`
4. Make changes and write tests
5. Run pre-commit: `pre-commit run --all-files`
6. Test locally: `pytest`
7. Submit pull request with completed security checklist

### Pull Request Template
Pull requests must include our security checklist found in [.github/pull_request_template.md](.github/pull_request_template.md).

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Security Note**: This API implements industry-standard security practices. For production deployment, additional measures such as HTTPS, rate limiting, and centralized logging should be implemented.
