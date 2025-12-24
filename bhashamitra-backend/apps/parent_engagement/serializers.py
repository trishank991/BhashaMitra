"""
Parent Dashboard Serializers.
"""

from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta

from apps.children.models import Child
from apps.progress.models import DailyProgress, ActivityLog
from apps.parent_engagement.models import LearningGoal


class ChildBasicSerializer(serializers.ModelSerializer):
    """Basic child info for parent views."""

    age = serializers.SerializerMethodField()
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = Child
        fields = [
            'id', 'name', 'date_of_birth', 'age',
            'language', 'avatar_url', 'total_points',
            'level', 'created_at'
        ]

    def get_age(self, obj):
        if obj.date_of_birth:
            today = timezone.now().date()
            age = today.year - obj.date_of_birth.year
            if (today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day):
                age -= 1
            return age
        return None

    def get_avatar_url(self, obj):
        # avatar is a CharField (emoji/string), not an ImageField
        if hasattr(obj, 'avatar') and obj.avatar:
            return obj.avatar
        return None


class ActivityLogSerializer(serializers.ModelSerializer):
    """Activity log entry."""

    time_ago = serializers.SerializerMethodField()
    icon = serializers.SerializerMethodField()

    class Meta:
        model = ActivityLog
        fields = [
            'id', 'activity_type', 'description',
            'points_earned', 'created_at', 'time_ago', 'icon'
        ]

    def get_time_ago(self, obj):
        now = timezone.now()
        diff = now - obj.created_at

        if diff < timedelta(minutes=1):
            return "Just now"
        elif diff < timedelta(hours=1):
            mins = diff.seconds // 60
            return f"{mins} min{'s' if mins > 1 else ''} ago"
        elif diff < timedelta(days=1):
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff < timedelta(days=7):
            days = diff.days
            return f"{days} day{'s' if days > 1 else ''} ago"
        else:
            return obj.created_at.strftime("%b %d")

    def get_icon(self, obj):
        ICONS = {
            'LESSON_STARTED': '📚',
            'LESSON_COMPLETED': '✅',
            'EXERCISE_COMPLETED': '📝',
            'GAME_COMPLETED': '🎮',
            'BADGE_EARNED': '🏆',
            'LEVEL_UP': '⬆️',
            'STREAK_MILESTONE': '🔥',
            'FIRST_LOGIN': '👋',
        }
        return ICONS.get(obj.activity_type, '📌')


class DailyProgressSerializer(serializers.ModelSerializer):
    """Daily progress entry."""

    day_name = serializers.SerializerMethodField()

    class Meta:
        model = DailyProgress
        fields = [
            'date', 'day_name', 'time_spent_minutes',
            'lessons_completed', 'exercises_completed',
            'games_played', 'points_earned'
        ]

    def get_day_name(self, obj):
        return obj.date.strftime('%a')


class LearningGoalSerializer(serializers.Serializer):
    """Learning goal."""

    id = serializers.CharField()
    type = serializers.CharField(source='goal_type')
    title = serializers.SerializerMethodField()
    target_value = serializers.IntegerField()
    current_value = serializers.IntegerField()
    percentage = serializers.SerializerMethodField()
    deadline = serializers.DateField(source='end_date', allow_null=True)
    is_completed = serializers.SerializerMethodField()
    reward_points = serializers.IntegerField(default=50)

    def get_title(self, obj):
        """Generate title from goal type and target."""
        titles = {
            'DAILY_MINUTES': f'Learn for {obj.target_value} minutes daily',
            'WEEKLY_STORIES': f'Complete {obj.target_value} stories this week',
            'MONTHLY_POINTS': f'Earn {obj.target_value} points this month',
            'LEVEL_TARGET': f'Reach level {obj.target_value}',
        }
        return titles.get(obj.goal_type, f'{obj.goal_type}: {obj.target_value}')

    def get_percentage(self, obj):
        if obj.target_value == 0:
            return 0
        return min(100, round((obj.current_value / obj.target_value) * 100))

    def get_is_completed(self, obj):
        return obj.current_value >= obj.target_value


class WeeklyReportSerializer(serializers.Serializer):
    """Weekly progress report."""

    daily_data = serializers.ListField()
    summary = serializers.DictField()
    comparison = serializers.DictField()
    highlights = serializers.ListField()
    suggestions = serializers.ListField()


class ProgressUpdateSerializer(serializers.Serializer):
    """Progress update request."""

    type = serializers.ChoiceField(choices=['lesson', 'exercise', 'game'])
    duration_minutes = serializers.IntegerField(min_value=0, default=0)
    points_earned = serializers.IntegerField(min_value=0, default=0)
    details = serializers.DictField(required=False, default=dict)


class GoalCreateSerializer(serializers.Serializer):
    """Goal creation request."""

    type = serializers.ChoiceField(choices=[
        'daily_time', 'weekly_lessons', 'weekly_words', 'streak'
    ])
    target = serializers.IntegerField(min_value=1)
    deadline = serializers.DateField(required=False, allow_null=True)


class ParentPreferencesSerializer(serializers.Serializer):
    """Parent notification preferences."""

    notification_frequency = serializers.ChoiceField(
        choices=['DAILY', 'WEEKLY', 'MONTHLY', 'NONE'],
        required=False
    )
    email_reports = serializers.BooleanField(required=False)
    push_notifications = serializers.BooleanField(required=False)
    sms_alerts = serializers.BooleanField(required=False)
    preferred_report_day = serializers.IntegerField(
        min_value=0,
        max_value=6,
        required=False
    )
    timezone = serializers.CharField(max_length=50, required=False)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
