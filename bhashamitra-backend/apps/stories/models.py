"""Story models."""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import TimeStampedModel
from apps.children.models import Child


class Story(TimeStampedModel):
    """Story content cached from StoryWeaver."""

    class Tier(models.TextChoices):
        FREE = 'free', 'Free'
        STANDARD = 'standard', 'Standard'
        PREMIUM = 'premium', 'Premium'

    storyweaver_id = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, blank=True, db_index=True)
    title = models.CharField(max_length=500)
    title_translit = models.CharField(max_length=500, blank=True, null=True)
    language = models.CharField(max_length=20, choices=Child.Language.choices)
    level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    page_count = models.IntegerField()
    cover_image_url = models.URLField(blank=True)
    synopsis = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    illustrator = models.CharField(max_length=255, blank=True, null=True)
    categories = models.JSONField(default=list)
    cached_at = models.DateTimeField(auto_now_add=True)
    last_accessed_at = models.DateTimeField(auto_now=True)
    # L1 Curriculum fields
    title_hindi = models.CharField(max_length=500, blank=True, help_text='Hindi title')
    title_romanized = models.CharField(max_length=500, blank=True, help_text='Romanized title')
    age_min = models.PositiveIntegerField(default=4, help_text='Minimum age')
    age_max = models.PositiveIntegerField(default=14, help_text='Maximum age')
    is_l1_content = models.BooleanField(default=False, help_text='Part of L1 curriculum')
    theme = models.CharField(max_length=100, blank=True, help_text='Story theme')
    # Tier and gamification fields
    tier = models.CharField(max_length=20, choices=Tier.choices, default=Tier.FREE, help_text='Subscription tier')
    moral_hindi = models.TextField(blank=True, help_text='Moral of story in Hindi')
    moral_english = models.TextField(blank=True, help_text='Moral of story in English')
    xp_reward = models.PositiveIntegerField(default=10, help_text='XP reward for completing story')
    estimated_minutes = models.PositiveIntegerField(default=3, help_text='Estimated reading time')
    is_featured = models.BooleanField(default=False, help_text='Featured on homepage')
    sort_order = models.PositiveIntegerField(default=0, help_text='Display order')
    is_active = models.BooleanField(default=True, help_text='Story is active')

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
    text_hindi = models.TextField(blank=True, help_text='Hindi text')
    text_romanized = models.TextField(blank=True, help_text='Romanized text')
    # Interactive elements for vocabulary learning
    highlight_words = models.JSONField(default=list, blank=True, help_text='Words to highlight for learning')
    image_description = models.TextField(blank=True, help_text='Description for AI image generation')

    class Meta:
        db_table = 'story_pages'
        unique_together = ['story', 'page_number']
        ordering = ['page_number']

    def __str__(self):
        return f"{self.story.title} - Page {self.page_number}"


class StoryVocabulary(TimeStampedModel):
    """Vocabulary words from stories for learning."""

    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='vocabulary')
    word_hindi = models.CharField(max_length=100)
    word_transliteration = models.CharField(max_length=100)
    word_english = models.CharField(max_length=100)
    example_hindi = models.TextField(blank=True)
    example_english = models.TextField(blank=True)
    audio_url = models.CharField(max_length=500, blank=True)
    image_url = models.CharField(max_length=500, blank=True)

    class Meta:
        db_table = 'story_vocabulary'
        ordering = ['story', 'word_hindi']

    def __str__(self):
        return f"{self.word_hindi} - {self.word_english}"
