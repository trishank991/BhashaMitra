"""
Curriculum Validation for BhashaMitra

Ensures content aligns with NCERT standards and is age-appropriate.
"""
from typing import Dict, List, Any, Optional


class NCERTValidator:
    """
    Validates content against NCERT curriculum standards.

    NCERT (National Council of Educational Research and Training) sets
    the standard curriculum for Indian schools, which we follow for
    curriculum accuracy.
    """

    # NCERT-verified Hindi alphabet order
    HINDI_VOWELS = ['अ', 'आ', 'इ', 'ई', 'उ', 'ऊ', 'ऋ', 'ए', 'ऐ', 'ओ', 'औ', 'अं', 'अः']

    HINDI_CONSONANTS = [
        # क वर्ग (Velar)
        'क', 'ख', 'ग', 'घ', 'ङ',
        # च वर्ग (Palatal)
        'च', 'छ', 'ज', 'झ', 'ञ',
        # ट वर्ग (Retroflex)
        'ट', 'ठ', 'ड', 'ढ', 'ण',
        # त वर्ग (Dental)
        'त', 'थ', 'द', 'ध', 'न',
        # प वर्ग (Labial)
        'प', 'फ', 'ब', 'भ', 'म',
        # अंतःस्थ (Semivowels)
        'य', 'र', 'ल', 'व',
        # ऊष्म (Fricatives)
        'श', 'ष', 'स', 'ह',
    ]

    # Standard transliterations per NCERT
    HINDI_TRANSLITERATIONS = {
        'अ': 'a', 'आ': 'aa', 'इ': 'i', 'ई': 'ee', 'उ': 'u', 'ऊ': 'oo',
        'ऋ': 'ri', 'ए': 'e', 'ऐ': 'ai', 'ओ': 'o', 'औ': 'au',
        'अं': 'am', 'अः': 'ah',
        'क': 'ka', 'ख': 'kha', 'ग': 'ga', 'घ': 'gha', 'ङ': 'nga',
        'च': 'cha', 'छ': 'chha', 'ज': 'ja', 'झ': 'jha', 'ञ': 'nya',
        'ट': 'ta', 'ठ': 'tha', 'ड': 'da', 'ढ': 'dha', 'ण': 'na',
        'त': 'ta', 'थ': 'tha', 'द': 'da', 'ध': 'dha', 'न': 'na',
        'प': 'pa', 'फ': 'pha', 'ब': 'ba', 'भ': 'bha', 'म': 'ma',
        'य': 'ya', 'र': 'ra', 'ल': 'la', 'व': 'va',
        'श': 'sha', 'ष': 'sha', 'स': 'sa', 'ह': 'ha',
    }

    # NCERT standard example words for each letter
    NCERT_EXAMPLES = {
        'अ': 'अनार', 'आ': 'आम', 'इ': 'इमली', 'ई': 'ईख', 'उ': 'उल्लू', 'ऊ': 'ऊन',
        'क': 'कमल', 'ख': 'खरगोश', 'ग': 'गमला', 'घ': 'घड़ी',
        'च': 'चम्मच', 'छ': 'छतरी', 'ज': 'जहाज़', 'झ': 'झंडा',
        'ट': 'टमाटर', 'ठ': 'ठेला', 'ड': 'डमरू', 'ढ': 'ढोल',
        'त': 'तरबूज़', 'थ': 'थाली', 'द': 'दवात', 'ध': 'धनुष', 'न': 'नल',
        'प': 'पतंग', 'फ': 'फल', 'ब': 'बतख़', 'भ': 'भालू', 'म': 'मछली',
        'य': 'यज्ञ', 'र': 'रथ', 'ल': 'लड्डू', 'व': 'वन',
        'श': 'शहद', 'स': 'सेब', 'ह': 'हाथी',
    }

    def validate_hindi_letter(self, letter: str, transliteration: str) -> Dict[str, Any]:
        """
        Validate that a Hindi letter and its transliteration match NCERT standards.
        """
        # Check if letter is in NCERT alphabet
        all_letters = self.HINDI_VOWELS + self.HINDI_CONSONANTS

        if letter not in all_letters:
            return {
                'is_valid': False,
                'message': f"Letter '{letter}' not in NCERT Hindi alphabet",
                'suggestion': 'Check for typos or use standard Devanagari character',
            }

        # Check transliteration
        expected_trans = self.HINDI_TRANSLITERATIONS.get(letter)
        if expected_trans and transliteration.lower() != expected_trans:
            return {
                'is_valid': True,  # Not blocking, just warning
                'is_standard': False,
                'message': f"Transliteration differs from NCERT standard",
                'provided': transliteration,
                'expected': expected_trans,
            }

        return {
            'is_valid': True,
            'is_standard': True,
            'letter_type': 'vowel' if letter in self.HINDI_VOWELS else 'consonant',
            'ncert_example': self.NCERT_EXAMPLES.get(letter),
        }

    def validate_hindi_alphabet_order(self, letters: List[str]) -> Dict[str, Any]:
        """
        Validate that a list of letters follows NCERT alphabet order.
        """
        expected_order = self.HINDI_VOWELS + self.HINDI_CONSONANTS
        expected_subset = [l for l in expected_order if l in letters]

        if letters == expected_subset:
            return {
                'is_valid': True,
                'message': 'Letters follow NCERT order',
            }

        # Find misorderings
        misorderings = []
        for i, letter in enumerate(letters):
            if letter in expected_order:
                expected_idx = expected_order.index(letter)
                if i > 0 and letters[i-1] in expected_order:
                    prev_expected_idx = expected_order.index(letters[i-1])
                    if expected_idx < prev_expected_idx:
                        misorderings.append({
                            'letter': letter,
                            'should_come_before': letters[i-1],
                        })

        return {
            'is_valid': len(misorderings) == 0,
            'misorderings': misorderings,
            'expected_order': expected_subset,
        }

    def get_letter_category(self, letter: str) -> Optional[str]:
        """Get the grammatical category of a Hindi letter."""
        if letter in self.HINDI_VOWELS:
            return 'स्वर (Vowel)'

        # Consonant categories
        consonant_groups = {
            'क वर्ग (Velar)': ['क', 'ख', 'ग', 'घ', 'ङ'],
            'च वर्ग (Palatal)': ['च', 'छ', 'ज', 'झ', 'ञ'],
            'ट वर्ग (Retroflex)': ['ट', 'ठ', 'ड', 'ढ', 'ण'],
            'त वर्ग (Dental)': ['त', 'थ', 'द', 'ध', 'न'],
            'प वर्ग (Labial)': ['प', 'फ', 'ब', 'भ', 'म'],
            'अंतःस्थ (Semivowel)': ['य', 'र', 'ल', 'व'],
            'ऊष्म (Fricative)': ['श', 'ष', 'स', 'ह'],
        }

        for category, letters in consonant_groups.items():
            if letter in letters:
                return category

        return None


