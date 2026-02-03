"""
Peppi TTS Provider - Wrapper around Sarvam AI for Peppi narrator voice.

Peppi is the friendly AI tutor character for BhashaMitra.
This service configures Sarvam AI voices with Peppi-specific settings.
"""

import logging
from typing import Tuple, Optional
from apps.speech.services.sarvam_provider import SarvamAIProvider

logger = logging.getLogger(__name__)


class PeppiTTSProvider:
    """
    Peppi Narrator TTS Provider.

    Wraps SarvamAIProvider with Peppi-specific voice configurations
    optimized for child-friendly narration.
    """

    # Peppi voice configuration per language and gender
    # Pace 0.7 = balanced speed for children - clear and easy to follow
    PEPPI_VOICE_CONFIG = {
        'HINDI': {
            'male': {
                'speaker': 'arvind',
                'pitch': 0.4,
                'pace': 0.7,
                'model': 'bulbul:v2'
            },
            'female': {
                'speaker': 'anushka',
                'pitch': 0.3,
                'pace': 0.7,
                'model': 'bulbul:v2'
            }
        },
        'TAMIL': {
            'male': {
                'speaker': 'kumar',
                'pitch': 0.4,
                'pace': 0.7,
                'model': 'bulbul:v2'
            },
            'female': {
                'speaker': 'anushka',
                'pitch': 0.3,
                'pace': 0.7,
                'model': 'bulbul:v2'
            }
        },
        'GUJARATI': {
            'male': {
                'speaker': 'arvind',
                'pitch': 0.4,
                'pace': 0.7,
                'model': 'bulbul:v2'
            },
            'female': {
                'speaker': 'anushka',
                'pitch': 0.3,
                'pace': 0.7,
                'model': 'bulbul:v2'
            }
        },
        'PUNJABI': {
            'male': {
                'speaker': 'arvind',
                'pitch': 0.4,
                'pace': 0.7,
                'model': 'bulbul:v2'
            },
            'female': {
                'speaker': 'anushka',
                'pitch': 0.3,
                'pace': 0.7,
                'model': 'bulbul:v2'
            }
        },
        'TELUGU': {
            'male': {
                'speaker': 'arvind',
                'pitch': 0.4,
                'pace': 0.7,
                'model': 'bulbul:v2'
            },
            'female': {
                'speaker': 'anushka',
                'pitch': 0.3,
                'pace': 0.7,
                'model': 'bulbul:v2'
            }
        },
        'MALAYALAM': {
            'male': {
                'speaker': 'arvind',
                'pitch': 0.4,
                'pace': 0.7,
                'model': 'bulbul:v2'
            },
            'female': {
                'speaker': 'anushka',
                'pitch': 0.3,
                'pace': 0.7,
                'model': 'bulbul:v2'
            }
        },
        'BENGALI': {
            'male': {
                'speaker': 'arvind',
                'pitch': 0.4,
                'pace': 0.7,
                'model': 'bulbul:v2'
            },
            'female': {
                'speaker': 'anushka',
                'pitch': 0.3,
                'pace': 0.7,
                'model': 'bulbul:v2'
            }
        },
        'MARATHI': {
            'male': {
                'speaker': 'arvind',
                'pitch': 0.4,
                'pace': 0.7,
                'model': 'bulbul:v2'
            },
            'female': {
                'speaker': 'anushka',
                'pitch': 0.3,
                'pace': 0.7,
                'model': 'bulbul:v2'
            }
        },
        'KANNADA': {
            'male': {
                'speaker': 'arvind',
                'pitch': 0.4,
                'pace': 0.7,
                'model': 'bulbul:v2'
            },
            'female': {
                'speaker': 'anushka',
                'pitch': 0.3,
                'pace': 0.7,
                'model': 'bulbul:v2'
            }
        },
        'ODIA': {
            'male': {
                'speaker': 'arvind',
                'pitch': 0.4,
                'pace': 0.7,
                'model': 'bulbul:v2'
            },
            'female': {
                'speaker': 'anushka',
                'pitch': 0.3,
                'pace': 0.7,
                'model': 'bulbul:v2'
            }
        },
    }

    # Cultural terms for addressing children
    CULTURAL_TERMS = {
        'HINDI': {
            'male': 'भैया',      # Bhaiya
            'female': 'दीदी'      # Didi
        },
        'TAMIL': {
            'male': 'அண்ணா',     # Anna
            'female': 'அக்கா'     # Akka
        },
        'GUJARATI': {
            'male': 'ભાઈ',       # Bhai
            'female': 'બેન'       # Ben
        },
        'PUNJABI': {
            'male': 'ਵੀਰਜੀ',      # Veerji
            'female': 'ਭੈਣਜੀ'     # Bhainji
        },
        'TELUGU': {
            'male': 'అన్న',      # Anna
            'female': 'అక్క'      # Akka
        },
        'MALAYALAM': {
            'male': 'ചേട്ടൻ',     # Chetta
            'female': 'ചേച്ചി'    # Chechi
        },
        'BENGALI': {
            'male': 'দাদা',       # Dada
            'female': 'দিদি'      # Didi
        },
        'MARATHI': {
            'male': 'भाऊ',        # Bhau
            'female': 'दीदी'       # Didi
        },
        'KANNADA': {
            'male': 'ಅಣ್ಣ',       # Anna
            'female': 'ಅಕ್ಕ'      # Akka
        },
        'ODIA': {
            'male': 'ଭାଇ',        # Bhai
            'female': 'ଭଉଣୀ'      # Bhauni
        },
    }

    @classmethod
    def is_available(cls) -> bool:
        """Check if Peppi TTS is available (depends on Sarvam AI)."""
        return SarvamAIProvider.is_available()

    @classmethod
    def get_cultural_term(cls, language: str, gender: str) -> str:
        """
        Get cultural addressing term for a language and gender.

        Args:
            language: Language code (HINDI, TAMIL, etc.)
            gender: Gender preference ('male' or 'female')

        Returns:
            Cultural term in native script
        """
        if language not in cls.CULTURAL_TERMS:
            logger.warning(f"Language {language} not supported, defaulting to Hindi")
            language = 'HINDI'

        gender_lower = gender.lower() if gender else 'female'
        if gender_lower not in ['male', 'female']:
            gender_lower = 'female'

        return cls.CULTURAL_TERMS[language][gender_lower]

    @classmethod
    def get_peppi_name(cls, language: str, gender: str) -> str:
        """
        Get Peppi's name with cultural addressing term.

        Args:
            language: Language code (HINDI, TAMIL, etc.)
            gender: Gender preference ('male' or 'female')

        Returns:
            Peppi name with cultural term (e.g., "Peppi Didi", "Peppi Anna")
        """
        cultural_term = cls.get_cultural_term(language, gender)
        return f"Peppi {cultural_term}"

    @classmethod
    def narrate(
        cls,
        text: str,
        language: str = 'HINDI',
        gender: str = 'female',
        child_name: Optional[str] = None,
        addressing_mode: str = 'CULTURAL'
    ) -> Tuple[bytes, int]:
        """
        Generate Peppi narration for text.

        Args:
            text: Text to narrate
            language: Language code (HINDI, TAMIL, etc.)
            gender: Peppi gender ('male' or 'female')
            child_name: Child's name (optional, for personalization)
            addressing_mode: How Peppi addresses child ('CULTURAL' or 'BY_NAME')

        Returns:
            Tuple of (audio_bytes, generation_time_ms)

        Raises:
            Exception: If narration generation fails
        """
        # Get voice configuration for language and gender
        if language not in cls.PEPPI_VOICE_CONFIG:
            logger.warning(f"Language {language} not configured for Peppi, using Hindi")
            language = 'HINDI'

        gender_lower = gender.lower() if gender else 'female'
        if gender_lower not in ['male', 'female']:
            gender_lower = 'female'

        voice_config = cls.PEPPI_VOICE_CONFIG[language][gender_lower]

        # Generate speech using Sarvam AI with Peppi voice settings
        try:
            audio_bytes, generation_time = SarvamAIProvider.text_to_speech(
                text=text,
                language=language,
                voice=voice_config['speaker'],
                model=voice_config['model'],
                pace=voice_config['pace']
            )

            logger.info(
                f"Peppi narration generated: {language}, {gender_lower}, "
                f"{len(text)} chars, {generation_time}ms"
            )

            return audio_bytes, generation_time

        except Exception as e:
            logger.error(f"Peppi narration failed: {e}")
            raise

    @classmethod
    def get_supported_languages(cls) -> list:
        """Get list of languages supported by Peppi."""
        return list(cls.PEPPI_VOICE_CONFIG.keys())

    @classmethod
    def get_voice_config(cls, language: str, gender: str) -> dict:
        """
        Get voice configuration for a language and gender.

        Args:
            language: Language code
            gender: Gender preference ('male' or 'female')

        Returns:
            Voice configuration dict
        """
        if language not in cls.PEPPI_VOICE_CONFIG:
            language = 'HINDI'

        gender_lower = gender.lower() if gender else 'female'
        if gender_lower not in ['male', 'female']:
            gender_lower = 'female'

        return cls.PEPPI_VOICE_CONFIG[language][gender_lower]
