"""
Peppi Voice Service - Playful Kitten Voice for BhashaMitra's Mascot

Peppi is a friendly, playful kitten who helps children learn Indian languages.
This service provides a customized voice with:
- Higher pitch for a cute, childlike sound
- Slightly faster speaking rate for energy
- SSML support for expressive speech
- Sound effects integration (meows, giggles)

Voice Settings:
- Pitch: +3.0 (higher = more playful/childlike)
- Speaking Rate: 1.05 (slightly faster = energetic)
- Voice: Female (warmer, friendlier for children)
"""

import os
import logging
from typing import Tuple, Optional, Dict, List
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class PeppiMood(Enum):
    """Peppi's emotional states affect voice parameters."""
    HAPPY = "happy"           # Excited, celebrating
    ENCOURAGING = "encouraging"  # Supportive, gentle
    TEACHING = "teaching"     # Clear, patient
    PLAYFUL = "playful"       # Fun, energetic
    PROUD = "proud"           # Congratulatory
    CURIOUS = "curious"       # Questioning, wondering


@dataclass
class PeppiVoiceSettings:
    """Voice configuration for different moods."""
    pitch: float          # -20.0 to +20.0 semitones
    speaking_rate: float  # 0.25 to 4.0
    volume_gain_db: float # -96.0 to +16.0


# Mood-based voice settings
# Optimized for Indian diaspora children learning languages abroad
# Key priorities: SLOW for clarity, WARM for engagement, ENERGETIC for fun
PEPPI_MOOD_SETTINGS: Dict[PeppiMood, PeppiVoiceSettings] = {
    PeppiMood.HAPPY: PeppiVoiceSettings(
        pitch=1.5,           # Warm, natural pitch
        speaking_rate=0.80,  # Slow for diaspora learners
        volume_gain_db=2.0,  # Energetic, louder
    ),
    PeppiMood.ENCOURAGING: PeppiVoiceSettings(
        pitch=1.0,           # Warm, supportive
        speaking_rate=0.75,  # Very slow, gentle
        volume_gain_db=1.0,  # Warm presence
    ),
    PeppiMood.TEACHING: PeppiVoiceSettings(
        pitch=0.5,           # Clear, natural
        speaking_rate=0.70,  # Slowest for learning content
        volume_gain_db=0.0,  # Normal volume
    ),
    PeppiMood.PLAYFUL: PeppiVoiceSettings(
        pitch=2.0,           # Fun, slightly higher
        speaking_rate=0.85,  # Slow but energetic
        volume_gain_db=2.0,  # Energetic volume
    ),
    PeppiMood.PROUD: PeppiVoiceSettings(
        pitch=1.5,           # Celebratory warmth
        speaking_rate=0.80,  # Clear celebration
        volume_gain_db=3.0,  # Extra emphasis for achievement
    ),
    PeppiMood.CURIOUS: PeppiVoiceSettings(
        pitch=2.0,           # Inquisitive, friendly
        speaking_rate=0.80,  # Slow questioning
        volume_gain_db=1.0,
    ),
}

# Default Peppi settings (warm, slow for diaspora learners)
DEFAULT_PEPPI_SETTINGS = PeppiVoiceSettings(
    pitch=1.5,           # Warm, friendly
    speaking_rate=0.80,  # Slow for clarity
    volume_gain_db=1.5,  # Energetic presence
)


