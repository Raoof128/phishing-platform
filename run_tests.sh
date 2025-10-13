#!/bin/bash

# Phishing Platform - Test Runner
# Automatically activates virtual environment and runs comprehensive tests

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo ""
echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}  Phishing Platform - Test Suite${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo -e "${RED}✗ Virtual environment not found!${NC}"
    echo "Please run: ./setup.sh"
    exit 1
fi

# Activate virtual environment
echo -e "${BLUE}▶ Activating virtual environment...${NC}"
source venv/bin/activate

# Run comprehensive tests
echo -e "${BLUE}▶ Running comprehensive tests...${NC}"
echo ""
python3 comprehensive_test.py

# Store exit code
TEST_EXIT_CODE=$?

# Deactivate venv
deactivate

echo ""
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✓ All tests completed successfully!${NC}"
else
    echo -e "${RED}✗ Some tests failed. Please review the output above.${NC}"
fi

echo ""
exit $TEST_EXIT_CODE
