#!/usr/bin/env python3
"""
Unit tests for utility functions
"""

import pytest
import tempfile
from pathlib import Path
from automation.utils import (
    load_config,
    validate_email,
    sanitize_string,
    calculate_percentage,
    safe_dict_get,
    format_timestamp,
    ValidationError,
    ConfigurationError
)


class TestLoadConfig:
    """Tests for load_config function"""

    def test_load_valid_config(self, tmp_path):
        """Test loading a valid YAML configuration file"""
        config_file = tmp_path / "config.yaml"
        config_file.write_text("key: value\nnested:\n  item: 123")

        config = load_config(str(config_file))

        assert config['key'] == 'value'
        assert config['nested']['item'] == 123

    def test_load_nonexistent_config(self):
        """Test loading a non-existent configuration file"""
        with pytest.raises(FileNotFoundError):
            load_config("nonexistent.yaml")

    def test_load_invalid_yaml(self, tmp_path):
        """Test loading an invalid YAML file"""
        config_file = tmp_path / "invalid.yaml"
        config_file.write_text("invalid: yaml: syntax:")

        with pytest.raises(ValueError):
            load_config(str(config_file))


class TestValidateEmail:
    """Tests for validate_email function"""

    def test_valid_emails(self):
        """Test validation of valid email addresses"""
        valid_emails = [
            "test@example.com",
            "user.name@company.co.uk",
            "admin+tag@domain.org",
            "123@test.com"
        ]

        for email in valid_emails:
            assert validate_email(email), f"Email should be valid: {email}"

    def test_invalid_emails(self):
        """Test validation of invalid email addresses"""
        invalid_emails = [
            "invalid",
            "@example.com",
            "user@",
            "user @example.com",
            "",
            None,
            123
        ]

        for email in invalid_emails:
            assert not validate_email(email), f"Email should be invalid: {email}"


class TestSanitizeString:
    """Tests for sanitize_string function"""

    def test_strip_whitespace(self):
        """Test stripping of whitespace"""
        assert sanitize_string("  test  ") == "test"
        assert sanitize_string("\n\ttext\t\n") == "text"

    def test_max_length(self):
        """Test maximum length enforcement"""
        long_string = "a" * 100
        assert len(sanitize_string(long_string, max_length=50)) == 50

    def test_non_string_input(self):
        """Test handling of non-string input"""
        assert sanitize_string(None) == ""
        assert sanitize_string(123) == ""
        assert sanitize_string([]) == ""


class TestCalculatePercentage:
    """Tests for calculate_percentage function"""

    def test_normal_calculation(self):
        """Test normal percentage calculation"""
        assert calculate_percentage(25, 100) == 25.0
        assert calculate_percentage(1, 3, decimals=2) == 33.33

    def test_zero_denominator(self):
        """Test division by zero handling"""
        assert calculate_percentage(10, 0) == 0.0

    def test_rounding(self):
        """Test decimal rounding"""
        assert calculate_percentage(1, 3, decimals=0) == 33.0
        assert calculate_percentage(2, 3, decimals=1) == 66.7


class TestSafeDictGet:
    """Tests for safe_dict_get function"""

    def test_existing_key(self):
        """Test retrieving existing key"""
        d = {'a': 1, 'b': 2}
        assert safe_dict_get(d, 'a') == 1

    def test_missing_key(self):
        """Test retrieving missing key with default"""
        d = {'a': 1}
        assert safe_dict_get(d, 'b', default=0) == 0

    def test_non_dict_input(self):
        """Test handling of non-dictionary input"""
        assert safe_dict_get(None, 'key', default='default') == 'default'
        assert safe_dict_get("string", 'key', default='default') == 'default'


class TestFormatTimestamp:
    """Tests for format_timestamp function"""

    def test_valid_timestamp(self):
        """Test formatting valid timestamp"""
        timestamp = "2025-01-15T10:30:00"
        result = format_timestamp(timestamp)
        assert result == "2025-01-15 10:30:00"

    def test_none_timestamp(self):
        """Test handling None timestamp"""
        assert format_timestamp(None) == 'N/A'

    def test_invalid_timestamp(self):
        """Test handling invalid timestamp"""
        result = format_timestamp("invalid")
        assert result == "invalid"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
