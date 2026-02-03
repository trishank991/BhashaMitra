"""Base settings for Peppi Languages (part of Peppi Academy)."""
import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'change-me-in-production')

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'django_filters',
]

LOCAL_APPS = [
    'apps.core',
    'apps.users',
    'apps.children',
    'apps.stories',
    'apps.progress',
    'apps.gamification',
    'apps.speech',
    'apps.curriculum',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Custom user model
AUTH_USER_MODEL = 'users.User'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Pacific/Auckland'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'apps.core.pagination.CursorPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
        'auth': '10/minute',
        'speech': '20/minute',
        'tts': '20/minute',
    },
    'EXCEPTION_HANDLER': 'apps.core.exceptions.custom_exception_handler',
}

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# CORS Settings
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:3000').split(',')
CORS_ALLOW_CREDENTIALS = True

# ===========================================
# EXTERNAL API CONFIGURATION
# ===========================================

# Hugging Face (TTS using Parler-TTS Space)
# Get token from: https://huggingface.co/settings/tokens
# PRO account ($9/month) recommended for better rate limits
HUGGINGFACE_API_TOKEN = os.getenv('HUGGINGFACE_API_TOKEN', '')
HUGGINGFACE_ACCOUNT_TYPE = os.getenv('HUGGINGFACE_ACCOUNT_TYPE', 'free')
TTS_SPACE_ID = os.getenv('TTS_SPACE_ID', 'parler-tts/parler_tts')

# TTS Cache settings
TTS_CACHE_TTL = int(os.getenv('TTS_CACHE_TTL_SECONDS', 86400))  # 24 hours in Redis
TTS_DEFAULT_VOICE_STYLE = os.getenv('TTS_DEFAULT_VOICE_STYLE', 'storyteller')

# StoryWeaver API
STORYWEAVER_BASE_URL = 'https://storyweaver.org.in/api/v1'

# ===========================================
# GAMIFICATION CONFIGURATION
# ===========================================

# Points awarded for activities
POINTS_CONFIG = {
    'STORY_STARTED': 10,
    'PAGE_READ': 5,
    'STORY_COMPLETED_BASE': 50,  # Multiplied by story level
    'VOICE_RECORDING': 15,
    'FLASHCARD_CORRECT': 5,
    'FLASHCARD_SESSION': 20,
    'GAME_COMPLETED': 25,
    'ASSESSMENT_PASSED': 100,
    'LETTER_MASTERED': 10,
    'WORD_MASTERED': 5,
}

# Level thresholds (points required)
LEVEL_THRESHOLDS = {
    1: 0,
    2: 100,
    3: 500,
    4: 1500,
    5: 3000,
}

# ===========================================
# APP CONFIGURATION
# ===========================================

# Maximum children per parent account
MAX_CHILDREN_PER_USER = 5

# Child age limits
MIN_CHILD_AGE = 2
MAX_CHILD_AGE = 18

# Cache timeouts (seconds)
CACHE_TIMEOUT_STORY = 3600  # 1 hour
CACHE_TIMEOUT_TTS = 86400   # 24 hours
CACHE_TIMEOUT_PIPELINE = 3600  # 1 hour

# ===========================================
# LANGUAGE CONFIGURATION
# ===========================================

SUPPORTED_LANGUAGES = {
    'HINDI': {'code': 'hi', 'name': 'Hindi', 'native': 'हिन्दी', 'script': 'Devanagari'},
    'TAMIL': {'code': 'ta', 'name': 'Tamil', 'native': 'தமிழ்', 'script': 'Tamil'},
    'GUJARATI': {'code': 'gu', 'name': 'Gujarati', 'native': 'ગુજરાતી', 'script': 'Gujarati'},
    'PUNJABI': {'code': 'pa', 'name': 'Punjabi', 'native': 'ਪੰਜਾਬੀ', 'script': 'Gurmukhi'},
    'TELUGU': {'code': 'te', 'name': 'Telugu', 'native': 'తెలుగు', 'script': 'Telugu'},
    'MALAYALAM': {'code': 'ml', 'name': 'Malayalam', 'native': 'മലയാളം', 'script': 'Malayalam'},
}
