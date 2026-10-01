"""
Test script for the Flask registration application.

This script demonstrates all registration endpoints and validation scenarios.
Run this after starting the Flask app: python app.py
"""

import json
import requests
from typing import Dict, Any


BASE_URL = 'http://127.0.0.1:5000'


def print_response(test_name: str, response: requests.Response) -> None:
    """
    Pretty print test response.

    Args:
        test_name: Name of the test.
        response: Response from the server.
    """
    print(f"\n{'='*70}")
    print(f"TEST: {test_name}")
    print(f"{'='*70}")
    print(f"Status Code: {response.status_code}")
    print(f"Response:\n{json.dumps(response.json(), indent=2)}")


def test_health_check() -> None:
    """Test health check endpoint."""
    response = requests.get(f'{BASE_URL}/health')
    print_response("Health Check", response)
    assert response.status_code == 200


def test_valid_registration() -> None:
    """Test successful user registration."""
    data = {
        'username': 'john_doe',
        'email': 'john@example.com',
        'password': 'SecurePass123',
        'confirm_password': 'SecurePass123',
    }
    response = requests.post(f'{BASE_URL}/register', json=data)
    print_response("Valid Registration", response)
    assert response.status_code == 201
    assert 'user' in response.json()


def test_duplicate_username() -> None:
    """Test registration with duplicate username."""
    data = {
        'username': 'john_doe',  # Already registered in test_valid_registration
        'email': 'different@example.com',
        'password': 'AnotherPass456',
        'confirm_password': 'AnotherPass456',
    }
    response = requests.post(f'{BASE_URL}/register', json=data)
    print_response("Duplicate Username", response)
    assert response.status_code == 409


def test_duplicate_email() -> None:
    """Test registration with duplicate email."""
    data = {
        'username': 'different_user',
        'email': 'john@example.com',  # Already registered
        'password': 'AnotherPass456',
        'confirm_password': 'AnotherPass456',
    }
    response = requests.post(f'{BASE_URL}/register', json=data)
    print_response("Duplicate Email", response)
    assert response.status_code == 409


def test_password_too_short() -> None:
    """Test registration with password too short."""
    data = {
        'username': 'user123',
        'email': 'user123@example.com',
        'password': 'short1',
        'confirm_password': 'short1',
    }
    response = requests.post(f'{BASE_URL}/register', json=data)
    print_response("Password Too Short", response)
    assert response.status_code == 400
    assert 'password' in response.json()['details']


def test_password_no_numbers() -> None:
    """Test registration with password without numbers."""
    data = {
        'username': 'user123',
        'email': 'user123@example.com',
        'password': 'NoNumbers',
        'confirm_password': 'NoNumbers',
    }
    response = requests.post(f'{BASE_URL}/register', json=data)
    print_response("Password Without Numbers", response)
    assert response.status_code == 400
    assert 'password' in response.json()['details']


def test_passwords_not_matching() -> None:
    """Test registration with non-matching passwords."""
    data = {
        'username': 'user123',
        'email': 'user123@example.com',
        'password': 'SecurePass123',
        'confirm_password': 'DifferentPass456',
    }
    response = requests.post(f'{BASE_URL}/register', json=data)
    print_response("Passwords Not Matching", response)
    assert response.status_code == 400
    assert 'confirm_password' in response.json()['details']


def test_missing_password_confirmation() -> None:
    """Test registration without a password confirmation."""
    data = {
        'username': 'user456',
        'email': 'user456@example.com',
        'password': 'SecurePass123',
    }
    response = requests.post(f'{BASE_URL}/register', json=data)
    print_response("Missing Password Confirmation", response)
    assert response.status_code == 400
    assert response.json()['details']['confirm_password'] == (
        'Password confirmation is required'
    )


def test_invalid_email() -> None:
    """Test registration with invalid email format."""
    data = {
        'username': 'user123',
        'email': 'invalid.email',
        'password': 'SecurePass123',
        'confirm_password': 'SecurePass123',
    }
    response = requests.post(f'{BASE_URL}/register', json=data)
    print_response("Invalid Email Format", response)
    assert response.status_code == 400
    assert 'email' in response.json()['details']


def test_username_too_short() -> None:
    """Test registration with username too short."""
    data = {
        'username': 'ab',
        'email': 'user@example.com',
        'password': 'SecurePass123',
        'confirm_password': 'SecurePass123',
    }
    response = requests.post(f'{BASE_URL}/register', json=data)
    print_response("Username Too Short", response)
    assert response.status_code == 400
    assert 'username' in response.json()['details']


def test_username_invalid_format() -> None:
    """Test registration with invalid username format."""
    data = {
        'username': '123_invalid',
        'email': 'user@example.com',
        'password': 'SecurePass123',
        'confirm_password': 'SecurePass123',
    }
    response = requests.post(f'{BASE_URL}/register', json=data)
    print_response("Invalid Username Format", response)
    assert response.status_code == 400
    assert 'username' in response.json()['details']


def test_missing_fields() -> None:
    """Test registration with missing fields."""
    data = {
        'username': 'user123',
        # Missing email, password, confirm_password
    }
    response = requests.post(f'{BASE_URL}/register', json=data)
    print_response("Missing Required Fields", response)
    assert response.status_code == 400
    assert 'details' in response.json()


def test_empty_request() -> None:
    """Test registration with empty request."""
    response = requests.post(f'{BASE_URL}/register', json={})
    print_response("Empty Request Body", response)
    assert response.status_code == 400


def test_invalid_endpoint() -> None:
    """Test invalid endpoint."""
    response = requests.get(f'{BASE_URL}/invalid')
    print_response("Invalid Endpoint (404)", response)
    assert response.status_code == 404


def run_all_tests() -> None:
    """Run all test cases."""
    print("\n" + "="*70)
    print("FLASK REGISTRATION SYSTEM - COMPREHENSIVE TEST SUITE")
    print("="*70)

    tests = [
        ("Health Check", test_health_check),
        ("Valid Registration", test_valid_registration),
        ("Duplicate Username", test_duplicate_username),
        ("Duplicate Email", test_duplicate_email),
        ("Password Too Short", test_password_too_short),
        ("Password Without Numbers", test_password_no_numbers),
        ("Passwords Not Matching", test_passwords_not_matching),
        ("Invalid Email Format", test_invalid_email),
        ("Username Too Short", test_username_too_short),
        ("Invalid Username Format", test_username_invalid_format),
        ("Missing Required Fields", test_missing_fields),
        ("Empty Request Body", test_empty_request),
        ("Invalid Endpoint (404)", test_invalid_endpoint),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"\n❌ TEST FAILED: {test_name}")
            print(f"Error: {str(e)}")
            failed += 1

    print("\n" + "="*70)
    print(f"TEST SUMMARY: {passed} passed, {failed} failed out of {len(tests)} tests")
    print("="*70 + "\n")

    if failed == 0:
        print("✅ All tests passed!")
    else:
        print(f"❌ {failed} test(s) failed!")


if __name__ == '__main__':
    print("\n📝 Starting Flask Registration System Tests...")
    print("⚠️  Make sure the Flask app is running: python app.py\n")

    try:
        run_all_tests()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to Flask app at http://127.0.0.1:5000")
        print("Make sure the Flask application is running:")
        print("   python app.py")
    except KeyboardInterrupt:
        print("\n\n⛔ Tests interrupted by user")
