"""
Flask registration application.

This module initializes the Flask application, sets up the database,
and implements the registration endpoint with full validation and
security measures.
"""

import logging
import os
from typing import Any, Dict, Tuple

from flask import Flask, request, jsonify, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config import config
from models import db, User
from validators import validate_registration_form


# Initialize Flask app
def create_app(config_name: str | None = None) -> Flask:
    """
    Create and configure the Flask application.

    Args:
        config_name: Configuration environment name. Defaults to environment
                     variable or 'development'.

    Returns:
        Configured Flask application instance.
    """
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config.get(config_name, config['default']))

    # Initialize extensions
    db.init_app(app)

    # Initialize rate limiter
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://",
    )

    # Setup logging
    setup_logging(app)

    # Register routes
    register_routes(app, limiter)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app


def setup_logging(app: Flask) -> None:
    """
    Configure logging for the application.

    Args:
        app: Flask application instance.
    """
    if not app.debug:
        # Console handler for production
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)
        app.logger.setLevel(logging.INFO)


def register_routes(app: Flask, limiter: Limiter) -> None:
    """
    Register application routes.

    Args:
        app: Flask application instance.
        limiter: Flask-Limiter instance for rate limiting.
    """

    @app.route('/health', methods=['GET'])
    def health_check() -> Tuple[Dict[str, str], int]:
        """Health check endpoint for monitoring."""
        return {'status': 'ok'}, 200

    @app.route('/', methods=['GET'])
    @app.route('/register', methods=['GET'])
    def register_form() -> str:
        """Render the registration form template."""
        return render_template('register.html')

    @app.route('/register', methods=['POST'])
    @limiter.limit("20 per minute")
    def register() -> Tuple[Dict[str, Any], int]:
        """
        User registration endpoint.

        Accepts POST requests with JSON or form data containing:
        - username: 4-20 character username
        - email: Valid email address
        - password: 8+ character password with at least one number
        - confirm_password: Confirmation of password

        Returns:
            JSON response with appropriate HTTP status code:
            - 201: User created successfully
            - 400: Validation error
            - 409: Username or email already exists
            - 500: Server error

        Rate Limit: 20 requests per minute per IP
        """
        try:
            # Get request data (handles both JSON and form data)
            if request.is_json:
                data = request.get_json() or {}
            else:
                data = request.form.to_dict()

            # Validate all form fields
            is_valid, errors = validate_registration_form(data)

            if not is_valid:
                app.logger.warning(
                    f"Registration validation failed: {errors}"
                )
                return {
                    'error': 'Registration failed',
                    'details': errors,
                }, 400

            username = data.get('username', '').strip()
            email = data.get('email', '').strip()
            password = data.get('password', '')

            # Check if username already exists
            if User.query.filter_by(username=username).first():
                app.logger.warning(
                    f"Registration attempt with existing username: {username}"
                )
                return {
                    'error': 'Registration failed. Username or email already exists.',
                }, 409

            # Check if email already exists
            if User.query.filter_by(email=email).first():
                app.logger.warning(
                    f"Registration attempt with existing email: {email}"
                )
                return {
                    'error': 'Registration failed. Username or email already exists.',
                }, 409

            # Create new user
            user = User(username=username, email=email)
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            app.logger.info(f"New user registered: {username} ({email})")

            return {
                'message': 'User registered successfully',
                'user': user.to_dict(),
            }, 201

        except ValueError as e:
            # Handle validation errors from model
            app.logger.error(f"Validation error: {str(e)}")
            return {
                'error': 'Registration failed',
                'details': {'general': str(e)},
            }, 400

        except Exception as e:
            # Handle unexpected errors
            db.session.rollback()
            app.logger.error(f"Unexpected error during registration: {str(e)}")
            return {
                'error': 'An unexpected error occurred. Please try again later.',
            }, 500

    @app.errorhandler(429)
    def ratelimit_handler(e: Any) -> Tuple[Dict[str, str], int]:
        """Handle rate limit exceeded errors."""
        app.logger.warning(f"Rate limit exceeded: {e}")
        return {
            'error': 'Too many requests. Please try again later.',
        }, 429

    @app.errorhandler(404)
    def not_found(e: Any) -> Tuple[Dict[str, str], int]:
        """Handle 404 Not Found errors."""
        return {
            'error': 'Endpoint not found',
        }, 404

    @app.errorhandler(500)
    def internal_error(e: Any) -> Tuple[Dict[str, str], int]:
        """Handle 500 Internal Server errors."""
        app.logger.error(f"Internal server error: {str(e)}")
        db.session.rollback()
        return {
            'error': 'An unexpected error occurred. Please try again later.',
        }, 500


# Application factory
app = create_app()


if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=app.config['DEBUG'],
    )
