"""Teaching personalities and instructors for BhashaMitra."""
import uuid
from django.db import models
from apps.core.models import TimeStampedModel


class Teacher(TimeStampedModel):
    """Teaching personalities and instructors (Peppi for L1-L5, Gyan for L6-L10)."""

    class CharacterType(models.TextChoices):
        CAT = 'CAT', 'Ragdoll Cat (Peppi)'
        OWL = 'OWL', 'Wise Owl (Gyan)'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, help_text='Teacher name in English')
    name_hindi = models.CharField(max_length=100, help_text='Teacher name in Hindi')
    character_type = models.CharField(
        max_length=20,
        choices=CharacterType.choices,
        help_text='Type of character (Cat/Owl)'
    )
    breed = models.CharField(max_length=100, blank=True, help_text='Animal breed')
    personality = models.TextField(help_text='Personality traits and teaching style')
    voice_style = models.CharField(max_length=100, help_text='Voice characteristics')
    avatar_url = models.URLField(blank=True, help_text='URL to avatar image')
    intro_message = models.TextField(blank=True, help_text='Default introduction message')
    encouragement_phrases = models.JSONField(
        default=list,
        help_text='List of encouragement phrases'
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'curriculum_teachers'
        ordering = ['character_type', 'name']
        indexes = [
            models.Index(fields=['character_type']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.name} ({self.character_type})"
