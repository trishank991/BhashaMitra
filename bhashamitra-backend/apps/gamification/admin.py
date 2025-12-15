"""Gamification admin configuration."""
from django.contrib import admin
from .models import Badge, ChildBadge, Streak, VoiceRecording


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'criteria_type', 'criteria_value', 'points_bonus', 'display_order']
    list_filter = ['criteria_type']
    search_fields = ['name', 'description']
    ordering = ['display_order']


@admin.register(ChildBadge)
class ChildBadgeAdmin(admin.ModelAdmin):
    list_display = ['child', 'badge', 'earned_at']
    list_filter = ['badge', 'earned_at']
    search_fields = ['child__name', 'badge__name']
    ordering = ['-earned_at']


@admin.register(Streak)
class StreakAdmin(admin.ModelAdmin):
    list_display = ['child', 'current_streak', 'longest_streak', 'last_activity_date']
    search_fields = ['child__name']
    ordering = ['-current_streak']


@admin.register(VoiceRecording)
class VoiceRecordingAdmin(admin.ModelAdmin):
    list_display = ['child', 'story', 'page_number', 'duration_ms', 'recorded_at']
    list_filter = ['recorded_at']
    search_fields = ['child__name']
    ordering = ['-recorded_at']
