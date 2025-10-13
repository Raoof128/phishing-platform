#!/usr/bin/env python3
"""
Campaign Manager - GoPhish Campaign Automation
Handles campaign creation, scheduling, and management via GoPhish API
"""

import requests
import json
import yaml
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import urllib3

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_config(config_path: str) -> Dict:
    """
    Load configuration from YAML file

    Args:
        config_path: Path to configuration file

    Returns:
        Dictionary with configuration
    """
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {config_path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Error parsing configuration file: {e}")
        raise


class GophishCampaign:
    """
    Manages GoPhish campaigns via API
    Provides methods for creating, scheduling, and monitoring campaigns
    """
    
    def __init__(self, config_path: str = 'automation/config/api_config.yaml'):
        """
        Initialize GoPhish campaign manager
        
        Args:
            config_path: Path to API configuration file
        """
        self.config = self._load_config(config_path)
        self.api_key = self.config['gophish']['api_key']
        self.server_url = self.config['gophish']['server_url']
        self.verify_ssl = self.config['gophish']['verify_ssl']
        self.timeout = self.config['gophish']['timeout']
        
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        logger.info(f"Initialized GoPhish Campaign Manager for {self.server_url}")
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {config_path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Error parsing configuration file: {e}")
            raise
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> requests.Response:
        """
        Make HTTP request to GoPhish API
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            data: Request payload
            
        Returns:
            Response object
        """
        url = f"{self.server_url}/api/{endpoint}"
        
        try:
            if method == 'GET':
                response = requests.get(
                    url,
                    headers=self.headers,
                    verify=self.verify_ssl,
                    timeout=self.timeout
                )
            elif method == 'POST':
                response = requests.post(
                    url,
                    headers=self.headers,
                    json=data,
                    verify=self.verify_ssl,
                    timeout=self.timeout
                )
            elif method == 'PUT':
                response = requests.put(
                    url,
                    headers=self.headers,
                    json=data,
                    verify=self.verify_ssl,
                    timeout=self.timeout
                )
            elif method == 'DELETE':
                response = requests.delete(
                    url,
                    headers=self.headers,
                    verify=self.verify_ssl,
                    timeout=self.timeout
                )
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise
    
    def test_connection(self) -> bool:
        """
        Test connection to GoPhish API
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            response = self._make_request('GET', 'campaigns/')
            logger.info("✓ API connection successful")
            return True
        except Exception as e:
            logger.error(f"✗ API connection failed: {e}")
            return False
    
    def get_campaigns(self) -> List[Dict]:
        """
        Get all campaigns (alias for list_campaigns for compatibility)

        Returns:
            List of campaign dictionaries
        """
        return self.list_campaigns()

    def list_campaigns(self) -> List[Dict]:
        """
        List all campaigns

        Returns:
            List of campaign dictionaries
        """
        try:
            response = self._make_request('GET', 'campaigns/')
            campaigns = response.json()
            logger.info(f"Retrieved {len(campaigns)} campaigns")
            return campaigns
        except Exception as e:
            logger.error(f"Failed to list campaigns: {e}")
            return []
    
    def get_campaign(self, campaign_id: int) -> Optional[Dict]:
        """
        Get specific campaign details
        
        Args:
            campaign_id: Campaign ID
            
        Returns:
            Campaign dictionary or None
        """
        try:
            response = self._make_request('GET', f'campaigns/{campaign_id}')
            campaign = response.json()
            logger.info(f"Retrieved campaign: {campaign['name']}")
            return campaign
        except Exception as e:
            logger.error(f"Failed to get campaign {campaign_id}: {e}")
            return None
    
    def create_campaign(
        self,
        name: str,
        template_name: str,
        landing_page_name: str,
        smtp_name: str,
        group_name: str,
        launch_date: Optional[datetime] = None,
        send_by_date: Optional[datetime] = None,
        url: str = 'http://localhost'
    ) -> Optional[Dict]:
        """
        Create a new phishing campaign
        
        Args:
            name: Campaign name
            template_name: Email template name
            landing_page_name: Landing page name
            smtp_name: SMTP profile name
            group_name: Target group name
            launch_date: Campaign launch date/time
            send_by_date: Send all emails by this date/time
            url: Phishing URL
            
        Returns:
            Created campaign dictionary or None
        """
        # Default launch date to now + 5 minutes
        if launch_date is None:
            launch_date = datetime.now() + timedelta(minutes=5)
        
        # Default send_by_date to launch_date + 2 hours
        if send_by_date is None:
            send_by_date = launch_date + timedelta(hours=2)
        
        campaign_data = {
            'name': name,
            'template': {'name': template_name},
            'page': {'name': landing_page_name},
            'smtp': {'name': smtp_name},
            'groups': [{'name': group_name}],
            'url': url,
            'launch_date': launch_date.strftime('%Y-%m-%dT%H:%M:%S'),
            'send_by_date': send_by_date.strftime('%Y-%m-%dT%H:%M:%S')
        }
        
        try:
            response = self._make_request('POST', 'campaigns/', data=campaign_data)
            campaign = response.json()
            logger.info(f"✓ Created campaign: {name} (ID: {campaign.get('id')})")
            logger.info(f"  Launch Date: {launch_date}")
            logger.info(f"  Send By: {send_by_date}")
            return campaign
        except Exception as e:
            logger.error(f"✗ Failed to create campaign: {e}")
            return None
    
    def delete_campaign(self, campaign_id: int) -> bool:
        """
        Delete a campaign
        
        Args:
            campaign_id: Campaign ID to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._make_request('DELETE', f'campaigns/{campaign_id}')
            logger.info(f"✓ Deleted campaign ID: {campaign_id}")
            return True
        except Exception as e:
            logger.error(f"✗ Failed to delete campaign {campaign_id}: {e}")
            return False
    
    def get_campaign_results(self, campaign_id: int) -> Dict:
        """
        Get campaign results/metrics (alias for get_campaign_summary for compatibility)

        Args:
            campaign_id: Campaign ID

        Returns:
            Dictionary with campaign metrics
        """
        return self.get_campaign_summary(campaign_id)

    def get_campaign_summary(self, campaign_id: int) -> Dict:
        """
        Get campaign summary statistics

        Args:
            campaign_id: Campaign ID

        Returns:
            Dictionary with campaign statistics
        """
        campaign = self.get_campaign(campaign_id)
        if not campaign:
            return {}

        results = campaign.get('results', [])
        timeline = campaign.get('timeline', [])

        summary = {
            'campaign_id': campaign_id,
            'name': campaign['name'],
            'status': campaign['status'],
            'created_date': campaign['created_date'],
            'launch_date': campaign.get('launch_date', 'N/A'),
            'completed_date': campaign.get('completed_date', 'N/A'),
            'total_targets': len(results),
            'emails_sent': sum(1 for r in results if r['status'] != 'Error'),
            'emails_opened': sum(1 for r in results if r['status'] in ['Email Opened', 'Clicked Link', 'Submitted Data']),
            'links_clicked': sum(1 for r in results if r['status'] in ['Clicked Link', 'Submitted Data']),
            'data_submitted': sum(1 for r in results if r['status'] == 'Submitted Data'),
            'emails_reported': sum(1 for r in results if r['status'] == 'Email Reported'),
            'reported': sum(1 for r in results if r['status'] == 'Email Reported'),  # Add alias
            'errors': sum(1 for r in results if r['status'] == 'Error'),
        }

        # Calculate rates
        if summary['emails_sent'] > 0:
            summary['open_rate'] = round((summary['emails_opened'] / summary['emails_sent']) * 100, 2)
            summary['click_rate'] = round((summary['links_clicked'] / summary['emails_sent']) * 100, 2)
            summary['submission_rate'] = round((summary['data_submitted'] / summary['emails_sent']) * 100, 2)
            summary['submit_rate'] = summary['submission_rate']  # Add alias
            summary['report_rate'] = round((summary['emails_reported'] / summary['emails_sent']) * 100, 2)
        else:
            summary['open_rate'] = 0
            summary['click_rate'] = 0
            summary['submission_rate'] = 0
            summary['submit_rate'] = 0
            summary['report_rate'] = 0

        return summary
    
    def print_campaign_summary(self, campaign_id: int):
        """Print formatted campaign summary"""
        summary = self.get_campaign_summary(campaign_id)
        if not summary:
            print(f"Campaign {campaign_id} not found")
            return
        
        print(f"\n{'='*70}")
        print(f"Campaign Summary: {summary['name']}")
        print(f"{'='*70}")
        print(f"Status: {summary['status']}")
        print(f"Campaign ID: {summary['campaign_id']}")
        print(f"Launch Date: {summary['launch_date']}")
        print(f"\nTarget Statistics:")
        print(f"  Total Targets: {summary['total_targets']}")
        print(f"  Emails Sent: {summary['emails_sent']}")
        print(f"  Emails Opened: {summary['emails_opened']} ({summary['open_rate']:.1f}%)")
        print(f"  Links Clicked: {summary['links_clicked']} ({summary['click_rate']:.1f}%)")
        print(f"  Data Submitted: {summary['data_submitted']} ({summary['submission_rate']:.1f}%)")
        print(f"  Emails Reported: {summary['emails_reported']} ({summary['report_rate']:.1f}%)")
        print(f"  Errors: {summary['errors']}")
        print(f"{'='*70}\n")
    
    def list_templates(self) -> List[Dict]:
        """List all email templates"""
        try:
            response = self._make_request('GET', 'templates/')
            templates = response.json()
            logger.info(f"Retrieved {len(templates)} templates")
            return templates
        except Exception as e:
            logger.error(f"Failed to list templates: {e}")
            return []
    
    def list_landing_pages(self) -> List[Dict]:
        """List all landing pages"""
        try:
            response = self._make_request('GET', 'pages/')
            pages = response.json()
            logger.info(f"Retrieved {len(pages)} landing pages")
            return pages
        except Exception as e:
            logger.error(f"Failed to list landing pages: {e}")
            return []
    
    def list_groups(self) -> List[Dict]:
        """List all target groups"""
        try:
            response = self._make_request('GET', 'groups/')
            groups = response.json()
            logger.info(f"Retrieved {len(groups)} groups")
            return groups
        except Exception as e:
            logger.error(f"Failed to list groups: {e}")
            return []
    
    def list_smtp_profiles(self) -> List[Dict]:
        """List all SMTP profiles"""
        try:
            response = self._make_request('GET', 'smtp/')
            profiles = response.json()
            logger.info(f"Retrieved {len(profiles)} SMTP profiles")
            return profiles
        except Exception as e:
            logger.error(f"Failed to list SMTP profiles: {e}")
            return []


def main():
    """Command-line interface for campaign manager"""
    import argparse
    
    parser = argparse.ArgumentParser(description='GoPhish Campaign Manager')
    parser.add_argument('--test', action='store_true', help='Test API connection')
    parser.add_argument('--list-campaigns', action='store_true', help='List all campaigns')
    parser.add_argument('--campaign-id', type=int, help='Campaign ID for operations')
    parser.add_argument('--summary', action='store_true', help='Show campaign summary')
    parser.add_argument('--create', action='store_true', help='Create new campaign')
    parser.add_argument('--name', type=str, help='Campaign name')
    parser.add_argument('--template', type=str, help='Email template name')
    parser.add_argument('--landing-page', type=str, help='Landing page name')
    parser.add_argument('--smtp', type=str, help='SMTP profile name')
    parser.add_argument('--group', type=str, help='Target group name')
    parser.add_argument('--launch', type=str, help='Launch date/time (YYYY-MM-DD HH:MM)')
    parser.add_argument('--url', type=str, default='http://localhost', help='Phishing URL')
    parser.add_argument('--list-resources', action='store_true', help='List templates, pages, groups, SMTP')
    
    args = parser.parse_args()
    
    # Initialize campaign manager
    manager = GophishCampaign()
    
    if args.test:
        manager.test_connection()
    
    elif args.list_campaigns:
        campaigns = manager.list_campaigns()
        print(f"\n{'='*70}")
        print(f"Total Campaigns: {len(campaigns)}")
        print(f"{'='*70}")
        for camp in campaigns:
            print(f"[ID: {camp['id']}] {camp['name']} - Status: {camp['status']}")
        print(f"{'='*70}\n")
    
    elif args.summary and args.campaign_id:
        manager.print_campaign_summary(args.campaign_id)
    
    elif args.create:
        if not all([args.name, args.template, args.landing_page, args.smtp, args.group]):
            print("Error: --create requires --name, --template, --landing-page, --smtp, and --group")
            return
        
        launch_date = None
        if args.launch:
            try:
                launch_date = datetime.strptime(args.launch, '%Y-%m-%d %H:%M')
            except ValueError:
                print("Error: Invalid date format. Use YYYY-MM-DD HH:MM")
                return
        
        campaign = manager.create_campaign(
            name=args.name,
            template_name=args.template,
            landing_page_name=args.landing_page,
            smtp_name=args.smtp,
            group_name=args.group,
            launch_date=launch_date,
            url=args.url
        )
        
        if campaign:
            print(f"\n✓ Campaign created successfully!")
            print(f"  Campaign ID: {campaign.get('id')}")
            print(f"  Name: {campaign.get('name')}")
            print(f"  Status: {campaign.get('status')}\n")
    
    elif args.list_resources:
        print("\n" + "="*70)
        print("TEMPLATES")
        print("="*70)
        templates = manager.list_templates()
        for t in templates:
            print(f"  - {t['name']}")
        
        print("\n" + "="*70)
        print("LANDING PAGES")
        print("="*70)
        pages = manager.list_landing_pages()
        for p in pages:
            print(f"  - {p['name']}")
        
        print("\n" + "="*70)
        print("TARGET GROUPS")
        print("="*70)
        groups = manager.list_groups()
        for g in groups:
            print(f"  - {g['name']} ({len(g.get('targets', []))} targets)")
        
        print("\n" + "="*70)
        print("SMTP PROFILES")
        print("="*70)
        profiles = manager.list_smtp_profiles()
        for s in profiles:
            print(f"  - {s['name']} ({s.get('host', 'N/A')})")
        print("")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
