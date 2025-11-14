#!/usr/bin/env python3
"""
Utilities - Shared utility functions
Provides common functionality used across modules
"""

import re
import logging
import yaml
from typing import Dict, Any, Optional
from pathlib import Path
from functools import wraps
import time
from automation.constants import EMAIL_REGEX_PATTERN, RETRY_BACKOFF_FACTOR

logger = logging.getLogger(__name__)


def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load configuration from YAML file with validation

    Args:
        config_path: Path to configuration file

    Returns:
        Dictionary with configuration

    Raises:
        FileNotFoundError: If config file doesn't exist
        ValueError: If config is invalid
    """
    config_file = Path(config_path)

    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)

        if not isinstance(config, dict):
            raise ValueError("Configuration must be a dictionary")

        return config

    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing configuration file: {e}")


def validate_email(email: str) -> bool:
    """
    Validate email address format

    Args:
        email: Email address to validate

    Returns:
        True if valid email format, False otherwise
    """
    if not email or not isinstance(email, str):
        return False

    return re.match(EMAIL_REGEX_PATTERN, email.strip()) is not None


def sanitize_string(text: str, max_length: Optional[int] = None) -> str:
    """
    Sanitize string input by stripping whitespace and limiting length

    Args:
        text: Input text
        max_length: Maximum allowed length

    Returns:
        Sanitized string
    """
    if not isinstance(text, str):
        return ""

    sanitized = text.strip()

    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length]

    return sanitized


def retry_on_failure(max_retries: int = 3, backoff_factor: float = RETRY_BACKOFF_FACTOR):
    """
    Decorator to retry a function on failure with exponential backoff

    Args:
        max_retries: Maximum number of retry attempts
        backoff_factor: Multiplier for delay between retries

    Returns:
        Decorated function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e

                    if attempt < max_retries:
                        delay = backoff_factor ** attempt
                        logger.warning(
                            f"{func.__name__} failed (attempt {attempt + 1}/{max_retries + 1}). "
                            f"Retrying in {delay}s... Error: {e}"
                        )
                        time.sleep(delay)
                    else:
                        logger.error(f"{func.__name__} failed after {max_retries + 1} attempts")

            raise last_exception

        return wrapper
    return decorator


def calculate_percentage(numerator: int, denominator: int, decimals: int = 2) -> float:
    """
    Safely calculate percentage with division by zero handling

    Args:
        numerator: Numerator value
        denominator: Denominator value
        decimals: Number of decimal places

    Returns:
        Percentage value (0-100)
    """
    if denominator <= 0:
        return 0.0

    percentage = (numerator / denominator) * 100
    return round(percentage, decimals)


def safe_dict_get(dictionary: Dict, key: str, default: Any = None) -> Any:
    """
    Safely get value from dictionary with type checking

    Args:
        dictionary: Dictionary to query
        key: Key to retrieve
        default: Default value if key not found

    Returns:
        Value from dictionary or default
    """
    if not isinstance(dictionary, dict):
        return default

    return dictionary.get(key, default)


def format_timestamp(timestamp: Optional[str], format_str: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    Format timestamp string consistently

    Args:
        timestamp: Timestamp string or None
        format_str: Desired format string

    Returns:
        Formatted timestamp or 'N/A'
    """
    if not timestamp:
        return 'N/A'

    try:
        from datetime import datetime
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime(format_str)
    except (ValueError, AttributeError):
        return timestamp if isinstance(timestamp, str) else 'N/A'


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


class ConfigurationError(Exception):
    """Custom exception for configuration errors"""
    pass


class APIError(Exception):
    """Custom exception for API errors"""
    pass
