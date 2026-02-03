"""Peppi AI companion models."""
from django.db import models
from apps.core.models import TimeStampedModel


class PeppiPhrase(TimeStampedModel):
    """Peppi feedback phrases for different scenarios."""

    class Category(models.TextChoices):
        CORRECT = 'correct', 'Correct Answer'
        WRONG = 'wrong', 'Wrong Answer'
        STREAK = 'streak', 'Streak Celebration'
        GREETING = 'greeting', 'Greeting'
        FAREWELL = 'farewell', 'Farewell'
        ENCOURAGEMENT = 'encouragement', 'Encouragement'
        COMPLETION = 'completion', 'Completion'
        BADGE = 'badge', 'Badge Earned'

    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        help_text='Phrase category'
    )
    text_hindi = models.TextField(help_text='Hindi/Hinglish text')
    text_english = models.TextField(blank=True, help_text='English translation')
    text_romanized = models.TextField(blank=True, help_text='Romanized text')
    audio_file = models.CharField(max_length=255, blank=True, help_text='Audio file path')
    streak_count = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text='Streak count for streak phrases'
    )
    context = models.CharField(
        max_length=50,
        blank=True,
        help_text='Context (e.g., morning, afternoon, return)'
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'peppi_phrases'
        ordering = ['category', 'id']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.category}: {self.text_hindi[:50]}"


class PeppiPersonality(TimeStampedModel):
    """Peppi's personality traits and behavior settings."""

    age_group = models.CharField(
        max_length=20,
        unique=True,
        help_text='Age group (4-5, 6-8, 9-11, 12-14)'
    )
    greeting_style = models.TextField(help_text='How Peppi greets children')
    encouragement_phrases = models.JSONField(
        default=list,
        help_text='List of encouragement phrases'
    )
    teaching_style = models.TextField(help_text='Teaching approach description')
    voice_tone = models.CharField(
        max_length=50,
        help_text='Voice tone and style'
    )
    avatar_expression = models.CharField(
        max_length=50,
        default='happy',
        help_text='Default avatar expression'
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'peppi_personalities'
        verbose_name_plural = 'Peppi Personalities'

    def __str__(self):
        return f"Peppi Personality: {self.age_group}"


class PeppiLearningContext(TimeStampedModel):
    """Tracks Peppi's learning context with each child."""

    child = models.OneToOneField(
        'children.Child',
        on_delete=models.CASCADE,
        related_name='peppi_context'
    )
    current_topic = models.CharField(
        max_length=200,
        blank=True,
        help_text='Current learning topic'
    )
    words_taught_today = models.JSONField(
        default=list,
        help_text='Words taught in current session'
    )
    mistakes_made = models.JSONField(
        default=list,
        help_text='Recent mistakes for adaptive learning'
    )
    mood = models.CharField(
        max_length=50,
        default='neutral',
        help_text='Current mood assessment'
    )
    last_interaction = models.DateTimeField(
        auto_now=True,
        help_text='Last interaction timestamp'
    )
    total_sessions = models.PositiveIntegerField(
        default=0,
        help_text='Total learning sessions'
    )
    streak_days = models.PositiveIntegerField(
        default=0,
        help_text='Current learning streak'
    )

    class Meta:
        db_table = 'peppi_learning_contexts'
        verbose_name_plural = 'Peppi Learning Contexts'

    def __str__(self):
        return f"Peppi Context: {self.child.name}"
