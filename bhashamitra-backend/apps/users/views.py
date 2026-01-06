"""User views."""
import logging
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model

from django.conf import settings
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    RequestPasswordResetSerializer,
    ResetPasswordSerializer,
    VerifyEmailSerializer,
    ResendVerificationSerializer,
    GoogleAuthSerializer,
)
from .models import EmailVerificationToken, PasswordResetToken
from .email_service import EmailService

logger = logging.getLogger(__name__)
User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """Register a new parent account."""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    throttle_scope = 'auth'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Create verification token and send email
        try:
            token = EmailVerificationToken.create_for_user(user)
            EmailService.send_verification_email(user, token)
            logger.info(f"Verification email sent to {user.email}")
        except Exception as e:
            logger.error(f"Failed to send verification email: {e}")
            # Don't fail registration if email fails

        # Send welcome email
        try:
            EmailService.send_welcome_email(user)
        except Exception as e:
            logger.error(f"Failed to send welcome email: {e}")

        refresh = RefreshToken.for_user(user)

        return Response({
            'data': UserSerializer(user).data,
            'session': {
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            },
            'meta': {
                'message': 'Registration successful. Please check your email to verify your account.',
                'email_verification_sent': True,
            }
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """Login and get JWT tokens."""
    permission_classes = [AllowAny]
    throttle_scope = 'auth'

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request,
            username=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )

        if not user:
            return Response(
                {'detail': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if user.is_deleted:
            return Response(
                {'detail': 'Account has been deactivated'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            'data': {
                'user': UserSerializer(user).data,
                'session': {
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                }
            }
        })


class LogoutView(APIView):
    """Logout and blacklist refresh token."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
        except Exception:
            pass

        return Response({'meta': {'message': 'Logged out successfully'}})


class MeView(generics.RetrieveUpdateAPIView):
    """Get or update current user."""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class SubscriptionTiersView(APIView):
    """Get available subscription tiers and pricing."""
    permission_classes = [AllowAny]

    def get(self, request):
        """Return all subscription tier information for pricing page."""
        from apps.users.tier_config import TIER_FEATURE_MATRIX

        return Response({
            'data': {
                'tiers': TIER_FEATURE_MATRIX,
                'currency': 'NZD',
                'billing_cycles': ['monthly', 'yearly'],
                'contact_for_custom': {
                    'email': 'support@bhashamitra.co.nz',
                    'note': 'For additional live classes and private sessions, contact our support team.',
                },
            }
        })


class CurrentSubscriptionDetailView(APIView):
    """Get detailed subscription info for current user's homepage."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return subscription details with homepage configuration."""
        from apps.users.tier_config import get_tier_features, get_tier_pricing

        user = request.user
        features = get_tier_features(user.subscription_tier)
        pricing = get_tier_pricing(user.subscription_tier)

        # Check both tier AND subscription active status for paid tier access
        is_paid = user.subscription_tier in ['STANDARD', 'PREMIUM'] and user.is_subscription_active

        return Response({
            'data': {
                'user_id': str(user.id),
                'tier': user.subscription_tier,
                'is_paid_tier': is_paid,
                'is_subscription_active': user.is_subscription_active,
                'expires_at': user.subscription_expires_at,
                # Homepage Configuration
                'homepage_mode': 'classroom' if is_paid else 'playground',
                'homepage_title': "Peppi's Classroom" if is_paid else "Peppi's Playground",
                # Feature Access
                'features': {
                    'has_curriculum_progression': features.has_curriculum_progression,
                    'has_peppi_ai_chat': features.has_peppi_ai_chat,
                    'has_peppi_narration': features.has_peppi_narration,
                    'has_live_classes': features.has_live_classes,
                    'has_progress_reports': features.has_progress_reports,
                    'content_access_mode': features.content_access_mode,
                    'tts_provider': features.tts_provider,
                },
                # Content Limits
                'limits': {
                    'story_limit': features.story_limit,
                    'games_per_day': features.games_per_day,
                    'child_profiles': features.child_profiles,
                    'free_live_classes': features.free_live_classes_per_month,
                },
                # Upgrade CTA (for free users)
                'upgrade_cta': None if is_paid else {
                    'message': 'Unlock the full learning journey!',
                    'button_text': 'Upgrade to Standard',
                    'price': f"NZD ${get_tier_pricing('STANDARD')['monthly']}/month",
                },
            }
        })


class VerifyEmailView(APIView):
    """Verify email address with token."""
    permission_classes = [AllowAny]
    throttle_scope = 'auth'

    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token_str = serializer.validated_data['token']

        try:
            token = EmailVerificationToken.objects.get(token=token_str)
        except EmailVerificationToken.DoesNotExist:
            return Response(
                {'detail': 'Invalid verification token'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not token.is_valid:
            return Response(
                {'detail': 'Token has expired or already been used'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Mark token as used and verify user
        token.use()
        token.user.verify_email()

        logger.info(f"Email verified for user {token.user.email}")

        return Response({
            'meta': {'message': 'Email verified successfully'},
            'data': {'email': token.user.email}
        })


class ResendVerificationView(APIView):
    """Resend verification email."""
    permission_classes = [AllowAny]
    throttle_scope = 'auth'

    def post(self, request):
        serializer = ResendVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Don't reveal if user exists
            return Response({
                'meta': {'message': 'If an account exists with this email, a verification link has been sent.'}
            })

        if user.email_verified:
            return Response({
                'meta': {'message': 'Email is already verified.'}
            })

        # Create new token and send
        token = EmailVerificationToken.create_for_user(user)
        EmailService.send_verification_email(user, token)

        logger.info(f"Verification email resent to {email}")

        return Response({
            'meta': {'message': 'If an account exists with this email, a verification link has been sent.'}
        })


class RequestPasswordResetView(APIView):
    """Request a password reset email."""
    permission_classes = [AllowAny]
    throttle_scope = 'auth'

    def post(self, request):
        serializer = RequestPasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
            # Create token and send email
            token = PasswordResetToken.create_for_user(user)
            EmailService.send_password_reset_email(user, token)
            logger.info(f"Password reset email sent to {email}")
        except User.DoesNotExist:
            # Don't reveal if user exists - just log
            logger.info(f"Password reset requested for non-existent email: {email}")

        # Always return success to prevent email enumeration
        return Response({
            'meta': {'message': 'If an account exists with this email, a password reset link has been sent.'}
        })


class ResetPasswordView(APIView):
    """Reset password with token."""
    permission_classes = [AllowAny]
    throttle_scope = 'auth'

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token_str = serializer.validated_data['token']
        new_password = serializer.validated_data['password']

        try:
            token = PasswordResetToken.objects.get(token=token_str)
        except PasswordResetToken.DoesNotExist:
            return Response(
                {'detail': 'Invalid reset token'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not token.is_valid:
            return Response(
                {'detail': 'Token has expired or already been used'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update password and mark token as used
        user = token.user
        user.set_password(new_password)
        user.save(update_fields=['password'])
        token.use()

        logger.info(f"Password reset successfully for user {user.email}")

        return Response({
            'meta': {'message': 'Password has been reset successfully. You can now log in with your new password.'}
        })


class CompleteOnboardingView(APIView):
    """Mark user's onboarding as complete."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user.complete_onboarding()
        serializer = UserSerializer(user)
        return Response({
            'success': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class GoogleAuthView(APIView):
    """Google OAuth authentication."""
    permission_classes = [AllowAny]
    throttle_scope = 'auth'

    def post(self, request):
        """
        Handle Google OAuth authentication.

        Accepts Google ID token from frontend, validates it,
        and creates/logs in user, returning JWT tokens.
        """
        serializer = GoogleAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        google_token = serializer.validated_data['token']

        try:
            # Verify the Google token using Google's tokeninfo endpoint
            import requests
            response = requests.get(
                f'https://oauth2.googleapis.com/tokeninfo?id_token={google_token}',
                timeout=10
            )

            if response.status_code != 200:
                logger.error(f"Google token validation failed: {response.text}")
                return Response(
                    {'detail': 'Invalid Google token'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            idinfo = response.json()

            # Verify token is for our app (if client ID is configured)
            google_client_id = getattr(settings, 'GOOGLE_OAUTH_CLIENT_ID', '')
            if google_client_id:
                if idinfo.get('aud') != google_client_id:
                    return Response(
                        {'detail': 'Invalid token audience'},
                        status=status.HTTP_401_UNAUTHORIZED
                    )
            else:
                # In production, this should be configured
                if not settings.DEBUG:
                    logger.warning(
                        "GOOGLE_OAUTH_CLIENT_ID not configured in production. "
                        "Token audience validation skipped - this is a security risk!"
                    )

            # Extract user info from Google token
            email = idinfo.get('email')
            name = idinfo.get('name', '')
            avatar_url = idinfo.get('picture', '')
            email_verified = idinfo.get('email_verified', 'false') == 'true'

            if not email:
                return Response(
                    {'detail': 'Email not provided by Google'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check if user exists
            try:
                user = User.objects.get(email=email)

                # Check if account is deleted
                if user.is_deleted:
                    return Response(
                        {'detail': 'Account has been deactivated'},
                        status=status.HTTP_401_UNAUTHORIZED
                    )

                # Update user info if changed
                updated = False
                if avatar_url and user.avatar_url != avatar_url:
                    user.avatar_url = avatar_url
                    updated = True

                # Mark email as verified if Google confirms it
                if email_verified and not user.email_verified:
                    user.verify_email()
                    updated = True

                if updated:
                    user.save()

                is_new_user = False
                logger.info(f"Google OAuth login for existing user: {email}")

            except User.DoesNotExist:
                # Create new user
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    name=name or email.split('@')[0],
                    avatar_url=avatar_url,
                )

                # Mark email as verified if Google confirms it
                if email_verified:
                    user.verify_email()

                is_new_user = True
                logger.info(f"New user created via Google OAuth: {email}")

                # Send welcome email for new users
                try:
                    EmailService.send_welcome_email(user)
                except Exception as e:
                    logger.error(f"Failed to send welcome email: {e}")

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)

            return Response({
                'data': {
                    'user': UserSerializer(user).data,
                    'session': {
                        'access_token': str(refresh.access_token),
                        'refresh_token': str(refresh),
                    }
                },
                'meta': {
                    'is_new_user': is_new_user,
                    'message': 'Registration successful' if is_new_user else 'Login successful',
                    'auth_provider': 'google'
                }
            }, status=status.HTTP_201_CREATED if is_new_user else status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Google OAuth error: {e}")
            return Response(
                {'detail': 'Authentication failed. Please try again.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
