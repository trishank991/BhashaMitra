"""Child profile models."""
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel, SoftDeleteModel, SoftDeleteManager


class Child(TimeStampedModel, SoftDeleteModel):
    """Child profile linked to a parent user."""

    class Language(models.TextChoices):
        FIJI_HINDI = 'FIJI_HINDI', 'Fiji Hindi'
        GUJARATI = 'GUJARATI', 'Gujarati'
        HINDI = 'HINDI', 'Hindi'
        MALAYALAM = 'MALAYALAM', 'Malayalam'
        PUNJABI = 'PUNJABI', 'Punjabi'
        TAMIL = 'TAMIL', 'Tamil'
        TELUGU = 'TELUGU', 'Telugu'

    class PeppiAddressing(models.TextChoices):
        BY_NAME = 'BY_NAME', 'By Name'
        CULTURAL = 'CULTURAL', _('Cultural (Yaar/Dost)')  # Friend terms

    class PeppiGender(models.TextChoices):
        MALE = 'MALE', 'Male (Peppi Bhaiya)'
        FEMALE = 'FEMALE', 'Female (Peppi Didi)'

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='children'
    )
    name = models.CharField(max_length=100)
    avatar = models.CharField(max_length=50, default='default')
    date_of_birth = models.DateField()
    language = models.CharField(
        max_length=20,
        choices=Language.choices,
        default=Language.HINDI
    )
    level = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    total_points = models.IntegerField(default=0)

    # Peppi preferences
    peppi_addressing = models.CharField(
        max_length=20,
        choices=PeppiAddressing.choices,
        default=PeppiAddressing.BY_NAME,
        help_text='How Peppi addresses the child (friend terms, not elder sibling)'
    )
    peppi_gender = models.CharField(
        max_length=10,
        choices=PeppiGender.choices,
        default=PeppiGender.FEMALE,
        help_text='Peppi voice gender preference'
    )

    # Streak tracking
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)

    # Family link (for family competitions and challenges)
    family = models.ForeignKey(
        'family.Family',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children'
    )

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        db_table = 'children'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['language', 'level']),
        ]

    def __str__(self):
        return f"{self.name} ({self.user.email})"

    @property
    def age(self):
        from apps.core.utils import calculate_age
        return calculate_age(self.date_of_birth)

    def update_streak(self) -> int:
        """
        Update the child's activity streak based on daily activity.
        Call this when the child completes any learning activity.
        Returns the updated current streak.
        """
        from django.utils import timezone
        from datetime import timedelta

        today = timezone.now().date()

        if self.last_activity_date is None:
            # First activity ever
            self.current_streak = 1
            self.longest_streak = 1
            self.last_activity_date = today
        elif self.last_activity_date == today:
            # Already recorded activity today, no change
            pass
        elif self.last_activity_date == today - timedelta(days=1):
            # Consecutive day - increment streak
            self.current_streak += 1
            if self.current_streak > self.longest_streak:
                self.longest_streak = self.current_streak
            self.last_activity_date = today
        else:
            # Streak broken - reset to 1
            self.current_streak = 1
            self.last_activity_date = today

        self.save(update_fields=['current_streak', 'longest_streak', 'last_activity_date'])
        return self.current_streak

    def get_current_streak(self) -> int:
        """
        Get the current streak, accounting for broken streaks.
        If no activity yesterday or today, streak is 0.
        """
        from django.utils import timezone
        from datetime import timedelta

        if self.last_activity_date is None:
            return 0

        today = timezone.now().date()
        yesterday = today - timedelta(days=1)

        if self.last_activity_date == today or self.last_activity_date == yesterday:
            return self.current_streak
        else:
            # Streak is broken
            return 0
