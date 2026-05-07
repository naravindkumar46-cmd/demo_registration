"""
Input validation functions for the registration system.

This module provides comprehensive validation for username, email,
password, and registration form data.
"""

import re
from typing import Tuple


# Common weak passwords to check against
COMMON_PASSWORDS = {
    'password',
    '12345678',
    'qwerty',
    'abc12345',
    'password123',
    '123456',
    'admin',
    'letmein',
}


def validate_username(username: str) -> Tuple[bool, str]:
    """
    Validate username format and length.

    Username must:
    - Be 4-20 characters long
    - Start with a letter
    - Contain only alphanumeric characters and underscores

    Args:
        username: Username to validate.

    Returns:
        Tuple of (is_valid: bool, error_message: str)
    """
    if not username:
        return False, "Username is required"

    if not isinstance(username, str):
        return False, "Username must be a string"

    username = username.strip()

    if len(username) < 4:
        return False, "Username must be at least 4 characters"

    if len(username) > 20:
        return False, "Username must not exceed 20 characters"

    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', username):
        return False, (
            "Username must start with a letter and contain only letters, "
            "numbers, and underscores"
        )

    return True, ""


def validate_email(email: str) -> Tuple[bool, str]:
    """
    Validate email format and length.

    Args:
        email: Email address to validate.

    Returns:
        Tuple of (is_valid: bool, error_message: str)
    """
    if not email:
        return False, "Email is required"

    if not isinstance(email, str):
        return False, "Email must be a string"

    email = email.strip()

    if len(email) > 120:
        return False, "Email is too long (max 120 characters)"

    # RFC 5322 simplified email pattern
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if not re.match(email_pattern, email):
        return False, "Invalid email format"

    return True, ""


def validate_password(password: str) -> Tuple[bool, str]:
    """
    Validate password strength.

    Password must:
    - Be at least 8 characters long
    - Contain at least one number
    - Not be a common/weak password

    Args:
        password: Password to validate.

    Returns:
        Tuple of (is_valid: bool, error_message: str)
    """
    if not password:
        return False, "Password is required"

    if not isinstance(password, str):
        return False, "Password must be a string"

    if len(password) < 8:
        return False, "Password must be at least 8 characters"

    if len(password) > 128:
        return False, "Password is too long"

    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"

    if password.lower() in COMMON_PASSWORDS:
        return False, "Password is too common. Please choose a stronger password"

    return True, ""


def validate_passwords_match(
    password: str,
    confirm_password: str
) -> Tuple[bool, str]:
    """
    Validate that passwords match.

    Args:
        password: First password.
        confirm_password: Confirmation password.

    Returns:
        Tuple of (is_valid: bool, error_message: str)
    """
    if not password or not confirm_password:
        return False, "Both password fields are required"

    if password != confirm_password:
        return False, "Passwords do not match"

    return True, ""


def validate_registration_form(data: dict) -> Tuple[bool, dict]:
    """
    Validate all registration form fields.

    Args:
        data: Dictionary containing registration form data.

    Returns:
        Tuple of (is_valid: bool, errors: dict)
        errors dict contains field names as keys and error messages as values.
    """
    errors = {}

    # Validate username
    username = data.get('username', '').strip() if data.get('username') else ''
    if not username:
        errors['username'] = 'Username is required'
    else:
        is_valid, msg = validate_username(username)
        if not is_valid:
            errors['username'] = msg

    # Validate email
    email = data.get('email', '').strip() if data.get('email') else ''
    if not email:
        errors['email'] = 'Email is required'
    else:
        is_valid, msg = validate_email(email)
        if not is_valid:
            errors['email'] = msg

    # Validate password
    password = data.get('password', '')
    if not password:
        errors['password'] = 'Password is required'
    else:
        is_valid, msg = validate_password(password)
        if not is_valid:
            errors['password'] = msg

    # Validate confirm password
    confirm_password = data.get('confirm_password', '')
    if not confirm_password:
        errors['confirm_password'] = 'Password confirmation is required'
    elif password:  # Only check match if password exists
        is_valid, msg = validate_passwords_match(password, confirm_password)
        if not is_valid:
            errors['confirm_password'] = msg

    is_valid = len(errors) == 0

    return is_valid, errors
