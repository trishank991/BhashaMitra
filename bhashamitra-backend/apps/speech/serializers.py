"""Speech serializers."""
from rest_framework import serializers
from apps.speech.models import PeppiMimicChallenge, PeppiMimicAttempt, PeppiMimicProgress


# ========================================
# TTS/STT Serializers
# ========================================

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


# ========================================
# Peppi Mimic Serializers
# ========================================

class MimicChallengeListSerializer(serializers.ModelSerializer):
    """Serializer for listing mimic challenges."""
    best_stars = serializers.SerializerMethodField()
    mastered = serializers.SerializerMethodField()
    attempts = serializers.SerializerMethodField()

    class Meta:
        model = PeppiMimicChallenge
        fields = [
            'id', 'word', 'romanization', 'meaning', 'language',
            'category', 'difficulty', 'points_reward', 'audio_url',
            'best_stars', 'mastered', 'attempts'
        ]

    def get_best_stars(self, obj):
        """Get child's best star rating for this challenge."""
        progress = self._get_progress(obj)
        return progress.best_stars if progress else 0

    def get_mastered(self, obj):
        """Check if child has mastered this challenge."""
        progress = self._get_progress(obj)
        return progress.mastered if progress else False

    def get_attempts(self, obj):
        """Get child's total attempts for this challenge."""
        progress = self._get_progress(obj)
        return progress.total_attempts if progress else 0

    def _get_progress(self, obj):
        """Helper to get progress from context."""
        progress_map = self.context.get('progress_map', {})
        return progress_map.get(str(obj.id))


class MimicChallengeDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for a single challenge with Peppi scripts."""
    progress = serializers.SerializerMethodField()

    class Meta:
        model = PeppiMimicChallenge
        fields = [
            'id', 'word', 'romanization', 'meaning', 'language',
            'category', 'difficulty', 'points_reward', 'audio_url',
            'peppi_intro', 'peppi_perfect', 'peppi_good', 'peppi_try_again',
            'progress'
        ]

    def get_progress(self, obj):
        """Get child's progress on this challenge."""
        child = self.context.get('child')
        if not child:
            return None

        try:
            progress = PeppiMimicProgress.objects.get(child=child, challenge=obj)
            return {
                'best_score': progress.best_score,
                'best_stars': progress.best_stars,
                'total_attempts': progress.total_attempts,
                'mastered': progress.mastered,
                'mastered_at': progress.mastered_at,
            }
        except PeppiMimicProgress.DoesNotExist:
            return {
                'best_score': 0,
                'best_stars': 0,
                'total_attempts': 0,
                'mastered': False,
                'mastered_at': None,
            }


class MimicAttemptSerializer(serializers.ModelSerializer):
    """Serializer for mimic attempts."""
    challenge_word = serializers.CharField(source='challenge.word', read_only=True)

    class Meta:
        model = PeppiMimicAttempt
        fields = [
            'id', 'challenge', 'challenge_word', 'audio_url', 'duration_ms',
            'stt_transcription', 'stt_confidence', 'text_match_score',
            # V2 acoustic analysis fields
            'audio_energy_score', 'duration_match_score', 'scoring_version',
            'final_score', 'stars', 'points_earned', 'is_personal_best',
            'shared_to_family', 'shared_at', 'created_at'
        ]
        read_only_fields = [
            'id', 'stt_transcription', 'stt_confidence', 'text_match_score',
            'audio_energy_score', 'duration_match_score', 'scoring_version',
            'final_score', 'stars', 'points_earned', 'is_personal_best',
            'shared_at', 'created_at'
        ]


class MimicAttemptSubmitSerializer(serializers.Serializer):
    """Serializer for submitting a mimic attempt."""
    audio_url = serializers.URLField(help_text="URL to child's audio recording")
    duration_ms = serializers.IntegerField(
        min_value=100,
        max_value=10000,
        default=3000,
        help_text="Recording duration in milliseconds"
    )


class MimicAttemptResultSerializer(serializers.Serializer):
    """Serializer for mimic attempt result."""
    attempt_id = serializers.UUIDField()
    transcription = serializers.CharField()
    score = serializers.FloatField()
    stars = serializers.IntegerField()
    points_earned = serializers.IntegerField()
    is_personal_best = serializers.BooleanField()
    mastered = serializers.BooleanField()
    peppi_feedback = serializers.CharField()
    share_message = serializers.CharField()
    progress = serializers.DictField()
    # V2: Detailed scoring breakdown
    score_breakdown = serializers.DictField(required=False)
    scoring_version = serializers.IntegerField(required=False)


class MimicProgressSerializer(serializers.ModelSerializer):
    """Serializer for mimic progress."""
    challenge_word = serializers.CharField(source='challenge.word', read_only=True)
    challenge_romanization = serializers.CharField(source='challenge.romanization', read_only=True)
    challenge_category = serializers.CharField(source='challenge.category', read_only=True)

    class Meta:
        model = PeppiMimicProgress
        fields = [
            'id', 'challenge', 'challenge_word', 'challenge_romanization',
            'challenge_category', 'best_score', 'best_stars', 'total_attempts',
            'total_points', 'mastered', 'mastered_at', 'created_at', 'updated_at'
        ]


class MimicProgressSummarySerializer(serializers.Serializer):
    """Serializer for overall mimic progress summary."""
    total_challenges = serializers.IntegerField()
    challenges_attempted = serializers.IntegerField()
    challenges_mastered = serializers.IntegerField()
    total_attempts = serializers.IntegerField()
    total_points = serializers.IntegerField()
    average_score = serializers.FloatField()
    current_streak = serializers.IntegerField()
    categories = serializers.ListField(child=serializers.DictField())


class MimicShareSerializer(serializers.Serializer):
    """Serializer for sharing a mimic attempt."""
    shared_to_family = serializers.BooleanField(default=True)
