"""
Database Schema Documentation

This file documents the SQLite database schema used by the Flask registration system.
"""

# ============================================================================
# DATABASE SCHEMA
# ============================================================================

# Table: users
# Purpose: Stores user registration data with secure password hashing
# 
# CREATE TABLE users (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     username TEXT UNIQUE NOT NULL,
#     email TEXT UNIQUE NOT NULL,
#     password_hash TEXT NOT NULL,
#     created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
# );
#
# CREATE INDEX ix_users_username ON users (username);
# CREATE INDEX ix_users_email ON users (email);

# ============================================================================
# COLUMN DESCRIPTIONS
# ============================================================================

"""
Column: id
- Type: INTEGER
- Constraints: PRIMARY KEY AUTOINCREMENT
- Description: Unique user identifier automatically generated on insert
- Example: 1, 2, 3

Column: username
- Type: TEXT
- Constraints: UNIQUE, NOT NULL
- Description: Unique username chosen by user during registration
- Validation: 4-20 characters, starts with letter, alphanumeric + underscore
- Example: 'john_doe', 'user123', 'jsmith'

Column: email
- Type: TEXT
- Constraints: UNIQUE, NOT NULL
- Description: Unique email address for user communication
- Validation: Valid email format, max 120 characters
- Example: 'john@example.com', 'user@domain.co.uk'

Column: password_hash
- Type: TEXT
- Constraints: NOT NULL
- Description: Hashed password using PBKDF2-SHA256
- Details:
  - Algorithm: pbkdf2:sha256
  - Salt length: 16 bytes
  - Iterations: 600,000+
  - Never stores plain text
  - Format: 'pbkdf2:sha256$...$...'
- Example: 'pbkdf2:sha256$260000$...$...'

Column: created_at
- Type: TIMESTAMP
- Constraints: NOT NULL, DEFAULT CURRENT_TIMESTAMP
- Description: Timestamp when user registered
- Format: ISO 8601 (YYYY-MM-DD HH:MM:SS)
- Example: '2024-05-07 12:30:45'
"""

# ============================================================================
# INDEXES
# ============================================================================

"""
Index: ix_users_username
- Columns: username
- Purpose: Faster lookups when checking for duplicate usernames
- Query Performance: O(log n) instead of O(n)

Index: ix_users_email
- Columns: email
- Purpose: Faster lookups when checking for duplicate emails
- Query Performance: O(log n) instead of O(n)

Both indexes are created automatically by SQLAlchemy due to:
- UNIQUE constraints (SQLAlchemy automatically indexes unique columns)
- index=True parameter in column definition
"""

# ============================================================================
# SAMPLE QUERIES
# ============================================================================

"""
1. Get all users:
   SELECT * FROM users;

2. Get user by username:
   SELECT * FROM users WHERE username = 'john_doe';

3. Get user by email:
   SELECT * FROM users WHERE email = 'john@example.com';

4. Count total users:
   SELECT COUNT(*) FROM users;

5. Get users created in last 7 days:
   SELECT * FROM users
   WHERE created_at >= datetime('now', '-7 days')
   ORDER BY created_at DESC;

6. Check if username exists:
   SELECT EXISTS(SELECT 1 FROM users WHERE username = 'john_doe');

7. Check if email exists:
   SELECT EXISTS(SELECT 1 FROM users WHERE email = 'john@example.com');

8. Get users by creation date:
   SELECT username, email, created_at FROM users
   ORDER BY created_at DESC;

9. Get user count by date:
   SELECT DATE(created_at) as registration_date, COUNT(*) as count
   FROM users
   GROUP BY DATE(created_at)
   ORDER BY registration_date DESC;

10. Get all users with email domain:
    SELECT username, email, 
           substr(email, instr(email, '@') + 1) as domain
    FROM users
    ORDER BY domain, username;
"""

# ============================================================================
# DATABASE OPERATIONS IN APPLICATION
# ============================================================================

