#!/usr/bin/env python3
"""
Analytics Module - Phishing Campaign Analytics and Reporting
Provides comprehensive analytics, visualization, and risk scoring
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import json
import yaml
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PhishingAnalytics:
    """
    Phishing campaign analytics and reporting
    Analyzes campaign data, generates reports, and calculates risk scores
    """
    
    def __init__(self, config_path: str = 'automation/config/api_config.yaml'):
        """
        Initialize analytics module
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.db_path = self.config['analytics']['gophish_db_path']
        self.reports_dir = Path(self.config['analytics']['reports_dir'])
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Initialized PhishingAnalytics with database: {self.db_path}")
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {config_path}")
            raise
    
    def _connect_db(self) -> sqlite3.Connection:
        """Connect to GoPhish database"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            logger.error(f"Database connection failed: {e}")
            raise
    
    def get_campaign_results(self, campaign_id: int) -> Dict:
        """
        Get detailed campaign results
        
        Args:
            campaign_id: Campaign ID
            
        Returns:
            Dictionary with campaign metrics
        """
        conn = self._connect_db()
        cursor = conn.cursor()
        
        try:
            # Get campaign info
            cursor.execute("""
                SELECT id, name, created_date, launch_date, completed_date, status
                FROM campaigns
                WHERE id = ?
            """, (campaign_id,))
            campaign = cursor.fetchone()
            
            if not campaign:
                logger.warning(f"Campaign {campaign_id} not found")
                return {}
            
            # Get results
            cursor.execute("""
                SELECT email, first_name, last_name, position, status, ip, latitude, longitude
                FROM results
                WHERE campaign_id = ?
            """, (campaign_id,))
            results = cursor.fetchall()
            
            # Get timeline events
            cursor.execute("""
                SELECT email, time, message, details
                FROM events
                WHERE campaign_id = ?
                ORDER BY time
            """, (campaign_id,))
            events = cursor.fetchall()
            
            # Calculate metrics
            total = len(results)
            sent = sum(1 for r in results if r['status'] not in ['Error', 'Scheduled'])
            opened = sum(1 for r in results if r['status'] in ['Email Opened', 'Clicked Link', 'Submitted Data'])
            clicked = sum(1 for r in results if r['status'] in ['Clicked Link', 'Submitted Data'])
            submitted = sum(1 for r in results if r['status'] == 'Submitted Data')
            reported = sum(1 for r in results if r['status'] == 'Email Reported')
            
            metrics = {
                'campaign_id': campaign['id'],
                'name': campaign['name'],
                'status': campaign['status'],
                'created_date': campaign['created_date'],
                'launch_date': campaign['launch_date'],
                'completed_date': campaign['completed_date'],
                'total_targets': total,
                'emails_sent': sent,
                'emails_opened': opened,
                'links_clicked': clicked,
                'data_submitted': submitted,
                'emails_reported': reported,
                'open_rate': (opened / sent * 100) if sent > 0 else 0,
                'click_rate': (clicked / sent * 100) if sent > 0 else 0,
                'submission_rate': (submitted / sent * 100) if sent > 0 else 0,
                'report_rate': (reported / sent * 100) if sent > 0 else 0,
                'results': [dict(r) for r in results],
                'events': [dict(e) for e in events]
            }
            
            return metrics
            
        finally:
            conn.close()
    
    def calculate_risk_score(self, email: str) -> Tuple[int, Dict]:
        """
        Calculate risk score for a user (returns tuple for compatibility)

        Args:
            email: User email address

        Returns:
            Tuple of (risk_score, details_dict)
        """
        result = self.calculate_user_risk_score(email)
        return result['risk_score'], result

    def calculate_user_risk_score(self, email: str) -> Dict:
        """
        Calculate risk score for a user based on historical behavior

        Args:
            email: User email address

        Returns:
            Dictionary with risk score and details
        """
        conn = self._connect_db()
        cursor = conn.cursor()
        
        try:
            # Get user's campaign history
            cursor.execute("""
                SELECT c.id, c.name, r.status
                FROM results r
                JOIN campaigns c ON r.campaign_id = c.id
                WHERE r.email = ?
            """, (email,))
            history = cursor.fetchall()
            
            if not history:
                return {
                    'email': email,
                    'risk_score': 0,
                    'risk_level': 'Unknown',
                    'campaigns_participated': 0,
                    'details': 'No campaign history'
                }
            
            # Calculate risk factors
            total_campaigns = len(history)
            opened_count = sum(1 for h in history if h['status'] in ['Email Opened', 'Clicked Link', 'Submitted Data'])
            clicked_count = sum(1 for h in history if h['status'] in ['Clicked Link', 'Submitted Data'])
            submitted_count = sum(1 for h in history if h['status'] == 'Submitted Data')
            reported_count = sum(1 for h in history if h['status'] == 'Email Reported')
            
            # Risk scoring algorithm
            # Higher score = higher risk
            risk_score = 0
            
            # Email opened (10 points each)
            risk_score += opened_count * 10
            
            # Link clicked (25 points each)
            risk_score += clicked_count * 25
            
            # Data submitted (40 points each)
            risk_score += submitted_count * 40
            
            # Email reported (-15 points each, reduces risk)
            risk_score -= reported_count * 15
            
            # Cap risk score at 0-100
            risk_score = max(0, min(100, risk_score))
            
            # Determine risk level
            if risk_score >= 70:
                risk_level = 'High'
            elif risk_score >= 40:
                risk_level = 'Medium'
            elif risk_score > 0:
                risk_level = 'Low'
            else:
                risk_level = 'Minimal'
            
            return {
                'email': email,
                'risk_score': risk_score,
                'risk_level': risk_level,
                'campaigns_participated': total_campaigns,
                'emails_opened': opened_count,
                'links_clicked': clicked_count,
                'data_submitted': submitted_count,
                'emails_reported': reported_count,
                'details': f'Participated in {total_campaigns} campaigns'
            }
            
        finally:
            conn.close()
    
    def get_all_user_risks(self) -> pd.DataFrame:
        """
        Get risk scores for all users (alias for compatibility)

        Returns:
            DataFrame with user risk scores
        """
        return self.get_all_users_risk_scores()

    def get_all_users_risk_scores(self) -> pd.DataFrame:
        """
        Calculate risk scores for all users

        Returns:
            DataFrame with user risk scores
        """
        conn = self._connect_db()
        cursor = conn.cursor()
        
        try:
            # Get all unique users
            cursor.execute("SELECT DISTINCT email FROM results")
            users = [row['email'] for row in cursor.fetchall()]
            
            # Calculate risk for each user
            risk_data = []
            for email in users:
                risk_info = self.calculate_user_risk_score(email)
                risk_data.append(risk_info)
            
            df = pd.DataFrame(risk_data)
            df = df.sort_values('risk_score', ascending=False)
            
            return df
            
        finally:
            conn.close()
    
    def generate_campaign_report(self, campaign_id: int, output_format: str = 'html') -> str:
        """
        Generate comprehensive campaign report
        
        Args:
            campaign_id: Campaign ID
            output_format: Report format (html, pdf, csv)
            
        Returns:
            Path to generated report
        """
        metrics = self.get_campaign_results(campaign_id)
        
        if not metrics:
            logger.error(f"No data found for campaign {campaign_id}")
            return ""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_name = f"campaign_{campaign_id}_{timestamp}"
        
        if output_format == 'html':
            return self._generate_html_report(metrics, report_name)
        elif output_format == 'csv':
            return self._generate_csv_report(metrics, report_name)
        else:
            logger.warning(f"Unsupported format: {output_format}")
            return ""
    
    def _generate_html_report(self, metrics: Dict, report_name: str) -> str:
        """Generate HTML report"""
        report_path = self.reports_dir / f"{report_name}.html"
        
        # Create visualizations
        fig1 = self._create_metrics_chart(metrics)
        fig2 = self._create_timeline_chart(metrics)
        
        # Generate HTML
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Campaign Report - {metrics['name']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; }}
                h1 {{ color: #333; border-bottom: 3px solid #667eea; padding-bottom: 10px; }}
                .metric-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0; }}
                .metric-box {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; }}
                .metric-value {{ font-size: 36px; font-weight: bold; margin: 10px 0; }}
                .metric-label {{ font-size: 14px; opacity: 0.9; }}
                .chart-container {{ margin: 30px 0; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #667eea; color: white; }}
                tr:hover {{ background-color: #f5f5f5; }}
            </style>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        </head>
        <body>
            <div class="container">
                <h1>Campaign Report: {metrics['name']}</h1>
                <p><strong>Campaign ID:</strong> {metrics['campaign_id']}</p>
                <p><strong>Status:</strong> {metrics['status']}</p>
                <p><strong>Launch Date:</strong> {metrics['launch_date']}</p>
                <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                
                <h2>Key Metrics</h2>
                <div class="metric-grid">
                    <div class="metric-box">
                        <div class="metric-label">Emails Sent</div>
                        <div class="metric-value">{metrics['emails_sent']}</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">Opened</div>
                        <div class="metric-value">{metrics['emails_opened']}</div>
                        <div class="metric-label">{metrics['open_rate']:.1f}%</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">Clicked</div>
                        <div class="metric-value">{metrics['links_clicked']}</div>
                        <div class="metric-label">{metrics['click_rate']:.1f}%</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">Submitted</div>
                        <div class="metric-value">{metrics['data_submitted']}</div>
                        <div class="metric-label">{metrics['submission_rate']:.1f}%</div>
                    </div>
                </div>
                
                <div class="chart-container">
                    <h2>Campaign Performance</h2>
                    {fig1.to_html(full_html=False, include_plotlyjs=False)}
                </div>
                
                <h2>Individual Results</h2>
                <table>
                    <tr>
                        <th>Email</th>
                        <th>Name</th>
                        <th>Status</th>
                        <th>Location</th>
                    </tr>
        """
        
        for result in metrics['results'][:50]:  # Limit to 50 results
            html_content += f"""
                    <tr>
                        <td>{result['email']}</td>
                        <td>{result['first_name']} {result['last_name']}</td>
                        <td>{result['status']}</td>
                        <td>{result.get('ip', 'N/A')}</td>
                    </tr>
            """
        
        html_content += """
                </table>
            </div>
        </body>
        </html>
        """
        
        with open(report_path, 'w') as f:
            f.write(html_content)
        
        logger.info(f"Generated HTML report: {report_path}")
        return str(report_path)
    
    def _generate_csv_report(self, metrics: Dict, report_name: str) -> str:
        """Generate CSV report"""
        report_path = self.reports_dir / f"{report_name}.csv"
        
        df = pd.DataFrame(metrics['results'])
        df.to_csv(report_path, index=False)
        
        logger.info(f"Generated CSV report: {report_path}")
        return str(report_path)
    
    def _create_metrics_chart(self, metrics: Dict) -> go.Figure:
        """Create metrics visualization"""
        categories = ['Sent', 'Opened', 'Clicked', 'Submitted', 'Reported']
        values = [
            metrics['emails_sent'],
            metrics['emails_opened'],
            metrics['links_clicked'],
            metrics['data_submitted'],
            metrics['emails_reported']
        ]
        
        fig = go.Figure(data=[
            go.Bar(x=categories, y=values, marker_color=['#667eea', '#ffc107', '#ff6b6b', '#ee5a6f', '#51cf66'])
        ])
        
        fig.update_layout(
            title='Campaign Metrics Overview',
            xaxis_title='Metric',
            yaxis_title='Count',
            height=400
        )
        
        return fig
    
    def _create_timeline_chart(self, metrics: Dict) -> go.Figure:
        """Create timeline visualization"""
        # This would create a timeline chart from events
        # Simplified version for now
        fig = go.Figure()
        fig.update_layout(title='Campaign Timeline', height=300)
        return fig
    
    def print_risk_summary(self):
        """Print summary of user risk scores"""
        df = self.get_all_users_risk_scores()
        
        print("\n" + "="*80)
        print("USER RISK SUMMARY")
        print("="*80)
        print(f"Total Users: {len(df)}")
        print(f"High Risk: {len(df[df['risk_level'] == 'High'])}")
        print(f"Medium Risk: {len(df[df['risk_level'] == 'Medium'])}")
        print(f"Low Risk: {len(df[df['risk_level'] == 'Low'])}")
        print("\nTop 10 High-Risk Users:")
        print("-"*80)
        
        for idx, row in df.head(10).iterrows():
            print(f"{row['email']:40} Risk: {row['risk_score']:3.0f} ({row['risk_level']:6}) - {row['campaigns_participated']} campaigns")
        
        print("="*80 + "\n")


