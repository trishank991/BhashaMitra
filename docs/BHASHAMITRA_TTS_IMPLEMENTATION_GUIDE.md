# BhashaMitra TTS Implementation Guide

> **Purpose**: Complete implementation guide for Text-to-Speech using AI4Bharat Indic Parler-TTS
> **Provider**: Hugging Face Inference API (PRO Plan - $9/month)
> **Strategy**: Aggressive caching to support unlimited users
> **NO Bhashini**: This replaces the Bhashini integration entirely

---

## 🎯 Overview

### What We're Building
A high-quality Text-to-Speech system for BhashaMitra that:
- Uses AI4Bharat's Indic Parler-TTS (best quality for Indian languages)
- Caches all audio permanently (generate once, serve forever)
- Supports unlimited users after initial caching
- Costs ~$0.07/month after setup (within $2 PRO credits)

### Why This Approach
| Factor | Decision |
|--------|----------|
| **Quality** | Indic Parler-TTS has warm, natural voices perfect for children |
| **Cost** | $9/month HF PRO covers everything with caching |
| **Simplicity** | No Bhashini registration, no government API dependencies |
| **Reliability** | Hugging Face has 99.9% uptime |
| **Scalability** | Cache-first = unlimited users |

### Supported Languages
- ✅ Hindi (official)
- ✅ Tamil (official)
- ✅ Gujarati (official)
- ✅ Punjabi (unofficial but works)
- ✅ Telugu (official)
- ✅ Malayalam (official)

---

## 📁 File Structure

```
bhashamitra-backend/
├── apps/
│   └── speech/
│       ├── __init__.py
│       ├── models.py              # AudioCache model
│       ├── serializers.py
│       ├── views.py               # TTS API endpoints
│       ├── urls.py
│       ├── admin.py
│       ├── services/
│       │   ├── __init__.py
│       │   ├── tts_service.py     # Main TTS service
│       │   ├── cache_service.py   # Audio caching logic
│       │   └── voice_profiles.py  # Voice descriptions
│       └── tests/
│           ├── __init__.py
│           ├── test_tts_service.py
│           └── test_views.py
├── external/
│   └── huggingface/
│       ├── __init__.py
│       └── inference_client.py    # HF API client
└── scripts/
    └── prewarm_tts_cache.py       # Pre-generate all story audio
```

---

## 🔧 Dependencies

### Add to requirements/base.txt

```txt
# TTS Dependencies
huggingface-hub>=0.20.0
transformers>=4.36.0
torch>=2.0.0
torchaudio>=2.0.0
soundfile>=0.12.0
numpy>=1.24.0

# Caching
django-redis>=5.4.0
redis>=5.0.0

# Storage (for permanent audio cache)
django-storages>=1.14.0
boto3>=1.34.0  # For S3/R2 compatible storage
```

### Install System Dependencies (Dockerfile)

```dockerfile
# Add to Dockerfile
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*
```

---

## ⚙️ Configuration

### Environment Variables

```bash
# .env - Add these variables

# Hugging Face (PRO Account - $9/month)
HUGGINGFACE_API_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
HUGGINGFACE_ACCOUNT_TYPE=pro  # 'free' or 'pro'

# Redis Cache
REDIS_URL=redis://localhost:6379/0

# Audio Storage (Cloudflare R2 or S3)
AUDIO_STORAGE_BACKEND=storages.backends.s3boto3.S3Boto3Storage
AWS_ACCESS_KEY_ID=your_r2_access_key
AWS_SECRET_ACCESS_KEY=your_r2_secret_key
AWS_STORAGE_BUCKET_NAME=bhashamitra-audio
AWS_S3_ENDPOINT_URL=https://xxxx.r2.cloudflarestorage.com
AWS_S3_REGION_NAME=auto
AWS_DEFAULT_ACL=public-read
AWS_QUERYSTRING_AUTH=False

# TTS Settings
TTS_CACHE_TTL_SECONDS=86400  # 24 hours in Redis
TTS_DEFAULT_VOICE_STYLE=storyteller
TTS_ENABLE_PREWARMING=true
```

### Django Settings

```python
# config/settings/base.py

# =============================================================================
# HUGGING FACE CONFIGURATION
# =============================================================================

HUGGINGFACE_API_TOKEN = os.getenv('HUGGINGFACE_API_TOKEN')
HUGGINGFACE_ACCOUNT_TYPE = os.getenv('HUGGINGFACE_ACCOUNT_TYPE', 'pro')

# Model to use for TTS
TTS_MODEL_ID = 'ai4bharat/indic-parler-tts'

# =============================================================================
# CACHING CONFIGURATION
# =============================================================================

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'bhashamitra',
    }
}

# TTS specific cache settings
TTS_CACHE_TTL = int(os.getenv('TTS_CACHE_TTL_SECONDS', 86400))  # 24 hours
TTS_DEFAULT_VOICE_STYLE = os.getenv('TTS_DEFAULT_VOICE_STYLE', 'storyteller')

# =============================================================================
# AUDIO STORAGE CONFIGURATION
# =============================================================================

# Use S3/R2 for permanent audio storage
AUDIO_STORAGE_BACKEND = os.getenv('AUDIO_STORAGE_BACKEND', 'django.core.files.storage.FileSystemStorage')

if 's3boto3' in AUDIO_STORAGE_BACKEND:
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_ENDPOINT_URL = os.getenv('AWS_S3_ENDPOINT_URL')
    AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'auto')
    AWS_DEFAULT_ACL = os.getenv('AWS_DEFAULT_ACL', 'public-read')
    AWS_QUERYSTRING_AUTH = os.getenv('AWS_QUERYSTRING_AUTH', 'False').lower() == 'true'
    AWS_S3_CUSTOM_DOMAIN = os.getenv('AWS_S3_CUSTOM_DOMAIN')  # Optional CDN

# =============================================================================
# RATE LIMITING FOR TTS
# =============================================================================

REST_FRAMEWORK = {
    # ... existing settings ...
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '1000/hour',
        'tts': '100/hour',  # TTS specific limit
        'tts_burst': '10/minute',  # Burst protection
    }
}
```