class PeppiVoiceService:
    """
    Dedicated voice service for Peppi the kitten mascot.

    Uses Google Cloud TTS with customized settings for a playful,
    child-friendly voice character.
    """

    # Peppi's preferred voices by language
    PEPPI_VOICES = {
        'HINDI': {
            'standard': 'hi-IN-Standard-A',   # Female, child-friendly
            'wavenet': 'hi-IN-Wavenet-A',     # Premium female
        },
        'TAMIL': {
            'standard': 'ta-IN-Standard-A',
            'wavenet': 'ta-IN-Wavenet-A',
        },
        'TELUGU': {
            'standard': 'te-IN-Standard-A',
            'wavenet': None,  # Not available
        },
        'GUJARATI': {
            'standard': 'gu-IN-Standard-A',
            'wavenet': 'gu-IN-Wavenet-A',
        },
        'MALAYALAM': {
            'standard': 'ml-IN-Standard-A',
            'wavenet': 'ml-IN-Wavenet-A',
        },
        'PUNJABI': {
            'standard': 'pa-IN-Standard-A',
            'wavenet': 'pa-IN-Wavenet-A',
        },
        'BENGALI': {
            'standard': 'bn-IN-Standard-A',
            'wavenet': 'bn-IN-Wavenet-A',
        },
        'KANNADA': {
            'standard': 'kn-IN-Standard-A',
            'wavenet': 'kn-IN-Wavenet-A',
        },
        'MARATHI': {
            'standard': 'mr-IN-Standard-A',
            'wavenet': 'mr-IN-Wavenet-A',
        },
    }

    # Language codes for Google TTS
    LANGUAGE_CODES = {
        'HINDI': 'hi-IN',
        'TAMIL': 'ta-IN',
        'TELUGU': 'te-IN',
        'GUJARATI': 'gu-IN',
        'MALAYALAM': 'ml-IN',
        'PUNJABI': 'pa-IN',
        'BENGALI': 'bn-IN',
        'KANNADA': 'kn-IN',
        'MARATHI': 'mr-IN',
    }

    @classmethod
    def speak(
        cls,
        text: str,
        language: str = 'HINDI',
        mood: PeppiMood = PeppiMood.PLAYFUL,
        use_wavenet: bool = False,
    ) -> Tuple[bytes, int]:
        """
        Generate Peppi's voice for the given text.

        Args:
            text: Text for Peppi to speak
            language: Language code (HINDI, TAMIL, etc.)
            mood: Peppi's emotional state
            use_wavenet: Use premium WaveNet voice (PREMIUM tier)

        Returns:
            Tuple of (audio_bytes, duration_ms)
        """
        try:
            from google.cloud import texttospeech
        except ImportError:
            raise RuntimeError("google-cloud-texttospeech not installed")

        settings = PEPPI_MOOD_SETTINGS.get(mood, DEFAULT_PEPPI_SETTINGS)
        voice_config = cls.PEPPI_VOICES.get(language, cls.PEPPI_VOICES['HINDI'])
        language_code = cls.LANGUAGE_CODES.get(language, 'hi-IN')

        # Select voice (WaveNet for premium, Standard otherwise)
        if use_wavenet and voice_config.get('wavenet'):
            voice_name = voice_config['wavenet']
        else:
            voice_name = voice_config['standard']

        logger.info(f"Peppi speaking ({mood.value}): '{text[:50]}...' in {language}")

        client = texttospeech.TextToSpeechClient()

        # Use SSML for more expressive speech
        ssml_text = cls._wrap_in_ssml(text, mood)

        synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name=voice_name,
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=settings.speaking_rate,
            pitch=settings.pitch,
            volume_gain_db=settings.volume_gain_db,
            sample_rate_hertz=24000,
            effects_profile_id=['small-bluetooth-speaker-class-device'],
        )

        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config,
        )

        audio_bytes = response.audio_content
        duration_ms = int((len(audio_bytes) / 3000) * 1000)  # Estimate

        logger.info(f"Peppi generated {len(audio_bytes)} bytes, ~{duration_ms}ms")

        return audio_bytes, duration_ms

    @classmethod
    def _wrap_in_ssml(cls, text: str, mood: PeppiMood) -> str:
        """
        Wrap text in SSML for more expressive speech.

        SSML (Speech Synthesis Markup Language) allows:
        - Emphasis on words
        - Pauses for dramatic effect
        - Pronunciation hints
        """
        # Add emphasis and expression based on mood
        if mood == PeppiMood.HAPPY:
            # Excited emphasis
            ssml = f'<speak><prosody rate="fast" pitch="+2st">{text}</prosody></speak>'
        elif mood == PeppiMood.ENCOURAGING:
            # Gentle, supportive
            ssml = f'<speak><prosody rate="slow" pitch="+1st">{text}</prosody></speak>'
        elif mood == PeppiMood.TEACHING:
            # Clear with pauses
            ssml = f'<speak><prosody rate="slow">{text}</prosody></speak>'
        elif mood == PeppiMood.PROUD:
            # Celebratory
            ssml = f'<speak><emphasis level="strong">{text}</emphasis></speak>'
        elif mood == PeppiMood.CURIOUS:
            # Rising intonation (question-like)
            ssml = f'<speak><prosody pitch="+3st">{text}</prosody></speak>'
        else:
            # Playful default
            ssml = f'<speak>{text}</speak>'

        return ssml

    @classmethod
    def get_greeting(cls, child_name: str, language: str = 'HINDI') -> str:
        """Get a personalized greeting from Peppi."""
        greetings = PEPPI_PHRASES.get('greetings', {}).get(language, [])
        if greetings:
            import random
            greeting = random.choice(greetings)
            return greeting.replace('{name}', child_name)
        return f"Hello {child_name}!"

    @classmethod
    def get_encouragement(cls, language: str = 'HINDI') -> str:
        """Get an encouraging phrase from Peppi."""
        phrases = PEPPI_PHRASES.get('encouragement', {}).get(language, [])
        if phrases:
            import random
            return random.choice(phrases)
        return "Keep trying, you're doing great!"

    @classmethod
    def get_celebration(cls, language: str = 'HINDI') -> str:
        """Get a celebration phrase from Peppi."""
        phrases = PEPPI_PHRASES.get('celebration', {}).get(language, [])
        if phrases:
            import random
            return random.choice(phrases)
        return "Wonderful! You did it!"

    @classmethod
    def get_teaching_intro(cls, topic: str, language: str = 'HINDI') -> str:
        """Get a teaching introduction from Peppi."""
        intros = PEPPI_PHRASES.get('teaching_intro', {}).get(language, [])
        if intros:
            import random
            intro = random.choice(intros)
            return intro.replace('{topic}', topic)
        return f"Let's learn about {topic} together!"


