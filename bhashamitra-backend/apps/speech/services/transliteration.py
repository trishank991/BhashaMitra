"""
Transliteration service for Indian languages to Roman/Hinglish.

Provides:
- Hindi to Roman transliteration (Hinglish)
- Tamil to Roman transliteration
- Gujarati to Roman transliteration
- Other Indian language support
"""

import re
import unicodedata
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)


# ============================================
# TRANSLITERATION MAPPINGS
# ============================================

# Hindi to Roman/Hinglish transliteration map
HINDI_TO_ROMAN: Dict[str, str] = {
    # Vowels
    '\u0905': 'a', '\u0906': 'aa', '\u0907': 'i', '\u0908': 'ee', '\u0909': 'u', '\u090a': 'oo',
    '\u090f': 'e', '\u0910': 'ai', '\u0913': 'o', '\u0914': 'au', '\u0905\u0902': 'an', '\u0905\u0903': 'ah',

    # Consonants
    '\u0915': 'ka', '\u0916': 'kha', '\u0917': 'ga', '\u0918': 'gha', '\u0919': 'nga',
    '\u091a': 'cha', '\u091b': 'chha', '\u091c': 'ja', '\u091d': 'jha', '\u091e': 'nya',
    '\u091f': 'ta', '\u0920': 'tha', '\u0921': 'da', '\u0922': 'dha', '\u0923': 'na',
    '\u0924': 'ta', '\u0925': 'tha', '\u0926': 'da', '\u0927': 'dha', '\u0928': 'na',
    '\u092a': 'pa', '\u092b': 'pha', '\u092c': 'ba', '\u092d': 'bha', '\u092e': 'ma',
    '\u092f': 'ya', '\u0930': 'ra', '\u0932': 'la', '\u0935': 'va', '\u0936': 'sha',
    '\u0937': 'sha', '\u0938': 'sa', '\u0939': 'ha',

    # Special consonants
    '\u0915\u094d\u0937': 'ksha', '\u0924\u094d\u0930': 'tra', '\u091c\u094d\u091e': 'gya', '\u0936\u094d\u0930': 'shra',

    # Matras (vowel signs)
    '\u093e': 'aa', '\u093f': 'i', '\u0940': 'ee', '\u0941': 'u', '\u0942': 'oo',
    '\u0947': 'e', '\u0948': 'ai', '\u094b': 'o', '\u094c': 'au',
    '\u0902': 'n', '\u0903': 'h', '\u094d': '',  # Halant removes inherent vowel

    # Nukta consonants
    '\u0958': 'qa', '\u0959': 'kha', '\u095a': 'gha', '\u095b': 'za',
    '\u095c': 'da', '\u095d': 'dha', '\u095e': 'fa',

    # Numbers
    '\u0966': '0', '\u0967': '1', '\u0968': '2', '\u0969': '3', '\u096a': '4',
    '\u096b': '5', '\u096c': '6', '\u096d': '7', '\u096e': '8', '\u096f': '9',

    # Punctuation
    '\u0964': '.', '\u0965': '.',
}

# Tamil to Roman transliteration (basic)
TAMIL_TO_ROMAN: Dict[str, str] = {
    '\u0b85': 'a', '\u0b86': 'aa', '\u0b87': 'i', '\u0b88': 'ee', '\u0b89': 'u', '\u0b8a': 'oo',
    '\u0b8e': 'e', '\u0b8f': 'ae', '\u0b90': 'ai', '\u0b92': 'o', '\u0b93': 'oo', '\u0b94': 'au',
    '\u0b95': 'ka', '\u0b99': 'nga', '\u0b9a': 'sa', '\u0b9e': 'nya', '\u0b9f': 'ta', '\u0ba3': 'na',
    '\u0ba4': 'tha', '\u0ba8': 'na', '\u0baa': 'pa', '\u0bae': 'ma', '\u0baf': 'ya', '\u0bb0': 'ra',
    '\u0bb2': 'la', '\u0bb5': 'va', '\u0bb4': 'zha', '\u0bb3': 'la', '\u0bb1': 'ra', '\u0ba9': 'na',
    # Matras
    '\u0bbe': 'aa', '\u0bbf': 'i', '\u0bc0': 'ee', '\u0bc1': 'u', '\u0bc2': 'oo',
    '\u0bc6': 'e', '\u0bc7': 'ae', '\u0bc8': 'ai', '\u0bca': 'o', '\u0bcb': 'oo', '\u0bcc': 'au',
}

