#!/usr/bin/env python3
"""
Logging configuration module for the Phishing Awareness Training Platform

Provides centralized logging setup with support for multiple handlers,
formatters, and environment-specific configurations.
"""

import logging
import logging.config
import os
import sys
from pathlib import Path
from typing import Optional
import yaml


def setup_logging(
    config_path: Optional[str] = None,
    log_level: Optional[str] = None,
    environment: str = 'development'
) -> None:
    """
    Configure logging for the application

    Args:
        config_path: Path to logging configuration YAML file
        log_level: Override log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        environment: Environment name (development, production, testing)
    """
    # Default config path
    if config_path is None:
        config_path = os.path.join(
            os.path.dirname(__file__),
            '..',
            'config',
            'logging.yaml'
        )

    # Ensure log directory exists
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)

    # Load configuration
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        # Apply environment-specific overrides
        if environment in config:
            env_config = config[environment]
            # Merge environment config with base config
            if 'root' in env_config:
                config['root'].update(env_config['root'])
            if 'loggers' in env_config:
                for logger_name, logger_config in env_config['loggers'].items():
                    if logger_name in config['loggers']:
                        config['loggers'][logger_name].update(logger_config)
            if 'formatters' in env_config:
                config['formatters'].update(env_config['formatters'])

        # Apply logging configuration
        logging.config.dictConfig(config)

        # Override log level if specified
        if log_level:
            logging.root.setLevel(log_level.upper())

        logger = logging.getLogger(__name__)
        logger.info(f"Logging configured successfully (environment: {environment})")

    except FileNotFoundError:
        # Fallback to basic configuration if config file not found
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler('logs/app.log')
            ]
        )
        logger = logging.getLogger(__name__)
        logger.warning(f"Logging config file not found: {config_path}. Using basic configuration.")

    except Exception as e:
        # Fallback to basic configuration on error
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        logger = logging.getLogger(__name__)
        logger.error(f"Error loading logging configuration: {e}. Using basic configuration.")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name

    Args:
        name: Logger name (typically __name__ of the module)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


def log_security_event(
    event_type: str,
    description: str,
    severity: str = 'WARNING',
    **context
) -> None:
    """
    Log a security event with structured information

    Args:
        event_type: Type of security event (e.g., 'authentication_failure', 'rate_limit_exceeded')
        description: Human-readable description of the event
        severity: Log severity (WARNING, ERROR, CRITICAL)
        **context: Additional context information
    """
    logger = logging.getLogger('security')

    log_message = f"[{event_type}] {description}"
    if context:
        log_message += f" | Context: {context}"

    # Log at appropriate level
    level = getattr(logging, severity.upper(), logging.WARNING)
    logger.log(level, log_message)


def log_api_request(
    method: str,
    endpoint: str,
    status_code: int,
    response_time: float,
    user_agent: Optional[str] = None,
    ip_address: Optional[str] = None,
    **extra
) -> None:
    """
    Log an API request with structured information

    Args:
        method: HTTP method (GET, POST, etc.)
        endpoint: API endpoint path
        status_code: HTTP status code
        response_time: Response time in seconds
        user_agent: User agent string
        ip_address: Client IP address
        **extra: Additional request context
    """
    logger = logging.getLogger('dashboard')

    log_data = {
        'method': method,
        'endpoint': endpoint,
        'status_code': status_code,
        'response_time_ms': round(response_time * 1000, 2),
        'user_agent': user_agent,
        'ip_address': ip_address,
        **extra
    }

    logger.info(f"API Request: {method} {endpoint} - {status_code} ({log_data['response_time_ms']}ms)", extra=log_data)


def log_audit_event(
    action: str,
    resource: str,
    user: Optional[str] = None,
    success: bool = True,
    **details
) -> None:
    """
    Log an audit event for compliance and tracking

    Args:
        action: Action performed (create, update, delete, read)
        resource: Resource affected (campaign, user, group)
        user: User who performed the action
        success: Whether the action succeeded
        **details: Additional audit details
    """
    logger = logging.getLogger('audit')

    log_message = f"[{action.upper()}] {resource}"
    if user:
        log_message += f" by {user}"
    log_message += f" - {'SUCCESS' if success else 'FAILED'}"

    if details:
        log_message += f" | {details}"

    logger.info(log_message)


