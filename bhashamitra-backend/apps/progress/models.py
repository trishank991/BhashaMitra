"""Progress models."""
from django.db import models
from apps.core.models import TimeStampedModel
from apps.children.models import Child
from apps.stories.models import Story


class Progress(TimeStampedModel):
    """Reading progress for a child on a story."""

    class Status(models.TextChoices):
        NOT_STARTED = 'NOT_STARTED', 'Not Started'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'

    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='progress_records')
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='progress_records')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NOT_STARTED)
    current_page = models.IntegerField(default=0)
    pages_completed = models.IntegerField(default=0)
    time_spent_seconds = models.IntegerField(default=0)
    points_earned = models.IntegerField(default=0)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'progress'
        unique_together = ['child', 'story']

    def __str__(self):
        return f"{self.child.name} - {self.story.title} ({self.status})"


class DailyActivity(TimeStampedModel):
    """Aggregated daily activity for analytics."""

    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='daily_activities')
    date = models.DateField()
    stories_started = models.IntegerField(default=0)
    stories_completed = models.IntegerField(default=0)
    pages_read = models.IntegerField(default=0)
    time_spent_seconds = models.IntegerField(default=0)
    points_earned = models.IntegerField(default=0)
    recordings_made = models.IntegerField(default=0)

    class Meta:
        db_table = 'daily_activities'
        unique_together = ['child', 'date']
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['child', 'date']),
        ]

    def __str__(self):
        return f"{self.child.name} - {self.date}"


class DailyProgress(TimeStampedModel):
    """Daily learning progress tracking for parent dashboard."""

    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='daily_progress')
    date = models.DateField()
    time_spent_minutes = models.IntegerField(default=0)
    lessons_completed = models.IntegerField(default=0)
    exercises_completed = models.IntegerField(default=0)
    games_played = models.IntegerField(default=0)
    points_earned = models.IntegerField(default=0)

    class Meta:
        db_table = 'daily_progress'
        unique_together = ['child', 'date']
        ordering = ['-date']
        indexes = [
            models.Index(fields=['date']),
        ]

    def __str__(self):
        return f"{self.child.name} - {self.date}"


class ActivityLog(TimeStampedModel):
    """Activity log entries for tracking child learning activities."""

    class ActivityType(models.TextChoices):
        LESSON_STARTED = 'LESSON_STARTED', 'Lesson Started'
        LESSON_COMPLETED = 'LESSON_COMPLETED', 'Lesson Completed'
        EXERCISE_COMPLETED = 'EXERCISE_COMPLETED', 'Exercise Completed'
        GAME_COMPLETED = 'GAME_COMPLETED', 'Game Completed'
        BADGE_EARNED = 'BADGE_EARNED', 'Badge Earned'
        LEVEL_UP = 'LEVEL_UP', 'Level Up'
        STREAK_MILESTONE = 'STREAK_MILESTONE', 'Streak Milestone'
        FIRST_LOGIN = 'FIRST_LOGIN', 'First Login'

    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='activity_logs')
    activity_type = models.CharField(max_length=30, choices=ActivityType.choices)
    description = models.TextField(blank=True, default='')
    points_earned = models.IntegerField(default=0)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'activity_logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['child', '-created_at']),
            models.Index(fields=['activity_type']),
        ]

    def __str__(self):
        return f"{self.child.name} - {self.activity_type}"


