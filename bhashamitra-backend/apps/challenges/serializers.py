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
    """Serializer for creating a new challenge."""

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
    category = serializers.ChoiceField(
        choices=ChallengeCategory.choices,
        default=ChallengeCategory.VOCABULARY
    )
    difficulty = serializers.ChoiceField(
        choices=ChallengeDifficulty.choices,
        default=ChallengeDifficulty.EASY
    )
    question_count = serializers.IntegerField(min_value=3, max_value=10, default=5)
    time_limit_seconds = serializers.IntegerField(min_value=10, max_value=120, default=30)
    child_id = serializers.UUIDField(required=False, allow_null=True)


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
    """
    Challenge serializer for the creator's list view.
    Includes comprehensive stats but strips answers from questions for security.
    """

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
        """Strip correct_index from questions to prevent cheating."""
        from .services import ChallengeService
        return ChallengeService.strip_answers(obj.questions)


class PublicChallengeSerializer(serializers.ModelSerializer):
    """
    Public challenge serializer - NO CORRECT ANSWERS!
    Used when participants access a challenge to play.
    """

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
        """Strip correct_index from questions to prevent cheating."""
        from .services import ChallengeService
        return ChallengeService.strip_answers(obj.questions)


class ChallengeAttemptCreateSerializer(serializers.Serializer):
    """Serializer for starting a challenge attempt."""

    participant_name = serializers.CharField(max_length=50)
    participant_location = serializers.CharField(max_length=50, required=False, allow_blank=True)


class ChallengeSubmitSerializer(serializers.Serializer):
    """Serializer for submitting challenge answers."""

    attempt_id = serializers.UUIDField()
    answers = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=3),
        min_length=1,
        max_length=10
    )
    time_taken_seconds = serializers.IntegerField(min_value=0)


class ChallengeAttemptSerializer(serializers.ModelSerializer):
    """Full attempt serializer with detailed results."""

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
    """Serializer for leaderboard entries."""

    rank = serializers.ReadOnlyField()

    class Meta:
        model = ChallengeAttempt
        fields = [
            'id', 'participant_name', 'participant_location', 'score',
            'max_score', 'percentage', 'time_taken_seconds', 'rank', 'completed_at',
        ]


class QuotaSerializer(serializers.ModelSerializer):
    """Serializer for user's challenge quota."""

    can_create = serializers.SerializerMethodField()
    message = serializers.SerializerMethodField()

    class Meta:
        model = UserChallengeQuota
        fields = [
            'challenges_created_today', 'total_challenges_created',
            'last_reset_date', 'can_create', 'message',
        ]

    def get_can_create(self, obj):
        user = self.context.get('user')
        is_paid = user.is_premium_tier or user.is_standard_tier if user else False
        can_create, _ = obj.can_create_challenge(is_paid)
        return can_create

    def get_message(self, obj):
        user = self.context.get('user')
        is_paid = user.is_premium_tier or user.is_standard_tier if user else False
        _, message = obj.can_create_challenge(is_paid)
        return message


class CategorySerializer(serializers.Serializer):
    """Serializer for available challenge categories."""

    value = serializers.CharField()
    label = serializers.CharField()
    item_count = serializers.IntegerField()
