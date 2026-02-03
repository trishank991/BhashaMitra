"""Django Admin configuration for Challenges."""

from django.contrib import admin
from .models import Challenge, ChallengeAttempt, UserChallengeQuota


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = [
        'code', 'title', 'language', 'category', 'difficulty',
        'total_attempts', 'total_completions', 'average_score',
        'is_active', 'created_at'
    ]
    list_filter = ['language', 'category', 'difficulty', 'is_active']
    search_fields = ['code', 'title', 'creator__email']
    readonly_fields = [
        'code', 'total_attempts', 'total_completions', 'average_score',
        'created_at', 'updated_at'
    ]
    ordering = ['-created_at']

    fieldsets = (
        ('Challenge Info', {
            'fields': ('code', 'title', 'title_native', 'language', 'category', 'difficulty')
        }),
        ('Creator', {
            'fields': ('creator', 'creator_child')
        }),
        ('Configuration', {
            'fields': ('question_count', 'time_limit_seconds', 'questions')
        }),
        ('Stats', {
            'fields': ('total_attempts', 'total_completions', 'average_score')
        }),
        ('Status', {
            'fields': ('is_active', 'expires_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ChallengeAttempt)
class ChallengeAttemptAdmin(admin.ModelAdmin):
    list_display = [
        'participant_name', 'challenge', 'score', 'max_score',
        'percentage', 'time_taken_seconds', 'is_completed', 'created_at'
    ]
    list_filter = ['is_completed', 'challenge__language']
    search_fields = ['participant_name', 'challenge__code', 'challenge__title']
    readonly_fields = ['created_at', 'updated_at', 'completed_at']
    ordering = ['-created_at']

    fieldsets = (
        ('Challenge', {
            'fields': ('challenge',)
        }),
        ('Participant', {
            'fields': ('participant_name', 'participant_location', 'participant_user', 'participant_child')
        }),
        ('Results', {
            'fields': ('score', 'max_score', 'percentage', 'time_taken_seconds', 'answers')
        }),
        ('Status', {
            'fields': ('is_completed', 'completed_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserChallengeQuota)
class UserChallengeQuotaAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'challenges_created_today', 'total_challenges_created', 'last_reset_date'
    ]
    search_fields = ['user__email']
    readonly_fields = ['last_reset_date']
    ordering = ['-last_reset_date']
