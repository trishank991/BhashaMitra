"""User views."""
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model

from .serializers import UserSerializer, RegisterSerializer, LoginSerializer

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

        refresh = RefreshToken.for_user(user)

        return Response({
            'data': UserSerializer(user).data,
            'session': {
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            },
            'meta': {'message': 'Registration successful'}
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
