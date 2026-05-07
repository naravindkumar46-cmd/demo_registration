---
name: flask-security
description: "Use when implementing secure password hashing and authentication in Flask applications."
---

# Flask Security Best Practices

## Password Hashing

Never store plain text passwords. Use `werkzeug.security` (built-in with Flask) or `bcrypt`.

### Option 1: werkzeug.security (Built-in)

```python
from werkzeug.security import generate_password_hash, check_password_hash

# Hash password before storing
password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

# Verify password during login
is_valid = check_password_hash(password_hash, user_input_password)
```

### Option 2: bcrypt (Recommended for production)

```python
import bcrypt

# Hash password
password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))

# Verify password
is_valid = bcrypt.checkpw(user_input_password.encode('utf-8'), password_hash)
```

## User Model Example

```python
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
```

## Secure Registration Route

```python
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Backend validation (ALWAYS required)
    if not data.get('username') or not data.get('email') or not data.get('password'):
        return {'error': 'Missing required fields'}, 400
    
    # Check if user exists
    if User.query.filter_by(username=data['username']).first():
        return {'error': 'Username already taken'}, 409
    
    if User.query.filter_by(email=data['email']).first():
        return {'error': 'Email already registered'}, 409
    
    # Create new user
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return {'message': 'User registered successfully'}, 201
```

## Key Security Rules

1. ✅ Always hash passwords—never store plain text
2. ✅ Use salt (automatically handled by werkzeug/bcrypt)
3. ✅ Use proper cost factors (12+ rounds for bcrypt)
4. ✅ Validate input on backend, not just frontend
5. ✅ Use prepared statements (ORM handles this)
6. ✅ Return generic error messages to prevent user enumeration
7. ✅ HTTPS only in production
8. ✅ Implement rate limiting on registration endpoint
