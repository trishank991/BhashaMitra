"""Progress admin configuration."""
from django.contrib import admin
from .models import Progress, DailyActivity


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ['child', 'story', 'status', 'current_page', 'points_earned', 'last_read_at']
    list_filter = ['status', 'created_at']
    search_fields = ['child__name', 'story__title']
    ordering = ['-last_read_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(DailyActivity)
class DailyActivityAdmin(admin.ModelAdmin):
    list_display = ['child', 'date', 'stories_completed', 'pages_read', 'points_earned']
    list_filter = ['date']
    search_fields = ['child__name']
    ordering = ['-date']
