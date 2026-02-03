"""Serializers for Teacher model."""
from rest_framework import serializers
from apps.curriculum.models.teacher import Teacher


class TeacherSerializer(serializers.ModelSerializer):
    """Basic Teacher serializer."""

    class Meta:
        model = Teacher
        fields = [
            'id', 'name', 'name_hindi', 'character_type', 'breed',
            'personality', 'voice_style', 'avatar_url', 'intro_message',
            'encouragement_phrases', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TeacherDetailSerializer(serializers.ModelSerializer):
    """Detailed Teacher serializer."""

    class Meta:
        model = Teacher
        fields = [
            'id', 'name', 'name_hindi', 'character_type', 'breed',
            'personality', 'voice_style', 'avatar_url', 'intro_message',
            'encouragement_phrases', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
