"""Serializers for Song model."""
from rest_framework import serializers
from apps.curriculum.models import Song


class SongSerializer(serializers.ModelSerializer):
    """Serializer for Song model."""

    level_code = serializers.CharField(source='level.code', read_only=True)
    level_name = serializers.CharField(source='level.name_english', read_only=True)

    class Meta:
        model = Song
        fields = [
            'id',
            'language',
            'title_english',
            'title_hindi',
            'title_romanized',
            'lyrics_hindi',
            'lyrics_romanized',
            'lyrics_english',
            'age_min',
            'age_max',
            'level',
            'level_code',
            'level_name',
            'duration_seconds',
            'audio_url',
            'video_url',
            'category',
            'actions',
            'order',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SongListSerializer(serializers.ModelSerializer):
    """Simplified serializer for song lists."""

    level_code = serializers.CharField(source='level.code', read_only=True)

    class Meta:
        model = Song
        fields = [
            'id',
            'language',
            'title_english',
            'title_hindi',
            'title_romanized',
            'level_code',
            'duration_seconds',
            'category',
            'audio_url',
            'order',
        ]
