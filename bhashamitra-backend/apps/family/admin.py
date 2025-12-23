"""Admin configuration for family models."""
from django.contrib import admin
from .models import Family, FamilyLeaderboard, SiblingChallenge


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ['name', 'primary_parent', 'family_code', 'total_children', 'discount_tier']
    list_filter = ['discount_tier']
    search_fields = ['name', 'primary_parent__email', 'family_code']
    readonly_fields = ['id', 'created_at', 'updated_at', 'family_code']


@admin.register(FamilyLeaderboard)
class FamilyLeaderboardAdmin(admin.ModelAdmin):
    list_display = ['family', 'week_start', 'total_points', 'stories_completed', 'rank']
    list_filter = ['week_start']
    search_fields = ['family__name']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(SiblingChallenge)
class SiblingChallengeAdmin(admin.ModelAdmin):
    list_display = ['title', 'family', 'challenge_type', 'status', 'start_date', 'end_date', 'winner']
    list_filter = ['challenge_type', 'status', 'start_date']
    search_fields = ['title', 'family__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
