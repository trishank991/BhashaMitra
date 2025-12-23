"""Serializers for Peppi models."""
from rest_framework import serializers
from apps.curriculum.models import PeppiPersonality, PeppiLearningContext


class PeppiPersonalitySerializer(serializers.ModelSerializer):
    """Serializer for PeppiPersonality model."""

    class Meta:
        model = PeppiPersonality
        fields = [
            'id',
            'age_group',
            'greeting_style',
            'encouragement_phrases',
            'teaching_style',
            'voice_tone',
            'avatar_expression',
            'is_active',
        ]
        read_only_fields = ['id']


class PeppiLearningContextSerializer(serializers.ModelSerializer):
    """Serializer for PeppiLearningContext model."""

    child_name = serializers.CharField(source='child.name', read_only=True)
    child_age = serializers.IntegerField(source='child.age', read_only=True)

    class Meta:
        model = PeppiLearningContext
        fields = [
            'id',
            'child',
            'child_name',
            'child_age',
            'current_topic',
            'words_taught_today',
            'mistakes_made',
            'mood',
            'last_interaction',
            'total_sessions',
            'streak_days',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'last_interaction']


class PeppiGreetingRequestSerializer(serializers.Serializer):
    """Serializer for greeting request."""

    time_of_day = serializers.ChoiceField(
        choices=['morning', 'afternoon', 'evening', 'night'],
        required=False
    )


class PeppiTeachWordRequestSerializer(serializers.Serializer):
    """Serializer for teach word request."""

    word_id = serializers.UUIDField(required=True)
    context = serializers.CharField(required=False, allow_blank=True)


class PeppiFeedbackRequestSerializer(serializers.Serializer):
    """Serializer for feedback request."""

    is_correct = serializers.BooleanField(required=True)
    activity_type = serializers.ChoiceField(
        choices=['pronunciation', 'vocabulary', 'listening', 'game'],
        required=True
    )
    difficulty = serializers.ChoiceField(
        choices=['easy', 'medium', 'hard'],
        required=False
    )
