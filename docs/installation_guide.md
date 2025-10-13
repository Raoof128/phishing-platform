# Installation Guide - Phishing Attack Simulation Platform

This guide provides step-by-step instructions for installing and configuring the Phishing Attack Simulation and Training Platform.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [GoPhish Installation](#gophish-installation)
3. [SMTP Configuration](#smtp-configuration)
4. [Python Environment Setup](#python-environment-setup)
5. [API Configuration](#api-configuration)
6. [Initial Testing](#initial-testing)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements
- **Operating System**: Linux (Ubuntu 20.04+, Debian 11+, or similar)
- **RAM**: 8GB minimum, 16GB recommended
- **Disk Space**: 10GB available
- **Network**: Internet connection for email sending
- **Permissions**: sudo access for installation

### Required Software
- **Python**: 3.10 or higher
- **pip**: Python package manager
- **wget/curl**: For downloading GoPhish
- **unzip**: For extracting archives

Check your Python version:
```bash
python3 --version
```

If Python 3.10+ is not installed:
```bash
sudo apt update
sudo apt install python3.10 python3-pip python3-venv
```

---

## GoPhish Installation

### Step 1: Download GoPhish

Navigate to the project directory and download GoPhish:

```bash
cd phishing-platform/gophish

# Download latest release (v0.12.1)
wget https://github.com/gophish/gophish/releases/download/v0.12.1/gophish-v0.12.1-linux-64bit.zip

# Extract archive
unzip gophish-v0.12.1-linux-64bit.zip

# Make executable
chmod +x gophish

# Verify installation
./gophish --help
```

### Step 2: Initial Configuration

Edit the GoPhish configuration file:

```bash
nano config.json
```

Key configuration options:

```json
{
  "admin_server": {
    "listen_url": "0.0.0.0:3333",
    "use_tls": true,
    "cert_path": "gophish_admin.crt",
    "key_path": "gophish_admin.key"
  },
  "phish_server": {
    "listen_url": "0.0.0.0:80",
    "use_tls": false
  },
  "db_name": "sqlite3",
  "db_path": "gophish.db",
  "migrations_prefix": "db/db_"
}
```

**Important Settings:**
- `admin_server.listen_url`: Admin dashboard address (default: localhost:3333)
- `phish_server.listen_url`: Landing page server (default: localhost:80)
- `db_path`: Database location

### Step 3: Run GoPhish

Start GoPhish for the first time:

```bash
./gophish
```

You should see output like:
```
time="2025-10-13T10:00:00+10:00" level=info msg="Admin server started at https://127.0.0.1:3333"
time="2025-10-13T10:00:00+10:00" level=info msg="Phishing server started at http://0.0.0.0:80"
time="2025-10-13T10:00:00+10:00" level=info msg="Please login with the username admin and the password: [GENERATED_PASSWORD]"
```

**Save the generated password!**

### Step 4: Access Admin Dashboard

1. Open browser and navigate to: `https://127.0.0.1:3333`
2. Accept the self-signed certificate warning
3. Login with:
   - Username: `admin`
   - Password: (from console output above)
4. **Immediately change the password** via Settings > Account Settings

### Step 5: Run as Background Service (Optional)

Create a systemd service for automatic startup:

```bash
sudo nano /etc/systemd/system/gophish.service
```

Add the following:

```ini
[Unit]
Description=GoPhish Phishing Framework
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/home/your-username/phishing-platform/gophish
ExecStart=/home/your-username/phishing-platform/gophish/gophish
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable gophish
sudo systemctl start gophish
sudo systemctl status gophish
```

---

## SMTP Configuration

### Option 1: Gmail SMTP

1. **Enable 2-Factor Authentication** on your Google account
2. **Generate App-Specific Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (custom name)"
   - Name it "GoPhish" and click "Generate"
   - Save the 16-character password

3. **Configure in GoPhish**:
   - Navigate to "Sending Profiles" in GoPhish dashboard
   - Click "New Profile"
   - Fill in:
     - **Name**: Gmail SMTP
     - **From**: your-email@gmail.com
     - **Host**: smtp.gmail.com:587
     - **Username**: your-email@gmail.com
     - **Password**: (app-specific password from step 2)
   - Click "Send Test Email" to verify
   - Click "Save Profile"

### Option 2: SendGrid

1. **Create SendGrid Account**: https://signup.sendgrid.com/
2. **Generate API Key**:
   - Go to Settings > API Keys
   - Click "Create API Key"
   - Name it "GoPhish" with "Full Access"
   - Save the API key

3. **Configure in GoPhish**:
   - **Name**: SendGrid
   - **From**: verified-sender@yourdomain.com
   - **Host**: smtp.sendgrid.net:587
   - **Username**: apikey
   - **Password**: (API key from step 2)

### Option 3: Custom SMTP Server

If you have your own mail server:

- **Host**: mail.yourdomain.com:587 (or 25, 465)
- **Username**: your SMTP username
- **Password**: your SMTP password
- **From**: phishing@yourdomain.com

### Testing SMTP Configuration

Send a test email from GoPhish:
1. Go to "Sending Profiles"
2. Click on your profile
3. Click "Send Test Email"
4. Enter your personal email address
5. Verify email arrives in inbox (check spam folder)

---

## Python Environment Setup

### Step 1: Create Virtual Environment

```bash
cd phishing-platform

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Verify activation (should show venv path)
which python
```

### Step 2: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install required packages
pip install -r requirements.txt

# Verify installations
pip list
```

### Step 3: Verify Installations

Test key packages:

```bash
python3 << 'PYEOF'
import flask
import pandas
import plotly
import yaml
print("All packages imported successfully!")
PYEOF
```

---

## API Configuration

### Step 1: Generate GoPhish API Key

1. Login to GoPhish admin dashboard
2. Navigate to: **Settings** > **API Keys**
3. Click "Generate New API Key"
4. Copy the generated key (it won't be shown again!)

### Step 2: Update Configuration File

Edit the API configuration:

```bash
nano automation/config/api_config.yaml
```

Replace `your-api-key-here` with your actual API key:

```yaml
gophish:
  server_url: https://127.0.0.1:3333
  api_key: YOUR_ACTUAL_API_KEY_HERE
  verify_ssl: false
  timeout: 30
```

### Step 3: Test API Connection

```bash
cd automation
python3 << 'PYEOF'
import yaml
import requests

# Load config
with open('config/api_config.yaml') as f:
    config = yaml.safe_load(f)

# Test connection
api_key = config['gophish']['api_key']
server_url = config['gophish']['server_url']
headers = {'Authorization': f'Bearer {api_key}'}

response = requests.get(
    f'{server_url}/api/campaigns/',
    headers=headers,
    verify=False
)

if response.status_code == 200:
    print("✓ API connection successful!")
    print(f"  Campaigns found: {len(response.json())}")
else:
    print(f"✗ API connection failed: {response.status_code}")
    print(f"  Error: {response.text}")
PYEOF
```

---

## Initial Testing

### Test 1: Send Test Email

```bash
cd automation
python3 << 'PYEOF'
import requests
import yaml
from datetime import datetime, timedelta

# Load config
with open('config/api_config.yaml') as f:
    config = yaml.safe_load(f)

api_key = config['gophish']['api_key']
server_url = config['gophish']['server_url']
headers = {'Authorization': f'Bearer {api_key}'}

# Get SMTP profiles
response = requests.get(
    f'{server_url}/api/smtp/',
    headers=headers,
    verify=False
)

if response.status_code == 200:
    profiles = response.json()
    if profiles:
        print(f"✓ Found {len(profiles)} SMTP profile(s)")
        for profile in profiles:
            print(f"  - {profile['name']}")
    else:
        print("✗ No SMTP profiles configured")
        print("  Please configure SMTP in GoPhish dashboard")
else:
    print(f"✗ Failed to retrieve SMTP profiles: {response.status_code}")
PYEOF
```

### Test 2: Create Test Campaign

You can create a simple test campaign through the GoPhish dashboard:

1. Create a test user group with your personal email
2. Use a simple email template
3. Use a basic landing page
4. Schedule for immediate delivery
5. Monitor the campaign and check your email

---

## Troubleshooting

### Issue: Cannot access GoPhish dashboard

**Solution**:
```bash
# Check if GoPhish is running
ps aux | grep gophish

# Check if port 3333 is in use
sudo netstat -tulpn | grep 3333

# Restart GoPhish
cd gophish
./gophish
```

### Issue: SMTP authentication failed

**Solutions**:
- **Gmail**: Ensure 2FA is enabled and using app-specific password (not account password)
- **SendGrid**: Verify API key has full access permissions
- **Custom**: Check firewall allows outbound connections on SMTP port

### Issue: SSL certificate errors

**Solution**:
```bash
# For GoPhish admin dashboard
# Accept self-signed certificate in browser

# For Python scripts
# Already configured with verify_ssl: false in api_config.yaml
```

### Issue: Python package installation fails

**Solution**:
```bash
# Update pip and setuptools
pip install --upgrade pip setuptools wheel

# Install packages one at a time to identify issues
pip install flask
pip install pandas
# etc.

# For specific package issues, check Python version compatibility
python3 --version
```

### Issue: Permission denied on port 80

**Solution**:
```bash
# Option 1: Run GoPhish with sudo (not recommended)
sudo ./gophish

# Option 2: Use a higher port (8080) and configure reverse proxy
# Edit config.json:
{
  "phish_server": {
    "listen_url": "0.0.0.0:8080"
  }
}
```

### Issue: Database locked

**Solution**:
```bash
# Stop all GoPhish processes
pkill gophish

# Check for lock files
ls -la gophish/gophish.db*

# Remove lock if exists
rm gophish/gophish.db-wal gophish/gophish.db-shm

# Restart GoPhish
cd gophish && ./gophish
```

---

## Next Steps

After successful installation:

1. **Create Email Templates**: See Phase 2 documentation
2. **Build Landing Pages**: See Phase 3 documentation
3. **Set Up Automation**: See Phase 4 documentation
4. **Launch Dashboard**: See Phase 5 documentation

---

## Security Reminders

- Keep GoPhish admin password secure
- Store API keys in environment variables (not in code)
- Restrict access to GoPhish dashboard (firewall rules)
- Regularly backup the GoPhish database
- Use HTTPS for production deployments
- Never commit sensitive credentials to version control

---

## Support

For issues not covered in this guide, refer to:
- [GoPhish Documentation](https://docs.getgophish.com/)
- [Troubleshooting Guide](troubleshooting.md)
- Project GitHub issues

---

**Installation Complete!** You're now ready to begin creating phishing campaigns.
