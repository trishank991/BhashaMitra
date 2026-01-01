"""
Subscription Tier Configuration for BhashaMitra.

Updated Tier Strategy (December 2024):
======================================

FREE ($0 NZD/month):
- Browse Mode: Basic alphabets, words, pronunciations
- Limited Content: 5 stories, 2 games per day
- No structured curriculum progression
- Cache-only TTS (pre-cached audio from curriculum)
- 1 child profile

STANDARD ($20 NZD/month):
- Full L1-L10 Curriculum Progression (CBSE/ICSE inspired structure)
- Guided Learning Journey with level progression
- Peppi's Advanced AI Chat System
- Unlimited Stories with Peppi narration
- Unlimited Games
- All content access within current level
- Google Cloud TTS Standard voices (high quality)
- 3 child profiles
- Progress tracking & reports

PREMIUM ($30 NZD/month):
- Everything in Standard
- 2 FREE Live Classes per month
- Google Cloud TTS WaveNet voices (highest quality, most natural)
- 5 child profiles
- Priority support
- Early access to new content
- Additional live sessions available (contact support for pricing)

TTS Provider Routing:
- FREE: cache_only (accesses pre-cached curriculum audio)
- STANDARD: google (Google TTS Standard voices, ~$4/million chars)
- PREMIUM: google_wavenet (Google TTS WaveNet voices, ~$16/million chars)
"""

from dataclasses import dataclass
from typing import Optional, List
from decimal import Decimal


@dataclass
class TierFeatures:
    """Feature set for a subscription tier."""
    # Content Limits
    story_limit: int  # -1 = unlimited
    games_per_day: int  # -1 = unlimited
    child_profiles: int

    # Access Controls
    has_curriculum_progression: bool
    has_peppi_ai_chat: bool
    has_peppi_narration: bool
    has_live_classes: bool
    free_live_classes_per_month: int

    # TTS Configuration
    tts_provider: str  # 'cache_only', 'svara', 'sarvam'

    # Content Access
    content_access_mode: str  # 'browse', 'level_gated'

    # Additional Features
    has_progress_reports: bool
    has_offline_downloads: bool
    has_priority_support: bool
    has_early_access: bool


# Tier Configuration Dictionary
TIER_CONFIG = {
    'FREE': TierFeatures(
        # Content Limits
        story_limit=5,
        games_per_day=2,
        child_profiles=1,

        # Access Controls
        has_curriculum_progression=False,
        has_peppi_ai_chat=False,
        has_peppi_narration=False,
        has_live_classes=False,
        free_live_classes_per_month=0,

        # TTS Configuration
        tts_provider='cache_only',

        # Content Access
        content_access_mode='browse',  # Can browse all L1 content only

        # Additional Features
        has_progress_reports=False,
        has_offline_downloads=False,
        has_priority_support=False,
        has_early_access=False,
    ),

    'STANDARD': TierFeatures(
        # Content Limits
        story_limit=-1,  # Unlimited
        games_per_day=-1,  # Unlimited
        child_profiles=3,

        # Access Controls
        has_curriculum_progression=True,  # Full L1-L10 Journey
        has_peppi_ai_chat=True,
        has_peppi_narration=True,
        has_live_classes=False,
        free_live_classes_per_month=0,

        # TTS Configuration
        tts_provider='google',  # Google TTS Standard voices

        # Content Access
        content_access_mode='level_gated',  # Content unlocked by level

        # Additional Features
        has_progress_reports=True,
        has_offline_downloads=False,
        has_priority_support=False,
        has_early_access=False,
    ),

    'PREMIUM': TierFeatures(
        # Content Limits
        story_limit=-1,  # Unlimited
        games_per_day=-1,  # Unlimited
        child_profiles=5,

        # Access Controls
        has_curriculum_progression=True,  # Full L1-L10 Journey
        has_peppi_ai_chat=True,
        has_peppi_narration=True,
        has_live_classes=True,
        free_live_classes_per_month=2,

        # TTS Configuration
        tts_provider='google_wavenet',  # Google TTS WaveNet - highest quality

        # Content Access
        content_access_mode='level_gated',  # Content unlocked by level

        # Additional Features
        has_progress_reports=True,
        has_offline_downloads=True,
        has_priority_support=True,
        has_early_access=True,
    ),
}


# Pricing Configuration (NZD)
TIER_PRICING = {
    'FREE': {
        'monthly': Decimal('0.00'),
        'yearly': Decimal('0.00'),
        'currency': 'NZD',
        'display_name': 'Free',
        'tagline': 'Get started with basics',
    },
    'STANDARD': {
        'monthly': Decimal('20.00'),
        'yearly': Decimal('200.00'),  # 2 months free
        'currency': 'NZD',
        'display_name': 'Standard',
        'tagline': 'Full curriculum journey',
    },
}

