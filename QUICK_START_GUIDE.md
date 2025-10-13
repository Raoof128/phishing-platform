# Phishing Platform - Quick Start Guide

## 🚀 Super Quick Start (Automated)

```bash
./quickstart.sh
```

This script will:
- ✅ Start GoPhish server
- ✅ Display admin credentials
- ✅ Save credentials to `.gophish_credentials`
- ✅ Create logs directory
- ✅ Show next steps

---

## 📋 Step-by-Step Manual Setup

### Step 1: Start GoPhish

```bash
./run_gophish.sh
```

**Save the admin password displayed!** It will look like: `6d3e10f2078218c6`

**Access GoPhish Admin:**
- URL: https://127.0.0.1:3333
- Username: `admin`
- Password: `<the-password-displayed>`

### Step 2: Generate API Key

1. Login to GoPhish admin panel
2. You'll be prompted to change your password (choose a strong one)
3. Navigate to: **Settings** → **Account Settings**
4. Click **"Reset API Key"**
5. Copy the generated API key

### Step 3: Update Configuration

**Easy Way (Recommended):**
```bash
./update_api_key.sh YOUR_API_KEY_HERE
```

**Manual Way:**
```bash
nano automation/config/api_config.yaml
```
Update the `api_key` line:
```yaml
api_key: YOUR_ACTUAL_API_KEY_HERE
```

### Step 4: Start Dashboard

```bash
./run_dashboard.sh
```

Access dashboard at: http://localhost:5000

---

## 🎯 Creating Your First Campaign

### 1. Import Target Users

Create a CSV file with user data:
```csv
email,first_name,last_name,position
john.doe@company.com,John,Doe,Software Engineer
jane.smith@company.com,Jane,Smith,Marketing Manager
```

Import the users:
```bash
source venv/bin/activate
python3 -m automation.user_import --csv users.csv --group "Test Users"
```

Or create a sample CSV:
```bash
source venv/bin/activate
python3 -m automation.user_import --create-sample-csv sample_users.csv
python3 -m automation.user_import --csv sample_users.csv --group "Sample Group"
```

### 2. Create Email Template in GoPhish

1. Login to GoPhish admin panel
2. Go to **Email Templates** → **New Template**
3. Name: "Password Reset Test"
4. Use one of the templates from `templates/emails/` directory
5. Important variables to include:
   - `{{.FirstName}}` - Recipient's first name
   - `{{.Email}}` - Recipient's email
   - `{{.URL}}` - Phishing link (automatically tracked)

### 3. Create Landing Page

1. Go to **Landing Pages** → **New Page**
2. Name: "Office 365 Login"
3. Import HTML from `templates/landing_pages/office365_login.html`
4. Check "Capture Submitted Data"
5. Check "Capture Passwords"
6. Add redirect URL (optional)

### 4. Configure SMTP Profile

1. Go to **Sending Profiles** → **New Profile**
2. Configure your SMTP settings
3. Test the connection

Or use the config file:
```bash
nano automation/config/smtp_config.yaml
```

### 5. Launch Campaign via CLI

```bash
source venv/bin/activate

# List available resources
python3 -m automation.campaign_manager --list-resources

# Create a campaign
python3 -m automation.campaign_manager --create \
  --name "Q4 Security Awareness Test" \
  --template "Password Reset Test" \
  --landing-page "Office 365 Login" \
  --smtp "Company SMTP" \
  --group "Test Users" \
  --url "http://localhost:8080"
```

### 6. Monitor Campaign

**View in Dashboard:**
```bash
# Open http://localhost:5000
```

**View via CLI:**
```bash
source venv/bin/activate

# List all campaigns
python3 -m automation.campaign_manager --list-campaigns

# View specific campaign details
python3 -m automation.campaign_manager --campaign-id 1 --summary
```

---

## 📊 Analytics & Reporting

### View User Risk Scores

```bash
source venv/bin/activate
python3 -m automation.analytics --risk-summary
```

### Generate Campaign Report

```bash
source venv/bin/activate

# HTML report
python3 -m automation.analytics --campaign-id 1 --format html

# CSV export
python3 -m automation.analytics --campaign-id 1 --format csv
```

Reports are saved to: `reports/`

### Check Individual User Risk

```bash
source venv/bin/activate
python3 -m automation.analytics --user-risk john.doe@company.com
```

---

## 🎓 Automated Training Assignment

### Assign Training Based on Campaign Results

```bash
source venv/bin/activate

# Automatically assign training to users who failed
python3 -m automation.training_automation --campaign-id 1 --auto-assign-by-risk
```

This will:
- ✅ Analyze campaign results
- ✅ Calculate risk scores
- ✅ Assign appropriate training modules
- ✅ Send training assignment emails