---

## 📦 Models

### Audio Cache Model

```python
# apps/speech/models.py

import uuid
from django.db import models
from apps.core.models import TimeStampedModel


class AudioCache(TimeStampedModel):
    """
    Permanent cache for generated TTS audio files.
    Once generated, audio is stored forever and served from cache.
    """
    
    class Language(models.TextChoices):
        HINDI = 'HINDI', 'Hindi'
        TAMIL = 'TAMIL', 'Tamil'
        GUJARATI = 'GUJARATI', 'Gujarati'
        PUNJABI = 'PUNJABI', 'Punjabi'
        TELUGU = 'TELUGU', 'Telugu'
        MALAYALAM = 'MALAYALAM', 'Malayalam'
    
    class VoiceStyle(models.TextChoices):
        STORYTELLER = 'storyteller', 'Storyteller (Warm & Engaging)'
        CALM = 'calm', 'Calm (Soft & Soothing)'
        ENTHUSIASTIC = 'enthusiastic', 'Enthusiastic (Energetic)'
    
    # Unique identifier for this audio
    cache_key = models.CharField(max_length=64, unique=True, db_index=True)
    
    # Content details
    text_content = models.TextField(help_text="Original text that was converted to speech")
    text_hash = models.CharField(max_length=64, db_index=True, help_text="MD5 hash of text for lookup")
    language = models.CharField(max_length=20, choices=Language.choices)
    voice_style = models.CharField(max_length=20, choices=VoiceStyle.choices, default=VoiceStyle.STORYTELLER)
    
    # Audio file details
    audio_url = models.URLField(help_text="URL to the cached audio file")
    audio_duration_ms = models.IntegerField(default=0, help_text="Duration in milliseconds")
    audio_size_bytes = models.IntegerField(default=0, help_text="File size in bytes")
    audio_format = models.CharField(max_length=10, default='wav')
    
    # Usage tracking
    access_count = models.IntegerField(default=0, help_text="Number of times this audio was accessed")
    last_accessed_at = models.DateTimeField(auto_now=True)
    
    # Generation metadata
    generation_time_ms = models.IntegerField(default=0, help_text="Time taken to generate in ms")
    generation_cost_usd = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    
    # Optional: Link to story page (for pre-warming)
    story = models.ForeignKey(
        'stories.Story',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audio_cache'
    )
    page_number = models.IntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'audio_cache'
        verbose_name = 'Audio Cache'
        verbose_name_plural = 'Audio Cache Entries'
        indexes = [
            models.Index(fields=['language', 'voice_style']),
            models.Index(fields=['story', 'page_number']),
            models.Index(fields=['text_hash']),
        ]
    
    def __str__(self):
        return f"{self.language} - {self.text_content[:50]}..."
    
    def increment_access(self):
        """Increment access count (called when audio is served)"""
        self.access_count += 1
        self.save(update_fields=['access_count', 'last_accessed_at'])


class TTSUsageLog(TimeStampedModel):
    """
    Track TTS API usage for cost monitoring.
    """
    
    class Status(models.TextChoices):
        SUCCESS = 'success', 'Success'
        CACHED = 'cached', 'Served from Cache'
        ERROR = 'error', 'Error'
    
    # Request details
    text_length = models.IntegerField()
    language = models.CharField(max_length=20)
    voice_style = models.CharField(max_length=20)
    
    # Response details
    status = models.CharField(max_length=20, choices=Status.choices)
    was_cached = models.BooleanField(default=False)
    response_time_ms = models.IntegerField(default=0)
    
    # Cost tracking
    estimated_cost_usd = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    
    # Error details (if any)
    error_message = models.TextField(blank=True)
    
    # User tracking (optional)
    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    class Meta:
        db_table = 'tts_usage_log'
        verbose_name = 'TTS Usage Log'
        verbose_name_plural = 'TTS Usage Logs'
```

---

## 🎤 Voice Profiles

```python
# apps/speech/services/voice_profiles.py

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
```

---

## 🔌 Hugging Face Client

