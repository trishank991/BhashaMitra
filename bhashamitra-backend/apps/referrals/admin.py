"""Admin configuration for referral models."""
from django.contrib import admin
from .models import ReferralCode, Referral, AmbassadorProgram


@admin.register(ReferralCode)
class ReferralCodeAdmin(admin.ModelAdmin):
    list_display = ['user', 'code', 'total_referrals', 'successful_referrals', 'is_active']
    list_filter = ['is_active']
    search_fields = ['user__email', 'code']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ['referrer', 'referred_email', 'status', 'reward_amount', 'converted_at']
    list_filter = ['status']
    search_fields = ['referrer__email', 'referred_email']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(AmbassadorProgram)
class AmbassadorProgramAdmin(admin.ModelAdmin):
    list_display = ['user', 'tier', 'commission_rate', 'total_earnings', 'lifetime_referrals', 'is_active']
    list_filter = ['tier', 'is_active']
    search_fields = ['user__email']
    readonly_fields = ['id', 'created_at', 'updated_at']
