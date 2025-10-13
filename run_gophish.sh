#!/bin/bash

# Phishing Platform - GoPhish Launcher
# This script starts the GoPhish server

echo "=================================================="
echo "Phishing Platform - GoPhish Server"
echo "=================================================="
echo ""

# Check if gophish binary exists
if [ ! -f "gophish/gophish" ]; then
    echo "❌ Error: GoPhish binary not found!"
    echo "Expected location: gophish/gophish"
    exit 1
fi

# Check if already running
if pgrep -x "gophish" > /dev/null; then
    echo "⚠️  GoPhish is already running!"
    echo ""
    read -p "Kill existing process and restart? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pkill -x "gophish"
        sleep 2
    else
        exit 0
    fi
fi

# Start GoPhish
echo "Starting GoPhish server..."
echo ""
echo "🔒 IMPORTANT: Save the admin password shown below!"
echo "=================================================="
echo ""

cd gophish && ./gophish
