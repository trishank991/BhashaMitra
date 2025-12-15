# BhashaMitra - Django Implementation Guide

> **Purpose**: Complete technical specification to build BhashaMitra
> **Stack**: Django 5.x + PostgreSQL + React (Next.js) Frontend
> **Timeline**: 30-day MVP

---

## 🎯 Project Context

### What is BhashaMitra?
A heritage language learning platform for Indian diaspora children (ages 4-14) in New Zealand/Australia. Children learn Hindi, Tamil, Gujarati, and Punjabi through interactive stories with text-to-speech audio.

### Your Role
You are a **Senior Full-Stack Engineer** building this MVP. Follow clean architecture principles, write production-quality code, and prioritize:
1. Security (child data protection, COPPA compliance)
2. Performance (< 3s load time, mobile-first)
3. Maintainability (clear separation of concerns)
4. Testability (aim for 80% coverage on critical paths)

### Tech Stack Decision
**Backend**: Django 5.x + Django REST Framework + PostgreSQL
**Frontend**: Next.js 14 (separate repo, API-first integration)
**Why Django over Next.js API routes**:
- Battle-tested ORM for complex parent-child-progress relationships
- Built-in admin panel for content management
- Superior for data-heavy operations and reporting
- Mature ecosystem for EdTech scale

---

## 📁 Project Structure

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
│   ├── users/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── services.py
│   │   ├── admin.py
│   │   └── tests/
│   │       ├── __init__.py
│   │       ├── test_models.py
│   │       ├── test_views.py
│   │       └── test_services.py
│   ├── children/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── services.py
│   │   ├── admin.py
│   │   └── tests/
│   ├── stories/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── services.py
│   │   ├── admin.py
│   │   └── tests/
│   ├── progress/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── services.py
│   │   ├── admin.py
│   │   └── tests/
│   ├── gamification/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── points.py
│   │   │   ├── streaks.py
│   │   │   ├── badges.py
│   │   │   └── levels.py
│   │   ├── admin.py
│   │   └── tests/
│   ├── speech/
│   │   ├── __init__.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── bhashini_client.py
│   │   │   └── audio_cache.py
│   │   └── tests/
│   └── core/
│       ├── __init__.py
│       ├── models.py          # Base models (TimeStampedModel, etc.)
│       ├── permissions.py     # Custom DRF permissions
│       ├── pagination.py      # Cursor pagination
│       ├── exceptions.py      # Custom exceptions
│       └── utils.py
├── external/
│   ├── __init__.py
│   ├── storyweaver/
│   │   ├── __init__.py
│   │   ├── client.py
│   │   └── sync.py
│   └── bhashini/
│       ├── __init__.py
│       └── client.py
├── templates/
│   └── admin/                 # Admin customizations
├── static/
├── media/
├── scripts/
│   ├── seed_badges.py
│   └── sync_stories.py
├── docker/
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   └── docker-compose.yml
├── .env.example
├── .gitignore
├── pytest.ini
├── setup.cfg
└── README.md
```

---

## 🗄️ Database Schema

### Complete Models Definition

```python
# apps/core/models.py
import uuid
from django.db import models