# Gujarati to Roman transliteration (basic)
GUJARATI_TO_ROMAN: Dict[str, str] = {
    '\u0a85': 'a', '\u0a86': 'aa', '\u0a87': 'i', '\u0a88': 'ee', '\u0a89': 'u', '\u0a8a': 'oo',
    '\u0a8f': 'e', '\u0a90': 'ai', '\u0a93': 'o', '\u0a94': 'au',
    '\u0a95': 'ka', '\u0a96': 'kha', '\u0a97': 'ga', '\u0a98': 'gha', '\u0a99': 'nga',
    '\u0a9a': 'cha', '\u0a9b': 'chha', '\u0a9c': 'ja', '\u0a9d': 'jha', '\u0a9e': 'nya',
    '\u0a9f': 'ta', '\u0aa0': 'tha', '\u0aa1': 'da', '\u0aa2': 'dha', '\u0aa3': 'na',
    '\u0aa4': 'ta', '\u0aa5': 'tha', '\u0aa6': 'da', '\u0aa7': 'dha', '\u0aa8': 'na',
    '\u0aaa': 'pa', '\u0aab': 'pha', '\u0aac': 'ba', '\u0aad': 'bha', '\u0aae': 'ma',
    '\u0aaf': 'ya', '\u0ab0': 'ra', '\u0ab2': 'la', '\u0ab5': 'va', '\u0ab6': 'sha',
    '\u0ab7': 'sha', '\u0ab8': 'sa', '\u0ab9': 'ha',
    # Matras
    '\u0abe': 'aa', '\u0abf': 'i', '\u0ac0': 'ee', '\u0ac1': 'u', '\u0ac2': 'oo',
    '\u0ac7': 'e', '\u0ac8': 'ai', '\u0acb': 'o', '\u0acc': 'au',
    '\u0a82': 'n', '\u0a83': 'h', '\u0acd': '',  # Halant
}


def get_char_map(language: str) -> Dict[str, str]:
    """Get the character map for a specific language."""
    language_upper = language.upper()
    if language_upper in ['HINDI', 'FIJI_HINDI']:
        return HINDI_TO_ROMAN
    elif language_upper == 'TAMIL':
        return TAMIL_TO_ROMAN
    elif language_upper == 'GUJARATI':
        return GUJARATI_TO_ROMAN
    # Default to Hindi for other Indian languages
    return HINDI_TO_ROMAN


def transliterate_to_roman(text: str, language: str = 'HINDI') -> str:
    """
    Convert native script text to Roman/Hinglish transliteration.

    Examples:
        "namaste" -> "namaste"
        "kaise ho" -> "kaise ho"

    Args:
        text: Text in native script
        language: Language code (HINDI, TAMIL, GUJARATI, etc.)

    Returns:
        Roman/Hinglish transliteration
    """
    if not text:
        return ''

    char_map = get_char_map(language)
    result = []
    i = 0
    text_len = len(text)

    while i < text_len:
        # Try three-character combinations first (for conjuncts)
        if i + 2 < text_len:
            three_char = text[i:i+3]
            if three_char in char_map:
                result.append(char_map[three_char])
                i += 3
                continue

        # Try two-character combinations
        if i + 1 < text_len:
            two_char = text[i:i+2]
            if two_char in char_map:
                result.append(char_map[two_char])
                i += 2
                continue

        # Single character
        char = text[i]
        if char in char_map:
            result.append(char_map[char])
        elif char == ' ':
            result.append(' ')
        elif char.isascii():
            result.append(char)
        # Skip unknown characters

        i += 1

    # Clean up double vowels and formatting
    roman = ''.join(result)
    roman = re.sub(r'\s+', ' ', roman)  # Multiple spaces to single
    return roman.strip()


