"""Speech admin configuration."""
from django.contrib import admin
from django.utils.html import format_html
from .models import AudioCache, TTSUsageLog


@admin.register(AudioCache)
class AudioCacheAdmin(admin.ModelAdmin):
    list_display = [
        'short_text',
        'language',
        'voice_style',
        'access_count',
        'audio_size_display',
        'generation_cost_usd',
        'created_at'
    ]
    list_filter = ['language', 'voice_style', 'created_at']
    search_fields = ['text_content', 'cache_key']
    readonly_fields = [
        'cache_key',
        'text_hash',
        'audio_url',
        'audio_size_bytes',
        'generation_time_ms',
        'generation_cost_usd',
        'access_count',
        'last_accessed_at'
    ]
    ordering = ['-created_at']

    def short_text(self, obj):
        return obj.text_content[:50] + '...' if len(obj.text_content) > 50 else obj.text_content
    short_text.short_description = 'Text'

    def audio_size_display(self, obj):
        if obj.audio_size_bytes:
            kb = obj.audio_size_bytes / 1024
            return f"{kb:.1f} KB"
        return "-"
    audio_size_display.short_description = 'Size'


@admin.register(TTSUsageLog)
class TTSUsageLogAdmin(admin.ModelAdmin):
    list_display = [
        'created_at',
        'language',
        'status_badge',
        'was_cached',
        'text_length',
        'response_time_ms',
        'estimated_cost_usd'
    ]
    list_filter = ['status', 'was_cached', 'language', 'created_at']
    ordering = ['-created_at']

    def status_badge(self, obj):
        colors = {
            'success': 'green',
            'cached': 'blue',
            'error': 'red'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.status.upper()
        )
    status_badge.short_description = 'Status'