```python
# external/huggingface/inference_client.py

"""
Hugging Face Inference API client for TTS.
Uses the PRO account ($9/month) for reliable access.
"""

import os
import time
import logging
import requests
from typing import Optional
from django.conf import settings

logger = logging.getLogger(__name__)


class HuggingFaceInferenceError(Exception):
    """Custom exception for HF API errors"""
    pass


class HuggingFaceClient:
    """
    Client for Hugging Face Inference API.
    
    Pricing (PRO account):
    - $2.00 monthly credits included
    - Pay-as-you-go after credits exhausted
    - ~$0.00012/second for GPU inference
    
    For TTS:
    - ~3 seconds per story page = ~$0.00036 per page
    - With caching, this is a ONE-TIME cost per unique text
    """
    
    BASE_URL = "https://api-inference.huggingface.co/models"
    
    def __init__(self):
        self.api_token = settings.HUGGINGFACE_API_TOKEN
        if not self.api_token:
            raise ValueError("HUGGINGFACE_API_TOKEN not configured")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }
        
        self.model_id = settings.TTS_MODEL_ID
    
    def text_to_speech(
        self,
        text: str,
        description: str,
        max_retries: int = 3,
        timeout: int = 120
    ) -> bytes:
        """
        Generate speech from text using Indic Parler-TTS.
        
        Args:
            text: The text to convert to speech (in target language script)
            description: Voice description (controls voice characteristics)
            max_retries: Number of retry attempts
            timeout: Request timeout in seconds
            
        Returns:
            Audio bytes (WAV format)
            
        Raises:
            HuggingFaceInferenceError: If generation fails
        """
        url = f"{self.BASE_URL}/{self.model_id}"
        
        payload = {
            "inputs": text,
            "parameters": {
                "description": description,
            }
        }
        
        for attempt in range(max_retries):
            try:
                start_time = time.time()
                
                response = requests.post(
                    url,
                    headers=self.headers,
                    json=payload,
                    timeout=timeout
                )
                
                elapsed_ms = int((time.time() - start_time) * 1000)
                
                # Handle rate limiting
                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 60))
                    logger.warning(f"Rate limited. Waiting {retry_after}s...")
                    time.sleep(retry_after)
                    continue
                
                # Handle model loading
                if response.status_code == 503:
                    estimated_time = response.json().get('estimated_time', 30)
                    logger.info(f"Model loading. Waiting {estimated_time}s...")
                    time.sleep(min(estimated_time, 60))
                    continue
                
                # Handle credit exhaustion
                if response.status_code == 402:
                    raise HuggingFaceInferenceError(
                        "Monthly credits exhausted. Upgrade to PRO or wait for reset."
                    )
                
                response.raise_for_status()
                
                logger.info(f"TTS generated in {elapsed_ms}ms for {len(text)} chars")
                return response.content
                
            except requests.exceptions.Timeout:
                logger.warning(f"Timeout on attempt {attempt + 1}/{max_retries}")
                if attempt == max_retries - 1:
                    raise HuggingFaceInferenceError("TTS request timed out")
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed: {e}")
                if attempt == max_retries - 1:
                    raise HuggingFaceInferenceError(f"TTS request failed: {e}")
        
        raise HuggingFaceInferenceError("Max retries exceeded")
    
    def check_model_status(self) -> dict:
        """Check if the TTS model is loaded and ready."""
        url = f"{self.BASE_URL}/{self.model_id}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                return {"status": "ready", "model": self.model_id}
            elif response.status_code == 503:
                data = response.json()
                return {
                    "status": "loading",
                    "estimated_time": data.get('estimated_time', 'unknown'),
                    "model": self.model_id
                }
            else:
                return {"status": "error", "code": response.status_code}
                
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_usage_stats(self) -> dict:
        """
        Get current usage statistics.
        Note: This is approximate - check HF dashboard for exact values.
        """
        # HF doesn't provide a direct API for usage stats
        # This is a placeholder - actual tracking done in TTSUsageLog
        return {
            "account_type": settings.HUGGINGFACE_ACCOUNT_TYPE,
            "model": self.model_id,
            "note": "Check https://huggingface.co/settings/billing for exact usage"
        }
```

---

## 💾 Cache Service

```python
# apps/speech/services/cache_service.py

"""
Audio caching service for TTS.
Implements a two-tier cache:
1. Redis (fast, short-term) - 24 hour TTL
2. S3/R2 (permanent, long-term) - Forever

Strategy: Generate once, cache forever, serve unlimited users.
"""

import hashlib
import logging
import io
from typing import Optional, Tuple
from django.conf import settings
from django.core.cache import cache
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from apps.speech.models import AudioCache

logger = logging.getLogger(__name__)


class AudioCacheService:
    """
    Two-tier caching for TTS audio:
    - Tier 1: Redis (fast, 24h TTL)
    - Tier 2: S3/R2 storage (permanent)
    - Tier 3: Database record (metadata + URL)
    """
    
    REDIS_TTL = settings.TTS_CACHE_TTL  # 24 hours default
    STORAGE_PATH_PREFIX = "audio/tts"
    
    @classmethod
    def _generate_cache_key(cls, text: str, language: str, voice_style: str) -> str:
        """Generate a unique cache key for the text."""
        content = f"{text}:{language}:{voice_style}"
        return hashlib.md5(content.encode()).hexdigest()
    
    @classmethod
    def _generate_text_hash(cls, text: str) -> str:
        """Generate hash of just the text content."""
        return hashlib.md5(text.encode()).hexdigest()
    
    @classmethod
    def get_cached_audio(
        cls,
        text: str,
        language: str,
        voice_style: str = 'storyteller'
    ) -> Tuple[Optional[bytes], bool, Optional[str]]:
        """
        Try to get audio from cache.
        
        Returns:
            Tuple of (audio_bytes, was_cached, audio_url)
            - audio_bytes: The audio data if found, None otherwise
            - was_cached: True if found in any cache tier
            - audio_url: URL to the cached audio (for streaming)
        """
        cache_key = cls._generate_cache_key(text, language, voice_style)
        
        # Tier 1: Check Redis cache (fastest)
        redis_key = f"tts:audio:{cache_key}"
        cached_audio = cache.get(redis_key)
        if cached_audio:
            logger.debug(f"Redis cache hit for {cache_key[:8]}...")
            # Update access count in background
            cls._update_access_count(cache_key)
            return cached_audio, True, None
        
        # Tier 2: Check database for URL (serves from S3/R2)
        try:
            audio_cache = AudioCache.objects.get(cache_key=cache_key)
            
            # Try to get from storage
            storage_path = f"{cls.STORAGE_PATH_PREFIX}/{cache_key}.wav"
            if default_storage.exists(storage_path):
                # Read from storage
                with default_storage.open(storage_path, 'rb') as f:
                    audio_bytes = f.read()
                
                # Warm Redis cache for next request
                cache.set(redis_key, audio_bytes, cls.REDIS_TTL)
                
                # Update access count
                audio_cache.increment_access()
                
                logger.debug(f"Storage cache hit for {cache_key[:8]}...")
                return audio_bytes, True, audio_cache.audio_url
                
        except AudioCache.DoesNotExist:
            pass
        except Exception as e:
            logger.warning(f"Cache lookup error: {e}")
        
        logger.debug(f"Cache miss for {cache_key[:8]}...")
        return None, False, None
    
    @classmethod
    def store_audio(
        cls,
        text: str,
        language: str,
        voice_style: str,
        audio_bytes: bytes,
        generation_time_ms: int = 0,
        story_id: Optional[str] = None,
        page_number: Optional[int] = None
    ) -> AudioCache:
        """
        Store generated audio in all cache tiers.
        
        Args:
            text: Original text
            language: Language code
            voice_style: Voice style used
            audio_bytes: Generated audio data
            generation_time_ms: Time taken to generate
            story_id: Optional story ID (for pre-warming)
            page_number: Optional page number
            
        Returns:
            AudioCache model instance
        """
        cache_key = cls._generate_cache_key(text, language, voice_style)
        text_hash = cls._generate_text_hash(text)
        
        # Tier 1: Store in Redis
        redis_key = f"tts:audio:{cache_key}"
        cache.set(redis_key, audio_bytes, cls.REDIS_TTL)
        
        # Tier 2: Store in S3/R2
        storage_path = f"{cls.STORAGE_PATH_PREFIX}/{cache_key}.wav"
        saved_path = default_storage.save(storage_path, ContentFile(audio_bytes))
        audio_url = default_storage.url(saved_path)
        
        # Calculate estimated cost (~$0.00012/second, assume 3 seconds)
        estimated_cost = 0.00036  # ~3 seconds of GPU time
        
        # Tier 3: Store metadata in database
        audio_cache, created = AudioCache.objects.update_or_create(
            cache_key=cache_key,
            defaults={
                'text_content': text,
                'text_hash': text_hash,
                'language': language,
                'voice_style': voice_style,
                'audio_url': audio_url,
                'audio_size_bytes': len(audio_bytes),
                'audio_format': 'wav',
                'generation_time_ms': generation_time_ms,
                'generation_cost_usd': estimated_cost,
                'story_id': story_id,
                'page_number': page_number,
            }
        )
        
        logger.info(
            f"Cached audio: {cache_key[:8]}... "
            f"({len(audio_bytes)} bytes, {generation_time_ms}ms)"
        )
        
        return audio_cache
    
    @classmethod
    def _update_access_count(cls, cache_key: str):
        """Update access count in background."""
        try:
            AudioCache.objects.filter(cache_key=cache_key).update(
                access_count=models.F('access_count') + 1
            )
        except Exception as e:
            logger.warning(f"Failed to update access count: {e}")
    
    @classmethod
    def get_cache_stats(cls) -> dict:
        """Get cache statistics for monitoring."""
        from django.db.models import Sum, Count, Avg
        
        stats = AudioCache.objects.aggregate(
            total_entries=Count('id'),
            total_size_bytes=Sum('audio_size_bytes'),
            total_cost_usd=Sum('generation_cost_usd'),
            total_accesses=Sum('access_count'),
            avg_generation_time=Avg('generation_time_ms'),
        )
        
        # Calculate savings
        if stats['total_accesses'] and stats['total_entries']:
            cache_hits = stats['total_accesses'] - stats['total_entries']
            savings = cache_hits * 0.00036  # Cost per generation avoided
            stats['estimated_savings_usd'] = round(savings, 4)
        
        return stats
    
    @classmethod
    def get_story_page_audio_url(cls, story_id: str, page_number: int) -> Optional[str]:
        """
        Get the audio URL for a specific story page.
        Useful for pre-loading audio in the frontend.
        """
        try:
            audio_cache = AudioCache.objects.get(
                story_id=story_id,
                page_number=page_number
            )
            return audio_cache.audio_url
        except AudioCache.DoesNotExist:
            return None
```

