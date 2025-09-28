from app import get_db_connection  # Import to inspect DB state

# All test functions will automatically receive the 'client' fixture
# defined in conftest.py

# Valid test data that meets pydantic requirements
VALID_USERNAME = "testuser"
VALID_PASSWORD = "StrongPass1!"

# Additional test data
VALID_USERNAME2 = "user2"
VALID_PASSWORD2 = "AnotherPass2!"

# Invalid test data for validation tests
INVALID_USERNAME_SHORT = "ab"  # too short (< 3)
INVALID_USERNAME_LONG = "a" * 21  # too long (> 20)
INVALID_USERNAME_SPECIAL = "user@name"  # special chars
INVALID_PASSWORD_SHORT = "Short1!"  # too short (< 8)
INVALID_PASSWORD_NO_UPPER = "password1!"  # no uppercase
INVALID_PASSWORD_NO_LOWER = "PASSWORD1!"  # no lowercase
INVALID_PASSWORD_NO_DIGIT = "Password!"  # no digit
INVALID_PASSWORD_NO_SPECIAL = "Password1"  # no special char


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["status"] == "healthy"
    assert json_data["database_connection"] == "ok"


def test_get_users_empty(client):
    """Test getting users when the database is empty."""
    response = client.get("/users")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["users"] == []


def test_create_user_success(client, app):
    """Test successful user creation."""
    response = client.post(
        "/users", json={"username": VALID_USERNAME, "password": VALID_PASSWORD}
    )
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data["message"] == "User created successfully"
    assert json_data["username"] == "testuser"

    # Verify user was actually added to the database
    with app.app_context():
        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username = 'testuser'"
        ).fetchone()
        conn.close()
        assert user is not None
        assert user["username"] == "testuser"


def test_create_user_duplicate(client):
    """Test creating a user with a username that already exists."""
    # First, create a user
    client.post("/users", json={"username": "duplicate", "password": VALID_PASSWORD})

    # Now, try to create another with the same username
    response = client.post(
        "/users", json={"username": "duplicate", "password": VALID_PASSWORD}
    )
    assert response.status_code == 409
    json_data = response.get_json()
    assert json_data["error"] == "Username already exists"


def test_create_user_missing_data(client):
    """Test creating a user with missing username or password."""
    # Missing password
    response = client.post("/users", json={"username": VALID_USERNAME})
    assert response.status_code == 400
    errors = response.get_json()["errors"]
    assert len(errors) == 1
    assert errors[0]["loc"] == ["password"]
    assert errors[0]["type"] == "missing"
    assert "Field required" in errors[0]["msg"]

    # Missing username
    response = client.post("/users", json={"password": VALID_PASSWORD})
    assert response.status_code == 400
    errors = response.get_json()["errors"]
    assert len(errors) == 1
    assert errors[0]["loc"] == ["username"]
    assert errors[0]["type"] == "missing"
    assert "Field required" in errors[0]["msg"]


def test_login_success(client):
    """Test a successful login."""
    # First, create the user to log in with
    client.post("/users", json={"username": VALID_USERNAME, "password": VALID_PASSWORD})

    # Now, attempt to log in
    response = client.post(
        "/login", json={"username": VALID_USERNAME, "password": VALID_PASSWORD}
    )

    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["message"] == "Login successful"
    assert "user_id" in json_data


def test_login_wrong_password(client):
    """Test a login attempt with an incorrect password."""
    # Create the user
    client.post(
        "/users", json={"username": VALID_USERNAME2, "password": VALID_PASSWORD2}
    )

    # Attempt to log in with the wrong password
    response = client.post(
        "/login", json={"username": VALID_USERNAME2, "password": "wrongpassword"}
    )

    assert response.status_code == 401
    json_data = response.get_json()
    assert json_data["error"] == "Invalid username or password"


def test_login_nonexistent_user(client):
    """Test a login attempt for a user that does not exist."""
    response = client.post(
        "/login", json={"username": "nosuchuser", "password": "anypassword"}
    )
    assert response.status_code == 401
    json_data = response.get_json()
    assert json_data["error"] == "Invalid username or password"


def test_get_users_with_data(client):
    """Test getting the user list after creating users."""
    client.post("/users", json={"username": "user1", "password": VALID_PASSWORD})
    client.post("/users", json={"username": "user2", "password": VALID_PASSWORD2})

    response = client.get("/users")
    assert response.status_code == 200
    json_data = response.get_json()

    assert len(json_data["users"]) == 2
    usernames = {u["username"] for u in json_data["users"]}
    assert "user1" in usernames
    assert "user2" in usernames
    # Ensure password hashes are not returned
    for user in json_data["users"]:
        assert "password_hash" not in user


