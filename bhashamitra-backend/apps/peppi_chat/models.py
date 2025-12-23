"""Peppi Chat models for conversation management."""
from django.db import models
from apps.core.models import TimeStampedModel


class ChatMode(models.TextChoices):
    """Chat mode choices."""
    FESTIVAL_STORY = 'FESTIVAL_STORY', 'Festival Story'
    CURRICULUM_HELP = 'CURRICULUM_HELP', 'Curriculum Help'
    GENERAL = 'GENERAL', 'General'


class MessageRole(models.TextChoices):
    """Message role choices."""
    USER = 'user', 'User'
    ASSISTANT = 'assistant', 'Assistant'
    SYSTEM = 'system', 'System'


class InputType(models.TextChoices):
    """Input type choices."""
    TEXT = 'text', 'Text'
    VOICE = 'voice', 'Voice'


class ModerationAction(models.TextChoices):
    """Moderation action choices."""
    BLOCKED = 'BLOCKED', 'Blocked'
    MODIFIED = 'MODIFIED', 'Modified'
    FLAGGED = 'FLAGGED', 'Flagged'
    ALLOWED = 'ALLOWED', 'Allowed'


class Severity(models.TextChoices):
    """Severity level choices."""
    LOW = 'LOW', 'Low'
    MEDIUM = 'MEDIUM', 'Medium'
    HIGH = 'HIGH', 'High'
    CRITICAL = 'CRITICAL', 'Critical'


class PeppiConversation(TimeStampedModel):
    """
    Stores Peppi AI chat conversation sessions.

    Each conversation belongs to a child and can be in one of three modes:
    - FESTIVAL_STORY: Interactive storytelling about festivals
    - CURRICULUM_HELP: Help with vocabulary, grammar, lessons
    - GENERAL: General chat within learning topics
    """

    child = models.ForeignKey(
        'children.Child',
        on_delete=models.CASCADE,
        related_name='peppi_conversations',
        help_text='The child participating in this conversation'
    )
    mode = models.CharField(
        max_length=20,
        choices=ChatMode.choices,
        default=ChatMode.GENERAL,
        help_text='The conversation mode'
    )

    # Context references (for mode-specific conversations)
    festival = models.ForeignKey(
        'festivals.Festival',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='peppi_conversations',
        help_text='Festival for FESTIVAL_STORY mode'
    )
    story = models.ForeignKey(
        'stories.Story',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='peppi_conversations',
        help_text='Story being narrated'
    )
    lesson = models.ForeignKey(
        'curriculum.Lesson',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='peppi_conversations',
        help_text='Lesson for CURRICULUM_HELP mode'
    )

    # Status
    is_active = models.BooleanField(
        default=True,
        help_text='Whether the conversation is still active'
    )

    # Metrics
    messages_count = models.PositiveIntegerField(
        default=0,
        help_text='Total messages in this conversation'
    )
    total_tokens_used = models.PositiveIntegerField(
        default=0,
        help_text='Total tokens consumed by this conversation'
    )

    # Language
    language = models.CharField(
        max_length=20,
        default='HINDI',
        help_text='Primary language for this conversation'
    )

    # Context snapshot for resuming (stores serialized context)
    context_snapshot = models.JSONField(
        default=dict,
        blank=True,
        help_text='Serialized context for conversation resumption'
    )

    # Timestamps
    last_message_at = models.DateTimeField(
        auto_now=True,
        help_text='When the last message was sent'
    )
    ended_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When the conversation was ended'
    )

    class Meta:
        db_table = 'peppi_conversations'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['child', 'is_active']),
            models.Index(fields=['mode']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Peppi Chat: {self.child.name} - {self.mode} ({self.created_at.date()})"

    def end_conversation(self):
        """Mark the conversation as ended."""
        from django.utils import timezone
        self.is_active = False
        self.ended_at = timezone.now()
        self.save(update_fields=['is_active', 'ended_at'])


class PeppiChatMessage(TimeStampedModel):
    """
    Individual chat messages in a Peppi conversation.

    Stores multi-language content and optional audio references.
    """

    conversation = models.ForeignKey(
        PeppiConversation,
        on_delete=models.CASCADE,
        related_name='messages',
        help_text='The conversation this message belongs to'
    )
    role = models.CharField(
        max_length=10,
        choices=MessageRole.choices,
        help_text='Who sent this message'
    )

    # Multi-language content
    content_primary = models.TextField(
        help_text='Primary language content (e.g., Hindi)'
    )
    content_romanized = models.TextField(
        blank=True,
        help_text='Romanized version of the content'
    )
    content_english = models.TextField(
        blank=True,
        help_text='English translation/version'
    )

    # Voice support
    audio_input_url = models.URLField(
        blank=True,
        help_text='URL of the user voice recording (for voice input)'
    )
    audio_output_url = models.URLField(
        blank=True,
        help_text='URL of Peppi TTS response audio'
    )

    # Metadata
    input_type = models.CharField(
        max_length=10,
        choices=InputType.choices,
        default=InputType.TEXT,
        help_text='How the message was input'
    )
    token_count = models.PositiveIntegerField(
        default=0,
        help_text='Token count for this message'
    )
    latency_ms = models.PositiveIntegerField(
        default=0,
        help_text='Response latency in milliseconds'
    )

    # Moderation
    was_moderated = models.BooleanField(
        default=False,
        help_text='Whether this message was modified by moderation'
    )
    original_content = models.TextField(
        blank=True,
        help_text='Original content before moderation (if moderated)'
    )

    class Meta:
        db_table = 'peppi_chat_messages'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversation', 'created_at']),
            models.Index(fields=['role']),
        ]

    def __str__(self):
        preview = self.content_primary[:50] + '...' if len(self.content_primary) > 50 else self.content_primary
        return f"{self.role}: {preview}"


