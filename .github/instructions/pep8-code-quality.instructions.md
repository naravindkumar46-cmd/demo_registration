---
applyTo: "**/*.py"
description: "PEP 8 code style standards and Python best practices for all Python files."
---

# PEP 8 & Code Quality Standards

All Python code must follow PEP 8 standards and best practices for readability and maintainability.

## Naming Conventions

```python
# ✅ CORRECT
class UserRegistration:  # PascalCase for classes
    def register_user(self, username):  # snake_case for functions
        MAX_USERNAME_LENGTH = 20  # UPPER_CASE for constants
        is_valid = True  # leading lowercase for variables
        
# ❌ WRONG
class user_registration:  # Should be PascalCase
    def RegisterUser(self):  # Should be snake_case
        maxUsernameLength = 20  # Should be UPPER_CASE
```

## Line Length & Formatting

```python
# ✅ CORRECT: 79 characters per line (PEP 8 standard)
error_message = (
    "Username must be between 4 and 20 characters "
    "and contain only letters, numbers, and underscores."
)

# ✅ CORRECT: 4-space indentation
def validate_form(data):
    if 'username' in data:
        username = data['username']
        return validate_username(username)

# ❌ WRONG: Exceeds 79 characters
error_message = "Username must be between 4 and 20 characters and contain only letters, numbers, and underscores."

# ❌ WRONG: Inconsistent indentation (tabs vs spaces)
def validate_form(data):
→   if 'username' in data:  # TAB (incorrect)
    return True  # SPACES (correct)
```

## Imports

```python
# ✅ CORRECT: Group imports in order
import os
import sys
from datetime import datetime

from flask import Flask, request
from werkzeug.security import generate_password_hash

import myapp.models

# ❌ WRONG: Unsorted, mixed
from myapp.models import User
import sys
from flask import Flask
import os
from werkzeug.security import generate_password_hash
```

## Docstrings & Comments

```python
# ✅ CORRECT: Module docstring
"""
User registration module.

Handles user registration, validation, and database persistence.
"""

def validate_email(email: str) -> tuple[bool, str]:
    """
    Validate email format and length.
    
    Args:
        email: The email address to validate.
    
    Returns:
        A tuple of (is_valid: bool, error_message: str)
    
    Raises:
        ValueError: If email is None or not a string.
    """
    if not email:
        raise ValueError("Email cannot be empty")
    
    # Check format with regex
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        return False, "Invalid email format"
    
    return True, ""

# ❌ WRONG: Missing docstring
def check_email(e):
    # returns true if valid
    return '@' in e
```

## Type Hints

```python
# ✅ CORRECT: Add type hints to all functions
from typing import Optional, Dict, Tuple

def create_user(
    username: str,
    email: str,
    password: str
) -> Dict[str, any]:
    """Create and store a new user."""
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return {'id': user.id, 'username': user.username}

def get_user(user_id: int) -> Optional['User']:
    """Retrieve user by ID or None if not found."""
    return User.query.get(user_id)

# ❌ WRONG: No type hints
def create_user(username, email, password):
    return user
```

## Error Handling

```python
# ✅ CORRECT: Specific exception handling
try:
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
except IntegrityError:
    db.session.rollback()
    logger.warning(f"Duplicate user attempt: {email}")
    return {'error': 'Email already exists'}, 409
except Exception as e:
    db.session.rollback()
    logger.error(f"Unexpected error: {e}")
    return {'error': 'Registration failed'}, 500

# ❌ WRONG: Bare except clause
try:
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
except:  # Catches everything, including KeyboardInterrupt!
    return 'Error', 500
```

## Code Organization

```
project/
├── app.py                 # Main Flask app
├── config.py              # Configuration
├── requirements.txt       # Dependencies
├── models.py              # Database models
├── routes.py              # Route handlers
├── validators.py          # Validation functions
├── utils.py               # Utility functions
└── templates/
    ├── base.html
    └── register.html
```

## PEP 8 Quick Reference

| Rule | Standard | Example |
|------|----------|---------|
| Line length | 79 chars | Long lines split across multiple |
| Indentation | 4 spaces | Consistent, no tabs |
| Variable names | snake_case | `user_email`, `password_hash` |
| Class names | PascalCase | `class UserModel` |
| Constants | UPPER_CASE | `MAX_ATTEMPTS = 5` |
| Functions | snake_case | `def register_user()` |
| Imports | Grouped & sorted | stdlib, third-party, local |
| Docstrings | Triple quotes | `"""Description"""` |

## Auto-Formatting Tools

```bash
# Install formatters
pip install black flake8 autopep8

# Format code automatically
black app.py
autopep8 --in-place app.py

# Check for PEP 8 violations
flake8 app.py
```

## Pre-commit Configuration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
  
  - repo: https://github.com/PyCQA/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
```
