#!/usr/bin/env python3
"""
Comprehensive Test Suite for Phishing Platform
Tests all modules, imports, configurations, and functionality

IMPORTANT: Run with: source venv/bin/activate && python3 comprehensive_test.py
Or use: ./run_tests.sh
"""

import sys
import os
from pathlib import Path

# Check if running in virtual environment
if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    print("\n⚠️  WARNING: Not running in virtual environment!")
    print("Please run: source venv/bin/activate && python3 comprehensive_test.py")
    print("Or use: ./run_tests.sh\n")
    # Continue anyway but warn

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

passed_tests = 0
failed_tests = 0
warnings = 0

def print_test(name, status, message=""):
    global passed_tests, failed_tests, warnings
    if status == "PASS":
        print(f"{GREEN}✓{RESET} {name}")
        passed_tests += 1
    elif status == "FAIL":
        print(f"{RED}✗{RESET} {name}")
        if message:
            print(f"  {RED}Error: {message}{RESET}")
        failed_tests += 1
    elif status == "WARN":
        print(f"{YELLOW}⚠{RESET} {name}")
        if message:
            print(f"  {YELLOW}{message}{RESET}")
        warnings += 1

def print_header(text):
    print(f"\n{BLUE}{'='*70}{RESET}")
    print(f"{BLUE}{text}{RESET}")
    print(f"{BLUE}{'='*70}{RESET}\n")

# Test 1: Python Modules Import
print_header("Testing Python Module Imports")

try:
    from automation import campaign_manager
    print_test("automation.campaign_manager", "PASS")
except Exception as e:
    print_test("automation.campaign_manager", "FAIL", str(e))

try:
    from automation import analytics
    print_test("automation.analytics", "PASS")
except Exception as e:
    print_test("automation.analytics", "FAIL", str(e))

try:
    from automation import training_automation
    print_test("automation.training_automation", "PASS")
except Exception as e:
    print_test("automation.training_automation", "FAIL", str(e))

try:
    from automation import user_import
    print_test("automation.user_import", "PASS")
except Exception as e:
    print_test("automation.user_import", "FAIL", str(e))

try:
    from dashboard import app
    print_test("dashboard.app", "PASS")
except Exception as e:
    print_test("dashboard.app", "FAIL", str(e))

# Test 2: Configuration Files
print_header("Testing Configuration Files")

try:
    import yaml
    with open('automation/config/api_config.yaml', 'r') as f:
        config = yaml.safe_load(f)
        if 'gophish' in config and 'api_key' in config['gophish']:
            print_test("automation/config/api_config.yaml structure", "PASS")
        else:
            print_test("automation/config/api_config.yaml structure", "WARN", "Missing required keys")
except Exception as e:
    print_test("automation/config/api_config.yaml", "FAIL", str(e))

try:
    with open('automation/config/smtp_config.yaml', 'r') as f:
        config = yaml.safe_load(f)
        if 'smtp_profiles' in config:
            print_test("automation/config/smtp_config.yaml structure", "PASS")
        else:
            print_test("automation/config/smtp_config.yaml structure", "WARN", "Missing smtp_profiles")
except Exception as e:
    print_test("automation/config/smtp_config.yaml", "FAIL", str(e))

try:
    import json
    with open('gophish/config.json', 'r') as f:
        config = json.load(f)
        if 'admin_server' in config and 'phish_server' in config:
            print_test("gophish/config.json structure", "PASS")
        else:
            print_test("gophish/config.json structure", "FAIL", "Missing required keys")
except Exception as e:
    print_test("gophish/config.json", "FAIL", str(e))

# Test 3: File Existence
print_header("Testing Required Files")

required_files = [
    'requirements.txt',
    'README.md',
    'GETTING_STARTED.md',
    'setup.sh',
    'quickstart.sh',
    'run_gophish.sh',
    'run_dashboard.sh',
    'update_api_key.sh',
    'automation/__init__.py',
    'dashboard/__init__.py',
    'dashboard/templates/index.html',
]

