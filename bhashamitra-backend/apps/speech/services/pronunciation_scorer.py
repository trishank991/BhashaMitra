"""
Pronunciation Scoring Service for Peppi Mimic.

V2 Enhanced Scoring with Acoustic Analysis:
- STT confidence (50%): How clearly speech was recognized
- Text matching (30%): How close transcription matches expected
- Audio energy (15%): RMS energy analysis (sufficient volume/clarity)
- Duration match (5%): Recording duration similarity to reference

Dependencies:
- soundfile: For audio file reading
- numpy: For RMS calculation
"""

import difflib
import re
import tempfile
import os
import logging
from dataclasses import dataclass
from typing import Optional, Tuple
import requests

from .feedback_service import get_pronunciation_feedback

logger = logging.getLogger(__name__)

@dataclass
class AudioAnalysisResult:
    """Result of acoustic audio analysis."""
    energy_score: float      # 0-100 based on RMS energy
    duration_ms: int         # Actual duration in milliseconds
    duration_match_score: float  # 0-100 based on duration similarity
    rms_energy: float        # Raw RMS value
    is_valid: bool           # Whether analysis was successful


@dataclass
class PronunciationResult:
    """Result of pronunciation scoring."""
    transcription: str
    expected_word: str
    stt_confidence: float       # 0-1 from STT provider
    text_match_score: float     # 0-100 from text comparison
    energy_score: float         # 0-100 from audio energy analysis
    duration_match_score: float # 0-100 from duration comparison
    final_score: float          # 0-100 combined score
    stars: int                  # 0-3 star rating
    feedback_key: str           # 'perfect', 'good', 'try_again'
    scoring_version: int        # Algorithm version (2 = hybrid)
    score_breakdown: dict       # Detailed breakdown for debugging
    
    # Move fields with default values to the bottom
    language_name: str = "Hindi"
    ai_coach_tip: str = ""      # The new MiniMax feedback field