# ============================================
# PEPPI'S PHRASE LIBRARY
# ============================================
# Organized by category and language
# These can be pre-cached for instant playback

PEPPI_PHRASES = {
    # Greetings (use {name} placeholder for child's name)
    'greetings': {
        'HINDI': [
            "नमस्ते दोस्त! मैं पेप्पी हूँ, चलो मज़े से सीखते हैं!",
            "अरे वाह, मेरे दोस्त {name} आ गए! चलो आज कुछ नया सीखें!",
            "हेलो दोस्त! आज हम साथ में खेलेंगे और सीखेंगे!",
            "{name}, स्वागत है! मैं तुम्हारा दोस्त पेप्पी!",
            "कैसे हो दोस्त? चलो मिलकर हिंदी सीखें!",
            "नमस्ते {name}! तुम मेरे सबसे अच्छे दोस्त हो!",
        ],
        'TAMIL': [
            "வணக்கம் {name}! நான் பெப்பி, சேர்ந்து கற்போம்!",
            "{name}, வரவேற்கிறேன்! இன்று என்ன கற்போம்?",
        ],
        'TELUGU': [
            "నమస్కారం {name}! నేను పెప్పీ, కలిసి నేర్చుకుందాం!",
        ],
        'GUJARATI': [
            "નમસ્તે {name}! હું પેપ્પી છું, ચાલો શીખીએ!",
        ],
    },

    # Encouragement phrases
    'encouragement': {
        'HINDI': [
            "शाबाश! बहुत अच्छा!",
            "वाह, तुम तो बहुत होशियार हो!",
            "बहुत बढ़िया, कोशिश करते रहो!",
            "अरे वाह! तुमने तो कमाल कर दिया!",
            "एकदम सही! ऐसे ही करते रहो!",
            "तुम सीख रहे हो, यह बहुत अच्छी बात है!",
            "गलती होती है, कोई बात नहीं, फिर से कोशिश करो!",
            "धीरे-धीरे सीखोगे, मैं तुम्हारे साथ हूँ!",
        ],
        'TAMIL': [
            "மிகவும் நன்று!",
            "அருமை! நீ சிறந்த மாணவன்!",
            "நன்றாக முயற்சி செய்கிறாய்!",
        ],
        'TELUGU': [
            "చాలా బాగుంది!",
            "అద్భుతం! నువ్వు చాలా తెలివైనవాడివి!",
        ],
        'GUJARATI': [
            "ખૂબ સરસ!",
            "વાહ! તું ખૂબ હોશિયાર છે!",
        ],
    },

    # Celebration phrases (correct answer, level up, etc.)
    'celebration': {
        'HINDI': [
            "यह रहा! तुमने कर दिखाया!",
            "वाह वाह वाह! एकदम सही!",
            "बधाई हो! तुम चैंपियन हो!",
            "क्या बात है! शानदार!",
            "हुर्रे! तुमने जीत लिया!",
            "तुम तो सुपरस्टार हो!",
            "जोरदार! मुझे तुम पर गर्व है!",
        ],
        'TAMIL': [
            "வாழ்த்துக்கள்! நீ சாம்பியன்!",
            "அற்புதம்! மிகவும் நன்றாக செய்தாய்!",
        ],
        'TELUGU': [
            "అభినందనలు! నువ్వు చాంపియన్!",
            "అద్భుతం! చాలా బాగా చేశావు!",
        ],
        'GUJARATI': [
            "અભિનંદન! તું ચેમ્પિયન છે!",
            "વાહ! ખૂબ સરસ કર્યું!",
        ],
    },

    # Teaching introductions (use {topic} placeholder)
    'teaching_intro': {
        'HINDI': [
            "चलो आज {topic} सीखते हैं!",
            "आज हम {topic} के बारे में जानेंगे!",
            "क्या तुम {topic} सीखने के लिए तैयार हो?",
            "आओ, मैं तुम्हें {topic} सिखाता हूँ!",
            "{topic} बहुत मज़ेदार है, देखो!",
        ],
        'TAMIL': [
            "இன்று {topic} கற்போம்!",
            "{topic} பற்றி தெரிந்துகொள்வோம்!",
        ],
        'TELUGU': [
            "ఈ రోజు {topic} నేర్చుకుందాం!",
        ],
        'GUJARATI': [
            "ચાલો આજે {topic} શીખીએ!",
        ],
    },

    # Goodbye phrases
    'goodbye': {
        'HINDI': [
            "बाय बाय! कल फिर मिलेंगे!",
            "अलविदा! तुम बहुत अच्छे हो!",
            "चलता हूँ, फिर मिलेंगे!",
            "बाय! मज़ा आया तुम्हारे साथ!",
        ],
        'TAMIL': [
            "பை பை! நாளை சந்திப்போம்!",
        ],
        'TELUGU': [
            "బై బై! రేపు కలుద్దాం!",
        ],
        'GUJARATI': [
            "બાય બાય! કાલે મળીશું!",
        ],
    },

    # Alphabet/Letter teaching
    'letter_teaching': {
        'HINDI': [
            "यह है '{letter}', इसे ऐसे बोलते हैं...",
            "देखो यह अक्षर '{letter}', मेरे साथ बोलो!",
            "'{letter}' को ध्यान से देखो और सुनो!",
        ],
    },

    # Word teaching
    'word_teaching': {
        'HINDI': [
            "यह शब्द है '{word}', इसका मतलब है {meaning}",
            "'{word}' बोलो मेरे साथ!",
            "सुनो ध्यान से: {word}",
        ],
    },

    # Story narration intros
    'story_intro': {
        'HINDI': [
            "चलो एक मज़ेदार कहानी सुनते हैं!",
            "आज की कहानी बहुत अच्छी है, सुनो!",
            "एक बार की बात है...",
            "यह कहानी तुम्हें बहुत पसंद आएगी!",
        ],
        'TAMIL': [
            "ஒரு சுவாரஸ்யமான கதை கேட்போம்!",
        ],
    },

    # Hints when child is stuck
    'hints': {
        'HINDI': [
            "एक छोटा सा संकेत... ध्यान से सोचो!",
            "हिंट लो: पहला अक्षर है...",
            "कोई बात नहीं, मैं मदद करता हूँ!",
        ],
    },

    # Wrong answer responses (gentle)
    'wrong_answer': {
        'HINDI': [
            "अरे, ज़रा फिर से कोशिश करो!",
            "लगभग सही था! एक बार और!",
            "कोई बात नहीं, गलती से सीखते हैं!",
            "हम्म, यह नहीं था, फिर से देखो!",
        ],
        'TAMIL': [
            "பரவாயில்லை, மீண்டும் முயற்சி செய்!",
        ],
    },

    # Peppi's fun expressions
    'expressions': {
        'HINDI': [
            "म्याऊं!",  # Meow
            "हाहाहा!",  # Laughter
            "वाह!",
            "अरे वाह!",
            "हुर्रे!",
            "यीहा!",
        ],
    },
}


