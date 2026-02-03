"""
Challenge API Serializers.

Two types of serializers:
1. Full serializers - For authenticated creators (includes correct answers)
2. Public serializers - For participants (no correct answers, no cheating!)
"""

from rest_framework import serializers
from django.utils import timezone
from .models import Challenge, ChallengeAttempt, UserChallengeQuota, ChallengeCategory, ChallengeDifficulty


class ChallengeCreateSerializer(serializers.Serializer):
    """Serializer for creating a new challenge with automatic case normalization."""

    title = serializers.CharField(max_length=100)
    title_native = serializers.CharField(max_length=100, required=False, allow_blank=True)
    language = serializers.ChoiceField(choices=[
        ('HINDI', 'Hindi'),
        ('TAMIL', 'Tamil'),
        ('GUJARATI', 'Gujarati'),
        ('PUNJABI', 'Punjabi'),
        ('TELUGU', 'Telugu'),
        ('MALAYALAM', 'Malayalam'),
        ('FIJI_HINDI', 'Fiji Hindi'),
    ])
    category = serializers.CharField()  # Changed to CharField to allow normalization
    difficulty = serializers.CharField() # Changed to CharField to allow normalization
    question_count = serializers.IntegerField(min_value=3, max_value=10, default=5)
    time_limit_seconds = serializers.IntegerField(min_value=10, max_value=120, default=30)
    child_id = serializers.UUIDField(required=False, allow_null=True)

    def validate_category(self, value):
        """Force VOCABULARY/ALPHABET to lowercase 'vocabulary'/'alphabet'."""
        normalized = value.lower()
        # Validate against allowed model choices
        valid_choices = [choice[0] for choice in ChallengeCategory.choices]
        if normalized not in valid_choices:
            raise serializers.ValidationError(f"'{value}' is not a valid category. Choices are: {valid_choices}")
        return normalized

    def validate_difficulty(self, value):
        """Force easy/EASY to lowercase 'easy'."""
        normalized = value.lower()
        valid_choices = [choice[0] for choice in ChallengeDifficulty.choices]
        if normalized not in valid_choices:
            raise serializers.ValidationError(f"'{value}' is not a valid difficulty. Choices are: {valid_choices}")
        return normalized


class ChallengeSerializer(serializers.ModelSerializer):
    """Full challenge serializer for creators."""

    share_url = serializers.ReadOnlyField()
    language_name = serializers.ReadOnlyField()
    is_expired = serializers.ReadOnlyField()
    participant_count = serializers.ReadOnlyField()
    creator_name = serializers.SerializerMethodField()

    class Meta:
        model = Challenge
        fields = [
            'id', 'code', 'title', 'title_native', 'language', 'language_name',
            'category', 'difficulty', 'question_count', 'time_limit_seconds',
            'questions', 'is_active', 'total_attempts', 'total_completions',
            'average_score', 'participant_count', 'expires_at', 'is_expired',
            'share_url', 'creator_name', 'created_at',
        ]
        read_only_fields = [
            'id', 'code', 'total_attempts', 'total_completions', 'average_score',
            'created_at', 'share_url', 'language_name', 'is_expired', 'participant_count',
        ]

    def get_creator_name(self, obj):
        if obj.creator_child:
            return obj.creator_child.display_name
        return obj.creator.email.split('@')[0]


class ChallengeListSerializer(serializers.ModelSerializer):
    """Serializer for the creator's list view (strips answers)."""

    share_url = serializers.ReadOnlyField()
    language_name = serializers.ReadOnlyField()
    is_expired = serializers.ReadOnlyField()
    participant_count = serializers.ReadOnlyField()
    creator_name = serializers.SerializerMethodField()
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Challenge
        fields = [
            'id', 'code', 'title', 'title_native', 'language', 'language_name',
            'category', 'difficulty', 'question_count', 'time_limit_seconds',
            'questions', 'is_active', 'total_attempts', 'total_completions',
            'average_score', 'participant_count', 'expires_at', 'is_expired',
            'share_url', 'creator_name', 'created_at',
        ]

    def get_creator_name(self, obj):
        if obj.creator_child:
            return obj.creator_child.display_name
        return obj.creator.email.split('@')[0]

    def get_questions(self, obj):
        from .services import ChallengeService
        return ChallengeService.strip_answers(obj.questions)


