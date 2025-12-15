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
