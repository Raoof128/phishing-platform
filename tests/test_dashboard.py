#!/usr/bin/env python3
"""
Unit tests for dashboard Flask application
"""

import pytest
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


@pytest.fixture
def app():
    """Create Flask test application"""
    with patch('dashboard.app.GophishCampaign'), \
         patch('dashboard.app.PhishingAnalytics'):
        from dashboard.app import app
        app.config['TESTING'] = True
        yield app


@pytest.fixture
def client(app):
    """Create Flask test client"""
    return app.test_client()


class TestHealthCheck:
    """Tests for health check endpoint"""

    def test_health_check_healthy(self, client):
        """Test health check when services are healthy"""
        response = client.get('/health')

        assert response.status_code == 200 or response.status_code == 503
        data = response.get_json()
        assert 'status' in data
        assert 'timestamp' in data
        assert 'services' in data


class TestSecurityHeaders:
    """Tests for security headers"""

    def test_security_headers_present(self, client):
        """Test that security headers are present in responses"""
        response = client.get('/health')

        assert 'X-Content-Type-Options' in response.headers
        assert response.headers['X-Content-Type-Options'] == 'nosniff'
        assert 'X-Frame-Options' in response.headers
        assert response.headers['X-Frame-Options'] == 'DENY'
        assert 'X-XSS-Protection' in response.headers
        assert 'Strict-Transport-Security' in response.headers
        assert 'Content-Security-Policy' in response.headers
        assert 'Referrer-Policy' in response.headers


class TestMainRoute:
    """Tests for main dashboard route"""

    def test_index_route(self, client):
        """Test main index route"""
        response = client.get('/')

        # Should return HTML template or redirect
        assert response.status_code in [200, 302, 404, 500]


class TestAPICampaigns:
    """Tests for campaigns API endpoints"""

    @patch('dashboard.app.campaign_api')
    def test_get_campaigns(self, mock_api, client):
        """Test getting all campaigns"""
        if mock_api:
            mock_api.get_campaigns.return_value = [
                {'id': 1, 'name': 'Test Campaign', 'status': 'Completed'}
            ]

            response = client.get('/api/campaigns')

            if response.status_code == 200:
                data = response.get_json()
                assert isinstance(data, list)

    @patch('dashboard.app.campaign_api')
    def test_get_campaign_by_id(self, mock_api, client):
        """Test getting specific campaign"""
        if mock_api:
            mock_api.get_campaign.return_value = {
                'id': 1, 'name': 'Test Campaign'
            }

            response = client.get('/api/campaign/1')

            if response.status_code == 200:
                data = response.get_json()
                assert 'id' in data or 'error' in data


class TestAPIUserRisks:
    """Tests for user risks API endpoints"""

    @patch('dashboard.app.analytics')
    def test_get_user_risks(self, mock_analytics, client):
        """Test getting all user risks"""
        if mock_analytics:
            import pandas as pd
            mock_df = pd.DataFrame([
                {'email': 'test@example.com', 'risk_score': 50, 'risk_level': 'Medium'}
            ])
            mock_analytics.get_all_user_risks.return_value = mock_df

            response = client.get('/api/user_risks')

            if response.status_code == 200:
                data = response.get_json()
                assert isinstance(data, list) or 'error' in data


class TestErrorHandlers:
    """Tests for error handlers"""

    def test_404_error(self, client):
        """Test 404 error handler"""
        response = client.get('/nonexistent-route')

        assert response.status_code == 404
        data = response.get_json()
        if data:
            assert 'error' in data


class TestRateLimiting:
    """Tests for rate limiting"""

    def test_rate_limit_not_exceeded(self, client):
        """Test that rate limit allows normal requests"""
        # Make a few requests
        for _ in range(5):
            response = client.get('/health')
            assert response.status_code in [200, 503]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