---

## 🎵 Main TTS Service

```python
# apps/speech/services/tts_service.py

"""
Main TTS service for BhashaMitra.
Uses AI4Bharat Indic Parler-TTS via Hugging Face Inference API.
Implements cache-first strategy for cost optimization.
"""

import time
import logging
from typing import Optional, Tuple
from django.conf import settings

from external.huggingface.inference_client import HuggingFaceClient, HuggingFaceInferenceError
from apps.speech.services.cache_service import AudioCacheService
from apps.speech.services.voice_profiles import get_voice_description
from apps.speech.models import TTSUsageLog

logger = logging.getLogger(__name__)


class TTSServiceError(Exception):
    """Custom exception for TTS service errors"""
    pass


class TTSService:
    """
    Text-to-Speech service for BhashaMitra.
    
    Features:
    - High-quality Indian language TTS (Indic Parler-TTS)
    - Two-tier caching (Redis + S3/R2)
    - Cost tracking and optimization
    - Automatic fallback handling
    
    Usage:
        audio_bytes, was_cached = TTSService.text_to_speech(
            text="नमस्ते बच्चों",
            language="HINDI",
            voice_style="storyteller"
        )
    """
    
    _client: Optional[HuggingFaceClient] = None
    
    @classmethod
    def _get_client(cls) -> HuggingFaceClient:
        """Lazy-load the HF client."""
        if cls._client is None:
            cls._client = HuggingFaceClient()
        return cls._client
    
    @classmethod
    def text_to_speech(
        cls,
        text: str,
        language: str = 'HINDI',
        voice_style: str = 'storyteller',
        user_id: Optional[str] = None,
        story_id: Optional[str] = None,
        page_number: Optional[int] = None,
    ) -> Tuple[bytes, bool]:
        """
        Convert text to speech with automatic caching.
        
        Args:
            text: Text to convert (in target language script)
            language: Language code (HINDI, TAMIL, GUJARATI, PUNJABI, TELUGU, MALAYALAM)
            voice_style: Voice style (storyteller, calm, enthusiastic)
            user_id: Optional user ID for logging
            story_id: Optional story ID for cache association
            page_number: Optional page number for cache association
            
        Returns:
            Tuple of (audio_bytes, was_cached)
            
        Raises:
            TTSServiceError: If TTS generation fails
        """
        start_time = time.time()
        
        # Validate inputs
        if not text or not text.strip():
            raise TTSServiceError("Text cannot be empty")
        
        if len(text) > 5000:
            raise TTSServiceError("Text too long (max 5000 characters)")
        
        # Check cache first (FREE - no API cost!)
        cached_audio, was_cached, audio_url = AudioCacheService.get_cached_audio(
            text=text,
            language=language,
            voice_style=voice_style
        )
        
        if cached_audio:
            # Log cache hit
            cls._log_usage(
                text_length=len(text),
                language=language,
                voice_style=voice_style,
                status='cached',
                was_cached=True,
                response_time_ms=int((time.time() - start_time) * 1000),
                user_id=user_id
            )
            return cached_audio, True
        
        # Generate new audio (COSTS ~$0.00036)
        try:
            client = cls._get_client()
            
            # Get voice description for this language/style
            voice_description = get_voice_description(language, voice_style)
            
            generation_start = time.time()
            audio_bytes = client.text_to_speech(
                text=text,
                description=voice_description
            )
            generation_time_ms = int((time.time() - generation_start) * 1000)
            
            # Store in cache (so we never pay for this text again!)
            AudioCacheService.store_audio(
                text=text,
                language=language,
                voice_style=voice_style,
                audio_bytes=audio_bytes,
                generation_time_ms=generation_time_ms,
                story_id=story_id,
                page_number=page_number
            )
            
            # Log successful generation
            cls._log_usage(
                text_length=len(text),
                language=language,
                voice_style=voice_style,
                status='success',
                was_cached=False,
                response_time_ms=int((time.time() - start_time) * 1000),
                estimated_cost=0.00036,
                user_id=user_id
            )
            
            return audio_bytes, False
            
        except HuggingFaceInferenceError as e:
            # Log error
            cls._log_usage(
                text_length=len(text),
                language=language,
                voice_style=voice_style,
                status='error',
                was_cached=False,
                response_time_ms=int((time.time() - start_time) * 1000),
                error_message=str(e),
                user_id=user_id
            )
            raise TTSServiceError(f"TTS generation failed: {e}")
    
    @classmethod
    def get_story_page_audio(
        cls,
        story_id: str,
        page_number: int,
        text: str,
        language: str,
        voice_style: str = 'storyteller'
    ) -> Tuple[bytes, bool]:
        """
        Get audio for a specific story page.
        Optimized for story reading flow.
        
        Args:
            story_id: Story UUID
            page_number: Page number (1-indexed)
            text: Page text content
            language: Story language
            voice_style: Voice style to use
            
        Returns:
            Tuple of (audio_bytes, was_cached)
        """
        return cls.text_to_speech(
            text=text,
            language=language,
            voice_style=voice_style,
            story_id=story_id,
            page_number=page_number
        )
    
    @classmethod
    def prewarm_story(cls, story_id: str) -> dict:
        """
        Pre-generate and cache all audio for a story.
        Call this when a new story is added to the library.
        
        Args:
            story_id: Story UUID
            
        Returns:
            Summary of pre-warming results
        """
        from apps.stories.models import Story, StoryPage
        
        try:
            story = Story.objects.prefetch_related('pages').get(id=story_id)
        except Story.DoesNotExist:
            raise TTSServiceError(f"Story not found: {story_id}")
        
        results = {
            'story_id': story_id,
            'story_title': story.title,
            'pages_total': story.pages.count(),
            'pages_cached': 0,
            'pages_generated': 0,
            'pages_failed': 0,
            'total_cost_usd': 0,
        }
        
        for page in story.pages.all():
            try:
                _, was_cached = cls.get_story_page_audio(
                    story_id=str(story.id),
                    page_number=page.page_number,
                    text=page.text_content,
                    language=story.language,
                )
                
                if was_cached:
                    results['pages_cached'] += 1
                else:
                    results['pages_generated'] += 1
                    results['total_cost_usd'] += 0.00036
                    
            except Exception as e:
                logger.error(f"Failed to prewarm page {page.page_number}: {e}")
                results['pages_failed'] += 1
        
        return results
    
    @classmethod
    def check_service_status(cls) -> dict:
        """Check if the TTS service is healthy."""
        try:
            client = cls._get_client()
            model_status = client.check_model_status()
            cache_stats = AudioCacheService.get_cache_stats()
            
            return {
                'status': 'healthy',
                'model': model_status,
                'cache': cache_stats
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e)
            }
    
    @classmethod
    def _log_usage(
        cls,
        text_length: int,
        language: str,
        voice_style: str,
        status: str,
        was_cached: bool,
        response_time_ms: int,
        estimated_cost: float = 0,
        error_message: str = '',
        user_id: Optional[str] = None
    ):
        """Log TTS usage for monitoring."""
        try:
            TTSUsageLog.objects.create(
                text_length=text_length,
                language=language,
                voice_style=voice_style,
                status=status,
                was_cached=was_cached,
                response_time_ms=response_time_ms,
                estimated_cost_usd=estimated_cost,
                error_message=error_message,
                user_id=user_id
            )
        except Exception as e:
            logger.warning(f"Failed to log TTS usage: {e}")
```

