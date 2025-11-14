#!/usr/bin/env python3
"""
Analytics Dashboard for Phishing Platform

Flask web application providing real-time analytics and visualizations
for phishing campaigns.
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import sys
import os
import logging
from functools import wraps
from typing import Any, Callable

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from automation.campaign_manager import GophishCampaign
from automation.analytics import PhishingAnalytics
from automation.constants import (
    RATE_LIMIT_REQUESTS_PER_MINUTE,
    RATE_LIMIT_REQUESTS_PER_HOUR
)
from automation.validation import (
    validate_path_param,
    validate_request_args,
    sanitize_string
)
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Security configurations
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max request size

# Security headers middleware
@app.after_request
def add_security_headers(response):
    """Add security headers to all responses"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdn.plot.ly https://cdnjs.cloudflare.com; style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; img-src 'self' data:; font-src 'self' https://cdnjs.cloudflare.com;"
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    return response

# CORS with restricted origins (configure based on your needs)
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:*", "http://127.0.0.1:*"],
        "methods": ["GET", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=[
        f"{RATE_LIMIT_REQUESTS_PER_MINUTE} per minute",
        f"{RATE_LIMIT_REQUESTS_PER_HOUR} per hour"
    ],
    storage_uri="memory://"
)

# Configuration
CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'automation', 'config', 'api_config.yaml')

# Initialize components
try:
    campaign_api = GophishCampaign(config_path=CONFIG_PATH)
    analytics = PhishingAnalytics(config_path=CONFIG_PATH)
    logger.info("Successfully initialized API components")
except Exception as e:
    logger.error(f"Could not initialize API connections: {e}")
    campaign_api = None
    analytics = None


# Helper decorators and functions
def handle_api_errors(f: Callable) -> Callable:
    """
    Decorator to handle API errors consistently

    Args:
        f: Function to wrap

    Returns:
        Wrapped function with error handling
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {f.__name__}: {str(e)}", exc_info=True)
            return jsonify({
                'error': 'An error occurred processing your request',
                'details': str(e) if app.debug else None
            }), 500
    return decorated_function


def require_initialized_services(f: Callable) -> Callable:
    """
    Decorator to ensure services are initialized

    Args:
        f: Function to wrap

    Returns:
        Wrapped function with service check
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not campaign_api or not analytics:
            logger.warning("Attempted to access API endpoint with uninitialized services")
            return jsonify({
                'error': 'Services not initialized',
                'message': 'API components are not properly configured'
            }), 503
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')


@app.route('/health')
@limiter.exempt
def health_check():
    """
    Health check endpoint for monitoring

    Returns:
        JSON response with service status
    """
    status = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'services': {
            'campaign_api': campaign_api is not None,
            'analytics': analytics is not None
        }
    }

    # Overall health based on service availability
    all_healthy = all(status['services'].values())
    status_code = 200 if all_healthy else 503

    if not all_healthy:
        status['status'] = 'unhealthy'
        logger.warning("Health check failed - some services unavailable")

    return jsonify(status), status_code


@app.route('/api/campaigns')
@handle_api_errors
@require_initialized_services
def get_campaigns():
    """Get all campaigns"""
    campaigns = campaign_api.get_campaigns()

    # Simplify response
    result = []
    for c in campaigns:
        result.append({
            'id': c['id'],
            'name': c['name'],
            'status': c['status'],
            'created_date': c['created_date'],
            'launch_date': c.get('launch_date'),
            'completed_date': c.get('completed_date')
        })

    return jsonify(result)


@app.route('/api/campaign/<int:campaign_id>')
@handle_api_errors
@require_initialized_services
@validate_path_param('campaign_id', 'integer', min_val=1)
def get_campaign(campaign_id: int):
    """Get specific campaign details"""
    campaign = campaign_api.get_campaign(campaign_id)
    return jsonify(campaign)


@app.route('/api/campaign/<int:campaign_id>/stats')
@handle_api_errors
@require_initialized_services
@validate_path_param('campaign_id', 'integer', min_val=1)
def get_campaign_stats(campaign_id: int):
    """Get campaign statistics"""
    metrics = campaign_api.get_campaign_results(campaign_id)
    return jsonify(metrics)


@app.route('/api/campaign/<int:campaign_id>/chart')
@handle_api_errors
@require_initialized_services
@validate_path_param('campaign_id', 'integer', min_val=1)
def get_campaign_chart(campaign_id: int):
    """Get campaign results as chart data"""
    metrics = campaign_api.get_campaign_results(campaign_id)

    # Create chart data
    chart_data = {
        'labels': ['Sent', 'Opened', 'Clicked', 'Submitted', 'Reported'],
        'values': [
            metrics['emails_sent'],
            metrics['emails_opened'],
            metrics['links_clicked'],
            metrics['data_submitted'],
            metrics['reported']
        ],
        'percentages': [
            100,
            metrics.get('open_rate', 0),
            metrics.get('click_rate', 0),
            metrics.get('submit_rate', 0),
            metrics.get('report_rate', 0)
        ]
    }

    return jsonify(chart_data)