class AudioAnalyzer:
    """
    Analyze audio files for pronunciation scoring.

    Uses RMS (Root Mean Square) energy to assess:
    - Whether the child spoke clearly and loudly enough
    - Audio quality/clarity
    - Recording duration vs expected duration
    """

    # Minimum RMS threshold for "good" audio (empirically tuned)
    MIN_RMS_THRESHOLD = 0.01
    # Optimal RMS range for children's speech
    OPTIMAL_RMS_MIN = 0.03
    OPTIMAL_RMS_MAX = 0.5

    # Duration tolerance (±30% of expected is acceptable)
    DURATION_TOLERANCE = 0.30

    @classmethod
    def analyze(
        cls,
        audio_url: str,
        expected_duration_ms: Optional[int] = None
    ) -> AudioAnalysisResult:
        """
        Analyze audio from URL for energy and duration.

        Args:
            audio_url: URL to audio file
            expected_duration_ms: Expected duration for comparison (optional)

        Returns:
            AudioAnalysisResult with scores
        """
        try:
            # Download audio
            audio_data = cls._download_audio(audio_url)
            if not audio_data:
                return cls._default_result()

            # Analyze using soundfile
            return cls._analyze_audio_data(audio_data, expected_duration_ms)

        except Exception as e:
            logger.warning(f"Audio analysis failed: {e}")
            return cls._default_result()

    @classmethod
    def _download_audio(cls, url: str, max_retries: int = 3) -> Optional[bytes]:
        """
        Get audio content from URL or local file.

        For local media URLs (containing /media/), reads directly from disk
        to avoid HTTP timeout issues when server downloads from itself.
        """
        from django.conf import settings
        import time

        # Check if this is a local media URL
        if '/media/' in url:
            try:
                # Extract relative path from URL
                # URL: https://bhashamitra.onrender.com/media/mimic_recordings/xxx/yyy.webm
                # Relative path: mimic_recordings/xxx/yyy.webm
                relative_path = url.split('/media/')[-1]
                file_path = os.path.join(settings.MEDIA_ROOT, relative_path)

                if os.path.exists(file_path):
                    logger.info(f"Reading audio from local file: {file_path}")
                    with open(file_path, 'rb') as f:
                        return f.read()
                else:
                    logger.warning(f"Local file not found: {file_path}, falling back to HTTP")
            except Exception as e:
                logger.warning(f"Failed to read local file, falling back to HTTP: {e}")

        # Fall back to HTTP download for external URLs or if local read failed
        for attempt in range(max_retries):
            try:
                response = requests.get(url, timeout=15)
                response.raise_for_status()
                return response.content
            except requests.exceptions.Timeout:
                logger.warning(f"Audio download timeout (attempt {attempt + 1}/{max_retries})")
                if attempt < max_retries - 1:
                    time.sleep(1 * (attempt + 1))  # Exponential backoff
            except requests.exceptions.RequestException as e:
                logger.warning(f"Audio download failed (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(0.5 * (attempt + 1))

        logger.error(f"Failed to download audio after {max_retries} attempts: {url}")
        return None

    @classmethod
    def _analyze_audio_data(
        cls,
        audio_data: bytes,
        expected_duration_ms: Optional[int] = None
    ) -> AudioAnalysisResult:
        """Analyze audio data using soundfile and numpy."""
        try:
            import soundfile as sf
            import numpy as np
            import io

            # Read audio from bytes
            audio_bytes_io = io.BytesIO(audio_data)

            try:
                # Try to read audio file
                samples, sample_rate = sf.read(audio_bytes_io)
            except Exception as e:
                # Try saving to temp file for format detection
                logger.debug(f"Direct read failed, trying temp file: {e}")
                with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as f:
                    f.write(audio_data)
                    temp_path = f.name

                try:
                    samples, sample_rate = sf.read(temp_path)
                finally:
                    os.unlink(temp_path)

            # Convert to mono if stereo
            if len(samples.shape) > 1:
                samples = samples.mean(axis=1)

            # Calculate RMS energy
            rms_energy = float(np.sqrt(np.mean(samples ** 2)))

            # Calculate duration
            duration_ms = int(len(samples) / sample_rate * 1000)

            # Calculate energy score (0-100)
            energy_score = cls._calculate_energy_score(rms_energy)

            # Calculate duration match score (0-100)
            duration_match_score = cls._calculate_duration_score(
                duration_ms, expected_duration_ms
            )

            logger.info(
                f"Audio analysis: RMS={rms_energy:.4f}, "
                f"duration={duration_ms}ms, energy_score={energy_score:.1f}, "
                f"duration_match={duration_match_score:.1f}"
            )

            return AudioAnalysisResult(
                energy_score=energy_score,
                duration_ms=duration_ms,
                duration_match_score=duration_match_score,
                rms_energy=rms_energy,
                is_valid=True
            )

        except ImportError as e:
            logger.error(f"Missing audio analysis dependency: {e}")
            return cls._default_result()
        except Exception as e:
            logger.warning(f"Audio analysis error: {e}")
            return cls._default_result()

    @classmethod
    def _calculate_energy_score(cls, rms: float) -> float:
        """
        Convert RMS energy to 0-100 score.

        Scoring:
        - Below MIN_RMS_THRESHOLD: 0-30 (too quiet)
        - In OPTIMAL range: 80-100 (good volume)
        - Above OPTIMAL_MAX: 60-80 (maybe too loud/clipping)
        """
        if rms < cls.MIN_RMS_THRESHOLD:
            # Too quiet - scale 0-30
            return (rms / cls.MIN_RMS_THRESHOLD) * 30

        if rms < cls.OPTIMAL_RMS_MIN:
            # Quiet but audible - scale 30-80
            ratio = (rms - cls.MIN_RMS_THRESHOLD) / (cls.OPTIMAL_RMS_MIN - cls.MIN_RMS_THRESHOLD)
            return 30 + (ratio * 50)

        if rms <= cls.OPTIMAL_RMS_MAX:
            # Optimal range - scale 80-100
            ratio = (rms - cls.OPTIMAL_RMS_MIN) / (cls.OPTIMAL_RMS_MAX - cls.OPTIMAL_RMS_MIN)
            return 80 + (ratio * 20)

        # Above optimal (possible clipping) - scale down from 80
        excess_ratio = min((rms - cls.OPTIMAL_RMS_MAX) / cls.OPTIMAL_RMS_MAX, 1.0)
        return max(60, 80 - (excess_ratio * 20))

    @classmethod
    def _calculate_duration_score(
        cls,
        actual_ms: int,
        expected_ms: Optional[int]
    ) -> float:
        """
        Calculate duration match score (0-100).

        If no expected duration, return default of 75.
        """
        if not expected_ms or expected_ms <= 0:
            return 75.0  # Default when no reference

        # Calculate ratio
        ratio = actual_ms / expected_ms

        # Perfect match = 1.0
        # Score decreases as ratio deviates from 1.0
        deviation = abs(1.0 - ratio)

        if deviation <= cls.DURATION_TOLERANCE:
            # Within tolerance - score 80-100
            normalized = 1 - (deviation / cls.DURATION_TOLERANCE)
            return 80 + (normalized * 20)

        # Outside tolerance - score decreases
        excess = deviation - cls.DURATION_TOLERANCE
        return max(0, 80 - (excess * 100))

    @classmethod
    def _default_result(cls) -> AudioAnalysisResult:
        """Return default result when analysis fails."""
        return AudioAnalysisResult(
            energy_score=50.0,  # Neutral score
            duration_ms=0,
            duration_match_score=75.0,  # Neutral score
            rms_energy=0.0,
            is_valid=False
        )


class PronunciationScorer:
    """
    Score pronunciation attempts using hybrid analysis.

    V2 Scoring Algorithm (Hybrid):
    - 50% weight: STT confidence (how clearly speech was recognized)
    - 30% weight: Text match (how close transcription matches expected)
    - 15% weight: Audio energy (clarity/volume of recording)
    - 5% weight: Duration match (recording length vs expected)
    - Bonus: +10 points for exact text match

    Star Thresholds:
    - 3 stars: 85+ score
    - 2 stars: 65-84 score
    - 1 star: 40-64 score
    - 0 stars: <40 score
    """

    # Scoring version
    SCORING_VERSION = 2

    # Weight configuration (v2 hybrid)
    WEIGHT_STT = 0.50
    WEIGHT_TEXT = 0.30
    WEIGHT_ENERGY = 0.15
    WEIGHT_DURATION = 0.05

    # Star thresholds
    THREE_STAR_THRESHOLD = 85
    TWO_STAR_THRESHOLD = 65
    ONE_STAR_THRESHOLD = 40

    # Points per star level
    POINTS_MAP = {
        3: 25,  # Perfect
        2: 15,  # Good
        1: 10,  # Try again
        0: 5,   # Participation points
    }

    # Bonus points
    PERSONAL_BEST_BONUS = 10
    EXACT_MATCH_BONUS = 10

    def score(
        self,
        transcription: str,
        expected_word: str,
        stt_confidence: float,
        language_name: str = "Hindi",
        expected_romanization: Optional[str] = None,
        audio_url: Optional[str] = None,
        expected_duration_ms: Optional[int] = None
    ) -> PronunciationResult:
        """
        Score a pronunciation attempt using hybrid analysis.

        Args:
            transcription: What the STT heard
            expected_word: The target word in native script
            stt_confidence: Confidence from STT (0-1)
            expected_romanization: Optional romanization for fallback matching
            audio_url: URL to child's recording for acoustic analysis
            expected_duration_ms: Expected duration from reference audio

        Returns:
            PronunciationResult with scores and feedback
        """
        # Clean inputs
        transcription_clean = self._normalize_text(transcription)
        expected_clean = self._normalize_text(expected_word)

        # Validate and normalize STT confidence (should be 0-1, some providers return >1)
        stt_confidence = max(0.0, min(1.0, stt_confidence))
        # Apply minimum floor for very low confidence to avoid unfair penalties
        if stt_confidence < 0.1 and transcription_clean:
            # If we got a transcription but confidence is very low, use floor of 0.3
            stt_confidence = max(stt_confidence, 0.3)
            logger.debug(f"Applied STT confidence floor: {stt_confidence}")

        # Calculate text match score
        text_match_score = self._calculate_text_match(
            transcription_clean,
            expected_clean,
            expected_romanization
        )

        # Check for exact match
        is_exact_match = (
            transcription_clean == expected_clean or
            (expected_romanization and
             transcription_clean == self._normalize_text(expected_romanization))
        )

        # Perform acoustic analysis if audio URL provided
        if audio_url:
            audio_result = AudioAnalyzer.analyze(audio_url, expected_duration_ms)
            energy_score = audio_result.energy_score
            duration_match_score = audio_result.duration_match_score
        else:
            # Fallback to neutral scores
            energy_score = 75.0
            duration_match_score = 75.0

        # Calculate weighted final score
        confidence_component = (stt_confidence * 100) * self.WEIGHT_STT
        text_component = text_match_score * self.WEIGHT_TEXT
        energy_component = energy_score * self.WEIGHT_ENERGY
        duration_component = duration_match_score * self.WEIGHT_DURATION

        final_score = (
            confidence_component +
            text_component +
            energy_component +
            duration_component
        )

        # Bonus for exact match
        if is_exact_match:
            final_score = min(final_score + self.EXACT_MATCH_BONUS, 100)

        # Determine stars and feedback
        stars, feedback_key = self._get_stars_and_feedback(final_score)

        # Get rich feedback from static feedback service (free, fast, reliable)
        rich_feedback = get_pronunciation_feedback(
            score=int(round(final_score)),
            language=language_name,
            word=expected_word,
            transcription=transcription,
        )
        ai_feedback = rich_feedback.get('tip', 'Keep practicing!')

        # Build score breakdown for transparency
        score_breakdown = {
            'stt_confidence': {
                'raw': stt_confidence,
                'weighted': round(confidence_component, 2),
                'weight': self.WEIGHT_STT
            },
            'text_match': {
                'raw': text_match_score,
                'weighted': round(text_component, 2),
                'weight': self.WEIGHT_TEXT
            },
            'energy': {
                'raw': energy_score,
                'weighted': round(energy_component, 2),
                'weight': self.WEIGHT_ENERGY
            },
            'duration': {
                'raw': duration_match_score,
                'weighted': round(duration_component, 2),
                'weight': self.WEIGHT_DURATION
            },
            'exact_match_bonus': self.EXACT_MATCH_BONUS if is_exact_match else 0,
            'is_exact_match': is_exact_match
        }

        return PronunciationResult(
            transcription=transcription,
            expected_word=expected_word,
            stt_confidence=stt_confidence,
            text_match_score=text_match_score,
            energy_score=energy_score,
            duration_match_score=duration_match_score,
            final_score=round(final_score, 1),
            stars=stars,
            feedback_key=feedback_key,
            scoring_version=self.SCORING_VERSION,
            score_breakdown=score_breakdown,
            language_name=language_name,
            ai_coach_tip=ai_feedback
        )

    def _normalize_text(self, text: str) -> str:
        """Normalize text for comparison."""
        if not text:
            return ""
        # Remove extra whitespace, convert to lowercase
        text = text.strip().lower()
        # Remove punctuation
        text = re.sub(r'[^\w\s]', '', text)
        # Normalize whitespace
        text = ' '.join(text.split())
        return text

    def _calculate_text_match(
        self,
        transcription: str,
        expected: str,
        romanization: Optional[str] = None
    ) -> float:
        """
        Calculate text match score (0-100).
        Uses sequence matching with romanization fallback.
        """
        if not transcription or not expected:
            return 0.0

        # Primary match against expected word
        primary_ratio = difflib.SequenceMatcher(
            None, transcription, expected
        ).ratio()

        # Secondary match against romanization (for accent variations)
        roman_ratio = 0.0
        if romanization:
            roman_clean = self._normalize_text(romanization)
            roman_ratio = difflib.SequenceMatcher(
                None, transcription, roman_clean
            ).ratio()

        # Use the better match
        best_ratio = max(primary_ratio, roman_ratio)

        return best_ratio * 100

    def _get_stars_and_feedback(self, score: float) -> Tuple[int, str]:
        """Determine star rating and feedback key based on score."""
        if score >= self.THREE_STAR_THRESHOLD:
            return 3, 'perfect'
        elif score >= self.TWO_STAR_THRESHOLD:
            return 2, 'good'
        elif score >= self.ONE_STAR_THRESHOLD:
            return 1, 'try_again'
        else:
            return 0, 'try_again'

    def get_points(self, stars: int, is_personal_best: bool = False) -> int:
        """
        Calculate points earned for an attempt.

        Args:
            stars: Star rating (0-3)
            is_personal_best: Whether this is a new high score

        Returns:
            Points earned
        """
        base_points = self.POINTS_MAP.get(stars, 5)

        if is_personal_best:
            base_points += self.PERSONAL_BEST_BONUS

        return base_points

    def get_peppi_feedback(
        self,
        challenge,
        feedback_key: str,
        child_name: Optional[str] = None
    ) -> str:
        """
        Get Peppi's feedback message based on performance.

        Args:
            challenge: PeppiMimicChallenge instance
            feedback_key: 'perfect', 'good', or 'try_again'
            child_name: Optional child name for personalization

        Returns:
            Peppi's feedback message
        """
        # Default messages with cat-themed words
        default_messages = {
            'perfect': "MEOW! That was PURRRFECT! You're a paw-some language star! Nani ko zaroor sunao!",
            'good': "Meow meow! Almost purrrfect! You're doing great, let's try one meow time?",
            'try_again': "Meow! Good try little cub! Let's try one more time - listen and repeat after me!",
        }

        # Try to get custom message from challenge
        message = ""
        if feedback_key == 'perfect' and challenge.peppi_perfect:
            message = challenge.peppi_perfect
        elif feedback_key == 'good' and challenge.peppi_good:
            message = challenge.peppi_good
        elif challenge.peppi_try_again:
            message = challenge.peppi_try_again
        else:
            message = default_messages.get(feedback_key, default_messages['try_again'])

        # Personalize with child name if available
        if child_name and '{name}' in message:
            message = message.replace('{name}', child_name)

        return message

    def generate_share_message(
        self,
        child_name: str,
        word: str,
        romanization: str,
        language: str,
        stars: int,
        score: float
    ) -> str:
        """
        Generate a message for sharing achievements via WhatsApp.

        Args:
            child_name: Name of the child
            word: The word in native script
            romanization: The transliteration
            language: Language name
            stars: Star rating achieved
            score: Final score percentage

        Returns:
            Formatted share message
        """
        star_emojis = "⭐" * stars if stars > 0 else "💪"

        if stars == 3:
            achievement = "got a PERFECT score"
        elif stars == 2:
            achievement = "did great"
        else:
            achievement = "is practicing hard"

        return (
            f"🎉 {child_name} {achievement}!\n\n"
            f"Word: {word} ({romanization})\n"
            f"Score: {star_emojis} {score:.0f}%\n\n"
            f"Learning {language.title()} on BhashaMitra! 📚🐱\n\n"
            f"Send them an encouraging voice message! 💕"
        )


# Singleton instance for easy access
pronunciation_scorer = PronunciationScorer()