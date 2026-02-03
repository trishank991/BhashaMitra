"""Speech services - Bhashini API integration."""
import base64
import hashlib
import logging
import requests
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)


class BhashiniService:
    """Service for Bhashini TTS/STT APIs (Government of India).

    Bhashini provides free speech services for 22 Indian languages.
    Apply for API access at: https://bhashini.gov.in/
    """

    AUTH_URL = 'https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline'
    COMPUTE_URL = 'https://dhruva-api.bhashini.gov.in/services/inference/pipeline'

    # Language code mapping (our codes -> Bhashini codes)
    LANGUAGE_CODES = {
        'HINDI': 'hi',
        'TAMIL': 'ta',
        'GUJARATI': 'gu',
        'PUNJABI': 'pa',
        'TELUGU': 'te',
        'MALAYALAM': 'ml',
        'MARATHI': 'mr',
        'BENGALI': 'bn',
        'KANNADA': 'kn',
        'URDU': 'ur',
    }

    def __init__(self):
        self.user_id = settings.BHASHINI_USER_ID
        self.api_key = settings.BHASHINI_API_KEY
        self.session = requests.Session()

    def _get_pipeline_config(self, task_type, language):
        """Get pipeline configuration from Bhashini."""
        cache_key = f"bhashini_pipeline_{task_type}_{language}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        lang_code = self.LANGUAGE_CODES.get(language, 'hi')

        try:
            if task_type == 'tts':
                payload = {
                    "pipelineTasks": [
                        {"taskType": "tts", "config": {"language": {"sourceLanguage": lang_code}}}
                    ],
                    "pipelineRequestConfig": {"pipelineId": "64392f96daac500b55c543cd"}
                }
            else:  # asr (STT)
                payload = {
                    "pipelineTasks": [
                        {"taskType": "asr", "config": {"language": {"sourceLanguage": lang_code}}}
                    ],
                    "pipelineRequestConfig": {"pipelineId": "64392f96daac500b55c543cd"}
                }

            response = self.session.post(
                self.AUTH_URL,
                json=payload,
                headers={
                    'Content-Type': 'application/json',
                    'ulcaApiKey': self.api_key,
                    'userID': self.user_id,
                },
                timeout=10
            )
            response.raise_for_status()

            config = response.json()
            cache.set(cache_key, config, settings.CACHE_TIMEOUT_PIPELINE)
            return config

        except requests.RequestException as e:
            logger.error(f"Bhashini pipeline error: {e}")
            return None

    def text_to_speech(self, text, language='HINDI', voice='female', speed=1.0):
        """Convert text to speech.

        Args:
            text: Text to convert
            language: Language code (e.g., 'HINDI', 'TAMIL')
            voice: 'male' or 'female'
            speed: Speech speed (0.5 to 2.0)

        Returns:
            dict with audio_url or audio_base64, duration, and cached flag
        """
        # Check cache first
        cache_key = self._get_tts_cache_key(text, language, voice, speed)
        cached = cache.get(cache_key)
        if cached:
            return {**cached, 'cached': True}

        # Get pipeline config
        config = self._get_pipeline_config('tts', language)
        if not config:
            return {'error': 'Failed to get TTS pipeline configuration'}

        try:
            pipeline_info = config.get('pipelineResponseConfig', [{}])[0]
            service_id = pipeline_info.get('config', [{}])[0].get('serviceId', '')

            lang_code = self.LANGUAGE_CODES.get(language, 'hi')

            payload = {
                "pipelineTasks": [{
                    "taskType": "tts",
                    "config": {
                        "language": {"sourceLanguage": lang_code},
                        "gender": voice,
                        "samplingRate": 16000,
                    }
                }],
                "inputData": {
                    "input": [{"source": text}]
                }
            }

            # Get compute URL from config
            callback_url = config.get('pipelineInferenceAPIEndPoint', {}).get('callbackUrl', self.COMPUTE_URL)
            auth_key = config.get('pipelineInferenceAPIEndPoint', {}).get('inferenceApiKey', {}).get('value', '')

            response = self.session.post(
                callback_url,
                json=payload,
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': auth_key,
                },
                timeout=30
            )
            response.raise_for_status()

            result = response.json()
            audio_content = result.get('pipelineResponse', [{}])[0].get('audio', [{}])[0]
            audio_base64 = audio_content.get('audioContent', '')

            output = {
                'audio_base64': audio_base64,
                'audio_url': f"data:audio/wav;base64,{audio_base64}",
                'duration_seconds': len(base64.b64decode(audio_base64)) / (16000 * 2) if audio_base64 else 0,
                'cached': False,
            }

            # Cache the result
            cache.set(cache_key, output, settings.CACHE_TIMEOUT_TTS)
            return output

        except requests.RequestException as e:
            logger.error(f"Bhashini TTS error: {e}")
            return {'error': f'TTS service unavailable: {str(e)}'}
        except Exception as e:
            logger.error(f"Bhashini TTS processing error: {e}")
            return {'error': f'TTS processing error: {str(e)}'}

    def speech_to_text(self, audio_url=None, audio_base64=None, language='HINDI'):
        """Convert speech to text.

        Args:
            audio_url: URL of audio file
            audio_base64: Base64 encoded audio
            language: Language code

        Returns:
            dict with transcription and confidence
        """
        # Get audio content
        if audio_url and not audio_base64:
            try:
                response = requests.get(audio_url, timeout=10)
                audio_base64 = base64.b64encode(response.content).decode('utf-8')
            except Exception as e:
                return {'error': f'Failed to fetch audio: {str(e)}'}

        if not audio_base64:
            return {'error': 'No audio content provided'}

        # Get pipeline config
        config = self._get_pipeline_config('asr', language)
        if not config:
            return {'error': 'Failed to get STT pipeline configuration'}

        try:
            lang_code = self.LANGUAGE_CODES.get(language, 'hi')

            payload = {
                "pipelineTasks": [{
                    "taskType": "asr",
                    "config": {
                        "language": {"sourceLanguage": lang_code},
                        "audioFormat": "wav",
                        "samplingRate": 16000,
                    }
                }],
                "inputData": {
                    "audio": [{"audioContent": audio_base64}]
                }
            }

            callback_url = config.get('pipelineInferenceAPIEndPoint', {}).get('callbackUrl', self.COMPUTE_URL)
            auth_key = config.get('pipelineInferenceAPIEndPoint', {}).get('inferenceApiKey', {}).get('value', '')

            response = self.session.post(
                callback_url,
                json=payload,
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': auth_key,
                },
                timeout=30
            )
            response.raise_for_status()

            result = response.json()
            output = result.get('pipelineResponse', [{}])[0].get('output', [{}])[0]

            return {
                'transcription': output.get('source', ''),
                'confidence': output.get('confidence', 0.0),
            }

        except requests.RequestException as e:
            logger.error(f"Bhashini STT error: {e}")
            return {'error': f'STT service unavailable: {str(e)}'}
        except Exception as e:
            logger.error(f"Bhashini STT processing error: {e}")
            return {'error': f'STT processing error: {str(e)}'}

    def compare_pronunciation(self, transcription, expected_text, language='HINDI'):
        """Compare transcription with expected text for pronunciation scoring.

        Args:
            transcription: What the user actually said (from STT)
            expected_text: What they should have said
            language: Language code

        Returns:
            dict with accuracy_score, feedback, and word_scores
        """
        # Normalize texts
        trans_words = transcription.strip().split()
        expected_words = expected_text.strip().split()

        if not trans_words or not expected_words:
            return {
                'accuracy_score': 0.0,
                'feedback': 'Could not process the pronunciation',
                'word_scores': [],
            }

        # Simple word-by-word comparison
        word_scores = []
        correct_count = 0

        for i, expected in enumerate(expected_words):
            if i < len(trans_words):
                actual = trans_words[i]
                # Simple match (could be enhanced with phonetic comparison)
                is_correct = actual.lower() == expected.lower()
                score = 1.0 if is_correct else 0.0

                word_scores.append({
                    'word': expected,
                    'spoken': actual,
                    'score': score,
                    'correct': is_correct,
                })

                if is_correct:
                    correct_count += 1
            else:
                word_scores.append({
                    'word': expected,
                    'spoken': '',
                    'score': 0.0,
                    'correct': False,
                })

        accuracy = (correct_count / len(expected_words)) * 100 if expected_words else 0

        # Generate feedback
        if accuracy >= 90:
            feedback = "Excellent pronunciation! Keep up the great work!"
        elif accuracy >= 70:
            feedback = "Good job! Practice the highlighted words a bit more."
        elif accuracy >= 50:
            feedback = "Nice effort! Try speaking a little slower and clearer."
        else:
            feedback = "Keep practicing! Listen to the audio again and try to match the sounds."

        return {
            'accuracy_score': round(accuracy, 2),
            'feedback': feedback,
            'word_scores': word_scores,
        }

    def get_available_voices(self):
        """Get available TTS voices for each language."""
        return {
            'HINDI': [
                {'id': 'female', 'name': 'Female', 'default': True},
                {'id': 'male', 'name': 'Male', 'default': False},
            ],
            'TAMIL': [
                {'id': 'female', 'name': 'Female', 'default': True},
                {'id': 'male', 'name': 'Male', 'default': False},
            ],
            'GUJARATI': [
                {'id': 'female', 'name': 'Female', 'default': True},
                {'id': 'male', 'name': 'Male', 'default': False},
            ],
            # Add more languages as they become available
        }

    def _get_tts_cache_key(self, text, language, voice, speed):
        """Generate cache key for TTS results."""
        content = f"{text}_{language}_{voice}_{speed}"
        return f"tts_{hashlib.md5(content.encode()).hexdigest()}"
