"""
BhashaMitra Challenge System Models

Tier Model:
- FREE Users: 2 challenges per day
- STANDARD/PREMIUM Users: Unlimited challenges
- PARTICIPANTS: No account needed to play
"""

import os
import random
import string
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import timedelta

from apps.core.models import TimeStampedModel


def generate_challenge_code():
    """Generate a short, memorable challenge code (e.g., '7K3M')"""
    chars = string.ascii_uppercase + string.digits
    # Avoid confusing characters
    chars = chars.replace('O', '').replace('0', '').replace('I', '').replace('1', '').replace('L', '')
    return ''.join(random.choices(chars, k=4))


class ChallengeCategory(models.TextChoices):
    ALPHABET = 'alphabet', 'Alphabet Recognition'
    VOCABULARY = 'vocabulary', 'Vocabulary'
    NUMBERS = 'numbers', 'Numbers & Counting'
    COLORS = 'colors', 'Colors'
    ANIMALS = 'animals', 'Animals'
    FAMILY = 'family', 'Family Members'
    FOOD = 'food', 'Food & Fruits'
    GREETINGS = 'greetings', 'Greetings & Phrases'
    GRAMMAR = 'grammar', 'Grammar'


class ChallengeDifficulty(models.TextChoices):
    EASY = 'easy', 'Easy (Ages 4-6)'
    MEDIUM = 'medium', 'Medium (Ages 7-10)'
    HARD = 'hard', 'Hard (Ages 11-14)'


class Challenge(TimeStampedModel):
    """
    A shareable challenge/quiz that can be taken by anyone with the link.
    Creator must be logged in, but participants don't need accounts.
    """

    # Short shareable code (e.g., "7K3M" -> bhashamitra.app/c/7K3M)
    code = models.CharField(max_length=10, unique=True, default=generate_challenge_code, db_index=True)

    # Creator information
    # FIXED: Changed related_name to base_created_challenges to avoid clashes
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='base_created_challenges'
    )
    creator_child = models.ForeignKey(
        'children.Child',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='base_child_challenges'
    )

    # Challenge details
    title = models.CharField(max_length=100)
    title_native = models.CharField(max_length=100, blank=True)

    language = models.CharField(max_length=20, choices=[
        ('HINDI', 'Hindi'),
        ('TAMIL', 'Tamil'),
        ('GUJARATI', 'Gujarati'),
        ('PUNJABI', 'Punjabi'),
        ('TELUGU', 'Telugu'),
        ('MALAYALAM', 'Malayalam'),
        ('FIJI_HINDI', 'Fiji Hindi'),
    ])

    category = models.CharField(
        max_length=20,
        choices=ChallengeCategory.choices,
        default=ChallengeCategory.VOCABULARY
    )
    difficulty = models.CharField(
        max_length=10,
        choices=ChallengeDifficulty.choices,
        default=ChallengeDifficulty.EASY
    )

    # Quiz configuration
    question_count = models.PositiveIntegerField(
        default=5,
        validators=[MinValueValidator(3), MaxValueValidator(10)]
    )
    time_limit_seconds = models.PositiveIntegerField(default=30)  # per question

    # The actual questions (stored as JSON)
    questions = models.JSONField(default=list)

    # Metadata
    is_active = models.BooleanField(default=True)

    # Stats
    total_attempts = models.PositiveIntegerField(default=0)
    total_completions = models.PositiveIntegerField(default=0)
    average_score = models.FloatField(default=0.0)

    # Expiry (30 days for free users, null for paid)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'challenges'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['creator', 'created_at']),
            models.Index(fields=['language', 'category']),
        ]

    def __str__(self):
        return f"{self.title} ({self.code})"

    @property
    def share_url(self):
        # Use environment variable or default to localhost for local development
        base_url = os.environ.get('FRONTEND_URL', 'http://localhost:3000')
        return f"{base_url}/c/{self.code}"

    @property
    def is_expired(self):
        if self.expires_at is None:
            return False
        return timezone.now() > self.expires_at

    @property
    def participant_count(self):
        return self.attempts.filter(is_completed=True).values('participant_name').distinct().count()

    @property
    def language_name(self):
        language_map = {
            'HINDI': 'Hindi',
            'TAMIL': 'Tamil',
            'GUJARATI': 'Gujarati',
            'PUNJABI': 'Punjabi',
            'TELUGU': 'Telugu',
            'MALAYALAM': 'Malayalam',
            'FIJI_HINDI': 'Fiji Hindi',
        }
        return language_map.get(self.language, self.language)