def main():
    """Command-line interface for analytics"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Phishing Campaign Analytics')
    parser.add_argument('--campaign-id', type=int, help='Campaign ID for analysis')
    parser.add_argument('--output', type=str, default='report.html', help='Output file path')
    parser.add_argument('--format', type=str, default='html', choices=['html', 'csv'], help='Report format')
    parser.add_argument('--risk-summary', action='store_true', help='Show user risk summary')
    parser.add_argument('--user-risk', type=str, help='Calculate risk for specific user email')
    
    args = parser.parse_args()
    
    analytics = PhishingAnalytics()
    
    if args.campaign_id:
        report_path = analytics.generate_campaign_report(args.campaign_id, args.format)
        print(f"\n✓ Report generated: {report_path}\n")
    
    elif args.risk_summary:
        analytics.print_risk_summary()
    
    elif args.user_risk:
        risk = analytics.calculate_user_risk_score(args.user_risk)
        print(f"\nRisk Assessment for {risk['email']}:")
        print(f"  Risk Score: {risk['risk_score']}/100")
        print(f"  Risk Level: {risk['risk_level']}")
        print(f"  Campaigns: {risk['campaigns_participated']}")
        print(f"  Opened: {risk['emails_opened']}, Clicked: {risk['links_clicked']}, Submitted: {risk['data_submitted']}\n")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
