#!/usr/bin/env python3
"""
Shared pytest fixtures and configuration for all tests
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock, MagicMock


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_config_file(temp_dir):
    """Create a mock configuration file"""
    config_file = temp_dir / "test_config.yaml"
    config_content = """
gophish:
  api_key: test-api-key-12345
  server_url: https://localhost:3333
  verify_ssl: false
  timeout: 30

campaign_defaults:
  timezone: UTC
  default_launch_time: "09:00"
  duration_days: 7

analytics:
  gophish_db_path: ./test_gophish.db
  reports_dir: ./test_reports

training:
  risk_thresholds:
    high: 70
    medium: 40
    low: 0
  training_modules:
    high_risk:
      - Advanced Phishing Recognition
      - Social Engineering Defense
      - Incident Response Training
    medium_risk:
      - Email Security Basics
      - Safe Browsing Practices
    low_risk:
      - Security Awareness Overview

user_import:
  csv_columns:
    email: email
    first_name: first_name
    last_name: last_name
    position: position
    department: department
  validate_emails: true
  skip_invalid: true
"""
    config_file.write_text(config_content)
    return str(config_file)


@pytest.fixture
def mock_database(temp_dir):
    """Create a mock SQLite database for testing"""
    import sqlite3

    db_path = temp_dir / "test_gophish.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    # Create campaigns table
    cursor.execute("""
        CREATE TABLE campaigns (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            created_date TEXT,
            launch_date TEXT,
            completed_date TEXT,
            status TEXT
        )
    """)

    # Create results table
    cursor.execute("""
        CREATE TABLE results (
            id INTEGER PRIMARY KEY,
            campaign_id INTEGER,
            email TEXT,
            first_name TEXT,
            last_name TEXT,
            position TEXT,
            status TEXT,
            ip TEXT,
            latitude REAL,
            longitude REAL,
            FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
        )
    """)

    # Create events table
    cursor.execute("""
        CREATE TABLE events (
            id INTEGER PRIMARY KEY,
            campaign_id INTEGER,
            email TEXT,
            time TEXT,
            message TEXT,
            details TEXT,
            FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
        )
    """)

    # Insert sample data
    cursor.execute("""
        INSERT INTO campaigns (id, name, created_date, launch_date, status)
        VALUES (1, 'Test Campaign', '2025-01-01', '2025-01-02', 'Completed')
    """)

    cursor.execute("""
        INSERT INTO results (campaign_id, email, first_name, last_name, position, status)
        VALUES
            (1, 'user1@test.com', 'John', 'Doe', 'Engineer', 'Email Opened'),
            (1, 'user2@test.com', 'Jane', 'Smith', 'Manager', 'Clicked Link'),
            (1, 'user3@test.com', 'Bob', 'Johnson', 'Analyst', 'Submitted Data'),
            (1, 'user4@test.com', 'Alice', 'Williams', 'Director', 'Email Reported')
    """)

    conn.commit()
    conn.close()

    return str(db_path)


@pytest.fixture
def mock_campaign_data():
    """Sample campaign data for testing"""
    return {
        'id': 1,
        'name': 'Test Campaign',
        'status': 'Completed',
        'created_date': '2025-01-01T00:00:00',
        'launch_date': '2025-01-02T09:00:00',
        'completed_date': '2025-01-09T17:00:00',
        'results': [
            {'email': 'user1@test.com', 'status': 'Email Sent', 'first_name': 'John', 'last_name': 'Doe'},
            {'email': 'user2@test.com', 'status': 'Email Opened', 'first_name': 'Jane', 'last_name': 'Smith'},
            {'email': 'user3@test.com', 'status': 'Clicked Link', 'first_name': 'Bob', 'last_name': 'Johnson'},
            {'email': 'user4@test.com', 'status': 'Submitted Data', 'first_name': 'Alice', 'last_name': 'Williams'},
        ],
        'timeline': []
    }


@pytest.fixture
def mock_user_data():
    """Sample user data for testing"""
    return [
        {
            'email': 'john.doe@company.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'position': 'Software Engineer'
        },
        {
            'email': 'jane.smith@company.com',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'position': 'Marketing Manager'
        },
        {
            'email': 'bob.jones@company.com',
            'first_name': 'Bob',
            'last_name': 'Jones',
            'position': 'Sales Representative'
        }
    ]


@pytest.fixture
def mock_csv_file(temp_dir, mock_user_data):
    """Create a mock CSV file for user import testing"""
    import csv

    csv_file = temp_dir / "test_users.csv"

    with open(csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['email', 'first_name', 'last_name', 'position'])
        writer.writeheader()
        writer.writerows(mock_user_data)

    return str(csv_file)


@pytest.fixture
def mock_api_response():
    """Create a mock API response"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'id': 1, 'name': 'Test Campaign'}
    return mock_response


@pytest.fixture
def mock_smtp_server():
    """Create a mock SMTP server"""
    mock_server = MagicMock()
    mock_server.__enter__ = Mock(return_value=mock_server)
    mock_server.__exit__ = Mock(return_value=False)
    mock_server.starttls = Mock()
    mock_server.login = Mock()
    mock_server.send_message = Mock()
    return mock_server
