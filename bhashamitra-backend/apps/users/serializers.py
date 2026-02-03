"""User serializers."""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """User details serializer."""
    subscription_info = serializers.SerializerMethodField()
    tts_provider = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'name', 'role', 'avatar_url', 'created_at',
            'subscription_tier', 'subscription_expires_at', 'subscription_info', 'tts_provider',
            'email_verified', 'is_onboarded', 'onboarding_completed_at'
        ]
        read_only_fields = ['id', 'role', 'created_at', 'subscription_tier', 'subscription_expires_at',
                            'email_verified', 'is_onboarded', 'onboarding_completed_at']

    def get_subscription_info(self, obj):
        """Return subscription details with full tier features."""
        from apps.users.tier_config import get_tier_pricing, get_tier_features

        pricing = get_tier_pricing(obj.subscription_tier)
        features = get_tier_features(obj.subscription_tier)

        return {
            'tier': obj.subscription_tier,
            'display_name': pricing['display_name'],
            'price_monthly': f"NZD ${pricing['monthly']}",
            'price_yearly': f"NZD ${pricing['yearly']}",
            'tagline': pricing['tagline'],
            'is_active': obj.is_subscription_active,
            'expires_at': obj.subscription_expires_at,
            # Content Limits
            'story_limit': obj.story_limit,
            'daily_game_limit': obj.daily_game_limit,
            'child_profile_limit': obj.child_profile_limit,
            # Feature Access
            'has_curriculum_progression': obj.can_access_curriculum_progression,
            'has_peppi_ai_chat': obj.can_access_peppi_ai_chat,
            'has_peppi_narration': obj.can_access_peppi_narration,
            'has_live_classes': obj.can_access_live_classes,
            'free_live_classes_remaining': obj.free_live_classes_remaining,
            'content_access_mode': obj.content_access_mode,
            'tts_provider': obj.tts_provider,
        }

    def get_tts_provider(self, obj):
        """Return the TTS provider for this user's tier."""
        return obj.tts_provider


class RegisterSerializer(serializers.ModelSerializer):
    """User registration serializer."""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password_confirm']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password_confirm': 'Passwords do not match'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
        )
        return user


class LoginSerializer(serializers.Serializer):
    """Login serializer."""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class RequestPasswordResetSerializer(serializers.Serializer):
    """Serializer for requesting a password reset."""
    email = serializers.EmailField()

    def validate_email(self, value):
        """Check if a user with this email exists."""
        # We don't reveal if the email exists for security
        # Just return the value and handle it in the view
        return value.lower()


class ResetPasswordSerializer(serializers.Serializer):
    """Serializer for resetting password with token."""
    token = serializers.CharField(max_length=64)
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password_confirm': 'Passwords do not match'})
        return attrs


class VerifyEmailSerializer(serializers.Serializer):
    """Serializer for email verification."""
    token = serializers.CharField(max_length=64)


class ResendVerificationSerializer(serializers.Serializer):
    """Serializer for resending verification email."""
    email = serializers.EmailField()

    def validate_email(self, value):
        return value.lower()


class GoogleAuthSerializer(serializers.Serializer):
    """Google OAuth token serializer."""
    token = serializers.CharField(
        required=True,
        help_text="Google OAuth ID token from frontend"
    )

    def validate_token(self, value):
        """Validate the Google token."""
        if not value:
            raise serializers.ValidationError("Token is required")
        return value
class ChallengeSubmitSerializer(serializers.Serializer):
    """
    Serializer for submitting challenge answers.
    Handles both snake_case (Backend) and camelCase (Frontend) to prevent 400 errors.
    """
    attempt_id = serializers.UUIDField(required=False)
    attemptId = serializers.UUIDField(required=False) 
    
    answers = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=3),
        min_length=1
    )
    
    time_taken_seconds = serializers.IntegerField(required=False)
    timeTaken = serializers.IntegerField(required=False)

    def validate(self, data):
        # Map camelCase from frontend to snake_case for backend logic
        if 'attemptId' in data:
            data['attempt_id'] = data.pop('attemptId')
        
        if 'timeTaken' in data:
            data['time_taken_seconds'] = data.pop('timeTaken')

        # Final check to ensure we have the ID needed for the database
        if not data.get('attempt_id'):
            raise serializers.ValidationError("An attempt_id or attemptId is required.")
            
        return data