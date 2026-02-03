"""Admin configuration for payments app."""
from django.contrib import admin
from .models import StripeCustomer, Subscription, Payment, WebhookEvent


@admin.register(StripeCustomer)
class StripeCustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'stripe_customer_id', 'created_at']
    search_fields = ['user__email', 'stripe_customer_id']
    readonly_fields = ['id', 'stripe_customer_id', 'created_at', 'updated_at']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'tier', 'status', 'billing_cycle', 'current_period_end', 'cancel_at_period_end']
    list_filter = ['status', 'tier', 'billing_cycle', 'cancel_at_period_end']
    search_fields = ['user__email', 'stripe_subscription_id']
    readonly_fields = ['id', 'stripe_subscription_id', 'stripe_price_id', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'currency', 'status', 'created_at']
    list_filter = ['status', 'currency', 'payment_method_type']
    search_fields = ['user__email', 'stripe_payment_intent_id', 'stripe_invoice_id']
    readonly_fields = ['id', 'stripe_payment_intent_id', 'stripe_invoice_id', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(WebhookEvent)
class WebhookEventAdmin(admin.ModelAdmin):
    list_display = ['event_type', 'stripe_event_id', 'processed', 'created_at', 'processed_at']
    list_filter = ['event_type', 'processed']
    search_fields = ['stripe_event_id', 'event_type']
    readonly_fields = ['id', 'stripe_event_id', 'event_type', 'payload', 'created_at']
    date_hierarchy = 'created_at'