# Add Premium pricing if enabled
from django.conf import settings as django_settings
if getattr(django_settings, 'ENABLE_PREMIUM_TIER', False):
    TIER_PRICING['PREMIUM'] = {
        'monthly': Decimal('30.00'),
        'yearly': Decimal('300.00'),  # 2 months free
        'currency': 'NZD',
        'display_name': 'Premium',
        'tagline': 'Live classes + premium features',
    }


# Feature Display Matrix for Frontend
TIER_FEATURE_MATRIX = {
    'FREE': {
        'name': 'Free',
        'price': '$0',
        'price_yearly': '$0',
        'currency': 'NZD',
        'icon': '🌱',
        'color': '#22c55e',
        'features': [
            {'text': 'Basic Hindi alphabets', 'enabled': True},
            {'text': 'Basic vocabulary & pronunciation', 'enabled': True},
            {'text': '5 stories', 'enabled': True},
            {'text': '2 games per day', 'enabled': True},
            {'text': '1 child profile', 'enabled': True},
            {'text': 'Pre-cached audio only', 'enabled': True},
            {'text': 'L1-L10 Curriculum Journey', 'enabled': False},
            {'text': 'Peppi AI Chat', 'enabled': False},
            {'text': 'Peppi Story Narration', 'enabled': False},
            {'text': 'Unlimited games', 'enabled': False},
            {'text': 'Live classes', 'enabled': False},
        ],
        'cta': 'Start Free',
        'featured': False,
    },
    'STANDARD': {
        'name': 'Standard',
        'price': '$20/mo',
        'price_yearly': '$200/yr',
        'currency': 'NZD',
        'icon': '⭐',
        'color': '#f59e0b',
        'features': [
            {'text': 'Full L1-L10 Curriculum (CBSE/ICSE inspired)', 'enabled': True},
            {'text': 'Guided learning journey', 'enabled': True},
            {'text': 'Peppi AI Chat system', 'enabled': True},
            {'text': 'Peppi story narration', 'enabled': True},
            {'text': 'Unlimited stories', 'enabled': True},
            {'text': 'Unlimited games', 'enabled': True},
            {'text': '3 child profiles', 'enabled': True},
            {'text': 'Progress reports', 'enabled': True},
            {'text': 'Google Cloud TTS (high quality)', 'enabled': True},
            {'text': 'Live classes', 'enabled': False},
            {'text': 'WaveNet premium voices', 'enabled': False},
        ],
        'cta': 'Get Standard',
        'featured': True,
    },
}

# Check if Premium tier should be included (based on settings)
from django.conf import settings as django_settings
if getattr(django_settings, 'ENABLE_PREMIUM_TIER', False):
    TIER_FEATURE_MATRIX['PREMIUM'] = {
        'name': 'Premium',
        'price': '$30/mo',
        'price_yearly': '$300/yr',
        'currency': 'NZD',
        'icon': '👑',
        'color': '#8b5cf6',
        'features': [
            {'text': 'Everything in Standard', 'enabled': True},
            {'text': '2 FREE live classes/month', 'enabled': True},
            {'text': 'Google WaveNet voices (highest quality)', 'enabled': True},
            {'text': '5 child profiles', 'enabled': True},
            {'text': 'Priority support', 'enabled': True},
            {'text': 'Early access to new content', 'enabled': True},
            {'text': 'Offline downloads', 'enabled': True},
            {'text': 'Additional live sessions available', 'enabled': True, 'note': 'Contact support for pricing'},
        ],
        'cta': 'Get Premium',
        'featured': False,
    }


def get_tier_features(tier: str) -> TierFeatures:
    """Get features for a specific tier."""
    return TIER_CONFIG.get(tier, TIER_CONFIG['FREE'])


def get_tier_pricing(tier: str) -> dict:
    """Get pricing for a specific tier."""
    return TIER_PRICING.get(tier, TIER_PRICING['FREE'])


def get_tier_display(tier: str) -> dict:
    """Get display configuration for a specific tier."""
    return TIER_FEATURE_MATRIX.get(tier, TIER_FEATURE_MATRIX['FREE'])


def can_access_content(tier: str, content_level: int, user_level: int) -> bool:
    """
    Check if a user can access content based on their tier and level.

    FREE tier: Can only access L1 content in browse mode
    STANDARD/PREMIUM: Can access content up to their current level
    """
    features = get_tier_features(tier)

    if features.content_access_mode == 'browse':
        # Free tier can only browse L1 content
        return content_level == 1
    else:
        # Paid tiers can access content up to their level
        return content_level <= user_level


def get_daily_game_limit(tier: str) -> int:
    """Get the daily game limit for a tier. Returns -1 for unlimited."""
    return get_tier_features(tier).games_per_day


def get_story_limit(tier: str) -> int:
    """Get the story limit for a tier. Returns -1 for unlimited."""
    return get_tier_features(tier).story_limit
