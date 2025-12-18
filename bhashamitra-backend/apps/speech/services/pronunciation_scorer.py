"""
Pronunciation Scoring Service for Peppi Mimic.
Combines STT confidence with text matching to score pronunciation attempts.
"""

import difflib
import re
from dataclasses import dataclass
from typing import Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class PronunciationResult:
    """Result of pronunciation scoring."""
    transcription: str
    expected_word: str
    stt_confidence: float  # 0-1 from STT provider
    text_match_score: float  # 0-100 from text comparison
    final_score: float  # 0-100 combined score
    stars: int  # 0-3 star rating
    feedback_key: str  # 'perfect', 'good', 'try_again'


class PronunciationScorer:
    """
    Score pronunciation attempts using STT confidence and text matching.

    Scoring Algorithm:
    - 60% weight: STT confidence (how clearly the speech was recognized)
    - 40% weight: Text match (how close transcription matches expected word)
    - Bonus: +10 points for exact match

    Star Thresholds:
    - 3 stars: 85+ score
    - 2 stars: 65-84 score
    - 1 star: 40-64 score
    - 0 stars: <40 score
    """

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
        expected_romanization: Optional[str] = None
    ) -> PronunciationResult:
        """
        Score a pronunciation attempt.

        Args:
            transcription: What the STT heard
            expected_word: The target word in native script
            stt_confidence: Confidence from STT (0-1)
            expected_romanization: Optional romanization for fallback matching

        Returns:
            PronunciationResult with scores and feedback
        """
        # Clean inputs
        transcription_clean = self._normalize_text(transcription)
        expected_clean = self._normalize_text(expected_word)

        # Calculate text match score using sequence matching
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

        # Calculate final score
        # 60% from STT confidence, 40% from text match
        confidence_component = stt_confidence * 60
        match_component = (text_match_score / 100) * 40

        final_score = confidence_component + match_component

        # Bonus for exact match
        if is_exact_match:
            final_score = min(final_score + self.EXACT_MATCH_BONUS, 100)

        # Determine stars and feedback
        stars, feedback_key = self._get_stars_and_feedback(final_score)

        return PronunciationResult(
            transcription=transcription,
            expected_word=expected_word,
            stt_confidence=stt_confidence,
            text_match_score=text_match_score,
            final_score=round(final_score, 1),
            stars=stars,
            feedback_key=feedback_key
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

    def _get_stars_and_feedback(self, score: float) -> tuple[int, str]:
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
        # Default messages if challenge doesn't have custom ones
        default_messages = {
            'perfect': "WOOOW! 🌟 PERFECT! Tum toh superstar ho! Nani ko zaroor sunao!",
            'good': "Bahut accha! 👏 Almost perfect! Ek baar aur try karo?",
            'try_again': "Good try! 🤗 Mere saath bolo - sunoge phir try karo!",
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

        message = (
            f"🎉 {child_name} {achievement}!\n\n"
            f"Word: {word} ({romanization})\n"
            f"Score: {star_emojis} {score:.0f}%\n\n"
            f"Learning {language.title()} on BhashaMitra! 📚🐱\n\n"
            f"Send them an encouraging voice message! 💕"
        )

        return message


# Singleton instance for easy access
pronunciation_scorer = PronunciationScorer()
