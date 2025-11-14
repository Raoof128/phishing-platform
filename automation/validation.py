#!/usr/bin/env python3
"""
Input validation utilities for API endpoints

Provides validation functions and decorators for securing API endpoints
against common injection attacks and malformed input.
"""

import re
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Union
from flask import request, jsonify


# Validation patterns
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
ALPHANUMERIC_PATTERN = re.compile(r'^[a-zA-Z0-9_-]+$')
INTEGER_PATTERN = re.compile(r'^\d+$')
SAFE_STRING_PATTERN = re.compile(r'^[a-zA-Z0-9\s\-_.,!?@#()]+$')


class ValidationError(Exception):
    """Custom exception for validation errors"""
    def __init__(self, message: str, field: Optional[str] = None):
        self.message = message
        self.field = field
        super().__init__(self.message)


def validate_email(email: str) -> bool:
    """
    Validate email address format

    Args:
        email: Email address to validate

    Returns:
        True if valid, False otherwise
    """
    if not email or not isinstance(email, str):
        return False
    return bool(EMAIL_PATTERN.match(email))


def validate_integer(value: Any, min_val: Optional[int] = None, max_val: Optional[int] = None) -> bool:
    """
    Validate integer value within optional range

    Args:
        value: Value to validate
        min_val: Minimum allowed value
        max_val: Maximum allowed value

    Returns:
        True if valid, False otherwise
    """
    try:
        int_val = int(value)
        if min_val is not None and int_val < min_val:
            return False
        if max_val is not None and int_val > max_val:
            return False
        return True
    except (ValueError, TypeError):
        return False


def validate_string(
    value: str,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    pattern: Optional[re.Pattern] = None,
    allow_empty: bool = False
) -> bool:
    """
    Validate string value with optional constraints

    Args:
        value: String to validate
        min_length: Minimum allowed length
        max_length: Maximum allowed length
        pattern: Regex pattern to match
        allow_empty: Whether empty strings are allowed

    Returns:
        True if valid, False otherwise
    """
    if not isinstance(value, str):
        return False

    if not allow_empty and not value.strip():
        return False

    if min_length is not None and len(value) < min_length:
        return False

    if max_length is not None and len(value) > max_length:
        return False

    if pattern is not None and not pattern.match(value):
        return False

    return True


def sanitize_string(value: str, max_length: int = 255) -> str:
    """
    Sanitize string by removing dangerous characters

    Args:
        value: String to sanitize
        max_length: Maximum allowed length

    Returns:
        Sanitized string
    """
    if not isinstance(value, str):
        return ""

    # Remove control characters and null bytes
    sanitized = ''.join(char for char in value if ord(char) >= 32 or char in '\n\r\t')

    # Trim to max length
    sanitized = sanitized[:max_length]

    # Strip leading/trailing whitespace
    return sanitized.strip()