class ChallengeAttempt(TimeStampedModel):
    """
    A single attempt at a challenge by a participant.
    Participants don't need accounts - just enter their name.
    """

    challenge = models.ForeignKey(
        Challenge,
        on_delete=models.CASCADE,
        related_name='attempts'
    )

    # Participant info (no account needed!)
    participant_name = models.CharField(max_length=50)
    participant_location = models.CharField(max_length=50, blank=True)

    # Optional: if participant is a registered user
    participant_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='challenge_attempts'
    )
    participant_child = models.ForeignKey(
        'children.Child',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='base_challenge_attempts'
    )

    # Results
    score = models.PositiveIntegerField(default=0)
    max_score = models.PositiveIntegerField(default=0)
    percentage = models.FloatField(default=0.0)
    time_taken_seconds = models.PositiveIntegerField(default=0)

    # Detailed answers (stored as JSON)
    answers = models.JSONField(default=list)

    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'challenge_attempts'
        ordering = ['-percentage', 'time_taken_seconds']
        indexes = [
            models.Index(fields=['challenge', 'is_completed']),
            models.Index(fields=['challenge', 'percentage', 'time_taken_seconds']),
        ]

    def __str__(self):
        return f"{self.participant_name} - {self.score}/{self.max_score}"

    @property
    def rank(self):
        """Get rank among all completed attempts for this challenge"""
        if not self.is_completed:
            return None

        better_attempts = ChallengeAttempt.objects.filter(
            challenge=self.challenge,
            is_completed=True
        ).filter(
            models.Q(percentage__gt=self.percentage) |
            models.Q(percentage=self.percentage, time_taken_seconds__lt=self.time_taken_seconds)
        ).count()
        return better_attempts + 1


class UserChallengeQuota(models.Model):
    """
    Track daily challenge creation quota for users.
    FREE: 2 challenges per day
    STANDARD/PREMIUM: Unlimited
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='challenge_quota'
    )

    challenges_created_today = models.PositiveIntegerField(default=0)
    last_reset_date = models.DateField(auto_now_add=True)
    total_challenges_created = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'user_challenge_quotas'

    def __str__(self):
        return f"{self.user.email} - {self.challenges_created_today} today"

    def reset_if_new_day(self):
        """Reset daily quota if it's a new day"""
        today = timezone.now().date()
        if self.last_reset_date < today:
            self.challenges_created_today = 0
            self.last_reset_date = today
            self.save(update_fields=['challenges_created_today', 'last_reset_date'])

    def can_create_challenge(self, is_paid_user: bool) -> tuple:
        """Check if user can create a new challenge."""
        self.reset_if_new_day()

        if is_paid_user:
            return True, "Unlimited challenges for paid users"

        FREE_DAILY_LIMIT = 2

        if self.challenges_created_today >= FREE_DAILY_LIMIT:
            return False, f"Daily limit reached ({FREE_DAILY_LIMIT}/day). Upgrade for unlimited!"

        remaining = FREE_DAILY_LIMIT - self.challenges_created_today
        return True, f"You have {remaining} challenge(s) remaining today"

    def record_challenge_created(self):
        """Record that a challenge was created"""
        self.reset_if_new_day()
        self.challenges_created_today += 1
        self.total_challenges_created += 1
        self.save(update_fields=['challenges_created_today', 'total_challenges_created'])


class PlayerRating(TimeStampedModel):
    """ELO-style competitive rating for registered players."""

    child = models.OneToOneField(
        'children.Child',
        on_delete=models.CASCADE,
        related_name='challenge_rating'
    )

    # Current rating
    current_rating = models.IntegerField(default=1000)
    highest_rating = models.IntegerField(default=1000)
    lowest_rating = models.IntegerField(default=1000)

    # Match statistics
    total_matches = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)

    # Streaks
    current_win_streak = models.IntegerField(default=0)
    best_win_streak = models.IntegerField(default=0)
    current_loss_streak = models.IntegerField(default=0)

    # Underdog statistics
    underdog_wins = models.IntegerField(default=0)  # Wins against higher-rated opponents
    giant_slayer_wins = models.IntegerField(default=0)  # Wins against 200+ higher rated

    # Derived fields
    rank_title = models.CharField(max_length=50, default='Learner')

    class Meta:
        db_table = 'player_ratings'
        ordering = ['-current_rating']

    @property
    def win_rate(self) -> float:
        if self.total_matches == 0:
            return 0.0
        return round((self.wins / self.total_matches) * 100, 1)

    def update_rank_title(self):
        """Update rank title based on current rating."""
        from django.conf import settings
        titles = settings.RATING_CONFIG['RANK_TITLES']

        for rating_threshold in sorted(titles.keys(), reverse=True):
            if self.current_rating >= rating_threshold:
                self.rank_title = titles[rating_threshold]
                break
        self.save(update_fields=['rank_title'])

    def __str__(self):
        return f"{self.child.name} - {self.current_rating} ({self.rank_title})"


class RatingHistory(TimeStampedModel):
    """Track rating changes over time."""

    player_rating = models.ForeignKey(
        PlayerRating,
        on_delete=models.CASCADE,
        related_name='history'
    )
    challenge_attempt = models.ForeignKey(
        ChallengeAttempt,
        on_delete=models.CASCADE,
        related_name='rating_changes'
    )

    rating_before = models.IntegerField()
    rating_after = models.IntegerField()
    rating_change = models.IntegerField()

    opponent_rating = models.IntegerField(null=True, blank=True)
    is_win = models.BooleanField()

    class Meta:
        db_table = 'rating_history'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.player_rating.child.name}: {self.rating_before} -> {self.rating_after}"