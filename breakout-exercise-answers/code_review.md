```markdown
## Code Review Comments

**🔴 SECURITY: Hard coded API key**
**Line 19:** hard coded API key
**Impact:** the API key would be posted on a commit, making it publically visible and susceptible to abuse
**Suggestion:** 
```python
# Instead of this vulnerable code:
API_KEY = "sk-live-1234567890abcdef"

# Use this secure approach:
api_key = os.environ.get("API_KEY")
```
**Priority:** Critical


```markdown
## Code Review Comments

**🔴 SECURITY: SQL injection and plaintext password storage**
**Line 25, 38:** f strings allow arbitrary sql to be injected. also, passwords are stored plaintext
**Impact:** attacker could run arbitrary queries and exfiltrate data or delete data. passwords can also be stolen
**Suggestion:** 
```python
# Instead of this vulnerable code:
query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"

# Use this secure approach:
query = f"SELECT * FROM users WHERE username=? AND password=?"
cursor.execute(query, (username, hashed(password)))
```
**Priority:** Critical

```markdown
## Code Review Comments

**🔴 SECURITY: printing plaintext password**
**Line 29:** plaintext password attempt is printed to the screen
**Impact:** someone could read the password 
**Suggestion:** 
```python
# Instead of this vulnerable code:
query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"

# Use this secure approach:
query = f"SELECT * FROM users WHERE username=? AND password=?"
cursor.execute(query, (username, hashed(password)))
```
**Priority:** High

```markdown
## Code Review Comments

**🔴 SECURITY: insecure hashing function**
**Line 43:** md5 hashing algorithm is used, which is insecure.
**Impact:** an attacker can easily compute md5 hashes and perform a brute force attack. There is also no salting, which allows for a rainbow table attack.
**Suggestion:** 
```python
# Instead of this vulnerable code:
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

# Use this secure approach:
import bcrypt
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))
```
**Priority:** High

```markdown
## Code Review Comments

**🔴 SECURITY: hardcoded admin**
**Line 45-48:** admin is checked with a hardcoded approach. It also doesn't check with the database.
**Impact:** an attacker can submit user_id = "admin" to get admin privilges.
**Suggestion:** 
```python
# Instead of this vulnerable code:
def admin_check(user_id):
    if user_id == 1 or user_id == "admin":
        return True
    return False


# Use this secure approach:
def admin_check(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = "SELECT is_admin FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()

    if result and result[0] == 1:
        return True
    return False
```
**Priority:** Critical

**🔴 SECURITY: password is stored in plaintext, and is open to sql injection**
**Line 36-40:** password is stored in plaintext in the database. Also, f-strings allow for sql injection
**Impact:** an attacker can steal passwords and take control of the database
**Suggestion:** 
```python
# Instead of this vulnerable code:
def reset_password(user_id, new_password):
    conn = sqlite3.connect("users.db")
    query = f"UPDATE users SET password='{new_password}' WHERE id={user_id}"
    conn.execute(query)
    conn.commit()


# Use this secure approach:
def reset_password(user_id, new_password):
    conn = sqlite3.connect("users.db")
    query = "UPDATE users SET password_hash = ? WHERE id = ?"
    hashed_password = hash_password(new_password)
    cursor.execute(query, (hashed_password, user_id))
    cursor = conn.cursor()
```
**Priority:** Critical
