"""
Content Validation System for BhashaMitra

Ensures curriculum content meets quality standards:
1. Language purity (no mixed languages)
2. NCERT alignment (verified curriculum)
3. Age appropriateness
4. Audio file integrity
5. Transliteration accuracy
"""
import re
import logging
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class ValidationSeverity(Enum):
    ERROR = 'error'       # Blocks content from being published
    WARNING = 'warning'   # Should be reviewed but doesn't block
    INFO = 'info'         # Informational only


@dataclass
class ValidationIssue:
    """Represents a single validation issue."""
    field: str
    message: str
    severity: ValidationSeverity
    suggestion: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


@dataclass
class ValidationResult:
    """Result of content validation."""
    is_valid: bool
    issues: List[ValidationIssue] = field(default_factory=list)
    content_id: Optional[str] = None
    content_type: Optional[str] = None

    @property
    def errors(self) -> List[ValidationIssue]:
        return [i for i in self.issues if i.severity == ValidationSeverity.ERROR]

    @property
    def warnings(self) -> List[ValidationIssue]:
        return [i for i in self.issues if i.severity == ValidationSeverity.WARNING]

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def add_error(self, field: str, message: str, suggestion: str = None):
        self.issues.append(ValidationIssue(
            field=field,
            message=message,
            severity=ValidationSeverity.ERROR,
            suggestion=suggestion,
        ))
        self.is_valid = False

    def add_warning(self, field: str, message: str, suggestion: str = None):
        self.issues.append(ValidationIssue(
            field=field,
            message=message,
            severity=ValidationSeverity.WARNING,
            suggestion=suggestion,
        ))

    def add_info(self, field: str, message: str):
        self.issues.append(ValidationIssue(
            field=field,
            message=message,
            severity=ValidationSeverity.INFO,
        ))

    def to_dict(self) -> Dict:
        return {
            'is_valid': self.is_valid,
            'content_id': self.content_id,
            'content_type': self.content_type,
            'error_count': len(self.errors),
            'warning_count': len(self.warnings),
            'issues': [
                {
                    'field': i.field,
                    'message': i.message,
                    'severity': i.severity.value,
                    'suggestion': i.suggestion,
                }
                for i in self.issues
            ],
        }


class ContentValidationError(Exception):
    """Raised when content validation fails."""
    def __init__(self, result: ValidationResult):
        self.result = result
        super().__init__(f"Content validation failed with {len(result.errors)} errors")


