# Code Review Exercise - In-Class Breakout

**Duration:** 15 minutes  
**Format:** Individual work with team discussion  
**Objective:** Practice identifying security vulnerabilities and writing professional code review comments

---

## The Code to Review

You're reviewing this Python authentication code that has multiple security issues. Your job is to find them and provide professional feedback.

```python
# auth_system.py - Find the security issues
import requests
import sqlite3
import hashlib

# 🔴 SECURITY: Hardcoded secrets (API key & DB creds)
# Don't Hard Code API KEY, please use .env file
API_KEY = "sk-live-1234567890abcdef"
DATABASE_URL = "postgresql://admin:password123@localhost/prod"

# 🟠 SECURITY: DEBUG flag enabled by default
# risks verbose logging and debug behaviors in prod.
DEBUG_MODE = True

def authenticate_user(username, password):
    conn = sqlite3.connect("users.db")
    # Vulnerable:
    # 🔴 SECURITY: Sensitive data logging
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    
    result = conn.execute(query).fetchone()

    # High Security Issue printing password 
    # Queries assume plaintext storage; reset_password writes new password in plaintext.
    # Store hashed passwords (argon2/bcrypt) and verify securely:
    print(f"Login attempt: {username}:{password}")
    # 🟠 SECURITY: Unvalidated/unbounded external API call
    # no timeout, error handling, or response validation.
    response = requests.post("https://api.auth.com/verify", 
                           data={"user": username, "key": API_KEY})
#    🟠 SECURITY: Returning raw upstream JSON to callers 
# leaks third-party schema/errors to clients.
    return response.json()

def reset_password(user_id, new_password):
    conn = sqlite3.connect("users.db")

    # Vulnerable:
    # Queries assume plaintext storage; reset_password writes new password in plaintext.
    # Store hashed passwords (argon2/bcrypt) and verify securely:
    query = f"UPDATE users SET password='{new_password}' WHERE id={user_id}"
    conn.execute(query)
    conn.commit()

    # 🟠 SECURITY/RELIABILITY: DB connection handling & resource leaks
    # connections are never closed; no context managers or error handling.

def hash_password(password):
    # 🔴 SECURITY: Weak hashing (MD5)
    # cryptographically broken and unsalted.
    return hashlib.md5(password.encode()).hexdigest()


# 🔴 SECURITY: Insecure admin/backdoor check
# assumes magic values confer admin.
def admin_check(user_id):
    if user_id == 1 or user_id == "admin":
        return True
    return False
```

---

## Your Task (10 minutes individual work)

**Find and document at least 6 security issues** using this professional format:

```markdown
## Code Review Comments

**🔴 SECURITY: [Issue Type]**
**Line X:** [Specific problem description]
**Impact:** [What could go wrong if exploited]
**Suggestion:** 
```python
# Instead of this vulnerable code:
vulnerable_example()

# Use this secure approach:
secure_example()
```
**Priority:** Critical/High/Medium/Low
```

---

## Hints

- Look for hardcoded secrets and credentials
- Check for SQL injection risks in string-formatted queries
- Watch for logging of sensitive data
- Ensure passwords are hashed with modern algorithms
- Validate inputs and handle errors
- Avoid insecure external API usage without checking responses
- Beware of hidden backdoors and insecure defaults

---

## Team Discussion (5 minutes)

** Share with your breakout room: **
1. Which issues did you find?
- Hardcoded secrets (API key, DB credentials)
- SQL injection in string-formatted queries
- Plaintext password storage & use of MD5
- Logging sensitive data (username + password)
- Insecure admin_check backdoor
- Debug mode enabled in production
- Unvalidated/unbounded external API call

2. Which ones did you miss?
I had to have chat help me with all of this pretty much. I found 2 or 3 myself and the rest came from ai.

3. How would you prioritize fixing them?
Critical fixes first: Remove hardcoded secrets, replace plaintext/MD5 with Argon2/Bcrypt, and parameterize SQL queries.
- High priority: Remove sensitive logging, secure the admin check, and fix the external API call (timeouts, headers, validation).
- Medium priority: Disable debug in production, close DB connections properly, validate inputs, and prevent brute force attacks.
- Low priority: Standardize return values instead of exposing raw JSON.


4. What was challenging about writing professional review comments?
- Balancing technical accuracy with clarity so comments are understandable.
- Avoiding being too harsh—framing feedback as constructive.
- Providing not just what’s wrong, but why it matters and how to fix it.
- Deciding which issues are most important to highlight given limited time.


**Discussion Questions:**
- What makes a code review comment helpful vs. just critical?

Helpful comments explain the impact of the issue and suggest a fix.
Critical-only comments just say “this is wrong” without context.


- How do you balance being thorough with being constructive?

Focus on the biggest risks first, then note smaller improvements if time allows.
Phrase comments in a supportive way: “Consider changing X for better security” instead of “This is bad.”


- What would you want to see in a review of your own code?

- Clear, specific explanations of problems.
- Example code showing a safer or cleaner approach.
- Prioritization (what must be fixed now vs. what can wait).
- Respectful tone that assumes good intent.


---

---

## Real-World Application

These are the exact types of issues you'll encounter in professional code reviews:
- **Hardcoded secrets** appear in ~15% of repositories
- **SQL injection** remains a top security vulnerability
- **Weak password hashing** affects millions of users
- **Missing input validation** leads to data breaches

The review skills you practice here directly apply to protecting your team's production systems.