class TimeStampedModel(models.Model):
    """Base model with created/updated timestamps."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    """Base model with soft delete capability."""
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def soft_delete(self):
        from django.utils import timezone
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])

    @property
    def is_deleted(self):
        return self.deleted_at is not None
```

```python
# apps/users/models.py
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
    
    # Use email as username
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

```python
# apps/children/models.py
from django.db import models
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
        constraints = [
            models.CheckConstraint(
                check=models.Q(level__gte=1, level__lte=5),
                name='valid_level_range'
            )
        ]
    
    def __str__(self):
        return f"{self.name} ({self.user.email})"
    
    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
```

```python
# apps/stories/models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import TimeStampedModel
from apps.children.models import Child


class Story(TimeStampedModel):
    """Story content cached from StoryWeaver."""
    
    storyweaver_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=500)
    title_translit = models.CharField(max_length=500, blank=True, null=True)
    language = models.CharField(max_length=20, choices=Child.Language.choices)
    level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    page_count = models.IntegerField()
    cover_image_url = models.URLField()
    synopsis = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    illustrator = models.CharField(max_length=255, blank=True, null=True)
    categories = models.JSONField(default=list)
    cached_at = models.DateTimeField(auto_now_add=True)
    last_accessed_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'stories'
        indexes = [
            models.Index(fields=['language', 'level']),
            models.Index(fields=['storyweaver_id']),
        ]
        verbose_name_plural = 'stories'
    
    def __str__(self):
        return f"{self.title} (Level {self.level})"


class StoryPage(TimeStampedModel):
    """Individual pages of a story."""
    
    story = models.ForeignKey(
        Story,
        on_delete=models.CASCADE,
        related_name='pages'
    )
    page_number = models.IntegerField()
    text_content = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    audio_url = models.URLField(blank=True, null=True)  # Cached TTS audio
    
    class Meta:
        db_table = 'story_pages'
        unique_together = ['story', 'page_number']
        ordering = ['page_number']
        indexes = [
            models.Index(fields=['story', 'page_number']),
        ]
    
    def __str__(self):
        return f"{self.story.title} - Page {self.page_number}"
```

```python
# apps/progress/models.py
from django.db import models
from apps.core.models import TimeStampedModel
from apps.children.models import Child
from apps.stories.models import Story


class Progress(TimeStampedModel):
    """Reading progress for a child on a story."""
    
    class Status(models.TextChoices):
        NOT_STARTED = 'NOT_STARTED', 'Not Started'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
    
    child = models.ForeignKey(
        Child,
        on_delete=models.CASCADE,
        related_name='progress_records'
    )
    story = models.ForeignKey(
        Story,
        on_delete=models.CASCADE,
        related_name='progress_records'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NOT_STARTED
    )
    current_page = models.IntegerField(default=0)
    pages_completed = models.IntegerField(default=0)
    time_spent_seconds = models.IntegerField(default=0)
    points_earned = models.IntegerField(default=0)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'progress'
        unique_together = ['child', 'story']
        indexes = [
            models.Index(fields=['child', 'status']),
            models.Index(fields=['story']),
        ]
        verbose_name_plural = 'progress records'
    
    def __str__(self):
        return f"{self.child.name} - {self.story.title} ({self.status})"


class DailyActivity(TimeStampedModel):
    """Aggregated daily activity for analytics."""
    
    child = models.ForeignKey(
        Child,
        on_delete=models.CASCADE,
        related_name='daily_activities'
    )
    date = models.DateField()
    stories_started = models.IntegerField(default=0)
    stories_completed = models.IntegerField(default=0)
    pages_read = models.IntegerField(default=0)
    time_spent_seconds = models.IntegerField(default=0)
    points_earned = models.IntegerField(default=0)
    recordings_made = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'daily_activities'
        unique_together = ['child', 'date']
        indexes = [
            models.Index(fields=['child', 'date']),
        ]
    
    def __str__(self):
        return f"{self.child.name} - {self.date}"
```

```python
# apps/gamification/models.py
from django.db import models
from apps.core.models import TimeStampedModel
from apps.children.models import Child


class Badge(TimeStampedModel):
    """Achievement badges that children can earn."""
    
    class CriteriaType(models.TextChoices):
        STORIES_COMPLETED = 'STORIES_COMPLETED', 'Stories Completed'
        STREAK_DAYS = 'STREAK_DAYS', 'Streak Days'
        POINTS_EARNED = 'POINTS_EARNED', 'Points Earned'
        TIME_SPENT_MINUTES = 'TIME_SPENT_MINUTES', 'Time Spent (Minutes)'
        VOICE_RECORDINGS = 'VOICE_RECORDINGS', 'Voice Recordings'
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50)
    criteria_type = models.CharField(max_length=30, choices=CriteriaType.choices)
    criteria_value = models.IntegerField()
    display_order = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'badges'
        ordering = ['display_order']
    
    def __str__(self):
        return self.name


class ChildBadge(TimeStampedModel):
    """Junction table for badges earned by children."""
    
    child = models.ForeignKey(
        Child,
        on_delete=models.CASCADE,
        related_name='earned_badges'
    )
    badge = models.ForeignKey(
        Badge,
        on_delete=models.CASCADE,
        related_name='child_badges'
    )
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'child_badges'
        unique_together = ['child', 'badge']
        indexes = [
            models.Index(fields=['child']),
        ]
    
    def __str__(self):
        return f"{self.child.name} - {self.badge.name}"


class Streak(TimeStampedModel):
    """Streak tracking for daily activity."""
    
    child = models.OneToOneField(
        Child,
        on_delete=models.CASCADE,
        related_name='streak'
    )
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = 'streaks'
    
    def __str__(self):
        return f"{self.child.name} - {self.current_streak} days"


class VoiceRecording(TimeStampedModel):
    """Voice recordings made by children."""
    
    child = models.ForeignKey(
        Child,
        on_delete=models.CASCADE,
        related_name='voice_recordings'
    )
    story = models.ForeignKey(
        'stories.Story',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    page_number = models.IntegerField(null=True, blank=True)
    audio_url = models.URLField()
    duration_ms = models.IntegerField()
    transcription = models.TextField(blank=True, null=True)
    confidence_score = models.FloatField(null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'voice_recordings'
        indexes = [
            models.Index(fields=['child']),
            models.Index(fields=['recorded_at']),
        ]
    
    def __str__(self):
        return f"{self.child.name} - Recording {self.id}"
```

---

## 🔌 API Specification

### Authentication Endpoints

```
POST   /api/v1/auth/register/     - Register new parent
POST   /api/v1/auth/login/        - Login (returns JWT)
POST   /api/v1/auth/logout/       - Logout (blacklist token)
POST   /api/v1/auth/refresh/      - Refresh JWT token
GET    /api/v1/auth/me/           - Get current user
PATCH  /api/v1/auth/me/           - Update current user
POST   /api/v1/auth/password/reset/    - Request password reset
POST   /api/v1/auth/password/confirm/  - Confirm password reset
```

### Children Endpoints

```
GET    /api/v1/children/          - List parent's children
POST   /api/v1/children/          - Create child profile
GET    /api/v1/children/{id}/     - Get child details
PATCH  /api/v1/children/{id}/     - Update child profile
DELETE /api/v1/children/{id}/     - Soft delete child
```

### Stories Endpoints

```
GET    /api/v1/stories/           - List stories (filterable)
GET    /api/v1/stories/{id}/      - Get story with pages
GET    /api/v1/stories/{id}/pages/ - Get story pages only
```

### Progress Endpoints

```
GET    /api/v1/children/{child_id}/progress/      - Get all progress
POST   /api/v1/children/{child_id}/progress/      - Start/update progress
GET    /api/v1/children/{child_id}/progress/{story_id}/ - Get specific progress
GET    /api/v1/children/{child_id}/stats/         - Get aggregated stats
```

### Gamification Endpoints

```
GET    /api/v1/children/{child_id}/badges/        - Get badges (earned + available)
GET    /api/v1/children/{child_id}/streak/        - Get streak info
GET    /api/v1/children/{child_id}/leaderboard/   - Get family leaderboard (future)
```

### Speech Endpoints

```
POST   /api/v1/speech/tts/        - Generate text-to-speech
POST   /api/v1/speech/stt/        - Speech to text (pronunciation check)
```

### Voice Recording Endpoints

```
GET    /api/v1/children/{child_id}/recordings/    - List recordings
POST   /api/v1/children/{child_id}/recordings/    - Save recording
DELETE /api/v1/children/{child_id}/recordings/{id}/ - Delete recording
```

---

## 🔧 Implementation Tasks

Execute these tasks in order. Each task is self-contained.

---

### PHASE 1: PROJECT SETUP (Day 1-2)

#### TASK-001: Initialize Django Project

```bash
# Create project directory
mkdir bhashamitra-backend && cd bhashamitra-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install initial dependencies
pip install django djangorestframework django-cors-headers psycopg2-binary python-dotenv

# Create Django project
django-admin startproject config .

# Create apps directory
mkdir apps && touch apps/__init__.py
```

**Create `requirements/base.txt`:**
```
Django>=5.0,<6.0
djangorestframework>=3.14,<4.0
django-cors-headers>=4.3,<5.0
django-filter>=23.5,<24.0
djangorestframework-simplejwt>=5.3,<6.0
psycopg2-binary>=2.9,<3.0
python-dotenv>=1.0,<2.0
gunicorn>=21.0,<22.0
whitenoise>=6.6,<7.0
Pillow>=10.0,<11.0
requests>=2.31,<3.0
boto3>=1.34,<2.0  # For S3/R2 storage
django-storages>=1.14,<2.0
celery>=5.3,<6.0  # For async tasks
redis>=5.0,<6.0
```

**Create `requirements/dev.txt`:**
```
-r base.txt
pytest>=7.4,<8.0
pytest-django>=4.7,<5.0
pytest-cov>=4.1,<5.0
factory-boy>=3.3,<4.0
faker>=22.0,<23.0
black>=23.12,<24.0
isort>=5.13,<6.0
flake8>=7.0,<8.0
django-debug-toolbar>=4.2,<5.0
ipython>=8.18,<9.0
```

**Create `requirements/prod.txt`:**
```
-r base.txt
sentry-sdk>=1.38,<2.0
django-health-check>=3.17,<4.0
```

---

#### TASK-002: Configure Settings

**Create `config/settings/base.py`:**
```python
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

# REST Framework
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
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}

# CORS Settings
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:3000').split(',')
CORS_ALLOW_CREDENTIALS = True

# Bhashini API
BHASHINI_USER_ID = os.getenv('BHASHINI_USER_ID', '')
BHASHINI_API_KEY = os.getenv('BHASHINI_API_KEY', '')
BHASHINI_PIPELINE_ID = os.getenv('BHASHINI_PIPELINE_ID', '')

# StoryWeaver
STORYWEAVER_BASE_URL = 'https://storyweaver.org.in/api/v1'

# Points Configuration
POINTS_CONFIG = {
    'STORY_STARTED': 10,
    'PAGE_READ': 5,
    'STORY_COMPLETED_BASE': 50,
    'VOICE_RECORDING': 15,
}

# Level Thresholds
LEVEL_THRESHOLDS = {
    1: 0,
    2: 501,
    3: 1501,
    4: 3501,
    5: 7001,
}

# App Constants
MAX_CHILDREN_PER_USER = 5
```

**Create `config/settings/dev.py`:**
```python
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
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'apps': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
```

**Create `config/settings/prod.py`:**
```python
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
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}

# Sentry Error Tracking
sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.1,
    send_default_pii=False,
)

# Email (Production)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@bhashamitra.co.nz')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            'class': 'pythonjsonlogger.jsonlogger.JsonFormatter',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}
```

**Create `config/settings/__init__.py`:**
```python
import os

environment = os.getenv('DJANGO_ENV', 'dev')

if environment == 'prod':
    from .prod import *
else:
    from .dev import *
```

---

#### TASK-003: Create Core App

**Create `apps/core/pagination.py`:**
```python
from rest_framework.pagination import CursorPagination as BaseCursorPagination


class CursorPagination(BaseCursorPagination):
    page_size = 20
    page_size_query_param = 'limit'
    max_page_size = 50
    ordering = '-created_at'
```

**Create `apps/core/permissions.py`:**
```python
from rest_framework import permissions


class IsParentOfChild(permissions.BasePermission):
    """Permission to check if user is the parent of the child."""
    
    def has_object_permission(self, request, view, obj):
        # obj can be Child or any model with child FK
        if hasattr(obj, 'user'):
            return obj.user == request.user
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

**Create `apps/core/exceptions.py`:**
```python
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
    
    # Format according to RFC 7807
    error_response = {
        'type': f'https://bhashamitra.co.nz/errors/{get_error_type(response.status_code)}',
        'title': get_error_title(response.status_code),
        'status': response.status_code,
        'detail': get_error_detail(response.data),
    }
    
    if isinstance(response.data, dict) and 'errors' in response.data:
        error_response['errors'] = response.data['errors']
    
    response.data = error_response
    return response


def get_error_type(status_code):
    types = {
        400: 'validation',
        401: 'unauthorized',
        403: 'forbidden',
        404: 'not-found',
        409: 'conflict',
        429: 'rate-limited',
        500: 'internal',
        503: 'unavailable',
    }
    return types.get(status_code, 'error')


def get_error_title(status_code):
    titles = {
        400: 'Validation Error',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found',
        409: 'Conflict',
        429: 'Rate Limited',
        500: 'Internal Server Error',
        503: 'Service Unavailable',
    }
    return titles.get(status_code, 'Error')


def get_error_detail(data):
    if isinstance(data, dict):
        if 'detail' in data:
            return data['detail']
        if 'non_field_errors' in data:
            return data['non_field_errors'][0]
        # Return first error message
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


class PermissionDeniedError(AppException):
    status_code = status.HTTP_403_FORBIDDEN
    default_message = 'Permission denied'
```

**Create `apps/core/utils.py`:**
```python
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

#### TASK-004: Create Users App

**Create `apps/users/serializers.py`:**
```python
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user details."""
    
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'role', 'avatar_url', 'created_at']
        read_only_fields = ['id', 'role', 'created_at']


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    
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
            username=validated_data['email'],  # Use email as username
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
        )
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class PasswordResetSerializer(serializers.Serializer):
    """Serializer for password reset request."""
    
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Serializer for password reset confirmation."""
    
    token = serializers.CharField()
    password = serializers.CharField(validators=[validate_password])
    password_confirm = serializers.CharField()
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password_confirm': 'Passwords do not match'})
        return attrs
```

**Create `apps/users/views.py`:**
```python
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import authenticate, get_user_model

from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
)

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
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'data': UserSerializer(user).data,
            'session': {
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            },
            'meta': {
                'message': 'Registration successful'
            }
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
            pass  # Token already blacklisted or invalid
        
        return Response({
            'meta': {
                'message': 'Logged out successfully'
            }
        })


class MeView(generics.RetrieveUpdateAPIView):
    """Get or update current user."""
    
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class CustomTokenRefreshView(TokenRefreshView):
    """Custom token refresh view."""
    
    throttle_scope = 'auth'
```

**Create `apps/users/urls.py`:**
```python
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('me/', views.MeView.as_view(), name='me'),
]
```

**Create `apps/users/admin.py`:**
```python
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

### PHASE 2: CORE FEATURES (Day 3-10)

Continue implementing remaining apps following the same pattern:
- `apps/children/` - Child profile management
- `apps/stories/` - Story library and caching
- `apps/progress/` - Reading progress tracking
- `apps/gamification/` - Points, streaks, badges
- `apps/speech/` - Bhashini TTS/STT integration

---

## 🔗 URL Configuration

**Update `config/urls.py`:**
```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API v1
    path('api/v1/auth/', include('apps.users.urls', namespace='auth')),
    path('api/v1/children/', include('apps.children.urls', namespace='children')),
    path('api/v1/stories/', include('apps.stories.urls', namespace='stories')),
    path('api/v1/speech/', include('apps.speech.urls', namespace='speech')),
    
    # Health check
    path('health/', include('health_check.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # Debug toolbar
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
```

---

## 🐳 Docker Configuration

**Create `docker/Dockerfile`:**
```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements/prod.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "config.wsgi:application"]
```

**Create `docker/docker-compose.yml`:**
```yaml
version: '3.8'

services:
  db:
    image: postgres:16
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: bhashamitra_dev
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  web:
    build:
      context: ..
      dockerfile: docker/Dockerfile.dev
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ..:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    environment:
      - DJANGO_ENV=dev
      - DB_HOST=db
      - DB_NAME=bhashamitra_dev
      - DB_USER=postgres
      - DB_PASSWORD=postgres
      - REDIS_URL=redis://redis:6379/0

volumes:
  postgres_data:
```

---

## 📋 Environment Variables

**Create `.env.example`:**
```bash
# Django
DJANGO_ENV=dev
SECRET_KEY=your-secret-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=bhashamitra_dev
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000

# Bhashini API
BHASHINI_USER_ID=
BHASHINI_API_KEY=
BHASHINI_PIPELINE_ID=

# Email (Development uses console backend)
EMAIL_HOST=
EMAIL_PORT=587
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=noreply@bhashamitra.co.nz

# Sentry (Production only)
SENTRY_DSN=

# Storage (Production)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
AWS_S3_ENDPOINT_URL=  # For Cloudflare R2
```

---

## 🧪 Testing Setup

**Create `pytest.ini`:**
```ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings.dev
python_files = tests.py test_*.py *_tests.py
addopts = -v --tb=short --strict-markers
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
```

**Create `apps/users/tests/test_views.py`:**
```python
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.users.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_data():
    return {
        'email': 'test@example.com',
        'name': 'Test User',
        'password': 'testpassword123',
        'password_confirm': 'testpassword123',
    }


@pytest.mark.django_db
class TestRegistration:
    
    def test_register_success(self, api_client, user_data):
        url = reverse('auth:register')
        response = api_client.post(url, user_data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert 'access_token' in response.data['session']
        assert response.data['data']['email'] == user_data['email']
    
    def test_register_duplicate_email(self, api_client, user_data):
        User.objects.create_user(
            username=user_data['email'],
            email=user_data['email'],
            name=user_data['name'],
            password=user_data['password'],
        )
        
        url = reverse('auth:register')
        response = api_client.post(url, user_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_register_password_mismatch(self, api_client, user_data):
        user_data['password_confirm'] = 'differentpassword'
        
        url = reverse('auth:register')
        response = api_client.post(url, user_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestLogin:
    
    def test_login_success(self, api_client, user_data):
        # Create user first
        User.objects.create_user(
            username=user_data['email'],
            email=user_data['email'],
            name=user_data['name'],
            password=user_data['password'],
        )
        
        url = reverse('auth:login')
        response = api_client.post(url, {
            'email': user_data['email'],
            'password': user_data['password'],
        }, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access_token' in response.data['data']['session']
    
    def test_login_invalid_credentials(self, api_client):
        url = reverse('auth:login')
        response = api_client.post(url, {
            'email': 'wrong@example.com',
            'password': 'wrongpassword',
        }, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
```

---

## 🚀 Getting Started Commands

```bash
# 1. Clone and setup
git clone <your-repo>
cd bhashamitra-backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements/dev.txt

# 4. Copy environment variables
cp .env.example .env
# Edit .env with your values

# 5. Start PostgreSQL (via Docker or local)
docker-compose -f docker/docker-compose.yml up -d db

# 6. Run migrations
python manage.py migrate

# 7. Create superuser
python manage.py createsuperuser

# 8. Seed initial data
python manage.py seed_badges

# 9. Run development server
python manage.py runserver

# 10. Run tests
pytest
```

---

## 📝 Implementation Checklist

### Phase 1: Foundation (Day 1-2)
- [ ] TASK-001: Initialize Django project
- [ ] TASK-002: Configure settings (base, dev, prod)
- [ ] TASK-003: Create core app (pagination, permissions, exceptions)
- [ ] TASK-004: Create users app (models, serializers, views)
- [ ] TASK-005: Setup Docker and docker-compose
- [ ] TASK-006: Configure pytest

### Phase 2: Core Features (Day 3-10)
- [ ] TASK-007: Create children app
- [ ] TASK-008: Create stories app with StoryWeaver integration
- [ ] TASK-009: Create progress app
- [ ] TASK-010: Create gamification app (points, streaks, badges)
- [ ] TASK-011: Create speech app with Bhashini integration
- [ ] TASK-012: Implement voice recordings

### Phase 3: Polish & Deploy (Day 11-14)
- [ ] TASK-013: Write comprehensive tests
- [ ] TASK-014: Setup CI/CD pipeline
- [ ] TASK-015: Configure production deployment
- [ ] TASK-016: Security audit and hardening

---

## ⚠️ Important Development Notes

1. **Always create `__init__.py`** files in every Python package directory
2. **Run migrations** after creating/modifying models: `python manage.py makemigrations && python manage.py migrate`
3. **Follow Django REST Framework patterns** for serializers and views
4. **Use type hints** for better code clarity
5. **Write docstrings** for all classes and complex functions
6. **Log errors appropriately** - use the configured logging
7. **Never commit `.env`** files or secrets
8. **Test your code** - run pytest after implementing each feature

---

## 🤝 Support

If you encounter issues:
1. Check Django documentation: https://docs.djangoproject.com/
2. Check DRF documentation: https://www.django-rest-framework.org/
3. Review error logs in console
4. Ask for clarification with specific error messages

**Remember**: Build incrementally, test frequently, commit often.
