"""Gamification models."""
from django.db import models
from apps.core.models import TimeStampedModel
from apps.children.models import Child


class Badge(TimeStampedModel):
    """Achievement badges."""

    class CriteriaType(models.TextChoices):
        STORIES_COMPLETED = 'STORIES_COMPLETED', 'Stories Completed'
        STREAK_DAYS = 'STREAK_DAYS', 'Streak Days'
        POINTS_EARNED = 'POINTS_EARNED', 'Points Earned'
        TIME_SPENT_MINUTES = 'TIME_SPENT_MINUTES', 'Time Spent'
        VOICE_RECORDINGS = 'VOICE_RECORDINGS', 'Voice Recordings'
        LETTERS_MASTERED = 'LETTERS_MASTERED', 'Letters Mastered'
        WORDS_MASTERED = 'WORDS_MASTERED', 'Words Mastered'

    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50)
    criteria_type = models.CharField(max_length=30, choices=CriteriaType.choices)
    criteria_value = models.IntegerField()
    display_order = models.IntegerField(default=0)
    points_bonus = models.IntegerField(default=0)

    class Meta:
        db_table = 'badges'
        ordering = ['display_order']

    def __str__(self):
        return self.name


class ChildBadge(TimeStampedModel):
    """Junction table for badges earned by children."""

    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='earned_badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='child_badges')
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'child_badges'
        unique_together = ['child', 'badge']

    def __str__(self):
        return f"{self.child.name} - {self.badge.name}"


class Streak(TimeStampedModel):
    """Streak tracking for daily activity."""

    child = models.OneToOneField(Child, on_delete=models.CASCADE, related_name='streak')
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'streaks'

    def __str__(self):
        return f"{self.child.name} - {self.current_streak} days"


class VoiceRecording(TimeStampedModel):
    """Voice recordings made by children."""

    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='voice_recordings')
    story = models.ForeignKey('stories.Story', on_delete=models.SET_NULL, null=True, blank=True)
    page_number = models.IntegerField(null=True, blank=True)
    audio_url = models.URLField()
    duration_ms = models.IntegerField()
    transcription = models.TextField(blank=True, null=True)
    confidence_score = models.FloatField(null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'voice_recordings'
        indexes = [models.Index(fields=['child', 'recorded_at'])]

    def __str__(self):
        return f"{self.child.name} - Recording {self.id}"