---

## 🌐 API Views

```python
# apps/speech/views.py

"""
TTS API endpoints for BhashaMitra.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from django.http import HttpResponse
import logging

from apps.speech.services.tts_service import TTSService, TTSServiceError
from apps.speech.services.cache_service import AudioCacheService

logger = logging.getLogger(__name__)


class TextToSpeechView(APIView):
    """
    POST /api/v1/speech/tts/
    
    Generate speech from text. Returns audio file directly.
    
    Request Body:
    {
        "text": "नमस्ते बच्चों, आज हम एक कहानी सुनेंगे",
        "language": "HINDI",
        "voice_style": "storyteller"  // optional
    }
    
    Response: Audio file (WAV format)
    
    Headers in response:
    - X-TTS-Cached: true/false
    - X-TTS-Language: HINDI
    - Content-Type: audio/wav
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'tts'
    
    def post(self, request):
        text = request.data.get('text')
        language = request.data.get('language', 'HINDI')
        voice_style = request.data.get('voice_style', 'storyteller')
        
        # Validation
        if not text:
            return Response(
                {"detail": "Text is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if len(text) > 5000:
            return Response(
                {"detail": "Text too long (max 5000 characters)"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        valid_languages = ['HINDI', 'TAMIL', 'GUJARATI', 'PUNJABI', 'TELUGU', 'MALAYALAM']
        if language not in valid_languages:
            return Response(
                {"detail": f"Invalid language. Must be one of: {valid_languages}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        valid_styles = ['storyteller', 'calm', 'enthusiastic']
        if voice_style not in valid_styles:
            return Response(
                {"detail": f"Invalid voice_style. Must be one of: {valid_styles}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            audio_bytes, was_cached = TTSService.text_to_speech(
                text=text,
                language=language,
                voice_style=voice_style,
                user_id=str(request.user.id)
            )
            
            response = HttpResponse(audio_bytes, content_type='audio/wav')
            response['Content-Disposition'] = 'inline; filename="speech.wav"'
            response['Content-Length'] = len(audio_bytes)
            response['X-TTS-Cached'] = str(was_cached).lower()
            response['X-TTS-Language'] = language
            response['Cache-Control'] = 'public, max-age=86400'  # Browser cache 24h
            
            return response
            
        except TTSServiceError as e:
            logger.error(f"TTS error: {e}")
            return Response(
                {"detail": str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


class StoryPageAudioView(APIView):
    """
    GET /api/v1/stories/{story_id}/pages/{page_number}/audio/
    
    Get audio for a specific story page.
    Optimized for story reading with pre-caching.
    
    Query Parameters:
    - voice_style: storyteller (default), calm, enthusiastic
    
    Response: Audio file (WAV format)
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'tts'
    
    def get(self, request, story_id, page_number):
        from apps.stories.models import Story, StoryPage
        
        voice_style = request.query_params.get('voice_style', 'storyteller')
        
        try:
            story = Story.objects.get(id=story_id)
            page = StoryPage.objects.get(story=story, page_number=page_number)
        except Story.DoesNotExist:
            return Response(
                {"detail": "Story not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except StoryPage.DoesNotExist:
            return Response(
                {"detail": f"Page {page_number} not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            audio_bytes, was_cached = TTSService.get_story_page_audio(
                story_id=str(story.id),
                page_number=page_number,
                text=page.text_content,
                language=story.language,
                voice_style=voice_style
            )
            
            response = HttpResponse(audio_bytes, content_type='audio/wav')
            response['Content-Disposition'] = f'inline; filename="page_{page_number}.wav"'
            response['Content-Length'] = len(audio_bytes)
            response['X-TTS-Cached'] = str(was_cached).lower()
            response['X-Story-ID'] = str(story_id)
            response['X-Page-Number'] = str(page_number)
            response['Cache-Control'] = 'public, max-age=604800'  # Browser cache 7 days
            
            return response
            
        except TTSServiceError as e:
            logger.error(f"TTS error for story {story_id} page {page_number}: {e}")
            return Response(
                {"detail": str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


class TTSStatusView(APIView):
    """
    GET /api/v1/speech/status/
    
    Check TTS service health and cache statistics.
    
    Response:
    {
        "status": "healthy",
        "model": {"status": "ready", "model": "ai4bharat/indic-parler-tts"},
        "cache": {
            "total_entries": 150,
            "total_size_bytes": 52428800,
            "total_cost_usd": 0.054,
            "estimated_savings_usd": 1.23
        }
    }
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        status_info = TTSService.check_service_status()
        return Response({"data": status_info})


class PrewarmStoryAudioView(APIView):
    """
    POST /api/v1/speech/prewarm/{story_id}/
    
    Pre-generate and cache all audio for a story.
    Admin only - use when adding new stories.
    
    Response:
    {
        "story_id": "xxx",
        "story_title": "चिड़िया और बिल्ली",
        "pages_total": 10,
        "pages_cached": 0,
        "pages_generated": 10,
        "total_cost_usd": 0.0036
    }
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, story_id):
        # Check if user is admin
        if not request.user.role == 'ADMIN':
            return Response(
                {"detail": "Admin access required"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            results = TTSService.prewarm_story(story_id)
            return Response({"data": results})
            
        except TTSServiceError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
```

