"""Admin configuration for parent engagement models."""
from django.contrib import admin
from .models import ParentPreferences, LearningGoal, WeeklyReport, ParentChildActivity


@admin.register(ParentPreferences)
class ParentPreferencesAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_frequency', 'email_reports', 'push_notifications']
    list_filter = ['notification_frequency', 'email_reports']
    search_fields = ['user__email']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(LearningGoal)
class LearningGoalAdmin(admin.ModelAdmin):
    list_display = ['child', 'goal_type', 'target_value', 'current_value', 'is_active']
    list_filter = ['goal_type', 'is_active']
    search_fields = ['child__name']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(WeeklyReport)
class WeeklyReportAdmin(admin.ModelAdmin):
    list_display = ['child', 'week_start', 'week_end', 'stories_completed', 'points_earned', 'sent_at']
    list_filter = ['week_start']
    search_fields = ['child__name']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(ParentChildActivity)
class ParentChildActivityAdmin(admin.ModelAdmin):
    list_display = ['title', 'activity_type', 'language', 'duration_minutes', 'is_featured']
    list_filter = ['activity_type', 'language', 'is_featured']
    search_fields = ['title']
    readonly_fields = ['id', 'created_at', 'updated_at']
