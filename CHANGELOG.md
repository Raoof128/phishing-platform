# Changelog

All notable changes to the Phishing Awareness Training Platform are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-01-15

### Added

#### New Modules
- **automation/constants.py** - Centralized constants and enums for configuration values
- **automation/utils.py** - Shared utility functions to eliminate code duplication
- **tests/test_utils.py** - Unit tests for utility functions
- **tests/test_campaign_manager.py** - Unit tests for campaign manager
- **IMPROVEMENTS.md** - Comprehensive documentation of all improvements
- **CHANGELOG.md** - This changelog file

#### Security Features
- Flask-Limiter integration for rate limiting (60 req/min, 1000 req/hour)
- CORS configuration with origin restrictions
- Health check endpoint (`/health`) for monitoring
- Error handling decorators (`@handle_api_errors`, `@require_initialized_services`)
- Structured error responses (no information leakage in production)

#### Testing Infrastructure
- pytest test framework configuration
- Mock-based unit tests for external dependencies
- Test fixtures for common scenarios
- Coverage tracking support (pytest-cov)

#### Code Quality Tools
- mypy for static type checking
- pylint for code linting
- Type stubs (types-pyyaml, types-requests)
- Black formatter integration

#### Performance Features
- Database connection context manager for automatic cleanup
- API retry logic with exponential backoff (3 retries, 2x backoff)
- Connection pooling support

### Changed

#### automation/campaign_manager.py
- Added comprehensive type hints to all methods
- Replaced hardcoded config loading with `utils.load_config()`
- Implemented retry logic for API requests using `@retry_on_failure`
- Used `calculate_percentage()` utility instead of inline calculations
- Enhanced error handling with specific exception types
- Added configuration validation on initialization
- Improved logging with context

#### automation/analytics.py
- Added comprehensive type hints
- Implemented database connection context manager (`_get_db_connection`)
- Replaced magic numbers with constants from `constants.py`
- Used `RiskLevel` enum for type safety
- Integrated `calculate_percentage()` utility
- Enhanced error handling and logging
- Configuration validation on initialization

#### automation/training_automation.py
- Added type hints for all methods
- Integrated with constants module for thresholds
- Used `load_config()` utility
- Improved configuration validation
- Enhanced error handling

#### automation/user_import.py
- Added comprehensive type hints
- Used `validate_email()` and `sanitize_string()` utilities
- Integrated with constants module
- Improved configuration validation
- Enhanced error handling with specific exceptions

#### dashboard/app.py
- Added Flask-Limiter for rate limiting
- Implemented error handling decorators
- Added health check endpoint
- Restricted CORS origins
- Enhanced logging configuration
- Type hints for all route handlers
- Graceful error handling in all endpoints
- Service availability checks

#### requirements.txt
- Added `flask-limiter==3.5.0`
- Added pytest testing dependencies (`pytest-mock`, `pytest-flask`)
- Added type checking tools (`mypy`, type stubs)
- Added code quality tools (`pylint`)
- Added production server (`gunicorn`)

### Improved

#### Error Handling
- Custom exception hierarchy (`APIError`, `ValidationError`, `ConfigurationError`)
- Specific exception handling for different error types
- Exception chaining for better debugging
- Contextual error messages
- Structured logging

#### Documentation
- Enhanced docstrings with Args, Returns, Raises sections
- Added type information to all docstrings
- Inline comments for complex logic
- Code examples in docstrings
- Architecture documentation

#### Configuration Management
- Centralized configuration loading with validation
- Required key validation on initialization
- Type-safe configuration access
- Clear error messages for misconfigurations

#### Code Organization
- Removed code duplication through utilities module
- Separated concerns with new modules
- Consistent code style across all modules
- Modular architecture

### Fixed

- Database connection leaks (now properly closed via context manager)
- Inconsistent percentage calculations (now uses utility function)
- Hardcoded magic numbers (now uses constants)
- Missing error handling in several endpoints
- Potential division by zero errors
- SSL warning spam in logs

### Security

- **Rate Limiting**: Prevents API abuse and DoS attacks
- **CORS Restrictions**: Limits cross-origin requests to trusted origins
- **Error Message Sanitization**: Prevents information disclosure
- **Input Validation**: Email validation and string sanitization
- **Configuration Validation**: Prevents misconfiguration-based vulnerabilities

## [1.0.0] - 2025-01-14

### Added
- Initial release
- GoPhish campaign management
- User risk scoring analytics
- Automated training assignment
- Web dashboard with visualizations
- CSV user import functionality
- Email templates and landing pages
- Comprehensive test suite
- Docker support
- Documentation

---

## Upgrade Guide

### From 1.0.0 to 1.1.0

1. **Install new dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Update configuration (if needed):**
   - No configuration changes required
   - All new features are backwards compatible

3. **Run tests to verify:**
   ```bash
   pytest tests/ -v
   ```

4. **Optional - Use new utilities:**
   ```python
   # In your custom code, you can now use:
   from automation.utils import load_config, validate_email, calculate_percentage
   from automation.constants import RISK_THRESHOLD_HIGH, RiskLevel
   ```

5. **Optional - Run type checking:**
   ```bash
   mypy automation/
   ```

### Breaking Changes
**None** - All changes are backwards compatible.

---

## Deprecated

- None in this release

## Removed

- None in this release

---

## Notes

### Development
- All modules now have comprehensive type hints
- Run `black automation/ dashboard/ tests/` to format code
- Run `pytest tests/ --cov=automation` for coverage report

### Production
- Use `gunicorn` for production deployment:
  ```bash
  gunicorn -w 4 -b 0.0.0.0:5000 dashboard.app:app
  ```
- Monitor health endpoint: `GET /health`
- Configure rate limits in `automation/constants.py`

---

For detailed information about improvements, see [IMPROVEMENTS.md](IMPROVEMENTS.md).
