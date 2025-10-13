#!/usr/bin/env python3
"""
Comprehensive Platform Test Script
Tests all components of the Phishing Platform
"""

import os
import sys
import subprocess
from pathlib import Path


class PlatformTester:
    """Test suite for the phishing platform"""

    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.passed = 0
        self.failed = 0
        self.warnings = 0

    def print_header(self, text):
        """Print section header"""
        print(f"\n{'='*60}")
        print(f"  {text}")
        print(f"{'='*60}\n")

    def test_python_imports(self):
        """Test if all Python modules can be imported"""
        self.print_header("Testing Python Imports")

        modules = [
            ('automation.campaign_manager', 'Campaign Manager'),
            ('automation.analytics', 'Analytics'),
            ('automation.training_automation', 'Training Automation'),
            ('automation.user_import', 'User Import'),
        ]

        for module_name, description in modules:
            try:
                # Change to base directory for imports
                sys.path.insert(0, str(self.base_dir))
                __import__(module_name)
                print(f"  ✓ {description}: Import successful")
                self.passed += 1
            except ImportError as e:
                print(f"  ✗ {description}: Import failed - {e}")
                self.failed += 1
            except Exception as e:
                print(f"  ⚠ {description}: Warning - {e}")
                self.warnings += 1

    def test_configuration_files(self):
        """Test configuration file validity"""
        self.print_header("Testing Configuration Files")

        # Test YAML files
        try:
            import yaml

            configs = [
                'config/api_config.yaml',
                'config/smtp_config.yaml',
                'examples/campaign_config_example.yaml'
            ]

            for config_file in configs:
                path = self.base_dir / config_file
                if path.exists():
                    try:
                        with open(path, 'r') as f:
                            yaml.safe_load(f)
                        print(f"  ✓ {config_file}: Valid YAML")
                        self.passed += 1
                    except Exception as e:
                        print(f"  ✗ {config_file}: Invalid - {e}")
                        self.failed += 1
                else:
                    print(f"  ⚠ {config_file}: Not found")
                    self.warnings += 1

        except ImportError:
            print("  ⚠ PyYAML not installed, skipping YAML validation")
            self.warnings += 1

    def test_templates(self):
        """Test HTML template files"""
        self.print_header("Testing Templates")

        # Email templates
        email_templates = [
            'templates/emails/password_reset.html',
            'templates/emails/hr_document.html',
            'templates/emails/security_alert.html',
            'templates/emails/ceo_fraud.html',
            'templates/emails/account_verification.html',
        ]

        for template in email_templates:
            path = self.base_dir / template
            if path.exists() and path.stat().st_size > 0:
                # Check for GoPhish variables
                content = path.read_text()
                has_vars = '{{.FirstName}}' in content or '{{.Email}}' in content
                if has_vars:
                    print(f"  ✓ {template}: Valid with GoPhish variables")
                    self.passed += 1
                else:
                    print(f"  ⚠ {template}: Missing GoPhish variables")
                    self.warnings += 1
            else:
                print(f"  ✗ {template}: Not found or empty")
                self.failed += 1

        # Landing pages
        landing_pages = [
            'templates/landing_pages/office365_login.html',
            'templates/landing_pages/gmail_login.html',
            'templates/landing_pages/corporate_portal.html',
            'templates/landing_pages/awareness_page.html',
            'templates/landing_pages/training_redirect.html',
        ]

        for page in landing_pages:
            path = self.base_dir / page
            if path.exists() and path.stat().st_size > 0:
                content = path.read_text()
                has_tracker = '{{.Tracker}}' in content
                if has_tracker:
                    print(f"  ✓ {page}: Valid with tracking")
                    self.passed += 1
                else:
                    print(f"  ⚠ {page}: Missing tracker variable")
                    self.warnings += 1
            else:
                print(f"  ✗ {page}: Not found or empty")
                self.failed += 1

    def test_documentation(self):
        """Test documentation files"""
        self.print_header("Testing Documentation")

        docs = [
            'README.md',
            'GETTING_STARTED.md',
            'PROJECT_SUMMARY.md',
            'docs/installation.md',
            'docs/user_manual.md',
            'docs/api_documentation.md',
        ]

        for doc in docs:
            path = self.base_dir / doc
            if path.exists():
                size = path.stat().st_size
                if size > 1000:  # At least 1KB
                    print(f"  ✓ {doc}: Present ({size:,} bytes)")
                    self.passed += 1
                else:
                    print(f"  ⚠ {doc}: Too small ({size} bytes)")
                    self.warnings += 1
            else:
                print(f"  ✗ {doc}: Not found")
                self.failed += 1

    def test_training_modules(self):
        """Test training module files"""
        self.print_header("Testing Training Modules")

        modules = [
            'training/modules/module1_phishing_recognition.md',
            'training/modules/module2_social_engineering.md',
            'training/modules/module3_email_safety.md',
        ]

        for module in modules:
            path = self.base_dir / module
            if path.exists():
                content = path.read_text()
                # Check for key sections
                has_content = len(content) > 2000 and '##' in content
                if has_content:
                    print(f"  ✓ {module}: Complete ({len(content):,} chars)")
                    self.passed += 1
                else:
                    print(f"  ⚠ {module}: May be incomplete")
                    self.warnings += 1
            else:
                print(f"  ✗ {module}: Not found")
                self.failed += 1

    def test_scripts(self):
        """Test shell scripts and executables"""
        self.print_header("Testing Scripts")

        scripts = [
            'run_gophish.sh',
            'run_dashboard.sh',
            'setup.sh',
            'verify_installation.py',
            'gophish/gophish',
        ]

        for script in scripts:
            path = self.base_dir / script
            if path.exists():
                if os.access(path, os.X_OK):
                    print(f"  ✓ {script}: Executable")
                    self.passed += 1
                else:
                    print(f"  ⚠ {script}: Not executable (chmod +x needed)")
                    self.warnings += 1
            else:
                print(f"  ✗ {script}: Not found")
                self.failed += 1

    def test_dependencies(self):
        """Test Python dependencies"""
        self.print_header("Testing Python Dependencies")

        required = [
            'flask',
            'requests',
            'pandas',
            'yaml',
            'matplotlib',
        ]

        optional = [
            'plotly',
            'seaborn',
        ]

        for dep in required:
            try:
                __import__(dep)
                print(f"  ✓ {dep}: Installed")
                self.passed += 1
            except ImportError:
                print(f"  ✗ {dep}: Not installed (required)")
                self.failed += 1

        for dep in optional:
            try:
                __import__(dep)
                print(f"  ✓ {dep}: Installed")
                self.passed += 1
            except ImportError:
                print(f"  ⚠ {dep}: Not installed (optional)")
                self.warnings += 1

    def run_all_tests(self):
        """Run all test suites"""
        print("="*60)
        print("  Phishing Platform - Comprehensive Test Suite")
        print("="*60)

        self.test_dependencies()
        self.test_python_imports()
        self.test_configuration_files()
        self.test_templates()
        self.test_documentation()
        self.test_training_modules()
        self.test_scripts()

        # Summary
        self.print_header("Test Summary")

        total_tests = self.passed + self.failed + self.warnings
        pass_rate = (self.passed / total_tests * 100) if total_tests > 0 else 0

        print(f"Total Tests: {total_tests}")
        print(f"✓ Passed:    {self.passed} ({pass_rate:.1f}%)")
        print(f"✗ Failed:    {self.failed}")
        print(f"⚠ Warnings:  {self.warnings}")
        print()

        if self.failed == 0:
            print("🎉 All critical tests passed!")
            if self.warnings > 0:
                print(f"⚠️  {self.warnings} warning(s) - review recommended")
            return 0
        else:
            print(f"❌ {self.failed} test(s) failed - please fix before deployment")
            return 1


def main():
    """Main test runner"""
    tester = PlatformTester()
    sys.exit(tester.run_all_tests())


if __name__ == "__main__":
    main()
