"""Views for payments app."""
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .serializers import (
    CreateCheckoutSerializer,
    SubscriptionSerializer,
    PaymentSerializer,
    CancelSubscriptionSerializer,
)
from .services.stripe_service import StripeService, StripeServiceError
from .models import Subscription, Payment

logger = logging.getLogger(__name__)


class CreateCheckoutSessionView(APIView):
    """
    POST /api/v1/payments/checkout/

    Create a Stripe Checkout session for subscription.
    Returns the checkout URL to redirect the user.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateCheckoutSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = StripeService.create_checkout_session(
                user=request.user,
                tier=serializer.validated_data['tier'],
                billing_cycle=serializer.validated_data.get('billing_cycle', 'monthly'),
                success_url=serializer.validated_data.get('success_url'),
                cancel_url=serializer.validated_data.get('cancel_url'),
            )
            return Response(result, status=status.HTTP_200_OK)

        except StripeServiceError as e:
            logger.error(f"Checkout error for {request.user.email}: {e}")
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class CustomerPortalView(APIView):
    """
    POST /api/v1/payments/portal/

    Create a Stripe Customer Portal session.
    Returns the portal URL for managing subscription.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return_url = request.data.get('return_url')

        try:
            url = StripeService.create_customer_portal_session(
                user=request.user,
                return_url=return_url,
            )
            return Response({'url': url}, status=status.HTTP_200_OK)

        except StripeServiceError as e:
            logger.error(f"Portal error for {request.user.email}: {e}")
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class SubscriptionView(APIView):
    """
    GET /api/v1/payments/subscription/

    Get current user's subscription details.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        subscription = Subscription.objects.filter(
            user=request.user,
            status__in=['active', 'trialing', 'past_due']
        ).order_by('-created_at').first()

        if not subscription:
            return Response({
                'subscription': None,
                'tier': request.user.subscription_tier,
                'has_subscription': False,
            })

        return Response({
            'subscription': SubscriptionSerializer(subscription).data,
            'tier': request.user.subscription_tier,
            'has_subscription': True,
        })


class CancelSubscriptionView(APIView):
    """
    POST /api/v1/payments/subscription/cancel/

    Cancel the current subscription.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CancelSubscriptionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Find active subscription
        subscription = Subscription.objects.filter(
            user=request.user,
            status__in=['active', 'trialing']
        ).first()

        if not subscription:
            return Response(
                {'detail': 'No active subscription found'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            cancel_immediately = serializer.validated_data.get('cancel_immediately', False)
            reason = serializer.validated_data.get('reason')

            updated_sub = StripeService.cancel_subscription(
                subscription=subscription,
                cancel_at_period_end=not cancel_immediately,
                reason=reason,
            )

            return Response({
                'message': 'Subscription canceled successfully',
                'subscription': SubscriptionSerializer(updated_sub).data,
            })

        except StripeServiceError as e:
            logger.error(f"Cancel error for {request.user.email}: {e}")
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class PaymentHistoryView(APIView):
    """
    GET /api/v1/payments/history/

    Get user's payment history.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payments = Payment.objects.filter(user=request.user).order_by('-created_at')[:20]
        return Response({
            'payments': PaymentSerializer(payments, many=True).data
        })


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(APIView):
    """
    POST /api/v1/payments/webhooks/stripe/

    Handle Stripe webhook events.
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

        if not sig_header:
            logger.warning("Webhook received without signature")
            return Response(
                {'detail': 'Missing signature'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            success = StripeService.handle_webhook_event(payload, sig_header)
            if success:
                return Response({'received': True})
            else:
                return Response(
                    {'detail': 'Event processing failed'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        except StripeServiceError as e:
            logger.error(f"Webhook error: {e}")
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class PricingInfoView(APIView):
    """
    GET /api/v1/payments/pricing/

    Get pricing information for all tiers (public endpoint).
    """
    permission_classes = [AllowAny]

    def get(self, request):
        from apps.users.tier_config import TIER_PRICING, TIER_FEATURE_MATRIX

        return Response({
            'pricing': TIER_PRICING,
            'features': TIER_FEATURE_MATRIX,
            'currency': 'NZD',
            'trial_days': 7,
        })
