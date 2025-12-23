"""Festival models."""
from django.db import models
from django.utils import timezone
import uuid


class Religion(models.TextChoices):
    HINDU = 'HINDU', 'Hindu'
    MUSLIM = 'MUSLIM', 'Muslim'
    SIKH = 'SIKH', 'Sikh'
    CHRISTIAN = 'CHRISTIAN', 'Christian'
    JAIN = 'JAIN', 'Jain'
    BUDDHIST = 'BUDDHIST', 'Buddhist'


class ActivityType(models.TextChoices):
    """Types of festival activities."""
    STORY = 'STORY', 'Story'
    CRAFT = 'CRAFT', 'Craft'
    COOKING = 'COOKING', 'Cooking'
    SONG = 'SONG', 'Song'
    GAME = 'GAME', 'Game'
    VOCABULARY = 'VOCABULARY', 'Vocabulary'
    QUIZ = 'QUIZ', 'Quiz'
    VIDEO = 'VIDEO', 'Video'


class Festival(models.Model):
    """Festival model storing information about cultural/religious festivals."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    name_native = models.CharField(max_length=100, help_text='Name in native script')

    # Multi-language support
    name_hindi = models.CharField(max_length=100, blank=True, help_text='Name in Hindi')
    name_tamil = models.CharField(max_length=100, blank=True, help_text='Name in Tamil')
    name_gujarati = models.CharField(max_length=100, blank=True, help_text='Name in Gujarati')
    name_punjabi = models.CharField(max_length=100, blank=True, help_text='Name in Punjabi')
    name_telugu = models.CharField(max_length=100, blank=True, help_text='Name in Telugu')
    name_malayalam = models.CharField(max_length=100, blank=True, help_text='Name in Malayalam')

    religion = models.CharField(max_length=20, choices=Religion.choices)
    description = models.TextField()
    significance = models.TextField(blank=True, help_text='Cultural/religious significance')
    typical_month = models.IntegerField(help_text='1-12 for typical celebration month')
    is_lunar_calendar = models.BooleanField(
        default=False,
        help_text='True if festival follows lunar calendar (dates vary)'
    )
    image_url = models.URLField(blank=True, null=True, help_text='Festival banner/image URL')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'festivals'
        ordering = ['typical_month', 'name']
        indexes = [
            models.Index(fields=['religion']),
            models.Index(fields=['typical_month']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.name} ({self.religion})"

    def get_name_for_language(self, language):
        """Get festival name in the specified language."""
        language_map = {
            'HINDI': self.name_hindi,
            'TAMIL': self.name_tamil,
            'GUJARATI': self.name_gujarati,
            'PUNJABI': self.name_punjabi,
            'TELUGU': self.name_telugu,
            'MALAYALAM': self.name_malayalam,
        }
        return language_map.get(language.upper()) or self.name


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


class FestivalActivity(models.Model):
    """Activities associated with festivals (crafts, songs, games, etc)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    festival = models.ForeignKey(
        Festival,
        on_delete=models.CASCADE,
        related_name='activities'
    )
    title = models.CharField(max_length=200)
    activity_type = models.CharField(
        max_length=20,
        choices=ActivityType.choices,
        help_text='Type of activity'
    )
    description = models.TextField(help_text='Brief description of the activity')
    instructions = models.TextField(help_text='Step-by-step instructions')
    materials_needed = models.JSONField(
        default=list,
        blank=True,
        help_text='List of materials needed for this activity'
    )
    min_age = models.IntegerField(
        default=3,
        help_text='Minimum recommended age'
    )
    max_age = models.IntegerField(
        default=8,
        help_text='Maximum recommended age'
    )
    duration_minutes = models.IntegerField(
        default=15,
        help_text='Estimated duration in minutes'
    )
    difficulty_level = models.IntegerField(
        default=1,
        help_text='Difficulty level (1-5)'
    )
    points_reward = models.IntegerField(
        default=25,
        help_text='Points awarded on completion'
    )
    image_url = models.URLField(blank=True, null=True, help_text='Activity image URL')
    video_url = models.URLField(blank=True, null=True, help_text='Tutorial video URL')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'festival_activities'
        verbose_name_plural = 'festival activities'
        ordering = ['festival', 'activity_type', 'title']
        indexes = [
            models.Index(fields=['festival', 'activity_type']),
            models.Index(fields=['min_age', 'max_age']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.festival.name} - {self.title} ({self.activity_type})"

    def is_age_appropriate(self, child_age):
        """Check if activity is appropriate for child's age."""
        return self.min_age <= child_age <= self.max_age


class FestivalProgress(models.Model):
    """Track child's progress through festival activities and stories."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    child = models.ForeignKey(
        'children.Child',
        on_delete=models.CASCADE,
        related_name='festival_progress'
    )
    festival = models.ForeignKey(
        Festival,
        on_delete=models.CASCADE,
        related_name='child_progress'
    )
    activity = models.ForeignKey(
        FestivalActivity,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='completions',
        help_text='Completed activity (if applicable)'
    )
    story = models.ForeignKey(
        'stories.Story',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='festival_completions',
        help_text='Completed story (if applicable)'
    )
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    points_earned = models.IntegerField(default=0)
    notes = models.TextField(blank=True, help_text='Optional notes or feedback')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'festival_progress'
        verbose_name_plural = 'festival progress'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['child', 'festival']),
            models.Index(fields=['child', 'is_completed']),
            models.Index(fields=['festival', 'is_completed']),
        ]

    def __str__(self):
        if self.activity:
            return f"{self.child.name} - {self.activity.title}"
        elif self.story:
            return f"{self.child.name} - {self.story.title}"
        return f"{self.child.name} - {self.festival.name}"

    def mark_complete(self):
        """Mark progress as complete and award points."""
        if not self.is_completed:
            self.is_completed = True
            self.completed_at = timezone.now()

            # Award points
            if self.activity:
                self.points_earned = self.activity.points_reward
            else:
                self.points_earned = 10  # Default points for story completion

            self.save()

            # Update child's total points if the field exists
            if hasattr(self.child, 'total_points'):
                self.child.total_points += self.points_earned
                self.child.save(update_fields=['total_points'])

            return self.points_earned
        return 0
