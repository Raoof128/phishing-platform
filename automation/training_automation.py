#!/usr/bin/env python3
"""
Training Automation - Automated Security Awareness Training
Assigns and tracks security training based on campaign performance
"""

import smtplib
import yaml
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import Dict, List
from pathlib import Path

from automation.analytics import PhishingAnalytics

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TrainingAutomation:
    """
    Automates security awareness training assignment and tracking
    """
    
    def __init__(self, config_path: str = 'automation/config/api_config.yaml'):
        """
        Initialize training automation
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.analytics = PhishingAnalytics(config_path)
        self.training_config = self.config['training']
        
        logger.info("Initialized TrainingAutomation")
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {config_path}")
            raise
    
    def assign_training_based_on_risk(self, email: str) -> List[str]:
        """
        Assign training modules based on user risk score
        
        Args:
            email: User email address
            
        Returns:
            List of assigned training module names
        """
        risk_info = self.analytics.calculate_user_risk_score(email)
        risk_score = risk_info['risk_score']
        
        # Get risk thresholds
        high_threshold = self.training_config['risk_thresholds']['high']
        medium_threshold = self.training_config['risk_thresholds']['medium']
        
        # Assign training modules
        if risk_score >= high_threshold:
            modules = self.training_config['training_modules']['high_risk']
            logger.info(f"Assigned HIGH risk training to {email} (score: {risk_score})")
        elif risk_score >= medium_threshold:
            modules = self.training_config['training_modules']['medium_risk']
            logger.info(f"Assigned MEDIUM risk training to {email} (score: {risk_score})")
        else:
            modules = self.training_config['training_modules']['low_risk']
            logger.info(f"Assigned LOW risk training to {email} (score: {risk_score})")
        
        return modules
    
    def send_training_email(
        self,
        recipient_email: str,
        recipient_name: str,
        training_modules: List[str],
        risk_score: int
    ) -> bool:
        """
        Send training assignment email
        
        Args:
            recipient_email: Recipient email address
            recipient_name: Recipient name
            training_modules: List of training modules
            risk_score: User risk score
            
        Returns:
            True if email sent successfully
        """
        try:
            # Load SMTP configuration
            smtp_config_path = 'automation/config/smtp_config.yaml'
            with open(smtp_config_path, 'r') as f:
                smtp_config = yaml.safe_load(f)
            
            # Get default SMTP profile
            default_profile = smtp_config['default_profile']
            profile = smtp_config['smtp_profiles'][default_profile]
            
            # Create email
            msg = MIMEMultipart('alternative')
            msg['Subject'] = 'Security Awareness Training Assignment'
            msg['From'] = f"{profile['from_name']} <{profile['from_address']}>"
            msg['To'] = recipient_email
            
            # Determine risk level
            if risk_score >= 70:
                risk_level = "High"
                risk_color = "#d32f2f"
            elif risk_score >= 40:
                risk_level = "Medium"
                risk_color = "#ff9800"
            else:
                risk_level = "Low"
                risk_color = "#4caf50"
            
            # Create HTML body
            modules_html = "".join([f"<li style='padding: 8px 0;'>{module}</li>" for module in training_modules])
            
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
                    .content {{ background: white; padding: 30px; border: 1px solid #ddd; border-top: none; }}
                    .risk-box {{ background-color: {risk_color}; color: white; padding: 15px; border-radius: 6px; margin: 20px 0; text-align: center; }}
                    .modules {{ background-color: #f5f5f5; padding: 20px; border-radius: 6px; margin: 20px 0; }}
                    .button {{ display: inline-block; background-color: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; margin: 20px 0; }}
                    .footer {{ text-align: center; padding: 20px; font-size: 12px; color: #666; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1 style="margin: 0;">Security Awareness Training</h1>
                        <p style="margin: 10px 0 0;">Required Training Assignment</p>
                    </div>
                    
                    <div class="content">
                        <p>Dear {recipient_name},</p>
                        
                        <p>Based on your recent participation in our security awareness program, you have been assigned personalized training modules to enhance your ability to recognize and respond to security threats.</p>
                        
                        <div class="risk-box">
                            <strong>Your Security Risk Level: {risk_level}</strong><br>
                            Risk Score: {risk_score}/100
                        </div>
                        
                        <h3>Assigned Training Modules:</h3>
                        <div class="modules">
                            <ul style="margin: 0; padding-left: 20px;">
                                {modules_html}
                            </ul>
                        </div>
                        
                        <p><strong>Completion Deadline:</strong> {(datetime.now() + timedelta(days=14)).strftime('%B %d, %Y')}</p>
                        
                        <p>These modules are specifically selected based on your interaction with simulated phishing emails. Completing this training will help you:</p>
                        <ul>
                            <li>Recognize phishing attempts and social engineering tactics</li>
                            <li>Protect sensitive company and personal information</li>
                            <li>Respond appropriately to suspicious emails and requests</li>
                            <li>Contribute to a more secure work environment</li>
                        </ul>
                        
                        <center>
                            <a href="#" class="button">Start Training Now</a>
                        </center>
                        
                        <p style="margin-top: 30px;">If you have any questions about this training assignment, please contact the Security Team at security@company.com.</p>
                        
                        <p>Best regards,<br>
                        <strong>Security Awareness Team</strong></p>
                    </div>
                    
                    <div class="footer">
                        <p>&copy; 2025 Security Awareness Training Program. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(html_body, 'html'))
            
            # Send email
            with smtplib.SMTP(profile['host'], profile['port']) as server:
                if profile.get('use_tls', True):
                    server.starttls()
                server.login(profile['username'], profile['password'])
                server.send_message(msg)
            
            logger.info(f"✓ Sent training email to {recipient_email}")
            return True
            
        except Exception as e:
            logger.error(f"✗ Failed to send training email to {recipient_email}: {e}")
            return False
    
    def process_campaign_training_assignments(self, campaign_id: int) -> Dict:
        """
        Process training assignments for all users in a campaign
        
        Args:
            campaign_id: Campaign ID
            
        Returns:
            Dictionary with assignment statistics
        """
        metrics = self.analytics.get_campaign_results(campaign_id)
        
        if not metrics:
            logger.error(f"Campaign {campaign_id} not found")
            return {}
        
        stats = {
            'campaign_id': campaign_id,
            'total_users': 0,
            'assignments_sent': 0,
            'assignments_failed': 0,
            'high_risk_users': 0,
            'medium_risk_users': 0,
            'low_risk_users': 0
        }
        
        # Process each user who interacted with campaign
        for result in metrics['results']:
            # Only assign training to users who clicked or submitted
            if result['status'] in ['Clicked Link', 'Submitted Data']:
                stats['total_users'] += 1
                
                email = result['email']
                name = f"{result['first_name']} {result['last_name']}"
                
                # Get risk score and assign training
                risk_info = self.analytics.calculate_user_risk_score(email)
                training_modules = self.assign_training_based_on_risk(email)
                
                # Track risk levels
                if risk_info['risk_level'] == 'High':
                    stats['high_risk_users'] += 1
                elif risk_info['risk_level'] == 'Medium':
                    stats['medium_risk_users'] += 1
                else:
                    stats['low_risk_users'] += 1
                
                # Send training email
                if self.send_training_email(email, name, training_modules, risk_info['risk_score']):
                    stats['assignments_sent'] += 1
                else:
                    stats['assignments_failed'] += 1
        
        logger.info(f"Processed training assignments for campaign {campaign_id}")
        logger.info(f"  Total users: {stats['total_users']}")
        logger.info(f"  Assignments sent: {stats['assignments_sent']}")
        logger.info(f"  High risk: {stats['high_risk_users']}, Medium: {stats['medium_risk_users']}, Low: {stats['low_risk_users']}")
        
        return stats
    
    def track_training_completion(self, email: str) -> Dict:
        """
        Track training completion for a user
        (Placeholder - would integrate with training platform)
        
        Args:
            email: User email
            
        Returns:
            Dictionary with completion status
        """
        # This would integrate with an actual training platform
        # For now, return placeholder data
        return {
            'email': email,
            'assigned_modules': [],
            'completed_modules': [],
            'completion_rate': 0,
            'last_activity': None
        }


def main():
    """Command-line interface for training automation"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Training Automation')
    parser.add_argument('--campaign-id', type=int, help='Process training for campaign')
    parser.add_argument('--auto-assign-by-risk', action='store_true', help='Auto-assign training based on risk')
    parser.add_argument('--user-email', type=str, help='User email for individual assignment')
    
    args = parser.parse_args()
    
    training = TrainingAutomation()
    
    if args.campaign_id:
        if args.auto_assign_by_risk:
            stats = training.process_campaign_training_assignments(args.campaign_id)
            
            print(f"\n{'='*70}")
            print(f"Training Assignment Summary - Campaign {args.campaign_id}")
            print(f"{'='*70}")
            print(f"Total Users Requiring Training: {stats['total_users']}")
            print(f"Assignments Sent: {stats['assignments_sent']}")
            print(f"Assignments Failed: {stats['assignments_failed']}")
            print(f"\nRisk Distribution:")
            print(f"  High Risk: {stats['high_risk_users']}")
            print(f"  Medium Risk: {stats['medium_risk_users']}")
            print(f"  Low Risk: {stats['low_risk_users']}")
            print(f"{'='*70}\n")
        else:
            print("Use --auto-assign-by-risk to automatically assign training")
    
    elif args.user_email:
        modules = training.assign_training_based_on_risk(args.user_email)
        print(f"\nAssigned training modules for {args.user_email}:")
        for module in modules:
            print(f"  - {module}")
        print()
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