def test_create_user_username_invalid_chars(client):
    """Test creating a user with invalid username characters."""
    response = client.post(
        "/users",
        json={"username": INVALID_USERNAME_SPECIAL, "password": VALID_PASSWORD},
    )
    assert response.status_code == 400
    errors = response.get_json()["errors"]
    assert len(errors) == 1
    assert errors[0]["loc"] == ["username"]
    assert (
        "Username must contain only letters, numbers, and underscores"
        in errors[0]["msg"]
    )


def test_create_user_username_too_short(client):
    """Test creating a user with username too short."""
    response = client.post(
        "/users", json={"username": INVALID_USERNAME_SHORT, "password": VALID_PASSWORD}
    )
    assert response.status_code == 400
    errors = response.get_json()["errors"]
    assert len(errors) == 1
    assert errors[0]["loc"] == ["username"]
    assert "too_short" in errors[0]["type"]


def test_create_user_username_too_long(client):
    """Test creating a user with username too long."""
    response = client.post(
        "/users", json={"username": INVALID_USERNAME_LONG, "password": VALID_PASSWORD}
    )
    assert response.status_code == 400
    errors = response.get_json()["errors"]
    assert len(errors) == 1
    assert errors[0]["loc"] == ["username"]
    assert "too_long" in errors[0]["type"]


def test_create_user_password_too_short(client):
    """Test creating a user with password too short."""
    response = client.post(
        "/users", json={"username": VALID_USERNAME, "password": INVALID_PASSWORD_SHORT}
    )
    assert response.status_code == 400
    errors = response.get_json()["errors"]
    assert len(errors) == 1
    assert errors[0]["loc"] == ["password"]
    assert "Password must be at least 8 characters long" in errors[0]["msg"]


def test_create_user_password_no_uppercase(client):
    """Test creating a user with password missing uppercase."""
    response = client.post(
        "/users",
        json={"username": VALID_USERNAME, "password": INVALID_PASSWORD_NO_UPPER},
    )
    assert response.status_code == 400
    errors = response.get_json()["errors"]
    assert len(errors) == 1
    assert errors[0]["loc"] == ["password"]
    assert "Password must contain at least one uppercase letter" in errors[0]["msg"]


def test_create_user_password_no_lowercase(client):
    """Test creating a user with password missing lowercase."""
    response = client.post(
        "/users",
        json={"username": VALID_USERNAME, "password": INVALID_PASSWORD_NO_LOWER},
    )
    assert response.status_code == 400
    errors = response.get_json()["errors"]
    assert len(errors) == 1
    assert errors[0]["loc"] == ["password"]
    assert "Password must contain at least one lowercase letter" in errors[0]["msg"]


def test_create_user_password_no_digit(client):
    """Test creating a user with password missing digit."""
    response = client.post(
        "/users",
        json={"username": VALID_USERNAME, "password": INVALID_PASSWORD_NO_DIGIT},
    )
    assert response.status_code == 400
    errors = response.get_json()["errors"]
    assert len(errors) == 1
    assert errors[0]["loc"] == ["password"]
    assert "Password must contain at least one digit" in errors[0]["msg"]


def test_create_user_password_no_special(client):
    """Test creating a user with password missing special character."""
    response = client.post(
        "/users",
        json={"username": VALID_USERNAME, "password": INVALID_PASSWORD_NO_SPECIAL},
    )
    assert response.status_code == 400
    errors = response.get_json()["errors"]
    assert len(errors) == 1
    assert errors[0]["loc"] == ["password"]
    assert "Password must contain at least one special character" in errors[0]["msg"]


def test_login_missing_data(client):
    """Test login with missing username or password."""
    # Missing password
    response = client.post("/login", json={"username": VALID_USERNAME})
    assert response.status_code == 400
    errors = response.get_json()["errors"]
    assert len(errors) == 1
    assert errors[0]["loc"] == ["password"]
    assert errors[0]["type"] == "missing"

    # Missing username
    response = client.post("/login", json={"password": VALID_PASSWORD})
    assert response.status_code == 400
    errors = response.get_json()["errors"]
    assert len(errors) == 1
    assert errors[0]["loc"] == ["username"]
    assert errors[0]["type"] == "missing"
