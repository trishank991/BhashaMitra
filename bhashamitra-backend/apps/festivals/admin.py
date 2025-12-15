"""Festival admin."""
from django.contrib import admin
from apps.festivals.models import Festival, FestivalStory


@admin.register(Festival)
class FestivalAdmin(admin.ModelAdmin):
    """Admin for Festival model."""

    list_display = ['name', 'name_native', 'religion', 'typical_month', 'is_active', 'created_at']
    list_filter = ['religion', 'typical_month', 'is_active']
    search_fields = ['name', 'name_native', 'description']
    ordering = ['typical_month', 'name']
    readonly_fields = ['id', 'created_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'name', 'name_native', 'religion')
        }),
        ('Details', {
            'fields': ('description', 'typical_month', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at',)
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
