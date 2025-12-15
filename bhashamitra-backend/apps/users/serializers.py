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
        """Return subscription details."""
        tier_prices = {
            'FREE': '$0',
            'STANDARD': 'NZD $12/month',
            'PREMIUM': 'NZD $20/month',
        }
        tier_descriptions = {
            'FREE': 'Pre-cached curriculum audio only',
            'STANDARD': 'Unlimited Svara TTS (AI voices)',
            'PREMIUM': 'Sarvam AI human-like voices',
        }
        return {
            'tier': obj.subscription_tier,
            'price': tier_prices.get(obj.subscription_tier, 'Unknown'),
            'description': tier_descriptions.get(obj.subscription_tier, 'Unknown'),
            'is_active': obj.is_subscription_active,
            'expires_at': obj.subscription_expires_at,
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
