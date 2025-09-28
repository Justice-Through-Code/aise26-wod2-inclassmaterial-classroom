# Integration Strategy
I would first merge branch A, and then go through line by line on branch B to add the relevant features. Specifically, I would add the additional imports, the database setup, the user class declaration, and the pattern of initializing a Session object and querying the database.

# What to test
I would test for the following things:

Input validation on POST /users:
- Username too short → 400 with clear message.
- Password too short → 400 with clear message.
- Missing JSON → 400 with clear message.

Persistence and hashing:
- Successful user creation returns 201, includes id and username only.
- Database stores a bcrypt hash (not plaintext)
- Duplicate username → 401 with {"error": "invalid username or password"} 

Login with JWT:
- Wrong username → 401.
- Wrong password → 401.
- Correct credentials → 200 with token

GET /users:
- Returns list of users without passwords; 200 status.


# Possible conflicts/issues
Since we are picking features from both branches, we need to go through the code manually, line by line, to complete the merge. It can be error prone and lengthy. 