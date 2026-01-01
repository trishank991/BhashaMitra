"""Gamification admin configuration."""
from django.contrib import admin
from .models import (
    # Existing models
    Badge, ChildBadge, Streak, VoiceRecording,
    # Peppi Outfits & Accessories
    PeppiOutfit, PeppiOutfitTranslation, PeppiAccessory,
    # Child Peppi State
    ChildPeppiState, ChildUnlockedOutfit, ChildUnlockedAccessory,
    ChildUnlockedPhrase, ChildEquippedAccessories,
    # Daily Challenges
    DailyChallengeTemplate, ChildDailyChallenge,
)
# Note: PeppiPhrase admin is in apps.curriculum.admin
# Note: Festival admin is in apps.festivals.admin


# ===========================================
# EXISTING GAMIFICATION MODELS ADMIN
# ===========================================

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


# ===========================================
# PEPPI OUTFITS & ACCESSORIES ADMIN
# ===========================================

class PeppiOutfitTranslationInline(admin.TabularInline):
    model = PeppiOutfitTranslation
    extra = 1


@admin.register(PeppiOutfit)
class PeppiOutfitAdmin(admin.ModelAdmin):
    list_display = ['code', 'name_english', 'category', 'rarity', 'unlock_type', 'unlock_value', 'is_active']
    list_filter = ['category', 'rarity', 'unlock_type', 'primary_language', 'is_active']
    search_fields = ['code', 'name_english', 'description']
    ordering = ['sort_order', 'name_english']
    inlines = [PeppiOutfitTranslationInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('code', 'name_english', 'description', 'category', 'rarity')
        }),
        ('Unlock Requirements', {
            'fields': ('primary_language', 'unlock_type', 'unlock_value', 'unlock_festival')
        }),
        ('Media', {
            'fields': ('image_url', 'thumbnail_url')
        }),
        ('Settings', {
            'fields': ('sort_order', 'is_active')
        }),
    )


@admin.register(PeppiAccessory)
class PeppiAccessoryAdmin(admin.ModelAdmin):
    list_display = ['code', 'name_english', 'slot', 'rarity', 'unlock_type', 'unlock_value', 'is_active']
    list_filter = ['slot', 'rarity', 'unlock_type', 'is_active']
    search_fields = ['code', 'name_english']
    ordering = ['slot', 'name_english']


# PeppiPhrase admin is in apps.curriculum.admin


# ===========================================
# CHILD PEPPI STATE ADMIN
# ===========================================

@admin.register(ChildPeppiState)
class ChildPeppiStateAdmin(admin.ModelAdmin):
    list_display = ['child', 'evolution_stage', 'happiness', 'hunger', 'coins', 'gems', 'current_outfit']
    list_filter = ['evolution_stage']
    search_fields = ['child__name']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Child', {
            'fields': ('child',)
        }),
        ('Peppi Vitals', {
            'fields': ('happiness', 'hunger', 'evolution_stage')
        }),
        ('Appearance', {
            'fields': ('current_outfit',)
        }),
        ('Currency', {
            'fields': ('coins', 'gems')
        }),
        ('Stats', {
            'fields': ('total_pets', 'last_fed_at', 'last_played_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ChildUnlockedOutfit)
class ChildUnlockedOutfitAdmin(admin.ModelAdmin):
    list_display = ['child', 'outfit', 'unlocked_at', 'is_new']
    list_filter = ['unlocked_at', 'is_new']
    search_fields = ['child__name', 'outfit__name_english']
    ordering = ['-unlocked_at']


@admin.register(ChildUnlockedAccessory)
class ChildUnlockedAccessoryAdmin(admin.ModelAdmin):
    list_display = ['child', 'accessory', 'unlocked_at', 'is_new']
    list_filter = ['unlocked_at', 'is_new']
    search_fields = ['child__name', 'accessory__name_english']
    ordering = ['-unlocked_at']


@admin.register(ChildUnlockedPhrase)
class ChildUnlockedPhraseAdmin(admin.ModelAdmin):
    list_display = ['child', 'phrase', 'unlocked_at', 'is_new']
    list_filter = ['unlocked_at', 'is_new']
    search_fields = ['child__name', 'phrase__code']
    ordering = ['-unlocked_at']


@admin.register(ChildEquippedAccessories)
class ChildEquippedAccessoriesAdmin(admin.ModelAdmin):
    list_display = ['child', 'accessory', 'slot', 'equipped_at']
    list_filter = ['slot', 'equipped_at']
    search_fields = ['child__name', 'accessory__name_english']
    ordering = ['-equipped_at']


# ===========================================
# DAILY CHALLENGES ADMIN
# ===========================================

@admin.register(DailyChallengeTemplate)
class DailyChallengeTemplateAdmin(admin.ModelAdmin):
    list_display = ['code', 'title_english', 'challenge_type', 'difficulty', 'target', 'xp_reward', 'coin_reward', 'is_active']
    list_filter = ['challenge_type', 'difficulty', 'is_active']
    search_fields = ['code', 'title_english', 'description_english']
    ordering = ['difficulty', 'code']
    fieldsets = (
        ('Basic Information', {
            'fields': ('code', 'title_english', 'description_english', 'challenge_type', 'icon')
        }),
        ('Challenge Parameters', {
            'fields': ('target', 'difficulty')
        }),
        ('Rewards', {
            'fields': ('xp_reward', 'coin_reward')
        }),
        ('Level Gating', {
            'fields': ('min_level', 'max_level')
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
    )


@admin.register(ChildDailyChallenge)
class ChildDailyChallengeAdmin(admin.ModelAdmin):
    list_display = ['child', 'template', 'date', 'progress', 'is_completed', 'reward_claimed']
    list_filter = ['date', 'is_completed', 'reward_claimed']
    search_fields = ['child__name', 'template__title_english']
    ordering = ['-date', 'child']


# Festival admin is in apps.festivals.admin
