"""Progress serializers."""
from rest_framework import serializers
from .models import Progress, DailyActivity
from apps.stories.serializers import StoryListSerializer


class ProgressSerializer(serializers.ModelSerializer):
    """Progress serializer."""
    story = StoryListSerializer(read_only=True)
    progress_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Progress
        fields = [
            'id', 'story', 'status', 'current_page', 'pages_completed',
            'progress_percentage', 'time_spent_seconds', 'points_earned',
            'started_at', 'completed_at', 'last_read_at'
        ]

    def get_progress_percentage(self, obj):
        """Calculate progress percentage based on story page count."""
        if obj.story and obj.story.page_count > 0:
            return int((obj.pages_completed / obj.story.page_count) * 100)
        return 0


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
            'recordings_made'
        ]


class StartReadingSerializer(serializers.Serializer):
    """Start reading a story."""
    story_id = serializers.UUIDField()


class EndSessionSerializer(serializers.Serializer):
    """End a reading session."""
    end_page = serializers.IntegerField(min_value=0)
    duration_seconds = serializers.IntegerField(min_value=0)
