"""
Configuration management for the Flask registration application.

This module provides configuration settings for different environments
(development, testing, production).
"""

import os
from datetime import timedelta


class Config:
    """Base configuration class with common settings."""

    # Flask settings
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    TESTING = False

    # Database settings
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///users.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # Security settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max request size
    JSON_SORT_KEYS = False


class DevelopmentConfig(Config):
    """Development environment configuration."""

    DEBUG = True
    TESTING = False
    SESSION_COOKIE_SECURE = False  # Allow HTTP in development


class TestingConfig(Config):
    """Testing environment configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    """Production environment configuration."""

    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True


# Configuration dictionary for easy switching
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
