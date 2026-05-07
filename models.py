"""
SQLAlchemy models for the registration system.

This module defines the User model with proper constraints, validation,
and password hashing methods.
"""

from datetime import datetime
from typing import Optional

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    """
    User database model for registration system.

    Attributes:
        id: Unique user identifier (primary key).
        username: Unique username (4-20 characters).
        email: Unique email address.
        password_hash: Hashed password using werkzeug.security.
        created_at: Timestamp of user creation.
    """

    __tablename__ = 'users'

    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(
        db.String(20),
        unique=True,
        nullable=False,
        index=True
    )
    email: str = db.Column(
        db.String(120),
        unique=True,
        nullable=False,
        index=True
    )
    password_hash: str = db.Column(db.String(255), nullable=False)
    created_at: datetime = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    def set_password(self, password: str) -> None:
        """
        Hash and store the password.

        Args:
            password: Plain text password to hash and store.

        Raises:
            ValueError: If password is empty or not a string.
        """
        if not password or not isinstance(password, str):
            raise ValueError("Password must be a non-empty string")

        self.password_hash = generate_password_hash(
            password,
            method='pbkdf2:sha256',
            salt_length=16
        )

    def check_password(self, password: str) -> bool:
        """
        Verify a plain text password against the stored hash.

        Args:
            password: Plain text password to verify.

        Returns:
            True if password matches, False otherwise.
        """
        if not password or not isinstance(password, str):
            return False

        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        """Return string representation of User instance."""
        return f'<User {self.username}>'

    def to_dict(self) -> dict:
        """
        Convert User instance to dictionary (safe for JSON serialization).

        Returns:
            Dictionary with user id, username, email, and created_at.
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
        }
