#!/bin/bash

# Phishing Platform - Automated Setup Script
# This script automates the complete installation process

set -e  # Exit on error

echo "============================================================"
echo "  Phishing Platform - Automated Setup"
echo "============================================================"
echo ""

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "ℹ $1"
}

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    print_error "This script is designed for Linux systems"
    exit 1
fi

# Check Python version
echo "Step 1/8: Checking Python version..."
if command -v python3 &> /dev/null; then
    # Use Python to compare versions instead of bc
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    VERSION_CHECK=$(python3 -c "import sys; print('OK' if sys.version_info >= (3, 10) else 'FAIL')")

    if [ "$VERSION_CHECK" = "OK" ]; then
        print_success "Python $PYTHON_VERSION found"
    else
        print_error "Python 3.10+ required (found $PYTHON_VERSION)"
        exit 1
    fi
else
    print_error "Python 3 not found. Please install Python 3.10+"
    exit 1
fi

# Create virtual environment
echo ""
echo "Step 2/8: Creating virtual environment..."
if [ -d "venv" ]; then
    print_warning "Virtual environment already exists"
    read -p "Remove and recreate? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf venv
        python3 -m venv venv
        print_success "Virtual environment recreated"
    else
        print_info "Using existing virtual environment"
    fi
else
    python3 -m venv venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo ""
echo "Step 3/8: Installing Python dependencies..."
if pip install --upgrade pip >> /tmp/phishing-platform-setup.log 2>&1; then
    print_info "pip upgraded successfully"
else
    print_warning "pip upgrade failed (non-critical)"
fi

if pip install -r requirements.txt >> /tmp/phishing-platform-setup.log 2>&1; then
    print_success "Python dependencies installed"
else
    print_error "Failed to install Python dependencies"
    print_info "Check /tmp/phishing-platform-setup.log for details"
    exit 1
fi

# Check GoPhish binary
echo ""
echo "Step 4/8: Verifying GoPhish installation..."
if [ -f "gophish/gophish" ]; then
    if [ -x "gophish/gophish" ]; then
        print_success "GoPhish binary is executable"
    else
        chmod +x gophish/gophish
        print_success "Made GoPhish binary executable"
    fi
else
    print_error "GoPhish binary not found at gophish/gophish"
    print_info "Please download GoPhish from https://github.com/gophish/gophish/releases"
    exit 1
fi

# Make shell scripts executable
echo ""
echo "Step 5/8: Setting up launcher scripts..."
chmod +x run_gophish.sh run_dashboard.sh verify_installation.py
print_success "Launcher scripts are executable"

# Create .env file if it doesn't exist
echo ""
echo "Step 6/8: Configuring environment..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    print_success "Created .env file from template"
    print_warning "Please edit .env file with your actual credentials"
else
    print_info ".env file already exists"
fi

# Create necessary directories
echo ""
echo "Step 7/8: Creating data directories..."
mkdir -p data logs reports
print_success "Created data directories"

# Run verification
echo ""
echo "Step 8/8: Running installation verification..."
if python3 verify_installation.py; then
    print_success "Installation verification passed"
else
    print_warning "Some verification checks failed (see details above)"
fi

# Summary
echo ""
echo "============================================================"
echo "  Setup Complete!"
echo "============================================================"
echo ""
echo "Next Steps:"
echo ""
echo "1. Configure your environment:"
echo "   ${YELLOW}nano .env${NC}"
echo ""
echo "2. Update API configuration:"
echo "   ${YELLOW}nano config/api_config.yaml${NC}"
echo ""
echo "3. Start GoPhish:"
echo "   ${YELLOW}./run_gophish.sh${NC}"
echo "   - Login at https://127.0.0.1:3333"
echo "   - Default: admin / gophish"
echo "   - Generate API key in Settings"
echo ""
echo "4. Start Dashboard:"
echo "   ${YELLOW}./run_dashboard.sh${NC}"
echo "   - Access at http://localhost:5000"
echo ""
echo "5. Read documentation:"
echo "   ${YELLOW}cat GETTING_STARTED.md${NC}"
echo ""
print_success "Setup complete! Ready to launch."
echo ""
