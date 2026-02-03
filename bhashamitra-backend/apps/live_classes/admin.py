"""Admin configuration for live classes models."""
from django.contrib import admin
from .models import (
    Teacher, TeacherCertification, LiveSession, SessionParticipant,
    SessionRating, SessionModerationLog, TeacherPerformanceMetrics
)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'user', 'status', 'rating', 'total_sessions', 'verified_at']
    list_filter = ['status', 'languages']
    search_fields = ['display_name', 'user__email']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(TeacherCertification)
class TeacherCertificationAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'title', 'issuing_organization', 'is_verified']
    list_filter = ['is_verified']
    search_fields = ['teacher__display_name', 'title']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(LiveSession)
class LiveSessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'teacher', 'session_type', 'language', 'scheduled_start', 'status']
    list_filter = ['session_type', 'status', 'language']
    search_fields = ['title', 'teacher__display_name']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(SessionParticipant)
class SessionParticipantAdmin(admin.ModelAdmin):
    list_display = ['session', 'child', 'status', 'joined_at']
    list_filter = ['status']
    search_fields = ['session__title', 'child__name']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(SessionRating)
class SessionRatingAdmin(admin.ModelAdmin):
    list_display = ['session', 'child', 'rating', 'would_recommend']
    list_filter = ['rating', 'would_recommend']
    search_fields = ['session__title']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(SessionModerationLog)
class SessionModerationLogAdmin(admin.ModelAdmin):
    list_display = ['session', 'moderator', 'action', 'timestamp']
    list_filter = ['action']
    search_fields = ['session__title']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(TeacherPerformanceMetrics)
class TeacherPerformanceMetricsAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'month', 'sessions_conducted', 'average_rating', 'earnings']
    list_filter = ['month']
    search_fields = ['teacher__display_name']
    readonly_fields = ['id', 'created_at', 'updated_at']
