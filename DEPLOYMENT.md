# 🚀 Production Deployment Guide

**Phishing Awareness Training Platform**
**Version:** 1.0
**Last Updated:** October 14, 2025

---

## 📋 Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [System Requirements](#system-requirements)
3. [Production Setup](#production-setup)
4. [Security Hardening](#security-hardening)
5. [Configuration](#configuration)
6. [SSL/TLS Setup](#ssltls-setup)
7. [Backup and Recovery](#backup-and-recovery)
8. [Monitoring](#monitoring)
9. [Troubleshooting](#troubleshooting)

---

## ✅ Pre-Deployment Checklist

### Before Deploying to Production

- [ ] **System Requirements Met**
  - Python 3.10+ installed
  - Sufficient disk space (1GB minimum)
  - Network ports available (3333, 5000, 8080)
  - Firewall configured

- [ ] **Security Review**
  - All credentials changed from defaults
  - API keys generated and secured
  - SSL certificates obtained
  - File permissions reviewed
  - .gitignore configured properly

- [ ] **Testing Complete**
  - All 51 comprehensive tests passing
  - Manual functionality tests completed
  - Load testing performed
  - Backup/restore tested

- [ ] **Documentation Ready**
  - User manual available
  - API documentation current
  - Troubleshooting guide accessible
  - Contact information updated

---

## 🖥️ System Requirements

### Minimum Requirements

```
OS: Linux (Ubuntu 20.04+ recommended)
CPU: 2 cores
RAM: 4GB
Disk: 1GB free space
Python: 3.10 or higher
Network: Stable internet connection
```

### Recommended for Production

```
OS: Linux (Ubuntu 22.04 LTS)
CPU: 4+ cores
RAM: 8GB+
Disk: 10GB+ (for logs and data)
Python: 3.11
Network: Dedicated server with static IP
```

### Required Ports

| Port | Service | Access |
|------|---------|--------|
| 3333 | GoPhish Admin | Internal only (127.0.0.1) |
| 5000 | Analytics Dashboard | Internal network |
| 8080 | Phishing Landing Pages | Public (via reverse proxy) |

---

## 🚀 Production Setup

### 1. Clone Repository

```bash
# Clone the repository
git clone <your-repo-url> phishing-platform
cd phishing-platform

# Checkout stable version
git checkout main
```

### 2. Run Setup

```bash
# Make scripts executable
chmod +x *.sh

# Run setup script
./setup.sh
```

This will:
- Check Python version
- Create virtual environment
- Install dependencies
- Set up directory structure

### 3. Configure Production Settings

```bash
# Copy example configurations
cp config/api_config.yaml.example automation/config/api_config.yaml
cp config/smtp_config.yaml.example automation/config/smtp_config.yaml

# Edit with production values
nano automation/config/api_config.yaml
nano automation/config/smtp_config.yaml
```

### 4. Start Services

```bash
# Start GoPhish and Dashboard
./quickstart.sh

# Or start individually:
./run_gophish.sh     # Terminal 1
./run_dashboard.sh   # Terminal 2
```

### 5. Initial Configuration

```bash
# 1. Get GoPhish credentials
cat .gophish_credentials

# 2. Log into GoPhish Admin
# URL: https://127.0.0.1:3333
# Username: admin
# Password: (from .gophish_credentials)

# 3. Change default password immediately!

# 4. Get API key from GoPhish settings
# Settings > Users > API Key

# 5. Update configuration with API key
./update_api_key.sh YOUR_API_KEY_HERE
```

---

## 🔒 Security Hardening

### 1. Change Default Credentials

**Immediately after first login:**

```
1. Log into GoPhish (https://127.0.0.1:3333)
2. Go to Settings > Account Settings
3. Change password to strong passphrase
4. Generate new API key
5. Update configuration with new API key
```

### 2. File Permissions

```bash
# Secure configuration files
chmod 600 automation/config/api_config.yaml
chmod 600 automation/config/smtp_config.yaml
chmod 600 .gophish_credentials

# Secure database
chmod 600 gophish/gophish.db

# Secure private keys
chmod 600 gophish/*.key
```

### 3. Network Security

**Firewall Configuration (UFW example):**

```bash
# Allow SSH
sudo ufw allow 22/tcp

# Block external access to admin panel
sudo ufw deny 3333/tcp

# Allow dashboard on internal network only
sudo ufw allow from 192.168.0.0/16 to any port 5000

# Allow phishing server (via reverse proxy)
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable
```

### 4. Reverse Proxy Setup (Nginx)

**Install Nginx:**

```bash
sudo apt install nginx certbot python3-certbot-nginx
```

**Configure Nginx** (`/etc/nginx/sites-available/phishing-platform`):

```nginx
# Phishing landing pages (public)
server {
    listen 80;
    server_name your-phishing-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

# Analytics Dashboard (internal network only)
server {
    listen 5000;
    server_name your-dashboard-domain.local;

    # Restrict to internal IPs
    allow 192.168.0.0/16;
    allow 10.0.0.0/8;
    deny all;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Enable site:**

```bash
sudo ln -s /etc/nginx/sites-available/phishing-platform /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 5. SSL/TLS Certificates

**Option A: Let's Encrypt (Free)**

```bash
# Obtain certificate
sudo certbot --nginx -d your-phishing-domain.com

# Auto-renewal
sudo certbot renew --dry-run
```

**Option B: Self-Signed (Development/Internal)**

```bash
# Generate certificate
openssl req -x509 -newkey rsa:4096 -nodes \
    -keyout gophish/gophish.key \
    -out gophish/gophish.crt \
    -days 365 \
    -subj "/CN=your-domain.com"

# Update GoPhish config to use TLS
nano gophish/config.json
# Set use_tls: true
# Set cert_path and key_path
```

---

## ⚙️ Configuration

### API Configuration Template

**File:** `automation/config/api_config.yaml`

```yaml
gophish:
  api_key: "YOUR_PRODUCTION_API_KEY_HERE"
  server_url: "https://127.0.0.1:3333"
  verify_ssl: true  # Set to true in production with valid cert

logging:
  level: "INFO"  # Use INFO or WARNING in production
  file: "logs/automation.log"
  max_bytes: 10485760  # 10MB
  backup_count: 5
```

### SMTP Configuration Template

**File:** `automation/config/smtp_config.yaml`

```yaml
smtp_profiles:
  production_email:
    name: "Corporate Email"
    host: "smtp.your-domain.com"
    port: 587
    username: "phishing@your-domain.com"
    password: "USE_SECURE_PASSWORD_HERE"
    from_address: "security@your-domain.com"
    use_tls: true
    ignore_cert_errors: false
```

### Environment Variables (Optional)

Create `.env` file (excluded from git):

```bash
# GoPhish
GOPHISH_API_KEY=your_api_key_here
GOPHISH_URL=https://127.0.0.1:3333

# SMTP
SMTP_HOST=smtp.your-domain.com
SMTP_PORT=587
SMTP_USER=phishing@your-domain.com
SMTP_PASS=your_password_here

# Logging
LOG_LEVEL=INFO
```

---

## 🔐 SSL/TLS Setup

### GoPhish Admin Panel SSL

**Edit** `gophish/config.json`:

```json
{
  "admin_server": {
    "listen_url": "127.0.0.1:3333",
    "use_tls": true,
    "cert_path": "gophish_admin.crt",
    "key_path": "gophish_admin.key"
  }
}
```

**Generate self-signed certificate:**

```bash
cd gophish
openssl req -newkey rsa:2048 -nodes -keyout gophish_admin.key \
    -x509 -days 365 -out gophish_admin.crt
cd ..
```

### Phishing Server SSL

For production phishing campaigns, use valid SSL certificates via reverse proxy (Nginx/Apache) with Let's Encrypt.

---

## 💾 Backup and Recovery

### What to Backup

1. **GoPhish Database** - `gophish/gophish.db`
2. **Configuration Files** - `automation/config/*.yaml`
3. **Templates** - `templates/` directory
4. **Logs** - `logs/` directory (optional)

### Automated Backup Script

Create `backup.sh`:

```bash
#!/bin/bash

BACKUP_DIR="/backups/phishing-platform"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="phishing-platform-backup-${DATE}.tar.gz"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Create backup
tar -czf "$BACKUP_DIR/$BACKUP_FILE" \
    gophish/gophish.db \
    automation/config/ \
    templates/ \
    .gophish_credentials

echo "Backup created: $BACKUP_DIR/$BACKUP_FILE"

# Keep only last 7 backups
cd "$BACKUP_DIR"
ls -t | tail -n +8 | xargs -r rm

echo "Backup complete!"
```

**Schedule daily backups:**

```bash
# Add to crontab
crontab -e

# Add line (backup daily at 2 AM):
0 2 * * * /path/to/phishing-platform/backup.sh
```

### Recovery Procedure

```bash
# 1. Stop services
pkill gophish
pkill -f dashboard/app.py

# 2. Extract backup
tar -xzf phishing-platform-backup-YYYYMMDD_HHMMSS.tar.gz

# 3. Restore files
cp -r backup/gophish/gophish.db gophish/
cp -r backup/automation/config/* automation/config/

# 4. Restart services
./quickstart.sh
```

---

## 📊 Monitoring

### Log Files

| Log File | Purpose | Location |
|----------|---------|----------|
| GoPhish | Server operations | `logs/gophish.log` |
| Dashboard | Web app logs | `logs/dashboard.log` |
| Automation | Script execution | `logs/automation.log` |

### Health Check Script

Create `healthcheck.sh`:

```bash
#!/bin/bash

# Check GoPhish
if curl -k -s https://127.0.0.1:3333 > /dev/null; then
    echo "✓ GoPhish: Running"
else
    echo "✗ GoPhish: DOWN"
fi

# Check Dashboard
if curl -s http://localhost:5000 > /dev/null; then
    echo "✓ Dashboard: Running"
else
    echo "✗ Dashboard: DOWN"
fi

# Check database
if [ -f "gophish/gophish.db" ]; then
    echo "✓ Database: Present"
else
    echo "✗ Database: Missing"
fi

# Check disk space
DISK_USAGE=$(df -h . | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -lt 80 ]; then
    echo "✓ Disk Space: ${DISK_USAGE}% used"
else
    echo "⚠ Disk Space: ${DISK_USAGE}% used (WARNING)"
fi
```

**Run periodically:**

```bash
chmod +x healthcheck.sh
watch -n 60 ./healthcheck.sh
```

---

## 🐛 Troubleshooting

### GoPhish Won't Start

**Symptoms:** GoPhish exits immediately
**Solutions:**

1. Check port availability:
   ```bash
   sudo lsof -i :3333
   sudo lsof -i :8080
   ```

2. Check logs:
   ```bash
   cat logs/gophish.log
   ```

3. Verify configuration:
   ```bash
   cat gophish/config.json | python3 -m json.tool
   ```

### Dashboard Not Loading Data

**Symptoms:** Dashboard shows errors or no data
**Solutions:**

1. Verify API key:
   ```bash
   ./update_api_key.sh YOUR_API_KEY
   ```

2. Test connection:
   ```bash
   source venv/bin/activate
   python3 -c "from automation.campaign_manager import GophishCampaign; gc = GophishCampaign(); print(gc.test_connection())"
   ```

3. Check GoPhish is running:
   ```bash
   curl -k https://127.0.0.1:3333
   ```

### SSL Certificate Errors

**Symptoms:** SSL verification failures
**Solutions:**

1. For development, disable verification:
   ```yaml
   # In api_config.yaml
   gophish:
     verify_ssl: false
   ```

2. For production, use valid certificates:
   ```bash
   sudo certbot --nginx -d your-domain.com
   ```

### Permission Denied Errors

**Symptoms:** Can't bind to port 80/443
**Solutions:**

1. Use non-privileged ports (8080, 8443)
2. Use reverse proxy (Nginx) with sudo
3. Or grant capability:
   ```bash
   sudo setcap 'cap_net_bind_service=+ep' gophish/gophish
   ```

---

## 📚 Additional Resources

- **Quick Start Guide:** `QUICK_START_GUIDE.md`
- **User Manual:** `docs/user_manual.md`
- **API Documentation:** `docs/api_documentation.md`
- **Troubleshooting:** `TROUBLESHOOTING.md`

---

## 🆘 Support

### Before Contacting Support

1. Run comprehensive tests:
   ```bash
   ./run_tests.sh
   ```

2. Check logs:
   ```bash
   tail -f logs/gophish.log
   tail -f logs/dashboard.log
   ```

3. Verify configuration:
   ```bash
   python3 verify_installation.py
   ```

### Getting Help

1. Check documentation in `docs/` directory
2. Review `TROUBLESHOOTING.md`
3. Check GoPhish documentation: https://docs.getgophish.com/

---

## 🔄 Updating the Platform

### Safe Update Procedure

```bash
# 1. Backup current installation
./backup.sh

# 2. Stop services
pkill gophish
pkill -f dashboard/app.py

# 3. Pull latest changes
git pull origin main

# 4. Update dependencies
source venv/bin/activate
pip install -r requirements.txt --upgrade

# 5. Run tests
./run_tests.sh

# 6. Restart services
./quickstart.sh
```

---

## ✅ Production Checklist

### Initial Deployment

- [ ] System requirements met
- [ ] Setup completed successfully
- [ ] All tests passing (51/51)
- [ ] Default credentials changed
- [ ] API key generated and configured
- [ ] SSL certificates installed
- [ ] Firewall configured
- [ ] File permissions secured
- [ ] Backup script configured
- [ ] Monitoring enabled
- [ ] Documentation accessible

### Ongoing Operations

- [ ] Daily backups running
- [ ] Logs monitored regularly
- [ ] Disk space checked
- [ ] Health checks passing
- [ ] Certificates current (not expired)
- [ ] Updates applied when available

---

**Production deployment complete! Your phishing awareness training platform is ready for secure, reliable operation.**

🚀 **Status:** Production Ready
📅 **Deployed:** [DATE]
👤 **Deployed By:** [NAME]
