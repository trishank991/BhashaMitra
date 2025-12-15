"""Vocabulary serializers."""
from rest_framework import serializers
from apps.curriculum.models.vocabulary import VocabularyTheme, VocabularyWord, WordProgress


class VocabularyWordSerializer(serializers.ModelSerializer):
    """Basic vocabulary word serializer."""

    class Meta:
        model = VocabularyWord
        fields = [
            'id', 'word', 'romanization', 'translation',
            'part_of_speech', 'gender', 'pronunciation_audio_url',
            'image_url', 'order'
        ]


class VocabularyWordDetailSerializer(serializers.ModelSerializer):
    """Detailed vocabulary word serializer."""
    theme_name = serializers.CharField(source='theme.name', read_only=True)

    class Meta:
        model = VocabularyWord
        fields = [
            'id', 'word', 'romanization', 'translation',
            'part_of_speech', 'gender', 'pronunciation_audio_url',
            'image_url', 'example_sentence', 'difficulty',
            'order', 'theme_name'
        ]


class VocabularyThemeSerializer(serializers.ModelSerializer):
    """Basic theme serializer."""
    word_count = serializers.SerializerMethodField()

    class Meta:
        model = VocabularyTheme
        fields = [
            'id', 'language', 'name', 'name_native', 'description',
            'icon', 'level', 'order', 'is_premium', 'word_count'
        ]

    def get_word_count(self, obj):
        return obj.words.count()


class VocabularyThemeDetailSerializer(serializers.ModelSerializer):
    """Detailed theme serializer with words."""
    words = VocabularyWordSerializer(many=True, read_only=True)
    word_count = serializers.SerializerMethodField()

    class Meta:
        model = VocabularyTheme
        fields = [
            'id', 'language', 'name', 'name_native', 'description',
            'icon', 'level', 'order', 'is_premium', 'word_count', 'words'
        ]

    def get_word_count(self, obj):
        return obj.words.count()


class WordProgressSerializer(serializers.ModelSerializer):
    """Word progress serializer."""
    word = VocabularyWordSerializer(read_only=True)
    accuracy = serializers.ReadOnlyField()

    class Meta:
        model = WordProgress
        fields = [
            'id', 'word', 'ease_factor', 'interval_days',
            'repetitions', 'next_review', 'last_reviewed',
            'times_reviewed', 'times_correct', 'accuracy',
            'mastered', 'mastered_at'
        ]


class FlashcardSerializer(serializers.Serializer):
    """Serializer for flashcard review data."""
    word_id = serializers.UUIDField()
    word = serializers.CharField()
    romanization = serializers.CharField()
    translation = serializers.CharField()
    part_of_speech = serializers.CharField()
    gender = serializers.CharField()
    example_sentence = serializers.CharField(allow_blank=True)
    pronunciation_audio_url = serializers.URLField(allow_null=True)
    image_url = serializers.URLField(allow_null=True)
    # Progress info
    times_reviewed = serializers.IntegerField()
    interval_days = serializers.IntegerField()
    is_new = serializers.BooleanField()


class FlashcardReviewSerializer(serializers.Serializer):
    """Serializer for submitting flashcard review."""
    word_id = serializers.UUIDField()
    quality = serializers.IntegerField(min_value=0, max_value=5)


class FlashcardSessionSerializer(serializers.Serializer):
    """Serializer for batch flashcard review."""
    reviews = FlashcardReviewSerializer(many=True)
