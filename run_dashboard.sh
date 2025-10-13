#!/bin/bash

# Phishing Platform - Dashboard Launcher
# This script starts the analytics dashboard

echo "=================================================="
echo "Phishing Platform - Analytics Dashboard"
echo "=================================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Error: Virtual environment not found!"
    echo "Please run: python3 -m venv venv"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if GoPhish is running
if ! pgrep -x "gophish" > /dev/null; then
    echo "⚠️  Warning: GoPhish doesn't appear to be running"
    echo "Please start GoPhish first with: cd gophish && ./gophish"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Start dashboard
echo "Starting analytics dashboard..."
echo ""
cd dashboard && python app.py
