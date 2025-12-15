"""Progress serializers."""
from rest_framework import serializers
from .models import Progress, DailyActivity, ReadingSession
from apps.stories.serializers import StoryListSerializer


class ProgressSerializer(serializers.ModelSerializer):
    """Progress serializer."""
    story = StoryListSerializer(read_only=True)
    progress_percentage = serializers.IntegerField(read_only=True)

    class Meta:
        model = Progress
        fields = [
            'id', 'story', 'status', 'current_page', 'total_pages',
            'progress_percentage', 'time_spent_seconds',
            'started_at', 'completed_at', 'read_count', 'last_read_at'
        ]


class ProgressUpdateSerializer(serializers.Serializer):
    """Update progress serializer."""
    page = serializers.IntegerField(min_value=0)
    time_spent = serializers.IntegerField(min_value=0, required=False)


class DailyActivitySerializer(serializers.ModelSerializer):
    """Daily activity serializer."""

    class Meta:
        model = DailyActivity
        fields = [
            'date', 'stories_started', 'stories_completed',
            'pages_read', 'time_spent_seconds', 'points_earned',
            'recordings_made', 'letters_practiced', 'words_practiced',
            'games_played'
        ]


class ReadingSessionSerializer(serializers.ModelSerializer):
    """Reading session serializer."""

    class Meta:
        model = ReadingSession
        fields = [
            'id', 'story', 'start_page', 'end_page',
            'duration_seconds', 'started_at', 'ended_at'
        ]


class StartReadingSerializer(serializers.Serializer):
    """Start reading a story."""
    story_id = serializers.UUIDField()


class EndSessionSerializer(serializers.Serializer):
    """End a reading session."""
    end_page = serializers.IntegerField(min_value=0)
    duration_seconds = serializers.IntegerField(min_value=0)