def validate_request_args(schema: Dict[str, Dict[str, Any]]) -> Callable:
    """
    Decorator to validate request query parameters against a schema

    Schema format:
    {
        'param_name': {
            'required': bool,
            'type': 'string' | 'integer' | 'email',
            'min_length': int (for strings),
            'max_length': int (for strings),
            'min_val': int (for integers),
            'max_val': int (for integers),
            'pattern': re.Pattern (for strings)
        }
    }

    Args:
        schema: Validation schema dictionary

    Returns:
        Decorated function
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs):
            errors = []

            for param_name, rules in schema.items():
                value = request.args.get(param_name)

                # Check required fields
                if rules.get('required', False) and not value:
                    errors.append(f"Missing required parameter: {param_name}")
                    continue

                # Skip validation for optional missing parameters
                if not value:
                    continue

                param_type = rules.get('type', 'string')

                # Validate by type
                if param_type == 'integer':
                    if not validate_integer(
                        value,
                        min_val=rules.get('min_val'),
                        max_val=rules.get('max_val')
                    ):
                        errors.append(f"Invalid integer value for parameter: {param_name}")

                elif param_type == 'email':
                    if not validate_email(value):
                        errors.append(f"Invalid email format for parameter: {param_name}")

                elif param_type == 'string':
                    if not validate_string(
                        value,
                        min_length=rules.get('min_length'),
                        max_length=rules.get('max_length'),
                        pattern=rules.get('pattern')
                    ):
                        errors.append(f"Invalid string value for parameter: {param_name}")

            if errors:
                return jsonify({'error': 'Validation failed', 'details': errors}), 400

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def validate_json_body(schema: Dict[str, Dict[str, Any]]) -> Callable:
    """
    Decorator to validate JSON request body against a schema

    Args:
        schema: Validation schema dictionary (same format as validate_request_args)

    Returns:
        Decorated function
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({'error': 'Request must be JSON'}), 400

            data = request.get_json()
            if not data:
                return jsonify({'error': 'Empty request body'}), 400

            errors = []

            for field_name, rules in schema.items():
                value = data.get(field_name)

                # Check required fields
                if rules.get('required', False) and value is None:
                    errors.append(f"Missing required field: {field_name}")
                    continue

                # Skip validation for optional missing fields
                if value is None:
                    continue

                field_type = rules.get('type', 'string')

                # Validate by type
                if field_type == 'integer':
                    if not validate_integer(
                        value,
                        min_val=rules.get('min_val'),
                        max_val=rules.get('max_val')
                    ):
                        errors.append(f"Invalid integer value for field: {field_name}")

                elif field_type == 'email':
                    if not validate_email(value):
                        errors.append(f"Invalid email format for field: {field_name}")

                elif field_type == 'string':
                    if not validate_string(
                        value,
                        min_length=rules.get('min_length'),
                        max_length=rules.get('max_length'),
                        pattern=rules.get('pattern')
                    ):
                        errors.append(f"Invalid string value for field: {field_name}")

                elif field_type == 'list':
                    if not isinstance(value, list):
                        errors.append(f"Field must be a list: {field_name}")
                    elif rules.get('max_items') and len(value) > rules['max_items']:
                        errors.append(f"Too many items in field: {field_name}")

                elif field_type == 'dict':
                    if not isinstance(value, dict):
                        errors.append(f"Field must be an object: {field_name}")

            if errors:
                return jsonify({'error': 'Validation failed', 'details': errors}), 400

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def validate_path_param(param_name: str, param_type: str = 'integer', **kwargs) -> Callable:
    """
    Decorator to validate path parameters

    Args:
        param_name: Name of the parameter in the function signature
        param_type: Type of validation ('integer', 'string', 'email')
        **kwargs: Additional validation rules

    Returns:
        Decorated function
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **func_kwargs):
            value = func_kwargs.get(param_name)

            if value is None:
                return jsonify({'error': f'Missing path parameter: {param_name}'}), 400

            # Validate by type
            if param_type == 'integer':
                if not validate_integer(
                    value,
                    min_val=kwargs.get('min_val'),
                    max_val=kwargs.get('max_val')
                ):
                    return jsonify({'error': f'Invalid {param_name}: must be a valid integer'}), 400

            elif param_type == 'email':
                if not validate_email(value):
                    return jsonify({'error': f'Invalid {param_name}: must be a valid email'}), 400

            elif param_type == 'string':
                if not validate_string(
                    str(value),
                    min_length=kwargs.get('min_length'),
                    max_length=kwargs.get('max_length'),
                    pattern=kwargs.get('pattern')
                ):
                    return jsonify({'error': f'Invalid {param_name}: invalid format'}), 400

            return f(*args, **func_kwargs)
        return decorated_function
    return decorator


# Common validation schemas for reuse
CAMPAIGN_ID_VALIDATION = {
    'campaign_id': {
        'required': True,
        'type': 'integer',
        'min_val': 1
    }
}

EMAIL_VALIDATION = {
    'email': {
        'required': True,
        'type': 'email'
    }
}

PAGINATION_VALIDATION = {
    'page': {
        'required': False,
        'type': 'integer',
        'min_val': 1
    },
    'per_page': {
        'required': False,
        'type': 'integer',
        'min_val': 1,
        'max_val': 100
    }
}
