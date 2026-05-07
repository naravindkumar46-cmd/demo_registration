---
name: "Python Registration System"
description: "Coordinate all agents, skills, and instructions for secure, professional user registration system development."
---

# Python User Registration System - Complete Implementation Guide

## Project Overview

Build a secure Flask-based user registration system with:
- **Backend**: Flask web framework with SQLite database
- **Frontend**: HTML5 + CSS3 with Tailwind CSS
- **Security**: Password hashing, input validation, OWASP compliance
- **Quality**: PEP 8 standards, comprehensive testing

## Available Agents

### 1. **Backend Developer - Flask**
**When to use**: Building `app.py`, routes, database operations, business logic
- Initialize Flask app and database
- Create User model with SQLAlchemy
- Implement `/register` endpoint
- Handle validation and error responses

**Try**: "Use Backend Developer to create the Flask app structure and /register route"

### 2. **Frontend Developer - HTML/CSS**
**When to use**: Building registration form, styling, responsive design
- Create HTML registration form
- Apply Tailwind CSS styling
- Add responsive design
- Implement error/success message display

**Try**: "Use Frontend Developer to build the registration form template"

### 3. **Security Specialist**
**When to use**: Implementing security measures, reviewing for vulnerabilities
- Review password hashing implementation
- Audit input validation
- Check OWASP compliance
- Recommend security improvements

**Try**: "Use Security Specialist to audit the registration endpoint for vulnerabilities"

### 4. **Database Designer**
**When to use**: Designing schema, managing migrations, optimizing queries
- Create users table schema
- Define constraints and indexes
- Plan migrations (if needed)
- Optimize database queries

**Try**: "Use Database Designer to create the SQLite schema for the users table"

## Available Skills

### 1. **Flask Security Best Practices** (`#skill:flask-security`)
Comprehensive guide for:
- Password hashing with bcrypt or werkzeug
- User model creation with proper constraints
- Secure registration route implementation
- Security rules and patterns

### 2. **Form Validation & Input Sanitization** (`#skill:form-validation`)
Complete validation reference for:
- Password strength requirements
- Email format validation
- Username validation rules
- Backend validation implementation
- Input sanitization techniques

## File-Level Instructions

### 1. **Security Requirements** (applies to `app.py`, `models.py`, `routes.py`)
- OWASP Top 10 compliance checklist
- Password security implementation
- Input validation requirements
- Error handling standards
- Rate limiting
- Environment variables for secrets

### 2. **PEP 8 & Code Quality** (applies to all `**/*.py`)
- Naming conventions
- Line length and formatting
- Import organization
- Docstrings and type hints
- Error handling best practices
- Code organization structure

## Project Structure

```
project/
├── .github/
│   ├── agents/
│   │   ├── backend-developer.agent.md
│   │   ├── frontend-developer.agent.md
│   │   ├── security-specialist.agent.md
│   │   └── database-designer.agent.md
│   ├── skills/
│   │   ├── flask-security/SKILL.md
│   │   └── form-validation/SKILL.md
│   └── instructions/
│       ├── security-registration.instructions.md
│       └── pep8-code-quality.instructions.md
├── app.py                    # Main Flask app
├── models.py                 # SQLAlchemy models
├── config.py                 # Configuration
├── requirements.txt          # Dependencies
└── templates/
    ├── base.html             # Base template
    └── register.html         # Registration form
```

## Implementation Workflow

### Step 1: Database Design
```
Request: "Use Database Designer to create the SQLite schema"
Output: User model with proper constraints and indexes
```

### Step 2: Backend Development
```
Request: "Use Backend Developer to implement Flask app and /register route"
Required skills: #skill:flask-security, #skill:form-validation
Output: app.py, models.py, routes.py with security best practices
```

### Step 3: Frontend Development
```
Request: "Use Frontend Developer to build the registration form"
Output: register.html with Tailwind CSS styling and responsive design
```

### Step 4: Security Review
```
Request: "Use Security Specialist to audit the registration system"
Output: Security audit report with recommendations
```

### Step 5: Testing
```
Request: "Use Test Case Generator to create comprehensive tests"
Output: pytest test suite with unit, integration, and edge case tests
```

## Key Requirements Summary

### Functional Requirements
- ✅ Registration form with username, email, password, confirm_password
- ✅ Backend validation for all inputs
- ✅ Duplicate username/email checking
- ✅ Password hashing before storage
- ✅ Success and error message display

### Security Requirements
- ✅ Password hashing with bcrypt/werkzeug (never plain text)
- ✅ Backend validation (don't trust frontend)
- ✅ SQL injection prevention (use ORM)
- ✅ Input sanitization
- ✅ Rate limiting (max 5 attempts/minute)
- ✅ Generic error messages (prevent user enumeration)
- ✅ Secure session cookies
- ✅ Environment variables for secrets

### Code Quality Requirements
- ✅ PEP 8 compliance
- ✅ Type hints on all functions
- ✅ Docstrings and comments
- ✅ Proper error handling
- ✅ Logging for monitoring
- ✅ Modular structure

## Example Prompts

1. **"Set up the database using Database Designer to create the users table schema"**
2. **"Use Backend Developer to build the Flask app with secure registration endpoint"**
3. **"Use Frontend Developer to create a modern registration form with Tailwind CSS"**
4. **"Use Security Specialist to review for OWASP vulnerabilities"**
5. **"Use Test Case Generator to create comprehensive pytest test suite"**

## Security Checklist

Before deployment:
- [ ] Passwords hashed with bcrypt (12+ rounds)
- [ ] Backend validation on all inputs
- [ ] Rate limiting enabled
- [ ] Error messages are generic
- [ ] No hardcoded secrets
- [ ] HTTPS configured
- [ ] Dependencies audited (`pip audit`)
- [ ] Logging and monitoring in place
- [ ] Test coverage > 80%
- [ ] Code reviewed for PEP 8 compliance

## Dependencies

```
Flask==2.3.0
Flask-SQLAlchemy==3.0.0
bcrypt==4.0.0
python-dotenv==1.0.0
werkzeug==2.3.0
```

## Helpful Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py

# Run tests
pytest tests/ -v

# Check PEP 8
flake8 app.py

# Format code
black app.py

# Check for security issues
pip audit
```
