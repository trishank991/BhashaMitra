"""Admin configuration for localization models."""
from django.contrib import admin
from .models import MarketConfig, FestivalCalendar, RegionalContent


@admin.register(MarketConfig)
class MarketConfigAdmin(admin.ModelAdmin):
    list_display = ['market_code', 'name', 'currency_code', 'timezone', 'is_active', 'launch_date']
    list_filter = ['is_active', 'market_code']
    search_fields = ['name', 'market_code']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(FestivalCalendar)
class FestivalCalendarAdmin(admin.ModelAdmin):
    list_display = ['name', 'native_name', 'festival_type', 'date_2025', 'is_featured']
    list_filter = ['festival_type', 'is_featured', 'is_lunar_based']
    search_fields = ['name', 'native_name']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(RegionalContent)
class RegionalContentAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'content_id', 'market', 'is_available']
    list_filter = ['content_type', 'market', 'is_available']
    search_fields = ['content_id']
    readonly_fields = ['id', 'created_at', 'updated_at']
