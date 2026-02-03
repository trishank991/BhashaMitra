"""
Rich Static Feedback System for Pronunciation Coaching.

This module provides encouraging, age-appropriate feedback for children
learning heritage languages. It's designed to be:
- Free (no API costs)
- Fast (no network calls)
- Reliable (no external dependencies)
- Kid-friendly (ages 4-14)
- Culturally appropriate

Future enhancement: Add LLM API for personalized feedback when budget allows.
"""

import random
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class ScoreLevel(Enum):
    """Score level categories."""
    PERFECT = "perfect"      # 95-100
    EXCELLENT = "excellent"  # 85-94
    GREAT = "great"          # 70-84
    GOOD = "good"            # 50-69
    FAIR = "fair"            # 30-49
    NEEDS_PRACTICE = "needs_practice"  # 0-29


@dataclass
class FeedbackResponse:
    """Structured feedback response."""
    score_level: str
    emoji: str
    title: str
    message: str
    tip: str
    encouragement: str
    stars: int  # 0-5 stars for visual display
    celebration: Optional[str] = None  # Special celebration for perfect scores


class FeedbackService:
    """
    Provides rich, varied feedback for pronunciation attempts.

    Design principles:
    1. Always positive and encouraging
    2. Never discouraging or critical
    3. Age-appropriate language
    4. Actionable tips when score is lower
    5. Celebrations for high scores
    6. Language-specific guidance
    """

    # ===========================================
    # GENERAL FEEDBACK MESSAGES
    # ===========================================

    FEEDBACK_MESSAGES = {
        ScoreLevel.PERFECT: {
            "titles": [
                "Perfect!",
                "Amazing!",
                "Superstar!",
                "Incredible!",
                "Wow!",
            ],
            "messages": [
                "You sound just like a native speaker!",
                "That was absolutely perfect!",
                "You nailed it completely!",
                "Couldn't be any better!",
                "You're a pronunciation champion!",
            ],
            "encouragements": [
                "Your family will be so proud!",
                "Keep shining bright!",
                "You're becoming a language expert!",
                "That practice is really paying off!",
                "You make learning look easy!",
            ],
            "celebrations": [
                "Time to celebrate!",
                "You're a superstar!",
                "Fantastic achievement!",
                "Pronunciation royalty!",
                "Gold medal performance!",
            ],
            "emoji": "🌟",
            "stars": 5,
        },

        ScoreLevel.EXCELLENT: {
            "titles": [
                "Excellent!",
                "Brilliant!",
                "Fantastic!",
                "Wonderful!",
                "Outstanding!",
            ],
            "messages": [
                "Almost perfect pronunciation!",
                "That was really impressive!",
                "You're so close to perfect!",
                "Beautiful pronunciation!",
                "That sounded wonderful!",
            ],
            "encouragements": [
                "Just a tiny bit more practice!",
                "You're doing incredibly well!",
                "Your hard work shows!",
                "Almost there - keep going!",
                "So close to perfection!",
            ],
            "emoji": "⭐",
            "stars": 4,
        },

        ScoreLevel.GREAT: {
            "titles": [
                "Great job!",
                "Well done!",
                "Nice work!",
                "Good going!",
                "Super!",
            ],
            "messages": [
                "That was really good!",
                "You're getting better and better!",
                "Nice pronunciation!",
                "You're making great progress!",
                "That sounded good!",
            ],
            "encouragements": [
                "Keep practicing, you're improving!",
                "A little more practice will make it perfect!",
                "You're on the right track!",
                "Every try makes you stronger!",
                "Your dedication is showing!",
            ],
            "emoji": "👍",
            "stars": 3,
        },

        ScoreLevel.GOOD: {
            "titles": [
                "Good try!",
                "Nice effort!",
                "Keep going!",
                "You're learning!",
                "Making progress!",
            ],
            "messages": [
                "You're getting the hang of it!",
                "Good effort - keep practicing!",
                "You're learning well!",
                "That's a solid start!",
                "You're improving!",
            ],
            "encouragements": [
                "Listen again and try once more!",
                "Practice makes perfect!",
                "You've got this!",
                "Every expert was once a beginner!",
                "Keep trying - you're doing great!",
            ],
            "emoji": "💫",
            "stars": 2,
        },

        ScoreLevel.FAIR: {
            "titles": [
                "Good start!",
                "Keep trying!",
                "You can do it!",
                "Let's practice!",
                "Almost there!",
            ],
            "messages": [
                "Let's try that again together!",
                "You're learning something new!",
                "This word is tricky - let's practice!",
                "Good effort on a challenging word!",
                "You're brave for trying!",
            ],
            "encouragements": [
                "Listen carefully and try again!",
                "Slow down and say each sound!",
                "You'll get it with more practice!",
                "Don't give up - you're learning!",
                "Every try is a step forward!",
            ],
            "emoji": "💪",
            "stars": 1,
        },

        ScoreLevel.NEEDS_PRACTICE: {
            "titles": [
                "Let's try again!",
                "Practice time!",
                "Learning moment!",
                "New challenge!",
                "Let's listen!",
            ],
            "messages": [
                "This is a new sound for you!",
                "Let's listen to the word again!",
                "New words take time to learn!",
                "This one needs some practice!",
                "Let's break it down together!",
            ],
            "encouragements": [
                "Listen to the word 3 times, then try again!",
                "Say it slowly, sound by sound!",
                "Ask a family member to help you!",
                "Every expert started here!",
                "You're being brave by learning!",
            ],
            "emoji": "🎧",
            "stars": 1,
        },
    }

    # ===========================================
    # LANGUAGE-SPECIFIC PRONUNCIATION TIPS
    # ===========================================

    LANGUAGE_TIPS = {
        "HINDI": {
            "general": [
                "Hindi has many sounds that are made at the back of your mouth.",
                "Pay attention to whether letters are 'heavy' or 'light'.",
                "The 'a' in Hindi is shorter than in English.",
                "Try to pronounce each letter clearly.",
            ],
            "consonants": [
                "Hindi has special sounds like 'ड़' and 'ढ़' - curl your tongue back!",
                "The difference between 'क' and 'ख' is the breath - 'ख' has more air.",
                "'च' is softer than English 'ch' - keep your tongue behind your teeth.",
                "For 'ट', 'ठ', 'ड', 'ढ' - touch your tongue to the roof of your mouth.",
            ],
            "vowels": [
                "Hindi 'इ' is shorter than English 'ee'.",
                "'औ' sounds like 'ow' in 'cow'.",
                "'ऐ' is between 'a' and 'e' sounds.",
                "The 'अ' sound is like 'u' in 'but', not 'a' in 'cat'.",
            ],
            "common_mistakes": [
                "Don't add extra sounds at the end of words.",
                "Keep the 'schwa' sound short - don't stretch it.",
                "Watch out for aspirated vs non-aspirated sounds.",
            ],
        },

        "TAMIL": {
            "general": [
                "Tamil has unique sounds not found in other languages!",
                "The 'zh' sound (ழ) is special to Tamil - practice it!",
                "Tamil words often end in vowel sounds.",
                "Pay attention to short vs long vowels.",
            ],
            "consonants": [
                "The 'ற' sound is made by tapping your tongue quickly.",
                "'ண', 'ன', 'ந' are three different 'n' sounds!",
                "'ள' and 'ல' are different 'l' sounds - notice the difference.",
                "The unique 'ழ' doesn't exist in Hindi or English!",
            ],
            "vowels": [
                "Tamil has short and long versions of each vowel.",
                "'ஐ' sounds like 'eye'.",
                "'ஔ' sounds like 'ow' in 'how'.",
                "Pay attention to 'அ' vs 'ஆ' - short vs long.",
            ],
            "common_mistakes": [
                "Don't mix up 'ல' and 'ள' - they sound different!",
                "Watch the difference between 'ன' and 'ண'.",
                "Tamil 'r' is softer than Hindi 'r'.",
            ],
        },

        "GUJARATI": {
            "general": [
                "Gujarati has a musical quality - notice the rhythm!",
                "Many Gujarati words end softly.",
                "The language has a gentle, flowing sound.",
                "Pay attention to where the stress falls in words.",
            ],
            "consonants": [
                "Gujarati 'ળ' is a special retroflex 'l' sound.",
                "'ક' and 'ખ' differ by breath, like Hindi.",
                "'જ' is softer than English 'j'.",
                "'શ' and 'ષ' are slightly different 's' sounds.",
            ],
            "vowels": [
                "Gujarati doesn't use the 'schwa' as much as Hindi.",
                "Final vowels are often dropped in speech.",
                "'ઐ' and 'ઔ' are diphthongs - two sounds together.",
                "Pay attention to nasalized vowels.",
            ],
            "common_mistakes": [
                "Don't add Hindi-style endings to Gujarati words.",
                "The rhythm is different from Hindi - listen carefully.",
                "Some consonants sound softer than in Hindi.",
            ],
        },

        "PUNJABI": {
            "general": [
                "Punjabi has a strong, energetic sound!",
                "Tones are important in Punjabi - high, low, and level.",
                "Many words have a musical quality.",
                "Pay attention to the 'bounce' in the language.",
            ],
            "consonants": [
                "Punjabi has tonal consonants that change word meaning!",
                "'ਘ', 'ਝ', 'ਢ', 'ਭ' affect the tone of the word.",
                "'ੜ' is a special Punjabi sound - roll it!",
                "Doubled consonants should be held longer.",
            ],
            "vowels": [
                "Nasal vowels are shown with 'tippi' and 'bindi'.",
                "The 'ਾ' makes the vowel long.",
                "'ੈ' sounds like 'ai' in 'rain'.",
                "'ੌ' sounds like 'au' in 'caught'.",
            ],
            "common_mistakes": [
                "Don't ignore the tones - they change meaning!",
                "Punjabi 'v' is softer than English 'v'.",
                "The energy and rhythm are different from Hindi.",
            ],
        },

        "TELUGU": {
            "general": [
                "Telugu is known for its sweet, melodic sound!",
                "Words often end in vowels, giving it a flowing quality.",
                "Pay attention to doubled consonants.",
                "Telugu has more vowels than Hindi!",
            ],
            "consonants": [
                "Telugu 'ళ' and 'ఱ' are special sounds.",
                "Doubled consonants are pronounced clearly.",
                "'చ' is softer than English 'ch'.",
                "'ట' group sounds are retroflex - curl your tongue!",
            ],
            "vowels": [
                "Telugu has short and long versions of vowels.",
                "Most Telugu words end in vowels.",
                "'ఐ' and 'ఔ' are diphthongs.",
                "The 'అ' sound is shorter than you might think.",
            ],
            "common_mistakes": [
                "Don't skip the final vowels!",
                "Watch the gemination (doubled consonants).",
                "Telugu rhythm is different from Hindi.",
            ],
        },

        "MALAYALAM": {
            "general": [
                "Malayalam has a rich, flowing sound!",
                "It has more consonants than most Indian languages.",
                "Pay attention to the unique 'zh' sound.",
                "Words can be quite long - take your time!",
            ],
            "consonants": [
                "Malayalam has special consonants like 'ഴ' and 'റ'.",
                "'ള' and 'ല' are different 'l' sounds.",
                "'ണ' and 'ന' are different 'n' sounds.",
                "Chillu letters are half-consonants.",
            ],
            "vowels": [
                "Malayalam preserves ancient vowels carefully.",
                "Short and long vowels change meaning.",
                "'ഐ' and 'ഔ' are pronounced fully.",
                "Pay attention to vowel length.",
            ],
            "common_mistakes": [
                "Don't confuse 'ള' with 'ല'.",
                "The 'zh' sound needs practice.",
                "Malayalam 'r' sounds are distinct from Hindi.",
            ],
        },

        "BENGALI": {
            "general": [
                "Bengali has a soft, lyrical quality!",
                "Many consonants sound softer than Hindi.",
                "Pay attention to the unique vowel sounds.",
                "Bengali has a distinctive rhythm.",
            ],
            "consonants": [
                "Bengali 'জ' can sound like 'j' or 'z' depending on position.",
                "'শ', 'ষ', 'স' are all slightly different!",
                "Aspirated sounds are important in Bengali.",
                "'ড়' and 'ঢ়' are flapped sounds.",
            ],
            "vowels": [
                "Bengali 'অ' often sounds like 'o'.",
                "'এ' can be 'e' or 'ae' depending on context.",
                "Inherent vowels aren't always pronounced.",
                "'ও' and 'ঔ' are distinct sounds.",
            ],
            "common_mistakes": [
                "Don't pronounce 'অ' like Hindi 'अ' - it's more like 'o'.",
                "Bengali soft consonants need practice.",
                "The rhythm differs from Hindi - listen carefully.",
            ],
        },
    }

    # ===========================================
    # SCORE-SPECIFIC TIPS
    # ===========================================

    SCORE_TIPS = {
        ScoreLevel.PERFECT: [
            "You've mastered this word! Try the next challenge!",
            "Perfect! Can you teach this word to someone?",
            "Amazing! Try saying it faster now!",
            "Wonderful! You're ready for harder words!",
        ],
        ScoreLevel.EXCELLENT: [
            "Listen one more time and match the small details!",
            "You're so close! Pay attention to the ending sound.",
            "Try saying it just a tiny bit slower.",
            "Focus on the middle of the word.",
        ],
        ScoreLevel.GREAT: [
            "Listen to how the word starts - try to match it!",
            "Break the word into parts and practice each one.",
            "Try recording yourself and listening back!",
            "Say each sound clearly before putting them together.",
        ],
        ScoreLevel.GOOD: [
            "Listen to the word 3 times before trying again.",
            "Focus on one part of the word at a time.",
            "Ask someone to say it with you!",
            "Try saying it slowly first, then faster.",
        ],
        ScoreLevel.FAIR: [
            "Let's break this word into smaller sounds!",
            "Listen very carefully to the first sound.",
            "Try humming the rhythm of the word first.",
            "Point to each letter as you hear the sound.",
        ],
        ScoreLevel.NEEDS_PRACTICE: [
            "This is a tricky word! Listen 5 times first.",
            "Ask a family member to say it with you.",
            "Try just the first part of the word.",
            "It's okay - new sounds take time to learn!",
        ],
    }

    # ===========================================
    # STREAK AND MOTIVATION MESSAGES
    # ===========================================

    STREAK_MESSAGES = {
        2: "Two in a row!",
        3: "Three perfect! You're on fire!",
        5: "Five streak! Amazing!",
        10: "TEN in a row! You're unstoppable!",
    }

    FIRST_TRY_BONUS = [
        "Perfect on your first try! Bonus points!",
        "Got it in one! You're a natural!",
        "First try success! Incredible!",
    ]

    # ===========================================
    # MAIN METHODS
    # ===========================================

    def __init__(self):
        """Initialize the feedback service."""
        self._last_messages = {}  # Track last messages to avoid repetition

    def get_score_level(self, score: int) -> ScoreLevel:
        """Determine the score level category."""
        if score >= 95:
            return ScoreLevel.PERFECT
        elif score >= 85:
            return ScoreLevel.EXCELLENT
        elif score >= 70:
            return ScoreLevel.GREAT
        elif score >= 50:
            return ScoreLevel.GOOD
        elif score >= 30:
            return ScoreLevel.FAIR
        else:
            return ScoreLevel.NEEDS_PRACTICE

    def get_feedback(
        self,
        score: int,
        language: str,
        word: str,
        transcription: str,
        attempt_number: int = 1,
        streak: int = 0,
        child_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate comprehensive feedback for a pronunciation attempt.

        Args:
            score: Pronunciation score (0-100)
            language: Language code (e.g., 'HINDI', 'TAMIL')
            word: The expected word
            transcription: What was actually recognized
            attempt_number: Which attempt this is (1, 2, 3...)
            streak: Current streak of correct answers
            child_name: Optional child's name for personalization

        Returns:
            Comprehensive feedback dictionary
        """
        level = self.get_score_level(score)
        feedback_data = self.FEEDBACK_MESSAGES[level]

        # Get random messages (avoiding recent ones)
        title = self._get_varied_message(feedback_data["titles"], f"{level}_title")
        message = self._get_varied_message(feedback_data["messages"], f"{level}_message")
        encouragement = self._get_varied_message(feedback_data["encouragements"], f"{level}_encouragement")

        # Get score-specific tip
        tip = self._get_varied_message(self.SCORE_TIPS[level], f"{level}_tip")

        # Get language-specific tip for lower scores
        language_tip = None
        if score < 85 and language in self.LANGUAGE_TIPS:
            lang_tips = self.LANGUAGE_TIPS[language]
            all_lang_tips = (
                lang_tips.get("general", []) +
                lang_tips.get("consonants", []) +
                lang_tips.get("vowels", [])
            )
            if all_lang_tips:
                language_tip = random.choice(all_lang_tips)

        # Build response
        response = {
            "score": score,
            "score_level": level.value,
            "stars": feedback_data["stars"],
            "emoji": feedback_data["emoji"],
            "title": title,
            "message": message,
            "tip": tip,
            "encouragement": encouragement,
            "language_tip": language_tip,
            "is_correct": score >= 70,
            "word": word,
            "heard": transcription,
        }

        # Add celebration for perfect scores
        if level == ScoreLevel.PERFECT and "celebrations" in feedback_data:
            response["celebration"] = random.choice(feedback_data["celebrations"])

        # Add streak message if applicable
        if streak > 1 and streak in self.STREAK_MESSAGES:
            response["streak_message"] = self.STREAK_MESSAGES[streak]
        elif streak > 10:
            response["streak_message"] = f"{streak} streak! Legendary!"

        # Add first try bonus message
        if attempt_number == 1 and score >= 90:
            response["first_try_bonus"] = random.choice(self.FIRST_TRY_BONUS)

        # Personalize if name provided
        if child_name and score >= 85:
            response["personalized"] = f"Great job, {child_name}! "

        # Add improvement suggestion for retries
        if attempt_number > 1:
            if score > 70:
                response["improvement_note"] = "You're improving! Keep it up!"
            elif attempt_number >= 3:
                response["improvement_note"] = "Don't worry - this word is challenging. Try a different word and come back later!"

        return response

    def get_simple_feedback(self, score: int, language: str) -> Dict[str, str]:
        """
        Get simplified feedback (for API responses).

        Returns minimal feedback suitable for JSON responses.
        """
        level = self.get_score_level(score)
        feedback_data = self.FEEDBACK_MESSAGES[level]

        return {
            "level": level.value,
            "emoji": feedback_data["emoji"],
            "message": random.choice(feedback_data["messages"]),
            "tip": random.choice(self.SCORE_TIPS[level]),
            "stars": feedback_data["stars"],
        }

    def _get_varied_message(self, messages: list, category: str) -> str:
        """Get a message, avoiding the last one used in this category."""
        if len(messages) <= 1:
            return messages[0] if messages else ""

        last_used = self._last_messages.get(category)
        available = [m for m in messages if m != last_used]

        if not available:
            available = messages

        chosen = random.choice(available)
        self._last_messages[category] = chosen

        return chosen

    def get_language_tips(self, language: str, category: str = "general") -> list:
        """Get all tips for a language and category."""
        if language not in self.LANGUAGE_TIPS:
            return []
        return self.LANGUAGE_TIPS[language].get(category, [])

    def get_common_mistakes(self, language: str) -> list:
        """Get common mistakes for a language."""
        if language not in self.LANGUAGE_TIPS:
            return []
        return self.LANGUAGE_TIPS[language].get("common_mistakes", [])


# ===========================================
# SINGLETON INSTANCE
# ===========================================

_feedback_service = None


def get_feedback_service() -> FeedbackService:
    """Get or create the feedback service singleton."""
    global _feedback_service
    if _feedback_service is None:
        _feedback_service = FeedbackService()
    return _feedback_service


# ===========================================
# CONVENIENCE FUNCTION
# ===========================================

def get_pronunciation_feedback(
    score: int,
    language: str,
    word: str = "",
    transcription: str = "",
    **kwargs
) -> Dict[str, Any]:
    """
    Convenience function to get pronunciation feedback.

    Usage:
        feedback = get_pronunciation_feedback(
            score=85,
            language="HINDI",
            word="कुत्ता",
            transcription="कुत्ता"
        )
    """
    service = get_feedback_service()
    return service.get_feedback(
        score=score,
        language=language,
        word=word,
        transcription=transcription,
        **kwargs
    )
