# Phishing Attack Simulation and Training Platform

A comprehensive phishing simulation and security awareness training platform using GoPhish as the core engine, enhanced with Python automation for campaign management, analytics, and user training workflows.

## Overview

This platform simulates real-world phishing attacks, tracks user responses, and provides targeted training to improve organizational security awareness. It's designed for defensive security purposes only - helping organizations train their employees to recognize and resist phishing attacks.

## Features

- **Automated Campaign Management**: Schedule and manage phishing campaigns with Python automation
- **Realistic Email Templates**: Multiple attack scenario templates (credential harvesting, malware, urgency-based, social engineering)
- **Landing Pages**: Custom credential capture and awareness pages
- **Analytics Dashboard**: Real-time campaign performance tracking and visualization
- **Risk Scoring**: Individual user risk assessment based on historical behavior
- **Automated Training**: Personalized security awareness training based on performance
- **Comprehensive Reporting**: Detailed campaign reports with actionable insights

## System Architecture

- **Core Engine**: GoPhish (open-source phishing framework)
- **Automation Layer**: Python scripts for campaign orchestration
- **Analytics Dashboard**: Custom Flask-based reporting and visualization
- **Training Module**: Automated awareness content delivery
- **Email Infrastructure**: SMTP configuration for campaign delivery
- **Landing Pages**: Custom credential capture and awareness pages

## Technical Stack

- **Phishing Framework**: GoPhish v0.12+
- **Backend**: Python 3.10+, Flask
- **Database**: SQLite (GoPhish default) or PostgreSQL
- **Email**: SMTP (Gmail, SendGrid, or custom mail server)
- **Frontend**: HTML/CSS/JavaScript, Bootstrap 5
- **Analytics**: Pandas, Matplotlib, Plotly
- **Automation**: Python scheduled tasks

## Project Structure

```
phishing-platform/
├── README.md                   # This file
├── requirements.txt            # Python dependencies
├── gophish/                    # GoPhish installation directory
│   └── config.json            # GoPhish configuration
├── automation/                 # Python automation scripts
│   ├── __init__.py
│   ├── campaign_manager.py    # Campaign creation and scheduling
│   ├── analytics.py           # Analytics and reporting
│   ├── training_automation.py # Automated training assignment
│   ├── user_import.py         # User/group import utilities
│   └── config/
│       ├── api_config.yaml    # GoPhish API configuration
│       └── smtp_config.yaml   # SMTP server settings
├── dashboard/                  # Custom analytics dashboard
│   ├── app.py                 # Flask application
│   ├── templates/             # HTML templates
│   ├── static/                # CSS, JS, images
│   └── api/                   # API endpoints
├── templates/                  # Email and landing page templates
│   ├── emails/                # Phishing email templates
│   ├── landing_pages/         # Credential capture pages
│   └── assets/                # Shared assets
├── training/                   # Security awareness training content
│   └── modules/               # Training modules
├── config/                     # Configuration files
├── docs/                       # Documentation
└── tests/                      # Unit tests
```

## Installation

See [docs/installation_guide.md](docs/installation_guide.md) for complete installation instructions.

## Quick Start

### Import Users
```bash
python automation/user_import.py --csv users.csv --group "Finance Department"
```

### Create Campaign
```bash
python automation/campaign_manager.py \
  --template "password_reset" \
  --landing-page "office365_login" \
  --group "Finance Department" \
  --launch "2025-10-20 09:00"
```

### Monitor Results
```bash
python automation/analytics.py --campaign-id 5 --output report.html
```

## Security and Ethics

**IMPORTANT**: This platform is for authorized defensive security training only.

1. Get written permission before running campaigns
2. Clearly define scope and boundaries
3. Securely store captured data
4. Provide immediate training feedback
5. Focus on education, not punishment

## Legal Disclaimer

This platform is designed for authorized security awareness training and defensive security purposes only. Users are responsible for obtaining proper authorization and complying with all applicable laws.

## Documentation

- [Installation Guide](docs/installation_guide.md)
- [User Manual](docs/user_manual.md)
- [API Documentation](docs/api_documentation.md)
- [Troubleshooting](docs/troubleshooting.md)

---

**Built for defensive security and security awareness training**
