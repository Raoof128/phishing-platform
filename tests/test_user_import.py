#!/usr/bin/env python3
"""
Unit tests for user import module
"""

import pytest
from unittest.mock import Mock, patch
from automation.user_import import UserImporter
from automation.utils import validate_email


class TestUserImporterInit:
    """Tests for UserImporter initialization"""

    def test_initialization_success(self, mock_config_file):
        """Test successful initialization"""
        importer = UserImporter(config_path=mock_config_file)
        assert importer.api_key == "test-api-key-12345"
        assert importer.server_url == "https://localhost:3333"
        assert importer.import_config is not None


class TestImportUsersFromCSV:
    """Tests for import_users_from_csv method"""

    def test_import_valid_csv(self, mock_config_file, mock_csv_file):
        """Test importing valid CSV file"""
        importer = UserImporter(config_path=mock_config_file)
        users = importer.import_users_from_csv(mock_csv_file)

        assert len(users) == 3
        assert all('email' in user for user in users)
        assert all(validate_email(user['email']) for user in users)

    def test_import_nonexistent_csv(self, mock_config_file):
        """Test importing non-existent CSV file"""
        importer = UserImporter(config_path=mock_config_file)
        users = importer.import_users_from_csv('nonexistent.csv')

        assert users == []

    def test_import_with_invalid_emails(self, mock_config_file, temp_dir):
        """Test CSV import with invalid email addresses"""
        import csv

        csv_file = temp_dir / "invalid_emails.csv"
        with open(csv_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['email', 'first_name', 'last_name', 'position'])
            writer.writeheader()
            writer.writerow({'email': 'invalid-email', 'first_name': 'John', 'last_name': 'Doe', 'position': 'Engineer'})
            writer.writerow({'email': 'valid@test.com', 'first_name': 'Jane', 'last_name': 'Smith', 'position': 'Manager'})

        importer = UserImporter(config_path=mock_config_file)
        users = importer.import_users_from_csv(str(csv_file))

        # Should skip invalid email if skip_invalid is true
        assert len(users) == 1
        assert users[0]['email'] == 'valid@test.com'


class TestCreateGroup:
    """Tests for create_group method"""

    @patch('automation.user_import.requests.post')
    def test_create_group_success(self, mock_post, mock_config_file, mock_user_data):
        """Test successful group creation"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {'id': 1, 'name': 'Test Group', 'targets': mock_user_data}
        mock_post.return_value = mock_response

        importer = UserImporter(config_path=mock_config_file)
        group = importer.create_group('Test Group', mock_user_data)

        assert group is not None
        assert group['name'] == 'Test Group'
        mock_post.assert_called_once()

    @patch('automation.user_import.requests.post')
    def test_create_group_api_error(self, mock_post, mock_config_file, mock_user_data):
        """Test group creation with API error"""
        mock_post.side_effect = Exception("API Error")

        importer = UserImporter(config_path=mock_config_file)
        group = importer.create_group('Test Group', mock_user_data)

        assert group is None


class TestImportAndCreateGroup:
    """Tests for import_and_create_group method"""

    @patch('automation.user_import.UserImporter.create_group')
    @patch('automation.user_import.UserImporter.get_group_by_name')
    def test_import_and_create_new_group(self, mock_get_group, mock_create_group, mock_config_file, mock_csv_file):
        """Test importing CSV and creating new group"""
        mock_get_group.return_value = None  # Group doesn't exist
        mock_create_group.return_value = {'id': 1, 'name': 'New Group'}

        importer = UserImporter(config_path=mock_config_file)
        success = importer.import_and_create_group(mock_csv_file, 'New Group', update_existing=False)

        assert success is True
        mock_create_group.assert_called_once()

    @patch('automation.user_import.UserImporter.update_group')
    @patch('automation.user_import.UserImporter.get_group_by_name')
    def test_import_and_update_existing_group(self, mock_get_group, mock_update_group, mock_config_file, mock_csv_file):
        """Test importing CSV and updating existing group"""
        mock_get_group.return_value = {'id': 1, 'name': 'Existing Group'}
        mock_update_group.return_value = True

        importer = UserImporter(config_path=mock_config_file)
        success = importer.import_and_create_group(mock_csv_file, 'Existing Group', update_existing=True)

        assert success is True
        mock_update_group.assert_called_once()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
