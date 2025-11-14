#!/usr/bin/env python3
"""
Constants - Centralized configuration constants
Provides type-safe constants for the entire platform
"""

from enum import Enum
from typing import Final


# Risk Scoring Constants
RISK_SCORE_MIN: Final[int] = 0
RISK_SCORE_MAX: Final[int] = 100

# Risk score points for different actions
POINTS_EMAIL_OPENED: Final[int] = 10
POINTS_LINK_CLICKED: Final[int] = 25
POINTS_DATA_SUBMITTED: Final[int] = 40
POINTS_EMAIL_REPORTED: Final[int] = -15  # Negative = reduces risk

# Risk level thresholds
RISK_THRESHOLD_HIGH: Final[int] = 70
RISK_THRESHOLD_MEDIUM: Final[int] = 40
RISK_THRESHOLD_LOW: Final[int] = 1


class CampaignStatus(str, Enum):
    """Campaign status values"""
    SCHEDULED = "Scheduled"
    IN_PROGRESS = "In progress"
    COMPLETED = "Completed"
    PAUSED = "Paused"
    ERROR = "Error"


class UserStatus(str, Enum):
    """User interaction status values"""
    SCHEDULED = "Scheduled"
    SENT = "Email Sent"
    OPENED = "Email Opened"
    CLICKED = "Clicked Link"
    SUBMITTED = "Submitted Data"
    REPORTED = "Email Reported"
    ERROR = "Error"


class RiskLevel(str, Enum):
    """User risk level classifications"""
    UNKNOWN = "Unknown"
    MINIMAL = "Minimal"
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


# API Configuration
DEFAULT_API_TIMEOUT: Final[int] = 30
DEFAULT_REQUEST_RETRIES: Final[int] = 3
RETRY_BACKOFF_FACTOR: Final[float] = 2.0

# Database Configuration
DB_CONNECTION_POOL_SIZE: Final[int] = 5
DB_MAX_OVERFLOW: Final[int] = 10
DB_POOL_TIMEOUT: Final[int] = 30
DB_POOL_RECYCLE: Final[int] = 3600

# Email Validation
EMAIL_REGEX_PATTERN: Final[str] = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# Report Configuration
REPORT_MAX_RESULTS_DISPLAY: Final[int] = 50
REPORT_DATE_FORMAT: Final[str] = '%Y-%m-%d %H:%M:%S'
REPORT_FILENAME_DATE_FORMAT: Final[str] = '%Y%m%d_%H%M%S'

# Training Configuration
TRAINING_DEADLINE_DAYS: Final[int] = 14

# Rate Limiting
RATE_LIMIT_REQUESTS_PER_MINUTE: Final[int] = 60
RATE_LIMIT_REQUESTS_PER_HOUR: Final[int] = 1000

# Logging
LOG_FORMAT: Final[str] = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DATE_FORMAT: Final[str] = '%Y-%m-%d %H:%M:%S'
