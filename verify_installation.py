#!/usr/bin/env python3
"""
Installation Verification Script
Checks that all components of the Phishing Platform are properly installed
"""

import os
import sys
from pathlib import Path


def print_header(text):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def check_file(filepath, required=True):
    """Check if file exists"""
    exists = os.path.exists(filepath)
    status = "✓" if exists else ("✗" if required else "○")
    req_text = "" if required else " (optional)"
    print(f"  {status} {filepath}{req_text}")
    return exists


def check_directory(dirpath):
    """Check if directory exists"""
    exists = os.path.isdir(dirpath)
    status = "✓" if exists else "✗"
    print(f"  {status} {dirpath}/")
    return exists


def check_python_module(module_name):
    """Check if Python module is installed"""
    try:
        __import__(module_name)
        print(f"  ✓ {module_name}")
        return True
    except ImportError:
        print(f"  ✗ {module_name} (not installed)")
        return False


def main():
    print_header("Phishing Platform - Installation Verification")

    base_dir = Path(__file__).parent
    issues = []

    # Check directory structure
    print("Directory Structure:")
    dirs = [
        "gophish",
        "automation",
        "automation/config",
        "dashboard",
        "dashboard/templates",
        "dashboard/static",
        "templates",
        "templates/emails",
        "templates/landing_pages",
        "training",
        "training/modules",
        "config",
        "docs",
        "examples"
    ]

    for d in dirs:
        if not check_directory(base_dir / d):
            issues.append(f"Missing directory: {d}")

    # Check key files
    print("\nKey Files:")
    files = {
        "README.md": True,
        "requirements.txt": True,
        ".env.example": True,
        ".gitignore": True,
        "GETTING_STARTED.md": True,
        "gophish/gophish": True,
        "gophish/config.json": True,
        "automation/__init__.py": True,
        "automation/campaign_manager.py": True,
        "automation/analytics.py": True,
        "automation/training_automation.py": True,
        "automation/user_import.py": True,
        "dashboard/app.py": True,
        "dashboard/templates/index.html": True,
        "config/api_config.yaml": True,
        "config/smtp_config.yaml": True,
        ".env": False,  # Optional, user creates
    }

    for filepath, required in files.items():
        if not check_file(base_dir / filepath, required):
            if required:
                issues.append(f"Missing file: {filepath}")

    # Check email templates
    print("\nEmail Templates:")
    templates = [
        "templates/emails/password_reset.html",
        "templates/emails/hr_document.html",
        "templates/emails/security_alert.html",
        "templates/emails/ceo_fraud.html",
        "templates/emails/account_verification.html"
    ]

    for t in templates:
        if not check_file(base_dir / t):
            issues.append(f"Missing template: {t}")

    # Check landing pages
    print("\nLanding Pages:")
    pages = [
        "templates/landing_pages/office365_login.html",
        "templates/landing_pages/gmail_login.html",
        "templates/landing_pages/corporate_portal.html",
        "templates/landing_pages/awareness_page.html",
        "templates/landing_pages/training_redirect.html"
    ]

    for p in pages:
        if not check_file(base_dir / p):
            issues.append(f"Missing landing page: {p}")

    # Check training modules
    print("\nTraining Modules:")
    modules = [
        "training/modules/module1_phishing_recognition.md",
        "training/modules/module2_social_engineering.md",
        "training/modules/module3_email_safety.md"
    ]

    for m in modules:
        if not check_file(base_dir / m):
            issues.append(f"Missing training module: {m}")

    # Check documentation
    print("\nDocumentation:")
    docs = [
        "docs/installation.md",
        "docs/user_manual.md",
        "docs/api_documentation.md"
    ]

    for d in docs:
        if not check_file(base_dir / d):
            issues.append(f"Missing documentation: {d}")

    # Check Python dependencies
    print("\nPython Dependencies:")
    dependencies = [
        "flask",
        "requests",
        "pandas",
        "yaml",
        "matplotlib",
        "plotly"
    ]

    missing_deps = []
    for dep in dependencies:
        if not check_python_module(dep):
            missing_deps.append(dep)

    if missing_deps:
        issues.append(f"Missing Python packages: {', '.join(missing_deps)}")

    # Check GoPhish binary permissions
    print("\nGoPhish Binary:")
    gophish_bin = base_dir / "gophish" / "gophish"
    if gophish_bin.exists():
        if os.access(gophish_bin, os.X_OK):
            print(f"  ✓ GoPhish binary is executable")
        else:
            print(f"  ✗ GoPhish binary is not executable")
            issues.append("GoPhish binary needs execute permission: chmod +x gophish/gophish")
    else:
        print(f"  ✗ GoPhish binary not found")

    # Summary
    print_header("Verification Summary")

    if not issues:
        print("✓ All components verified successfully!")
        print("\n🎉 Your Phishing Platform is ready to use!")
        print("\nNext steps:")
        print("  1. Read GETTING_STARTED.md")
        print("  2. Configure your .env file")
        print("  3. Start GoPhish: ./run_gophish.sh")
        print("  4. Launch dashboard: ./run_dashboard.sh")
        return 0
    else:
        print(f"✗ Found {len(issues)} issue(s):\n")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")

        print("\n⚠️  Please fix these issues before proceeding.")
        print("Refer to docs/installation.md for help.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
