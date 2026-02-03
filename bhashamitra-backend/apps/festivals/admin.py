"""Festival admin."""
from django.contrib import admin
from apps.festivals.models import Festival, FestivalStory, FestivalActivity, FestivalProgress


@admin.register(Festival)
class FestivalAdmin(admin.ModelAdmin):
    """Admin for Festival model."""

    list_display = [
        'name',
        'name_native',
        'religion',
        'typical_month',
        'is_lunar_calendar',
        'is_active',
        'created_at'
    ]
    list_filter = ['religion', 'typical_month', 'is_lunar_calendar', 'is_active']
    search_fields = ['name', 'name_native', 'name_hindi', 'name_tamil', 'description']
    ordering = ['typical_month', 'name']
    readonly_fields = ['id', 'created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'name', 'name_native', 'religion')
        }),
        ('Multi-Language Names', {
            'fields': (
                'name_hindi',
                'name_tamil',
                'name_gujarati',
                'name_punjabi',
                'name_telugu',
                'name_malayalam'
            ),
            'classes': ('collapse',)
        }),
        ('Details', {
            'fields': ('description', 'significance', 'typical_month', 'is_lunar_calendar', 'image_url')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FestivalStory)
class FestivalStoryAdmin(admin.ModelAdmin):
    """Admin for FestivalStory junction model."""

    list_display = ['festival', 'story', 'is_primary']
    list_filter = ['is_primary', 'festival__religion']
    search_fields = ['festival__name', 'story__title']
    autocomplete_fields = ['festival', 'story']
    ordering = ['festival__name', '-is_primary']

    fieldsets = (
        ('Link Information', {
            'fields': ('festival', 'story', 'is_primary')
        }),
    )


@admin.register(FestivalActivity)
class FestivalActivityAdmin(admin.ModelAdmin):
    """Admin for FestivalActivity model."""

    list_display = [
        'title',
        'festival',
        'activity_type',
        'min_age',
        'max_age',
        'difficulty_level',
        'points_reward',
        'is_active'
    ]
    list_filter = [
        'activity_type',
        'difficulty_level',
        'is_active',
        'festival__religion',
        'min_age',
        'max_age'
    ]
    search_fields = ['title', 'description', 'festival__name']
    autocomplete_fields = ['festival']
    ordering = ['festival__name', 'activity_type', 'title']
    readonly_fields = ['id', 'created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'festival', 'title', 'activity_type')
        }),
        ('Content', {
            'fields': ('description', 'instructions', 'materials_needed')
        }),
        ('Age & Difficulty', {
            'fields': ('min_age', 'max_age', 'difficulty_level', 'duration_minutes')
        }),
        ('Media', {
            'fields': ('image_url', 'video_url')
        }),
        ('Gamification', {
            'fields': ('points_reward',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FestivalProgress)
class FestivalProgressAdmin(admin.ModelAdmin):
    """Admin for FestivalProgress model."""

    list_display = [
        'child',
        'festival',
        'activity',
        'story',
        'is_completed',
        'points_earned',
        'completed_at'
    ]
    list_filter = [
        'is_completed',
        'festival__religion',
        'created_at',
        'completed_at'
    ]
    search_fields = ['child__name', 'festival__name', 'activity__title', 'story__title']
    autocomplete_fields = ['child', 'festival', 'activity', 'story']
    ordering = ['-created_at']
    readonly_fields = ['id', 'points_earned', 'completed_at', 'created_at', 'updated_at']
    actions = ['mark_as_completed']

    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'child', 'festival')
        }),
        ('Activity/Story', {
            'fields': ('activity', 'story')
        }),
        ('Progress', {
            'fields': ('is_completed', 'completed_at', 'points_earned', 'notes')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    @admin.action(description='Mark selected progress as completed')
    def mark_as_completed(self, request, queryset):
        """Bulk action to mark progress items as completed."""
        count = 0
        for progress in queryset:
            if not progress.is_completed:
                progress.mark_complete()
                count += 1

        self.message_user(
            request,
            f'{count} progress item(s) marked as completed.'
        )
