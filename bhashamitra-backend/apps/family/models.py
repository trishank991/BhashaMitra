"""Family models for multi-child competition and challenges."""
from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.core.models import TimeStampedModel
import secrets


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
    # Invite code for joining family (10 char uppercase alphanumeric)
    invite_code = models.CharField(max_length=10, unique=True, blank=True)
    # Code expires for security
    invite_code_expires_at = models.DateTimeField(null=True, blank=True)
    discount_tier = models.IntegerField(
        default=0,
        help_text='Discount percentage based on number of children'
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
        if not self.invite_code:
            self._generate_invite_code()
        super().save(*args, **kwargs)

    def _generate_invite_code(self):
        """Generate a new invite code that expires in 30 days."""
        self.invite_code = secrets.token_urlsafe(6)[:10].upper()
        self.invite_code_expires_at = timezone.now() + timezone.timedelta(days=30)

    def refresh_invite_code(self):
        """Generate a new invite code and invalidate the old one."""
        self._generate_invite_code()
        self.save(update_fields=['invite_code', 'invite_code_expires_at'])

    def is_invite_code_valid(self):
        """Check if current invite code is valid and not expired."""
        if not self.invite_code:
            return False
        if self.invite_code_expires_at and self.invite_code_expires_at < timezone.now():
            return False
        return True

    def calculate_discount(self):
        """Calculate family discount based on number of children."""
        if self.total_children >= 4:
            return 25
        elif self.total_children >= 3:
            return 15
        elif self.total_children >= 2:
            return 10
        return 0

    def get_children(self):
        """Get all children in this family."""
        from apps.children.models import Child
        return Child.objects.filter(user=self.primary_parent)

    def add_child(self, child):
        """Add a child to the family."""
        from apps.children.models import Child
        if child.user != self.primary_parent:
            raise ValueError("Child must belong to the primary parent")
        if child.family == self:
            return  # Already in family
        child.family = self
        child.save(update_fields=['family'])
        self._update_child_count()

    def remove_child(self, child):
        """Remove a child from the family."""
        if child.family != self:
            return  # Not in this family
        child.family = None
        child.save(update_fields=['family'])
        self._update_child_count()

    def _update_child_count(self):
        """Update total_children count based on children with this family."""
        from apps.children.models import Child
        self.total_children = Child.objects.filter(family=self).count()
        self.discount_tier = self.calculate_discount()
        self.save(update_fields=['total_children', 'discount_tier'])


class FamilyMembership(TimeStampedModel):
    """Tracks which children belong to which family.
    
    This model allows children to be linked to families separately from the parent,
    enabling scenarios where a child might be moved between families or where
    we need explicit membership tracking.
    """

    family = models.ForeignKey(
        Family,
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    child = models.ForeignKey(
        'children.Child',
        on_delete=models.CASCADE,
        related_name='family_memberships'
    )
    role = models.CharField(
        max_length=20,
        choices=[
            ('MEMBER', 'Member'),
            ('OWNER', 'Owner'),
        ],
        default='MEMBER'
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'family_memberships'
        unique_together = ['family', 'child']
        indexes = [
            models.Index(fields=['family', 'is_active']),
            models.Index(fields=['child', 'is_active']),
        ]

    def __str__(self):
        return f"{self.child.name} in {self.family}"


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


class CurriculumChallenge(TimeStampedModel):
    """Curriculum-based challenges for family competition.
    
    Challenges are curriculum-aware, meaning they only include content
    that children have actually learned (based on their progress).
    """

    class ChallengeType(models.TextChoices):
        ALPHABET = 'ALPHABET', 'Alphabet Recognition'
        VOCABULARY = 'VOCABULARY', 'Vocabulary'
        SENTENCES = 'SENTENCES', 'Sentence Building'
        MIMIC_PRONUNCIATION = 'MIMIC_PRONUNCIATION', 'Pronunciation Practice'
        DICTATION = 'DICTATION', 'Dictation Game'

    class Difficulty(models.TextChoices):
        EASY = 'EASY', 'Easy'
        MEDIUM = 'MEDIUM', 'Medium'
        HARD = 'HARD', 'Hard'

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        ACTIVE = 'ACTIVE', 'Active'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    family = models.ForeignKey(
        Family,
        on_delete=models.CASCADE,
        related_name='curriculum_challenges'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    challenge_type = models.CharField(
        max_length=30,
        choices=ChallengeType.choices
    )
    difficulty = models.CharField(
        max_length=10,
        choices=Difficulty.choices,
        default=Difficulty.EASY
    )
    # Curriculum scope - only include content at these levels
    min_level = models.IntegerField(default=1, help_text='Minimum curriculum level (1-10)')
    max_level = models.IntegerField(default=2, help_text='Maximum curriculum level (1-10)')
    # For custom word challenges (mimic/dictation)
    custom_words = models.JSONField(
        default=list,
        blank=True,
        help_text='List of custom words for pronunciation/dictation challenges'
    )
    target_count = models.IntegerField(
        default=10,
        help_text='Number of items to complete (questions/words)'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    winner = models.ForeignKey(
        'children.Child',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='curriculum_challenges_won'
    )
    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_challenges'
    )

    class Meta:
        db_table = 'curriculum_challenges'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['family', 'status']),
            models.Index(fields=['family', 'challenge_type']),
            models.Index(fields=['start_date', 'end_date']),
        ]

    def __str__(self):
        return f"{self.title} ({self.get_challenge_type_display()})"

    def is_active(self):
        """Check if challenge is currently active."""
        now = timezone.now()
        return (
            self.status == self.Status.ACTIVE and
            self.start_date <= now <= self.end_date
        )

    def is_expired(self):
        """Check if challenge has expired."""
        return timezone.now() > self.end_date

    def can_be_completed(self):
        """Check if challenge can be completed."""
        return self.is_active()


class CurriculumChallengeParticipant(TimeStampedModel):
    """Tracks individual child's participation in a curriculum challenge."""

    challenge = models.ForeignKey(
        CurriculumChallenge,
        on_delete=models.CASCADE,
        related_name='participants'
    )
    child = models.ForeignKey(
        'children.Child',
        on_delete=models.CASCADE,
        related_name='challenge_participations'
    )
    # Progress tracking
    completed_count = models.IntegerField(default=0)
    correct_count = models.IntegerField(default=0)
    accuracy_score = models.FloatField(default=0.0, help_text='Percentage correct (0-100)')
    # For pronunciation challenges
    best_accuracy = models.FloatField(default=0.0)
    # Timestamps
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'curriculum_challenge_participants'
        unique_together = ['challenge', 'child']
        indexes = [
            models.Index(fields=['challenge', 'child']),
            models.Index(fields=['challenge', 'accuracy_score']),
        ]

    def __str__(self):
        return f"{self.child.name} - {self.challenge.title}"

    def update_progress(self, is_correct: bool):
        """Update progress after an attempt."""
        self.completed_count += 1
        if is_correct:
            self.correct_count += 1
        # Recalculate accuracy
        self.accuracy_score = (self.correct_count / self.completed_count * 100) if self.completed_count > 0 else 0
        self.save(update_fields=['completed_count', 'correct_count', 'accuracy_score'])

    def mark_complete(self):
        """Mark participant as completed."""
        self.completed_at = timezone.now()
        self.save(update_fields=['completed_at'])


class CurriculumChallengeAttempt(TimeStampedModel):
    """Individual attempt on a curriculum challenge item."""

    participant = models.ForeignKey(
        CurriculumChallengeParticipant,
        on_delete=models.CASCADE,
        related_name='attempts'
    )
    # Item details
    item_type = models.CharField(
        max_length=20,
        choices=[
            ('ALPHABET', 'Alphabet'),
            ('VOCABULARY', 'Vocabulary'),
            ('SENTENCE', 'Sentence'),
            ('PRONUNCIATION', 'Pronunciation'),
            ('DICTATION', 'Dictation'),
        ]
    )
    item_id = models.CharField(max_length=100, help_text='ID or text of the item')
    item_value = models.TextField(help_text='The actual content (word, letter, etc.)')
    # Attempt result
    user_answer = models.TextField(blank=True)
    is_correct = models.BooleanField(default=False)
    # For pronunciation/dictation
    audio_url = models.URLField(blank=True, null=True)
    transcription = models.TextField(blank=True, help_text='What child said (for dictation)')
    accuracy_score = models.FloatField(default=0.0, help_text='Pronunciation accuracy (0-100)')

    class Meta:
        db_table = 'curriculum_challenge_attempts'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['participant', 'created_at']),
        ]

    def __str__(self):
        return f"Attempt by {self.participant.child.name} on {self.item_value}"


# Keep legacy SiblingChallenge for backwards compatibility
class SiblingChallenge(TimeStampedModel):
    """Legacy: Friendly challenges between siblings. Use CurriculumChallenge instead."""

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
        related_name='sibling_challenges_won'
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