def generate_phonetic_hint(word: str, language: str = 'HINDI') -> str:
    """
    Generate a phonetic pronunciation hint for a word.

    Example: "namaste" -> "Say: na-ma-ste"

    Args:
        word: Word in native script
        language: Language code

    Returns:
        Phonetic hint string
    """
    roman = transliterate_to_roman(word, language)

    if not roman:
        return ''

    # Add syllable breaks for easier reading
    # This is a simplified version - could be enhanced with proper syllabification
    syllables = []
    current = ''
    vowels = 'aeiou'

    for i, char in enumerate(roman):
        current += char
        # Break after vowels (simplified)
        if char in vowels and i < len(roman) - 1:
            next_char = roman[i + 1] if i + 1 < len(roman) else ''
            # Don't break if next char is also a vowel (like 'aa', 'ee')
            if next_char not in vowels:
                syllables.append(current)
                current = ''

    if current:
        syllables.append(current)

    if syllables:
        return f"Say: {'-'.join(syllables)}"
    return f"Say: {roman}"


# ============================================
# WORD-BY-WORD COMPARISON
# ============================================

@dataclass
class WordComparison:
    """Comparison result for a single word."""
    expected: str
    expected_roman: str
    heard: str
    heard_roman: str
    is_correct: bool
    similarity: float
    phonetic_hint: Optional[str] = None


def compare_words(
    expected_text: str,
    heard_text: str,
    language: str = 'HINDI'
) -> List[WordComparison]:
    """
    Compare expected and heard text word by word.

    Returns a list of WordComparison objects showing which words
    matched and which didn't.

    Args:
        expected_text: The expected text
        heard_text: The transcribed text
        language: Language code

    Returns:
        List of word comparisons
    """
    expected_words = expected_text.split() if expected_text else []
    heard_words = heard_text.split() if heard_text else []

    comparisons = []

    # Match words using sequence matching for best alignment
    matcher = SequenceMatcher(None, expected_words, heard_words)

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            # Words match
            for k in range(i2 - i1):
                exp_word = expected_words[i1 + k]
                heard_word = heard_words[j1 + k]
                comparisons.append(WordComparison(
                    expected=exp_word,
                    expected_roman=transliterate_to_roman(exp_word, language),
                    heard=heard_word,
                    heard_roman=transliterate_to_roman(heard_word, language),
                    is_correct=True,
                    similarity=1.0,
                ))
        elif tag == 'replace':
            # Words differ - pair them up
            for k in range(max(i2 - i1, j2 - j1)):
                exp_idx = i1 + min(k, i2 - i1 - 1) if i2 > i1 else None
                heard_idx = j1 + min(k, j2 - j1 - 1) if j2 > j1 else None

                exp_word = expected_words[exp_idx] if exp_idx is not None else ''
                heard_word = heard_words[heard_idx] if heard_idx is not None else ''

                similarity = SequenceMatcher(None, exp_word, heard_word).ratio() if exp_word and heard_word else 0

                comparisons.append(WordComparison(
                    expected=exp_word,
                    expected_roman=transliterate_to_roman(exp_word, language) if exp_word else '',
                    heard=heard_word,
                    heard_roman=transliterate_to_roman(heard_word, language) if heard_word else '',
                    is_correct=similarity >= 0.8,
                    similarity=similarity,
                    phonetic_hint=generate_phonetic_hint(exp_word, language) if exp_word and similarity < 0.8 else None,
                ))
        elif tag == 'delete':
            # Expected word was not heard
            for k in range(i1, i2):
                exp_word = expected_words[k]
                comparisons.append(WordComparison(
                    expected=exp_word,
                    expected_roman=transliterate_to_roman(exp_word, language),
                    heard='',
                    heard_roman='',
                    is_correct=False,
                    similarity=0.0,
                    phonetic_hint=generate_phonetic_hint(exp_word, language),
                ))
        elif tag == 'insert':
            # Extra word was heard (not expected)
            for k in range(j1, j2):
                heard_word = heard_words[k]
                comparisons.append(WordComparison(
                    expected='',
                    expected_roman='',
                    heard=heard_word,
                    heard_roman=transliterate_to_roman(heard_word, language),
                    is_correct=False,
                    similarity=0.0,
                ))

    return comparisons


