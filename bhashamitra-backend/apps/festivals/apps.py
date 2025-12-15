"""Festivals app configuration."""
from django.apps import AppConfig


class FestivalsConfig(AppConfig):
    """Configuration for Festivals app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.festivals'
    verbose_name = 'Festivals'
