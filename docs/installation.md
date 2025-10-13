# Installation Guide

This guide will walk you through setting up the Phishing Attack Simulation and Training Platform from scratch.

## System Requirements

- **Operating System**: Linux (Ubuntu 20.04+ recommended)
- **RAM**: Minimum 8GB
- **Disk Space**: 5GB free space
- **Python**: 3.10 or higher
- **SMTP Server**: Access to Gmail, SendGrid, or custom mail server
- **Ports**: 80, 3333, 5000 (configurable)

## Step 1: Download and Extract Project

If you received this as a ZIP file:

```bash
cd ~/Desktop/Projects/P
ls phishing-platform/
```

The directory structure should look like this:

```
phishing-platform/
├── gophish/
├── automation/
├── dashboard/
├── templates/
├── config/
├── docs/
└── requirements.txt
```

## Step 2: Install Python Dependencies

Create a virtual environment and install required packages:

```bash
cd phishing-platform

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Verify installation:**

```bash
python -c "import flask; import pandas; import yaml; print('✓ All dependencies installed')"
```

## Step 3: Configure Environment Variables

Create your environment configuration file:

```bash
cp .env.example .env
nano .env
```

Fill in your actual credentials:

```env
# GoPhish API Configuration
GOPHISH_API_KEY=your_api_key_here
GOPHISH_API_URL=https://127.0.0.1:3333

# SMTP Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-specific-password
SMTP_FROM_ADDRESS=noreply@yourdomain.com
SMTP_FROM_NAME=IT Security Team

# Dashboard Configuration
DASHBOARD_HOST=0.0.0.0
DASHBOARD_PORT=5000
FLASK_SECRET_KEY=change-this-to-random-secret-key
```

**Note**: For Gmail, you need to create an [App Password](https://support.google.com/accounts/answer/185833):
1. Enable 2-Factor Authentication
2. Go to Security → App Passwords
3. Generate a password for "Mail"
4. Use that password in your .env file

## Step 4: Configure GoPhish

### 4.1 Review GoPhish Configuration

Check the GoPhish configuration:

```bash
cat gophish/config.json
```

Default configuration:

```json
{
    "admin_server": {
        "listen_url": "127.0.0.1:3333",
        "use_tls": true
    },
    "phish_server": {
        "listen_url": "0.0.0.0:80",
        "use_tls": false
    }
}
```

**Port 80 Access**: The phishing server needs port 80. If you can't use port 80:

```bash
# Option 1: Change to port 8080
nano gophish/config.json
# Change "0.0.0.0:80" to "0.0.0.0:8080"

# Option 2: Use iptables redirect (requires sudo)
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080
```

### 4.2 Start GoPhish

```bash
cd gophish
./gophish
```

**Expected Output:**

```
2025/10/13 10:00:00 Please login with the username admin and the password XXXXXXXX
2025/10/13 10:00:00 Starting admin server at https://127.0.0.1:3333
2025/10/13 10:00:00 Starting phishing server at http://0.0.0.0:80
```

**Important**: Save the password shown in the output!

### 4.3 First Login to GoPhish

1. Open browser and navigate to: `https://127.0.0.1:3333`
2. Accept the self-signed certificate warning
3. Login with:
   - Username: `admin`
   - Password: (from terminal output)
4. **Change your password immediately**

### 4.4 Generate API Key

1. In GoPhish dashboard, click on **Settings** (gear icon)
2. Go to **Account Settings**
3. Under **API Key**, click **Reset** to generate a new key
4. **Copy the API key**
5. Update your `.env` file with this key:

```bash
nano ../.env
# Update: GOPHISH_API_KEY=your_new_api_key_here
```

## Step 5: Configure SMTP in GoPhish

Configure email sending profile in GoPhish:

