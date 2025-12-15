"""Speech models for TTS caching."""
import uuid
from django.db import models
from apps.core.models import TimeStampedModel


class AudioCache(TimeStampedModel):
    """
    Permanent cache for generated TTS audio files.
    Once generated, audio is stored forever and served from cache.

    Three-tier TTS architecture:
    1. Cache (instant, free)
    2. Replicate.com (fast, cheap)
    3. Google Cloud TTS (reliable fallback)
    """

    class Language(models.TextChoices):
        HINDI = 'HINDI', 'Hindi'
        TAMIL = 'TAMIL', 'Tamil'
        GUJARATI = 'GUJARATI', 'Gujarati'
        PUNJABI = 'PUNJABI', 'Punjabi'
        TELUGU = 'TELUGU', 'Telugu'
        MALAYALAM = 'MALAYALAM', 'Malayalam'
        BENGALI = 'BENGALI', 'Bengali'
        KANNADA = 'KANNADA', 'Kannada'

    class VoiceStyle(models.TextChoices):
        STORYTELLER = 'storyteller', 'Storyteller (Warm & Engaging)'
        CALM = 'calm', 'Calm (Soft & Soothing)'
        ENTHUSIASTIC = 'enthusiastic', 'Enthusiastic (Energetic)'
        KID_FRIENDLY = 'kid_friendly', 'Kid Friendly (Default)'
        DEFAULT = 'default', 'Default'

    class Provider(models.TextChoices):
        CACHE = 'cache', 'Pre-generated Cache'
        REPLICATE = 'replicate', 'Replicate.com'
        GOOGLE = 'google', 'Google Cloud TTS'
        SVARA = 'svara', 'Svara TTS (Legacy)'
        MMS = 'mms', 'Facebook MMS'

    # Unique identifier for this audio
    cache_key = models.CharField(max_length=64, unique=True, db_index=True)

    # Content details
    text_content = models.TextField(help_text="Original text that was converted to speech")
    text_hash = models.CharField(max_length=64, db_index=True, help_text="MD5 hash of text for lookup")
    language = models.CharField(max_length=20, choices=Language.choices)
    voice_style = models.CharField(max_length=20, choices=VoiceStyle.choices, default=VoiceStyle.STORYTELLER)

    # Provider that generated this audio
    provider = models.CharField(
        max_length=20,
        choices=Provider.choices,
        default=Provider.CACHE
    )

    # Audio file details
    audio_file = models.FileField(upload_to='audio_cache/', blank=True)
    audio_url = models.URLField(blank=True, help_text="URL to the cached audio file")
    audio_duration_ms = models.IntegerField(default=0, help_text="Duration in milliseconds")
    audio_size_bytes = models.IntegerField(default=0, help_text="File size in bytes")
    audio_format = models.CharField(max_length=10, default='wav')
    sample_rate = models.IntegerField(default=22050)

    # Content type for curriculum linking
    content_type = models.CharField(max_length=50, blank=True)  # 'alphabet', 'vocabulary', 'phrase'
    content_id = models.CharField(max_length=50, blank=True)

    # Usage tracking
    access_count = models.IntegerField(default=0, help_text="Number of times this audio was accessed")
    last_accessed_at = models.DateTimeField(auto_now=True)

    # Generation metadata
    generation_time_ms = models.IntegerField(default=0, help_text="Time taken to generate in ms")
    generation_cost_usd = models.DecimalField(max_digits=10, decimal_places=6, default=0)

    # Optional: Link to story page (for pre-warming)
    story = models.ForeignKey(
        'stories.Story',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audio_cache'
    )
    page_number = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'audio_cache'
        verbose_name = 'Audio Cache'
        verbose_name_plural = 'Audio Cache Entries'
        indexes = [
            models.Index(fields=['language', 'voice_style']),
            models.Index(fields=['story', 'page_number']),
            models.Index(fields=['text_hash']),
            models.Index(fields=['content_type', 'content_id']),
            models.Index(fields=['provider']),
        ]

    def __str__(self):
        return f"{self.language} - {self.text_content[:50]}..."

    def increment_access(self):
        """Increment access count (called when audio is served)"""
        self.access_count += 1
        self.save(update_fields=['access_count', 'last_accessed_at'])


class TTSUsageLog(TimeStampedModel):
    """Track TTS API usage for cost monitoring."""

    class Status(models.TextChoices):
        SUCCESS = 'success', 'Success'
        CACHED = 'cached', 'Served from Cache'
        ERROR = 'error', 'Error'

    # Request details
    text_length = models.IntegerField()
    language = models.CharField(max_length=20)
    voice_style = models.CharField(max_length=20, default='default')
    provider = models.CharField(max_length=20, default='cache')

    # Response details
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SUCCESS)
    was_cached = models.BooleanField(default=False)
    response_time_ms = models.IntegerField(default=0)
    success = models.BooleanField(default=True)

    # Cost tracking (in USD cents for precision)
    estimated_cost_usd = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    estimated_cost_cents = models.DecimalField(max_digits=10, decimal_places=4, default=0)

    # Error details (if any)
    error_message = models.TextField(blank=True)

    # User tracking (optional)
    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'tts_usage_log'
        verbose_name = 'TTS Usage Log'
        verbose_name_plural = 'TTS Usage Logs'
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['provider', 'was_cached']),
        ]