class AgeAppropriatenessValidator:
    """
    Validates content is appropriate for the target age group.

    Age groups:
    - Junior (4-6): Simple, concrete concepts, basic vocabulary
    - Standard (7-10): More complex vocabulary, abstract concepts
    - Teen (11-14): Advanced vocabulary, grammar rules
    """

    # Words/topics appropriate for each age group
    AGE_APPROPRIATE_CATEGORIES = {
        'junior': {
            'allowed': ['family', 'colors', 'numbers', 'animals', 'food', 'body_parts', 'greetings'],
            'max_word_length': 6,
            'max_syllables': 3,
        },
        'standard': {
            'allowed': ['family', 'colors', 'numbers', 'animals', 'food', 'body_parts',
                       'greetings', 'actions', 'household', 'nature', 'time', 'emotions'],
            'max_word_length': 10,
            'max_syllables': 5,
        },
        'teen': {
            'allowed': 'all',  # All categories allowed
            'max_word_length': 15,
            'max_syllables': 8,
        },
    }

    # Topics that require specific age handling
    SENSITIVE_TOPICS = ['violence', 'fear', 'death', 'romance']

    def validate_content(
        self,
        content: str,
        category: str,
        min_age: int,
    ) -> Dict[str, Any]:
        """
        Validate content is appropriate for the specified age group.
        """
        age_group = self._get_age_group(min_age)
        config = self.AGE_APPROPRIATE_CATEGORIES[age_group]

        issues = []

        # Check category appropriateness
        if config['allowed'] != 'all':
            if category.lower() not in config['allowed']:
                issues.append({
                    'type': 'category',
                    'message': f"Category '{category}' may be too advanced for age {min_age}",
                })

        # Check word length
        if len(content) > config['max_word_length']:
            issues.append({
                'type': 'length',
                'message': f"Content length ({len(content)}) exceeds recommendation for age {min_age}",
            })

        return {
            'is_appropriate': len(issues) == 0,
            'age_group': age_group,
            'issues': issues,
            'recommendations': config,
        }

    def get_recommended_vocabulary_count(self, age: int) -> Dict[str, int]:
        """Get recommended vocabulary limits by age."""
        if age <= 6:
            return {
                'words_per_lesson': 3,
                'total_vocabulary': 100,
                'new_words_per_week': 10,
            }
        elif age <= 10:
            return {
                'words_per_lesson': 5,
                'total_vocabulary': 300,
                'new_words_per_week': 20,
            }
        else:
            return {
                'words_per_lesson': 8,
                'total_vocabulary': 500,
                'new_words_per_week': 30,
            }

    def _get_age_group(self, age: int) -> str:
        """Convert age to age group."""
        if age <= 6:
            return 'junior'
        elif age <= 10:
            return 'standard'
        return 'teen'