# ============================================
# SOUND EFFECTS CONFIGURATION
# ============================================
# Placeholder for sound effect files
# These should be short audio clips (< 1 second)

PEPPI_SOUND_EFFECTS = {
    'meow_happy': 'peppi_sounds/meow_happy.mp3',
    'meow_curious': 'peppi_sounds/meow_curious.mp3',
    'meow_excited': 'peppi_sounds/meow_excited.mp3',
    'giggle': 'peppi_sounds/giggle.mp3',
    'cheer': 'peppi_sounds/cheer.mp3',
    'purr': 'peppi_sounds/purr.mp3',
    'sparkle': 'peppi_sounds/sparkle.mp3',  # Achievement sound
    'whoosh': 'peppi_sounds/whoosh.mp3',    # Transition sound
}


def get_peppi_phrase(category: str, language: str = 'HINDI', **kwargs) -> str:
    """
    Get a random phrase from Peppi's phrase library.

    Args:
        category: Phrase category (greetings, encouragement, etc.)
        language: Language code
        **kwargs: Placeholder values (name, topic, letter, word, meaning)

    Returns:
        Formatted phrase string
    """
    import random

    phrases = PEPPI_PHRASES.get(category, {}).get(language, [])
    if not phrases:
        # Fallback to Hindi if language not available
        phrases = PEPPI_PHRASES.get(category, {}).get('HINDI', [])

    if not phrases:
        return ""

    phrase = random.choice(phrases)

    # Replace placeholders
    for key, value in kwargs.items():
        phrase = phrase.replace(f'{{{key}}}', str(value))

    return phrase
