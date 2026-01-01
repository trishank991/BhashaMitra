"""Admin configuration for family models."""
from django.contrib import admin
from .models import Family, FamilyMembership, FamilyLeaderboard, CurriculumChallenge, CurriculumChallengeParticipant, CurriculumChallengeAttempt, SiblingChallenge


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ['name', 'primary_parent', 'invite_code', 'total_children', 'discount_tier']
    list_filter = ['discount_tier', 'created_at']
    search_fields = ['name', 'primary_parent__email', 'invite_code']
    readonly_fields = ['id', 'created_at', 'updated_at', 'invite_code', 'invite_code_expires_at']
    filter_horizontal = ['members']


@admin.register(FamilyMembership)
class FamilyMembershipAdmin(admin.ModelAdmin):
    list_display = ['family', 'child', 'role', 'joined_at', 'is_active']
    list_filter = ['role', 'is_active', 'joined_at']
    search_fields = ['family__name', 'child__name']
    readonly_fields = ['id', 'created_at', 'updated_at', 'joined_at']


@admin.register(FamilyLeaderboard)
class FamilyLeaderboardAdmin(admin.ModelAdmin):
    list_display = ['family', 'week_start', 'total_points', 'stories_completed', 'rank']
    list_filter = ['week_start']
    search_fields = ['family__name']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(CurriculumChallenge)
class CurriculumChallengeAdmin(admin.ModelAdmin):
    list_display = ['title', 'family', 'challenge_type', 'difficulty', 'status', 'start_date', 'end_date', 'winner']
    list_filter = ['challenge_type', 'difficulty', 'status', 'start_date']
    search_fields = ['title', 'family__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    filter_horizontal = []  # Participants are managed through inline or API


@admin.register(CurriculumChallengeParticipant)
class CurriculumChallengeParticipantAdmin(admin.ModelAdmin):
    list_display = ['challenge', 'child', 'completed_count', 'correct_count', 'accuracy_score', 'started_at']
    list_filter = ['challenge__challenge_type', 'started_at']
    search_fields = ['challenge__title', 'child__name']
    readonly_fields = ['id', 'created_at', 'updated_at', 'started_at']


@admin.register(CurriculumChallengeAttempt)
class CurriculumChallengeAttemptAdmin(admin.ModelAdmin):
    list_display = ['participant', 'item_type', 'item_value', 'is_correct', 'accuracy_score', 'created_at']
    list_filter = ['item_type', 'is_correct', 'created_at']
    search_fields = ['participant__child__name', 'item_value']
    readonly_fields = ['id', 'created_at']


# Keep legacy SiblingChallenge for backwards compatibility
@admin.register(SiblingChallenge)
class SiblingChallengeAdmin(admin.ModelAdmin):
    list_display = ['title', 'family', 'challenge_type', 'status', 'start_date', 'end_date', 'winner']
    list_filter = ['challenge_type', 'status', 'start_date']
    search_fields = ['title', 'family__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
