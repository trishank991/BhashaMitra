"""Story serializers."""
from rest_framework import serializers
from .models import Story, StoryPage


class StoryPageSerializer(serializers.ModelSerializer):
    """Story page serializer."""

    class Meta:
        model = StoryPage
        fields = ['page_number', 'text_content', 'image_url', 'audio_url']


class StoryListSerializer(serializers.ModelSerializer):
    """Lightweight story list serializer."""

    class Meta:
        model = Story
        fields = [
            'id', 'storyweaver_id', 'title', 'title_translit', 'language',
            'level', 'page_count', 'cover_image_url', 'synopsis', 'author', 'categories'
        ]


class StoryDetailSerializer(serializers.ModelSerializer):
    """Full story with pages."""
    pages = StoryPageSerializer(many=True, read_only=True)

    class Meta:
        model = Story
        fields = [
            'id', 'storyweaver_id', 'title', 'title_translit', 'language',
            'level', 'page_count', 'cover_image_url', 'synopsis', 'author',
            'illustrator', 'categories', 'pages'
        ]
