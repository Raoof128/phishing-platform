#!/usr/bin/env python3
"""
Unit tests for campaign manager
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from automation.campaign_manager import GophishCampaign
from automation.utils import APIError


@pytest.fixture
def mock_config(tmp_path):
    """Create a mock configuration file"""
    config_file = tmp_path / "api_config.yaml"
    config_content = """
gophish:
  api_key: test-api-key
  server_url: https://localhost:3333
  verify_ssl: false
  timeout: 30
"""
    config_file.write_text(config_content)
    return str(config_file)


@pytest.fixture
def campaign_manager(mock_config):
    """Create a campaign manager instance with mock config"""
    return GophishCampaign(config_path=mock_config)


class TestGophishCampaignInit:
    """Tests for GophishCampaign initialization"""

    def test_initialization_success(self, mock_config):
        """Test successful initialization"""
        manager = GophishCampaign(config_path=mock_config)

        assert manager.api_key == "test-api-key"
        assert manager.server_url == "https://localhost:3333"
        assert manager.verify_ssl is False
        assert manager.timeout == 30

    def test_initialization_missing_config(self):
        """Test initialization with missing config file"""
        with pytest.raises(FileNotFoundError):
            GophishCampaign(config_path="nonexistent.yaml")


class TestMakeRequest:
    """Tests for _make_request method"""

    @patch('automation.campaign_manager.requests.get')
    def test_successful_get_request(self, mock_get, campaign_manager):
        """Test successful GET request"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'id': 1}
        mock_get.return_value = mock_response

        response = campaign_manager._make_request('GET', 'campaigns/')

        assert response.status_code == 200
        mock_get.assert_called_once()

    @patch('automation.campaign_manager.requests.post')
    def test_successful_post_request(self, mock_post, campaign_manager):
        """Test successful POST request"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_post.return_value = mock_response

        data = {'name': 'Test Campaign'}
        response = campaign_manager._make_request('POST', 'campaigns/', data=data)

        assert response.status_code == 201
        mock_post.assert_called_once()

    @patch('automation.campaign_manager.requests.get')
    def test_request_timeout(self, mock_get, campaign_manager):
        """Test request timeout handling"""
        from requests.exceptions import Timeout

        mock_get.side_effect = Timeout("Connection timeout")

        with pytest.raises(APIError):
            campaign_manager._make_request('GET', 'campaigns/')


class TestTestConnection:
    """Tests for test_connection method"""

    @patch.object(GophishCampaign, '_make_request')
    def test_connection_success(self, mock_request, campaign_manager):
        """Test successful connection test"""
        mock_request.return_value = Mock()

        result = campaign_manager.test_connection()

        assert result is True
        mock_request.assert_called_with('GET', 'campaigns/')

    @patch.object(GophishCampaign, '_make_request')
    def test_connection_failure(self, mock_request, campaign_manager):
        """Test failed connection test"""
        mock_request.side_effect = Exception("Connection failed")

        result = campaign_manager.test_connection()

        assert result is False


class TestListCampaigns:
    """Tests for list_campaigns method"""

    @patch.object(GophishCampaign, '_make_request')
    def test_list_campaigns_success(self, mock_request, campaign_manager):
        """Test successful campaign listing"""
        mock_response = Mock()
        mock_response.json.return_value = [
            {'id': 1, 'name': 'Campaign 1'},
            {'id': 2, 'name': 'Campaign 2'}
        ]
        mock_request.return_value = mock_response

        campaigns = campaign_manager.list_campaigns()

        assert len(campaigns) == 2
        assert campaigns[0]['name'] == 'Campaign 1'

    @patch.object(GophishCampaign, '_make_request')
    def test_list_campaigns_error(self, mock_request, campaign_manager):
        """Test campaign listing with error"""
        mock_request.side_effect = Exception("API Error")

        campaigns = campaign_manager.list_campaigns()

        assert campaigns == []


class TestGetCampaignSummary:
    """Tests for get_campaign_summary method"""

    @patch.object(GophishCampaign, 'get_campaign')
    def test_get_summary_with_results(self, mock_get_campaign, campaign_manager):
        """Test getting campaign summary with results"""
        mock_get_campaign.return_value = {
            'id': 1,
            'name': 'Test Campaign',
            'status': 'Completed',
            'created_date': '2025-01-01',
            'results': [
                {'status': 'Email Sent'},
                {'status': 'Email Opened'},
                {'status': 'Clicked Link'},
                {'status': 'Submitted Data'}
            ],
            'timeline': []
        }

        summary = campaign_manager.get_campaign_summary(1)

        assert summary['campaign_id'] == 1
        assert summary['total_targets'] == 4
        assert summary['emails_sent'] == 4
        assert summary['emails_opened'] == 3
        assert summary['links_clicked'] == 2
        assert summary['data_submitted'] == 1

    @patch.object(GophishCampaign, 'get_campaign')
    def test_get_summary_nonexistent_campaign(self, mock_get_campaign, campaign_manager):
        """Test getting summary for non-existent campaign"""
        mock_get_campaign.return_value = None

        summary = campaign_manager.get_campaign_summary(999)

        assert summary == {}


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
