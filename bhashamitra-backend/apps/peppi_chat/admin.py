"""Admin configuration for Peppi Chat models."""
from django.contrib import admin
from django.utils.html import format_html

from .models import (
    PeppiConversation,
    PeppiChatMessage,
    PeppiSafetyLog,
    PeppiChatUsage,
)


@admin.register(PeppiConversation)
class PeppiConversationAdmin(admin.ModelAdmin):
    """Admin for Peppi conversations."""

    list_display = [
        'id',
        'child_name',
        'mode',
        'language',
        'messages_count',
        'is_active',
        'created_at',
    ]
    list_filter = ['mode', 'language', 'is_active', 'created_at']
    search_fields = ['child__name', 'child__user__email']
    readonly_fields = ['created_at', 'updated_at', 'last_message_at']
    raw_id_fields = ['child', 'festival', 'story', 'lesson']

    def child_name(self, obj):
        return obj.child.name
    child_name.short_description = 'Child'


class PeppiChatMessageInline(admin.TabularInline):
    """Inline for chat messages in conversation admin."""
    model = PeppiChatMessage
    extra = 0
    readonly_fields = ['role', 'content_primary', 'input_type', 'created_at']
    can_delete = False


@admin.register(PeppiChatMessage)
class PeppiChatMessageAdmin(admin.ModelAdmin):
    """Admin for individual chat messages."""

    list_display = [
        'id',
        'conversation_id',
        'role',
        'content_preview',
        'input_type',
        'was_moderated',
        'created_at',
    ]
    list_filter = ['role', 'input_type', 'was_moderated', 'created_at']
    search_fields = ['content_primary', 'conversation__child__name']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['conversation']

    def content_preview(self, obj):
        content = obj.content_primary
        if len(content) > 50:
            return content[:50] + '...'
        return content
    content_preview.short_description = 'Content'


@admin.register(PeppiSafetyLog)
class PeppiSafetyLogAdmin(admin.ModelAdmin):
    """Admin for safety/moderation logs."""

    list_display = [
        'id',
        'child_name',
        'action_badge',
        'severity_badge',
        'reason_preview',
        'reviewed',
        'created_at',
    ]
    list_filter = ['action', 'severity', 'reviewed', 'created_at']
    search_fields = ['child__name', 'reason', 'input_content']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['conversation', 'child', 'reviewed_by']

    fieldsets = (
        ('Basic Info', {
            'fields': ('conversation', 'child', 'action', 'severity')
        }),
        ('Content', {
            'fields': ('input_content', 'output_content', 'reason', 'matched_patterns')
        }),
        ('Review', {
            'fields': ('reviewed', 'reviewed_at', 'reviewed_by', 'review_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def child_name(self, obj):
        return obj.child.name
    child_name.short_description = 'Child'

    def action_badge(self, obj):
        colors = {
            'BLOCKED': 'red',
            'MODIFIED': 'orange',
            'FLAGGED': 'yellow',
            'ALLOWED': 'green',
        }
        color = colors.get(obj.action, 'gray')
        return format_html(
            '<span style="background-color: {}; padding: 2px 8px; '
            'border-radius: 4px; color: white;">{}</span>',
            color, obj.action
        )
    action_badge.short_description = 'Action'

    def severity_badge(self, obj):
        colors = {
            'CRITICAL': 'darkred',
            'HIGH': 'red',
            'MEDIUM': 'orange',
            'LOW': 'green',
        }
        color = colors.get(obj.severity, 'gray')
        return format_html(
            '<span style="background-color: {}; padding: 2px 8px; '
            'border-radius: 4px; color: white;">{}</span>',
            color, obj.severity
        )
    severity_badge.short_description = 'Severity'

    def reason_preview(self, obj):
        if len(obj.reason) > 50:
            return obj.reason[:50] + '...'
        return obj.reason
    reason_preview.short_description = 'Reason'

    actions = ['mark_reviewed']

    @admin.action(description='Mark selected logs as reviewed')
    def mark_reviewed(self, request, queryset):
        from django.utils import timezone
        queryset.update(
            reviewed=True,
            reviewed_at=timezone.now(),
            reviewed_by=request.user
        )


@admin.register(PeppiChatUsage)
class PeppiChatUsageAdmin(admin.ModelAdmin):
    """Admin for daily usage tracking."""

    list_display = [
        'id',
        'child_name',
        'date',
        'messages_sent',
        'conversations_started',
        'voice_messages_sent',
        'tokens_used',
    ]
    list_filter = ['date']
    search_fields = ['child__name']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['child']
    date_hierarchy = 'date'

    def child_name(self, obj):
        return obj.child.name
    child_name.short_description = 'Child'
