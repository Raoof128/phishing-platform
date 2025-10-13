"""
Phishing Platform Automation Package
Provides automated campaign management, analytics, training, and user import functionality
"""

__version__ = '1.0.0'
__author__ = 'Security Team'

from .campaign_manager import GophishCampaign
from .analytics import PhishingAnalytics
from .training_automation import TrainingAutomation
from .user_import import UserImporter

__all__ = [
    'GophishCampaign',
    'PhishingAnalytics',
    'TrainingAutomation',
    'UserImporter',
]
