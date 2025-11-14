#!/usr/bin/env python3
"""
Unit tests for analytics module
"""

import pytest
import pandas as pd
from unittest.mock import Mock, patch, MagicMock
from automation.analytics import PhishingAnalytics
from automation.constants import RiskLevel, RISK_THRESHOLD_HIGH, RISK_THRESHOLD_MEDIUM


class TestPhishingAnalyticsInit:
    """Tests for PhishingAnalytics initialization"""

    def test_initialization_success(self, mock_config_file, temp_dir):
        """Test successful initialization"""
        # Update config with temp directory
        import yaml
        with open(mock_config_file, 'r') as f:
            config = yaml.safe_load(f)

        config['analytics']['gophish_db_path'] = str(temp_dir / 'test.db')
        config['analytics']['reports_dir'] = str(temp_dir / 'reports')

        with open(mock_config_file, 'w') as f:
            yaml.dump(config, f)

        analytics = PhishingAnalytics(config_path=mock_config_file)

        assert analytics.db_path == str(temp_dir / 'test.db')
        assert analytics.reports_dir.exists()

    def test_initialization_missing_config(self):
        """Test initialization with missing config file"""
        with pytest.raises(FileNotFoundError):
            PhishingAnalytics(config_path="nonexistent.yaml")


class TestGetCampaignResults:
    """Tests for get_campaign_results method"""

    def test_get_results_success(self, mock_config_file, mock_database, temp_dir):
        """Test successful retrieval of campaign results"""
        # Update config to use mock database
        import yaml
        with open(mock_config_file, 'r') as f:
            config = yaml.safe_load(f)

        config['analytics']['gophish_db_path'] = mock_database
        config['analytics']['reports_dir'] = str(temp_dir / 'reports')

        with open(mock_config_file, 'w') as f:
            yaml.dump(config, f)

        analytics = PhishingAnalytics(config_path=mock_config_file)
        results = analytics.get_campaign_results(1)

        assert results['campaign_id'] == 1
        assert results['name'] == 'Test Campaign'
        assert results['total_targets'] == 4
        assert results['emails_opened'] >= 2
        assert 'open_rate' in results
        assert 'click_rate' in results

    def test_get_results_nonexistent_campaign(self, mock_config_file, mock_database, temp_dir):
        """Test retrieval of non-existent campaign"""
        import yaml
        with open(mock_config_file, 'r') as f:
            config = yaml.safe_load(f)

        config['analytics']['gophish_db_path'] = mock_database
        config['analytics']['reports_dir'] = str(temp_dir / 'reports')

        with open(mock_config_file, 'w') as f:
            yaml.dump(config, f)

        analytics = PhishingAnalytics(config_path=mock_config_file)
        results = analytics.get_campaign_results(999)

        assert results == {}


class TestCalculateUserRiskScore:
    """Tests for calculate_user_risk_score method"""

    def test_calculate_risk_high(self, mock_config_file, mock_database, temp_dir):
        """Test risk calculation for high-risk user"""
        import yaml
        with open(mock_config_file, 'r') as f:
            config = yaml.safe_load(f)

        config['analytics']['gophish_db_path'] = mock_database
        config['analytics']['reports_dir'] = str(temp_dir / 'reports')

        with open(mock_config_file, 'w') as f:
            yaml.dump(config, f)

        analytics = PhishingAnalytics(config_path=mock_config_file)

        # user3@test.com submitted data (high risk)
        risk = analytics.calculate_user_risk_score('user3@test.com')

        assert 'risk_score' in risk
        assert 'risk_level' in risk
        assert risk['email'] == 'user3@test.com'
        assert risk['campaigns_participated'] >= 1

    def test_calculate_risk_unknown_user(self, mock_config_file, mock_database, temp_dir):
        """Test risk calculation for unknown user"""
        import yaml
        with open(mock_config_file, 'r') as f:
            config = yaml.safe_load(f)

        config['analytics']['gophish_db_path'] = mock_database
        config['analytics']['reports_dir'] = str(temp_dir / 'reports')

        with open(mock_config_file, 'w') as f:
            yaml.dump(config, f)

        analytics = PhishingAnalytics(config_path=mock_config_file)
        risk = analytics.calculate_user_risk_score('unknown@test.com')

        assert risk['risk_score'] == 0
        assert risk['risk_level'] == RiskLevel.UNKNOWN.value
        assert risk['campaigns_participated'] == 0

    def test_calculate_risk_tuple_compatibility(self, mock_config_file, mock_database, temp_dir):
        """Test calculate_risk_score returns tuple for backward compatibility"""
        import yaml
        with open(mock_config_file, 'r') as f:
            config = yaml.safe_load(f)

        config['analytics']['gophish_db_path'] = mock_database
        config['analytics']['reports_dir'] = str(temp_dir / 'reports')

        with open(mock_config_file, 'w') as f:
            yaml.dump(config, f)

        analytics = PhishingAnalytics(config_path=mock_config_file)
        score, details = analytics.calculate_risk_score('user1@test.com')

        assert isinstance(score, int)
        assert isinstance(details, dict)
        assert score == details['risk_score']


