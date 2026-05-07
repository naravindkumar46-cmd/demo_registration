# Project: Python User Registration System

## 1. Objective
Build a secure, standalone web page for user registration.

## 2. Technical Stack
- **Backend:** Python with Flask
- **Database:** SQLite (local `users.db`)
- **Security:** Password hashing using `werkzeug.security` (built-in with Flask) or `bcrypt`.
- **Frontend:** HTML5, CSS3 (using Tailwind CSS for layout).

## 3. Functional Requirements
### A. Registration Form
- **Fields:**
  - `username`: String (min 4, max 20 chars).
  - `email`: Valid email format (e.g., user@example.com).
  - `password`: String (min 8 chars, must contain at least one number).
  - `confirm_password`: Must exactly match the `password` field.
- **Action:** A "Register" button that POSTS data to the backend.

### B. Backend Logic
- **Validation:** - Reject empty fields.
  - Check if `username` or `email` already exists in the SQLite database.
  - Validate email syntax.
- **Security:** - Hash the password before storage. **Never** store plain text.
- **Persistence:** - Save valid users to the `users` table.

### C. UI/UX
- **Messages:** Show a green success message after registration.
- **Errors:** Show red alert messages for validation failures (e.g., "Email already taken").
- **Style:** A modern, centered card-style layout.

## 4. Database Schema
| Column | Type | Constraints |
| :--- | :--- | :--- |
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| username | TEXT | UNIQUE, NOT NULL |
| email | TEXT | UNIQUE, NOT NULL |
| password_hash | TEXT | NOT NULL |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

## 5. Non-Functional Requirements
- **Code Style:** Follow PEP 8 standards.
- **Structure:** Separate logic into `app.py` and templates into a `templates/` folder.