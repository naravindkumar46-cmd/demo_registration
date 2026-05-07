# Quick Start Guide - Flask Registration System

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Step 1: Setup Virtual Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# On macOS/Linux:
# source venv/bin/activate
```

## Step 2: Install Dependencies

```powershell
pip install -r requirements.txt
```

## Step 3: Run the Application

```powershell
python app.py
```

You should see:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

## Step 4: Test the Application

### Option A: Using cURL

```powershell
# Test successful registration
curl -X POST http://127.0.0.1:5000/register `
  -H "Content-Type: application/json" `
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPass123",
    "confirm_password": "TestPass123"
  }'

# Test duplicate username
curl -X POST http://127.0.0.1:5000/register `
  -H "Content-Type: application/json" `
  -d '{
    "username": "testuser",
    "email": "other@example.com",
    "password": "OtherPass456",
    "confirm_password": "OtherPass456"
  }'
```

### Option B: Using Python Script

```powershell
python test_registration.py
```

This will run comprehensive tests covering:
- ✅ Valid registration
- ✅ Duplicate username/email
- ✅ Password validation
- ✅ Email validation
- ✅ Username validation
- ✅ Error handling

### Option C: Using Python Requests

```powershell
python
```

Then in Python:

```python
import requests

response = requests.post(
    'http://127.0.0.1:5000/register',
    json={
        'username': 'pyuser',
        'email': 'py@example.com',
        'password': 'PyPass123',
        'confirm_password': 'PyPass123'
    }
)

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

## Step 5: View Database

### Using Python

```python
import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('SELECT username, email, created_at FROM users')
print(cursor.fetchall())
conn.close()
```

### Using SQLite CLI

```powershell
sqlite3 users.db
sqlite> SELECT * FROM users;
sqlite> .exit
```

## Project Files

| File | Purpose |
|------|---------|
| `app.py` | Main Flask application with routes |
| `models.py` | SQLAlchemy User model |
| `validators.py` | Input validation functions |
| `config.py` | Configuration management |
| `requirements.txt` | Python dependencies |
| `test_registration.py` | Test suite |
| `README.md` | Full documentation |
| `.env.example` | Environment variable template |
| `.gitignore` | Git ignore rules |
| `users.db` | SQLite database (created automatically) |

## Validation Rules

### Username
- 4-20 characters
- Start with letter
- Only letters, numbers, underscore
- Must be unique

### Email
- Valid email format
- Max 120 characters
- Must be unique

### Password
- Minimum 8 characters
- Must contain at least one number
- Cannot be common (password123, etc)

### Confirm Password
- Must match password exactly

## API Response Codes

| Code | Meaning | Scenario |
|------|---------|----------|
| 201 | Created | User registered successfully |
| 400 | Bad Request | Validation error |
| 409 | Conflict | Username or email exists |
| 429 | Too Many Requests | Rate limited (5/minute) |
| 500 | Server Error | Unexpected error |

## Troubleshooting

### Port 5000 already in use

Edit `app.py` and change:
```python
app.run(host='127.0.0.1', port=5001)
```

### Module not found error

Make sure virtual environment is activated:
```powershell
venv\Scripts\activate
```

Then reinstall dependencies:
```powershell
pip install -r requirements.txt
```

### Database locked error

Delete `users.db` and restart the app:
```powershell
# Stop the app (Ctrl+C)
# Delete the database file
del users.db
# Start app again
python app.py
```

## Security Features Implemented

✅ Password hashing (PBKDF2-SHA256)
✅ Input validation
✅ Rate limiting
✅ SQL injection prevention (SQLAlchemy ORM)
✅ Generic error messages
✅ Security logging
✅ OWASP compliance
✅ Type hints
✅ PEP 8 standards

## Next Steps

1. **Add Frontend**: Create HTML form in `templates/` folder
2. **Add Login**: Implement authentication endpoint
3. **Add Email Verification**: Send confirmation emails
4. **Add Password Reset**: Implement recovery mechanism
5. **Deploy**: Use Gunicorn/uWSGI with Nginx

## Support

For detailed documentation, see `README.md`