class TestGetAllUsersRiskScores:
    """Tests for get_all_users_risk_scores method"""

    def test_get_all_users(self, mock_config_file, mock_database, temp_dir):
        """Test getting risk scores for all users"""
        import yaml
        with open(mock_config_file, 'r') as f:
            config = yaml.safe_load(f)

        config['analytics']['gophish_db_path'] = mock_database
        config['analytics']['reports_dir'] = str(temp_dir / 'reports')

        with open(mock_config_file, 'w') as f:
            yaml.dump(config, f)

        analytics = PhishingAnalytics(config_path=mock_config_file)
        df = analytics.get_all_users_risk_scores()

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 4  # 4 users in mock database
        assert 'email' in df.columns
        assert 'risk_score' in df.columns
        assert 'risk_level' in df.columns

    def test_get_all_users_alias(self, mock_config_file, mock_database, temp_dir):
        """Test alias method get_all_user_risks"""
        import yaml
        with open(mock_config_file, 'r') as f:
            config = yaml.safe_load(f)

        config['analytics']['gophish_db_path'] = mock_database
        config['analytics']['reports_dir'] = str(temp_dir / 'reports')

        with open(mock_config_file, 'w') as f:
            yaml.dump(config, f)

        analytics = PhishingAnalytics(config_path=mock_config_file)
        df1 = analytics.get_all_user_risks()
        df2 = analytics.get_all_users_risk_scores()

        assert df1.equals(df2)


class TestGenerateCampaignReport:
    """Tests for generate_campaign_report method"""

    def test_generate_html_report(self, mock_config_file, mock_database, temp_dir):
        """Test HTML report generation"""
        import yaml
        with open(mock_config_file, 'r') as f:
            config = yaml.safe_load(f)

        config['analytics']['gophish_db_path'] = mock_database
        config['analytics']['reports_dir'] = str(temp_dir / 'reports')

        with open(mock_config_file, 'w') as f:
            yaml.dump(config, f)

        analytics = PhishingAnalytics(config_path=mock_config_file)
        report_path = analytics.generate_campaign_report(1, output_format='html')

        assert report_path != ""
        assert Path(report_path).exists()
        assert Path(report_path).suffix == '.html'

    def test_generate_csv_report(self, mock_config_file, mock_database, temp_dir):
        """Test CSV report generation"""
        import yaml
        with open(mock_config_file, 'r') as f:
            config = yaml.safe_load(f)

        config['analytics']['gophish_db_path'] = mock_database
        config['analytics']['reports_dir'] = str(temp_dir / 'reports')

        with open(mock_config_file, 'w') as f:
            yaml.dump(config, f)

        analytics = PhishingAnalytics(config_path=mock_config_file)
        report_path = analytics.generate_campaign_report(1, output_format='csv')

        assert report_path != ""
        assert Path(report_path).exists()
        assert Path(report_path).suffix == '.csv'

    def test_generate_report_nonexistent_campaign(self, mock_config_file, mock_database, temp_dir):
        """Test report generation for non-existent campaign"""
        import yaml
        with open(mock_config_file, 'r') as f:
            config = yaml.safe_load(f)

        config['analytics']['gophish_db_path'] = mock_database
        config['analytics']['reports_dir'] = str(temp_dir / 'reports')

        with open(mock_config_file, 'w') as f:
            yaml.dump(config, f)

        analytics = PhishingAnalytics(config_path=mock_config_file)
        report_path = analytics.generate_campaign_report(999, output_format='html')

        assert report_path == ""


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
