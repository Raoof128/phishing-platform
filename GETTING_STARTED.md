# Getting Started with Phishing Attack Simulation Platform

## Quick Start Guide

This guide will help you get the platform up and running quickly.

### Step 1: Install GoPhish (5 minutes)

```bash
cd phishing-platform/gophish

# Download GoPhish
wget https://github.com/gophish/gophish/releases/download/v0.12.1/gophish-v0.12.1-linux-64bit.zip
unzip gophish-v0.12.1-linux-64bit.zip
chmod +x gophish

# Start GoPhish
./gophish
```

**Important**: Note the generated admin password from the console output!

Access dashboard at: `https://127.0.0.1:3333`
- Username: `admin`
- Password: (from console output)

**Immediately change the default password!**

### Step 2: Configure SMTP (10 minutes)

#### Option A: Gmail (Recommended for Testing)

1. Enable 2-Factor Authentication on your Google account
2. Generate App Password: https://myaccount.google.com/apppasswords
3. In GoPhish dashboard:
   - Go to "Sending Profiles" → "New Profile"
   - Name: `Gmail SMTP`
   - From: `your-email@gmail.com`
   - Host: `smtp.gmail.com:587`
   - Username: `your-email@gmail.com`
   - Password: (app-specific password)
   - Click "Send Test Email" to verify

### Step 3: Install Python Dependencies (5 minutes)

```bash
cd phishing-platform

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Configure API Access (2 minutes)

1. In GoPhish dashboard: Settings → API Keys → Generate New API Key
2. Copy the API key
3. Edit configuration:

```bash
nano automation/config/api_config.yaml
```

Replace `your-api-key-here` with your actual API key.

### Step 5: Test the Setup (5 minutes)

```bash
# Test API connection
python3 automation/campaign_manager.py --test

# List available resources
python3 automation/campaign_manager.py --list-resources
```

### Step 6: Create Your First Campaign (15 minutes)

#### 6.1: Import Email Templates

1. Go to GoPhish dashboard → "Email Templates" → "Import"
2. Import templates from `templates/emails/`:
   - `password_reset.html`
   - `security_alert.html`
   - `hr_document.html`

#### 6.2: Import Landing Pages

1. Go to "Landing Pages" → "Import"
2. Import pages from `templates/landing_pages/`:
   - `office365_login.html`
   - `awareness_page.html`

#### 6.3: Create Test User Group

```bash
# Create sample CSV
python3 automation/user_import.py --create-sample-csv users.csv

# Edit users.csv with your test email addresses
nano users.csv

# Import to GoPhish
python3 automation/user_import.py --csv users.csv --group "Test Users"
```

#### 6.4: Launch Campaign

Via CLI:
```bash
python3 automation/campaign_manager.py \
  --create \
  --name "Test Campaign 1" \
  --template "Password Reset" \
  --landing-page "Office 365 Login" \
  --smtp "Gmail SMTP" \
  --group "Test Users" \
  --launch "2025-10-14 09:00"
```

Or use the GoPhish dashboard to create campaigns manually.

### Step 7: Monitor and Analyze (Ongoing)

```bash
# View campaign summary
python3 automation/campaign_manager.py --campaign-id 1 --summary

# Generate report
python3 automation/analytics.py --campaign-id 1 --output report.html

# View user risk scores
python3 automation/analytics.py --risk-summary

# Assign training based on risk
python3 automation/training_automation.py --campaign-id 1 --auto-assign-by-risk
```

## Common Workflows

### Import Multiple User Groups

```bash
# Finance department
python3 automation/user_import.py --csv finance_users.csv --group "Finance"

# IT department
python3 automation/user_import.py --csv it_users.csv --group "IT"

# Marketing department
python3 automation/user_import.py --csv marketing_users.csv --group "Marketing"
```

### Schedule Progressive Campaigns

```bash
# Easy campaign (next week)
python3 automation/campaign_manager.py \
  --create --name "Campaign 1: Basic" \
  --template "Account Verification" \
  --landing-page "Awareness Page" \
  --smtp "Gmail SMTP" --group "All Users" \
  --launch "2025-10-20 10:00"

# Medium campaign (2 weeks later)
python3 automation/campaign_manager.py \
  --create --name "Campaign 2: Intermediate" \
  --template "Security Alert" \
  --landing-page "Office 365 Login" \
  --smtp "Gmail SMTP" --group "All Users" \
  --launch "2025-11-03 10:00"

# Hard campaign (4 weeks later)
python3 automation/campaign_manager.py \
  --create --name "Campaign 3: Advanced" \
  --template "CEO Fraud" \
  --landing-page "Corporate Portal" \
  --smtp "Gmail SMTP" --group "All Users" \
  --launch "2025-11-17 10:00"
```

### Generate Reports

```bash
# HTML report
python3 automation/analytics.py --campaign-id 1 --format html

# CSV export
python3 automation/analytics.py --campaign-id 1 --format csv

# User risk assessment
python3 automation/analytics.py --user-risk john.doe@company.com
```

## Tips for Success

### 1. Start Small
- Begin with 5-10 test users (your own email addresses)
- Use obvious phishing indicators to test the system
- Gradually increase difficulty and scale

### 2. Communicate Clearly
- Inform participants that phishing simulations will be conducted
- Don't reveal specific timing or tactics
- Provide immediate feedback when users fall for simulations

### 3. Focus on Education
- Never shame or punish users who fail simulations
- Use failures as teachable moments
- Provide accessible training resources

### 4. Track Progress
- Run campaigns quarterly
- Measure improvement over time
- Celebrate successes when metrics improve

### 5. Mix It Up
- Vary email templates and scenarios
- Use different sending times (morning vs afternoon)
- Test both desktop and mobile responses

## Troubleshooting

### "API connection failed"
- Check that GoPhish is running: `ps aux | grep gophish`
- Verify API key in `automation/config/api_config.yaml`
- Check server URL is correct: `https://127.0.0.1:3333`

### "SMTP authentication failed"
- For Gmail: ensure using app-specific password (not account password)
- Verify 2FA is enabled on Gmail account
- Check SMTP port and host are correct

### "No campaigns found"
- Use GoPhish dashboard to create at least one campaign manually first
- Verify database path in config: `gophish/gophish.db`

### "Import failed"
- Check CSV format matches expected columns
- Ensure email addresses are valid
- Look for special characters or encoding issues

## Next Steps

1. **Review Documentation**: Read `docs/installation_guide.md` for detailed setup
2. **Customize Templates**: Modify email and landing page templates for your organization
3. **Create Training Content**: Develop security awareness training materials
4. **Schedule Regular Campaigns**: Set up quarterly phishing simulation schedule
5. **Monitor Metrics**: Track improvement in open rates, click rates, and report rates

## Security Reminders

- ⚠️ **Get authorization** before running campaigns
- 🔒 **Protect API keys** - never commit to version control
- 📧 **Use test emails** first to verify configuration
- 🎯 **Define scope** clearly with management
- 📊 **Report results** to stakeholders regularly

## Support

For detailed documentation:
- Installation: `docs/installation_guide.md`
- User Manual: `docs/user_manual.md`
- API Reference: `docs/api_documentation.md`
- Troubleshooting: `docs/troubleshooting.md`

---

**Happy phishing (simulations)!** 🎣🔒
