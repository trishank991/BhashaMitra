"""
Voice profile descriptions for Indic Parler-TTS.
These descriptions control how the generated speech sounds.
Optimized for children's storytelling.
"""

VOICE_PROFILES = {
    'HINDI': {
        'storyteller': (
            "Divya speaks in a warm, cheerful tone with moderate pace, "
            "perfect for storytelling to children. The recording is very high quality "
            "with clear pronunciation and no background noise."
        ),
        'calm': (
            "Ananya speaks in a soft, soothing voice with slow pace, "
            "gentle and calming for bedtime stories. Very clear audio "
            "with peaceful delivery."
        ),
        'enthusiastic': (
            "Rohan speaks with energy and enthusiasm, slightly faster pace, "
            "exciting and engaging for adventure stories. Clear and bright audio "
            "that captures children's attention."
        ),
    },
    'TAMIL': {
        'storyteller': (
            "Priya speaks in a melodic, nurturing voice with clear pronunciation, "
            "ideal for children's stories. The recording has high quality audio "
            "with warm, engaging tone."
        ),
        'calm': (
            "Lakshmi speaks softly with gentle, measured pace, "
            "soothing for young listeners. Clear audio with peaceful intonation."
        ),
        'enthusiastic': (
            "Karthik speaks with vibrant energy and expressive delivery, "
            "captivating for exciting tales. High quality clear audio."
        ),
    },
    'GUJARATI': {
        'storyteller': (
            "A female speaker with warm, friendly tone and clear Gujarati pronunciation, "
            "perfect for children's stories. Very clear high quality audio "
            "with engaging delivery."
        ),
        'calm': (
            "A gentle female voice with soft, measured pace, "
            "calming and soothing for young children. Clear audio."
        ),
        'enthusiastic': (
            "An energetic speaker with lively tone and expressive delivery, "
            "exciting for adventure stories. Bright, clear audio."
        ),
    },
    'PUNJABI': {
        'storyteller': (
            "A warm, friendly voice with clear Punjabi pronunciation and moderate pace, "
            "engaging storytelling style perfect for children. High quality audio "
            "with no background noise."
        ),
        'calm': (
            "A soft, gentle voice with slow, soothing pace, "
            "calming for bedtime stories. Very clear audio."
        ),
        'enthusiastic': (
            "An energetic, expressive voice with lively delivery, "
            "exciting and engaging. Clear, bright audio."
        ),
    },
    'TELUGU': {
        'storyteller': (
            "A melodic female voice with warm tone and clear Telugu pronunciation, "
            "perfect for children's storytelling. High quality recording "
            "with engaging delivery."
        ),
        'calm': (
            "A soft, gentle voice with measured pace, "
            "soothing and calming. Very clear audio."
        ),
        'enthusiastic': (
            "An expressive, energetic voice with lively delivery, "
            "captivating for exciting stories. Clear audio."
        ),
    },
    'MALAYALAM': {
        'storyteller': (
            "A warm, nurturing voice with clear Malayalam pronunciation, "
            "ideal for children's stories. High quality audio "
            "with engaging, friendly tone."
        ),
        'calm': (
            "A soft, gentle voice with slow, peaceful pace, "
            "soothing for young listeners. Clear audio."
        ),
        'enthusiastic': (
            "An energetic, expressive voice with vibrant delivery, "
            "exciting for adventure tales. Bright, clear audio."
        ),
    },
}


def get_voice_description(language: str, style: str = 'storyteller') -> str:
    """
    Get the voice description for TTS generation.

    Args:
        language: Language code (HINDI, TAMIL, etc.)
        style: Voice style (storyteller, calm, enthusiastic)

    Returns:
        Voice description string for Parler-TTS
    """
    lang_profiles = VOICE_PROFILES.get(language, VOICE_PROFILES['HINDI'])
    return lang_profiles.get(style, lang_profiles['storyteller'])


# Recommended voices per language (from Indic Parler-TTS documentation)
RECOMMENDED_VOICES = {
    'HINDI': ['Divya', 'Ananya', 'Rohan', 'Arvind'],
    'TAMIL': ['Priya', 'Lakshmi', 'Karthik', 'Senthil'],
    'GUJARATI': ['Meera', 'Nisha', 'Raj'],
    'PUNJABI': ['Simran', 'Harpreet', 'Gurpreet'],
    'TELUGU': ['Padma', 'Sravani', 'Ravi'],
    'MALAYALAM': ['Sreelakshmi', 'Anitha', 'Vijay'],
}