1. Go to **Sending Profiles**
2. Click **New Profile**
3. Enter details:
   - **Name**: `Production SMTP`
   - **From**: `noreply@yourdomain.com`
   - **Host**: `smtp.gmail.com:587` (or your SMTP server)
   - **Username**: Your email address
   - **Password**: Your app-specific password
4. Check **Ignore Certificate Errors** (if using self-signed certs)
5. Click **Send Test Email** to verify
6. Enter your email to receive test
7. If successful, click **Save Profile**

## Step 6: Configure API Settings

Update the API configuration file:

```bash
nano config/api_config.yaml
```

Update the API key:

```yaml
gophish:
  api_url: "https://127.0.0.1:3333"
  api_key: "YOUR_GOPHISH_API_KEY_HERE"  # Paste your API key
  verify_ssl: false
```

## Step 7: Test API Connection

Verify the API connection works:

```bash
cd automation
python campaign_manager.py --list
```

**Expected Output:**

```
Found 0 campaigns:
```

If you see an error, check:
- GoPhish is running
- API key is correct in `config/api_config.yaml`
- Server URL is correct

## Step 8: Start Analytics Dashboard

In a new terminal:

```bash
cd phishing-platform
source venv/bin/activate
cd dashboard
python app.py
```

**Expected Output:**

```
============================================================
Phishing Platform Analytics Dashboard
============================================================
Starting server at http://0.0.0.0:5000
Press Ctrl+C to stop
============================================================
```

Access dashboard at: `http://localhost:5000`

## Step 9: Verification Checklist

Verify everything is working:

- [ ] GoPhish admin panel accessible at https://127.0.0.1:3333
- [ ] GoPhish API key generated and configured
- [ ] SMTP test email sent successfully
- [ ] Python automation scripts can list campaigns
- [ ] Analytics dashboard accessible at http://localhost:5000
- [ ] No errors in any terminal windows

## Troubleshooting

### GoPhish won't start

**Error**: `bind: address already in use`

```bash
# Check what's using port 3333
sudo netstat -tulpn | grep 3333

# Kill the process or change GoPhish port in config.json
```

### Port 80 Permission Denied

**Error**: `bind: permission denied` on port 80

```bash
# Option 1: Run with sudo (not recommended)
sudo ./gophish

# Option 2: Use higher port and redirect
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080

# Then edit config.json to use port 8080
```

### SMTP Authentication Failed

**Error**: `535 Authentication failed`

For Gmail:
1. Verify 2FA is enabled
2. Use App Password, not regular password
3. Check "Less secure apps" is disabled
4. Try generating a new App Password

For other providers:
1. Verify SMTP host and port
2. Check credentials are correct
3. Ensure firewall allows outbound SMTP

### API Connection Failed

**Error**: `API request failed: Connection refused`

```bash
# Verify GoPhish is running
ps aux | grep gophish

# Check API key is correct
cat config/api_config.yaml | grep api_key

# Test API manually
curl -k -H "Authorization: Bearer YOUR_API_KEY" https://127.0.0.1:3333/api/campaigns/
```

### Import Errors

**Error**: `ModuleNotFoundError: No module named 'flask'`

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

## Next Steps

Once installation is complete:

1. Read the [User Manual](user_manual.md) to learn how to use the platform
2. Follow [Quick Start Guide](user_manual.md#quick-start) to run your first campaign
3. Review [API Documentation](api_documentation.md) for advanced usage

## Security Recommendations

Before using in production:

1. **Change all default passwords**
2. **Use strong API keys** (regenerate if exposed)
3. **Enable HTTPS** for the analytics dashboard
4. **Restrict network access** to admin interfaces
5. **Use firewall rules** to limit access
6. **Regularly backup** the GoPhish database
7. **Enable audit logging**

## Getting Help

If you encounter issues not covered here:

1. Check the [Troubleshooting Guide](troubleshooting.md)
2. Review GoPhish documentation: https://docs.getgophish.com
3. Check system logs: `tail -f gophish/gophish.log`
