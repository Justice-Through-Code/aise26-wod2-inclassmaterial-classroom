# Contributing Guidelines

We welcome contributions to the User Management API project! This document outlines our processes and standards to ensure high-quality, secure code that adheres to our team workflow.

## Table of Contents
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Security](#security)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Code Review](#code-review)
- [Reporting Issues](#reporting-issues)
- [Release Process](#release-process)

## Getting Started

### Prerequisites
- Python 3.13 or higher
- Git
- Virtual environment experience

### Setup
1. Fork and clone the repository
2. Set up the development environment (see README2.md Installation section)
3. Install pre-commit hooks: `pre-commit install`

### Branching Strategy
We use GitHub Flow:
- `main` branch is protected and always deployable
- Create feature branches from `main`
- Branch naming: `feature/description`, `bugfix/description`, `hotfix/description`

## Development Workflow

### Daily Development Cycle
1. **Update your main branch**: `git pull upstream main`
2. **Create feature branch**: `git checkout -b feature/your-feature`
3. **Make changes**: Write code and tests iteratively
4. **Commit frequently**: Small, focused commits
5. **Push and create PR**: When ready for review

### Commit Guidelines
- Use present tense: "Fix login validation" not "Fixed login validation"
- Limit first line to 72 characters
- Provide detailed description in body if needed
- Reference issue numbers: `#123`

Example:
```bash
git commit -m "Add password complexity validation

- Require minimum 8 characters
- Enforce mix of character types
- Update validation error messages

Closes #45"
```

## Code Standards

### Python Code Style
- **Formatting**: Black (88 character line length)
- **Imports**: isort (alphabetical, grouped by type)
- **Linting**: flake8 (PEP 8 compliant)
- **Type hints**: mypy type checking

### Formatting Example
```python
# Correct formatting with Black/isort
import os
from typing import Dict, List

from flask import Flask, jsonify, request
import bcrypt

def validate_password(password: str) -> bool:
    """Validate password strength."""
    return (
        len(password) >= 8
        and any(c.isupper() for c in password)
        and any(c.islower() for c in password)
    )
```

### File Organization
```
starter-code-simple/
├── app.py                 # Main application
├── config.py             # Configuration management
├── validation_models.py  # Pydantic models
└── tests/
    ├── conftest.py       # Test fixtures
    └── test_app.py       # Test cases
```

### Naming Conventions
- **Classes**: PascalCase
- **Functions/Methods**: snake_case
- **Variables**: snake_case
- **Constants**: UPPER_CASE
- **Modules**: snake_case

## Testing

### Test Structure
- Unit tests for individual functions/methods
- Integration tests for API endpoints
- Test fixtures in `conftest.py`

### Running Tests
```bash
# All tests with coverage
pytest --cov=. --cov-report=html

# Specific test file
pytest tests/test_app.py::test_login_success

# Run with verbose output
pytest -v
```

### Test Coverage Requirements
- Minimum 90% code coverage
- Cover both happy path and error scenarios
- Test edge cases and security boundaries

### Example Test Structure
```python
def test_user_registration_valid(client, valid_user_data):
    response = client.post("/users", json=valid_user_data)
    assert response.status_code == 201
    assert response.get_json()["message"] == "User created successfully"

def test_user_registration_duplicate(client, valid_user_data):
    client.post("/users", json=valid_user_data)
    response = client.post("/users", json=valid_user_data)
    assert response.status_code == 409
    assert "already exists" in response.get_json()["error"]
```

## Security

### Security-First Development
- **Never commit secrets**: Use environment variables
- **Validate all inputs**: Pydantic models for request validation
- **Secure credentials**: bcrypt for password hashing
- **Safe databases**: Parameterized queries prevent SQL injection

### Security Tools
- **bandit**: Static security analysis
- **detect-secrets**: Sensitive data detection
- **Pre-commit hooks**: Automatic security scans

### Security Checkpoints
Before committing:
1. Run bandit: `bandit -r starter-code-simple/`
2. Check secrets: `detect-secrets scan`
3. Run pre-commit: `pre-commit run --all-files`

## Documentation

### Code Documentation
- **Docstrings**: Use Google style for all public functions
- **Type hints**: Required for function parameters and return values
- **Comments**: Explain complex logic, not obvious code

Example:
```python
def authenticate_user(username: str, password: str) -> Dict[str, Any]:
    """Authenticate a user with username and password.

    Args:
        username: The user's username (3-20 chars)
        password: The user's password (hashed verification)

    Returns:
        Dict containing authentication result and user info

    Raises:
        ValueError: If authentication fails
    """
    # Implementation with detailed comments
```

### API Documentation
- Update README2.md for any API changes
- Include examples for new endpoints
- Document error responses

## Pull Request Process

### Before Creating PR
1. **Rebase on main**: `git fetch upstream && git rebase upstream/main`
2. **Squash commits**: Clean up commit history
3. **Test thoroughly**: All tests pass, pre-commit clean
4. **Document changes**: Update README if needed

### PR Template Requirements
- **Title**: Clear, descriptive summary
- **Description**: Detailed explanation of changes
- **Security Checklist**: Complete all security items
- **Testing**: Confirm tests pass
- **Documentation**: Update as needed

### PR Size Guidelines
- **Small PR**: < 200 lines, quick review
- **Medium PR**: 200-500 lines, detailed review
- **Large PR**: > 500 lines, break down or extensive review

## Code Review

### Review Criteria
- **Functionality**: Changes work as intended
- **Security**: No vulnerabilities introduced
- **Performance**: Efficient implementation
- **Readability**: Clear, maintainable code
- **Testing**: Adequate test coverage
- **Standards**: Follows team conventions

### Review Checklist
- [ ] Code follows style guidelines
- [ ] Tests included and passing
- [ ] Security checklist completed
- [ ] Documentation updated
- [ ] No new linting errors
- [ ] Database migrations safe

### Giving Reviews
- **Constructive feedback**: Focus on code, not person
- **Specific suggestions**: Propose improvements
- **Acknowledge good work**: Positive reinforcement
- **Security focus**: Always check security implications

## Reporting Issues

### Bug Reports
Use the GitHub issue template with:
- Clear title describing the issue
- Steps to reproduce (minimal example if possible)
- Expected vs actual behavior
- Environment details (Python version, OS, etc.)
- Logs or error messages

### Feature Requests
- Describe the proposed feature
- Explain the use case and benefits
- Consider implementation complexity
- Provide mock examples if helpful

### Security Issues
- **Do not report in public**: Use security@project-domain.com
- **Responsible disclosure**: Allow time for fix before public disclosure
- **Details**: Include steps to reproduce, impact assessment

## Release Process

### Version Numbering
Following [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes (API changes)
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, security improvements

### Release Checklist
- [ ] All tests pass and CI green
- [ ] Security scans pass
- [ ] Documentation updated
- [ ] Change log completed
- [ ] Version numbers updated
- [ ] Tag created and pushed

### Deployment
- Automated deployment from `main` branch
- Rollback plan documented
- Monitoring alerts configured


## Additional Resources

- [README2.md](starter-code-simple/README2.md) - Complete documentation
- [PRE-COMMIT-CONFIG](.pre-commit-config.yaml) - Code quality tools
- [CI Pipeline](.github/workflows/ci.yml) - Automated checks
- [Security Template](.github/pull_request_template.md) - PR security checklist

---

Thank you for contributing to our secure User Management API! Your contributions help make our project better and more secure for everyone.
