# Contributing to Phishing Awareness Training Platform

First off, thank you for considering contributing to this project! It's people like you that make this platform better for everyone.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)

---

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

---

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples**
- **Describe the behavior you observed and what you expected**
- **Include screenshots if applicable**
- **Include your environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description of the suggested enhancement**
- **Explain why this enhancement would be useful**
- **List any similar features in other tools if applicable**

### Pull Requests

We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code follows the coding standards
6. Issue the pull request!

---

## Development Setup

### Prerequisites

- Python 3.10 or higher
- Git
- Virtual environment tool (venv, virtualenv, or conda)

### Setup Steps

```bash
# Clone the repository
git clone https://github.com/Raoof128/phishing-platform.git
cd phishing-platform

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests to verify setup
pytest tests/ -v
```

---

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some modifications:

- **Line length**: 100 characters (configured in Black)
- **Indentation**: 4 spaces
- **Imports**: Organized with isort
- **Type hints**: Required for all new functions

### Code Formatting

We use **Black** for code formatting:

```bash
# Format all Python files
black automation/ dashboard/ tests/

# Check formatting without applying
black --check automation/ dashboard/ tests/
```

### Import Organization

We use **isort** for import sorting:

```bash
# Sort imports
isort automation/ dashboard/ tests/

# Check import sorting
isort --check-only automation/ dashboard/ tests/
```

### Linting

We use **flake8** and **pylint**:

```bash
# Run flake8
flake8 automation/ dashboard/

# Run pylint
pylint automation/
```

### Type Checking

We use **mypy** for static type checking:

```bash
# Run type checking
mypy automation/
```

### Code Quality Checklist

Before submitting a PR, ensure:

- [ ] Code is formatted with Black
- [ ] Imports are sorted with isort
- [ ] No flake8 warnings
- [ ] Pylint score > 8.0
- [ ] mypy passes with no errors
- [ ] All tests pass
- [ ] New code has tests
- [ ] Documentation is updated

---

## Testing Guidelines

### Writing Tests

- Use **pytest** for all tests
- Place tests in the `tests/` directory
- Name test files as `test_*.py`
- Use descriptive test function names: `test_<functionality>_<scenario>`
- Use fixtures for common setup
- Mock external dependencies (API calls, database, etc.)

### Test Structure

```python
def test_function_name_scenario():
    """Test description"""
    # Arrange - Set up test data
    input_data = {...}

    # Act - Execute the function
    result = function_under_test(input_data)

    # Assert - Verify the result
    assert result == expected_value
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_utils.py -v

# Run with coverage
pytest tests/ --cov=automation --cov-report=html

# Run only unit tests
pytest tests/ -m unit

# Run excluding slow tests
pytest tests/ -m "not slow"
```

### Coverage Requirements

- **Minimum coverage**: 80%
- **New code coverage**: 90%
- Exclude from coverage: `__repr__`, `__str__`, `if __name__ == "__main__"`

---

## Commit Message Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/):

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, missing semi-colons, etc.)
- **refactor**: Code refactoring
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **chore**: Maintenance tasks
- **ci**: CI/CD changes

### Examples

```
feat(analytics): add risk trend visualization

Implement new chart showing risk score trends over time for users.
Includes filterable date range and export to CSV functionality.

Closes #123
```

```
fix(dashboard): resolve rate limiting 429 errors

Increase rate limit from 60 to 100 requests per minute and add
retry logic with exponential backoff.

Fixes #456
```

---

## Pull Request Process

### Before Submitting

1. **Update documentation** if you changed functionality
2. **Add tests** for new features
3. **Run the full test suite** and ensure it passes
4. **Update CHANGELOG.md** with your changes
5. **Ensure code quality** tools pass (black, flake8, mypy, pylint)

### PR Title Format

Use conventional commits format:

```
feat(component): add new functionality
fix(component): resolve specific issue
docs: update installation guide
```

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe testing performed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] No new warnings
```

### Review Process

1. At least **one approving review** required
2. All **CI checks must pass**
3. **No unresolved conversations**
4. **No merge conflicts**
5. **Branch is up-to-date** with main

### After Approval

- Squash and merge (for clean history)
- Delete the source branch
- Close related issues

---

## Development Workflow

### Branching Strategy

- `main` - Production-ready code
- `develop` - Integration branch (if used)
- `feature/<name>` - New features
- `fix/<name>` - Bug fixes
- `docs/<name>` - Documentation updates
- `refactor/<name>` - Code refactoring

### Feature Development

```bash
# Create feature branch
git checkout -b feature/my-new-feature

# Make changes and commit
git add .
git commit -m "feat(component): add new feature"

# Push to remote
git push origin feature/my-new-feature

# Create pull request on GitHub
```

---

## Questions?

- Check the [documentation](docs/)
- Review existing [issues](https://github.com/Raoof128/phishing-platform/issues)
- Ask in [discussions](https://github.com/Raoof128/phishing-platform/discussions)

---

## Recognition

Contributors will be recognized in:

- [README.md](README.md) contributors section
- Release notes
- Project documentation

Thank you for contributing! 🎉
