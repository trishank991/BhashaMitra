"""Market localization and regional configuration models."""
from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel


class MarketConfig(TimeStampedModel):
    """Market-specific configuration for different regions."""

    class Market(models.TextChoices):
        NZ = 'NZ', 'New Zealand'
        AU = 'AU', 'Australia'
        IN = 'IN', 'India'
        US = 'US', 'United States'
        UK = 'UK', 'United Kingdom'
        CA = 'CA', 'Canada'

    market_code = models.CharField(max_length=5, choices=Market.choices, unique=True)
    name = models.CharField(max_length=100)
    currency_code = models.CharField(max_length=3, default='NZD')
    currency_symbol = models.CharField(max_length=5, default='$')
    timezone = models.CharField(max_length=50, default='Pacific/Auckland')
    primary_languages = models.JSONField(default=list)
    pricing_config = models.JSONField(
        default=dict,
        help_text='Tier pricing in local currency'
    )
    content_restrictions = models.JSONField(
        default=dict,
        help_text='Content availability restrictions'
    )
    legal_config = models.JSONField(
        default=dict,
        help_text='Legal requirements (COPPA, GDPR, etc.)'
    )
    payment_methods = models.JSONField(
        default=list,
        help_text='Available payment methods'
    )
    is_active = models.BooleanField(default=True)
    launch_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'market_configs'
        verbose_name = 'Market Configuration'
        verbose_name_plural = 'Market Configurations'

    def __str__(self):
        return f"{self.name} ({self.market_code})"


class FestivalCalendar(TimeStampedModel):
    """Cultural festivals and events calendar."""

    class FestivalType(models.TextChoices):
        RELIGIOUS = 'RELIGIOUS', 'Religious'
        CULTURAL = 'CULTURAL', 'Cultural'
        NATIONAL = 'NATIONAL', 'National Holiday'
        SEASONAL = 'SEASONAL', 'Seasonal'

    name = models.CharField(max_length=200)
    native_name = models.CharField(max_length=200, blank=True)
    festival_type = models.CharField(max_length=20, choices=FestivalType.choices)
    description = models.TextField(blank=True)
    languages = models.JSONField(default=list, help_text='Languages celebrating this festival')
    markets = models.JSONField(default=list, help_text='Markets where this is observed')
    date_2024 = models.DateField(null=True, blank=True)
    date_2025 = models.DateField(null=True, blank=True)
    date_2026 = models.DateField(null=True, blank=True)
    is_lunar_based = models.BooleanField(default=False)
    content_pack_id = models.UUIDField(null=True, blank=True, help_text='Related offline content pack')
    greeting_translations = models.JSONField(
        default=dict,
        help_text='Festival greetings in different languages'
    )
    traditions = models.JSONField(default=list)
    activities = models.JSONField(default=list, help_text='Suggested learning activities')
    is_featured = models.BooleanField(default=False)

    class Meta:
        db_table = 'festival_calendars'
        indexes = [
            models.Index(fields=['festival_type']),
            models.Index(fields=['date_2025']),
        ]

    def __str__(self):
        return f"{self.name} ({self.festival_type})"


class RegionalContent(TimeStampedModel):
    """Region-specific content variations."""

    content_type = models.CharField(max_length=50)
    content_id = models.UUIDField()
    market = models.ForeignKey(
        MarketConfig,
        on_delete=models.CASCADE,
        related_name='regional_content'
    )
    variations = models.JSONField(
        default=dict,
        help_text='Market-specific content variations'
    )
    is_available = models.BooleanField(default=True)
    availability_reason = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = 'regional_content'
        unique_together = ['content_type', 'content_id', 'market']
        indexes = [
            models.Index(fields=['content_type', 'market']),
        ]

    def __str__(self):
        return f"{self.content_type}:{self.content_id} ({self.market.market_code})"
