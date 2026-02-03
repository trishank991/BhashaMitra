"""
VoiceCharacter Service - Manage voice character profiles and TTS configuration.

Provides centralized service for:
- Retrieving voice characters by type and language
- Generating SSML/TTS configurations
- Preparing text with character personality enhancements
- Managing character availability
"""

import logging
import random
from typing import Optional, Dict, List
from django.core.cache import cache
from apps.speech.models import VoiceCharacter

logger = logging.getLogger(__name__)


class VoiceCharacterService:
    """
    Service for managing voice characters and their TTS configurations.
    """

    # Cache TTL for voice character queries (10 minutes)
    CACHE_TTL = 600

    @classmethod
    def get_character(
        cls,
        character_type: str,
        language: str,
        gender: str = 'FEMALE'
    ) -> Optional[VoiceCharacter]:
        """
        Get voice character by type, language, and gender.

        Args:
            character_type: Character type (PEPPI, GRANDMOTHER, etc.)
            language: Language code (HINDI, TAMIL, etc.)
            gender: Gender preference (MALE, FEMALE, NEUTRAL)

        Returns:
            VoiceCharacter instance or None if not found
        """
        cache_key = f'voice_char:{character_type}:{language}:{gender}'

        # Try cache first
        cached = cache.get(cache_key)
        if cached:
            return cached

        try:
            # Try to get default character first
            character = VoiceCharacter.objects.filter(
                character_type=character_type,
                language=language,
                gender=gender,
                is_active=True,
                is_default=True
            ).first()

            # If no default, get any active character
            if not character:
                character = VoiceCharacter.objects.filter(
                    character_type=character_type,
                    language=language,
                    gender=gender,
                    is_active=True
                ).first()

            # Cache result
            if character:
                cache.set(cache_key, character, cls.CACHE_TTL)

            return character

        except Exception as e:
            logger.error(f"Error retrieving voice character: {e}")
            return None

    @classmethod
    def get_default_peppi(cls, language: str, gender: str = 'FEMALE') -> Optional[VoiceCharacter]:
        """
        Get default Peppi character for a language.

        Args:
            language: Language code
            gender: Gender preference

        Returns:
            Peppi VoiceCharacter or None
        """
        return cls.get_character('PEPPI', language, gender)

    @classmethod
    def get_ssml_config(cls, character: VoiceCharacter) -> Dict:
        """
        Generate SSML configuration for a voice character.

        Args:
            character: VoiceCharacter instance

        Returns:
            dict: SSML configuration settings
        """
        config = {
            'speaking_rate': character.speaking_rate,
            'pitch': f"{character.pitch:+.1f}st",
            'volume': f"{character.volume_gain_db:+.1f}dB",
            'voice_id': character.voice_id,
            'voice_model': character.voice_model,
            'voice_source': character.voice_source,
        }

        return config

    @classmethod
    def prepare_text_for_character(
        cls,
        text: str,
        character: VoiceCharacter,
        add_warmth: bool = True,
        warmth_category: str = None
    ) -> str:
        """
        Prepare text for a voice character by adding personality touches.

        Args:
            text: Original text to narrate
            character: VoiceCharacter instance
            add_warmth: Whether to add warmth phrases
            warmth_category: Optional category of warmth phrase to add

        Returns:
            str: Enhanced text ready for TTS
        """
        enhanced_text = text

        # Add warmth phrases if enabled
        if add_warmth and character.warmth_phrases:
            phrases = character.get_warmth_phrases(warmth_category)
            if phrases:
                warmth_phrase = random.choice(phrases)

                # Add warmth phrase at the beginning
                if warmth_category in ['greeting', 'intro']:
                    enhanced_text = f"{warmth_phrase} {enhanced_text}"
                # Add at the end
                elif warmth_category in ['encouragement', 'praise']:
                    enhanced_text = f"{enhanced_text} {warmth_phrase}"

        return enhanced_text

    @classmethod
    def get_available_characters(
        cls,
        language: str = None,
        character_type: str = None
    ) -> List[VoiceCharacter]:
        """
        Get list of available voice characters.

        Args:
            language: Optional language filter
            character_type: Optional character type filter

        Returns:
            List of VoiceCharacter instances
        """
        queryset = VoiceCharacter.objects.filter(is_active=True)

        if language:
            queryset = queryset.filter(language=language)

        if character_type:
            queryset = queryset.filter(character_type=character_type)

        return list(queryset.order_by('character_type', 'language', 'gender'))

    @classmethod
    def get_character_by_id(cls, character_id: str) -> Optional[VoiceCharacter]:
        """
        Get voice character by UUID.

        Args:
            character_id: UUID of the character

        Returns:
            VoiceCharacter instance or None
        """
        try:
            return VoiceCharacter.objects.get(id=character_id, is_active=True)
        except VoiceCharacter.DoesNotExist:
            return None

    @classmethod
    def get_voice_config_for_tts(
        cls,
        character_type: str,
        language: str,
        gender: str = 'FEMALE'
    ) -> Optional[Dict]:
        """
        Get TTS-ready voice configuration for a character.

        Args:
            character_type: Character type
            language: Language code
            gender: Gender preference

        Returns:
            dict: TTS configuration or None if character not found
        """
        character = cls.get_character(character_type, language, gender)

        if not character:
            logger.warning(
                f"No voice character found for {character_type}/{language}/{gender}"
            )
            return None

        return character.get_voice_config()
