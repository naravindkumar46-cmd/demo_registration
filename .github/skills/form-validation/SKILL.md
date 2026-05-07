---
name: form-validation
description: "Use when implementing comprehensive form validation for user inputs including email format, password strength, and duplicate checking."
---

# Form Validation & Input Sanitization

## Password Validation Rules

### Strength Requirements

```python
import re

def validate_password(password):
    """
    Password must:
    - Be at least 8 characters long
    - Contain at least one number
    - Contain at least one uppercase letter (recommended)
    - NOT be a common password
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password should contain an uppercase letter"
    
    # Check against common passwords
    COMMON_PASSWORDS = {'password', '12345678', 'qwerty', 'abc12345'}
    if password.lower() in COMMON_PASSWORDS:
        return False, "Password is too common"
    
    return True, "Valid"
```

## Email Validation

```python
import re

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return False, "Invalid email format"
    
    if len(email) > 120:
        return False, "Email is too long"
    
    return True, "Valid"
```

## Username Validation

```python
def validate_username(username):
    """
    Username must:
    - Be 4-20 characters
    - Contain only alphanumeric and underscore
    - Start with letter
    """
    if len(username) < 4 or len(username) > 20:
        return False, "Username must be 4-20 characters"
    
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', username):
        return False, "Username must start with a letter and contain only letters, numbers, and underscores"
    
    return True, "Valid"
```

## Complete Validation Function

```python
def validate_registration_form(data):
    """Validate all registration fields"""
    errors = {}
    
    # Username validation
    username = data.get('username', '').strip()
    if not username:
        errors['username'] = 'Username is required'
    else:
        is_valid, msg = validate_username(username)
        if not is_valid:
            errors['username'] = msg
    
    # Email validation
    email = data.get('email', '').strip()
    if not email:
        errors['email'] = 'Email is required'
    else:
        is_valid, msg = validate_email(email)
        if not is_valid:
            errors['email'] = msg
    
    # Password validation
    password = data.get('password', '')
    if not password:
        errors['password'] = 'Password is required'
    else:
        is_valid, msg = validate_password(password)
        if not is_valid:
            errors['password'] = msg
    
    # Confirm password
    confirm_password = data.get('confirm_password', '')
    if password and confirm_password != password:
        errors['confirm_password'] = 'Passwords do not match'
    
    return len(errors) == 0, errors
```

## Frontend Validation (UX Only)

```html
<form id="registrationForm">
    <input 
        type="text" 
        name="username" 
        minlength="4" 
        maxlength="20" 
        required
        pattern="^[a-zA-Z][a-zA-Z0-9_]*$"
        title="Username must start with letter, 4-20 chars, letters/numbers/underscore only"
    >
    
    <input 
        type="email" 
        name="email" 
        required
        title="Enter a valid email address"
    >
    
    <input 
        type="password" 
        name="password" 
        minlength="8" 
        required
        title="At least 8 characters with a number"
    >
    
    <input 
        type="password" 
        name="confirm_password" 
        required
    >
</form>
```

## Input Sanitization

```python
from html import escape

def sanitize_input(value):
    """Prevent XSS by escaping HTML characters"""
    if isinstance(value, str):
        return escape(value.strip())
    return value

# Always sanitize before storing
username = sanitize_input(data['username'])
email = sanitize_input(data['email'])
```

## Backend Validation Checklist

- ✅ Always validate on backend (never trust frontend)
- ✅ Trim whitespace
- ✅ Check length limits
- ✅ Validate format with regex
- ✅ Escape HTML characters
- ✅ Check for duplicates in database
- ✅ Return specific error messages
- ✅ Log validation failures for security monitoring
