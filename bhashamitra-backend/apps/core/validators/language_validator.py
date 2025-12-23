"""
Language Purity Validator for BhashaMitra

Ensures content uses correct script and doesn't mix languages inappropriately.

Supported Languages:
- HINDI: Devanagari script (U+0900-U+097F)
- TAMIL: Tamil script (U+0B80-U+0BFF)
- GUJARATI: Gujarati script (U+0A80-U+0AFF)
- PUNJABI: Gurmukhi script (U+0A00-U+0A7F)
- TELUGU: Telugu script (U+0C00-U+0C7F)
- MALAYALAM: Malayalam script (U+0D00-U+0D7F)
- BENGALI: Bengali script (U+0980-U+09FF)
- KANNADA: Kannada script (U+0C80-U+0CFF)
"""
import re
from typing import Dict, List, Set, Any


class LanguagePurityValidator:
    """
    Validates that text content uses the correct script for the target language.

    Example:
        validator = LanguagePurityValidator()
        result = validator.validate_text("नमस्ते", "HINDI")
        # {'is_pure': True, 'script_ratio': 1.0}

        result = validator.validate_text("नमस्ते hello", "HINDI")
        # {'is_pure': False, 'foreign_chars': ['h', 'e', 'l', 'o'], 'foreign_ratio': 0.45}
    """

    # Unicode ranges for Indic scripts
    SCRIPT_RANGES = {
        'HINDI': (0x0900, 0x097F),       # Devanagari
        'MARATHI': (0x0900, 0x097F),     # Also Devanagari
        'TAMIL': (0x0B80, 0x0BFF),       # Tamil
        'GUJARATI': (0x0A80, 0x0AFF),    # Gujarati
        'PUNJABI': (0x0A00, 0x0A7F),     # Gurmukhi
        'TELUGU': (0x0C00, 0x0C7F),      # Telugu
        'MALAYALAM': (0x0D00, 0x0D7F),   # Malayalam
        'BENGALI': (0x0980, 0x09FF),     # Bengali
        'KANNADA': (0x0C80, 0x0CFF),     # Kannada
    }

    # Characters allowed in any language (punctuation, numbers, etc.)
    COMMON_ALLOWED = set(' ।॥,.-?!०१२३४५६७८९0123456789\n\t')

    def __init__(self):
        self._compiled_patterns: Dict[str, re.Pattern] = {}

    def validate_text(
        self,
        text: str,
        language: str,
        allow_mixed: bool = False,
        max_foreign_ratio: float = 0.0,
    ) -> Dict[str, Any]:
        """
        Validate that text uses the correct script for the specified language.

        Args:
            text: Text content to validate
            language: Target language (HINDI, TAMIL, etc.)
            allow_mixed: If True, allows some foreign characters
            max_foreign_ratio: Maximum ratio of foreign characters (0.0-1.0)

        Returns:
            Dictionary with validation results:
            - is_pure: Whether the text passes purity check
            - script_ratio: Ratio of target script characters
            - foreign_chars: List of foreign characters found
            - foreign_ratio: Ratio of foreign characters
        """
        if language not in self.SCRIPT_RANGES:
            return {
                'is_pure': False,
                'error': f"Unsupported language: {language}",
                'supported_languages': list(self.SCRIPT_RANGES.keys()),
            }

        script_range = self.SCRIPT_RANGES[language]

        target_chars = 0
        foreign_chars: List[str] = []
        total_chars = 0

        for char in text:
            if char in self.COMMON_ALLOWED:
                continue

            total_chars += 1
            char_code = ord(char)

            if script_range[0] <= char_code <= script_range[1]:
                target_chars += 1
            else:
                if char not in foreign_chars:
                    foreign_chars.append(char)

        if total_chars == 0:
            return {
                'is_pure': True,
                'script_ratio': 1.0,
                'foreign_chars': [],
                'foreign_ratio': 0.0,
            }

        foreign_ratio = len(foreign_chars) / total_chars if total_chars > 0 else 0
        script_ratio = target_chars / total_chars

        is_pure = (
            len(foreign_chars) == 0 or
            (allow_mixed and foreign_ratio <= max_foreign_ratio)
        )

        return {
            'is_pure': is_pure,
            'script_ratio': round(script_ratio, 3),
            'foreign_chars': foreign_chars[:10],  # Limit to first 10
            'foreign_ratio': round(foreign_ratio, 3),
            'language': language,
            'expected_script': self._get_script_name(language),
        }

    def get_script_characters(self, language: str) -> Set[str]:
        """Get all valid characters for a language's script."""
        if language not in self.SCRIPT_RANGES:
            return set()

        start, end = self.SCRIPT_RANGES[language]
        return {chr(i) for i in range(start, end + 1)}

    def extract_foreign_words(self, text: str, language: str) -> List[str]:
        """
        Extract foreign (non-target language) words from text.

        Useful for identifying English words mixed in with Hindi, etc.
        """
        if language not in self.SCRIPT_RANGES:
            return []

        script_range = self.SCRIPT_RANGES[language]

        # Split by spaces and filter
        words = text.split()
        foreign_words = []

        for word in words:
            is_foreign = False
            for char in word:
                if char in self.COMMON_ALLOWED:
                    continue
                char_code = ord(char)
                if not (script_range[0] <= char_code <= script_range[1]):
                    is_foreign = True
                    break

            if is_foreign:
                foreign_words.append(word)

        return foreign_words

    def suggest_corrections(self, text: str, language: str) -> Dict[str, Any]:
        """
        Suggest corrections for mixed-language text.

        Returns suggestions for replacing foreign characters or words.
        """
        foreign_words = self.extract_foreign_words(text, language)

        if not foreign_words:
            return {
                'has_suggestions': False,
                'message': 'No corrections needed',
            }

        suggestions = []
        for word in foreign_words:
            suggestions.append({
                'word': word,
                'suggestion': f"Replace '{word}' with {language} equivalent",
                'type': 'foreign_word',
            })

        return {
            'has_suggestions': True,
            'foreign_word_count': len(foreign_words),
            'suggestions': suggestions[:10],  # Limit suggestions
        }

    def _get_script_name(self, language: str) -> str:
        """Get the script name for a language."""
        script_names = {
            'HINDI': 'Devanagari',
            'MARATHI': 'Devanagari',
            'TAMIL': 'Tamil',
            'GUJARATI': 'Gujarati',
            'PUNJABI': 'Gurmukhi',
            'TELUGU': 'Telugu',
            'MALAYALAM': 'Malayalam',
            'BENGALI': 'Bengali',
            'KANNADA': 'Kannada',
        }
        return script_names.get(language, 'Unknown')

    def validate_transliteration_mapping(
        self,
        original: str,
        transliteration: str,
        language: str,
    ) -> Dict[str, Any]:
        """
        Validate that a transliteration correctly represents the original text.

        This is a basic check - full phonetic validation would require
        a language-specific dictionary or ML model.
        """
        # Basic checks
        if not original or not transliteration:
            return {
                'is_valid': False,
                'message': 'Both original and transliteration are required',
            }

        # Transliteration should be Latin alphabet
        if not re.match(r'^[a-zA-Z\s]+$', transliteration):
            return {
                'is_valid': False,
                'message': 'Transliteration should only contain Latin letters',
            }

        # Original should be in target script
        script_check = self.validate_text(original, language)
        if not script_check['is_pure']:
            return {
                'is_valid': False,
                'message': f'Original text contains non-{language} characters',
            }

        # Length ratio check (transliteration is usually longer due to multi-char mappings)
        length_ratio = len(transliteration) / len(original) if original else 0
        if length_ratio < 0.5 or length_ratio > 5:
            return {
                'is_valid': False,
                'message': 'Transliteration length seems incorrect',
                'length_ratio': round(length_ratio, 2),
            }

        return {
            'is_valid': True,
            'original_script': self._get_script_name(language),
            'length_ratio': round(length_ratio, 2),
        }
