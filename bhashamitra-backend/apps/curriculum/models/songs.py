"""Song models for traditional Hindi songs and rhymes."""
from django.db import models
from apps.core.models import TimeStampedModel


class Song(TimeStampedModel):
    """Traditional Hindi songs and rhymes."""

    class Category(models.TextChoices):
        RHYME = 'RHYME', 'Nursery Rhyme'
        FOLK = 'FOLK', 'Folk Song'
        EDUCATIONAL = 'EDUCATIONAL', 'Educational'
        FESTIVAL = 'FESTIVAL', 'Festival Song'

    title_english = models.CharField(max_length=200, help_text='English title')
    title_hindi = models.CharField(max_length=200, help_text='Hindi title')
    title_romanized = models.CharField(max_length=200, help_text='Romanized title')
    lyrics_hindi = models.TextField(help_text='Hindi lyrics')
    lyrics_romanized = models.TextField(help_text='Romanized lyrics')
    lyrics_english = models.TextField(help_text='English translation')
    age_min = models.PositiveIntegerField(default=4, help_text='Minimum age')
    age_max = models.PositiveIntegerField(default=6, help_text='Maximum age')
    level = models.ForeignKey(
        'CurriculumLevel',
        on_delete=models.CASCADE,
        related_name='songs',
        help_text='Curriculum level'
    )
    duration_seconds = models.PositiveIntegerField(default=60, help_text='Song duration in seconds')
    audio_url = models.URLField(blank=True, help_text='Audio file URL')
    video_url = models.URLField(blank=True, help_text='Video URL')
    category = models.CharField(
        max_length=50,
        choices=Category.choices,
        default=Category.RHYME,
        help_text='Song category'
    )
    actions = models.JSONField(
        default=list,
        help_text='Action instructions for the song'
    )
    order = models.PositiveIntegerField(default=0, help_text='Display order')
    is_active = models.BooleanField(default=True, help_text='Active status')

    class Meta:
        db_table = 'curriculum_songs'
        ordering = ['order']
        indexes = [
            models.Index(fields=['level', 'order']),
            models.Index(fields=['category']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.title_english} ({self.level.code})"