class PeppiSafetyLog(TimeStampedModel):
    """
    Logs content moderation actions for audit and compliance.

    Records all moderation events including blocked, modified, and flagged content.
    """

    conversation = models.ForeignKey(
        PeppiConversation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='safety_logs',
        help_text='The conversation where this occurred'
    )
    child = models.ForeignKey(
        'children.Child',
        on_delete=models.CASCADE,
        related_name='peppi_safety_logs',
        help_text='The child involved'
    )

    # Action details
    action = models.CharField(
        max_length=20,
        choices=ModerationAction.choices,
        help_text='What action was taken'
    )

    # Content
    input_content = models.TextField(
        help_text='The original input content'
    )
    output_content = models.TextField(
        blank=True,
        help_text='The modified output (if applicable)'
    )

    # Details
    reason = models.TextField(
        help_text='Reason for the moderation action'
    )
    matched_patterns = models.JSONField(
        default=list,
        blank=True,
        help_text='List of patterns that triggered moderation'
    )
    severity = models.CharField(
        max_length=10,
        choices=Severity.choices,
        default=Severity.LOW,
        help_text='Severity level of the content'
    )

    # Review status
    reviewed = models.BooleanField(
        default=False,
        help_text='Whether this has been reviewed by admin'
    )
    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When it was reviewed'
    )
    reviewed_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_safety_logs',
        help_text='Admin who reviewed this'
    )
    review_notes = models.TextField(
        blank=True,
        help_text='Notes from the review'
    )

    class Meta:
        db_table = 'peppi_safety_logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['child', 'created_at']),
            models.Index(fields=['action']),
            models.Index(fields=['severity']),
            models.Index(fields=['reviewed']),
        ]

    def __str__(self):
        return f"Safety Log: {self.action} - {self.child.name} ({self.created_at.date()})"


class PeppiChatUsage(TimeStampedModel):
    """
    Tracks daily chat usage per child for rate limiting.
    """

    child = models.ForeignKey(
        'children.Child',
        on_delete=models.CASCADE,
        related_name='peppi_chat_usage',
        help_text='The child'
    )
    date = models.DateField(
        help_text='The date of usage'
    )

    # Usage counts
    messages_sent = models.PositiveIntegerField(
        default=0,
        help_text='Messages sent today'
    )
    conversations_started = models.PositiveIntegerField(
        default=0,
        help_text='Conversations started today'
    )
    voice_messages_sent = models.PositiveIntegerField(
        default=0,
        help_text='Voice messages sent today'
    )
    tokens_used = models.PositiveIntegerField(
        default=0,
        help_text='Total tokens used today'
    )

    class Meta:
        db_table = 'peppi_chat_usage'
        unique_together = ['child', 'date']
        indexes = [
            models.Index(fields=['child', 'date']),
        ]

    def __str__(self):
        return f"Usage: {self.child.name} on {self.date} - {self.messages_sent} msgs"

    @classmethod
    def get_or_create_today(cls, child):
        """Get or create usage record for today."""
        from django.utils import timezone
        today = timezone.now().date()
        usage, _ = cls.objects.get_or_create(child=child, date=today)
        return usage

    def increment_messages(self):
        """Increment message count."""
        self.messages_sent += 1
        self.save(update_fields=['messages_sent'])

    def increment_conversations(self):
        """Increment conversation count."""
        self.conversations_started += 1
        self.save(update_fields=['conversations_started'])


class EscalationStatus(models.TextChoices):
    """Escalation status choices."""
    PENDING = 'PENDING', 'Pending'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    RESOLVED = 'RESOLVED', 'Resolved'
    CLOSED = 'CLOSED', 'Closed'


class PeppiEscalationReport(TimeStampedModel):
    """
    Stores escalation reports when Peppi cannot help.

    When Peppi's response includes [NEEDS_ESCALATION], the user can
    submit a report explaining their issue for the tech team to review.
    """

    conversation = models.ForeignKey(
        PeppiConversation,
        on_delete=models.CASCADE,
        related_name='escalation_reports',
        help_text='The conversation where escalation was needed'
    )
    child = models.ForeignKey(
        'children.Child',
        on_delete=models.CASCADE,
        related_name='peppi_escalation_reports',
        help_text='The child who needed help'
    )
    message = models.ForeignKey(
        PeppiChatMessage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='escalation_reports',
        help_text='The message that triggered escalation'
    )

    # User report
    user_description = models.TextField(
        help_text='User description of the issue/error'
    )
    mode = models.CharField(
        max_length=20,
        choices=ChatMode.choices,
        help_text='The chat mode when escalation occurred'
    )

    # Status tracking
    status = models.CharField(
        max_length=20,
        choices=EscalationStatus.choices,
        default=EscalationStatus.PENDING,
        help_text='Current status of the escalation'
    )

    # Admin response
    admin_response = models.TextField(
        blank=True,
        help_text='Response from the tech team'
    )
    resolved_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resolved_escalations',
        help_text='Admin who resolved this'
    )
    resolved_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When the escalation was resolved'
    )

    class Meta:
        db_table = 'peppi_escalation_reports'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['child', 'created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['conversation']),
        ]

    def __str__(self):
        return f"Escalation: {self.child.name} - {self.mode} ({self.status})"
