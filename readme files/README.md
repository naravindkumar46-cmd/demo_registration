# Flask User Registration System

A secure, production-ready Flask backend for user registration with proper validation, password hashing, and OWASP compliance.

## Features

- ✅ Secure password hashing using `werkzeug.security` (PBKDF2-SHA256)
- ✅ Comprehensive input validation (username, email, password)
- ✅ Duplicate checking for username and email
- ✅ Rate limiting (5 requests per minute per IP)
- ✅ SQLite database with SQLAlchemy ORM
- ✅ PEP 8 compliant code with type hints
- ✅ Proper HTTP status codes (201, 400, 409, 500)
- ✅ Security logging for registration events
- ✅ OWASP Top 10 compliance

## Project Structure

```
.
├── app.py              # Main Flask application and routes
├── config.py           # Configuration management (dev, test, prod)
├── models.py           # SQLAlchemy User model
├── validators.py       # Input validation functions
├── requirements.txt    # Python dependencies
├── users.db           # SQLite database (created automatically)
└── README.md          # This file
```

## Installation

### 1. Clone the repository or create the project directory

```bash
cd TEST_DEMO
```

### 2. Create a virtual environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

### Development Mode

```bash
# Windows
python app.py

# macOS/Linux
python3 app.py
```

The server will start at `http://127.0.0.1:5000`

### Production Mode

```bash
# Set environment variables
set FLASK_ENV=production    # Windows
export FLASK_ENV=production # macOS/Linux

set DEBUG=False             # Windows
export DEBUG=False          # macOS/Linux

python app.py
```

## API Endpoints

### Health Check

```bash
GET /health
```

Response:
```json
{
  "status": "ok"
}
```

### User Registration

```bash
POST /register
Content-Type: application/json
```

**Request Body:**

```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123",
  "confirm_password": "SecurePass123"
}
```

**Success Response (201 Created):**

```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "created_at": "2024-05-07T12:30:45.123456"
  }
}
```

**Validation Error (400 Bad Request):**

```json
{
  "error": "Registration failed",
  "details": {
    "password": "Password must be at least 8 characters",
    "confirm_password": "Passwords do not match"
  }
}
```

**Username/Email Already Exists (409 Conflict):**

```json
{
  "error": "Registration failed. Username or email already exists."
}
```

**Rate Limited (429 Too Many Requests):**

```json
{
  "error": "Too many requests. Please try again later."
}
```

## Validation Rules

### Username
- Length: 4-20 characters
- Pattern: Must start with a letter, contain only letters, numbers, and underscores
- Uniqueness: Must not already exist in database

**Examples:**
- ✅ Valid: `john_doe`, `user123`, `jsmith`
- ❌ Invalid: `jo`, `john-doe`, `@john`, `123user`

### Email
- Format: Must be valid email format
- Length: Max 120 characters
- Uniqueness: Must not already exist in database

**Examples:**
- ✅ Valid: `user@example.com`, `john.doe@company.co.uk`
- ❌ Invalid: `invalid.email`, `user@`, `@example.com`

### Password
- Length: Minimum 8 characters
- Requirements: Must contain at least one number
- Weakness: Not a common password (e.g., "password123")

**Examples:**
- ✅ Valid: `SecurePass123`, `MyP@ss2024`, `StrongPassword1`
- ❌ Invalid: `short1`, `NoNumbers`, `password123`, `12345678`

### Confirm Password
- Must exactly match the password field

## Security Features

### Password Hashing

- **Algorithm**: PBKDF2-SHA256 (via werkzeug.security)
- **Salt**: Automatically generated (16 bytes)
- **Iterations**: 600,000+ (werkzeug default)
- **Storage**: Never stores plain text passwords

### Input Validation

- Backend validation is enforced (frontend cannot bypass)
- All inputs are trimmed and validated
- Email syntax checked with regex pattern
- Username pattern validation prevents injection

