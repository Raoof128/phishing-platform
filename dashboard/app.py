#!/usr/bin/env python3
"""
Analytics Dashboard for Phishing Platform

Flask web application providing real-time analytics and visualizations
for phishing campaigns.
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from automation.campaign_manager import GophishCampaign
from automation.analytics import PhishingAnalytics
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta


app = Flask(__name__)
CORS(app)

# Configuration
CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'automation', 'config', 'api_config.yaml')

# Initialize components
try:
    campaign_api = GophishCampaign(config_path=CONFIG_PATH)
    analytics = PhishingAnalytics(config_path=CONFIG_PATH)

except Exception as e:
    print(f"Warning: Could not initialize API connections: {e}")
    campaign_api = None
    analytics = None


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')


@app.route('/api/campaigns')
def get_campaigns():
    """Get all campaigns"""
    try:
        if not campaign_api:
            return jsonify({'error': 'API not configured'}), 500

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

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/campaign/<int:campaign_id>')
def get_campaign(campaign_id):
    """Get specific campaign details"""
    try:
        if not campaign_api:
            return jsonify({'error': 'API not configured'}), 500

        campaign = campaign_api.get_campaign(campaign_id)
        return jsonify(campaign)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/campaign/<int:campaign_id>/stats')
def get_campaign_stats(campaign_id):
    """Get campaign statistics"""
    try:
        if not campaign_api:
            return jsonify({'error': 'API not configured'}), 500

        metrics = campaign_api.get_campaign_results(campaign_id)
        return jsonify(metrics)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/campaign/<int:campaign_id>/chart')
def get_campaign_chart(campaign_id):
    """Get campaign results as chart data"""
    try:
        if not campaign_api:
            return jsonify({'error': 'API not configured'}), 500

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

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/user_risks')
def get_user_risks():
    """Get risk scores for all users"""
    try:
        if not analytics:
            return jsonify({'error': 'Analytics not configured'}), 500

        df = analytics.get_all_user_risks()

        # Convert to dict for JSON
        users = df.to_dict('records')

        return jsonify(users)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/user_risk/<email>')
def get_user_risk(email):
    """Get risk score for specific user"""
    try:
        if not analytics:
            return jsonify({'error': 'Analytics not configured'}), 500

        score, details = analytics.calculate_risk_score(email)
        return jsonify(details)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/dashboard_summary')
def get_dashboard_summary():
    """Get overall dashboard summary statistics"""
    try:
        if not campaign_api or not analytics:
            return jsonify({'error': 'Services not configured'}), 500

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

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/risk_distribution')
def get_risk_distribution():
    """Get distribution of user risk levels"""
    try:
        if not analytics:
            return jsonify({'error': 'Analytics not configured'}), 500

        df = analytics.get_all_user_risks()

        # Count by risk level
        distribution = df['risk_level'].value_counts().to_dict()

        # Ensure all levels are present
        for level in ['NONE', 'LOW', 'MEDIUM', 'HIGH']:
            if level not in distribution:
                distribution[level] = 0

        return jsonify(distribution)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/campaign_trends')
def get_campaign_trends():
    """Get campaign performance trends over time"""
    try:
        if not campaign_api:
            return jsonify({'error': 'API not configured'}), 500

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

    except Exception as e:
        return jsonify({'error': str(e)}), 500


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
