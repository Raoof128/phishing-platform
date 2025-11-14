# Phishing Awareness Training Platform

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Security](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Tests](https://img.shields.io/badge/tests-pytest-orange.svg)](https://docs.pytest.org/)

> **A comprehensive phishing simulation and security awareness training platform for defensive security education**

A professional-grade platform for conducting authorized phishing simulations, tracking user responses, and providing targeted security awareness training. Built on GoPhish with enhanced Python automation, analytics, and training workflows.

---

## 🌟 Features

### Campaign Management
- ✅ **Automated Campaign Orchestration** - Schedule and manage phishing campaigns with Python automation
- ✅ **Multiple Attack Scenarios** - Pre-built templates for credential harvesting, malware, urgency-based attacks
- ✅ **Custom Landing Pages** - Professional credential capture and awareness pages
- ✅ **Bulk User Import** - CSV-based user and group management

### Analytics & Reporting
- 📊 **Real-Time Dashboard** - Flask-based web interface with interactive visualizations
- 📈 **Risk Scoring Algorithm** - Individual user risk assessment based on behavior patterns
- 📉 **Campaign Metrics** - Open rates, click rates, submission rates, and report rates
- 📑 **Comprehensive Reports** - Exportable reports with actionable insights

### Security & Training
- 🔒 **Automated Training Assignment** - Personalized training based on risk scores
- 🛡️ **Security Headers** - CSP, HSTS, X-Frame-Options, and more
- ⚡ **Rate Limiting** - Built-in protection (60 req/min, 1000 req/hour)
- 🔐 **Input Validation** - Comprehensive validation against injection attacks

### Development & Testing
- ✅ **Comprehensive Test Suite** - 60+ tests with pytest
- 🔄 **CI/CD Pipeline** - Automated testing across Python 3.10, 3.11, 3.12
- 🐳 **Docker Support** - Production-ready containerization
- 📝 **Type Hints** - Full type annotations for better code quality

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage](#-usage)
- [Architecture](#-architecture)
- [Documentation](#-documentation)
- [Development](#-development)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- GoPhish installation
- SMTP server access (Gmail, SendGrid, or custom)

### Installation

```bash
# Clone the repository
git clone https://github.com/Raoof128/phishing-platform.git
cd phishing-platform

# Initialize development environment
make init

# Configure API and SMTP settings
cp automation/config/api_config.yaml.example automation/config/api_config.yaml
cp automation/config/smtp_config.yaml.example automation/config/smtp_config.yaml
nano automation/config/api_config.yaml  # Edit with your settings

# Run tests
make test

# Start the dashboard
make run-dashboard
```

Visit `http://localhost:5000` to access the analytics dashboard.

---

## 💻 Installation

### Option 1: Local Installation

```bash
# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup pre-commit hooks (for development)
pip install pre-commit
pre-commit install

# Run tests
pytest tests/ -v
```

### Option 2: Docker Installation

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f dashboard

# Stop services
docker-compose down
```

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for production deployment instructions.

---

## 🎯 Usage

### Import Users

```bash
# Import users from CSV
python automation/user_import.py \
  --csv users.csv \
  --group "Finance Department"
```

**CSV Format:**
```csv
first_name,last_name,email,position
John,Doe,john.doe@company.com,Manager
Jane,Smith,jane.smith@company.com,Analyst
```

### Create and Launch Campaign

```bash
# Create a new campaign
python automation/campaign_manager.py \
  --action create \
  --name "Q1 Security Awareness" \
  --template "password_reset" \
  --landing-page "office365_login" \
  --group "Finance Department" \
  --launch "2025-03-01 09:00"
```

### View Campaign Results

```bash
# Get campaign statistics
python automation/analytics.py \
  --campaign-id 5 \
  --output report.html
```

### Access Web Dashboard

```bash
# Start the dashboard
python dashboard/app.py

# Or using Make
make run-dashboard
```

Access at: `http://localhost:5000`

**Available Endpoints:**
- `/` - Main dashboard
- `/api/campaigns` - List all campaigns
- `/api/user_risks` - User risk scores
- `/api/dashboard_summary` - Overall statistics

See [API.md](docs/API.md) for complete API documentation.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│  ┌──────────────────┐              ┌────────────────────┐   │
│  │  Web Dashboard   │              │    CLI Tools       │   │
│  │   (Flask App)    │              │  (Python Scripts)  │   │
│  └────────┬─────────┘              └─────────┬──────────┘   │
└───────────┼────────────────────────────────────┼─────────────┘
            │                                    │
┌───────────┼────────────────────────────────────┼─────────────┐
│           ▼              Application Layer     ▼             │
│  ┌────────────────┐  ┌──────────────┐  ┌──────────────────┐ │
│  │  Campaign API  │  │  Analytics   │  │  Training Auto   │ │
│  │                │  │   Engine     │  │                  │ │
│  └───────┬────────┘  └──────┬───────┘  └─────────┬────────┘ │
└──────────┼────────────────────┼────────────────────┼──────────┘
           │                    │                    │
┌──────────┼────────────────────┼────────────────────┼──────────┐
│          ▼     Integration    ▼                    ▼          │
│  ┌────────────────┐      ┌──────────────┐   ┌──────────────┐ │
│  │  GoPhish API   │      │ SMTP Server  │   │   Database   │ │
│  └────────────────┘      └──────────────┘   └──────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

**Key Components:**

- **GoPhish Core**: Campaign execution and email delivery
- **Python Automation**: Campaign management and orchestration
- **Analytics Engine**: Risk scoring and metrics calculation
- **Flask Dashboard**: Web-based visualization and reporting
- **Training Module**: Automated training assignment

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed architecture documentation with diagrams.

---

## 📚 Documentation

### User Documentation
- [Installation Guide](docs/DEPLOYMENT.md#local-development) - Complete installation instructions
- [API Documentation](docs/API.md) - REST API reference
- [Deployment Guide](docs/DEPLOYMENT.md) - Production deployment
- [Architecture Overview](docs/ARCHITECTURE.md) - System design and data flows

### Developer Documentation
- [Contributing Guidelines](CONTRIBUTING.md) - How to contribute
- [Code of Conduct](CODE_OF_CONDUCT.md) - Community standards
- [Security Policy](SECURITY.md) - Reporting vulnerabilities
- [Changelog](CHANGELOG.md) - Version history
- [Roadmap](ROADMAP.md) - Planned features

---

## 🛠️ Development

### Setup Development Environment

```bash
# Install development dependencies
make install-dev

# Run all checks
make check

# Format code
make format

# Run linters
make lint

# Run type checker
make type-check

# Run security checks
make security

# Run tests with coverage
make test
```

### Available Make Commands

```bash
make help              # Show all available commands
make init              # Initialize development environment
make test              # Run test suite with coverage
make format            # Format code with black and isort
make lint              # Run linters (flake8, pylint)
make type-check        # Run mypy type checker
make security          # Run security checks (bandit, safety)
make clean             # Clean build artifacts
make docker-up         # Start Docker containers
make pre-commit        # Run pre-commit hooks
```

### Project Structure

```
phishing-platform/
├── automation/              # Core Python modules
│   ├── campaign_manager.py  # Campaign CRUD operations
│   ├── analytics.py         # Risk scoring and analytics
│   ├── training_automation.py # Training assignment
│   ├── user_import.py       # User management
│   ├── validation.py        # Input validation (NEW)
│   ├── constants.py         # Configuration constants (NEW)
│   └── utils.py             # Shared utilities (NEW)
├── dashboard/               # Flask web application
│   ├── app.py              # Main Flask app with API
│   ├── templates/          # HTML templates
│   └── static/             # Static assets
├── tests/                   # Test suite (NEW)
│   ├── conftest.py         # Pytest fixtures
│   ├── test_campaign_manager.py
│   ├── test_analytics.py
│   ├── test_training_automation.py
│   ├── test_user_import.py
│   ├── test_dashboard.py
│   └── test_validation.py
├── docs/                    # Documentation (NEW)
│   ├── ARCHITECTURE.md     # Architecture diagrams
│   ├── API.md              # API documentation
│   └── DEPLOYMENT.md       # Deployment guide
├── .github/                 # GitHub configuration (NEW)
│   ├── workflows/ci.yml    # CI/CD pipeline
│   └── ISSUE_TEMPLATE/     # Issue templates
├── Dockerfile               # Docker configuration (NEW)
├── docker-compose.yml       # Multi-container setup (NEW)
├── Makefile                 # Development commands (NEW)
├── pyproject.toml           # Python project config (NEW)
├── .pre-commit-config.yaml  # Pre-commit hooks (NEW)
└── requirements.txt         # Python dependencies
```

---

## 🚢 Deployment

### Docker Deployment (Recommended)

```bash
# Production deployment with Docker Compose
docker-compose up -d

# Access services
# Dashboard: http://localhost:5000
# GoPhish Admin: http://localhost:3333
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000
```

### Manual Production Deployment

```bash
# Setup on Ubuntu 22.04
sudo apt update && sudo apt install -y python3.10 postgresql nginx

# Setup database
sudo -u postgres createdb gophish
sudo -u postgres createuser gophish

# Clone and configure
git clone https://github.com/Raoof128/phishing-platform.git
cd phishing-platform
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure systemd service
sudo cp phishing-dashboard.service /etc/systemd/system/
sudo systemctl enable phishing-dashboard
sudo systemctl start phishing-dashboard

# Configure Nginx reverse proxy
sudo cp nginx.conf /etc/nginx/sites-available/phishing-platform
sudo ln -s /etc/nginx/sites-available/phishing-platform /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for complete deployment instructions including AWS, GCP, and Azure.

---

## 🔒 Security

### Security Features

- ✅ Rate limiting (60 req/min, 1000 req/hour)
- ✅ Security headers (CSP, HSTS, X-Frame-Options)
- ✅ Input validation and sanitization
- ✅ CORS protection
- ✅ SQL injection prevention
- ✅ XSS protection
- ⏳ JWT authentication (planned v1.2.0)

### Reporting Security Issues

**DO NOT** open public issues for security vulnerabilities.

Please report security vulnerabilities to: **security@company.com**

See [SECURITY.md](SECURITY.md) for our security policy and disclosure process.

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on:

- Code of conduct
- Development process
- Submitting pull requests
- Coding standards
- Testing requirements

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`make test`)
5. Run pre-commit checks (`pre-commit run --all-files`)
6. Commit your changes (`git commit -m 'feat: Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

---

## 📊 Project Status

### Current Version: 1.1.0

**Recent Updates:**
- ✅ Comprehensive test suite (60+ tests)
- ✅ Security enhancements (headers, validation, rate limiting)
- ✅ Type hints and documentation
- ✅ CI/CD pipeline with GitHub Actions
- ✅ Docker support with multi-stage builds
- ✅ Professional project infrastructure

**Coming in v1.2.0 (Q1 2025):**
- 🔐 JWT-based authentication
- 👥 Role-based access control (RBAC)
- 📊 Advanced reporting and exports
- 🎨 Enhanced dashboard UI/UX

See [ROADMAP.md](ROADMAP.md) for the complete feature roadmap through 2026.

---

## ⚖️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Legal and Ethical Use

### Important Notice

**This platform is designed EXCLUSIVELY for authorized security awareness training and defensive security purposes.**

### Requirements

1. ✅ **Written Authorization** - Obtain explicit written permission before conducting any campaigns
2. ✅ **Scope Definition** - Clearly define boundaries and target audience
3. ✅ **Data Security** - Implement secure storage for all captured data
4. ✅ **Immediate Feedback** - Provide training materials immediately after simulation
5. ✅ **Educational Focus** - Focus on education and improvement, not punishment

### You Must NOT

- ❌ Use this platform for unauthorized phishing attacks
- ❌ Target individuals without proper authorization
- ❌ Retain captured credentials beyond training purposes
- ❌ Use platform capabilities for malicious purposes
- ❌ Violate applicable laws or regulations

**Users are solely responsible for ensuring lawful and authorized use.**

---

## 💬 Support

### Getting Help

- 📖 [Documentation](docs/)
- 🐛 [Issue Tracker](https://github.com/Raoof128/phishing-platform/issues)
- 💡 [Feature Requests](https://github.com/Raoof128/phishing-platform/issues/new?template=feature_request.yml)
- 🗨️ [Discussions](https://github.com/Raoof128/phishing-platform/discussions)

### Community

- Star this repository if you find it useful! ⭐
- Follow the project for updates
- Share your success stories in Discussions

---

## 🙏 Acknowledgments

- **GoPhish Team** - For the excellent phishing simulation framework
- **Flask Community** - For the powerful web framework
- **Contributors** - Thank you to all who have contributed to this project

---

## 📈 Statistics

![GitHub stars](https://img.shields.io/github/stars/Raoof128/phishing-platform?style=social)
![GitHub forks](https://img.shields.io/github/forks/Raoof128/phishing-platform?style=social)
![GitHub issues](https://img.shields.io/github/issues/Raoof128/phishing-platform)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Raoof128/phishing-platform)

---

<p align="center">
  <strong>Built with ❤️ for defensive security and security awareness training</strong>
</p>

<p align="center">
  <a href="#phishing-awareness-training-platform">Back to Top ↑</a>
</p>