@app.route('/api/user_risks')
@handle_api_errors
@require_initialized_services
def get_user_risks():
    """Get risk scores for all users"""
    df = analytics.get_all_user_risks()

    # Convert to dict for JSON
    users = df.to_dict('records')

    return jsonify(users)


@app.route('/api/user_risk/<email>')
@handle_api_errors
@require_initialized_services
@validate_path_param('email', 'email')
def get_user_risk(email: str):
    """Get risk score for specific user"""
    # Sanitize email to prevent injection
    email = sanitize_string(email, max_length=255)
    score, details = analytics.calculate_risk_score(email)
    return jsonify(details)


@app.route('/api/dashboard_summary')
@handle_api_errors
@require_initialized_services
def get_dashboard_summary():
    """Get overall dashboard summary statistics"""
    # Get all campaigns
    campaigns = campaign_api.get_campaigns()

    # Calculate overall stats
    total_campaigns = len(campaigns)
    active_campaigns = len([c for c in campaigns if c['status'] == 'In progress'])
    completed_campaigns = len([c for c in campaigns if c['status'] == 'Completed'])

    # Get user count
    df_users = analytics.get_all_user_risks()
    total_users = len(df_users)
    high_risk_users = len(df_users[df_users['risk_level'] == 'HIGH'])

    # Calculate aggregate metrics from all completed campaigns
    total_sent = 0
    total_opened = 0
    total_clicked = 0
    total_submitted = 0

    for campaign in campaigns:
        if campaign['status'] == 'Completed':
            try:
                metrics = campaign_api.get_campaign_results(campaign['id'])
                total_sent += metrics.get('emails_sent', 0)
                total_opened += metrics.get('emails_opened', 0)
                total_clicked += metrics.get('links_clicked', 0)
                total_submitted += metrics.get('data_submitted', 0)
            except:
                continue

    # Calculate overall rates
    overall_open_rate = round((total_opened / total_sent * 100), 2) if total_sent > 0 else 0
    overall_click_rate = round((total_clicked / total_sent * 100), 2) if total_sent > 0 else 0
    overall_submit_rate = round((total_submitted / total_sent * 100), 2) if total_sent > 0 else 0

    summary = {
        'total_campaigns': total_campaigns,
        'active_campaigns': active_campaigns,
        'completed_campaigns': completed_campaigns,
        'total_users': total_users,
        'high_risk_users': high_risk_users,
        'total_emails_sent': total_sent,
        'overall_open_rate': overall_open_rate,
        'overall_click_rate': overall_click_rate,
        'overall_submit_rate': overall_submit_rate,
        'last_updated': datetime.now().isoformat()
    }

    return jsonify(summary)


@app.route('/api/risk_distribution')
@handle_api_errors
@require_initialized_services
def get_risk_distribution():
    """Get distribution of user risk levels"""
    df = analytics.get_all_user_risks()

    # Count by risk level
    distribution = df['risk_level'].value_counts().to_dict()

    # Ensure all levels are present
    for level in ['NONE', 'LOW', 'MEDIUM', 'HIGH']:
        if level not in distribution:
            distribution[level] = 0

    return jsonify(distribution)


@app.route('/api/campaign_trends')
@handle_api_errors
@require_initialized_services
def get_campaign_trends():
    """Get campaign performance trends over time"""
    campaigns = campaign_api.get_campaigns()

    trends = []
    for campaign in sorted(campaigns, key=lambda x: x.get('launch_date', '')):
        if campaign['status'] == 'Completed' and campaign.get('launch_date'):
            try:
                metrics = campaign_api.get_campaign_results(campaign['id'])

                trends.append({
                    'campaign_name': campaign['name'],
                    'launch_date': campaign['launch_date'],
                    'click_rate': metrics.get('click_rate', 0),
                    'submit_rate': metrics.get('submit_rate', 0),
                    'report_rate': metrics.get('report_rate', 0)
                })
            except:
                continue

    return jsonify(trends)


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Get configuration from environment or config file
    try:
        import yaml
        with open(CONFIG_PATH, 'r') as f:
            config = yaml.safe_load(f)

        # Check both old and new config format
        if 'platform' in config:
            platform_config = config.get('platform', {})
            host = platform_config.get('dashboard_host', '0.0.0.0')
            port = platform_config.get('dashboard_port', 5000)
        else:
            host = '0.0.0.0'
            port = 5000
    except:
        host = '0.0.0.0'
        port = 5000

    print(f"\n{'='*60}")
    print(f"Phishing Platform Analytics Dashboard")
    print(f"{'='*60}")
    print(f"Starting server at http://{host}:{port}")
    print(f"Press Ctrl+C to stop")
    print(f"{'='*60}\n")

    app.run(host=host, port=port, debug=True)
