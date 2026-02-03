"""Serializers for Peppi Chat API."""
from rest_framework import serializers

from .models import (
    PeppiConversation,
    PeppiChatMessage,
    PeppiEscalationReport,
    ChatMode,
    InputType,
    EscalationStatus,
)


class PeppiChatMessageSerializer(serializers.ModelSerializer):
    """Serializer for individual chat messages."""

    class Meta:
        model = PeppiChatMessage
        fields = [
            'id',
            'role',
            'content_primary',
            'content_romanized',
            'content_english',
            'audio_input_url',
            'audio_output_url',
            'input_type',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'role',
            'content_romanized',
            'content_english',
            'audio_output_url',
            'created_at',
        ]


class PeppiConversationSerializer(serializers.ModelSerializer):
    """Serializer for conversations."""

    messages = PeppiChatMessageSerializer(many=True, read_only=True)
    child_name = serializers.CharField(source='child.name', read_only=True)

    class Meta:
        model = PeppiConversation
        fields = [
            'id',
            'child_name',
            'mode',
            'language',
            'festival',
            'story',
            'lesson',
            'is_active',
            'messages_count',
            'created_at',
            'last_message_at',
            'messages',
        ]
        read_only_fields = [
            'id',
            'child_name',
            'is_active',
            'messages_count',
            'created_at',
            'last_message_at',
            'messages',
        ]


class PeppiConversationListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for conversation lists."""

    child_name = serializers.CharField(source='child.name', read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = PeppiConversation
        fields = [
            'id',
            'child_name',
            'mode',
            'language',
            'is_active',
            'messages_count',
            'created_at',
            'last_message_at',
            'last_message',
        ]

    def get_last_message(self, obj):
        last_msg = obj.messages.order_by('-created_at').first()
        if last_msg:
            return {
                'role': last_msg.role,
                'content': last_msg.content_primary[:100] + '...' if len(last_msg.content_primary) > 100 else last_msg.content_primary,
                'created_at': last_msg.created_at,
            }
        return None


class StartConversationSerializer(serializers.Serializer):
    """Serializer for starting a new conversation."""

    mode = serializers.ChoiceField(
        choices=ChatMode.choices,
        default=ChatMode.GENERAL,
        help_text="Conversation mode"
    )
    language = serializers.CharField(
        default='HINDI',
        help_text="Primary language for the conversation"
    )
    festival_id = serializers.UUIDField(
        required=False,
        allow_null=True,
        help_text="Festival ID for FESTIVAL_STORY mode"
    )
    story_id = serializers.UUIDField(
        required=False,
        allow_null=True,
        help_text="Story ID for FESTIVAL_STORY mode"
    )
    lesson_id = serializers.UUIDField(
        required=False,
        allow_null=True,
        help_text="Lesson ID for CURRICULUM_HELP mode"
    )

    def validate(self, data):
        # Festival and story IDs are now optional for FESTIVAL_STORY mode
        # Users can chat about stories in general without specific context
        return data


class SendMessageSerializer(serializers.Serializer):
    """Serializer for sending a chat message."""

    content = serializers.CharField(
        max_length=1000,
        help_text="Message content"
    )
    input_type = serializers.ChoiceField(
        choices=InputType.choices,
        default=InputType.TEXT,
        help_text="How the message was input"
    )
    audio_url = serializers.URLField(
        required=False,
        allow_blank=True,
        help_text="URL of voice recording (for voice input)"
    )

    def validate_content(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Message cannot be empty")
        return value.strip()


class SendVoiceMessageSerializer(serializers.Serializer):
    """Serializer for voice message input."""

    audio_file = serializers.FileField(
        help_text="Voice recording file (WAV, MP3, or WebM)"
    )
    language = serializers.CharField(
        default='HINDI',
        help_text="Expected language for speech recognition"
    )

    def validate_audio_file(self, value):
        # Validate file size (max 10MB)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("Audio file too large. Maximum size is 10MB.")

        # Validate content type
        allowed_types = ['audio/wav', 'audio/mp3', 'audio/mpeg', 'audio/webm', 'audio/ogg']
        if value.content_type not in allowed_types:
            raise serializers.ValidationError(
                f"Invalid audio format. Allowed formats: WAV, MP3, WebM, OGG"
            )

        return value


class ChatResponseSerializer(serializers.Serializer):
    """Serializer for chat response."""

    message = PeppiChatMessageSerializer()
    conversation_id = serializers.IntegerField()
    is_streaming = serializers.BooleanField(default=False)
    audio_url = serializers.URLField(required=False, allow_null=True)


class ConversationHistorySerializer(serializers.Serializer):
    """Serializer for conversation history response."""

    conversation = PeppiConversationSerializer()
    messages = PeppiChatMessageSerializer(many=True)
    has_more = serializers.BooleanField(default=False)
    total_messages = serializers.IntegerField()


class SubmitEscalationSerializer(serializers.Serializer):
    """Serializer for submitting an escalation report."""

    message_id = serializers.UUIDField(
        required=False,
        allow_null=True,
        help_text="ID of the message that triggered escalation"
    )
    description = serializers.CharField(
        max_length=1000,
        help_text="User description of the issue"
    )

    def validate_description(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Description cannot be empty")
        return value.strip()


class PeppiEscalationReportSerializer(serializers.ModelSerializer):
    """Serializer for escalation reports."""

    child_name = serializers.CharField(source='child.name', read_only=True)
    conversation_mode = serializers.CharField(source='mode', read_only=True)

    class Meta:
        model = PeppiEscalationReport
        fields = [
            'id',
            'child_name',
            'conversation',
            'message',
            'user_description',
            'conversation_mode',
            'status',
            'admin_response',
            'created_at',
            'resolved_at',
        ]
        read_only_fields = [
            'id',
            'child_name',
            'conversation',
            'message',
            'conversation_mode',
            'status',
            'admin_response',
            'created_at',
            'resolved_at',
        ]