class ContentValidator:
    """
    Main content validator that orchestrates all validation checks.

    Usage:
        validator = ContentValidator()
        result = validator.validate_letter({
            'letter': 'क',
            'transliteration': 'ka',
            'example_word': 'कमल',
            'example_meaning': 'lotus',
            'language': 'HINDI',
        })

        if not result.is_valid:
            for issue in result.errors:
                print(f"Error: {issue.message}")
    """

    def __init__(self):
        from .language_validator import LanguagePurityValidator
        from .curriculum_validator import NCERTValidator, AgeAppropriatenessValidator

        self.language_validator = LanguagePurityValidator()
        self.ncert_validator = NCERTValidator()
        self.age_validator = AgeAppropriatenessValidator()

    def validate_letter(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate alphabet letter content."""
        result = ValidationResult(is_valid=True, content_type='letter')

        # Required fields
        required_fields = ['letter', 'transliteration', 'language']
        for field in required_fields:
            if not data.get(field):
                result.add_error(field, f"Missing required field: {field}")

        if result.has_errors:
            return result

        language = data['language']
        letter = data['letter']
        transliteration = data['transliteration']

        # Language purity check
        purity_result = self.language_validator.validate_text(letter, language)
        if not purity_result['is_pure']:
            result.add_error(
                'letter',
                f"Letter contains non-{language} characters",
                suggestion=f"Remove characters: {purity_result.get('foreign_chars', [])}"
            )

        # Transliteration format check
        if not self._is_valid_transliteration(transliteration):
            result.add_error(
                'transliteration',
                "Transliteration should only contain lowercase Latin letters",
                suggestion="Use only a-z characters"
            )

        # Example word validation (if provided)
        if data.get('example_word'):
            word_purity = self.language_validator.validate_text(data['example_word'], language)
            if not word_purity['is_pure']:
                result.add_warning(
                    'example_word',
                    f"Example word contains non-{language} characters",
                )

        # NCERT validation
        if language == 'HINDI':
            ncert_result = self.ncert_validator.validate_hindi_letter(letter, transliteration)
            if not ncert_result['is_valid']:
                result.add_warning(
                    'letter',
                    ncert_result.get('message', 'Letter may not align with NCERT curriculum'),
                )

        return result

    def validate_vocabulary(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate vocabulary word content."""
        result = ValidationResult(is_valid=True, content_type='vocabulary')

        # Required fields
        required_fields = ['word', 'transliteration', 'meaning', 'language']
        for field in required_fields:
            if not data.get(field):
                result.add_error(field, f"Missing required field: {field}")

        if result.has_errors:
            return result

        language = data['language']
        word = data['word']

        # Language purity check
        purity_result = self.language_validator.validate_text(word, language)
        if not purity_result['is_pure']:
            result.add_error(
                'word',
                f"Word contains non-{language} characters: {purity_result.get('foreign_chars', [])}",
            )

        # Meaning should be in English
        meaning = data['meaning']
        if self._contains_devanagari(meaning):
            result.add_warning(
                'meaning',
                "Meaning should be in English, not Hindi script",
                suggestion="Provide English translation"
            )

        # Transliteration format
        transliteration = data['transliteration']
        if not self._is_valid_transliteration(transliteration):
            result.add_error(
                'transliteration',
                "Transliteration should only contain lowercase Latin letters and spaces",
            )

        # Age appropriateness (if category provided)
        if data.get('category') and data.get('min_age'):
            age_result = self.age_validator.validate_content(
                word, data['category'], data['min_age']
            )
            if not age_result['is_appropriate']:
                result.add_warning(
                    'word',
                    age_result.get('message', 'Content may not be age-appropriate'),
                )

        return result

    def validate_story_page(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate story page content."""
        result = ValidationResult(is_valid=True, content_type='story_page')

        required_fields = ['text_content', 'language', 'page_number']
        for field in required_fields:
            if data.get(field) is None:
                result.add_error(field, f"Missing required field: {field}")

        if result.has_errors:
            return result

        language = data['language']
        text = data['text_content']

        # Language purity check (stories can have limited English)
        purity_result = self.language_validator.validate_text(
            text, language, allow_mixed=True, max_foreign_ratio=0.1
        )
        if not purity_result['is_pure']:
            result.add_warning(
                'text_content',
                f"Story contains too much non-{language} text ({purity_result.get('foreign_ratio', 0)*100:.1f}%)",
                suggestion="Keep non-target language content under 10%"
            )

        # Text length check
        if len(text) > 500:
            result.add_warning(
                'text_content',
                f"Story page text is quite long ({len(text)} chars)",
                suggestion="Consider splitting into multiple pages for better readability"
            )

        if len(text) < 20:
            result.add_warning(
                'text_content',
                "Story page text is very short",
                suggestion="Add more content for meaningful learning"
            )

        return result

    def validate_audio_cache(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate audio cache entry."""
        result = ValidationResult(is_valid=True, content_type='audio_cache')

        required_fields = ['text_content', 'language', 'cache_key']
        for field in required_fields:
            if not data.get(field):
                result.add_error(field, f"Missing required field: {field}")

        if result.has_errors:
            return result

        # Audio file validation
        if data.get('audio_file'):
            audio_file = data['audio_file']

            # Check file size (should be reasonable for speech)
            if hasattr(audio_file, 'size'):
                if audio_file.size > 5 * 1024 * 1024:  # 5MB
                    result.add_warning(
                        'audio_file',
                        f"Audio file is large ({audio_file.size / 1024 / 1024:.1f}MB)",
                        suggestion="Consider compressing or reducing quality"
                    )
                if audio_file.size < 1000:  # 1KB - too small for audio
                    result.add_error(
                        'audio_file',
                        "Audio file is too small, may be corrupted",
                    )

        # Duration check
        if data.get('audio_duration_ms'):
            duration = data['audio_duration_ms']
            if duration > 30000:  # 30 seconds
                result.add_warning(
                    'audio_duration_ms',
                    f"Audio duration is long ({duration/1000:.1f}s)",
                )
            if duration < 100:  # 0.1 seconds
                result.add_error(
                    'audio_duration_ms',
                    "Audio duration is too short",
                )

        return result

    def validate_batch(self, items: List[Dict], content_type: str) -> Dict:
        """Validate multiple items at once."""
        results = []
        valid_count = 0
        error_count = 0

        validator_map = {
            'letter': self.validate_letter,
            'vocabulary': self.validate_vocabulary,
            'story_page': self.validate_story_page,
            'audio_cache': self.validate_audio_cache,
        }

        validator = validator_map.get(content_type)
        if not validator:
            raise ValueError(f"Unknown content type: {content_type}")

        for item in items:
            result = validator(item)
            results.append(result.to_dict())

            if result.is_valid:
                valid_count += 1
            else:
                error_count += 1

        return {
            'total': len(items),
            'valid': valid_count,
            'invalid': error_count,
            'results': results,
        }

    def _is_valid_transliteration(self, text: str) -> bool:
        """Check if transliteration uses only valid characters."""
        return bool(re.match(r'^[a-z\s]+$', text.lower()))

    def _contains_devanagari(self, text: str) -> bool:
        """Check if text contains Devanagari script."""
        return bool(re.search(r'[\u0900-\u097F]', text))