def log_campaign_event(
    campaign_id: int,
    event_type: str,
    description: str,
    **context
) -> None:
    """
    Log a campaign-related event

    Args:
        campaign_id: Campaign ID
        event_type: Type of event (created, launched, completed, etc.)
        description: Event description
        **context: Additional context
    """
    logger = logging.getLogger('automation.campaign_manager')

    log_message = f"Campaign {campaign_id} [{event_type}]: {description}"
    if context:
        log_message += f" | {context}"

    logger.info(log_message)


def log_analytics_event(
    metric_type: str,
    value: float,
    campaign_id: Optional[int] = None,
    user_email: Optional[str] = None,
    **context
) -> None:
    """
    Log an analytics calculation event

    Args:
        metric_type: Type of metric (risk_score, click_rate, etc.)
        value: Metric value
        campaign_id: Related campaign ID
        user_email: Related user email
        **context: Additional context
    """
    logger = logging.getLogger('automation.analytics')

    log_message = f"Analytics [{metric_type}]: {value}"
    if campaign_id:
        log_message += f" (Campaign: {campaign_id})"
    if user_email:
        log_message += f" (User: {user_email})"
    if context:
        log_message += f" | {context}"

    logger.info(log_message)


def log_validation_failure(
    field: str,
    value: str,
    reason: str,
    endpoint: Optional[str] = None,
    ip_address: Optional[str] = None
) -> None:
    """
    Log input validation failure (security event)

    Args:
        field: Field name that failed validation
        value: Invalid value (sanitized)
        reason: Reason for failure
        endpoint: API endpoint where validation failed
        ip_address: Client IP address
    """
    logger = logging.getLogger('automation.validation')

    # Sanitize value for logging (truncate and remove sensitive data)
    safe_value = str(value)[:100] if value else 'None'

    log_message = f"Validation failed for field '{field}': {reason}"
    if endpoint:
        log_message += f" | Endpoint: {endpoint}"
    if ip_address:
        log_message += f" | IP: {ip_address}"
    log_message += f" | Value (truncated): {safe_value}"

    logger.warning(log_message)


class RequestLogger:
    """
    Context manager for logging request duration and outcome
    """

    def __init__(self, operation: str, logger: Optional[logging.Logger] = None):
        """
        Initialize request logger

        Args:
            operation: Description of the operation being logged
            logger: Logger instance (uses root logger if None)
        """
        self.operation = operation
        self.logger = logger or logging.getLogger()
        self.start_time = None

    def __enter__(self):
        """Start timing the operation"""
        import time
        self.start_time = time.time()
        self.logger.debug(f"Starting: {self.operation}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Log operation completion or failure"""
        import time
        duration = time.time() - self.start_time

        if exc_type is None:
            self.logger.info(f"Completed: {self.operation} ({duration:.3f}s)")
        else:
            self.logger.error(
                f"Failed: {self.operation} ({duration:.3f}s) - {exc_type.__name__}: {exc_val}"
            )
        return False  # Don't suppress exceptions


# Example usage
if __name__ == '__main__':
    # Setup logging
    setup_logging(environment='development')

    # Get logger
    logger = get_logger(__name__)

    # Test logging
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")

    # Test security event logging
    log_security_event(
        'authentication_failure',
        'Failed login attempt',
        severity='WARNING',
        username='admin',
        ip_address='192.168.1.100'
    )

    # Test API request logging
    log_api_request(
        'GET',
        '/api/campaigns',
        200,
        0.045,
        user_agent='Mozilla/5.0',
        ip_address='192.168.1.100'
    )

    # Test audit event logging
    log_audit_event(
        'create',
        'campaign',
        user='admin@example.com',
        success=True,
        campaign_id=123
    )

    # Test context manager
    with RequestLogger('Database query'):
        import time
        time.sleep(0.1)  # Simulate work

    print("Logging examples completed. Check logs/ directory for output.")
