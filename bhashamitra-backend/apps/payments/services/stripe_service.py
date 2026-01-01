"""Stripe integration service for BhashaMitra."""
import logging
from datetime import datetime
from decimal import Decimal
from typing import Optional, Dict, Any, Tuple

import stripe
from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.payments.models import StripeCustomer, Subscription, Payment, WebhookEvent
from apps.users.models import User

logger = logging.getLogger(__name__)


class StripeServiceError(Exception):
    """Custom exception for Stripe service errors."""
    pass


class StripeService:
    """Service for handling Stripe operations."""

    # Price IDs - configured via environment variables
    PRICE_IDS = {
        'STANDARD': {
            'monthly': settings.STRIPE_PRICE_STANDARD_MONTHLY,
            'yearly': settings.STRIPE_PRICE_STANDARD_YEARLY,
        },
        'PREMIUM': {
            'monthly': settings.STRIPE_PRICE_PREMIUM_MONTHLY,
            'yearly': settings.STRIPE_PRICE_PREMIUM_YEARLY,
        },
    }

    @classmethod
    def is_tier_available(cls, tier: str) -> bool:
        """Check if a tier is available for purchase."""
        if tier not in cls.PRICE_IDS:
            return False
        if tier == 'PREMIUM' and not settings.ENABLE_PREMIUM_TIER:
            return False
        return bool(cls.PRICE_IDS[tier].get('monthly'))

    @classmethod
    def _init_stripe(cls):
        """Initialize Stripe with API key."""
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.api_version = "2023-10-16"

    @classmethod
    def get_or_create_customer(cls, user: User) -> StripeCustomer:
        """Get or create a Stripe customer for a user."""
        cls._init_stripe()

        try:
            return user.stripe_customer
        except StripeCustomer.DoesNotExist:
            pass

        try:
            # Create customer in Stripe
            customer = stripe.Customer.create(
                email=user.email,
                name=user.name,
                metadata={
                    'user_id': str(user.id),
                }
            )

            # Save to database
            stripe_customer = StripeCustomer.objects.create(
                user=user,
                stripe_customer_id=customer.id
            )

            logger.info(f"Created Stripe customer {customer.id} for user {user.email}")
            return stripe_customer

        except stripe.error.StripeError as e:
            logger.error(f"Failed to create Stripe customer for {user.email}: {e}")
            raise StripeServiceError(f"Failed to create customer: {str(e)}")

    @classmethod
    def create_checkout_session(
        cls,
        user: User,
        tier: str,
        billing_cycle: str = 'monthly',
        trial_days: int = 7,
        success_url: str = None,
        cancel_url: str = None,
    ) -> Dict[str, Any]:
        """
        Create a Stripe Checkout Session for subscription.

        Returns the session ID and URL for redirecting the user.
        """
        cls._init_stripe()

        if tier not in cls.PRICE_IDS:
            raise StripeServiceError(f"Invalid tier: {tier}")

        # Check if tier is available (Premium may be disabled)
        if not cls.is_tier_available(tier):
            if tier == 'PREMIUM':
                raise StripeServiceError(
                    "Premium tier is not yet available. Please subscribe to Standard for now."
                )
            raise StripeServiceError(f"Tier {tier} is not available for purchase")

        if billing_cycle not in ['monthly', 'yearly']:
            raise StripeServiceError(f"Invalid billing cycle: {billing_cycle}")

        price_id = cls.PRICE_IDS[tier][billing_cycle]
        if not price_id:
            raise StripeServiceError(f"Price ID not configured for {tier} {billing_cycle}")

        # Get or create customer
        stripe_customer = cls.get_or_create_customer(user)

        # Build success/cancel URLs
        frontend_url = settings.FRONTEND_URL
        success_url = success_url or f"{frontend_url}/checkout/success?session_id={{CHECKOUT_SESSION_ID}}"
        cancel_url = cancel_url or f"{frontend_url}/pricing?canceled=true"

        try:
            # Check if user already has an active subscription
            existing_sub = Subscription.objects.filter(
                user=user,
                status__in=['active', 'trialing']
            ).first()

            if existing_sub:
                raise StripeServiceError(
                    "You already have an active subscription. "
                    "Please cancel it first or manage it from your profile."
                )

            # Create checkout session
            session_params = {
                'customer': stripe_customer.stripe_customer_id,
                'payment_method_types': ['card'],
                'mode': 'subscription',
                'line_items': [{
                    'price': price_id,
                    'quantity': 1,
                }],
                'success_url': success_url,
                'cancel_url': cancel_url,
                'metadata': {
                    'user_id': str(user.id),
                    'tier': tier,
                    'billing_cycle': billing_cycle,
                },
                'subscription_data': {
                    'metadata': {
                        'user_id': str(user.id),
                        'tier': tier,
                    },
                },
                'allow_promotion_codes': True,
            }

            # Add trial period for new customers only
            if trial_days > 0 and not user.subscriptions.exists():
                session_params['subscription_data']['trial_period_days'] = trial_days

            session = stripe.checkout.Session.create(**session_params)

            logger.info(
                f"Created checkout session {session.id} for user {user.email} "
                f"({tier} {billing_cycle})"
            )

            return {
                'session_id': session.id,
                'url': session.url,
            }

        except stripe.error.StripeError as e:
            logger.error(f"Failed to create checkout session: {e}")
            raise StripeServiceError(f"Failed to create checkout session: {str(e)}")

    @classmethod
    def create_customer_portal_session(cls, user: User, return_url: str = None) -> str:
        """
        Create a Stripe Customer Portal session for managing subscription.

        Returns the portal URL.
        """
        cls._init_stripe()

        try:
            stripe_customer = user.stripe_customer
        except StripeCustomer.DoesNotExist:
            raise StripeServiceError("No Stripe customer found for this user")

        frontend_url = settings.FRONTEND_URL
        return_url = return_url or f"{frontend_url}/profile"

        try:
            session = stripe.billing_portal.Session.create(
                customer=stripe_customer.stripe_customer_id,
                return_url=return_url,
            )

            logger.info(f"Created portal session for user {user.email}")
            return session.url

        except stripe.error.StripeError as e:
            logger.error(f"Failed to create portal session: {e}")
            raise StripeServiceError(f"Failed to create portal session: {str(e)}")

    @classmethod
    def cancel_subscription(
        cls,
        subscription: Subscription,
        cancel_at_period_end: bool = True,
        reason: str = None
    ) -> Subscription:
        """
        Cancel a subscription.

        Args:
            subscription: The subscription to cancel
            cancel_at_period_end: If True, cancel at end of billing period
            reason: Optional cancellation reason
        """
        cls._init_stripe()

        try:
            if cancel_at_period_end:
                # Cancel at end of period
                stripe_sub = stripe.Subscription.modify(
                    subscription.stripe_subscription_id,
                    cancel_at_period_end=True,
                    metadata={'cancellation_reason': reason} if reason else {}
                )
                subscription.cancel_at_period_end = True
            else:
                # Cancel immediately
                stripe_sub = stripe.Subscription.cancel(
                    subscription.stripe_subscription_id,
                )
                subscription.status = 'canceled'
                subscription.canceled_at = timezone.now()

            subscription.save()

            logger.info(
                f"Canceled subscription {subscription.stripe_subscription_id} "
                f"(at_period_end={cancel_at_period_end})"
            )

            return subscription

        except stripe.error.StripeError as e:
            logger.error(f"Failed to cancel subscription: {e}")
            raise StripeServiceError(f"Failed to cancel subscription: {str(e)}")

    @classmethod
    def handle_webhook_event(cls, payload: bytes, sig_header: str) -> bool:
        """
        Process a Stripe webhook event.

        Returns True if event was processed successfully.
        """
        cls._init_stripe()

        webhook_secret = settings.STRIPE_WEBHOOK_SECRET

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
        except ValueError as e:
            logger.error(f"Invalid webhook payload: {e}")
            raise StripeServiceError("Invalid payload")
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"Invalid webhook signature: {e}")
            raise StripeServiceError("Invalid signature")

        # Check for duplicate events (idempotency)
        event_id = event.id
        if WebhookEvent.objects.filter(stripe_event_id=event_id).exists():
            logger.info(f"Duplicate webhook event {event_id}, skipping")
            return True

        # Store the event
        webhook_event = WebhookEvent.objects.create(
            stripe_event_id=event_id,
            event_type=event.type,
            payload=event.data.object,
        )

        try:
            # Route to appropriate handler
            handler = cls._get_event_handler(event.type)
            if handler:
                handler(event.data.object)
            else:
                logger.debug(f"No handler for event type: {event.type}")

            webhook_event.mark_processed()
            return True

        except Exception as e:
            logger.error(f"Error processing webhook event {event_id}: {e}")
            webhook_event.mark_processed(error=str(e))
            return False

    @classmethod
    def _get_event_handler(cls, event_type: str):
        """Get the handler function for an event type."""
        handlers = {
            'checkout.session.completed': cls._handle_checkout_completed,
            'customer.subscription.created': cls._handle_subscription_created,
            'customer.subscription.updated': cls._handle_subscription_updated,
            'customer.subscription.deleted': cls._handle_subscription_deleted,
            'invoice.paid': cls._handle_invoice_paid,
            'invoice.payment_failed': cls._handle_payment_failed,
        }
        return handlers.get(event_type)

    @classmethod
    def _handle_checkout_completed(cls, session: Dict[str, Any]):
        """Handle checkout.session.completed event."""
        logger.info(f"Processing checkout.session.completed: {session.get('id')}")

        # The subscription is created separately via customer.subscription.created
        # This event mainly confirms the checkout was successful
        user_id = session.get('metadata', {}).get('user_id')
        if user_id:
            logger.info(f"Checkout completed for user {user_id}")

    @classmethod
    def _handle_subscription_created(cls, stripe_sub: Dict[str, Any]):
        """Handle customer.subscription.created event."""
        logger.info(f"Processing subscription created: {stripe_sub.get('id')}")
        cls._sync_subscription(stripe_sub)

    @classmethod
    def _handle_subscription_updated(cls, stripe_sub: Dict[str, Any]):
        """Handle customer.subscription.updated event."""
        logger.info(f"Processing subscription updated: {stripe_sub.get('id')}")
        cls._sync_subscription(stripe_sub)

    @classmethod
    def _handle_subscription_deleted(cls, stripe_sub: Dict[str, Any]):
        """Handle customer.subscription.deleted event."""
        logger.info(f"Processing subscription deleted: {stripe_sub.get('id')}")

        try:
            subscription = Subscription.objects.get(
                stripe_subscription_id=stripe_sub['id']
            )
            subscription.status = 'canceled'
            subscription.canceled_at = timezone.now()
            subscription.save()

            # Update user tier
            cls._update_user_tier(subscription.user)

        except Subscription.DoesNotExist:
            logger.warning(f"Subscription not found: {stripe_sub['id']}")

    @classmethod
    def _handle_invoice_paid(cls, invoice: Dict[str, Any]):
        """Handle invoice.paid event."""
        logger.info(f"Processing invoice paid: {invoice.get('id')}")

        # Find user from customer
        customer_id = invoice.get('customer')
        try:
            stripe_customer = StripeCustomer.objects.get(stripe_customer_id=customer_id)
            user = stripe_customer.user
        except StripeCustomer.DoesNotExist:
            logger.warning(f"Customer not found for invoice: {invoice['id']}")
            return

        # Find subscription if this is a subscription invoice
        subscription = None
        subscription_id = invoice.get('subscription')
        if subscription_id:
            try:
                subscription = Subscription.objects.get(
                    stripe_subscription_id=subscription_id
                )
            except Subscription.DoesNotExist:
                pass

        # Record payment
        Payment.objects.update_or_create(
            stripe_payment_intent_id=invoice.get('payment_intent', invoice['id']),
            defaults={
                'user': user,
                'subscription': subscription,
                'stripe_invoice_id': invoice['id'],
                'amount': Decimal(invoice['amount_paid']) / 100,  # Stripe uses cents
                'currency': invoice.get('currency', 'nzd').upper(),
                'status': 'succeeded',
                'description': f"Invoice {invoice['number']}",
            }
        )

    @classmethod
    def _handle_payment_failed(cls, invoice: Dict[str, Any]):
        """Handle invoice.payment_failed event."""
        logger.warning(f"Processing payment failed: {invoice.get('id')}")

        # Find subscription
        subscription_id = invoice.get('subscription')
        if subscription_id:
            try:
                subscription = Subscription.objects.get(
                    stripe_subscription_id=subscription_id
                )
                subscription.status = 'past_due'
                subscription.save()
            except Subscription.DoesNotExist:
                pass

    @classmethod
    def _sync_subscription(cls, stripe_sub: Dict[str, Any]):
        """Sync a Stripe subscription to the database."""
        # Get user from metadata or customer
        user_id = stripe_sub.get('metadata', {}).get('user_id')

        if not user_id:
            # Try to find via customer
            customer_id = stripe_sub.get('customer')
            try:
                stripe_customer = StripeCustomer.objects.get(
                    stripe_customer_id=customer_id
                )
                user = stripe_customer.user
            except StripeCustomer.DoesNotExist:
                logger.error(f"Cannot find user for subscription {stripe_sub['id']}")
                return
        else:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                logger.error(f"User not found: {user_id}")
                return

        # Get tier from metadata
        tier = stripe_sub.get('metadata', {}).get('tier', 'STANDARD')

        # Determine billing cycle from price
        items = stripe_sub.get('items', {}).get('data', [])
        billing_cycle = 'monthly'
        price_id = None
        if items:
            price = items[0].get('price', {})
            price_id = price.get('id')
            interval = price.get('recurring', {}).get('interval')
            if interval == 'year':
                billing_cycle = 'yearly'

        # Convert timestamps
        def ts_to_dt(ts):
            return datetime.fromtimestamp(ts, tz=timezone.utc) if ts else None

        # Create or update subscription
        subscription, created = Subscription.objects.update_or_create(
            stripe_subscription_id=stripe_sub['id'],
            defaults={
                'user': user,
                'stripe_price_id': price_id or '',
                'tier': tier,
                'billing_cycle': billing_cycle,
                'status': stripe_sub['status'],
                'current_period_start': ts_to_dt(stripe_sub.get('current_period_start')),
                'current_period_end': ts_to_dt(stripe_sub.get('current_period_end')),
                'trial_start': ts_to_dt(stripe_sub.get('trial_start')),
                'trial_end': ts_to_dt(stripe_sub.get('trial_end')),
                'cancel_at_period_end': stripe_sub.get('cancel_at_period_end', False),
            }
        )

        action = "Created" if created else "Updated"
        logger.info(f"{action} subscription {subscription.id} for user {user.email}")

        # Update user's subscription tier
        cls._update_user_tier(user)

    @classmethod
    def _update_user_tier(cls, user: User):
        """Update user's subscription tier based on active subscriptions."""
        # Find active subscription with highest tier
        active_sub = Subscription.objects.filter(
            user=user,
            status__in=['active', 'trialing']
        ).order_by(
            # Premium > Standard
            models.Case(
                models.When(tier='PREMIUM', then=0),
                models.When(tier='STANDARD', then=1),
                default=2,
            )
        ).first()

        if active_sub:
            user.subscription_tier = active_sub.tier
            user.subscription_expires_at = active_sub.current_period_end
        else:
            user.subscription_tier = 'FREE'
            user.subscription_expires_at = None

        user.save(update_fields=['subscription_tier', 'subscription_expires_at'])
        logger.info(f"Updated user {user.email} tier to {user.subscription_tier}")

    @classmethod
    def get_subscription_info(cls, user: User) -> Optional[Dict[str, Any]]:
        """Get user's current subscription information."""
        try:
            subscription = Subscription.objects.filter(
                user=user,
                status__in=['active', 'trialing', 'past_due']
            ).order_by('-created_at').first()

            if not subscription:
                return None

            return {
                'id': str(subscription.id),
                'tier': subscription.tier,
                'status': subscription.status,
                'billing_cycle': subscription.billing_cycle,
                'current_period_end': subscription.current_period_end.isoformat() if subscription.current_period_end else None,
                'cancel_at_period_end': subscription.cancel_at_period_end,
                'is_trialing': subscription.is_trialing,
                'trial_end': subscription.trial_end.isoformat() if subscription.trial_end else None,
            }
        except Exception as e:
            logger.error(f"Error getting subscription info: {e}")
            return None
