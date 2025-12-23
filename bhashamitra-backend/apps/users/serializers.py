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
            'subscription_tier', 'subscription_expires_at', 'subscription_info', 'tts_provider'
        ]
        read_only_fields = ['id', 'role', 'created_at', 'subscription_tier', 'subscription_expires_at']

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
