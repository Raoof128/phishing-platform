#!/usr/bin/env python3
"""
Unit tests for training automation module
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from automation.training_automation import TrainingAutomation


class TestTrainingAutomationInit:
    """Tests for TrainingAutomation initialization"""

    def test_initialization_success(self, mock_config_file):
        """Test successful initialization"""
        training = TrainingAutomation(config_path=mock_config_file)
        assert training.training_config is not None
        assert training.analytics is not None

    def test_initialization_missing_training_config(self, temp_dir):
        """Test initialization with missing training configuration"""
        import yaml
        config_file = temp_dir / "no_training.yaml"
        config = {"gophish": {"api_key": "test", "server_url": "http://localhost"}}
        with open(config_file, 'w') as f:
            yaml.dump(config, f)

        with pytest.raises(Exception):  # Should raise ConfigurationError
            TrainingAutomation(config_path=str(config_file))


class TestAssignTrainingBasedOnRisk:
    """Tests for assign_training_based_on_risk method"""

    @patch('automation.training_automation.PhishingAnalytics')
    def test_assign_high_risk_training(self, mock_analytics_class, mock_config_file):
        """Test assignment of high-risk training"""
        mock_analytics = Mock()
        mock_analytics.calculate_user_risk_score.return_value = {
            'risk_score': 80, 'risk_level': 'High'
        }
        mock_analytics_class.return_value = mock_analytics

        training = TrainingAutomation(config_path=mock_config_file)
        training.analytics = mock_analytics

        modules = training.assign_training_based_on_risk('test@example.com')

        assert isinstance(modules, list)
        assert len(modules) > 0
        assert 'Advanced Phishing Recognition' in modules

    @patch('automation.training_automation.PhishingAnalytics')
    def test_assign_medium_risk_training(self, mock_analytics_class, mock_config_file):
        """Test assignment of medium-risk training"""
        mock_analytics = Mock()
        mock_analytics.calculate_user_risk_score.return_value = {
            'risk_score': 50, 'risk_level': 'Medium'
        }
        mock_analytics_class.return_value = mock_analytics

        training = TrainingAutomation(config_path=mock_config_file)
        training.analytics = mock_analytics

        modules = training.assign_training_based_on_risk('test@example.com')

        assert isinstance(modules, list)
        assert 'Email Security Basics' in modules

    @patch('automation.training_automation.PhishingAnalytics')
    def test_assign_low_risk_training(self, mock_analytics_class, mock_config_file):
        """Test assignment of low-risk training"""
        mock_analytics = Mock()
        mock_analytics.calculate_user_risk_score.return_value = {
            'risk_score': 20, 'risk_level': 'Low'
        }
        mock_analytics_class.return_value = mock_analytics

        training = TrainingAutomation(config_path=mock_config_file)
        training.analytics = mock_analytics

        modules = training.assign_training_based_on_risk('test@example.com')

        assert isinstance(modules, list)
        assert 'Security Awareness Overview' in modules


class TestProcessCampaignTrainingAssignments:
    """Tests for process_campaign_training_assignments method"""

    @patch('automation.training_automation.PhishingAnalytics')
    def test_process_assignments(self, mock_analytics_class, mock_config_file):
        """Test processing training assignments for a campaign"""
        mock_analytics = Mock()
        mock_analytics.get_campaign_results.return_value = {
            'campaign_id': 1,
            'results': [
                {'email': 'user1@test.com', 'first_name': 'User', 'last_name': 'One', 'status': 'Clicked Link'},
                {'email': 'user2@test.com', 'first_name': 'User', 'last_name': 'Two', 'status': 'Submitted Data'},
            ]
        }
        mock_analytics.calculate_user_risk_score.return_value = {
            'risk_score': 50, 'risk_level': 'Medium'
        }
        mock_analytics_class.return_value = mock_analytics

        training = TrainingAutomation(config_path=mock_config_file)
        training.analytics = mock_analytics

        with patch.object(training, 'send_training_email', return_value=True):
            stats = training.process_campaign_training_assignments(1)

            assert stats['campaign_id'] == 1
            assert stats['total_users'] == 2
            assert 'assignments_sent' in stats
            assert 'high_risk_users' in stats


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
