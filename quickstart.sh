#!/bin/bash

# Phishing Platform - Quick Start Script
# This script automates the platform startup and configuration

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
}

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
    echo -e "${BLUE}ℹ${NC} $1"
}

print_header "Phishing Platform - Quick Start"

# Check if setup has been run
if [ ! -d "venv" ]; then
    print_warning "Virtual environment not found. Running setup first..."
    ./setup.sh
    echo ""
fi

# Check if GoPhish is already running
if pgrep -x "gophish" > /dev/null; then
    print_warning "GoPhish is already running!"
    echo ""
    read -p "Kill existing process and restart? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pkill -x "gophish"
        sleep 2
        print_success "Stopped existing GoPhish process"
    else
        print_info "Keeping existing GoPhish process"
        SKIP_GOPHISH=1
    fi
fi

# Start GoPhish in background if not skipped
if [ -z "$SKIP_GOPHISH" ]; then
    print_info "Starting GoPhish server..."
    cd gophish

    # Start GoPhish in background and capture output
    ./gophish > ../logs/gophish.log 2>&1 &
    GOPHISH_PID=$!

    cd ..

    # Give it a moment to start
    sleep 3

    # Check if it's running
    if ps -p $GOPHISH_PID > /dev/null; then
        print_success "GoPhish started (PID: $GOPHISH_PID)"

        # Extract password from log
        if [ -f "logs/gophish.log" ]; then
            PASSWORD=$(grep -oP 'password \K[a-f0-9]+' logs/gophish.log | tail -1)
            if [ ! -z "$PASSWORD" ]; then
                echo ""
                print_header "IMPORTANT - Save These Credentials"
                echo -e "${YELLOW}Admin URL:${NC} https://127.0.0.1:3333"
                echo -e "${YELLOW}Username:${NC}  admin"
                echo -e "${YELLOW}Password:${NC}  ${GREEN}${PASSWORD}${NC}"
                echo ""
                echo -e "${RED}⚠ SAVE THIS PASSWORD NOW!${NC}"
                echo ""

                # Save credentials to file
                cat > .gophish_credentials << EOF
GoPhish Admin Credentials
=========================
URL:      https://127.0.0.1:3333
Username: admin
Password: ${PASSWORD}

Generated: $(date)

Next Steps:
1. Login to GoPhish admin panel
2. Change your password (you'll be prompted)
3. Go to Settings > Account Settings
4. Generate API key
5. Update automation/config/api_config.yaml with your API key
EOF
                print_success "Credentials saved to .gophish_credentials"
            fi
        fi
    else
        print_error "Failed to start GoPhish. Check logs/gophish.log for details"
        exit 1
    fi
else
    # Check if there's a saved password
    if [ -f ".gophish_credentials" ]; then
        print_info "Using existing GoPhish instance"
        echo ""
        cat .gophish_credentials
        echo ""
    fi
fi

echo ""
print_header "Next Steps"

echo "1. Configure API Key:"
echo "   ${YELLOW}a)${NC} Login to GoPhish: https://127.0.0.1:3333"
echo "   ${YELLOW}b)${NC} Go to Settings > Account Settings"
echo "   ${YELLOW}c)${NC} Click 'Reset API Key' and copy it"
echo "   ${YELLOW}d)${NC} Run: ${GREEN}./update_api_key.sh YOUR_API_KEY${NC}"
echo ""

echo "2. Start Dashboard:"
echo "   ${GREEN}./run_dashboard.sh${NC}"
echo ""

echo "3. Access Dashboard:"
echo "   http://localhost:5000"
echo ""

echo "4. View Logs:"
echo "   ${GREEN}tail -f logs/gophish.log${NC}        # GoPhish logs"
echo "   ${GREEN}tail -f logs/dashboard.log${NC}      # Dashboard logs"
echo ""

print_header "Platform Status"
echo "GoPhish Server:    ${GREEN}Running${NC} (https://127.0.0.1:3333)"
echo "Phishing Server:   ${GREEN}Running${NC} (http://localhost:8080)"
echo "Dashboard:         ${YELLOW}Not Started${NC} (run ./run_dashboard.sh)"
echo ""

print_success "Quick start complete!"
echo ""