# ============================================
# CHILD-FRIENDLY FEEDBACK MESSAGES
# ============================================

@dataclass
class FeedbackMessages:
    """Feedback messages in both Hindi and English."""
    hindi: str
    english: str
    emoji: str
    encouragement: str


# Excellent (90%+)
EXCELLENT_MESSAGES = [
    FeedbackMessages("bahut badhiya!", "Amazing pronunciation!", "\u2b50", "You sound just like a native speaker!"),
    FeedbackMessages("shaabash!", "Fantastic job!", "\u2728", "Perfect! Keep up the great work!"),
    FeedbackMessages("waah! bahut achha!", "Wow! Excellent!", "\ud83c\udf89", "You're a pronunciation superstar!"),
    FeedbackMessages("ekdam sahi!", "Absolutely perfect!", "\ud83d\udcab", "That was beautiful!"),
]

# Good (70-89%)
GOOD_MESSAGES = [
    FeedbackMessages("achha!", "Good job!", "\ud83d\udc4d", "You're getting really good at this!"),
    FeedbackMessages("bahut achhe!", "Well done!", "\ud83d\ude0a", "Almost perfect! Just a tiny bit more practice."),
    FeedbackMessages("achhi koshish!", "Nice try!", "\ud83d\udcaa", "You're so close to perfect!"),
    FeedbackMessages("badhiya!", "Great effort!", "\ud83d\ude4c", "Keep practicing, you're doing great!"),
]

# Okay (50-69%)
OKAY_MESSAGES = [
    FeedbackMessages("theek hai!", "Getting there!", "\ud83d\udc4f", "Good effort! Let's try once more."),
    FeedbackMessages("koshish jaari rakho!", "Keep trying!", "\ud83d\udcaa", "You're improving! Listen again and try."),
    FeedbackMessages("aur koshish karo!", "Try again!", "\ud83d\udd04", "Practice makes perfect! You can do it!"),
]

# Needs Work (<50%)
TRY_AGAIN_MESSAGES = [
    FeedbackMessages("phir se suno!", "Listen again!", "\ud83d\udc42", "Listen carefully and give it another try!"),
    FeedbackMessages("dheere bolo!", "Speak slowly!", "\ud83d\udc22", "Try saying it slowly, one word at a time."),
    FeedbackMessages("phir koshish karo!", "Let's try again!", "\ud83d\udd01", "Don't worry! Every try makes you better!"),
]


def get_feedback_message(score: int, attempt_number: int = 1) -> FeedbackMessages:
    """
    Get an encouraging feedback message based on score.

    Args:
        score: Score from 0-100
        attempt_number: Which attempt this is (for varied messages)

    Returns:
        FeedbackMessages with Hindi, English, emoji, and encouragement
    """
    if score >= 90:
        messages = EXCELLENT_MESSAGES
    elif score >= 70:
        messages = GOOD_MESSAGES
    elif score >= 50:
        messages = OKAY_MESSAGES
    else:
        messages = TRY_AGAIN_MESSAGES

    # Vary messages based on attempt number for freshness
    index = (attempt_number - 1) % len(messages)
    return messages[index]