"""
Database operations are performed using SQLAlchemy ORM:

1. Create new user:
   user = User(username='john_doe', email='john@example.com')
   user.set_password('SecurePass123')
   db.session.add(user)
   db.session.commit()

2. Query user by username:
   user = User.query.filter_by(username='john_doe').first()

3. Query user by email:
   user = User.query.filter_by(email='john@example.com').first()

4. Check if username exists:
   exists = User.query.filter_by(username='john_doe').first() is not None

5. Check if email exists:
   exists = User.query.filter_by(email='john@example.com').first() is not None

6. Delete user:
   user = User.query.filter_by(username='john_doe').first()
   if user:
       db.session.delete(user)
       db.session.commit()

7. Update user email:
   user = User.query.filter_by(username='john_doe').first()
   if user:
       user.email = 'newemail@example.com'
       db.session.commit()

8. Get all users:
   users = User.query.all()

9. Get users paginated:
   users = User.query.paginate(page=1, per_page=10)

10. Get total user count:
    count = User.query.count()
"""

# ============================================================================
# CONSTRAINTS AND RELATIONSHIPS
# ============================================================================

"""
PRIMARY KEY Constraint:
- id is the primary key
- Ensures each user has a unique identifier
- Auto-incremented for each new row
- Used for internal references and indexing

UNIQUE Constraints:
- username is UNIQUE
  - Prevents duplicate usernames
  - Enforced at database level
  - Checked during registration
  
- email is UNIQUE
  - Prevents duplicate emails
  - Enforced at database level
  - Checked during registration

NOT NULL Constraints:
- username: Must provide value
- email: Must provide value
- password_hash: Must provide value
- created_at: Automatically set if not provided

DEFAULT Constraint:
- created_at: Automatically set to CURRENT_TIMESTAMP if not provided
"""

# ============================================================================
# PERFORMANCE CONSIDERATIONS
# ============================================================================

"""
Indexes:
- username and email have indexes for fast lookups
- Lookup time: O(log n) vs O(n) for full table scan
- Important for duplicate checking during registration

Unique Constraints:
- Enforced at database level
- Faster than application-level checks
- Reduces database queries

Database File:
- SQLite stores all data in users.db
- File size grows with number of users
- Typical user record: ~200-300 bytes
- 10,000 users: ~3MB

Connection:
- SQLAlchemy manages connection pooling
- Limits number of open connections
- Reduces database overhead
"""

# ============================================================================
# DATA INTEGRITY
# ============================================================================

"""
Data Validation:
1. Application layer (validators.py):
   - Username format and length
   - Email format and length
   - Password strength
   - Duplicate checking before insert

2. Database layer:
   - UNIQUE constraints
   - NOT NULL constraints
   - Length constraints (via TEXT type)

Referential Integrity:
- No foreign keys (users is standalone table)
- Future: Add references for orders, sessions, etc.

Password Security:
- Passwords are hashed, never stored plain text
- Hash verification uses check_password() method
- Salt is part of the hash string
- Cannot reverse engineer password from hash
"""

# ============================================================================
# BACKUP AND RECOVERY
# ============================================================================

"""
Backup:
- SQLite database is single file: users.db
- Can be backed up by copying the file
- Consider backing up regularly in production

Recovery:
- Restore from backup by replacing users.db
- No transaction logs to recover

Migrations:
- If schema changes needed, use Alembic
- Can add/remove columns without data loss
- Consider carefully before removing columns
"""

# ============================================================================
# MONITORING AND MAINTENANCE
# ============================================================================

"""
Check database integrity:
   PRAGMA integrity_check;

Optimize database:
   VACUUM;

Get database statistics:
   SELECT page_count * page_size as size_bytes FROM pragma_page_count(), pragma_page_size();

Get table size:
   SELECT page_count * page_size as size_bytes FROM pragma_page_count() WHERE table='users';

Check for unused indexes:
   PRAGMA index_info(ix_users_username);
   PRAGMA index_info(ix_users_email);

Get SQLite version:
   PRAGMA database_list;
"""
