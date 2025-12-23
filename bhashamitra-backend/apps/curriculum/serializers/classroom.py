"""Serializers for Classroom model."""
from rest_framework import serializers
from apps.curriculum.models.classroom import Classroom


class ClassroomSerializer(serializers.ModelSerializer):
    """Basic Classroom serializer."""
    level_code = serializers.CharField(source='level.code', read_only=True)
    level_name = serializers.CharField(source='level.name_english', read_only=True)

    class Meta:
        model = Classroom
        fields = [
            'id', 'level', 'level_code', 'level_name', 'name', 'name_hindi',
            'theme', 'description', 'elements', 'background_color',
            'background_image_url', 'unlock_animation', 'ambient_sounds',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ClassroomDetailSerializer(serializers.ModelSerializer):
    """Detailed Classroom serializer with level information."""
    level_info = serializers.SerializerMethodField()

    class Meta:
        model = Classroom
        fields = [
            'id', 'level', 'level_info', 'name', 'name_hindi', 'theme',
            'description', 'elements', 'background_color', 'background_image_url',
            'unlock_animation', 'ambient_sounds', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_level_info(self, obj):
        return {
            'code': obj.level.code,
            'name_english': obj.level.name_english,
            'name_hindi': obj.level.name_hindi,
            'emoji': obj.level.emoji,
            'theme_color': obj.level.theme_color,
        }