class PublicChallengeSerializer(serializers.ModelSerializer):
    """Public challenge serializer - NO CORRECT ANSWERS."""

    language_name = serializers.ReadOnlyField()
    is_expired = serializers.ReadOnlyField()
    creator_name = serializers.SerializerMethodField()
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Challenge
        fields = [
            'id', 'code', 'title', 'title_native', 'language', 'language_name',
            'category', 'difficulty', 'question_count', 'time_limit_seconds',
            'questions', 'is_expired', 'creator_name',
        ]

    def get_creator_name(self, obj):
        if obj.creator_child:
            return obj.creator_child.display_name
        return obj.creator.email.split('@')[0]

    def get_questions(self, obj):
        from .services import ChallengeService
        return ChallengeService.strip_answers(obj.questions)


class ChallengeAttemptCreateSerializer(serializers.Serializer):
    participant_name = serializers.CharField(max_length=50)
    participant_location = serializers.CharField(max_length=50, required=False, allow_blank=True)


class ChallengeSubmitSerializer(serializers.Serializer):
    attempt_id = serializers.UUIDField(required=False)
    attemptId = serializers.UUIDField(required=False) 
    
    answers = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1
    )
    
    time_taken_seconds = serializers.IntegerField(required=False)
    timeTaken = serializers.IntegerField(required=False)

    def validate(self, data):
        # Handle camelCase from frontend
        if 'attemptId' in data:
            data['attempt_id'] = data.pop('attemptId')
        if 'timeTaken' in data:
            data['time_taken_seconds'] = data.pop('timeTaken')
        return data


class ChallengeAttemptSerializer(serializers.ModelSerializer):
    rank = serializers.ReadOnlyField()
    challenge_title = serializers.SerializerMethodField()

    class Meta:
        model = ChallengeAttempt
        fields = [
            'id', 'challenge', 'challenge_title', 'participant_name',
            'participant_location', 'score', 'max_score', 'percentage',
            'time_taken_seconds', 'answers', 'is_completed', 'completed_at',
            'rank', 'created_at',
        ]
        read_only_fields = [
            'id', 'score', 'max_score', 'percentage', 'is_completed',
            'completed_at', 'rank', 'created_at',
        ]

    def get_challenge_title(self, obj):
        return obj.challenge.title


class LeaderboardEntrySerializer(serializers.ModelSerializer):
    rank = serializers.ReadOnlyField()

    class Meta:
        model = ChallengeAttempt
        fields = [
            'id', 'participant_name', 'participant_location', 'score',
            'max_score', 'percentage', 'time_taken_seconds', 'rank', 'completed_at',
        ]


class QuotaSerializer(serializers.ModelSerializer):
    can_create = serializers.SerializerMethodField()
    message = serializers.SerializerMethodField()
    daily_limit = serializers.SerializerMethodField()

    class Meta:
        model = UserChallengeQuota
        fields = [
            'challenges_created_today', 'total_challenges_created',
            'last_reset_date', 'can_create', 'message', 'daily_limit',
        ]

    def get_daily_limit(self, obj):
        user = self.context.get('user')
        is_paid = False
        if user:
            is_paid = getattr(user, 'is_premium_tier', False) or getattr(user, 'is_standard_tier', False)
        
        if is_paid:
            return None # Represents unlimited
        
        # Corresponds to FREE_DAILY_LIMIT in the model
        return 2

    def get_can_create(self, obj):
        user = self.context.get('user')
        # Safer attribute access for Custom User models
        is_paid = False
        if user:
            is_paid = getattr(user, 'is_premium_tier', False) or getattr(user, 'is_standard_tier', False)
        can_create, _ = obj.can_create_challenge(is_paid)
        return can_create

    def get_message(self, obj):
        user = self.context.get('user')
        is_paid = False
        if user:
            is_paid = getattr(user, 'is_premium_tier', False) or getattr(user, 'is_standard_tier', False)
        _, message = obj.can_create_challenge(is_paid)
        return message


class CategorySerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()
    item_count = serializers.IntegerField()
    