for file in required_files:
    if os.path.exists(file):
        print_test(f"File exists: {file}", "PASS")
    else:
        print_test(f"File exists: {file}", "FAIL", "File not found")

# Test 4: Directory Structure
print_header("Testing Directory Structure")

required_dirs = [
    'automation',
    'automation/config',
    'dashboard',
    'dashboard/templates',
    'config',
    'templates',
    'templates/emails',
    'templates/landing_pages',
    'training',
    'training/modules',
    'docs',
    'examples',
]

for dir_path in required_dirs:
    if os.path.isdir(dir_path):
        print_test(f"Directory exists: {dir_path}", "PASS")
    else:
        print_test(f"Directory exists: {dir_path}", "FAIL", "Directory not found")

# Test 5: Shell Scripts Executable
print_header("Testing Shell Script Permissions")

shell_scripts = [
    'setup.sh',
    'quickstart.sh',
    'run_gophish.sh',
    'run_dashboard.sh',
    'update_api_key.sh',
]

for script in shell_scripts:
    if os.path.exists(script):
        if os.access(script, os.X_OK):
            print_test(f"{script} executable", "PASS")
        else:
            print_test(f"{script} executable", "WARN", "Not executable - run: chmod +x " + script)
    else:
        print_test(f"{script} exists", "FAIL", "File not found")

# Test 6: Class Instantiation
print_header("Testing Class Instantiation")

try:
    from automation.campaign_manager import GophishCampaign, load_config
    print_test("GophishCampaign class import", "PASS")

    # Test if load_config function exists
    print_test("load_config function import", "PASS")
except Exception as e:
    print_test("GophishCampaign/load_config", "FAIL", str(e))

try:
    from automation.analytics import PhishingAnalytics
    print_test("PhishingAnalytics class import", "PASS")
except Exception as e:
    print_test("PhishingAnalytics class", "FAIL", str(e))

try:
    from automation.training_automation import TrainingAutomation
    print_test("TrainingAutomation class import", "PASS")
except Exception as e:
    print_test("TrainingAutomation class", "FAIL", str(e))

try:
    from automation.user_import import UserImporter
    print_test("UserImporter class import", "PASS")
except Exception as e:
    print_test("UserImporter class", "FAIL", str(e))

# Test 7: Dependencies
print_header("Testing Python Dependencies")

required_packages = [
    'flask',
    'flask_cors',
    'requests',
    'pandas',
    'yaml',
    'plotly',
]

for package in required_packages:
    try:
        __import__(package)
        print_test(f"Package: {package}", "PASS")
    except ImportError:
        print_test(f"Package: {package}", "FAIL", f"pip install {package}")

# Test 8: Template Files
print_header("Testing Template Files")

template_files = [
    'templates/emails/password_reset.html',
    'templates/emails/security_alert.html',
    'templates/landing_pages/office365_login.html',
    'templates/landing_pages/gmail_login.html',
]

for template in template_files:
    if os.path.exists(template):
        # Check if it's valid HTML
        with open(template, 'r') as f:
            content = f.read()
            if '<html' in content.lower() or '<!doctype' in content.lower():
                print_test(f"Template: {template}", "PASS")
            else:
                print_test(f"Template: {template}", "WARN", "May not be valid HTML")
    else:
        print_test(f"Template: {template}", "FAIL", "File not found")

# Summary
print_header("Test Summary")

total_tests = passed_tests + failed_tests + warnings

print(f"Total Tests: {total_tests}")
print(f"{GREEN}Passed: {passed_tests}{RESET}")
print(f"{RED}Failed: {failed_tests}{RESET}")
print(f"{YELLOW}Warnings: {warnings}{RESET}")
print()

if failed_tests == 0:
    print(f"{GREEN}✓ All critical tests passed!{RESET}")
    sys.exit(0)
else:
    print(f"{RED}✗ {failed_tests} tests failed{RESET}")
    sys.exit(1)
