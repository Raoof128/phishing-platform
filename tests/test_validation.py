#!/usr/bin/env python3
"""
Unit tests for validation module
"""

import pytest
import re
from automation.validation import (
    validate_email,
    validate_integer,
    validate_string,
    sanitize_string,
    ValidationError,
    EMAIL_PATTERN,
    SAFE_STRING_PATTERN
)


class TestEmailValidation:
    """Tests for email validation"""

    def test_valid_email(self):
        """Test valid email addresses"""
        assert validate_email('test@example.com') is True
        assert validate_email('user.name@company.co.uk') is True
        assert validate_email('first+last@domain.org') is True

    def test_invalid_email(self):
        """Test invalid email addresses"""
        assert validate_email('') is False
        assert validate_email('invalid') is False
        assert validate_email('@example.com') is False
        assert validate_email('test@') is False
        assert validate_email('test @example.com') is False
        assert validate_email(None) is False
        assert validate_email(123) is False

    def test_email_pattern(self):
        """Test email regex pattern"""
        assert EMAIL_PATTERN.match('valid@email.com') is not None
        assert EMAIL_PATTERN.match('invalid@') is None


class TestIntegerValidation:
    """Tests for integer validation"""

    def test_valid_integer(self):
        """Test valid integers"""
        assert validate_integer(123) is True
        assert validate_integer('456') is True
        assert validate_integer(0) is True
        assert validate_integer(-5) is True

    def test_integer_with_range(self):
        """Test integer validation with min/max range"""
        assert validate_integer(50, min_val=1, max_val=100) is True
        assert validate_integer(1, min_val=1, max_val=100) is True
        assert validate_integer(100, min_val=1, max_val=100) is True

    def test_integer_out_of_range(self):
        """Test integer validation outside range"""
        assert validate_integer(0, min_val=1, max_val=100) is False
        assert validate_integer(101, min_val=1, max_val=100) is False
        assert validate_integer(-5, min_val=0) is False

    def test_invalid_integer(self):
        """Test invalid integer values"""
        assert validate_integer('abc') is False
        assert validate_integer('12.5') is False
        assert validate_integer(None) is False
        assert validate_integer([]) is False


class TestStringValidation:
    """Tests for string validation"""

    def test_valid_string(self):
        """Test valid strings"""
        assert validate_string('hello') is True
        assert validate_string('test string 123') is True

    def test_string_length_validation(self):
        """Test string length constraints"""
        assert validate_string('test', min_length=3, max_length=10) is True
        assert validate_string('test', min_length=4, max_length=4) is True
        assert validate_string('ab', min_length=3) is False
        assert validate_string('verylongstring', max_length=5) is False

    def test_string_pattern_validation(self):
        """Test string pattern matching"""
        pattern = re.compile(r'^[a-z]+$')
        assert validate_string('abc', pattern=pattern) is True
        assert validate_string('ABC', pattern=pattern) is False
        assert validate_string('abc123', pattern=pattern) is False

    def test_empty_string_handling(self):
        """Test empty string validation"""
        assert validate_string('', allow_empty=True) is True
        assert validate_string('', allow_empty=False) is False
        assert validate_string('   ', allow_empty=False) is False

    def test_invalid_string_type(self):
        """Test non-string types"""
        assert validate_string(123) is False
        assert validate_string(None) is False
        assert validate_string([]) is False


class TestStringSanitization:
    """Tests for string sanitization"""

    def test_sanitize_normal_string(self):
        """Test sanitizing normal strings"""
        assert sanitize_string('hello world') == 'hello world'
        assert sanitize_string('test@email.com') == 'test@email.com'

    def test_sanitize_dangerous_chars(self):
        """Test removal of dangerous characters"""
        # Null bytes
        result = sanitize_string('test\x00dangerous')
        assert '\x00' not in result

        # Control characters
        result = sanitize_string('test\x01\x02\x03data')
        assert '\x01' not in result

    def test_sanitize_max_length(self):
        """Test max length enforcement"""
        long_string = 'a' * 500
        result = sanitize_string(long_string, max_length=100)
        assert len(result) == 100

    def test_sanitize_whitespace(self):
        """Test whitespace handling"""
        assert sanitize_string('  test  ') == 'test'
        assert sanitize_string('\n\ndata\n\n') == 'data'
        assert sanitize_string('  ') == ''

    def test_sanitize_invalid_input(self):
        """Test sanitization of invalid input"""
        assert sanitize_string(None) == ''
        assert sanitize_string(123) == ''
        assert sanitize_string([]) == ''


class TestSafeStringPattern:
    """Tests for safe string regex pattern"""

    def test_safe_characters(self):
        """Test allowed safe characters"""
        assert SAFE_STRING_PATTERN.match('Hello World') is not None
        assert SAFE_STRING_PATTERN.match('test-value_123') is not None
        assert SAFE_STRING_PATTERN.match('Price: $50.99!') is not None

    def test_unsafe_characters(self):
        """Test rejection of unsafe characters"""
        assert SAFE_STRING_PATTERN.match('test<script>') is None
        assert SAFE_STRING_PATTERN.match('value;DROP TABLE') is None
        assert SAFE_STRING_PATTERN.match('data|rm -rf') is None


class TestValidationError:
    """Tests for ValidationError exception"""

    def test_validation_error_creation(self):
        """Test creating validation error"""
        error = ValidationError('Test error')
        assert error.message == 'Test error'
        assert error.field is None

    def test_validation_error_with_field(self):
        """Test validation error with field"""
        error = ValidationError('Invalid value', field='email')
        assert error.message == 'Invalid value'
        assert error.field == 'email'

    def test_validation_error_exception(self):
        """Test validation error is raised correctly"""
        with pytest.raises(ValidationError) as exc_info:
            raise ValidationError('Test error', field='test_field')

        assert 'Test error' in str(exc_info.value)
        assert exc_info.value.field == 'test_field'


class TestValidationIntegration:
    """Integration tests for validation functions"""

    def test_email_validation_workflow(self):
        """Test complete email validation workflow"""
        valid_emails = [
            'user@example.com',
            'test.user@company.co.uk',
            'admin+tag@domain.org'
        ]

        invalid_emails = [
            '',
            'notanemail',
            '@example.com',
            'user@',
            'user @example.com'
        ]

        for email in valid_emails:
            assert validate_email(email), f"Expected {email} to be valid"

        for email in invalid_emails:
            assert not validate_email(email), f"Expected {email} to be invalid"

    def test_integer_validation_workflow(self):
        """Test complete integer validation workflow"""
        # ID validation (must be positive)
        assert validate_integer(1, min_val=1) is True
        assert validate_integer(0, min_val=1) is False
        assert validate_integer(-1, min_val=1) is False

        # Pagination validation (1-100)
        assert validate_integer(50, min_val=1, max_val=100) is True
        assert validate_integer(0, min_val=1, max_val=100) is False
        assert validate_integer(101, min_val=1, max_val=100) is False

    def test_string_sanitization_workflow(self):
        """Test complete string sanitization workflow"""
        # User input with potential XSS
        dangerous_input = '<script>alert("xss")</script>'
        safe_output = sanitize_string(dangerous_input)
        assert '<' not in safe_output or '>' not in safe_output

        # SQL injection attempt
        sql_injection = "'; DROP TABLE users; --"
        safe_sql = sanitize_string(sql_injection)
        assert safe_sql  # Should still have content but sanitized

        # Very long input
        long_input = 'A' * 10000
        safe_long = sanitize_string(long_input, max_length=255)
        assert len(safe_long) == 255


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
