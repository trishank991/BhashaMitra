"""Multi-child family and sibling challenge models."""
from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel


class Family(TimeStampedModel):
    """Family grouping for multi-child discounts and features."""

    name = models.CharField(max_length=100, blank=True)
    primary_parent = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='families_owned'
    )
    members = models.ManyToManyField(
        'users.User',
        related_name='families',
        blank=True
    )
    family_code = models.CharField(max_length=20, unique=True, blank=True)
    discount_tier = models.IntegerField(
        default=0,
        help_text='Discount percentage based on family size'
    )
    total_children = models.IntegerField(default=0)
    collective_points = models.IntegerField(default=0)
    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='families_created'
    )

    class Meta:
        db_table = 'families'
        verbose_name_plural = 'Families'

    def __str__(self):
        return self.name or f"Family of {self.primary_parent.email}"

    def save(self, *args, **kwargs):
        if not self.family_code:
            import secrets
            self.family_code = secrets.token_urlsafe(8)[:10].upper()
        super().save(*args, **kwargs)

    def calculate_discount(self):
        """Calculate family discount based on number of children."""
        if self.total_children >= 4:
            return 25
        elif self.total_children >= 3:
            return 15
        elif self.total_children >= 2:
            return 10
        return 0


class FamilyLeaderboard(TimeStampedModel):
    """Weekly family leaderboard."""

    family = models.ForeignKey(
        Family,
        on_delete=models.CASCADE,
        related_name='leaderboard_entries'
    )
    week_start = models.DateField()
    total_points = models.IntegerField(default=0)
    total_time_minutes = models.IntegerField(default=0)
    stories_completed = models.IntegerField(default=0)
    child_rankings = models.JSONField(
        default=list,
        help_text='Ordered list of children by points'
    )
    rank = models.IntegerField(default=0, help_text='Global rank among families')

    class Meta:
        db_table = 'family_leaderboards'
        unique_together = ['family', 'week_start']
        indexes = [
            models.Index(fields=['week_start', 'total_points']),
        ]

    def __str__(self):
        return f"{self.family} - Week of {self.week_start}"


class SiblingChallenge(TimeStampedModel):
    """Friendly challenges between siblings."""

    class ChallengeType(models.TextChoices):
        POINTS = 'POINTS', 'Most Points'
        STORIES = 'STORIES', 'Most Stories Read'
        TIME = 'TIME', 'Most Learning Time'
        STREAK = 'STREAK', 'Longest Streak'
        WORDS = 'WORDS', 'Most Words Learned'

    class ChallengeStatus(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    family = models.ForeignKey(
        Family,
        on_delete=models.CASCADE,
        related_name='sibling_challenges'
    )
    title = models.CharField(max_length=200)
    challenge_type = models.CharField(max_length=20, choices=ChallengeType.choices)
    status = models.CharField(
        max_length=20,
        choices=ChallengeStatus.choices,
        default=ChallengeStatus.ACTIVE
    )
    participants = models.ManyToManyField(
        'children.Child',
        related_name='sibling_challenges'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    target_value = models.IntegerField(default=0, help_text='Target to reach or compare against')
    participant_progress = models.JSONField(
        default=dict,
        help_text='Progress per participant {child_id: value}'
    )
    winner = models.ForeignKey(
        'children.Child',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='challenges_won'
    )
    prize_description = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = 'sibling_challenges'
        indexes = [
            models.Index(fields=['family', 'status']),
            models.Index(fields=['start_date', 'end_date']),
        ]

    def __str__(self):
        return f"{self.title} ({self.family})"
