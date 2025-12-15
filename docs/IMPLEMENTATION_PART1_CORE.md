# BhashaMitra - Complete Implementation Guide

> **Version**: 2.0 | **Last Updated**: December 2024  
> **Purpose**: Comprehensive Django backend implementation for BhashaMitra

---

# Part 1: Project Setup & Core Models

## Table of Contents
1. [Project Initialization](#1-project-initialization)
2. [Directory Structure](#2-directory-structure)
3. [Dependencies](#3-dependencies)
4. [Settings Configuration](#4-settings-configuration)
5. [Core Models](#5-core-models)
6. [User & Authentication](#6-user--authentication)
7. [Children Management](#7-children-management)

---

## 1. Project Initialization

### Create Project

```bash
# Create project directory
mkdir bhashamitra-backend && cd bhashamitra-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install Django
pip install django djangorestframework

# Create Django project
django-admin startproject config .

# Create apps directory
mkdir -p apps/{core,users,children,stories,progress,gamification,speech,curriculum}
touch apps/__init__.py
touch apps/{core,users,children,stories,progress,gamification,speech,curriculum}/__init__.py
```

---

## 2. Directory Structure

```
bhashamitra-backend/
├── manage.py
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── config/
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── prod.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── __init__.py
│   ├── core/                    # Base models, utilities
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── permissions.py
│   │   ├── pagination.py
│   │   ├── exceptions.py
│   │   └── utils.py
│   ├── users/                   # User authentication
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── tests/
│   ├── children/                # Child profiles
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── services.py
│   │   ├── admin.py
│   │   └── tests/
│   ├── stories/                 # StoryWeaver integration
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── services.py
│   │   ├── admin.py
│   │   └── tests/
│   ├── progress/                # Reading progress
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── services.py
│   │   ├── admin.py
│   │   └── tests/
│   ├── gamification/            # Points, badges, streaks
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── points.py
│   │   │   ├── levels.py
│   │   │   ├── streaks.py
│   │   │   └── badges.py
│   │   ├── admin.py
│   │   └── tests/
│   ├── speech/                  # Bhashini TTS/STT
│   │   ├── __init__.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── serializers.py
│   │   └── tests/
│   └── curriculum/              # Alphabets, vocabulary, grammar, games, assessments
│       ├── __init__.py
│       ├── models/
│       │   ├── __init__.py
│       │   ├── script.py
│       │   ├── vocabulary.py
│       │   ├── grammar.py
│       │   ├── games.py
│       │   └── assessment.py
│       ├── serializers/
│       ├── views/
│       ├── services/
│       ├── urls.py
│       ├── admin.py
│       └── tests/
├── external/                    # External API clients
│   ├── __init__.py
│   ├── storyweaver/
│   │   ├── __init__.py
│   │   └── client.py
│   └── bhashini/
│       ├── __init__.py
│       └── client.py
├── scripts/                     # Management scripts
│   ├── seed_badges.py
│   ├── seed_alphabet.py
│   └── seed_vocabulary.py
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── .env.example
├── .gitignore
├── pytest.ini
└── README.md
```

---

## 3. Dependencies

### requirements/base.txt
```txt
# Django
Django>=5.0,<6.0
djangorestframework>=3.14,<4.0
django-cors-headers>=4.3,<5.0
django-filter>=23.5,<24.0

# Authentication
djangorestframework-simplejwt>=5.3,<6.0

# Database
psycopg2-binary>=2.9,<3.0

# Environment
python-dotenv>=1.0,<2.0

# Production server
gunicorn>=21.0,<22.0
whitenoise>=6.6,<7.0

# Utils
Pillow>=10.0,<11.0
requests>=2.31,<3.0

# Storage (production)
boto3>=1.34,<2.0
django-storages>=1.14,<2.0

# Async tasks (optional)
celery>=5.3,<6.0
redis>=5.0,<6.0
```

### requirements/dev.txt
```txt
-r base.txt

# Testing
pytest>=7.4,<8.0
pytest-django>=4.7,<5.0
pytest-cov>=4.1,<5.0
factory-boy>=3.3,<4.0
faker>=22.0,<23.0

# Code quality
black>=23.12,<24.0
isort>=5.13,<6.0
flake8>=7.0,<8.0

# Development tools
django-debug-toolbar>=4.2,<5.0
ipython>=8.18,<9.0
```

### requirements/prod.txt
```txt
-r base.txt

# Monitoring
sentry-sdk>=1.38,<2.0

# Health checks
django-health-check>=3.17,<4.0
```

### Install Dependencies
```bash
pip install -r requirements/dev.txt
```

---

## 4. Settings Configuration

### config/settings/base.py
```python
"""Base settings for BhashaMitra."""
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

# Bhashini API (Government of India Speech Services)
BHASHINI_USER_ID = os.getenv('BHASHINI_USER_ID', '')
BHASHINI_API_KEY = os.getenv('BHASHINI_API_KEY', '')
BHASHINI_AUTH_URL = 'https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline'

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
```

### config/settings/dev.py
```python
"""Development settings."""
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'bhashamitra_dev'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Debug Toolbar
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
INTERNAL_IPS = ['127.0.0.1']

# Email (console backend for development)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# CORS - Allow all in development
CORS_ALLOW_ALL_ORIGINS = True

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'apps': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
```

### config/settings/prod.py
```python
"""Production settings."""
from .base import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

DEBUG = False
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'CONN_MAX_AGE': 60,
        'OPTIONS': {'sslmode': 'require'},
    }
}

# Sentry Error Tracking
if os.getenv('SENTRY_DSN'):
    sentry_sdk.init(
        dsn=os.getenv('SENTRY_DSN'),
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=False,
    )

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@bhashamitra.co.nz')
```

### config/settings/__init__.py
```python
"""Settings initialization."""
import os

environment = os.getenv('DJANGO_ENV', 'dev')

if environment == 'prod':
    from .prod import *
else:
    from .dev import *
```

---

## 5. Core Models

### apps/core/models.py
```python
"""Base models for the application."""
import uuid
from django.db import models


class TimeStampedModel(models.Model):
    """Abstract model with created/updated timestamps."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteManager(models.Manager):
    """Manager that excludes soft-deleted records by default."""
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class SoftDeleteModel(models.Model):
    """Abstract model with soft delete capability."""
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    objects = SoftDeleteManager()
    all_objects = models.Manager()  # Include deleted records

    class Meta:
        abstract = True

    def soft_delete(self):
        """Mark record as deleted."""
        from django.utils import timezone
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])
    
    def restore(self):
        """Restore a soft-deleted record."""
        self.deleted_at = None
        self.save(update_fields=['deleted_at'])

    @property
    def is_deleted(self):
        return self.deleted_at is not None
```

### apps/core/permissions.py
```python
"""Custom permissions."""
from rest_framework import permissions


class IsParentOfChild(permissions.BasePermission):
    """Permission to check if user is the parent of the child."""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Handle Child object
        if hasattr(obj, 'user'):
            return obj.user == request.user
        # Handle objects with child FK (Progress, etc.)
        if hasattr(obj, 'child'):
            return obj.child.user == request.user
        return False


class IsOwnerOrAdmin(permissions.BasePermission):
    """Permission for owners or admins."""
    
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'ADMIN':
            return True
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return obj == request.user
```

### apps/core/pagination.py
```python
"""Custom pagination classes."""
from rest_framework.pagination import CursorPagination as BaseCursorPagination


class CursorPagination(BaseCursorPagination):
    """Default cursor pagination."""
    page_size = 20
    page_size_query_param = 'limit'
    max_page_size = 50
    ordering = '-created_at'
```

### apps/core/exceptions.py
```python
"""Custom exception handling."""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """Custom exception handler following RFC 7807."""
    response = exception_handler(exc, context)
    
    if response is None:
        logger.exception("Unhandled exception", exc_info=exc)
        return Response(
            {
                'type': 'https://bhashamitra.co.nz/errors/internal',
                'title': 'Internal Server Error',
                'status': 500,
                'detail': 'An unexpected error occurred.',
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    error_types = {
        400: 'validation',
        401: 'unauthorized',
        403: 'forbidden',
        404: 'not-found',
        409: 'conflict',
        429: 'rate-limited',
        500: 'internal',
        503: 'unavailable',
    }
    
    error_titles = {
        400: 'Validation Error',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found',
        409: 'Conflict',
        429: 'Rate Limited',
        500: 'Internal Server Error',
        503: 'Service Unavailable',
    }
    
    error_response = {
        'type': f'https://bhashamitra.co.nz/errors/{error_types.get(response.status_code, "error")}',
        'title': error_titles.get(response.status_code, 'Error'),
        'status': response.status_code,
        'detail': _extract_detail(response.data),
    }
    
    response.data = error_response
    return response


def _extract_detail(data):
    """Extract error detail from response data."""
    if isinstance(data, dict):
        if 'detail' in data:
            return data['detail']
        if 'non_field_errors' in data:
            return data['non_field_errors'][0]
        for key, value in data.items():
            if isinstance(value, list):
                return f"{key}: {value[0]}"
            return f"{key}: {value}"
    if isinstance(data, list):
        return data[0] if data else 'An error occurred'
    return str(data)


class AppException(Exception):
    """Base exception for application errors."""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_message = 'An error occurred'
    
    def __init__(self, message=None, code=None):
        self.message = message or self.default_message
        self.code = code


class NotFoundError(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    default_message = 'Resource not found'


class ValidationError(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = 'Validation error'
```

### apps/core/utils.py
```python
"""Utility functions."""
from datetime import date


def calculate_age(date_of_birth: date) -> int:
    """Calculate age from date of birth."""
    today = date.today()
    return today.year - date_of_birth.year - (
        (today.month, today.day) < (date_of_birth.month, date_of_birth.day)
    )


def format_duration(seconds: int) -> str:
    """Format seconds into human-readable duration."""
    if seconds < 60:
        return f"{seconds}s"
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    if minutes < 60:
        return f"{minutes}m {remaining_seconds}s" if remaining_seconds else f"{minutes}m"
    hours = minutes // 60
    remaining_minutes = minutes % 60
    return f"{hours}h {remaining_minutes}m" if remaining_minutes else f"{hours}h"
```

---

## 6. User & Authentication

### apps/users/models.py
```python
"""User models."""
from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.core.models import TimeStampedModel, SoftDeleteModel


class User(AbstractUser, TimeStampedModel, SoftDeleteModel):
    """Custom user model for parents."""
    
    class Role(models.TextChoices):
        PARENT = 'PARENT', 'Parent'
        ADMIN = 'ADMIN', 'Admin'
    
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.PARENT)
    avatar_url = models.URLField(blank=True, null=True)
    
    # Email as username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
        ]
    
    def __str__(self):
        return self.email
```

### apps/users/serializers.py
```python
"""User serializers."""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """User details serializer."""
    
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'role', 'avatar_url', 'created_at']
        read_only_fields = ['id', 'role', 'created_at']


class RegisterSerializer(serializers.ModelSerializer):
    """User registration serializer."""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password_confirm']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password_confirm': 'Passwords do not match'})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
        )
        return user


class LoginSerializer(serializers.Serializer):
    """Login serializer."""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
```

### apps/users/views.py
```python
"""User views."""
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model

from .serializers import UserSerializer, RegisterSerializer, LoginSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """Register a new parent account."""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    throttle_scope = 'auth'
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'data': UserSerializer(user).data,
            'session': {
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            },
            'meta': {'message': 'Registration successful'}
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """Login and get JWT tokens."""
    permission_classes = [AllowAny]
    throttle_scope = 'auth'
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(
            request,
            username=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        
        if not user:
            return Response(
                {'detail': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if user.is_deleted:
            return Response(
                {'detail': 'Account has been deactivated'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'data': {
                'user': UserSerializer(user).data,
                'session': {
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                }
            }
        })


class LogoutView(APIView):
    """Logout and blacklist refresh token."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
        except Exception:
            pass
        
        return Response({'meta': {'message': 'Logged out successfully'}})


class MeView(generics.RetrieveUpdateAPIView):
    """Get or update current user."""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
```

### apps/users/urls.py
```python
"""User URL configuration."""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', views.MeView.as_view(), name='me'),
]
```

### apps/users/admin.py
```python
"""User admin configuration."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'name', 'role', 'is_active', 'created_at']
    list_filter = ['role', 'is_active', 'created_at']
    search_fields = ['email', 'name']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'avatar_url')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'created_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ['created_at']
```

---

## 7. Children Management

### apps/children/models.py
```python
"""Child profile models."""
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import TimeStampedModel, SoftDeleteModel


class Child(TimeStampedModel, SoftDeleteModel):
    """Child profile linked to a parent user."""
    
    class Language(models.TextChoices):
        HINDI = 'HINDI', 'Hindi'
        TAMIL = 'TAMIL', 'Tamil'
        GUJARATI = 'GUJARATI', 'Gujarati'
        PUNJABI = 'PUNJABI', 'Punjabi'
        TELUGU = 'TELUGU', 'Telugu'
        MALAYALAM = 'MALAYALAM', 'Malayalam'
    
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='children'
    )
    name = models.CharField(max_length=100)
    avatar = models.CharField(max_length=50, default='default')
    date_of_birth = models.DateField()
    language = models.CharField(
        max_length=20,
        choices=Language.choices,
        default=Language.HINDI
    )
    level = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    total_points = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'children'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['language', 'level']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.user.email})"
    
    @property
    def age(self):
        from apps.core.utils import calculate_age
        return calculate_age(self.date_of_birth)
```

### apps/children/serializers.py
```python
"""Child serializers."""
from rest_framework import serializers
from django.conf import settings
from datetime import date
from .models import Child


class ChildSerializer(serializers.ModelSerializer):
    """Child profile serializer."""
    age = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Child
        fields = [
            'id', 'name', 'avatar', 'date_of_birth', 'language',
            'level', 'total_points', 'age', 'created_at'
        ]
        read_only_fields = ['id', 'level', 'total_points', 'created_at']


class CreateChildSerializer(serializers.ModelSerializer):
    """Create child serializer."""
    
    class Meta:
        model = Child
        fields = ['name', 'date_of_birth', 'language', 'avatar']
    
    def validate_date_of_birth(self, value):
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        
        if age < settings.MIN_CHILD_AGE:
            raise serializers.ValidationError(f"Child must be at least {settings.MIN_CHILD_AGE} years old")
        if age > settings.MAX_CHILD_AGE:
            raise serializers.ValidationError(f"Child must be under {settings.MAX_CHILD_AGE} years old")
        
        return value
    
    def validate(self, attrs):
        user = self.context['request'].user
        if user.children.filter(deleted_at__isnull=True).count() >= settings.MAX_CHILDREN_PER_USER:
            raise serializers.ValidationError(
                f"Maximum of {settings.MAX_CHILDREN_PER_USER} children allowed per account"
            )
        return attrs
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class UpdateChildSerializer(serializers.ModelSerializer):
    """Update child serializer."""
    
    class Meta:
        model = Child
        fields = ['name', 'avatar', 'language']


class ChildStatsSerializer(serializers.Serializer):
    """Child statistics serializer."""
    child_id = serializers.UUIDField()
    period = serializers.CharField()
    stories_started = serializers.IntegerField()
    stories_completed = serializers.IntegerField()
    pages_read = serializers.IntegerField()
    time_spent_minutes = serializers.IntegerField()
    points_earned = serializers.IntegerField()
    recordings_made = serializers.IntegerField()
    current_streak = serializers.IntegerField()
    badges_earned = serializers.IntegerField()
```

### apps/children/views.py
```python
"""Child views."""
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta

from apps.core.permissions import IsParentOfChild
from .models import Child
from .serializers import (
    ChildSerializer,
    CreateChildSerializer,
    UpdateChildSerializer,
    ChildStatsSerializer,
)


class ChildListCreateView(generics.ListCreateAPIView):
    """List and create children for the authenticated parent."""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Child.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateChildSerializer
        return ChildSerializer


class ChildDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a child profile."""
    permission_classes = [IsAuthenticated, IsParentOfChild]
    
    def get_queryset(self):
        return Child.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UpdateChildSerializer
        return ChildSerializer
    
    def perform_destroy(self, instance):
        instance.soft_delete()


class ChildStatsView(APIView):
    """Get child statistics for a given period."""
    permission_classes = [IsAuthenticated, IsParentOfChild]
    
    def get(self, request, pk):
        try:
            child = Child.objects.get(pk=pk, user=request.user)
        except Child.DoesNotExist:
            return Response(
                {'detail': 'Child not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        period = request.query_params.get('period', 'week')
        
        # Calculate date range
        today = timezone.now().date()
        if period == 'day':
            start_date = today
        elif period == 'week':
            start_date = today - timedelta(days=7)
        elif period == 'month':
            start_date = today - timedelta(days=30)
        else:
            start_date = None  # All time
        
        # Get daily activities
        from apps.progress.models import DailyActivity
        activities = DailyActivity.objects.filter(child=child)
        if start_date:
            activities = activities.filter(date__gte=start_date)
        
        # Aggregate stats
        stats = activities.aggregate(
            stories_started=Sum('stories_started'),
            stories_completed=Sum('stories_completed'),
            pages_read=Sum('pages_read'),
            time_spent_seconds=Sum('time_spent_seconds'),
            points_earned=Sum('points_earned'),
            recordings_made=Sum('recordings_made'),
        )
        
        # Get streak and badges
        from apps.gamification.models import Streak, ChildBadge
        streak = Streak.objects.filter(child=child).first()
        badges_count = ChildBadge.objects.filter(child=child).count()
        
        response_data = {
            'child_id': child.id,
            'period': period,
            'stories_started': stats['stories_started'] or 0,
            'stories_completed': stats['stories_completed'] or 0,
            'pages_read': stats['pages_read'] or 0,
            'time_spent_minutes': (stats['time_spent_seconds'] or 0) // 60,
            'points_earned': stats['points_earned'] or 0,
            'recordings_made': stats['recordings_made'] or 0,
            'current_streak': streak.current_streak if streak else 0,
            'badges_earned': badges_count,
        }
        
        return Response({'data': response_data})
```

### apps/children/urls.py
```python
"""Children URL configuration."""
from django.urls import path
from . import views

app_name = 'children'

urlpatterns = [
    path('', views.ChildListCreateView.as_view(), name='list-create'),
    path('<uuid:pk>/', views.ChildDetailView.as_view(), name='detail'),
    path('<uuid:pk>/stats/', views.ChildStatsView.as_view(), name='stats'),
]
```

### apps/children/admin.py
```python
"""Children admin configuration."""
from django.contrib import admin
from .models import Child


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'language', 'level', 'total_points', 'created_at']
    list_filter = ['language', 'level', 'created_at']
    search_fields = ['name', 'user__email']
    ordering = ['-created_at']
    readonly_fields = ['total_points', 'created_at', 'updated_at']
```

---

## Next Steps

Continue to **Part 2** for:
- Stories & StoryWeaver Integration
- Progress Tracking
- Gamification (Points, Badges, Streaks, Levels)
- Speech Services (Bhashini TTS/STT)

Continue to **Part 3** for:
- Curriculum Module (Alphabets, Vocabulary, Grammar, Games, Assessments)
- Seed Scripts
- API Complete Reference
