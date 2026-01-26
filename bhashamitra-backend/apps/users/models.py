"""User models."""
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone
from datetime import timedelta
import uuid
import secrets


class SoftDeleteUserManager(UserManager):
    """Custom manager that excludes soft-deleted users by default."""
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class User(AbstractUser):
    """Custom user model for parents."""

    class Role(models.TextChoices):
        PARENT = 'PARENT', 'Parent'
        ADMIN = 'ADMIN', 'Admin'

    class SubscriptionTier(models.TextChoices):
        FREE = 'FREE', 'Free'
        STANDARD = 'STANDARD', 'Standard (NZD $20/month)'
        PREMIUM = 'PREMIUM', 'Premium (NZD $30/month)'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.PARENT)
    avatar_url = models.URLField(blank=True, null=True)

    # Multi-tenant support (nullable for backward compatibility)
    tenant = models.ForeignKey(
        'core.Tenant',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        help_text='Organization/tenant this user belongs to'
    )

    # Subscription fields
    subscription_tier = models.CharField(
        max_length=20,
        choices=SubscriptionTier.choices,
        default=SubscriptionTier.FREE,
        help_text='User subscription tier determines TTS provider and content access'
    )
    subscription_expires_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When the current subscription expires (null = never for free tier)'
    )

    # Email verification
    email_verified = models.BooleanField(
        default=False,
        help_text='Whether the user has verified their email address'
    )
    email_verified_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When the email was verified'
    )

    # Onboarding status
    is_onboarded = models.BooleanField(
        default=False,
        help_text='Whether the user has completed the onboarding process'
    )
    onboarding_completed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When the user completed onboarding'
    )

    # Live class tracking
    live_classes_used_this_month = models.IntegerField(
        default=0,
        help_text='Number of live classes used in the current month'
    )
    live_classes_month = models.DateField(
        null=True,
        blank=True,
        help_text='The month for which live_classes_used_this_month is tracked'
    )

    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Email as username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']  # Don't include username since email is USERNAME_FIELD

    objects = SoftDeleteUserManager()
    all_objects = UserManager()

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
        ]

    def __str__(self):
        return self.email

    @property
    def is_deleted(self):
        return self.deleted_at is not None

    def soft_delete(self):
        """Mark record as deleted."""
        from django.utils import timezone
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])

    def restore(self):
        """Restore a soft-deleted record."""
        self.deleted_at = None
        self.save(update_fields=['deleted_at'])

    @property
    def is_free_tier(self) -> bool:
        """Check if user is on free tier."""
        return self.subscription_tier == self.SubscriptionTier.FREE

    @property
    def is_standard_tier(self) -> bool:
        """Check if user is on standard tier."""
        return self.subscription_tier == self.SubscriptionTier.STANDARD

    @property
    def is_premium_tier(self) -> bool:
        """Check if user is on premium tier."""
        return self.subscription_tier == self.SubscriptionTier.PREMIUM

    @property
    def is_subscription_active(self) -> bool:
        """Check if user has an active paid subscription."""
        if self.is_free_tier:
            return True  # Free tier is always "active"
        if self.subscription_expires_at is None:
            return False
        return self.subscription_expires_at > timezone.now()

    @property
    def tts_provider(self) -> str:
        """Get the TTS provider for this user's tier.

        TTS Strategy (Dec 2024):
        - PREMIUM: google_wavenet (Google Cloud TTS WaveNet - highest quality)
        - STANDARD: google (Google Cloud TTS Standard - high quality)
        - FREE: cache_only (pre-cached content only)

        Paid tiers get real-time TTS. Free uses pre-cached audio.
        Fallback chain: Google → Sarvam → Svara
        """
        if self.is_premium_tier and self.is_subscription_active:
            return 'google_wavenet'
        elif self.is_standard_tier and self.is_subscription_active:
            return 'google'
        else:
            # Free tier - only serve pre-cached content
            return 'cache_only'

    def upgrade_to_tier(self, tier: str, duration_days: int = 30):
        """Upgrade user to a subscription tier."""
        if tier not in [t.value for t in self.SubscriptionTier]:
            raise ValueError(f"Invalid tier: {tier}")

        self.subscription_tier = tier
        if tier != self.SubscriptionTier.FREE:
            self.subscription_expires_at = timezone.now() + timedelta(days=duration_days)
        else:
            self.subscription_expires_at = None
        self.save(update_fields=['subscription_tier', 'subscription_expires_at'])

    @property
    def tier_features(self):
        """Get the feature configuration for this user's tier."""
        from apps.users.tier_config import get_tier_features
        return get_tier_features(self.subscription_tier)

    @property
    def story_limit(self) -> int:
        """Get the maximum number of stories this user can access."""
        if not self.is_subscription_active and not self.is_free_tier:
            return 5  # Expired subscription gets free tier limits
        return self.tier_features.story_limit

    @property
    def daily_game_limit(self) -> int:
        """Get the maximum games per day. Returns -1 for unlimited."""
        if not self.is_subscription_active and not self.is_free_tier:
            return 2  # Expired subscription gets free tier limits
        return self.tier_features.games_per_day

    @property
    def child_profile_limit(self) -> int:
        """Get the maximum number of child profiles allowed."""
        if not self.is_subscription_active and not self.is_free_tier:
            return 1  # Expired subscription gets free tier limits
        return self.tier_features.child_profiles

    @property
    def can_access_curriculum_progression(self) -> bool:
        """Check if user can access the L1-L10 curriculum journey."""
        return self.tier_features.has_curriculum_progression and self.is_subscription_active

    @property
    def can_access_peppi_ai_chat(self) -> bool:
        """Check if user can access Peppi's AI chat system."""
        return self.tier_features.has_peppi_ai_chat and self.is_subscription_active

    @property
    def can_access_peppi_narration(self) -> bool:
        """Check if user can access Peppi story narration."""
        return self.tier_features.has_peppi_narration and self.is_subscription_active

    @property
    def can_access_live_classes(self) -> bool:
        """Check if user can access live classes."""
        return self.tier_features.has_live_classes and self.is_subscription_active

    @property
    def free_live_classes_remaining(self) -> int:
        """Get remaining free live classes for this month."""
        if not self.can_access_live_classes:
            return 0

        # Check if we need to reset the monthly counter
        current_month = timezone.now().date().replace(day=1)
        if self.live_classes_month is None or self.live_classes_month < current_month:
            # New month or first time - full allowance available
            return self.tier_features.free_live_classes_per_month

        # Calculate remaining
        total_allowed = self.tier_features.free_live_classes_per_month
        remaining = total_allowed - self.live_classes_used_this_month
        return max(0, remaining)

    def record_live_class_usage(self) -> bool:
        """
        Record that the user attended a live class.
        Returns True if a free class was used, False if they need to pay.
        """
        if not self.can_access_live_classes:
            return False

        current_month = timezone.now().date().replace(day=1)

        # Reset counter if new month
        if self.live_classes_month is None or self.live_classes_month < current_month:
            self.live_classes_used_this_month = 0
            self.live_classes_month = current_month

        # Check if free classes remaining
        if self.free_live_classes_remaining > 0:
            self.live_classes_used_this_month += 1
            self.save(update_fields=['live_classes_used_this_month', 'live_classes_month'])
            return True

        return False

    @property
    def content_access_mode(self) -> str:
        """Get the content access mode: 'browse' or 'level_gated'."""
        if not self.is_subscription_active and not self.is_free_tier:
            return 'browse'  # Expired subscription gets free tier mode
        return self.tier_features.content_access_mode

    @property
    def can_access_games(self) -> bool:
        """Check if user can access games (with daily limits for free tier)."""
        # All tiers can access games, but free tier has daily limits
        return True

    @property
    def can_access_videos(self) -> bool:
        """Check if user can access cultural videos (paid tiers only)."""
        return (self.is_standard_tier or self.is_premium_tier) and self.is_subscription_active

    @property
    def voice_type(self) -> str:
        """Get the voice type for TTS based on tier."""
        if self.is_premium_tier and self.is_subscription_active:
            return 'premium'  # Sarvam AI (manisha/abhilash)
        else:
            return 'standard'  # Svara TTS for all tiers (FREE included)

    def can_access_level_content(self, content_level: int, child_level: int = 1) -> bool:
        """
        Check if user can access content at a specific level.

        FREE tier: Can only access L1 content
        STANDARD/PREMIUM: Can access content up to their child's current level
        """
        from apps.users.tier_config import can_access_content
        return can_access_content(self.subscription_tier, content_level, child_level)

    def verify_email(self):
        """Mark user's email as verified."""
        self.email_verified = True
        self.email_verified_at = timezone.now()
        self.save(update_fields=['email_verified', 'email_verified_at'])

    def complete_onboarding(self):
        """Mark user as having completed onboarding."""
        self.is_onboarded = True
        self.onboarding_completed_at = timezone.now()
        self.save(update_fields=['is_onboarded', 'onboarding_completed_at'])


