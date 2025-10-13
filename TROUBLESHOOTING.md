# Troubleshooting Guide

Common issues and solutions for the Phishing Platform.

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [GoPhish Problems](#gophish-problems)
3. [Python Errors](#python-errors)
4. [SMTP Issues](#smtp-issues)
5. [Dashboard Problems](#dashboard-problems)
6. [Campaign Issues](#campaign-issues)
7. [Database Errors](#database-errors)
8. [Network Issues](#network-issues)

---

## Installation Issues

### Virtual Environment Creation Fails

**Problem:** `python3 -m venv venv` fails

**Solutions:**
```bash
# Install venv package
sudo apt-get install python3-venv

# Or use virtualenv
pip3 install virtualenv
virtualenv venv
```

### Pip Install Fails

**Problem:** Dependencies won't install

**Solutions:**
```bash
# Upgrade pip
pip install --upgrade pip

# Install with verbose output to see errors
pip install -r requirements.txt -v

# Install individually to identify problem package
pip install flask requests pandas pyyaml
```

### Permission Denied

**Problem:** Cannot execute scripts

**Solution:**
```bash
# Make all scripts executable
chmod +x *.sh *.py automation/*.py
```

---

## GoPhish Problems

### Port 3333 Already in Use

**Problem:** GoPhish won't start - port in use

**Solutions:**
```bash
# Find what's using the port
sudo netstat -tulpn | grep 3333

# Kill the process
sudo kill -9 <PID>

# Or change GoPhish port in config.json
nano gophish/config.json
# Change listen_url to "127.0.0.1:3334"
```

### Port 80 Permission Denied

**Problem:** Cannot bind to port 80

**Solutions:**

**Option 1: Use sudo (not recommended)**
```bash
sudo ./gophish
```

**Option 2: Use port forwarding**
```bash
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080

# Update config.json to use port 8080
nano gophish/config.json
```

**Option 3: Use higher port**
```bash
# Edit config.json
nano gophish/config.json
# Change phish_server listen_url to "0.0.0.0:8080"
```

### GoPhish Database Locked

**Problem:** Database is locked error

**Solutions:**
```bash
# Stop all GoPhish processes
pkill -9 gophish

# Remove lock file
rm gophish/gophish.db-journal

# Restart GoPhish
./run_gophish.sh
```

### Cannot Access Admin Panel

**Problem:** https://127.0.0.1:3333 not loading

**Solutions:**
```bash
# Check if GoPhish is running
ps aux | grep gophish

# Check logs
tail -f gophish/gophish.log

# Try with http instead of https
http://127.0.0.1:3333

# Check firewall
sudo ufw status
sudo ufw allow 3333
```

---

## Python Errors

### Module Not Found

**Problem:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Verify you're in venv
which python  # Should show path to venv

# Reinstall dependencies
pip install -r requirements.txt
```

### Import Error in Scripts

**Problem:** Cannot import automation modules

**Solution:**
```bash
# Add project root to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or run from project root
cd /path/to/phishing-platform
python automation/campaign_manager.py --list
```

### YAML Parse Error

**Problem:** `yaml.scanner.ScannerError`

**Solution:**
```bash
# Validate YAML syntax
python3 -c "import yaml; yaml.safe_load(open('config/api_config.yaml'))"

# Common issues:
# - Tabs instead of spaces (use spaces only)
# - Incorrect indentation
# - Missing quotes around special characters
```

---

## SMTP Issues

### Authentication Failed (Gmail)

**Problem:** `535-5.7.8 Username and Password not accepted`

**Solutions:**

1. **Enable 2-Factor Authentication** on Google account
2. **Create App Password**:
   - Visit https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other"
   - Copy the 16-character password
   - Use this in smtp_config.yaml (not your regular password)

3. **Check settings**:
   ```yaml
   smtp:
     host: "smtp.gmail.com"
     port: 587
     username: "your-email@gmail.com"
     password: "app-specific-password-here"
   ```

### Connection Timeout

**Problem:** SMTP connection times out

**Solutions:**
```bash
# Test SMTP connection manually
telnet smtp.gmail.com 587

# Check firewall allows outbound SMTP
sudo ufw status
sudo ufw allow out 587

# Try alternative port
# Port 587 (TLS) or 465 (SSL)
```

### Emails Going to Spam

**Problem:** Phishing emails end up in spam

**Solutions:**

1. **Use authenticated SMTP** (not spoofed addresses)
2. **Start small** - send to few recipients first
3. **Reduce sending rate** in GoPhish
4. **Warm up** the email account (send normal emails first)
5. **Check SPF/DKIM** if using custom domain
6. **Test with different email providers**

---

## Dashboard Problems

### Dashboard Won't Start

**Problem:** Flask app fails to start

**Solutions:**
```bash
# Check if port 5000 is available
netstat -tulpn | grep 5000

# Use different port
export FLASK_RUN_PORT=5001
python dashboard/app.py

# Check logs
python dashboard/app.py 2>&1 | tee dashboard.log
```

### API Connection Failed

**Problem:** Dashboard can't connect to GoPhish

**Solutions:**
```bash
# Verify GoPhish is running
curl -k https://127.0.0.1:3333/api/campaigns/

# Check API key
cat config/api_config.yaml | grep api_key

# Test API manually
curl -k -H "Authorization: Bearer YOUR_API_KEY" \
  https://127.0.0.1:3333/api/campaigns/
```

### Charts Not Loading

**Problem:** Dashboard loads but charts are empty

**Solutions:**

1. **Check browser console** (F12) for JavaScript errors
2. **Verify data** is returning from API endpoints
3. **Clear browser cache** and reload
4. **Check Chart.js** is loading:
   ```javascript
   // In browser console
   typeof Chart
   // Should return "function"
   ```

---

## Campaign Issues

### Campaign Not Sending

**Problem:** Campaign created but emails not sending

**Solutions:**

1. **Check campaign status** in GoPhish dashboard
2. **Verify launch date** is not in the future
3. **Check SMTP profile** is configured correctly
4. **Test SMTP** with "Send Test Email"
5. **Review GoPhish logs**:
   ```bash
   tail -f gophish/gophish.log
   ```

### Template Not Found

**Problem:** Cannot create campaign - template/page not found

**Solution:**
```bash
# Templates must be created in GoPhish first
# CLI cannot create templates, only campaigns

# Steps:
# 1. Open GoPhish web interface
# 2. Create Email Template
# 3. Create Landing Page
# 4. Then use campaign_manager.py
```

### Users Not Receiving Emails

**Problem:** Campaign sent but users didn't get emails

**Solutions:**

1. **Check spam folders**
2. **Verify email addresses** are correct
3. **Check SMTP logs** in GoPhish
4. **Reduce sending rate** (may be rate limited)
5. **Check email server blacklisting**:
   ```bash
   # Check if IP is blacklisted
   # Visit: https://mxtoolbox.com/blacklists.aspx
   ```

---

## Database Errors

### SQLite Database Locked

**Problem:** `database is locked` error

**Solutions:**
```bash
# Close all connections
pkill -9 gophish
pkill -9 python

# Wait a moment, then restart
./run_gophish.sh
./run_dashboard.sh
```

### Database Corrupted

**Problem:** Database file is corrupted

**Solutions:**
```bash
# Backup current database
cp gophish/gophish.db gophish/gophish.db.backup

# Try to repair
sqlite3 gophish/gophish.db "PRAGMA integrity_check;"

# If repair fails, restore from backup or start fresh
# WARNING: This deletes all campaign data
rm gophish/gophish.db
# GoPhish will create new database on next start
```

### Cannot Access Analytics Data

**Problem:** Analytics script can't read database

**Solutions:**
```bash
# Check database exists
ls -la gophish/gophish.db

# Check permissions
chmod 644 gophish/gophish.db

# Verify database path in scripts
python automation/analytics.py --db gophish/gophish.db --all-risks
```

---

## Network Issues

### Cannot Connect to GoPhish from Other Machines

**Problem:** GoPhish only accessible from localhost

**Solution:**
```bash
# Edit config.json to bind to all interfaces
nano gophish/config.json

# Change:
"listen_url": "127.0.0.1:3333"
# To:
"listen_url": "0.0.0.0:3333"

# Warning: Use with caution, consider firewall rules
sudo ufw allow from 192.168.1.0/24 to any port 3333
```

### SSL Certificate Errors

**Problem:** SSL verification failed

**Solution:**
```python
# In Python scripts, SSL verification is disabled by default
# for GoPhish's self-signed certificate

# If you have proper SSL certs:
verify_ssl=True  # in campaign_manager.py
```

---

## Common Error Messages

### "Error loading config"

**Cause:** Configuration file not found or invalid

**Fix:**
```bash
# Check file exists
ls config/api_config.yaml

# Validate YAML
python3 -c "import yaml; yaml.safe_load(open('config/api_config.yaml'))"

# Regenerate from example
cp config/api_config.yaml.example config/api_config.yaml
```

### "API request failed: Connection refused"

**Cause:** GoPhish not running

**Fix:**
```bash
# Start GoPhish
./run_gophish.sh

# Or check if it's already running on different port
netstat -tulpn | grep gophish
```

### "Permission denied: gophish"

**Cause:** Binary not executable

**Fix:**
```bash
chmod +x gophish/gophish
```

---

## Getting Additional Help

### Diagnostic Information

When seeking help, provide:

```bash
# System information
uname -a
python3 --version

# Package versions
pip list | grep -E 'flask|requests|pandas|yaml'

# GoPhish version
cat gophish/VERSION

# Recent logs
tail -100 gophish/gophish.log

# Check running processes
ps aux | grep -E 'gophish|python'
```

### Log Files

Important logs to check:

- `gophish/gophish.log` - GoPhish server logs
- `logs/audit.log` - Platform audit logs (if enabled)
- Dashboard console output
- Browser developer console (F12)

### Testing Commands

```bash
# Test GoPhish API
curl -k https://127.0.0.1:3333/api/campaigns/

# Test Python imports
python3 -c "from automation import campaign_manager"

# Test database
sqlite3 gophish/gophish.db ".tables"

# Test SMTP
python3 -c "import smtplib; smtplib.SMTP('smtp.gmail.com', 587).quit()"
```

---

## Prevention Tips

### Before Starting Campaigns

- [ ] Test with your own email first
- [ ] Verify SMTP with test email
- [ ] Check all templates in GoPhish
- [ ] Confirm API key is correct
- [ ] Review campaign settings
- [ ] Start with small test group

### Regular Maintenance

- [ ] Backup gophish.db regularly
- [ ] Monitor disk space
- [ ] Check logs for errors
- [ ] Update dependencies
- [ ] Review security settings
- [ ] Clean old campaign data

### Best Practices

- [ ] Use version control for custom templates
- [ ] Document configuration changes
- [ ] Test in staging before production
- [ ] Keep credentials secure
- [ ] Monitor system resources
- [ ] Regular security audits

---

**Still having issues?**

1. Run the test suite: `python3 test_platform.py`
2. Verify installation: `python3 verify_installation.py`
3. Review documentation: `docs/installation.md`
4. Check GoPhish docs: https://docs.getgophish.com