### Training Module Levels

- **High Risk**: Advanced phishing recognition + Incident response
- **Medium Risk**: Intermediate security awareness + Email safety
- **Low Risk**: Basic email safety training

---

## 🔧 Useful Commands

### Check Platform Status

```bash
# Check if GoPhish is running
pgrep gophish && echo "GoPhish: Running" || echo "GoPhish: Stopped"

# View GoPhish logs
tail -f logs/gophish.log

# View dashboard logs
tail -f logs/dashboard.log
```

### Test API Connection

```bash
source venv/bin/activate
python3 -m automation.campaign_manager --test
```

### List All Resources

```bash
source venv/bin/activate
python3 -m automation.campaign_manager --list-resources
```

### List All Groups

```bash
source venv/bin/activate
python3 -m automation.user_import --list-groups
```

---

## 🛑 Stopping Services

### Stop GoPhish

```bash
pkill gophish
```

### Stop Dashboard

Press `Ctrl+C` in the terminal where it's running

---

## 📁 Important Files & Directories

```
phishing-platform/
├── quickstart.sh              # Automated startup script
├── update_api_key.sh          # API key configuration helper
├── setup.sh                   # Initial setup
├── run_gophish.sh            # Start GoPhish
├── run_dashboard.sh          # Start dashboard
├── .gophish_credentials      # Saved credentials (auto-generated)
├── automation/
│   ├── config/
│   │   ├── api_config.yaml   # Main configuration
│   │   └── smtp_config.yaml  # Email settings
│   ├── campaign_manager.py   # Campaign automation
│   ├── analytics.py          # Reporting & risk scoring
│   ├── training_automation.py # Training assignment
│   └── user_import.py        # User management
├── dashboard/
│   └── app.py               # Web dashboard
├── templates/
│   ├── emails/              # Email templates
│   └── landing_pages/       # Landing page templates
├── training/
│   └── modules/             # Training content
├── logs/                    # Log files
└── reports/                 # Generated reports
```

---

## 🆘 Troubleshooting

### GoPhish won't start

**Error: "bind: permission denied" on port 80**
- ✅ Already fixed! Configuration updated to use port 8080

**Error: "address already in use"**
```bash
# Check what's using the port
sudo lsof -i :3333
sudo lsof -i :8080

# Kill existing process
pkill gophish
```

### Dashboard shows "API not configured"

1. Make sure GoPhish is running
2. Verify API key is correct in `automation/config/api_config.yaml`
3. Test connection:
   ```bash
   source venv/bin/activate
   python3 -m automation.campaign_manager --test
   ```

### Import errors

```bash
# Reinstall dependencies
source venv/bin/activate
pip install -r requirements.txt
```

### Can't access admin panel

- URL must use `https://` not `http://`
- Accept the self-signed certificate warning
- Check if GoPhish is running: `pgrep gophish`

---

## 🔒 Security Notes

- ✅ This platform is for **legitimate security awareness training only**
- ✅ Always get proper authorization before conducting campaigns
- ✅ Follow your organization's security policies
- ✅ Store API keys and credentials securely
- ✅ Use HTTPS in production
- ✅ Regularly review and delete old campaign data

---

## 📚 Additional Resources

- **GoPhish Documentation**: https://docs.getgophish.com/
- **Project Documentation**: See `docs/` directory
- **Training Modules**: See `training/modules/` directory
- **Getting Started Guide**: `GETTING_STARTED.md`
- **API Documentation**: `docs/api_documentation.md`

---

## 💡 Pro Tips

1. **Test campaigns** on yourself first before sending to real users
2. **Start small** - test with 5-10 users before scaling up
3. **Use realistic scenarios** based on actual threats your organization faces
4. **Follow up** with training for users who fall for phishing attempts
5. **Track trends** over time to measure improvement
6. **Customize templates** to match your organization's email style
7. **Schedule campaigns** during business hours for realistic results

---

## ✅ Quick Checklist

- [ ] Run `./quickstart.sh`
- [ ] Login to GoPhish (https://127.0.0.1:3333)
- [ ] Generate API key
- [ ] Run `./update_api_key.sh YOUR_KEY`
- [ ] Start dashboard `./run_dashboard.sh`
- [ ] Import test users
- [ ] Create email template
- [ ] Create landing page
- [ ] Launch test campaign
- [ ] Monitor results in dashboard
- [ ] Generate reports
- [ ] Assign training to high-risk users

---

**Need Help?** Check the logs:
```bash
tail -f logs/gophish.log       # GoPhish logs
tail -f logs/dashboard.log     # Dashboard logs
```

**Happy phishing awareness training! 🎣🛡️**