class EmailVerificationToken(models.Model):
    """Token for email verification."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='verification_tokens'
    )
    token = models.CharField(max_length=64, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'email_verification_tokens'
        indexes = [
            models.Index(fields=['token']),
            models.Index(fields=['user', 'created_at']),
        ]

    def __str__(self):
        return f"Verification token for {self.user.email}"

    @classmethod
    def create_for_user(cls, user: User, hours_valid: int = 24) -> 'EmailVerificationToken':
        """Create a new verification token for a user."""
        # Invalidate any existing unused tokens
        cls.objects.filter(user=user, used_at__isnull=True).delete()

        token = secrets.token_urlsafe(48)
        expires_at = timezone.now() + timedelta(hours=hours_valid)

        return cls.objects.create(
            user=user,
            token=token,
            expires_at=expires_at
        )

    @property
    def is_valid(self) -> bool:
        """Check if token is still valid."""
        return (
            self.used_at is None and
            self.expires_at > timezone.now()
        )

    def use(self):
        """Mark token as used."""
        self.used_at = timezone.now()
        self.save(update_fields=['used_at'])


class PasswordResetToken(models.Model):
    """Token for password reset."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='password_reset_tokens'
    )
    token = models.CharField(max_length=64, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'password_reset_tokens'
        indexes = [
            models.Index(fields=['token']),
            models.Index(fields=['user', 'created_at']),
        ]

    def __str__(self):
        return f"Password reset token for {self.user.email}"

    @classmethod
    def create_for_user(cls, user: User, hours_valid: int = 1) -> 'PasswordResetToken':
        """Create a new password reset token for a user."""
        # Invalidate any existing unused tokens
        cls.objects.filter(user=user, used_at__isnull=True).delete()

        token = secrets.token_urlsafe(48)
        expires_at = timezone.now() + timedelta(hours=hours_valid)

        return cls.objects.create(
            user=user,
            token=token,
            expires_at=expires_at
        )

    @property
    def is_valid(self) -> bool:
        """Check if token is still valid."""
        return (
            self.used_at is None and
            self.expires_at > timezone.now()
        )

    def use(self):
        """Mark token as used."""
        self.used_at = timezone.now()
        self.save(update_fields=['used_at'])
