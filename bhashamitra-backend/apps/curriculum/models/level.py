"""Curriculum hierarchy models - Levels, Modules, Lessons."""
import uuid
from django.db import models
from django.core.validators import MinValueValidator
from apps.core.models import TimeStampedModel


class CurriculumLevel(TimeStampedModel):
    """Learning level L1-L10 representing age-appropriate curriculum stages."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=5, unique=True, help_text='Level code (L1, L2, etc.)')
    name_english = models.CharField(max_length=50, help_text='English name')
    name_hindi = models.CharField(max_length=50, help_text='Hindi name')
    name_romanized = models.CharField(max_length=50, help_text='Romanized Hindi name')
    min_age = models.PositiveSmallIntegerField(help_text='Minimum age for this level')
    max_age = models.PositiveSmallIntegerField(help_text='Maximum age for this level')
    description = models.TextField(help_text='Level description and goals')
    learning_objectives = models.JSONField(default=list, help_text='List of learning objectives')
    peppi_welcome = models.TextField(blank=True, help_text='Peppi welcome message for level')
    peppi_completion = models.TextField(blank=True, help_text='Peppi completion message')
    emoji = models.CharField(max_length=10, help_text='Emoji representing the level')
    theme_color = models.CharField(max_length=7, default='#6366f1', help_text='Hex color code')
    order = models.PositiveSmallIntegerField(unique=True, help_text='Display order')
    estimated_hours = models.PositiveSmallIntegerField(default=20, help_text='Estimated hours to complete')
    min_xp_required = models.PositiveIntegerField(default=0, help_text='Minimum XP required to unlock this level')
    xp_reward = models.PositiveIntegerField(default=100, help_text='XP reward for completing this level')
    is_free = models.BooleanField(default=False, help_text='Available in free tier')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'curriculum_levels'
        ordering = ['order']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['order']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.code}: {self.name_english}"


class CurriculumModule(TimeStampedModel):
    """Module within a level representing a focused learning unit."""

    class ModuleType(models.TextChoices):
        LISTENING = 'LISTENING', 'Listening & Recognition'
        SPEAKING = 'SPEAKING', 'Speaking & Pronunciation'
        VOCABULARY = 'VOCABULARY', 'Vocabulary Building'
        ALPHABET = 'ALPHABET', 'Alphabet & Letters'
        READING = 'READING', 'Reading Practice'
        GRAMMAR = 'GRAMMAR', 'Grammar Concepts'
        STORIES = 'STORIES', 'Story Time'
        SONGS = 'SONGS', 'Songs & Rhymes'
        GAMES = 'GAMES', 'Games & Activities'
        CULTURE = 'CULTURE', 'Cultural Learning'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    level = models.ForeignKey(
        CurriculumLevel,
        on_delete=models.CASCADE,
        related_name='modules',
        help_text='Parent curriculum level'
    )
    code = models.CharField(max_length=20, help_text='Module code (L1.M1, L2.M3, etc.)')
    name_english = models.CharField(max_length=100, help_text='English name')
    name_hindi = models.CharField(max_length=100, help_text='Hindi name')
    name_romanized = models.CharField(max_length=100, help_text='Romanized Hindi name')
    module_type = models.CharField(
        max_length=20,
        choices=ModuleType.choices,
        help_text='Type of learning module'
    )
    description = models.TextField(help_text='Module description and learning goals')
    objectives = models.JSONField(default=list, blank=True, help_text='List of learning objectives for this module')
    peppi_intro = models.TextField(blank=True, help_text='Peppi introduction for module')
    peppi_completion = models.TextField(blank=True, help_text='Peppi completion message')
    emoji = models.CharField(max_length=10, help_text='Emoji representing the module')
    order = models.PositiveSmallIntegerField(help_text='Order within level')
    estimated_minutes = models.PositiveSmallIntegerField(default=30, help_text='Estimated minutes to complete')
    xp_reward = models.PositiveIntegerField(default=30, help_text='XP reward for completing this module')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'curriculum_modules'
        ordering = ['level', 'order']
        unique_together = ['level', 'code']
        indexes = [
            models.Index(fields=['level', 'order']),
            models.Index(fields=['module_type']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.code}: {self.name_english}"


class Lesson(TimeStampedModel):
    """Individual lesson within a module containing specific learning activities."""

    class LessonType(models.TextChoices):
        INTRODUCTION = 'INTRODUCTION', 'Introduction'
        LEARNING = 'LEARNING', 'Learning'
        PRACTICE = 'PRACTICE', 'Practice'
        REVIEW = 'REVIEW', 'Review'
        STORY = 'STORY', 'Story Time'
        ASSESSMENT = 'ASSESSMENT', 'Assessment'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    module = models.ForeignKey(
        CurriculumModule,
        on_delete=models.CASCADE,
        related_name='lessons',
        help_text='Parent module'
    )
    code = models.CharField(max_length=30, help_text='Lesson code (L1.M1.LS1, etc.)')
    title_english = models.CharField(max_length=200, help_text='English title')
    title_hindi = models.CharField(max_length=200, help_text='Hindi title')
    title_romanized = models.CharField(max_length=200, help_text='Romanized Hindi title')
    lesson_type = models.CharField(
        max_length=20,
        choices=LessonType.choices,
        default=LessonType.LEARNING,
        help_text='Type of lesson'
    )
    description = models.TextField(blank=True, help_text='Lesson description')
    peppi_intro = models.TextField(blank=True, help_text='Peppi introduction for lesson')
    peppi_success = models.TextField(blank=True, help_text='Peppi success message')
    content = models.JSONField(
        default=dict,
        blank=True,
        help_text='Lesson content including sections, exercises, and summary'
    )
    order = models.PositiveSmallIntegerField(help_text='Order within module')
    estimated_minutes = models.PositiveSmallIntegerField(default=10, help_text='Estimated minutes')
    points_available = models.PositiveIntegerField(default=10, help_text='Points available for completion')
    mastery_threshold = models.PositiveSmallIntegerField(
        default=80,
        validators=[MinValueValidator(0)],
        help_text='Percentage required for mastery'
    )
    is_free = models.BooleanField(default=False, help_text='Available in free tier')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'curriculum_lessons'
        ordering = ['module', 'order']
        unique_together = ['module', 'code']
        indexes = [
            models.Index(fields=['module', 'order']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.code}: {self.title_english}"


class LessonContent(TimeStampedModel):
    """Links lessons to specific content items (vocabulary, games, assessments, etc.)."""

    class ContentType(models.TextChoices):
        VOCABULARY_THEME = 'VOCABULARY_THEME', 'Vocabulary Theme'
        VOCABULARY_WORD = 'VOCABULARY_WORD', 'Vocabulary Word'
        LETTER = 'LETTER', 'Alphabet Letter'
        GRAMMAR_TOPIC = 'GRAMMAR_TOPIC', 'Grammar Topic'
        GAME = 'GAME', 'Game'
        STORY = 'STORY', 'Story'
        ASSESSMENT = 'ASSESSMENT', 'Assessment'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='contents',
        help_text='Parent lesson'
    )
    content_type = models.CharField(
        max_length=30,
        choices=ContentType.choices,
        help_text='Type of content'
    )
    content_id = models.UUIDField(help_text='UUID of the referenced content')
    sequence_order = models.PositiveSmallIntegerField(
        default=0,
        help_text='Order in which content appears'
    )
    is_required = models.BooleanField(
        default=True,
        help_text='Whether this content is required for lesson completion'
    )

    class Meta:
        db_table = 'lesson_contents'
        ordering = ['lesson', 'sequence_order']
        unique_together = ['lesson', 'content_type', 'content_id']
        indexes = [
            models.Index(fields=['lesson', 'sequence_order']),
            models.Index(fields=['content_type', 'content_id']),
        ]

    def __str__(self):
        return f"{self.lesson.code} - {self.content_type}"
