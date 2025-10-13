#!/usr/bin/env python3
"""
User Import - Import and manage target users/groups
Handles CSV import and GoPhish group management
"""

import csv
import yaml
import logging
import requests
import re
from typing import List, Dict, Optional
from pathlib import Path
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class UserImporter:
    """
    Imports users from CSV and creates GoPhish groups
    """
    
    def __init__(self, config_path: str = 'automation/config/api_config.yaml'):
        """
        Initialize user importer
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.api_key = self.config['gophish']['api_key']
        self.server_url = self.config['gophish']['server_url']
        self.verify_ssl = self.config['gophish']['verify_ssl']
        self.import_config = self.config['user_import']
        
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        logger.info("Initialized UserImporter")
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {config_path}")
            raise
    
    def validate_email(self, email: str) -> bool:
        """
        Validate email address format
        
        Args:
            email: Email address to validate
            
        Returns:
            True if valid email format
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def import_users_from_csv(self, csv_file: str) -> List[Dict]:
        """
        Import users from CSV file
        
        Args:
            csv_file: Path to CSV file
            
        Returns:
            List of user dictionaries
        """
        users = []
        column_mapping = self.import_config['csv_columns']
        validate_emails = self.import_config['validate_emails']
        skip_invalid = self.import_config['skip_invalid']
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row_num, row in enumerate(reader, start=2):
                    try:
                        # Extract user data using column mapping
                        user = {
                            'email': row.get(column_mapping['email'], '').strip(),
                            'first_name': row.get(column_mapping['first_name'], '').strip(),
                            'last_name': row.get(column_mapping['last_name'], '').strip(),
                            'position': row.get(column_mapping['position'], '').strip()
                        }
                        
                        # Validate email if required
                        if validate_emails and not self.validate_email(user['email']):
                            logger.warning(f"Invalid email at row {row_num}: {user['email']}")
                            if skip_invalid:
                                continue
                        
                        # Check required fields
                        if not user['email']:
                            logger.warning(f"Missing email at row {row_num}")
                            if skip_invalid:
                                continue
                        
                        users.append(user)
                        
                    except Exception as e:
                        logger.error(f"Error processing row {row_num}: {e}")
                        if not skip_invalid:
                            raise
            
            logger.info(f"Imported {len(users)} users from {csv_file}")
            return users
            
        except FileNotFoundError:
            logger.error(f"CSV file not found: {csv_file}")
            return []
        except Exception as e:
            logger.error(f"Error reading CSV file: {e}")
            return []
    
    def create_group(self, group_name: str, users: List[Dict]) -> Optional[Dict]:
        """
        Create GoPhish group with users
        
        Args:
            group_name: Name for the group
            users: List of user dictionaries
            
        Returns:
            Created group dictionary or None
        """
        # Format users for GoPhish API
        targets = []
        for user in users:
            target = {
                'email': user['email'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'position': user['position']
            }
            targets.append(target)
        
        group_data = {
            'name': group_name,
            'targets': targets
        }
        
        try:
            response = requests.post(
                f"{self.server_url}/api/groups/",
                headers=self.headers,
                json=group_data,
                verify=self.verify_ssl
            )
            response.raise_for_status()
            
            group = response.json()
            logger.info(f"✓ Created group '{group_name}' with {len(targets)} users")
            return group
            
        except requests.exceptions.RequestException as e:
            logger.error(f"✗ Failed to create group: {e}")
            return None
    
    def get_group_by_name(self, group_name: str) -> Optional[Dict]:
        """
        Get group by name
        
        Args:
            group_name: Group name
            
        Returns:
            Group dictionary or None
        """
        try:
            response = requests.get(
                f"{self.server_url}/api/groups/",
                headers=self.headers,
                verify=self.verify_ssl
            )
            response.raise_for_status()
            
            groups = response.json()
            for group in groups:
                if group['name'] == group_name:
                    return group
            
            return None
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching groups: {e}")
            return None
    
    def update_group(self, group_id: int, users: List[Dict]) -> bool:
        """
        Update existing group with new users
        
        Args:
            group_id: Group ID
            users: List of user dictionaries
            
        Returns:
            True if successful
        """
        targets = []
        for user in users:
            target = {
                'email': user['email'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'position': user['position']
            }
            targets.append(target)
        
        try:
            # Get existing group
            response = requests.get(
                f"{self.server_url}/api/groups/{group_id}",
                headers=self.headers,
                verify=self.verify_ssl
            )
            response.raise_for_status()
            group = response.json()
            
            # Update targets
            group['targets'] = targets
            
            # Save updated group
            response = requests.put(
                f"{self.server_url}/api/groups/{group_id}",
                headers=self.headers,
                json=group,
                verify=self.verify_ssl
            )
            response.raise_for_status()
            
            logger.info(f"✓ Updated group ID {group_id} with {len(targets)} users")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"✗ Failed to update group: {e}")
            return False
    
    def import_and_create_group(self, csv_file: str, group_name: str, update_existing: bool = False) -> bool:
        """
        Import users from CSV and create/update GoPhish group
        
        Args:
            csv_file: Path to CSV file
            group_name: Name for the group
            update_existing: Update group if it already exists
            
        Returns:
            True if successful
        """
        # Import users
        users = self.import_users_from_csv(csv_file)
        
        if not users:
            logger.error("No users to import")
            return False
        
        # Check if group exists
        existing_group = self.get_group_by_name(group_name)
        
        if existing_group:
            if update_existing:
                logger.info(f"Group '{group_name}' exists, updating...")
                return self.update_group(existing_group['id'], users)
            else:
                logger.warning(f"Group '{group_name}' already exists. Use --update to update it.")
                return False
        else:
            # Create new group
            group = self.create_group(group_name, users)
            return group is not None
    
    def list_groups(self):
        """List all groups"""
        try:
            response = requests.get(
                f"{self.server_url}/api/groups/",
                headers=self.headers,
                verify=self.verify_ssl
            )
            response.raise_for_status()
            
            groups = response.json()
            
            print(f"\n{'='*70}")
            print(f"GoPhish Groups ({len(groups)} total)")
            print(f"{'='*70}")
            
            for group in groups:
                target_count = len(group.get('targets', []))
                modified = group.get('modified_date', 'N/A')
                print(f"[ID: {group['id']:3}] {group['name']:30} ({target_count:4} targets) - Modified: {modified}")
            
            print(f"{'='*70}\n")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching groups: {e}")


def main():
    """Command-line interface for user import"""
    import argparse
    
    parser = argparse.ArgumentParser(description='User Import and Group Management')
    parser.add_argument('--csv', type=str, help='CSV file to import')
    parser.add_argument('--group', type=str, help='Group name')
    parser.add_argument('--update', action='store_true', help='Update existing group')
    parser.add_argument('--list-groups', action='store_true', help='List all groups')
    parser.add_argument('--create-sample-csv', type=str, help='Create sample CSV file')
    
    args = parser.parse_args()
    
    importer = UserImporter()
    
    if args.list_groups:
        importer.list_groups()
    
    elif args.create_sample_csv:
        # Create sample CSV
        sample_data = [
            ['email', 'first_name', 'last_name', 'position'],
            ['john.doe@company.com', 'John', 'Doe', 'Software Engineer'],
            ['jane.smith@company.com', 'Jane', 'Smith', 'Marketing Manager'],
            ['bob.jones@company.com', 'Bob', 'Jones', 'Sales Representative'],
            ['alice.wilson@company.com', 'Alice', 'Wilson', 'HR Coordinator'],
        ]
        
        with open(args.create_sample_csv, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(sample_data)
        
        print(f"\n✓ Created sample CSV: {args.create_sample_csv}\n")
    
    elif args.csv and args.group:
        success = importer.import_and_create_group(args.csv, args.group, args.update)
        
        if success:
            print(f"\n✓ Successfully imported users and created/updated group '{args.group}'\n")
        else:
            print(f"\n✗ Failed to import users or create group\n")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