---

## 🔗 URL Configuration

```python
# apps/speech/urls.py

from django.urls import path
from . import views

app_name = 'speech'

urlpatterns = [
    # Main TTS endpoint
    path('tts/', views.TextToSpeechView.as_view(), name='tts'),
    
    # Story-specific audio
    path(
        'stories/<uuid:story_id>/pages/<int:page_number>/audio/',
        views.StoryPageAudioView.as_view(),
        name='story-page-audio'
    ),
    
    # Service status
    path('status/', views.TTSStatusView.as_view(), name='status'),
    
    # Pre-warm cache (admin only)
    path('prewarm/<uuid:story_id>/', views.PrewarmStoryAudioView.as_view(), name='prewarm'),
]
```

```python
# config/urls.py - Add to main urlpatterns

urlpatterns = [
    # ... existing urls ...
    path('api/v1/speech/', include('apps.speech.urls')),
]
```

---

## 🛠️ Management Commands

### Pre-warm All Stories

```python
# apps/speech/management/commands/prewarm_tts_cache.py

"""
Management command to pre-generate TTS audio for all stories.
Run this after syncing new stories from StoryWeaver.

Usage:
    python manage.py prewarm_tts_cache
    python manage.py prewarm_tts_cache --language=HINDI
    python manage.py prewarm_tts_cache --story-id=xxx
"""

from django.core.management.base import BaseCommand
from apps.stories.models import Story
from apps.speech.services.tts_service import TTSService
import time


class Command(BaseCommand):
    help = 'Pre-generate and cache TTS audio for stories'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--language',
            type=str,
            help='Only process stories in this language (HINDI, TAMIL, etc.)'
        )
        parser.add_argument(
            '--story-id',
            type=str,
            help='Process a specific story only'
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=None,
            help='Maximum number of stories to process'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without actually generating audio'
        )
    
    def handle(self, *args, **options):
        language = options.get('language')
        story_id = options.get('story_id')
        limit = options.get('limit')
        dry_run = options.get('dry_run')
        
        # Build queryset
        stories = Story.objects.prefetch_related('pages')
        
        if story_id:
            stories = stories.filter(id=story_id)
        elif language:
            stories = stories.filter(language=language)
        
        if limit:
            stories = stories[:limit]
        
        total_stories = stories.count()
        total_pages = 0
        total_generated = 0
        total_cached = 0
        total_failed = 0
        total_cost = 0
        
        self.stdout.write(f"\n🎵 Pre-warming TTS cache for {total_stories} stories\n")
        
        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN - No audio will be generated\n"))
        
        for i, story in enumerate(stories, 1):
            self.stdout.write(f"\n[{i}/{total_stories}] {story.title}")
            self.stdout.write(f"    Language: {story.language}, Pages: {story.pages.count()}")
            
            if dry_run:
                total_pages += story.pages.count()
                continue
            
            try:
                results = TTSService.prewarm_story(str(story.id))
                
                total_pages += results['pages_total']
                total_generated += results['pages_generated']
                total_cached += results['pages_cached']
                total_failed += results['pages_failed']
                total_cost += results['total_cost_usd']
                
                self.stdout.write(
                    f"    ✅ Generated: {results['pages_generated']}, "
                    f"Cached: {results['pages_cached']}, "
                    f"Failed: {results['pages_failed']}"
                )
                
                # Rate limiting - be nice to the API
                if results['pages_generated'] > 0:
                    time.sleep(1)
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"    ❌ Error: {e}"))
                total_failed += story.pages.count()
        
        # Summary
        self.stdout.write(f"\n{'='*50}")
        self.stdout.write(f"📊 Summary:")
        self.stdout.write(f"    Total Stories: {total_stories}")
        self.stdout.write(f"    Total Pages: {total_pages}")
        
        if not dry_run:
            self.stdout.write(f"    Pages Generated: {total_generated}")
            self.stdout.write(f"    Pages Already Cached: {total_cached}")
            self.stdout.write(f"    Pages Failed: {total_failed}")
            self.stdout.write(f"    Estimated Cost: ${total_cost:.4f}")
        
        self.stdout.write(self.style.SUCCESS(f"\n✨ Pre-warming complete!\n"))
```

