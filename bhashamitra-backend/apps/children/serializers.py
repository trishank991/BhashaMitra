"""Child serializers."""
from rest_framework import serializers
from django.conf import settings
from datetime import date
from .models import Child


class ChildSerializer(serializers.ModelSerializer):
    """Child profile serializer."""
    age = serializers.IntegerField(read_only=True)

    class Meta:
        model = Child
        fields = [
            'id', 'name', 'avatar', 'date_of_birth', 'language',
            'level', 'total_points', 'age', 'created_at'
        ]
        read_only_fields = ['id', 'level', 'total_points', 'created_at']


class CreateChildSerializer(serializers.ModelSerializer):
    """Create child serializer."""

    class Meta:
        model = Child
        fields = ['name', 'date_of_birth', 'language', 'avatar']

    def validate_date_of_birth(self, value):
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))

        if age < settings.MIN_CHILD_AGE:
            raise serializers.ValidationError(f"Child must be at least {settings.MIN_CHILD_AGE} years old")
        if age > settings.MAX_CHILD_AGE:
            raise serializers.ValidationError(f"Child must be under {settings.MAX_CHILD_AGE} years old")

        return value

    def validate(self, attrs):
        user = self.context['request'].user
        if user.children.filter(deleted_at__isnull=True).count() >= settings.MAX_CHILDREN_PER_USER:
            raise serializers.ValidationError(
                f"Maximum of {settings.MAX_CHILDREN_PER_USER} children allowed per account"
            )
        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class UpdateChildSerializer(serializers.ModelSerializer):
    """Update child serializer."""

    class Meta:
        model = Child
        fields = ['name', 'avatar', 'language']


class ChildStatsSerializer(serializers.Serializer):
    """Child statistics serializer."""
    child_id = serializers.UUIDField()
    period = serializers.CharField()
    stories_started = serializers.IntegerField()
    stories_completed = serializers.IntegerField()
    pages_read = serializers.IntegerField()
    time_spent_minutes = serializers.IntegerField()
    points_earned = serializers.IntegerField()
    recordings_made = serializers.IntegerField()
    current_streak = serializers.IntegerField()
    badges_earned = serializers.IntegerField()
