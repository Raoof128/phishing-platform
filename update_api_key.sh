#!/bin/bash

# Script to update GoPhish API key in configuration

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

if [ -z "$1" ]; then
    echo -e "${RED}Error: API key required${NC}"
    echo ""
    echo "Usage: $0 YOUR_API_KEY"
    echo ""
    echo "Steps to get your API key:"
    echo "  1. Login to GoPhish: https://127.0.0.1:3333"
    echo "  2. Go to Settings > Account Settings"
    echo "  3. Click 'Reset API Key'"
    echo "  4. Copy the generated key"
    echo "  5. Run: $0 YOUR_COPIED_KEY"
    exit 1
fi

API_KEY="$1"
CONFIG_FILE="automation/config/api_config.yaml"

if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${RED}Error: Config file not found: $CONFIG_FILE${NC}"
    exit 1
fi

# Backup original
cp "$CONFIG_FILE" "$CONFIG_FILE.backup"
echo -e "${GREEN}✓${NC} Backed up config to $CONFIG_FILE.backup"

# Update API key using sed
sed -i "s/api_key: .*/api_key: $API_KEY/" "$CONFIG_FILE"

# Verify update
if grep -q "$API_KEY" "$CONFIG_FILE"; then
    echo -e "${GREEN}✓${NC} API key updated successfully in $CONFIG_FILE"
    echo ""
    echo "Testing API connection..."

    # Test connection using Python
    python3 << EOF
import sys
sys.path.insert(0, '.')
try:
    from automation.campaign_manager import GophishCampaign

    manager = GophishCampaign(config_path='$CONFIG_FILE')
    if manager.test_connection():
        print("${GREEN}✓${NC} API connection successful!")
        print("")
        print("You can now:")
        print("  - Start the dashboard: ./run_dashboard.sh")
        print("  - List campaigns: python3 -m automation.campaign_manager --list-campaigns")
        print("  - List resources: python3 -m automation.campaign_manager --list-resources")
        sys.exit(0)
    else:
        print("${RED}✗${NC} API connection failed")
        print("Please check:")
        print("  1. GoPhish is running (./run_gophish.sh)")
        print("  2. API key is correct")
        sys.exit(1)
except Exception as e:
    print(f"${RED}✗${NC} Error: {e}")
    sys.exit(1)
EOF

else
    echo -e "${RED}✗${NC} Failed to update API key"
    echo "Restoring backup..."
    mv "$CONFIG_FILE.backup" "$CONFIG_FILE"
    exit 1
fi
