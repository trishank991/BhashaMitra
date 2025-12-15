"""Story models."""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import TimeStampedModel
from apps.children.models import Child


class Story(TimeStampedModel):
    """Story content cached from StoryWeaver."""

    storyweaver_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=500)
    title_translit = models.CharField(max_length=500, blank=True, null=True)
    language = models.CharField(max_length=20, choices=Child.Language.choices)
    level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    page_count = models.IntegerField()
    cover_image_url = models.URLField()
    synopsis = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    illustrator = models.CharField(max_length=255, blank=True, null=True)
    categories = models.JSONField(default=list)
    cached_at = models.DateTimeField(auto_now_add=True)
    last_accessed_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'stories'
        indexes = [
            models.Index(fields=['language', 'level']),
            models.Index(fields=['storyweaver_id']),
        ]
        verbose_name_plural = 'stories'

    def __str__(self):
        return f"{self.title} (Level {self.level})"


class StoryPage(TimeStampedModel):
    """Individual pages of a story."""

    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='pages')
    page_number = models.IntegerField()
    text_content = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    audio_url = models.URLField(blank=True, null=True)  # Cached TTS

    class Meta:
        db_table = 'story_pages'
        unique_together = ['story', 'page_number']
        ordering = ['page_number']

    def __str__(self):
        return f"{self.story.title} - Page {self.page_number}"