### Clear TTS Cache

```python
# apps/speech/management/commands/clear_tts_cache.py

"""
Management command to clear TTS cache.
Use with caution - will require regenerating all audio.

Usage:
    python manage.py clear_tts_cache --redis-only
    python manage.py clear_tts_cache --all
"""

from django.core.management.base import BaseCommand
from django.core.cache import cache
from apps.speech.models import AudioCache


class Command(BaseCommand):
    help = 'Clear TTS audio cache'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--redis-only',
            action='store_true',
            help='Clear only Redis cache (keeps S3/R2 and database)'
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Clear ALL caches (Redis, S3/R2, database)'
        )
        parser.add_argument(
            '--language',
            type=str,
            help='Clear only entries for this language'
        )
    
    def handle(self, *args, **options):
        redis_only = options.get('redis_only')
        clear_all = options.get('all')
        language = options.get('language')
        
        if not redis_only and not clear_all:
            self.stdout.write(
                self.style.ERROR("Must specify --redis-only or --all")
            )
            return
        
        # Clear Redis
        self.stdout.write("Clearing Redis cache...")
        cache.delete_pattern("tts:audio:*")
        self.stdout.write(self.style.SUCCESS("✅ Redis cache cleared"))
        
        if clear_all:
            # Clear database entries
            queryset = AudioCache.objects.all()
            if language:
                queryset = queryset.filter(language=language)
            
            count = queryset.count()
            
            # TODO: Also delete from S3/R2 storage
            # This would require iterating and deleting each file
            
            queryset.delete()
            self.stdout.write(
                self.style.SUCCESS(f"✅ Deleted {count} database entries")
            )
        
        self.stdout.write(self.style.SUCCESS("\n✨ Cache clearing complete!"))
```

---

## 🔐 Admin Configuration

```python
# apps/speech/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import AudioCache, TTSUsageLog


@admin.register(AudioCache)
class AudioCacheAdmin(admin.ModelAdmin):
    list_display = [
        'short_text',
        'language',
        'voice_style',
        'access_count',
        'audio_size_display',
        'generation_cost_usd',
        'created_at'
    ]
    list_filter = ['language', 'voice_style', 'created_at']
    search_fields = ['text_content', 'cache_key']
    readonly_fields = [
        'cache_key',
        'text_hash',
        'audio_url',
        'audio_size_bytes',
        'generation_time_ms',
        'generation_cost_usd',
        'access_count',
        'last_accessed_at'
    ]
    ordering = ['-created_at']
    
    def short_text(self, obj):
        return obj.text_content[:50] + '...' if len(obj.text_content) > 50 else obj.text_content
    short_text.short_description = 'Text'
    
    def audio_size_display(self, obj):
        if obj.audio_size_bytes:
            kb = obj.audio_size_bytes / 1024
            return f"{kb:.1f} KB"
        return "-"
    audio_size_display.short_description = 'Size'


@admin.register(TTSUsageLog)
class TTSUsageLogAdmin(admin.ModelAdmin):
    list_display = [
        'created_at',
        'language',
        'status_badge',
        'was_cached',
        'text_length',
        'response_time_ms',
        'estimated_cost_usd'
    ]
    list_filter = ['status', 'was_cached', 'language', 'created_at']
    ordering = ['-created_at']
    
    def status_badge(self, obj):
        colors = {
            'success': 'green',
            'cached': 'blue',
            'error': 'red'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.status.upper()
        )
    status_badge.short_description = 'Status'
```

---

## 🧪 Tests