def evaluate_pronunciation_enhanced(
    expected_text: str,
    transcribed_text: str,
    confidence: float,
    language: str = 'HINDI',
    attempt_number: int = 1,
) -> dict:
    """
    Enhanced pronunciation evaluation with child-friendly feedback.

    This extends the basic scoring with:
    - Hinglish/Roman transliteration
    - Word-by-word comparison
    - Child-friendly messages in Hindi and English
    - Phonetic hints for incorrect words

    Args:
        expected_text: The text the user was supposed to say
        transcribed_text: The transcribed text from STT
        confidence: STT confidence score (0.0 to 1.0)
        language: Language code (HINDI, TAMIL, etc.)
        attempt_number: Which attempt this is (for varied messages)

    Returns:
        Comprehensive evaluation dict with scoring, feedback, and hints
    """
    # Normalize texts
    def normalize(text: str) -> str:
        if not text:
            return ''
        text = unicodedata.normalize('NFC', text)
        text = text.lower().strip()
        text = re.sub(r'[\u0964\u0965,.!?;:\'"()\[\]{}]', '', text)  # Remove punctuation
        text = ' '.join(text.split())
        return text

    expected_norm = normalize(expected_text)
    transcribed_norm = normalize(transcribed_text)

    # Calculate text similarity
    if not expected_norm:
        similarity = 0.0
    elif expected_norm == transcribed_norm:
        similarity = 1.0
    else:
        similarity = SequenceMatcher(None, expected_norm, transcribed_norm).ratio()

    # Calculate final score (weighted: 70% similarity, 30% confidence)
    capped_confidence = min(max(confidence, 0.0), 1.0)
    final_score = int((similarity * 0.7 + capped_confidence * 0.3) * 100)
    final_score = min(100, max(0, final_score))

    # Determine stars (0-3)
    if final_score >= 90:
        stars = 3
    elif final_score >= 70:
        stars = 2
    elif final_score >= 50:
        stars = 1
    else:
        stars = 0

    # Get feedback message
    feedback = get_feedback_message(final_score, attempt_number)

    # Word-by-word comparison
    word_comparisons = compare_words(expected_text, transcribed_text or '', language)

    # Transliterations
    expected_roman = transliterate_to_roman(expected_text, language)
    heard_roman = transliterate_to_roman(transcribed_text, language) if transcribed_text else ''

    # Collect phonetic hints for incorrect words
    hints = [
        w.phonetic_hint
        for w in word_comparisons
        if w.phonetic_hint and not w.is_correct
    ]

    # Build response
    return {
        # Scoring
        'score': final_score,
        'similarity': int(similarity * 100),
        'confidence': int(capped_confidence * 100),
        'stars': stars,
        'is_correct': final_score >= 70,

        # What was expected vs heard
        'expected': {
            'native': expected_text,
            'roman': expected_roman,
        },
        'heard': {
            'native': transcribed_text or '',
            'roman': heard_roman,
        },

        # Child-friendly feedback
        'feedback': {
            'level': 'excellent' if final_score >= 90 else 'good' if final_score >= 70 else 'okay' if final_score >= 50 else 'try_again',
            'emoji': feedback.emoji,
            'message_hindi': feedback.hindi,
            'message_english': feedback.english,
            'encouragement': feedback.encouragement,
        },

        # Word-by-word breakdown
        'word_comparison': [
            {
                'expected': w.expected,
                'expected_roman': w.expected_roman,
                'heard': w.heard,
                'heard_roman': w.heard_roman,
                'is_correct': w.is_correct,
                'similarity': int(w.similarity * 100),
                'hint': w.phonetic_hint,
            }
            for w in word_comparisons
        ],

        # Phonetic hints for incorrect words
        'hints': hints,

        # Attempt tracking
        'attempt_number': attempt_number,
    }
