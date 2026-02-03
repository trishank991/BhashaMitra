"""Speech models for TTS caching and Peppi Mimic pronunciation practice."""
import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
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
        MARATHI = 'MARATHI', 'Marathi'
        ODIA = 'ODIA', 'Odia'
        ASSAMESE = 'ASSAMESE', 'Assamese'
        URDU = 'URDU', 'Urdu'
        FIJI_HINDI = 'FIJI_HINDI', 'Fiji Hindi'

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


class VoiceCharacter(TimeStampedModel):
    """
    Voice character profiles for TTS narration.

    Supports different character types (Peppi, Grandmother, Teacher, etc.)
    with customizable voice settings per language.

    Architecture supports:
    - Google TTS voices
    - Sarvam AI voices
    - Cloned voices (e.g., grandmother's voice via ElevenLabs/Replicate)
    - Custom voice providers
    """

    class CharacterType(models.TextChoices):
        PEPPI = 'PEPPI', 'Peppi (AI Tutor)'
        GRANDMOTHER = 'GRANDMOTHER', 'Grandmother'
        GRANDFATHER = 'GRANDFATHER', 'Grandfather'
        TEACHER = 'TEACHER', 'Teacher'
        NARRATOR = 'NARRATOR', 'Narrator'
        PARENT = 'PARENT', 'Parent'

    class Gender(models.TextChoices):
        MALE = 'MALE', 'Male'
        FEMALE = 'FEMALE', 'Female'
        NEUTRAL = 'NEUTRAL', 'Neutral'

    class VoiceSource(models.TextChoices):
        GOOGLE_TTS = 'GOOGLE_TTS', 'Google Cloud TTS'
        SARVAM_AI = 'SARVAM_AI', 'Sarvam AI (Indic)'
        CLONED = 'CLONED', 'Cloned Voice (ElevenLabs/Replicate)'
        CUSTOM = 'CUSTOM', 'Custom Provider'

    # Basic Info
    name = models.CharField(
        max_length=100,
        help_text="Character name in English (e.g., 'Peppi', 'Grandmother')"
    )
    name_native = models.CharField(
        max_length=100,
        blank=True,
        help_text="Character name in native script (e.g., 'पेप्पी', 'दादी')"
    )
    description = models.TextField(
        blank=True,
        help_text="Description of the character and voice style"
    )

    # Character Classification
    character_type = models.CharField(
        max_length=20,
        choices=CharacterType.choices,
        help_text="Type of character"
    )
    language = models.CharField(
        max_length=20,
        choices=AudioCache.Language.choices,
        help_text="Language for this voice character"
    )
    gender = models.CharField(
        max_length=10,
        choices=Gender.choices,
        help_text="Voice gender"
    )

    # Voice Configuration
    voice_source = models.CharField(
        max_length=20,
        choices=VoiceSource.choices,
        default=VoiceSource.SARVAM_AI,
        help_text="TTS provider/source for this voice"
    )
    voice_id = models.CharField(
        max_length=200,
        blank=True,
        help_text="External voice ID (e.g., ElevenLabs voice ID, Google voice name, Sarvam speaker)"
    )
    voice_model = models.CharField(
        max_length=100,
        blank=True,
        default='bulbul:v2',
        help_text="TTS model to use (e.g., 'bulbul:v2' for Sarvam)"
    )

    # Voice Characteristics (SSML/TTS settings)
    speaking_rate = models.FloatField(
        default=0.7,
        validators=[MinValueValidator(0.5), MaxValueValidator(2.0)],
        help_text="Speaking rate/pace: 0.5 (slow) to 2.0 (fast), 0.7 is balanced for children"
    )
    pitch = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(-20.0), MaxValueValidator(20.0)],
        help_text="Voice pitch adjustment: -20 to +20 semitones"
    )
    volume_gain_db = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(-10.0), MaxValueValidator(10.0)],
        help_text="Volume gain in decibels: -10 to +10 dB"
    )

    # Character Personality (used to enhance narration)
    warmth_phrases = models.JSONField(
        default=dict,
        blank=True,
        help_text="JSON object with warmth phrases per language"
    )
    personality_traits = models.JSONField(
        default=dict,
        blank=True,
        help_text="JSON object describing personality traits for AI prompt enhancement"
    )

    # Status
    is_active = models.BooleanField(
        default=True,
        help_text="Is this voice character available for use?"
    )
    is_default = models.BooleanField(
        default=False,
        help_text="Is this the default voice for this character type and language?"
    )

    # Cloned Voice Metadata (for future integration)
    cloned_from_user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cloned_voices',
        help_text="User who provided voice samples for cloning (e.g., parent/grandparent)"
    )
    clone_quality_score = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Quality score of cloned voice (0.0 to 1.0)"
    )
    clone_sample_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of voice samples used for cloning"
    )

    class Meta:
        db_table = 'voice_characters'
        verbose_name = 'Voice Character'
        verbose_name_plural = 'Voice Characters'
        indexes = [
            models.Index(fields=['character_type', 'language']),
            models.Index(fields=['language', 'is_active']),
            models.Index(fields=['voice_source']),
            models.Index(fields=['is_default']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['character_type', 'language', 'gender'],
                condition=models.Q(is_default=True),
                name='unique_default_per_character_language_gender'
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.get_character_type_display()}) - {self.language} - {self.gender}"

    def get_voice_config(self) -> dict:
        """Get voice configuration dict for TTS provider."""
        config = {
            'character_type': self.character_type,
            'language': self.language,
            'gender': self.gender,
            'voice_source': self.voice_source,
            'speaking_rate': self.speaking_rate,
            'pitch': self.pitch,
            'volume_gain_db': self.volume_gain_db,
        }

        if self.voice_source == self.VoiceSource.SARVAM_AI:
            config['speaker'] = self.voice_id or ('anushka' if self.gender == self.Gender.FEMALE else 'arvind')
            config['model'] = self.voice_model or 'bulbul:v2'
            config['pace'] = self.speaking_rate
        elif self.voice_source == self.VoiceSource.GOOGLE_TTS:
            config['voice_name'] = self.voice_id
            config['speed'] = self.speaking_rate
        elif self.voice_source == self.VoiceSource.CLONED:
            config['voice_id'] = self.voice_id
            config['model'] = self.voice_model

        return config

    def get_warmth_phrases(self, category: str = None) -> list:
        """Get warmth phrases for this character."""
        if not self.warmth_phrases:
            return []

        if category and category in self.warmth_phrases:
            return self.warmth_phrases.get(category, [])

        all_phrases = []
        for phrases_list in self.warmth_phrases.values():
            if isinstance(phrases_list, list):
                all_phrases.extend(phrases_list)
        return all_phrases


