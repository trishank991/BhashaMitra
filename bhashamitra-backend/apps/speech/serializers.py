"""Speech serializers."""
from rest_framework import serializers


class TTSRequestSerializer(serializers.Serializer):
    """Text-to-speech request serializer."""
    text = serializers.CharField(max_length=5000)
    language = serializers.CharField(max_length=20, default='HINDI')
    voice = serializers.CharField(max_length=20, default='female')
    speed = serializers.FloatField(min_value=0.5, max_value=2.0, default=1.0)


class TTSResponseSerializer(serializers.Serializer):
    """Text-to-speech response serializer."""
    audio_url = serializers.URLField()
    audio_base64 = serializers.CharField(required=False)
    duration_seconds = serializers.FloatField()
    cached = serializers.BooleanField()


class STTRequestSerializer(serializers.Serializer):
    """Speech-to-text request serializer."""
    audio_url = serializers.URLField(required=False)
    audio_base64 = serializers.CharField(required=False)
    language = serializers.CharField(max_length=20, default='HINDI')
    expected_text = serializers.CharField(required=False, max_length=5000)

    def validate(self, attrs):
        if not attrs.get('audio_url') and not attrs.get('audio_base64'):
            raise serializers.ValidationError(
                "Either audio_url or audio_base64 must be provided"
            )
        return attrs


class STTResponseSerializer(serializers.Serializer):
    """Speech-to-text response serializer."""
    transcription = serializers.CharField()
    confidence = serializers.FloatField()


class PronunciationCheckSerializer(serializers.Serializer):
    """Pronunciation check response serializer."""
    transcription = serializers.CharField()
    expected_text = serializers.CharField()
    accuracy_score = serializers.FloatField()
    feedback = serializers.CharField()
    word_scores = serializers.ListField(child=serializers.DictField())
