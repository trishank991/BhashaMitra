#!/usr/bin/env python
"""Test script to check for import errors and basic functionality."""
import sys
import os
import django

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

print("=" * 80)
print("BhashaMitra Backend - Import & Error Check")
print("=" * 80)

errors = []
warnings = []

# Test 1: Check critical imports
print("\n[1] Testing critical imports...")
try:
    from apps.users.models import User
    print("✓ apps.users.models.User")
except Exception as e:
    errors.append(f"apps.users.models.User: {e}")
    print(f"✗ apps.users.models.User: {e}")

try:
    from apps.children.models import Child
    print("✓ apps.children.models.Child")
except Exception as e:
    errors.append(f"apps.children.models.Child: {e}")
    print(f"✗ apps.children.models.Child: {e}")

try:
    from apps.speech.models import AudioCache, TTSUsageLog
    print("✓ apps.speech.models.AudioCache, TTSUsageLog")
except Exception as e:
    errors.append(f"apps.speech.models: {e}")
    print(f"✗ apps.speech.models: {e}")

try:
    from apps.speech.services.tts_service import TTSService
    print("✓ apps.speech.services.tts_service.TTSService")
except Exception as e:
    errors.append(f"TTSService: {e}")
    print(f"✗ TTSService: {e}")

try:
    from apps.speech.services.sarvam_provider import SarvamAIProvider
    print("✓ apps.speech.services.sarvam_provider.SarvamAIProvider")
except Exception as e:
    errors.append(f"SarvamAIProvider: {e}")
    print(f"✗ SarvamAIProvider: {e}")

try:
    from apps.speech.services.mms_provider import SvaraTTSProvider
    print("✓ apps.speech.services.mms_provider.SvaraTTSProvider")
except Exception as e:
    errors.append(f"SvaraTTSProvider: {e}")
    print(f"✗ SvaraTTSProvider: {e}")

try:
    from apps.speech.views import TextToSpeechView, StoryPageAudioView
    print("✓ apps.speech.views")
except Exception as e:
    errors.append(f"apps.speech.views: {e}")
    print(f"✗ apps.speech.views: {e}")

try:
    from apps.curriculum.views.alphabet import ScriptListView
    print("✓ apps.curriculum.views.alphabet")
except Exception as e:
    errors.append(f"apps.curriculum.views.alphabet: {e}")
    print(f"✗ apps.curriculum.views.alphabet: {e}")

try:
    from apps.curriculum.views.vocabulary import VocabularyThemeListView
    print("✓ apps.curriculum.views.vocabulary")
except Exception as e:
    errors.append(f"apps.curriculum.views.vocabulary: {e}")
    print(f"✗ apps.curriculum.views.vocabulary: {e}")

try:
    from apps.children.views import ChildListCreateView
    print("✓ apps.children.views")
except Exception as e:
    errors.append(f"apps.children.views: {e}")
    print(f"✗ apps.children.views: {e}")

# Test 2: Check TTS tier mapping
print("\n[2] Testing TTS tier mapping...")
try:
    from apps.users.models import User

    # Create a test user (without saving)
    test_user_free = User(
        email='test@example.com',
        name='Test User',
        subscription_tier='FREE'
    )

    if test_user_free.tts_provider != 'cache_only':
        errors.append(f"FREE tier should map to 'cache_only', got '{test_user_free.tts_provider}'")
        print(f"✗ FREE tier mapping incorrect: {test_user_free.tts_provider}")
    else:
        print(f"✓ FREE tier → {test_user_free.tts_provider}")

    test_user_standard = User(
        email='test2@example.com',
        name='Test User 2',
        subscription_tier='STANDARD'
    )

    if test_user_standard.tts_provider != 'svara':
        errors.append(f"STANDARD tier should map to 'svara', got '{test_user_standard.tts_provider}'")
        print(f"✗ STANDARD tier mapping incorrect: {test_user_standard.tts_provider}")
    else:
        print(f"✓ STANDARD tier → {test_user_standard.tts_provider}")

    test_user_premium = User(
        email='test3@example.com',
        name='Test User 3',
        subscription_tier='PREMIUM'
    )

    if test_user_premium.tts_provider != 'sarvam':
        errors.append(f"PREMIUM tier should map to 'sarvam', got '{test_user_premium.tts_provider}'")
        print(f"✗ PREMIUM tier mapping incorrect: {test_user_premium.tts_provider}")
    else:
        print(f"✓ PREMIUM tier → {test_user_premium.tts_provider}")

