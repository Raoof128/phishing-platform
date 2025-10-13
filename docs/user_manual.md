# User Manual

Complete guide to using the Phishing Attack Simulation and Training Platform.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Importing Users](#importing-users)
3. [Creating Email Templates](#creating-email-templates)
4. [Creating Landing Pages](#creating-landing-pages)
5. [Running Campaigns](#running-campaigns)
6. [Viewing Results](#viewing-results)
7. [Assigning Training](#assigning-training)
8. [Analytics Dashboard](#analytics-dashboard)

## Quick Start

Complete workflow to run your first phishing simulation campaign.

### Step 1: Import Target Users

Create a CSV file with your test users:

```csv
first_name,last_name,email,position
John,Doe,john.doe@yourcompany.com,Marketing Manager
Jane,Smith,jane.smith@yourcompany.com,Software Engineer
```

Import the users:

```bash
cd automation
python user_import.py --csv ../users.csv --group "Test Group"
```

### Step 2: Create Email Template in GoPhish

1. Go to GoPhish: https://127.0.0.1:3333
2. Click **Email Templates**
3. Click **New Template**
4. Fill in details:
   - **Name**: `Password Reset Test`
   - **Subject**: `URGENT: Your password expires tomorrow`
   - **HTML**: Copy content from `templates/emails/password_reset.html`
5. Click **Import Template** or paste HTML
6. Click **Save Template**

### Step 3: Create Landing Page in GoPhish

1. Click **Landing Pages**
2. Click **New Page**
3. Fill in details:
   - **Name**: `Office 365 Login`
   - **HTML**: Copy content from `templates/landing_pages/office365_login.html`
4. Check **Capture Submitted Data**
5. Check **Capture Passwords**
6. Click **Save Page**

### Step 4: Launch Campaign via CLI

```bash
python campaign_manager.py \
  --create \
  --name "Q4 2025 Password Reset Test" \
  --template "Password Reset Test" \
  --landing-page "Office 365 Login" \
  --group "Test Group" \
  --launch "2025-10-15 09:00"
```

### Step 5: Monitor Results

View campaign results:

```bash
python campaign_manager.py --results 1
```

Or use the analytics dashboard:

```bash
cd ../dashboard
python app.py
# Visit http://localhost:5000
```

### Step 6: Assign Training

Automatically assign training to users who failed:

```bash
cd ../automation
python training_automation.py \
  --campaign-id 1 \
  --auto-assign-by-risk \
  --min-risk 30
```

## Importing Users

### CSV Format

Your CSV file must have these columns:

- `first_name`: User's first name
- `last_name`: User's last name
- `email`: Email address (required)
- `position`: Job title (optional)

**Example CSV:**

```csv
first_name,last_name,email,position
Alice,Williams,alice@company.com,HR Director
Bob,Johnson,bob@company.com,Sales Manager
Charlie,Brown,charlie@company.com,Developer
```

### Import Command

```bash
python user_import.py --csv users.csv --group "Sales Team"
```

### Update Existing Group

```bash
python user_import.py --csv updated_users.csv --group "Sales Team" --update
```

### Validate Emails

Before importing, validate email addresses:

```bash
# Create emails.txt with one email per line
python user_import.py --validate-emails emails.txt
```

### Create Sample CSV

Generate a sample CSV template:

```bash
python user_import.py --create-sample
```

## Creating Email Templates

### Using Pre-built Templates

We provide 5 ready-to-use templates in `templates/emails/`:

1. **password_reset.html** - Urgent password expiration
2. **hr_document.html** - Important HR policy document
3. **security_alert.html** - Suspicious login detected
4. **ceo_fraud.html** - Urgent CEO request
5. **account_verification.html** - Account verification required

### GoPhish Template Variables

Use these variables for personalization:

- `{{.FirstName}}` - User's first name
- `{{.LastName}}` - User's last name
- `{{.Email}}` - User's email address
- `{{.Position}}` - User's job title
- `{{.URL}}` - Unique tracking link
- `{{.Tracker}}` - Tracking pixel (email opens)
- `{{.RId}}` - Result ID

### Import Template to GoPhish

1. Go to **Email Templates** → **New Template**
2. Enter template name
3. Enter subject line
4. Click **Import Email** and paste HTML from template file
5. Or manually paste HTML into editor
6. **Preview** to test rendering
7. Click **Save Template**

## Creating Landing Pages

### Using Pre-built Pages

We provide 5 landing pages in `templates/landing_pages/`:

**Credential Capture Pages:**
1. **office365_login.html** - Microsoft Office 365
2. **gmail_login.html** - Google Gmail
3. **corporate_portal.html** - Generic corporate portal

**Awareness Pages:**
4. **awareness_page.html** - "You've been phished!" notification
5. **training_redirect.html** - Redirect to training modules

### Import Landing Page to GoPhish

1. Go to **Landing Pages** → **New Page**
2. Enter page name
3. Paste HTML from template file
4. **For credential capture**: Check "Capture Submitted Data" and "Capture Passwords"
5. **For awareness**: Uncheck data capture options
6. Click **Save Page**

### Customize Landing Pages

Edit the HTML to match your organization:

- Update company logos
- Change color schemes
- Modify text and messaging
- Add organization-specific details

## Running Campaigns

### Create Campaign via CLI

```bash
python campaign_manager.py \
  --create \
  --name "Campaign Name" \
  --template "Email Template Name" \
  --landing-page "Landing Page Name" \
  --group "Target Group Name" \
  --launch "2025-10-15 14:00"
```

### Schedule Progressive Campaigns

Create a series of campaigns with increasing difficulty:

```python
from automation.campaign_manager import GophishCampaign, load_config

config = load_config()
campaign = GophishCampaign(
    api_key=config['gophish']['api_key'],
    server_url=config['gophish']['api_url']
)

difficulty_levels = [
    {'name': 'Easy Test', 'template': 'Basic Phish', 'page': 'Simple Login'},
    {'name': 'Medium Test', 'template': 'HR Document', 'page': 'Office365'},
    {'name': 'Hard Test', 'template': 'CEO Fraud', 'page': 'Corporate Portal'}
]

campaigns = campaign.schedule_progressive_campaigns(
    user_group='Finance Team',
    difficulty_levels=difficulty_levels,
    interval_days=14  # 2 weeks between campaigns
)
```

### List All Campaigns

```bash
python campaign_manager.py --list
```

## Viewing Results

### CLI Results

View detailed campaign results:

```bash
python campaign_manager.py --results 1
```

Output:

```
Campaign Results: Q4 2025 Password Reset Test
============================================================
Status: Completed
Emails Sent: 50
Opened: 42 (84.0%)
Clicked: 18 (36.0%)
Submitted Data: 7 (14.0%)
Reported: 3 (6.0%)
```

### Analytics Reports

Generate HTML report:

```bash
python analytics.py --campaign-id 1 --output report.html --format html
```

Generate JSON export:

```bash
python analytics.py --campaign-id 1 --output report.json --format json
```

### User Risk Scores

Calculate individual user risk:

```bash
python analytics.py --user-risk john.doe@company.com
```

Get all user risk scores:

```bash
python analytics.py --all-risks --output risks.csv
```

### Timeline Visualization

Generate campaign timeline plot:

```bash
python analytics.py --campaign-id 1 --plot-timeline --output timeline.png
```

## Assigning Training

### Automatic Training Assignment

Assign training based on risk scores:

```bash
python training_automation.py \
  --campaign-id 1 \
  --auto-assign-by-risk \
  --min-risk 0
```

**Risk-based assignment:**
- Risk Score 70-100: Advanced Phishing Recognition
- Risk Score 40-69: Intermediate Security Awareness
- Risk Score 1-39: Basic Email Safety
- Risk Score 0: Basic Email Safety (preventive)

### Minimum Risk Threshold

Only assign to users above a certain risk level:

```bash
python training_automation.py \
  --campaign-id 1 \
  --auto-assign-by-risk \
  --min-risk 50
```

This will only assign training to users with risk score ≥ 50.

### Individual User Training

Assign training to a specific user:

```bash
python training_automation.py \
  --user-email john.doe@company.com \
  --auto-assign-by-risk
```

## Analytics Dashboard

### Starting the Dashboard

```bash
cd dashboard
python app.py
```

Visit: `http://localhost:5000`

### Dashboard Features

**Overview Stats:**
- Total campaigns
- Active campaigns
- Total users
- High-risk users
- Overall click rate
- Overall submit rate

**Risk Distribution Chart:**
- Pie chart showing users by risk level
- High / Medium / Low / None categories

**Campaign Trends:**
- Line chart showing performance over time
- Click rate, submit rate, report rate trends

**Recent Campaigns Table:**
- ID, name, status, launch date, completion date
- Click rows for detailed view

**High Risk Users Table:**
- Top 10 users by risk score
- Name, email, position, scores
- Identify users needing immediate training

### Auto-Refresh

Dashboard automatically refreshes every 60 seconds.

Manual refresh: Click "↻ Refresh Data" button.

## Best Practices

### Campaign Planning

1. **Start Easy**: Begin with obvious phishing attempts
2. **Progressive Difficulty**: Gradually increase sophistication
3. **Regular Cadence**: Run campaigns quarterly
4. **Vary Tactics**: Mix different attack types
5. **Track Improvement**: Monitor trends over time

### User Communication

1. **Transparency**: Inform users about the program
2. **No Punishment**: Focus on education, not discipline
3. **Immediate Feedback**: Use awareness landing pages
4. **Follow-up Training**: Assign training promptly
5. **Celebrate Success**: Recognize users who report phishing

### Security Measures

1. **Secure Credentials**: Never commit real credentials to git
2. **Limit Access**: Restrict who can run campaigns
3. **Data Protection**: Encrypt captured credentials immediately
4. **Data Retention**: Auto-delete sensitive data after campaign
5. **Audit Logging**: Track all campaign activities

## Troubleshooting

### Campaign Not Sending

1. Check SMTP profile is configured correctly
2. Verify email credentials are valid
3. Test with "Send Test Email" in GoPhish
4. Check spam folder for test emails
5. Review GoPhish logs: `tail -f gophish/gophish.log`

### Users Not Receiving Emails

1. Check email addresses are correct
2. Verify users' email servers aren't blocking
3. Check SPF/DKIM records if using custom domain
4. Try different sending profile or SMTP server
5. Reduce sending rate to avoid spam filters

### Landing Page Not Loading

1. Verify phishing server is running on port 80
2. Check firewall allows access to port 80
3. Test landing page URL directly in browser
4. Review landing page HTML for errors
5. Check GoPhish phishing server logs

### Training Emails Not Sending

1. Verify SMTP settings in `config/smtp_config.yaml`
2. Test SMTP credentials manually
3. Check user email addresses are valid
4. Review Python script output for errors
5. Verify rate limits aren't exceeded

## Support

For additional help:

- Review [Installation Guide](installation.md)
- Check [Troubleshooting Guide](troubleshooting.md)
- Consult [API Documentation](api_documentation.md)
- Visit GoPhish docs: https://docs.getgophish.com
