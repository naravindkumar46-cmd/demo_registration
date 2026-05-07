---
applyTo: "app.py,models.py,routes.py,auth.py"
description: "Security best practices and OWASP compliance for registration system."
---

# Security Requirements for Registration System

## OWASP Top 10 Compliance

All code must address these critical security risks:

### A01: Broken Access Control
- ✅ Implement proper authentication for protected routes
- ✅ Validate user ownership before operations

### A02: Cryptographic Failures
- ✅ Use bcrypt or werkzeug for password hashing (12+ rounds)
- ✅ Never store plain text passwords
- ✅ Always use HTTPS in production

### A03: Injection
- ✅ Use SQLAlchemy ORM (parameterized queries)
- ✅ Never concatenate user input into SQL
- ✅ Escape HTML in user-provided content

### A04: Insecure Design
- ✅ Implement rate limiting on registration endpoint (max 5 attempts/minute)
- ✅ Add CSRF protection if using traditional forms
- ✅ Validate on backend—never trust frontend validation

### A05: Security Misconfiguration
- ✅ Use environment variables for secrets (never hardcode)
- ✅ Run Flask with debug=False in production
- ✅ Set secure session cookies (secure, httponly, samesite)

### A06: Vulnerable Dependencies
- ✅ Keep Flask, SQLAlchemy, bcrypt updated
- ✅ Regularly run `pip audit` to check for vulnerabilities
- ✅ Document Python version requirements (3.8+)

### A07: Authentication Failures
- ✅ Don't expose whether username or email exists (use generic error: "Username or email already exists")
- ✅ Hash passwords with salt before storage
- ✅ Implement password strength validation

## Password Security

```python
# ✅ CORRECT: Use bcrypt or werkzeug
from werkzeug.security import generate_password_hash
password_hash = generate_password_hash(password, salt_length=16)

# ❌ WRONG: Plain text storage
user.password = password  # SECURITY RISK!

# ❌ WRONG: Weak hashing
import hashlib
password_hash = hashlib.md5(password).hexdigest()  # Vulnerable!
```

## Input Validation

```python
# ✅ CORRECT: Validate on backend
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username', '').strip()
    
    # Validate length
    if len(username) < 4 or len(username) > 20:
        return "Invalid username", 400
    
    # Check database for duplicates
    if User.query.filter_by(username=username).first():
        return "Username taken", 409

# ❌ WRONG: Trust frontend validation only
# Frontend validation is for UX, not security!
```

## Error Handling

```python
# ✅ CORRECT: Generic error messages prevent user enumeration
return {'error': 'Registration failed. Please try again.'}, 400

# ❌ WRONG: Exposing sensitive information
if User.query.filter_by(email=email).first():
    return {'error': 'Email already registered'}, 409  # Tells attacker email exists!
```

## Rate Limiting

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/register', methods=['POST'])
@limiter.limit("5 per minute")
def register():
    # Prevents brute force attacks
    pass
```

## Environment Variables

```python
# ✅ CORRECT: Use environment variables
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-only')
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///users.db')

# ❌ WRONG: Hardcoded secrets
SECRET_KEY = 'super-secret-key-123'  # EXPOSED IN GIT!
```

## Logging & Monitoring

```python
import logging

logger = logging.getLogger(__name__)

@app.route('/register', methods=['POST'])
def register():
    try:
        # validation logic
        pass
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return {'error': 'An error occurred'}, 500
```

## Security Checklist

Before deployment:
- [ ] All passwords hashed with bcrypt/werkzeug
- [ ] Backend validation on all inputs
- [ ] No hardcoded secrets
- [ ] Rate limiting enabled
- [ ] Error messages are generic
- [ ] HTTPS configured
- [ ] CSRF tokens in forms
- [ ] SQL injection prevented (using ORM)
- [ ] XSS protection (HTML escaping)
- [ ] Logging for security events
- [ ] Dependencies audited with `pip audit`
