"""Festival models."""
from django.db import models
import uuid


class Religion(models.TextChoices):
    HINDU = 'HINDU', 'Hindu'
    MUSLIM = 'MUSLIM', 'Muslim'
    SIKH = 'SIKH', 'Sikh'
    CHRISTIAN = 'CHRISTIAN', 'Christian'
    JAIN = 'JAIN', 'Jain'
    BUDDHIST = 'BUDDHIST', 'Buddhist'


class Festival(models.Model):
    """Festival model storing information about cultural/religious festivals."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    name_native = models.CharField(max_length=100, help_text='Name in native script')
    religion = models.CharField(max_length=20, choices=Religion.choices)
    description = models.TextField()
    typical_month = models.IntegerField(help_text='1-12 for typical celebration month')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'festivals'
        ordering = ['typical_month', 'name']
        indexes = [
            models.Index(fields=['religion']),
            models.Index(fields=['typical_month']),
        ]

    def __str__(self):
        return f"{self.name} ({self.religion})"


class FestivalStory(models.Model):
    """Junction table linking festivals to stories."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    festival = models.ForeignKey(
        Festival,
        on_delete=models.CASCADE,
        related_name='festival_stories'
    )
    story = models.ForeignKey(
        'stories.Story',
        on_delete=models.CASCADE,
        related_name='festival_links'
    )
    is_primary = models.BooleanField(
        default=False,
        help_text='Primary story for this festival'
    )

    class Meta:
        db_table = 'festival_stories'
        unique_together = ['festival', 'story']
        indexes = [
            models.Index(fields=['festival', 'is_primary']),
        ]

    def __str__(self):
        return f"{self.festival.name} - {self.story.title}"
