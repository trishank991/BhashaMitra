"""
BhashaMitra TTS Services

Three-tier TTS architecture:
1. Cache (instant, free)
2. Replicate.com (fast, cheap)
3. Google Cloud TTS (reliable)
4. Svara TTS (legacy fallback)
"""

from apps.speech.services.tts_service import TTSService, TTSServiceError

__all__ = ['TTSService', 'TTSServiceError']
