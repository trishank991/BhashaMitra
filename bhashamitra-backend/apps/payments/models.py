"""Payment models for Stripe integration."""
import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone


class StripeCustomer(models.Model):
    """Links a User to their Stripe customer ID."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='stripe_customer'
    )
    stripe_customer_id = models.CharField(max_length=255, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'stripe_customers'
        verbose_name = 'Stripe Customer'
        verbose_name_plural = 'Stripe Customers'

    def __str__(self):
        return f"{self.user.email} - {self.stripe_customer_id}"


class Subscription(models.Model):
    """Tracks Stripe subscriptions."""

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        PAST_DUE = 'past_due', 'Past Due'
        CANCELED = 'canceled', 'Canceled'
        INCOMPLETE = 'incomplete', 'Incomplete'
        INCOMPLETE_EXPIRED = 'incomplete_expired', 'Incomplete Expired'
        TRIALING = 'trialing', 'Trialing'
        UNPAID = 'unpaid', 'Unpaid'
        PAUSED = 'paused', 'Paused'

    class BillingCycle(models.TextChoices):
        MONTHLY = 'monthly', 'Monthly'
        YEARLY = 'yearly', 'Yearly'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    stripe_subscription_id = models.CharField(max_length=255, unique=True, db_index=True)
    stripe_price_id = models.CharField(max_length=255)

    tier = models.CharField(max_length=20, choices=[
        ('STANDARD', 'Standard'),
        ('PREMIUM', 'Premium'),
    ])
    billing_cycle = models.CharField(
        max_length=10,
        choices=BillingCycle.choices,
        default=BillingCycle.MONTHLY
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.INCOMPLETE
    )

    # Dates
    current_period_start = models.DateTimeField(null=True, blank=True)
    current_period_end = models.DateTimeField(null=True, blank=True)
    trial_start = models.DateTimeField(null=True, blank=True)
    trial_end = models.DateTimeField(null=True, blank=True)
    canceled_at = models.DateTimeField(null=True, blank=True)
    cancel_at_period_end = models.BooleanField(default=False)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'subscriptions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['stripe_subscription_id']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.tier} ({self.status})"

    @property
    def is_active(self) -> bool:
        """Check if subscription is in an active state."""
        return self.status in [
            self.Status.ACTIVE,
            self.Status.TRIALING,
        ]

    @property
    def is_trialing(self) -> bool:
        """Check if subscription is in trial period."""
        return self.status == self.Status.TRIALING


class Payment(models.Model):
    """Records individual payment transactions."""

    class Status(models.TextChoices):
        SUCCEEDED = 'succeeded', 'Succeeded'
        PENDING = 'pending', 'Pending'
        FAILED = 'failed', 'Failed'
        REFUNDED = 'refunded', 'Refunded'
        PARTIALLY_REFUNDED = 'partially_refunded', 'Partially Refunded'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments'
    )

    stripe_payment_intent_id = models.CharField(max_length=255, unique=True, db_index=True)
    stripe_invoice_id = models.CharField(max_length=255, null=True, blank=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='NZD')
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    # Payment method info
    payment_method_type = models.CharField(max_length=50, null=True, blank=True)
    card_last4 = models.CharField(max_length=4, null=True, blank=True)
    card_brand = models.CharField(max_length=20, null=True, blank=True)

    # Metadata
    description = models.TextField(null=True, blank=True)
    failure_reason = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['stripe_payment_intent_id']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.amount} {self.currency} ({self.status})"


class WebhookEvent(models.Model):
    """Stores Stripe webhook events for idempotency and debugging."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stripe_event_id = models.CharField(max_length=255, unique=True, db_index=True)
    event_type = models.CharField(max_length=100)
    payload = models.JSONField()
    processed = models.BooleanField(default=False)
    processing_error = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'webhook_events'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['stripe_event_id']),
            models.Index(fields=['event_type', 'processed']),
        ]

    def __str__(self):
        return f"{self.event_type} - {self.stripe_event_id}"

    def mark_processed(self, error: str = None):
        """Mark the event as processed."""
        self.processed = True
        self.processed_at = timezone.now()
        if error:
            self.processing_error = error
        self.save(update_fields=['processed', 'processed_at', 'processing_error'])
