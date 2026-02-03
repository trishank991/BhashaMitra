"""Peppi Chat app configuration."""
from django.apps import AppConfig


class PeppiChatConfig(AppConfig):
    """Configuration for the Peppi AI Chat app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.peppi_chat'
    verbose_name = 'Peppi AI Chat'
