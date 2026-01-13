#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
sys.path.insert(0, '/home/trishank/BhashaMitra/bhashamitra-backend')
django.setup()

from apps.speech.models import PeppiMimicChallenge

print("=" * 60)
print("MIMIC FEATURE AUDIO URL CHECK")
print("=" * 60)

challenges = PeppiMimicChallenge.objects.filter(is_active=True)
total = challenges.count()
with_audio = challenges.exclude(audio_url='').exclude(audio_url__isnull=True).count()

print(f"\nTotal active challenges: {total}")
print(f"Challenges with audio_url: {with_audio}")
print(f"Challenges missing audio_url: {total - with_audio}")

if total > 0:
    print("\nFirst 5 challenges:")
    for c in challenges[:5]:
        audio_status = c.audio_url[:50] + "..." if c.audio_url and len(c.audio_url) > 50 else (c.audio_url or "EMPTY")
        print(f"  - {c.word} (ID: {c.id})")
        print(f"    audio_url: {audio_status}")

print("\n" + "=" * 60)
print("CHECK COMPLETE")
print("=" * 60)