"""Parent engagement models."""
from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel


class ParentPreferences(TimeStampedModel):
    """Parent notification and engagement preferences."""

    class NotificationFrequency(models.TextChoices):
        DAILY = 'DAILY', 'Daily'
        WEEKLY = 'WEEKLY', 'Weekly'
        MONTHLY = 'MONTHLY', 'Monthly'
        NONE = 'NONE', 'None'

    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        related_name='parent_preferences'
    )
    notification_frequency = models.CharField(
        max_length=20,
        choices=NotificationFrequency.choices,
        default=NotificationFrequency.WEEKLY
    )
    email_reports = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    sms_alerts = models.BooleanField(default=False)
    preferred_report_day = models.IntegerField(
        default=0,
        help_text='Day of week for reports (0=Monday, 6=Sunday)'
    )
    timezone = models.CharField(max_length=50, default='Pacific/Auckland')

    class Meta:
        db_table = 'parent_preferences'
        verbose_name_plural = 'Parent preferences'

    def __str__(self):
        return f"Preferences for {self.user.email}"


class LearningGoal(TimeStampedModel):
    """Parent-set learning goals for children."""

    class GoalType(models.TextChoices):
        DAILY_MINUTES = 'DAILY_MINUTES', 'Daily Screen Time'
        WEEKLY_STORIES = 'WEEKLY_STORIES', 'Stories per Week'
        MONTHLY_POINTS = 'MONTHLY_POINTS', 'Points per Month'
        LEVEL_TARGET = 'LEVEL_TARGET', 'Level Target'

    child = models.ForeignKey(
        'children.Child',
        on_delete=models.CASCADE,
        related_name='learning_goals'
    )
    goal_type = models.CharField(max_length=30, choices=GoalType.choices)
    target_value = models.IntegerField()
    current_value = models.IntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'learning_goals'
        indexes = [
            models.Index(fields=['child', 'is_active']),
            models.Index(fields=['goal_type']),
        ]

    def __str__(self):
        return f"{self.child.name} - {self.goal_type}"

    @property
    def progress_percentage(self):
        if self.target_value == 0:
            return 0
        return min(100, (self.current_value / self.target_value) * 100)


class WeeklyReport(TimeStampedModel):
    """Generated weekly reports for parents."""

    child = models.ForeignKey(
        'children.Child',
        on_delete=models.CASCADE,
        related_name='weekly_reports'
    )
    week_start = models.DateField()
    week_end = models.DateField()
    total_time_minutes = models.IntegerField(default=0)
    stories_completed = models.IntegerField(default=0)
    points_earned = models.IntegerField(default=0)
    new_words_learned = models.IntegerField(default=0)
    achievements_unlocked = models.JSONField(default=list)
    areas_of_strength = models.JSONField(default=list)
    areas_for_improvement = models.JSONField(default=list)
    peppi_interactions = models.IntegerField(default=0)
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'weekly_reports'
        unique_together = ['child', 'week_start']
        indexes = [
            models.Index(fields=['child', 'week_start']),
        ]

    def __str__(self):
        return f"{self.child.name} - Week of {self.week_start}"


class ParentChildActivity(TimeStampedModel):
    """Suggested parent-child activities."""

    class ActivityType(models.TextChoices):
        READ_TOGETHER = 'READ_TOGETHER', 'Read Together'
        PRACTICE_LETTERS = 'PRACTICE_LETTERS', 'Practice Letters'
        CULTURAL_CRAFT = 'CULTURAL_CRAFT', 'Cultural Craft'
        COOKING_ACTIVITY = 'COOKING_ACTIVITY', 'Cooking Activity'
        FESTIVAL_ACTIVITY = 'FESTIVAL_ACTIVITY', 'Festival Activity'

    title = models.CharField(max_length=200)
    activity_type = models.CharField(max_length=30, choices=ActivityType.choices)
    description = models.TextField()
    language = models.CharField(max_length=20)
    min_age = models.IntegerField(default=2)
    max_age = models.IntegerField(default=18)
    duration_minutes = models.IntegerField(default=15)
    materials_needed = models.JSONField(default=list)
    learning_outcomes = models.JSONField(default=list)
    is_featured = models.BooleanField(default=False)

    class Meta:
        db_table = 'parent_child_activities'
        verbose_name_plural = 'Parent-child activities'
        indexes = [
            models.Index(fields=['language', 'activity_type']),
            models.Index(fields=['min_age', 'max_age']),
        ]

    def __str__(self):
        return self.title