### Rate Limiting

- Maximum 5 registration attempts per minute per IP address
- Prevents brute force and abuse

### Error Messages

- Generic error messages prevent user enumeration
- Doesn't reveal whether username or email exists
- Detailed validation errors for developers (in `details` field)

### Database Security

- SQLAlchemy ORM prevents SQL injection
- No raw SQL queries
- Parameterized queries for all database operations

### Logging

- All registration events are logged
- Failed attempts are recorded
- Rate limit violations are tracked
- Errors are logged for debugging

## Testing

### Test with cURL

```bash
# Create a test user
curl -X POST http://127.0.0.1:5000/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPass123",
    "confirm_password": "TestPass123"
  }'

# Try duplicate username
curl -X POST http://127.0.0.1:5000/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "another@example.com",
    "password": "AnotherPass456",
    "confirm_password": "AnotherPass456"
  }'

# Invalid password (no numbers)
curl -X POST http://127.0.0.1:5000/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "new@example.com",
    "password": "NoNumbers",
    "confirm_password": "NoNumbers"
  }'
```

### Test with Python

```python
import requests

base_url = 'http://127.0.0.1:5000'

# Register a user
response = requests.post(
    f'{base_url}/register',
    json={
        'username': 'python_user',
        'email': 'python@example.com',
        'password': 'PythonPass123',
        'confirm_password': 'PythonPass123'
    }
)

print(response.status_code)
print(response.json())
```

## Database

The application uses SQLite with the following schema:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_users_username ON users (username);
CREATE INDEX ix_users_email ON users (email);
```

To inspect the database:

```bash
# Using sqlite3 CLI
sqlite3 users.db

# SQL query examples
sqlite> SELECT * FROM users;
sqlite> SELECT username, email, created_at FROM users ORDER BY created_at DESC;
sqlite> SELECT COUNT(*) FROM users;
```

## Configuration

Edit `config.py` to customize:

- **DATABASE_URL**: SQLite database file location
- **FLASK_ENV**: Environment (development, testing, production)
- **DEBUG**: Enable/disable debug mode
- **SESSION_COOKIE_***: Session cookie security settings
- **MAX_CONTENT_LENGTH**: Maximum request size

## Deployment

### Environment Variables

Create a `.env` file for production:

```bash
FLASK_ENV=production
DEBUG=False
DATABASE_URL=sqlite:///users.db
```

### Running with Gunicorn (Production)

```bash
pip install gunicorn

gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Running with uWSGI

```bash
pip install uwsgi

uwsgi --http :5000 --wsgi-file app.py --callable app --processes 4 --threads 2
```

## Security Checklist

- ✅ Passwords hashed with strong algorithm (PBKDF2-SHA256)
- ✅ Backend validation enforced (not just frontend)
- ✅ Input sanitization and validation
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ Generic error messages (prevents user enumeration)
- ✅ Rate limiting on registration
- ✅ HTTPS ready (secure cookies configured)
- ✅ Logging for security events
- ✅ Environment variables for secrets (not hardcoded)
- ✅ OWASP Top 10 compliance

## Common Issues

### Issue: "ModuleNotFoundError: No module named 'flask'"

**Solution**: Make sure you've activated the virtual environment and installed dependencies:

```bash
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Issue: "Database is locked"

**Solution**: Close any other connections to the database and restart the application.

### Issue: Port 5000 already in use

**Solution**: Change the port in `app.py`:

```python
app.run(host='127.0.0.1', port=5001)  # Use 5001 instead
```

## Code Quality

- **PEP 8**: Full compliance with Python style guide
- **Type Hints**: Complete type annotations
- **Docstrings**: Module, function, and method docstrings
- **Error Handling**: Comprehensive exception handling
- **Logging**: Security events and errors logged

## License

This project is provided as-is for educational and development purposes.

## Support

For issues or questions, review the code comments and docstrings for detailed explanations of each component.