```python
# apps/speech/tests/test_tts_service.py

import pytest
from unittest.mock import patch, MagicMock
from apps.speech.services.tts_service import TTSService, TTSServiceError
from apps.speech.services.cache_service import AudioCacheService
from apps.speech.models import AudioCache


@pytest.fixture
def mock_hf_client():
    """Mock Hugging Face client."""
    with patch('apps.speech.services.tts_service.HuggingFaceClient') as mock:
        client_instance = MagicMock()
        client_instance.text_to_speech.return_value = b'fake_audio_bytes'
        mock.return_value = client_instance
        yield client_instance


@pytest.fixture
def sample_audio_bytes():
    """Sample audio bytes for testing."""
    return b'RIFF' + b'\x00' * 100  # Fake WAV header


class TestTTSService:
    
    @pytest.mark.django_db
    def test_text_to_speech_generates_audio(self, mock_hf_client, sample_audio_bytes):
        """Test that TTS generates audio for new text."""
        mock_hf_client.text_to_speech.return_value = sample_audio_bytes
        
        audio, was_cached = TTSService.text_to_speech(
            text="नमस्ते",
            language="HINDI"
        )
        
        assert audio == sample_audio_bytes
        assert was_cached is False
        mock_hf_client.text_to_speech.assert_called_once()
    
    @pytest.mark.django_db
    def test_text_to_speech_returns_cached(self, mock_hf_client, sample_audio_bytes):
        """Test that cached audio is returned without API call."""
        # First call - generates and caches
        mock_hf_client.text_to_speech.return_value = sample_audio_bytes
        TTSService.text_to_speech(text="नमस्ते", language="HINDI")
        
        # Reset mock
        mock_hf_client.reset_mock()
        
        # Second call - should be cached
        audio, was_cached = TTSService.text_to_speech(
            text="नमस्ते",
            language="HINDI"
        )
        
        assert was_cached is True
        mock_hf_client.text_to_speech.assert_not_called()
    
    @pytest.mark.django_db
    def test_empty_text_raises_error(self):
        """Test that empty text raises error."""
        with pytest.raises(TTSServiceError) as exc:
            TTSService.text_to_speech(text="", language="HINDI")
        
        assert "empty" in str(exc.value).lower()
    
    @pytest.mark.django_db
    def test_text_too_long_raises_error(self):
        """Test that text over 5000 chars raises error."""
        long_text = "अ" * 5001
        
        with pytest.raises(TTSServiceError) as exc:
            TTSService.text_to_speech(text=long_text, language="HINDI")
        
        assert "too long" in str(exc.value).lower()


class TestCacheService:
    
    @pytest.mark.django_db
    def test_store_and_retrieve_audio(self, sample_audio_bytes):
        """Test storing and retrieving audio from cache."""
        # Store
        AudioCacheService.store_audio(
            text="टेस्ट",
            language="HINDI",
            voice_style="storyteller",
            audio_bytes=sample_audio_bytes
        )
        
        # Retrieve
        audio, was_cached, url = AudioCacheService.get_cached_audio(
            text="टेस्ट",
            language="HINDI",
            voice_style="storyteller"
        )
        
        assert audio == sample_audio_bytes
        assert was_cached is True
    
    @pytest.mark.django_db
    def test_different_voice_styles_cached_separately(self, sample_audio_bytes):
        """Test that different voice styles are cached separately."""
        # Store with storyteller style
        AudioCacheService.store_audio(
            text="टेस्ट",
            language="HINDI",
            voice_style="storyteller",
            audio_bytes=sample_audio_bytes
        )
        
        # Try to get with calm style - should be cache miss
        audio, was_cached, url = AudioCacheService.get_cached_audio(
            text="टेस्ट",
            language="HINDI",
            voice_style="calm"
        )
        
        assert was_cached is False
```

---

## 📋 Implementation Checklist

### Phase 1: Setup (Day 1)

- [ ] Add dependencies to requirements.txt
- [ ] Update Django settings with HF configuration
- [ ] Create speech app structure
- [ ] Create AudioCache and TTSUsageLog models
- [ ] Run migrations: `python manage.py makemigrations speech && python manage.py migrate`

### Phase 2: Core Services (Day 1-2)

- [ ] Implement `external/huggingface/inference_client.py`
- [ ] Implement `apps/speech/services/voice_profiles.py`
- [ ] Implement `apps/speech/services/cache_service.py`
- [ ] Implement `apps/speech/services/tts_service.py`

### Phase 3: API (Day 2)

- [ ] Implement `apps/speech/views.py`
- [ ] Implement `apps/speech/urls.py`
- [ ] Add URLs to main config
- [ ] Implement `apps/speech/admin.py`

### Phase 4: Management Commands (Day 2)

- [ ] Implement `prewarm_tts_cache` command
- [ ] Implement `clear_tts_cache` command

### Phase 5: Testing (Day 3)

- [ ] Write unit tests
- [ ] Test TTS endpoint manually
- [ ] Test caching works correctly
- [ ] Pre-warm existing stories

### Phase 6: Deployment (Day 3)

- [ ] Set up Redis
- [ ] Set up Cloudflare R2 / S3 storage
- [ ] Get Hugging Face PRO account ($9/month)
- [ ] Configure environment variables
- [ ] Deploy and test

---

## 🚀 Quick Test Commands

```bash
# 1. Test TTS endpoint
curl -X POST http://localhost:8000/api/v1/speech/tts/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text": "नमस्ते बच्चों", "language": "HINDI"}' \
  --output test_hindi.wav

# 2. Play the audio
play test_hindi.wav  # or open in browser

# 3. Check service status
curl http://localhost:8000/api/v1/speech/status/ \
  -H "Authorization: Bearer $TOKEN"

# 4. Pre-warm all Hindi stories
python manage.py prewarm_tts_cache --language=HINDI

# 5. Check cache stats
python manage.py shell -c "
from apps.speech.services.cache_service import AudioCacheService
print(AudioCacheService.get_cache_stats())
"
```

---

## 💰 Cost Summary

| Item | Cost | Frequency |
|------|------|-----------|
| Hugging Face PRO | $9.00 | Monthly |
| Initial cache (50 stories) | ~$0.18 | One-time |
| Monthly new stories (~20) | ~$0.07 | Monthly |
| **Total** | **~$9.25** | **Monthly** |

With caching, you can serve **unlimited users** for ~$9/month!

---

## ⚠️ Important Notes

1. **Get HF PRO Account First**: Sign up at https://huggingface.co/pricing
2. **Set API Token**: Get from https://huggingface.co/settings/tokens
3. **Pre-warm Cache**: Run `prewarm_tts_cache` after syncing stories
4. **Monitor Usage**: Check https://huggingface.co/settings/billing monthly
5. **Redis Required**: For fast cache lookups
6. **S3/R2 Required**: For permanent audio storage

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| 402 Error (Credits exhausted) | Check HF billing, upgrade if needed |
| 503 Error (Model loading) | Wait 30-60 seconds, retry |
| 429 Error (Rate limited) | Reduce request frequency |
| Audio sounds wrong | Check voice_style and language match |
| Cache not working | Verify Redis is running |
