"""Admin configuration for analytics models."""
from django.contrib import admin
from .models import LessonAnalytics, CohortAnalytics, PeppiAnalytics, EventLog


@admin.register(LessonAnalytics)
class LessonAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'content_id', 'language', 'total_views', 'completion_rate']
    list_filter = ['content_type', 'language']
    search_fields = ['content_id']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(CohortAnalytics)
class CohortAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['cohort_type', 'cohort_value', 'period_start', 'active_users', 'retention_rate']
    list_filter = ['cohort_type', 'period_start']
    search_fields = ['cohort_value']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(PeppiAnalytics)
class PeppiAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['child', 'date', 'total_interactions', 'voice_interactions', 'help_requests']
    list_filter = ['date']
    search_fields = ['child__name']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(EventLog)
class EventLogAdmin(admin.ModelAdmin):
    list_display = ['event_name', 'event_category', 'user', 'timestamp']
    list_filter = ['event_category', 'timestamp']
    search_fields = ['event_name', 'user__email']
    readonly_fields = ['id', 'created_at', 'updated_at']
