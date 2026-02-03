"""Themed learning environments for each curriculum level."""
import uuid
from django.db import models
from apps.core.models import TimeStampedModel


class Classroom(TimeStampedModel):
    """Themed learning environment for each level (Garden, Treehouse, etc.)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    level = models.OneToOneField(
        'CurriculumLevel',
        on_delete=models.CASCADE,
        related_name='classroom',
        help_text='Associated curriculum level'
    )
    name = models.CharField(max_length=100, help_text='Classroom name in English')
    name_hindi = models.CharField(max_length=100, help_text='Classroom name in Hindi')
    theme = models.CharField(max_length=100, help_text='Theme identifier')
    description = models.TextField(blank=True, help_text='Description of the classroom')
    elements = models.JSONField(
        default=list,
        help_text='Visual elements in the classroom'
    )
    background_color = models.CharField(max_length=7, help_text='Hex color code')
    background_image_url = models.URLField(blank=True, help_text='Background image URL')
    unlock_animation = models.CharField(max_length=50, blank=True, help_text='Animation type')
    ambient_sounds = models.JSONField(default=list, help_text='Ambient sound URLs')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'classrooms'
        ordering = ['level__order']
        indexes = [
            models.Index(fields=['level']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.name} ({self.level.code})"
