"""Live classes and teacher models."""
from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel


class Teacher(TimeStampedModel):
    """Verified teachers for live classes."""

    class TeacherStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending Verification'
        VERIFIED = 'VERIFIED', 'Verified'
        SUSPENDED = 'SUSPENDED', 'Suspended'
        INACTIVE = 'INACTIVE', 'Inactive'

    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        related_name='teacher_profile'
    )
    display_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    profile_image = models.URLField(blank=True)
    languages = models.JSONField(default=list, help_text='List of language codes')
    specializations = models.JSONField(default=list)
    status = models.CharField(
        max_length=20,
        choices=TeacherStatus.choices,
        default=TeacherStatus.PENDING
    )
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    total_sessions = models.IntegerField(default=0)
    total_students = models.IntegerField(default=0)
    verified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'teachers'
        indexes = [
            models.Index(fields=['status', 'rating']),
        ]

    def __str__(self):
        return self.display_name


class TeacherCertification(TimeStampedModel):
    """Teacher qualifications and certifications."""

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='certifications'
    )
    title = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    credential_url = models.URLField(blank=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        db_table = 'teacher_certifications'

    def __str__(self):
        return f"{self.teacher.display_name} - {self.title}"


class LiveSession(TimeStampedModel):
    """Live tutoring sessions."""

    class SessionType(models.TextChoices):
        ONE_ON_ONE = 'ONE_ON_ONE', 'One-on-One'
        GROUP = 'GROUP', 'Group Session'
        CULTURAL_EVENT = 'CULTURAL_EVENT', 'Cultural Event'

    class SessionStatus(models.TextChoices):
        SCHEDULED = 'SCHEDULED', 'Scheduled'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'
        NO_SHOW = 'NO_SHOW', 'No Show'

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='sessions'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    session_type = models.CharField(
        max_length=20,
        choices=SessionType.choices,
        default=SessionType.ONE_ON_ONE
    )
    language = models.CharField(max_length=20)
    scheduled_start = models.DateTimeField()
    scheduled_end = models.DateTimeField()
    actual_start = models.DateTimeField(null=True, blank=True)
    actual_end = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=SessionStatus.choices,
        default=SessionStatus.SCHEDULED
    )
    max_participants = models.IntegerField(default=1)
    meeting_url = models.URLField(blank=True)
    recording_url = models.URLField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    class Meta:
        db_table = 'live_sessions'
        indexes = [
            models.Index(fields=['teacher', 'scheduled_start']),
            models.Index(fields=['status', 'scheduled_start']),
            models.Index(fields=['language']),
        ]

    def __str__(self):
        return f"{self.title} - {self.teacher.display_name}"


class SessionParticipant(TimeStampedModel):
    """Children enrolled in live sessions."""

    class ParticipantStatus(models.TextChoices):
        REGISTERED = 'REGISTERED', 'Registered'
        ATTENDED = 'ATTENDED', 'Attended'
        NO_SHOW = 'NO_SHOW', 'No Show'
        CANCELLED = 'CANCELLED', 'Cancelled'

    session = models.ForeignKey(
        LiveSession,
        on_delete=models.CASCADE,
        related_name='participants'
    )
    child = models.ForeignKey(
        'children.Child',
        on_delete=models.CASCADE,
        related_name='live_sessions'
    )
    status = models.CharField(
        max_length=20,
        choices=ParticipantStatus.choices,
        default=ParticipantStatus.REGISTERED
    )
    joined_at = models.DateTimeField(null=True, blank=True)
    left_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'session_participants'
        unique_together = ['session', 'child']

    def __str__(self):
        return f"{self.child.name} - {self.session.title}"


class SessionRating(TimeStampedModel):
    """Ratings for live sessions."""

    session = models.ForeignKey(
        LiveSession,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    child = models.ForeignKey(
        'children.Child',
        on_delete=models.CASCADE,
        related_name='session_ratings'
    )
    parent = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='session_ratings'
    )
    rating = models.IntegerField(help_text='1-5 star rating')
    feedback = models.TextField(blank=True)
    would_recommend = models.BooleanField(default=True)

    class Meta:
        db_table = 'session_ratings'
        unique_together = ['session', 'child']

    def __str__(self):
        return f"{self.session.title} - {self.rating} stars"


class SessionModerationLog(TimeStampedModel):
    """Moderation log for live sessions."""

    class ModerationAction(models.TextChoices):
        WARNING = 'WARNING', 'Warning Issued'
        MUTED = 'MUTED', 'User Muted'
        REMOVED = 'REMOVED', 'User Removed'
        SESSION_ENDED = 'SESSION_ENDED', 'Session Ended'

    session = models.ForeignKey(
        LiveSession,
        on_delete=models.CASCADE,
        related_name='moderation_logs'
    )
    moderator = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='moderation_actions'
    )
    action = models.CharField(max_length=20, choices=ModerationAction.choices)
    target_user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='moderation_targets'
    )
    reason = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'session_moderation_logs'

    def __str__(self):
        return f"{self.session.title} - {self.action}"


class TeacherPerformanceMetrics(TimeStampedModel):
    """Monthly performance metrics for teachers."""

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='performance_metrics'
    )
    month = models.DateField(help_text='First day of the month')
    sessions_conducted = models.IntegerField(default=0)
    total_students = models.IntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    attendance_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    complaints = models.IntegerField(default=0)
    positive_reviews = models.IntegerField(default=0)

    class Meta:
        db_table = 'teacher_performance_metrics'
        unique_together = ['teacher', 'month']

    def __str__(self):
        return f"{self.teacher.display_name} - {self.month}"
