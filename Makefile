.PHONY: help install install-dev test lint format type-check security clean run docker-build docker-up docker-down docs

# Default target
.DEFAULT_GOAL := help

# Variables
PYTHON := python3
PIP := $(PYTHON) -m pip
PYTEST := pytest
BLACK := black
ISORT := isort
FLAKE8 := flake8
MYPY := mypy
PYLINT := pylint
SAFETY := safety
BANDIT := bandit

# Source directories
SRC_DIRS := automation dashboard tests

help: ## Show this help message
	@echo "Phishing Awareness Training Platform - Make Commands"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -r requirements.txt

install-dev: install ## Install development dependencies
	$(PIP) install -e ".[dev]"
	pre-commit install

test: ## Run test suite
	$(PYTEST) tests/ -v --cov=automation --cov=dashboard --cov-report=term --cov-report=html

test-quick: ## Run tests without coverage
	$(PYTEST) tests/ -v

test-unit: ## Run only unit tests
	$(PYTEST) tests/ -v -m unit

test-integration: ## Run only integration tests
	$(PYTEST) tests/ -v -m integration

format: ## Format code with black and isort
	$(BLACK) $(SRC_DIRS)
	$(ISORT) $(SRC_DIRS)

format-check: ## Check code formatting
	$(BLACK) --check $(SRC_DIRS)
	$(ISORT) --check-only $(SRC_DIRS)

lint: ## Run linters (flake8 and pylint)
	$(FLAKE8) automation/ dashboard/ --max-line-length=100
	$(PYLINT) automation/ --fail-under=8.0

type-check: ## Run type checker
	$(MYPY) automation/ --ignore-missing-imports

security: ## Run security checks
	$(SAFETY) check -r requirements.txt
	$(BANDIT) -r automation/ dashboard/ -ll

check: format-check lint type-check security test ## Run all checks

clean: ## Clean build artifacts and cache files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "build" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .coverage coverage.xml

run-dashboard: ## Run analytics dashboard
	$(PYTHON) dashboard/app.py

run-campaign: ## Run campaign manager CLI
	$(PYTHON) -m automation.campaign_manager --help

run-analytics: ## Run analytics CLI
	$(PYTHON) -m automation.analytics --help

docker-build: ## Build Docker image
	docker build -t phishing-platform:latest .

docker-up: ## Start Docker containers
	docker-compose up -d

docker-down: ## Stop Docker containers
	docker-compose down

docker-logs: ## View Docker logs
	docker-compose logs -f

docker-clean: ## Remove Docker containers and volumes
	docker-compose down -v
	docker system prune -f

docs: ## Generate documentation
	@echo "Documentation is in docs/ directory"
	@echo "Open docs/index.html in your browser"

update-deps: ## Update dependencies
	$(PIP) install --upgrade -r requirements.txt
	$(PIP) freeze > requirements-lock.txt

pre-commit: ## Run pre-commit hooks manually
	pre-commit run --all-files

version: ## Show version information
	@echo "Python: $$($(PYTHON) --version)"
	@echo "Pip: $$($(PIP) --version)"
	@echo "Platform: $$(cat automation/__init__.py 2>/dev/null | grep version || echo 'Version not found')"

init: install-dev ## Initialize development environment
	@echo "Copying configuration examples..."
	@cp -n automation/config/api_config.yaml.example automation/config/api_config.yaml 2>/dev/null || true
	@cp -n automation/config/smtp_config.yaml.example automation/config/smtp_config.yaml 2>/dev/null || true
	@cp -n .env.example .env 2>/dev/null || true
	@echo "Development environment initialized!"
	@echo "Edit automation/config/*.yaml and .env with your settings"

build: clean ## Build distribution packages
	$(PYTHON) -m build

all: clean install-dev format lint type-check security test ## Run full CI pipeline locally

.SILENT: help version
