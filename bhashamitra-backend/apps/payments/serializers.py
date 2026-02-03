"""Serializers for payments app."""
from rest_framework import serializers
from .models import Subscription, Payment


class CreateCheckoutSerializer(serializers.Serializer):
    """Serializer for creating a checkout session."""
    tier = serializers.ChoiceField(choices=['STANDARD', 'PREMIUM'])
    billing_cycle = serializers.ChoiceField(
        choices=['monthly', 'yearly'],
        default='monthly'
    )
    success_url = serializers.URLField(required=False, allow_null=True)
    cancel_url = serializers.URLField(required=False, allow_null=True)


class SubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for subscription details."""
    is_active = serializers.BooleanField(read_only=True)
    is_trialing = serializers.BooleanField(read_only=True)

    class Meta:
        model = Subscription
        fields = [
            'id',
            'tier',
            'status',
            'billing_cycle',
            'current_period_start',
            'current_period_end',
            'trial_start',
            'trial_end',
            'cancel_at_period_end',
            'is_active',
            'is_trialing',
            'created_at',
        ]
        read_only_fields = fields


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for payment history."""

    class Meta:
        model = Payment
        fields = [
            'id',
            'amount',
            'currency',
            'status',
            'payment_method_type',
            'card_last4',
            'card_brand',
            'description',
            'created_at',
        ]
        read_only_fields = fields


class CancelSubscriptionSerializer(serializers.Serializer):
    """Serializer for canceling a subscription."""
    cancel_immediately = serializers.BooleanField(default=False)
    reason = serializers.CharField(required=False, allow_blank=True, max_length=500)
