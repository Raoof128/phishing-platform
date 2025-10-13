# API Documentation

Complete reference for the Phishing Platform automation APIs.

## Table of Contents

1. [Campaign Manager API](#campaign-manager-api)
2. [Analytics API](#analytics-api)
3. [Training Automation API](#training-automation-api)
4. [User Import API](#user-import-api)
5. [Dashboard REST API](#dashboard-rest-api)

## Campaign Manager API

### GophishCampaign Class

Main class for managing phishing campaigns.

#### Initialize

```python
from automation.campaign_manager import GophishCampaign, load_config

config = load_config()
campaign_api = GophishCampaign(
    api_key=config['gophish']['api_key'],
    server_url=config['gophish']['api_url'],
    verify_ssl=False
)
```

#### Methods

**get_campaigns()**

Get all campaigns.

```python
campaigns = campaign_api.get_campaigns()
# Returns: List[dict]
```

**get_campaign(campaign_id: int)**

Get specific campaign by ID.

```python
campaign = campaign_api.get_campaign(1)
# Returns: dict
```

**create_campaign()**

Create a new phishing campaign.

```python
campaign = campaign_api.create_campaign(
    name="Q4 Security Test",
    template_name="Password Reset",
    page_name="Office365 Login",
    smtp_name="Production SMTP",
    group_name="Marketing Team",
    launch_date=datetime(2025, 10, 15, 9, 0)  # Optional
)
# Returns: dict with campaign details
```

**get_campaign_results(campaign_id: int)**

Get comprehensive campaign metrics.

```python
metrics = campaign_api.get_campaign_results(1)
# Returns: dict with metrics

# Example response:
{
    'campaign_id': 1,
    'campaign_name': 'Q4 Security Test',
    'status': 'Completed',
    'emails_sent': 100,
    'emails_opened': 85,
    'links_clicked': 35,
    'data_submitted': 12,
    'reported': 5,
    'open_rate': 85.0,
    'click_rate': 35.0,
    'submit_rate': 12.0,
    'report_rate': 5.0
}
```

**schedule_progressive_campaigns()**

Schedule multiple campaigns with increasing difficulty.

```python
difficulty_levels = [
    {'name': 'Easy', 'template': 'Basic', 'page': 'Simple'},
    {'name': 'Medium', 'template': 'HR Doc', 'page': 'Office365'},
    {'name': 'Hard', 'template': 'CEO Fraud', 'page': 'Portal'}
]

campaigns = campaign_api.schedule_progressive_campaigns(
    user_group='Finance Team',
    difficulty_levels=difficulty_levels,
    start_date=datetime.now(),
    interval_days=14
)
# Returns: List[dict] of created campaigns
```

### GophishGroups Class

Manage user groups.

```python
from automation.campaign_manager import GophishGroups

groups_api = GophishGroups(
    api_key=config['gophish']['api_key'],
    server_url=config['gophish']['api_url']
)
```

**create_group()**

```python
targets = [
    {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john@company.com',
        'position': 'Manager'
    }
]

group = groups_api.create_group(
    name='Sales Team',
    targets=targets
)
```

## Analytics API

### PhishingAnalytics Class

Analyze campaign data and calculate risk scores.

#### Initialize

```python
from automation.analytics import PhishingAnalytics

analytics = PhishingAnalytics('gophish/gophish.db')
```

#### Methods

**get_campaign_metrics(campaign_id: int)**

Extract metrics from database.

```python
metrics = analytics.get_campaign_metrics(1)
# Returns: dict
```

**calculate_risk_score(user_email: str)**

Calculate user risk score based on behavior.

```python
score, details = analytics.calculate_risk_score('john@company.com')

# score: int (0-100)
# details: dict with breakdown

# Example details:
{
    'email': 'john@company.com',
    'risk_score': 75,
    'risk_level': 'HIGH',
    'campaigns_participated': 3,
    'emails_opened': 3,
    'links_clicked': 2,
    'data_submitted': 1,
    'reported': 0
}
```

**Risk Score Calculation:**
- Email Opened: +10 points
- Link Clicked: +30 points
- Data Submitted: +50 points
- Email Reported: -20 points (good behavior)

**get_all_user_risks()**

Get risk scores for all users.

```python
df = analytics.get_all_user_risks()
# Returns: pandas DataFrame

# Columns: email, first_name, last_name, position, risk_score,
#          risk_level, campaigns_participated, links_clicked, etc.
```

**generate_report(campaign_id: int, output_format: str)**

Generate campaign report.

```python
# HTML report
html_report = analytics.generate_report(1, output_format='html')

# JSON export
json_data = analytics.generate_report(1, output_format='json')

# Text summary
text_report = analytics.generate_report(1, output_format='text')
```

**plot_campaign_timeline(campaign_id: int, output_path: str)**

Create timeline visualization.

```python
analytics.plot_campaign_timeline(
    campaign_id=1,
    output_path='timeline.png'
)
```

## Training Automation API

### TrainingAutomation Class

Automate training assignment based on risk.

#### Initialize

```python
from automation.training_automation import TrainingAutomation, load_smtp_config
from automation.analytics import PhishingAnalytics

smtp_config = load_smtp_config()
analytics = PhishingAnalytics('gophish/gophish.db')

training = TrainingAutomation(smtp_config, analytics)
```

#### Methods

**assign_training_based_on_risk(user_email: str)**

Automatically assign appropriate training.

```python
module = training.assign_training_based_on_risk('john@company.com')
# Returns: str (module identifier)

# Assigned based on risk score:
# 70-100: 'advanced_phishing_recognition'
# 40-69:  'intermediate_security_awareness'
# 1-39:   'basic_email_safety'
```

**assign_training_to_campaign_users(campaign_id: int, min_risk_score: int)**

Assign training to all campaign users above risk threshold.

```python
summary = training.assign_training_to_campaign_users(
    campaign_id=1,
    min_risk_score=30
)

# Returns: dict
{
    'total_users': 50,
    'assigned': 35,
    'skipped': 15,
    'failed': 0,
    'by_level': {
        'basic': 20,
        'intermediate': 10,
        'advanced': 5
    }
}
```

**send_training_email()**

Send training assignment email manually.

```python
success = training.send_training_email(
    user_email='john@company.com',
    user_name='John Doe',
    training_module='intermediate_security_awareness',
    risk_level='MEDIUM'
)
# Returns: bool
```

## User Import API

### Functions

**read_csv_users(csv_file: str)**

Read users from CSV file.

```python
from automation.user_import import read_csv_users

users = read_csv_users('users.csv')
# Returns: List[dict]

# Example:
[
    {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john@company.com',
        'position': 'Manager'
    }
]
```

**import_users_to_gophish()**

Import users and create GoPhish group.

```python
from automation.user_import import import_users_to_gophish

summary = import_users_to_gophish(
    csv_file='users.csv',
    group_name='Sales Team',
    update_existing=False
)

# Returns: dict
{
    'action': 'created',  # or 'updated'
    'group_id': 5,
    'group_name': 'Sales Team',
    'total_users': 25,
    'csv_file': 'users.csv'
}
```

**validate_email_list(emails: List[str])**

Validate email addresses.

```python
from automation.user_import import validate_email_list

emails = ['valid@example.com', 'invalid', 'test@test.com']
valid = validate_email_list(emails)
# Returns: ['valid@example.com', 'test@test.com']
```

## Dashboard REST API

The Flask dashboard provides REST endpoints.

### Base URL

```
http://localhost:5000/api
```

### Endpoints

#### GET /campaigns

List all campaigns.

**Request:**
```bash
curl http://localhost:5000/api/campaigns
```

**Response:**
```json
[
    {
        "id": 1,
        "name": "Q4 Security Test",
        "status": "Completed",
        "created_date": "2025-10-01T10:00:00Z",
        "launch_date": "2025-10-15T09:00:00Z",
        "completed_date": "2025-10-20T15:30:00Z"
    }
]
```

#### GET /campaign/{id}

Get specific campaign.

**Request:**
```bash
curl http://localhost:5000/api/campaign/1
```

#### GET /campaign/{id}/stats

Get campaign statistics.

**Response:**
```json
{
    "campaign_id": 1,
    "emails_sent": 100,
    "emails_opened": 85,
    "links_clicked": 35,
    "data_submitted": 12,
    "reported": 5,
    "open_rate": 85.0,
    "click_rate": 35.0,
    "submit_rate": 12.0,
    "report_rate": 5.0
}
```

#### GET /user_risks

Get all user risk scores.

**Response:**
```json
[
    {
        "email": "john@company.com",
        "first_name": "John",
        "last_name": "Doe",
        "risk_score": 75,
        "risk_level": "HIGH",
        "campaigns_participated": 3,
        "links_clicked": 2,
        "data_submitted": 1
    }
]
```

#### GET /user_risk/{email}

Get specific user's risk score.

```bash
curl http://localhost:5000/api/user_risk/john@company.com
```

#### GET /dashboard_summary

Get overall dashboard statistics.

**Response:**
```json
{
    "total_campaigns": 15,
    "active_campaigns": 2,
    "completed_campaigns": 13,
    "total_users": 250,
    "high_risk_users": 35,
    "overall_click_rate": 28.5,
    "overall_submit_rate": 11.2
}
```

#### GET /risk_distribution

Get user distribution by risk level.

**Response:**
```json
{
    "HIGH": 35,
    "MEDIUM": 80,
    "LOW": 100,
    "NONE": 35
}
```

#### GET /campaign_trends

Get performance trends over time.

**Response:**
```json
[
    {
        "campaign_name": "Q3 Test",
        "launch_date": "2025-07-15",
        "click_rate": 42.0,
        "submit_rate": 18.0,
        "report_rate": 3.0
    }
]
```

## Error Handling

All API methods may raise exceptions:

```python
try:
    campaign = campaign_api.get_campaign(999)
except Exception as e:
    print(f"Error: {e}")
```

Common errors:
- `ValueError`: Invalid parameters
- `FileNotFoundError`: Database not found
- `requests.exceptions.RequestException`: API connection failed

## Configuration

### Load Configuration

```python
from automation.campaign_manager import load_config

config = load_config('config/api_config.yaml')
```

### Configuration Structure

```yaml
gophish:
  api_url: "https://127.0.0.1:3333"
  api_key: "YOUR_API_KEY"
  verify_ssl: false

platform:
  dashboard_host: "0.0.0.0"
  dashboard_port: 5000

campaign_defaults:
  track_email_opens: true
  track_link_clicks: true
  risk_weights:
    email_opened: 10
    link_clicked: 30
    credentials_submitted: 50
    reported: -20
```

## Examples

### Complete Workflow

```python
from automation.campaign_manager import GophishCampaign, load_config
from automation.analytics import PhishingAnalytics
from automation.training_automation import TrainingAutomation, load_smtp_config

# Initialize
config = load_config()
campaign_api = GophishCampaign(
    api_key=config['gophish']['api_key'],
    server_url=config['gophish']['api_url']
)

# Create campaign
campaign = campaign_api.create_campaign(
    name="Security Test",
    template_name="Password Reset",
    page_name="Office365",
    smtp_name="Default",
    group_name="IT Team"
)

campaign_id = campaign['id']

# Wait for campaign to complete...

# Analyze results
analytics = PhishingAnalytics('gophish/gophish.db')
metrics = analytics.get_campaign_metrics(campaign_id)

print(f"Click Rate: {metrics['click_rate']}%")

# Assign training
smtp_config = load_smtp_config()
training = TrainingAutomation(smtp_config, analytics)

summary = training.assign_training_to_campaign_users(
    campaign_id=campaign_id,
    min_risk_score=40
)

print(f"Training assigned to {summary['assigned']} users")
```

## CLI Reference

All modules have CLI interfaces:

```bash
# Campaign management
python campaign_manager.py --list
python campaign_manager.py --create --name "Test" --template "Phish" --landing-page "Login" --group "Users"
python campaign_manager.py --results 1

# Analytics
python analytics.py --campaign-id 1 --output report.html
python analytics.py --user-risk john@company.com
python analytics.py --all-risks --output risks.csv

# Training
python training_automation.py --campaign-id 1 --auto-assign-by-risk
python training_automation.py --user-email john@company.com --auto-assign-by-risk

# User import
python user_import.py --csv users.csv --group "Team"
python user_import.py --create-sample
```
