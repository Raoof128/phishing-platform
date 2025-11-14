# API Documentation

## Overview

The Phishing Awareness Training Platform provides a RESTful API for managing campaigns, analyzing user risk, and accessing analytics data.

**Base URL**: `http://localhost:5000`

**API Version**: `1.1.0`

---

## Table of Contents

1. [Authentication](#authentication)
2. [Rate Limiting](#rate-limiting)
3. [Error Handling](#error-handling)
4. [Endpoints](#endpoints)
   - [Health Check](#health-check)
   - [Campaign Management](#campaign-management)
   - [User Risk Analysis](#user-risk-analysis)
   - [Dashboard Analytics](#dashboard-analytics)

---

## Authentication

> **Note**: Authentication is currently not implemented. All endpoints are publicly accessible. This will be addressed in version 1.2.0 with JWT-based authentication.

**Planned Authentication Flow:**
```
POST /api/auth/login
{
  "username": "admin",
  "password": "secure_password"
}

Response:
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "expires_in": 3600
}

Usage:
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

---

## Rate Limiting

The API implements rate limiting to prevent abuse:

- **Per Minute**: 60 requests
- **Per Hour**: 1000 requests

**Rate Limit Headers:**
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 58
X-RateLimit-Reset: 1642089600
```

**Rate Limit Exceeded Response:**
```json
{
  "error": "Rate limit exceeded",
  "message": "Too many requests. Please try again later.",
  "retry_after": 45
}
```
**Status Code**: `429 Too Many Requests`

---

## Error Handling

### Standard Error Response

```json
{
  "error": "Error type",
  "details": "Detailed error message",
  "timestamp": "2025-01-14T15:30:00Z"
}
```

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Authentication required |
| 404 | Not Found - Resource doesn't exist |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error |
| 503 | Service Unavailable - Services not initialized |

---

## Endpoints

### Health Check

#### GET /health

Check the health status of the API and its dependencies.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-14T15:30:00Z",
  "services": {
    "campaign_api": true,
    "analytics": true
  }
}
```

**Status Codes:**
- `200 OK` - All services healthy
- `503 Service Unavailable` - Some services unavailable

**Example:**
```bash
curl http://localhost:5000/health
```

---

### Campaign Management

#### GET /api/campaigns

Retrieve all campaigns.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Q1 2025 Security Awareness",
    "status": "Completed",
    "created_date": "2025-01-01T10:00:00Z",
    "launch_date": "2025-01-02T09:00:00Z",
    "completed_date": "2025-01-15T17:00:00Z"
  },
  {
    "id": 2,
    "name": "Executive Team Training",
    "status": "In progress",
    "created_date": "2025-01-10T14:00:00Z",
    "launch_date": "2025-01-11T08:00:00Z",
    "completed_date": null
  }
]
```

**Example:**
```bash
curl http://localhost:5000/api/campaigns
```

---

#### GET /api/campaign/:id

Retrieve detailed information about a specific campaign.

**Parameters:**
- `id` (integer, required): Campaign ID (must be >= 1)

**Response:**
```json
{
  "id": 1,
  "name": "Q1 2025 Security Awareness",
  "status": "Completed",
  "created_date": "2025-01-01T10:00:00Z",
  "launch_date": "2025-01-02T09:00:00Z",
  "completed_date": "2025-01-15T17:00:00Z",
  "template": {
    "name": "Fake Invoice",
    "subject": "Your invoice is ready"
  },
  "smtp": {
    "name": "Training SMTP Server"
  },
  "groups": [
    {
      "id": 5,
      "name": "All Employees"
    }
  ]
}
```

**Error Responses:**
```json
// Invalid ID
{
  "error": "Validation failed",
  "details": ["Invalid campaign_id: must be a valid integer"]
}

// Campaign not found
{
  "error": "Campaign not found",
  "details": "No campaign with ID 999"
}
```

**Example:**
```bash
curl http://localhost:5000/api/campaign/1
```

---

#### GET /api/campaign/:id/stats

Get statistical metrics for a specific campaign.

**Parameters:**
- `id` (integer, required): Campaign ID

**Response:**
```json
{
  "emails_sent": 150,
  "emails_opened": 68,
  "links_clicked": 34,
  "data_submitted": 12,
  "reported": 18,
  "open_rate": 45.33,
  "click_rate": 22.67,
  "submit_rate": 8.0,
  "report_rate": 12.0
}
```

**Field Descriptions:**
- `emails_sent`: Total phishing emails sent
- `emails_opened`: Number of emails opened
- `links_clicked`: Number of users who clicked the link
- `data_submitted`: Number of users who submitted credentials
- `reported`: Number of users who reported the email
- `*_rate`: Percentage calculated as (action_count / emails_sent * 100)

**Example:**
```bash
curl http://localhost:5000/api/campaign/1/stats
```

---

#### GET /api/campaign/:id/chart

Get campaign results formatted for chart visualization.

**Parameters:**
- `id` (integer, required): Campaign ID

**Response:**
```json
{
  "labels": ["Sent", "Opened", "Clicked", "Submitted", "Reported"],
  "values": [150, 68, 34, 12, 18],
  "percentages": [100, 45.33, 22.67, 8.0, 12.0]
}
```

**Example:**
```bash
curl http://localhost:5000/api/campaign/1/chart
```

**JavaScript Example:**
```javascript
fetch('/api/campaign/1/chart')
  .then(response => response.json())
  .then(data => {
    // Use with Chart.js, Plotly, or other charting library
    const chartData = {
      x: data.labels,
      y: data.values,
      type: 'bar'
    };
  });
```

---

### User Risk Analysis

#### GET /api/user_risks

Get risk scores for all users across all campaigns.

**Response:**
```json
[
  {
    "email": "john.doe@example.com",
    "risk_score": 65,
    "risk_level": "HIGH",
    "emails_opened": 2,
    "links_clicked": 1,
    "data_submitted": 1,
    "reported": 0,
    "campaigns_participated": 3
  },
  {
    "email": "jane.smith@example.com",
    "risk_score": 15,
    "risk_level": "LOW",
    "emails_opened": 1,
    "links_clicked": 0,
    "data_submitted": 0,
    "reported": 1,
    "campaigns_participated": 2
  }
]
```

**Risk Levels:**
- `NONE`: 0 points (no participation)
- `LOW`: 1-20 points
- `MEDIUM`: 21-50 points
- `HIGH`: 51+ points

**Risk Scoring:**
- Email opened: +10 points
- Link clicked: +25 points
- Data submitted: +40 points
- Email reported: -15 points

**Example:**
```bash
curl http://localhost:5000/api/user_risks
```

---

#### GET /api/user_risk/:email

Get risk score for a specific user.

**Parameters:**
- `email` (string, required): User email address (must be valid email format)

**Response:**
```json
{
  "email": "john.doe@example.com",
  "risk_score": 65,
  "risk_level": "HIGH",
  "emails_opened": 2,
  "links_clicked": 1,
  "data_submitted": 1,
  "reported": 0,
  "campaigns_participated": 3,
  "recent_campaigns": [
    {
      "campaign_id": 1,
      "campaign_name": "Q1 Security Test",
      "opened": true,
      "clicked": true,
      "submitted": false,
      "reported": false
    }
  ]
}
```

**Error Response:**
```json
// Invalid email format
{
  "error": "Validation failed",
  "details": ["Invalid email: must be a valid email"]
}

// User not found
{
  "error": "User not found",
  "details": "No data for email: nonexistent@example.com"
}
```

**Example:**
```bash
curl http://localhost:5000/api/user_risk/john.doe@example.com
```

---

### Dashboard Analytics

#### GET /api/dashboard_summary

Get aggregated statistics across all campaigns.

**Response:**
```json
{
  "total_campaigns": 8,
  "active_campaigns": 2,
  "completed_campaigns": 6,
  "total_users": 250,
  "high_risk_users": 35,
  "total_emails_sent": 1200,
  "overall_open_rate": 42.5,
  "overall_click_rate": 18.2,
  "overall_submit_rate": 6.4,
  "last_updated": "2025-01-14T15:30:00Z"
}
```

**Field Descriptions:**
- `total_campaigns`: All campaigns ever created
- `active_campaigns`: Currently running campaigns
- `completed_campaigns`: Finished campaigns
- `total_users`: Unique users across all campaigns
- `high_risk_users`: Users with HIGH risk level
- `overall_*_rate`: Aggregate metrics across all completed campaigns

**Example:**
```bash
curl http://localhost:5000/api/dashboard_summary
```

---

#### GET /api/risk_distribution

Get the distribution of users across risk levels.

**Response:**
```json
{
  "NONE": 45,
  "LOW": 128,
  "MEDIUM": 42,
  "HIGH": 35
}
```

**Example:**
```bash
curl http://localhost:5000/api/risk_distribution
```

**Pie Chart Example:**
```javascript
fetch('/api/risk_distribution')
  .then(response => response.json())
  .then(data => {
    const pieChart = {
      labels: Object.keys(data),
      values: Object.values(data),
      type: 'pie'
    };
  });
```

---

#### GET /api/campaign_trends

Get campaign performance trends over time.

**Response:**
```json
[
  {
    "campaign_name": "Q1 2025 Security Awareness",
    "launch_date": "2025-01-02T09:00:00Z",
    "click_rate": 22.67,
    "submit_rate": 8.0,
    "report_rate": 12.0
  },
  {
    "campaign_name": "Q2 2025 Executive Training",
    "launch_date": "2025-04-05T10:00:00Z",
    "click_rate": 18.5,
    "submit_rate": 5.2,
    "report_rate": 15.8
  }
]
```

**Use Case**: Track improvement in user awareness over time

**Example:**
```bash
curl http://localhost:5000/api/campaign_trends
```

---

## Code Examples

### Python

```python
import requests

# Base configuration
BASE_URL = "http://localhost:5000"
HEADERS = {"Content-Type": "application/json"}

# Get all campaigns
def get_campaigns():
    response = requests.get(f"{BASE_URL}/api/campaigns", headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Get user risk
def get_user_risk(email):
    response = requests.get(
        f"{BASE_URL}/api/user_risk/{email}",
        headers=HEADERS
    )
    return response.json()

# Get dashboard summary
def get_dashboard_summary():
    response = requests.get(
        f"{BASE_URL}/api/dashboard_summary",
        headers=HEADERS
    )
    return response.json()
```

### JavaScript

```javascript
const API_BASE = 'http://localhost:5000';

// Get all campaigns
async function getCampaigns() {
  const response = await fetch(`${API_BASE}/api/campaigns`);
  const data = await response.json();
  return data;
}

// Get campaign statistics
async function getCampaignStats(campaignId) {
  const response = await fetch(`${API_BASE}/api/campaign/${campaignId}/stats`);
  const data = await response.json();
  return data;
}

// Get user risks with error handling
async function getUserRisks() {
  try {
    const response = await fetch(`${API_BASE}/api/user_risks`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching user risks:', error);
    return [];
  }
}
```

### cURL

```bash
# Health check
curl http://localhost:5000/health

# Get all campaigns
curl http://localhost:5000/api/campaigns

# Get specific campaign
curl http://localhost:5000/api/campaign/1

# Get campaign stats
curl http://localhost:5000/api/campaign/1/stats

# Get user risks
curl http://localhost:5000/api/user_risks

# Get user risk by email
curl http://localhost:5000/api/user_risk/john.doe@example.com

# Get dashboard summary
curl http://localhost:5000/api/dashboard_summary

# Get risk distribution
curl http://localhost:5000/api/risk_distribution

# Get campaign trends
curl http://localhost:5000/api/campaign_trends
```

---

## WebSocket Support (Future)

**Planned for v1.4.0**: Real-time updates for campaign events

```javascript
const ws = new WebSocket('ws://localhost:5000/ws/campaign/1');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Real-time update:', data);
  // { type: 'email_opened', user: 'john@example.com', timestamp: '...' }
};
```

---

## Pagination (Future)

**Planned for v1.2.0**: Support for paginated results

```
GET /api/user_risks?page=1&per_page=50

Response:
{
  "data": [...],
  "pagination": {
    "page": 1,
    "per_page": 50,
    "total_items": 250,
    "total_pages": 5,
    "has_next": true,
    "has_prev": false
  }
}
```

---

## Filtering and Sorting (Future)

**Planned for v1.2.0**:

```
GET /api/campaigns?status=completed&sort_by=launch_date&order=desc
GET /api/user_risks?risk_level=HIGH&sort_by=risk_score&order=desc
```

---

## Changelog

### v1.1.0 (Current)
- Added input validation on all endpoints
- Added security headers
- Added rate limiting
- Improved error handling

### v1.0.0
- Initial API release
- Basic CRUD operations for campaigns
- User risk scoring
- Dashboard analytics

---

## Support

For API issues or questions:
- GitHub Issues: https://github.com/Raoof128/phishing-platform/issues
- Documentation: https://github.com/Raoof128/phishing-platform/docs

---

**Last Updated**: 2025-01-14
**API Version**: 1.1.0
