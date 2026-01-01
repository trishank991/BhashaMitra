"""Script and alphabet serializers."""
from rest_framework import serializers
from apps.curriculum.models.script import Script, AlphabetCategory, Letter, Matra, LetterProgress


class LetterSerializer(serializers.ModelSerializer):
    """Basic letter serializer."""

    class Meta:
        model = Letter
        fields = [
            'id', 'character', 'romanization', 'ipa',
            'pronunciation_guide', 'audio_url', 'example_image', 'order'
        ]


class LetterDetailSerializer(serializers.ModelSerializer):
    """Detailed letter serializer with example words."""

    class Meta:
        model = Letter
        fields = [
            'id', 'character', 'romanization', 'ipa',
            'pronunciation_guide', 'audio_url', 'stroke_order_url',
            'example_word', 'example_word_romanization',
            'example_word_translation', 'example_image', 'order', 'is_active'
        ]


class MatraSerializer(serializers.ModelSerializer):
    """Matra (vowel mark) serializer."""

    class Meta:
        model = Matra
        fields = ['id', 'symbol', 'name', 'example_with_ka', 'audio_url', 'order']


class AlphabetCategorySerializer(serializers.ModelSerializer):
    """Alphabet category with letters."""
    letters = LetterSerializer(many=True, read_only=True)
    letter_count = serializers.SerializerMethodField()

    class Meta:
        model = AlphabetCategory
        fields = [
            'id', 'name', 'name_native', 'category_type',
            'description', 'order', 'letter_count', 'letters'
        ]

    def get_letter_count(self, obj):
        return obj.letters.count()


class ScriptSerializer(serializers.ModelSerializer):
    """Basic script serializer."""
    category_count = serializers.SerializerMethodField()

    class Meta:
        model = Script
        fields = [
            'id', 'language', 'name', 'name_native',
            'description', 'total_letters', 'category_count'
        ]

    def get_category_count(self, obj):
        return obj.categories.count()


class ScriptDetailSerializer(serializers.ModelSerializer):
    """Detailed script serializer with categories and matras."""
    categories = AlphabetCategorySerializer(many=True, read_only=True)
    matras = MatraSerializer(many=True, read_only=True)

    class Meta:
        model = Script
        fields = [
            'id', 'language', 'name', 'name_native',
            'description', 'total_letters', 'categories', 'matras'
        ]


class LetterProgressSerializer(serializers.ModelSerializer):
    """Letter progress serializer."""
    letter = LetterSerializer(read_only=True)
    overall_score = serializers.ReadOnlyField()

    class Meta:
        model = LetterProgress
        fields = [
            'id', 'letter', 'recognition_score', 'listening_score',
            'tracing_score', 'writing_score', 'pronunciation_score',
            'overall_score', 'times_practiced', 'mastered', 'mastered_at'
        ]


class LetterProgressUpdateSerializer(serializers.Serializer):
    """Serializer for updating letter progress."""
    letter_id = serializers.UUIDField()
    skill_type = serializers.ChoiceField(choices=[
        'recognition', 'listening', 'tracing', 'writing', 'pronunciation'
    ])
    score = serializers.IntegerField(min_value=0, max_value=100)
