"""Story serializers."""
from rest_framework import serializers
from .models import Story, StoryPage, StoryVocabulary


class StoryPageSerializer(serializers.ModelSerializer):
    """Story page serializer."""

    class Meta:
        model = StoryPage
        fields = [
            'page_number', 'text_content', 'image_url', 'audio_url',
            'text_hindi', 'text_romanized', 'highlight_words', 'image_description'
        ]


class StoryVocabularySerializer(serializers.ModelSerializer):
    """Story vocabulary serializer."""

    class Meta:
        model = StoryVocabulary
        fields = [
            'word_hindi', 'word_transliteration', 'word_english',
            'example_hindi', 'example_english', 'audio_url', 'image_url'
        ]


class StoryListSerializer(serializers.ModelSerializer):
    """Lightweight story list serializer."""

    class Meta:
        model = Story
        fields = [
            'id', 'storyweaver_id', 'slug', 'title', 'title_hindi', 'title_romanized',
            'title_translit', 'language', 'level', 'page_count', 'cover_image_url',
            'synopsis', 'author', 'categories', 'tier', 'theme', 'moral_hindi',
            'moral_english', 'xp_reward', 'estimated_minutes', 'is_featured',
            'age_min', 'age_max', 'is_l1_content'
        ]


class StoryDetailSerializer(serializers.ModelSerializer):
    """Full story with pages and vocabulary."""
    pages = StoryPageSerializer(many=True, read_only=True)
    vocabulary = StoryVocabularySerializer(many=True, read_only=True)

    class Meta:
        model = Story
        fields = [
            'id', 'storyweaver_id', 'slug', 'title', 'title_hindi', 'title_romanized',
            'title_translit', 'language', 'level', 'page_count', 'cover_image_url',
            'synopsis', 'author', 'illustrator', 'categories', 'tier', 'theme',
            'moral_hindi', 'moral_english', 'xp_reward', 'estimated_minutes',
            'is_featured', 'age_min', 'age_max', 'is_l1_content', 'pages', 'vocabulary'
        ]
