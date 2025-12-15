"""User models."""
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone
from datetime import timedelta
import uuid


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
        STANDARD = 'STANDARD', 'Standard ($12/month)'
        PREMIUM = 'PREMIUM', 'Premium ($20/month)'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.PARENT)
    avatar_url = models.URLField(blank=True, null=True)

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

    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Email as username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'username']

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

        3-Tier TTS Strategy (Dec 2024):
        - FREE: cache_only (only pre-cached Svara content)
        - STANDARD: svara (real-time Svara TTS generation)
        - PREMIUM: sarvam (Sarvam AI Bulbul V2 - manisha voice at 50% pace)
        """
        if self.is_premium_tier and self.is_subscription_active:
            return 'sarvam'
        elif self.is_standard_tier and self.is_subscription_active:
            return 'svara'
        else:
            # FREE tier - only serve pre-cached content
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
    def story_limit(self) -> int:
        """Get the maximum number of stories this user can access."""
        if self.is_premium_tier and self.is_subscription_active:
            return 9999  # Unlimited
        elif self.is_standard_tier and self.is_subscription_active:
            return 8
        else:
            return 4  # FREE tier

    @property
    def can_access_games(self) -> bool:
        """Check if user can access games and quizzes (paid tiers only)."""
        return (self.is_standard_tier or self.is_premium_tier) and self.is_subscription_active

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
