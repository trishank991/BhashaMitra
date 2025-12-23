"""Analytics and event tracking models."""
from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel


class LessonAnalytics(TimeStampedModel):
    """Aggregated analytics per lesson/content."""

    content_type = models.CharField(max_length=50)
    content_id = models.UUIDField()
    language = models.CharField(max_length=20)
    total_views = models.IntegerField(default=0)
    unique_users = models.IntegerField(default=0)
    completion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    average_time_seconds = models.IntegerField(default=0)
    drop_off_points = models.JSONField(default=dict, help_text='Page/section where users drop off')
    difficulty_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    engagement_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        db_table = 'lesson_analytics'
        unique_together = ['content_type', 'content_id']
        indexes = [
            models.Index(fields=['content_type', 'language']),
        ]

    def __str__(self):
        return f"{self.content_type}:{self.content_id}"


class CohortAnalytics(TimeStampedModel):
    """Analytics aggregated by cohort (age, language, level)."""

    cohort_type = models.CharField(max_length=50, help_text='age_group, language, level, etc.')
    cohort_value = models.CharField(max_length=50)
    period_start = models.DateField()
    period_end = models.DateField()
    active_users = models.IntegerField(default=0)
    new_users = models.IntegerField(default=0)
    churned_users = models.IntegerField(default=0)
    average_session_duration = models.IntegerField(default=0)
    average_sessions_per_user = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    retention_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    conversion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        db_table = 'cohort_analytics'
        indexes = [
            models.Index(fields=['cohort_type', 'period_start']),
        ]

    def __str__(self):
        return f"{self.cohort_type}:{self.cohort_value} ({self.period_start})"


class PeppiAnalytics(TimeStampedModel):
    """Analytics for Peppi AI companion interactions."""

    child = models.ForeignKey(
        'children.Child',
        on_delete=models.CASCADE,
        related_name='peppi_analytics'
    )
    date = models.DateField()
    total_interactions = models.IntegerField(default=0)
    voice_interactions = models.IntegerField(default=0)
    text_interactions = models.IntegerField(default=0)
    help_requests = models.IntegerField(default=0)
    encouragements_given = models.IntegerField(default=0)
    corrections_given = models.IntegerField(default=0)
    topics_discussed = models.JSONField(default=list)
    sentiment_scores = models.JSONField(default=dict)
    average_response_time_ms = models.IntegerField(default=0)

    class Meta:
        db_table = 'peppi_analytics'
        unique_together = ['child', 'date']
        indexes = [
            models.Index(fields=['child', 'date']),
        ]

    def __str__(self):
        return f"{self.child.name} - {self.date}"


class EventLog(TimeStampedModel):
    """Raw event logging for detailed analytics."""

    class EventCategory(models.TextChoices):
        NAVIGATION = 'NAVIGATION', 'Navigation'
        CONTENT = 'CONTENT', 'Content Interaction'
        GAMIFICATION = 'GAMIFICATION', 'Gamification'
        SOCIAL = 'SOCIAL', 'Social'
        SYSTEM = 'SYSTEM', 'System'
        ERROR = 'ERROR', 'Error'

    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='event_logs'
    )
    child = models.ForeignKey(
        'children.Child',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='event_logs'
    )
    session_id = models.CharField(max_length=100, blank=True)
    event_category = models.CharField(max_length=30, choices=EventCategory.choices)
    event_name = models.CharField(max_length=100)
    event_data = models.JSONField(default=dict)
    page_url = models.CharField(max_length=500, blank=True)
    device_type = models.CharField(max_length=50, blank=True)
    app_version = models.CharField(max_length=20, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'event_logs'
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['event_category', 'event_name']),
            models.Index(fields=['session_id']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"{self.event_name} - {self.timestamp}"
