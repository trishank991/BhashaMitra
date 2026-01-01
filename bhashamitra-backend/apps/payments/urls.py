"""URL configuration for payments app."""
from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # Checkout
    path('checkout/', views.CreateCheckoutSessionView.as_view(), name='checkout'),

    # Customer portal
    path('portal/', views.CustomerPortalView.as_view(), name='portal'),

    # Subscription management
    path('subscription/', views.SubscriptionView.as_view(), name='subscription'),
    path('subscription/cancel/', views.CancelSubscriptionView.as_view(), name='cancel'),

    # Payment history
    path('history/', views.PaymentHistoryView.as_view(), name='history'),

    # Pricing info (public)
    path('pricing/', views.PricingInfoView.as_view(), name='pricing'),

    # Webhooks
    path('webhooks/stripe/', views.StripeWebhookView.as_view(), name='stripe-webhook'),
]
