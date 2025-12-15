"""
Bhashini API client.

DEPRECATED: This client is no longer used. BhashaMitra now uses Hugging Face's
AI4Bharat Indic Parler-TTS for text-to-speech. See:
- apps/speech/services/tts_service.py
- external/huggingface/inference_client.py

This file is kept for reference only. To use Bhashini as a fallback,
you would need to configure BHASHINI_USER_ID and BHASHINI_API_KEY in .env.
"""
import warnings
import requests
import logging
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

warnings.warn(
    "BhashiniClient is deprecated. Use TTSService from apps.speech.services.tts_service instead.",
    DeprecationWarning,
    stacklevel=2
)


class BhashiniClient:
    """Client for Bhashini speech services."""

    LANGUAGE_CODES = {
        'HINDI': 'hi',
        'TAMIL': 'ta',
        'GUJARATI': 'gu',
        'PUNJABI': 'pa',
        'TELUGU': 'te',
        'MALAYALAM': 'ml',
    }

    def __init__(self):
        self.user_id = getattr(settings, 'BHASHINI_USER_ID', '')
        self.api_key = getattr(settings, 'BHASHINI_API_KEY', '')
        self.auth_url = getattr(settings, 'BHASHINI_AUTH_URL', 'https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline')
        self._pipeline_cache = {}

    def text_to_speech(self, text: str, language: str) -> dict:
        """Convert text to speech."""
        lang_code = self.LANGUAGE_CODES.get(language, language.lower())

        # Get TTS pipeline
        pipeline = self._get_pipeline('tts', lang_code)
        if not pipeline:
            raise Exception(f"No TTS pipeline available for {language}")

        # Make TTS request
        headers = {
            'Content-Type': 'application/json',
            'Authorization': pipeline.get('authorizationKey', self.api_key),
        }

        payload = {
            'pipelineTasks': [{
                'taskType': 'tts',
                'config': {
                    'language': {'sourceLanguage': lang_code},
                    'gender': 'female',
                }
            }],
            'inputData': {
                'input': [{'source': text}]
            }
        }

        response = requests.post(
            pipeline.get('callbackUrl'),
            json=payload,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()

        data = response.json()
        audio_content = data.get('pipelineResponse', [{}])[0].get('audio', [{}])[0].get('audioContent')

        return {'audio_content': audio_content}

    def speech_to_text(self, audio_base64: str, language: str) -> dict:
        """Convert speech to text."""
        lang_code = self.LANGUAGE_CODES.get(language, language.lower())

        # Get ASR pipeline
        pipeline = self._get_pipeline('asr', lang_code)
        if not pipeline:
            raise Exception(f"No ASR pipeline available for {language}")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': pipeline.get('authorizationKey', self.api_key),
        }

        payload = {
            'pipelineTasks': [{
                'taskType': 'asr',
                'config': {
                    'language': {'sourceLanguage': lang_code},
                }
            }],
            'inputData': {
                'audio': [{'audioContent': audio_base64}]
            }
        }

        response = requests.post(
            pipeline.get('callbackUrl'),
            json=payload,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()

        data = response.json()
        result = data.get('pipelineResponse', [{}])[0].get('output', [{}])[0]

        return {
            'transcription': result.get('source', ''),
            'confidence': result.get('confidence', 0),
        }

    def _get_pipeline(self, task_type: str, language: str) -> dict:
        """Get pipeline configuration from Bhashini."""
        cache_key = f"bhashini_pipeline_{task_type}_{language}"

        cached = cache.get(cache_key)
        if cached:
            return cached

        headers = {
            'Content-Type': 'application/json',
            'userID': self.user_id,
            'ulcaApiKey': self.api_key,
        }

        payload = {
            'pipelineTasks': [{
                'taskType': task_type,
                'config': {
                    'language': {'sourceLanguage': language}
                }
            }],
            'pipelineRequestConfig': {
                'pipelineId': '64392f96daac500b55c543cd'  # Official Bhashini pipeline
            }
        }

        try:
            response = requests.post(
                self.auth_url,
                json=payload,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()
            pipeline = {
                'callbackUrl': data.get('pipelineInferenceAPIEndPoint', {}).get('callbackUrl'),
                'authorizationKey': data.get('pipelineInferenceAPIEndPoint', {}).get(
                    'inferenceApiKey', {}
                ).get('value'),
            }

            cache_timeout = getattr(settings, 'CACHE_TIMEOUT_PIPELINE', 3600)
            cache.set(cache_key, pipeline, cache_timeout)
            return pipeline

        except Exception as e:
            logger.error(f"Failed to get Bhashini pipeline: {e}")
            return None
