"""Referral and ambassador program models."""
from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel
import secrets


def generate_referral_code():
    return secrets.token_urlsafe(8)[:10].upper()


class ReferralCode(TimeStampedModel):
    """User referral codes."""

    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        related_name='referral_code'
    )
    code = models.CharField(max_length=20, unique=True, default=generate_referral_code)
    total_referrals = models.IntegerField(default=0)
    successful_referrals = models.IntegerField(default=0)
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'referral_codes'

    def __str__(self):
        return f"{self.user.email} - {self.code}"


class Referral(TimeStampedModel):
    """Individual referral tracking."""

    class ReferralStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        SIGNED_UP = 'SIGNED_UP', 'Signed Up'
        TRIAL = 'TRIAL', 'In Trial'
        CONVERTED = 'CONVERTED', 'Converted to Paid'
        EXPIRED = 'EXPIRED', 'Expired'

    referrer = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='referrals_made'
    )
    referred_user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='referred_by'
    )
    referral_code = models.ForeignKey(
        ReferralCode,
        on_delete=models.CASCADE,
        related_name='referrals'
    )
    status = models.CharField(
        max_length=20,
        choices=ReferralStatus.choices,
        default=ReferralStatus.PENDING
    )
    referred_email = models.EmailField(blank=True)
    reward_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    reward_paid_at = models.DateTimeField(null=True, blank=True)
    converted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'referrals'
        indexes = [
            models.Index(fields=['referrer', 'status']),
            models.Index(fields=['referral_code']),
        ]

    def __str__(self):
        return f"{self.referrer.email} -> {self.referred_email or 'Pending'}"


class AmbassadorProgram(TimeStampedModel):
    """Community ambassador program membership."""

    class AmbassadorTier(models.TextChoices):
        BRONZE = 'BRONZE', 'Bronze'
        SILVER = 'SILVER', 'Silver'
        GOLD = 'GOLD', 'Gold'
        PLATINUM = 'PLATINUM', 'Platinum'

    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        related_name='ambassador_profile'
    )
    tier = models.CharField(
        max_length=20,
        choices=AmbassadorTier.choices,
        default=AmbassadorTier.BRONZE
    )
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pending_payout = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    lifetime_referrals = models.IntegerField(default=0)
    active_referrals = models.IntegerField(default=0)
    bio = models.TextField(blank=True)
    social_links = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ambassador_programs'

    def __str__(self):
        return f"{self.user.email} - {self.tier}"

    @property
    def tier_benefits(self):
        benefits = {
            'BRONZE': {'commission': 10, 'perks': ['Basic analytics']},
            'SILVER': {'commission': 15, 'perks': ['Extended analytics', 'Priority support']},
            'GOLD': {'commission': 20, 'perks': ['Extended analytics', 'Priority support', 'Free premium']},
            'PLATINUM': {'commission': 25, 'perks': ['All Gold benefits', 'Custom landing page', 'Monthly calls']},
        }
        return benefits.get(self.tier, benefits['BRONZE'])