class PeppiMimicChallenge(TimeStampedModel):
    """
    Pronunciation challenges for Peppi Mimic feature.
    Kids listen to Peppi say a word, then record their own pronunciation.
    """

    class Category(models.TextChoices):
        GREETING = 'GREETING', 'Greetings'
        FAMILY = 'FAMILY', 'Family Words'
        FOOD = 'FOOD', 'Food & Drink'
        NUMBERS = 'NUMBERS', 'Numbers'
        COLORS = 'COLORS', 'Colors'
        ANIMALS = 'ANIMALS', 'Animals'
        FESTIVAL = 'FESTIVAL', 'Festival Words'
        DAILY = 'DAILY', 'Daily Words'
        ACTIONS = 'ACTIONS', 'Action Words'
        BODY = 'BODY', 'Body Parts'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Content
    word = models.CharField(max_length=100, help_text="Word in native script")
    romanization = models.CharField(max_length=100, help_text="Transliteration")
    meaning = models.CharField(max_length=200, help_text="English meaning")
    language = models.CharField(max_length=20, choices=AudioCache.Language.choices)

    # Audio - reference pronunciation
    audio_url = models.URLField(blank=True, help_text="Peppi's pronunciation audio URL")
    audio_cache = models.ForeignKey(
        'AudioCache',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mimic_challenges',
        help_text="Link to cached audio"
    )

    # Metadata
    category = models.CharField(max_length=20, choices=Category.choices)
    difficulty = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        help_text="1=Easy, 2=Medium, 3=Hard"
    )
    display_order = models.IntegerField(default=0)
    points_reward = models.PositiveIntegerField(default=25, help_text="Base points for completing")

    # Peppi Scripts - what Peppi says
    peppi_intro = models.TextField(
        blank=True,
        help_text="What Peppi says before (e.g., 'Listen carefully!')"
    )
    peppi_perfect = models.TextField(
        blank=True,
        help_text="3-star response (e.g., 'PERFECT! You're amazing!')"
    )
    peppi_good = models.TextField(
        blank=True,
        help_text="2-star response (e.g., 'Very good! Almost there!')"
    )
    peppi_try_again = models.TextField(
        blank=True,
        help_text="1-star or less response (e.g., 'Good try! Let's practice more!')"
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'peppi_mimic_challenges'
        ordering = ['category', 'difficulty', 'display_order']
        indexes = [
            models.Index(fields=['language', 'category']),
            models.Index(fields=['language', 'difficulty']),
            models.Index(fields=['is_active']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['word', 'language'],
                name='unique_word_per_language'
            )
        ]

    def __str__(self):
        return f"{self.word} ({self.romanization}) - {self.language}"


class PeppiMimicAttempt(TimeStampedModel):
    """Record of a child's pronunciation attempt."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    child = models.ForeignKey(
        'children.Child',
        on_delete=models.CASCADE,
        related_name='mimic_attempts'
    )
    challenge = models.ForeignKey(
        PeppiMimicChallenge,
        on_delete=models.CASCADE,
        related_name='attempts'
    )

    # Recording
    audio_url = models.URLField(help_text="Child's recording URL")
    duration_ms = models.PositiveIntegerField(default=0, help_text="Recording duration in ms")

    # Scoring (from STT analysis)
    stt_transcription = models.CharField(
        max_length=200,
        blank=True,
        help_text="What STT heard"
    )
    stt_confidence = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="STT confidence 0-1"
    )
    text_match_score = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Text similarity score 0-100"
    )
    final_score = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Combined final score 0-100"
    )
    stars = models.PositiveSmallIntegerField(
        default=0,
        validators=[MaxValueValidator(3)],
        help_text="Star rating 0-3"
    )

    # Acoustic Analysis (v2 scoring)
    audio_energy_score = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="RMS energy analysis score 0-100"
    )
    duration_match_score = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Duration similarity to reference 0-100"
    )
    scoring_version = models.PositiveSmallIntegerField(
        default=2,
        help_text="Scoring algorithm version (1=STT+text, 2=hybrid with acoustic)"
    )

    # Points
    points_earned = models.PositiveIntegerField(default=0)
    is_personal_best = models.BooleanField(default=False)

    # Sharing
    shared_to_family = models.BooleanField(default=False)
    shared_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'peppi_mimic_attempts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['child', 'challenge']),
            models.Index(fields=['child', 'created_at']),
            models.Index(fields=['stars']),
        ]

    def __str__(self):
        return f"{self.child.name} - {self.challenge.word} ({self.stars} stars)"


class PeppiMimicProgress(TimeStampedModel):
    """Track child's overall progress on each challenge."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    child = models.ForeignKey(
        'children.Child',
        on_delete=models.CASCADE,
        related_name='mimic_progress'
    )
    challenge = models.ForeignKey(
        PeppiMimicChallenge,
        on_delete=models.CASCADE,
        related_name='child_progress'
    )

    # Best Performance
    best_score = models.FloatField(default=0)
    best_stars = models.PositiveSmallIntegerField(default=0)
    best_attempt = models.ForeignKey(
        PeppiMimicAttempt,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )

    # Stats
    total_attempts = models.PositiveIntegerField(default=0)
    total_points = models.PositiveIntegerField(default=0)

    # Mastery
    mastered = models.BooleanField(default=False, help_text="3 stars achieved")
    mastered_at = models.DateTimeField(null=True, blank=True)

    # Streak tracking
    current_streak = models.PositiveIntegerField(default=0, help_text="Current consecutive day streak")
    longest_streak = models.PositiveIntegerField(default=0, help_text="Longest streak achieved")
    last_attempt_date = models.DateField(null=True, blank=True, help_text="Date of last attempt for streak tracking")

    class Meta:
        db_table = 'peppi_mimic_progress'
        unique_together = ['child', 'challenge']
        indexes = [
            models.Index(fields=['child', 'mastered']),
        ]

    def __str__(self):
        status = "Mastered" if self.mastered else f"{self.best_stars} stars"
        return f"{self.child.name} - {self.challenge.word}: {status}"

    def update_from_attempt(self, attempt: PeppiMimicAttempt) -> bool:
        """
        Update progress from a new attempt.
        Returns True if this was a personal best.
        """
        from django.utils import timezone
        from datetime import timedelta

        self.total_attempts += 1
        self.total_points += attempt.points_earned

        is_personal_best = attempt.final_score > self.best_score

        if is_personal_best:
            self.best_score = attempt.final_score
            self.best_stars = attempt.stars
            self.best_attempt = attempt

        # Check for mastery (3 stars)
        if attempt.stars == 3 and not self.mastered:
            self.mastered = True
            self.mastered_at = timezone.now()

        # Update streak tracking
        today = timezone.now().date()
        if self.last_attempt_date is None:
            # First attempt ever
            self.current_streak = 1
        elif self.last_attempt_date == today:
            # Same day, no streak change
            pass
        elif self.last_attempt_date == today - timedelta(days=1):
            # Consecutive day - increase streak
            self.current_streak += 1
        else:
            # Streak broken - reset to 1
            self.current_streak = 1

        # Update longest streak
        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak

        self.last_attempt_date = today

        self.save()
        return is_personal_best


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
