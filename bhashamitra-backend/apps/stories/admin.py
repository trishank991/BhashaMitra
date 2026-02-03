"""Stories admin configuration."""
from django.contrib import admin
from .models import Story, StoryPage


class StoryPageInline(admin.TabularInline):
    model = StoryPage
    extra = 0
    fields = ['page_number', 'text_content', 'image_url', 'audio_url']


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'language', 'level', 'page_count', 'author', 'cached_at']
    list_filter = ['language', 'level', 'cached_at']
    search_fields = ['title', 'author', 'storyweaver_id']
    ordering = ['-cached_at']
    inlines = [StoryPageInline]
    readonly_fields = ['cached_at', 'last_accessed_at', 'created_at', 'updated_at']
