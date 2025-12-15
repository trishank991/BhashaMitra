"""Gamification serializers."""
from rest_framework import serializers
from .models import Badge, ChildBadge, Streak, VoiceRecording


class BadgeSerializer(serializers.ModelSerializer):
    """Badge serializer."""

    class Meta:
        model = Badge
        fields = [
            'id', 'name', 'description', 'icon',
            'criteria_type', 'criteria_value',
            'display_order', 'points_bonus'
        ]


class ChildBadgeSerializer(serializers.ModelSerializer):
    """Child badge serializer."""
    badge = BadgeSerializer(read_only=True)

    class Meta:
        model = ChildBadge
        fields = ['id', 'badge', 'earned_at']


class StreakSerializer(serializers.ModelSerializer):
    """Streak serializer."""
    is_active_today = serializers.SerializerMethodField()

    class Meta:
        model = Streak
        fields = ['current_streak', 'longest_streak', 'last_activity_date', 'is_active_today']

    def get_is_active_today(self, obj):
        from django.utils import timezone
        today = timezone.now().date()
        return obj.last_activity_date == today


class VoiceRecordingSerializer(serializers.ModelSerializer):
    """Voice recording serializer."""

    class Meta:
        model = VoiceRecording
        fields = [
            'id', 'story', 'page_number', 'audio_url',
            'duration_ms', 'transcription', 'confidence_score',
            'recorded_at'
        ]
        read_only_fields = ['id', 'recorded_at']


class CreateRecordingSerializer(serializers.ModelSerializer):
    """Create voice recording serializer."""

    class Meta:
        model = VoiceRecording
        fields = [
            'story', 'page_number', 'audio_url', 'duration_ms'
        ]


class LeaderboardEntrySerializer(serializers.Serializer):
    """Leaderboard entry serializer."""
    rank = serializers.IntegerField()
    child_id = serializers.UUIDField()
    child_name = serializers.CharField()
    avatar = serializers.CharField()
    points = serializers.IntegerField()
    level = serializers.IntegerField()


class LevelProgressSerializer(serializers.Serializer):
    """Level progress serializer."""
    current_level = serializers.IntegerField()
    level_name = serializers.CharField()
    level_color = serializers.CharField()
    total_points = serializers.IntegerField()
    is_max_level = serializers.BooleanField()
    points_to_next = serializers.IntegerField()
    progress_percentage = serializers.IntegerField()