except Exception as e:
    errors.append(f"TTS tier mapping test failed: {e}")
    print(f"✗ TTS tier mapping test failed: {e}")

# Test 3: Check TTS service logic
print("\n[3] Testing TTS service routing logic...")
try:
    from apps.speech.services.tts_service import TTSService

    # Check supported languages
    languages = TTSService.get_supported_languages()
    if not languages:
        warnings.append("TTSService.get_supported_languages() returned empty list")
        print(f"⚠ No supported languages found")
    else:
        print(f"✓ Supported languages: {', '.join(languages)}")

    # Check service status
    status_info = TTSService.check_service_status()
    if 'providers' not in status_info:
        warnings.append("Service status missing 'providers' key")
        print(f"⚠ Service status format incorrect")
    else:
        print(f"✓ Service status check working")
        for provider in status_info.get('providers', []):
            print(f"  - {provider.get('name')}: {'available' if provider.get('available') else 'unavailable'}")

except Exception as e:
    errors.append(f"TTS service logic test failed: {e}")
    print(f"✗ TTS service logic test failed: {e}")

# Test 4: Check for missing environment variables
print("\n[4] Checking environment variables...")
try:
    import os

    required_vars = {
        'SECRET_KEY': os.getenv('SECRET_KEY'),
        'DJANGO_ENV': os.getenv('DJANGO_ENV'),
    }

    optional_vars = {
        'SARVAM_API_KEY': os.getenv('SARVAM_API_KEY'),
        'HUGGINGFACE_API_TOKEN': os.getenv('HUGGINGFACE_API_TOKEN'),
    }

    for var, value in required_vars.items():
        if not value:
            warnings.append(f"Required env var '{var}' not set")
            print(f"⚠ {var}: NOT SET (required)")
        else:
            print(f"✓ {var}: SET")

    for var, value in optional_vars.items():
        if not value:
            print(f"⚠ {var}: NOT SET (optional)")
        else:
            print(f"✓ {var}: SET")

except Exception as e:
    warnings.append(f"Environment variable check failed: {e}")
    print(f"⚠ Environment variable check failed: {e}")

# Test 5: Check for common security issues
print("\n[5] Security checks...")
try:
    from django.conf import settings

    # Check DEBUG setting
    if settings.DEBUG:
        warnings.append("DEBUG=True (should be False in production)")
        print(f"⚠ DEBUG=True (development mode)")
    else:
        print(f"✓ DEBUG=False (production mode)")

    # Check SECRET_KEY
    if settings.SECRET_KEY == 'change-me-in-production':
        warnings.append("SECRET_KEY is using default value")
        print(f"⚠ SECRET_KEY is using default value (change in production)")
    else:
        print(f"✓ SECRET_KEY is customized")

except Exception as e:
    warnings.append(f"Security check failed: {e}")
    print(f"⚠ Security check failed: {e}")

# Summary
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

if not errors and not warnings:
    print("✓ All checks passed! No errors or warnings found.")
    sys.exit(0)
else:
    if errors:
        print(f"\n✗ {len(errors)} ERROR(S) FOUND:")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")

    if warnings:
        print(f"\n⚠ {len(warnings)} WARNING(S) FOUND:")
        for i, warning in enumerate(warnings, 1):
            print(f"  {i}. {warning}")

    if errors:
        sys.exit(1)
    else:
        sys.exit(0)
