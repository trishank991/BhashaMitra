"""
Management command to seed Peppi Mimic challenges with sample words.

This creates pronunciation challenges for each language and generates
reference audio using TTS.
"""

import os
import logging
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import transaction

from apps.speech.models import PeppiMimicChallenge, AudioCache
from apps.speech.services.tts_service import TTSService, TTSServiceError

logger = logging.getLogger(__name__)


# Sample words for each language
MIMIC_CHALLENGE_DATA = {
    'HINDI': [
        {'word': 'नमस्ते', 'romanization': 'namaste', 'meaning': 'Hello', 'category': 'GREETING'},
        {'word': 'धन्यवाद', 'romanization': 'dhanyavaad', 'meaning': 'Thank you', 'category': 'GREETING'},
        {'word': 'माता', 'romanization': 'maata', 'meaning': 'Mother', 'category': 'FAMILY'},
        {'word': 'पिता', 'romanization': 'pita', 'meaning': 'Father', 'category': 'FAMILY'},
        {'word': 'भाई', 'romanization': 'bhaai', 'meaning': 'Brother', 'category': 'FAMILY'},
        {'word': 'बहन', 'romanization': 'bahen', 'meaning': 'Sister', 'category': 'FAMILY'},
        {'word': 'एक', 'romanization': 'ek', 'meaning': 'One', 'category': 'NUMBERS'},
        {'word': 'दो', 'romanization': 'do', 'meaning': 'Two', 'category': 'NUMBERS'},
        {'word': 'तीन', 'romanization': 'teen', 'meaning': 'Three', 'category': 'NUMBERS'},
        {'word': 'लाल', 'romanization': 'laal', 'meaning': 'Red', 'category': 'COLORS'},
        {'word': 'नीला', 'romanization': 'neela', 'meaning': 'Blue', 'category': 'COLORS'},
        {'word': 'हरा', 'romanization': 'hara', 'meaning': 'Green', 'category': 'COLORS'},
        {'word': 'केला', 'romanization': 'kela', 'meaning': 'Banana', 'category': 'FOOD'},
        {'word': 'आम', 'romanization': 'aam', 'meaning': 'Mango', 'category': 'FOOD'},
        {'word': 'पानी', 'romanization': 'paani', 'meaning': 'Water', 'category': 'FOOD'},
    ],
    'TAMIL': [
        {'word': 'வணக்கம்', 'romanization': 'vanakkam', 'meaning': 'Hello', 'category': 'GREETING'},
        {'word': 'நன்றி', 'romanization': 'nandri', 'meaning': 'Thank you', 'category': 'GREETING'},
        {'word': 'அம்மா', 'romanization': 'amma', 'meaning': 'Mother', 'category': 'FAMILY'},
        {'word': 'அப்பா', 'romanization': 'appa', 'meaning': 'Father', 'category': 'FAMILY'},
        {'word': 'ஒன்று', 'romanization': 'onru', 'meaning': 'One', 'category': 'NUMBERS'},
        {'word': 'இரண்டு', 'romanization': 'irandu', 'meaning': 'Two', 'category': 'NUMBERS'},
        {'word': 'சிவப்பு', 'romanization': 'sivappu', 'meaning': 'Red', 'category': 'COLORS'},
        {'word': 'நீலம்', 'romanization': 'neelam', 'meaning': 'Blue', 'category': 'COLORS'},
    ],
    'GUJARATI': [
        {'word': 'નમસ્તે', 'romanization': 'namaste', 'meaning': 'Hello', 'category': 'GREETING'},
        {'word': 'ધન્યવાદ', 'romanization': 'dhanyavaad', 'meaning': 'Thank you', 'category': 'GREETING'},
        {'word': 'માતા', 'romanization': 'maata', 'meaning': 'Mother', 'category': 'FAMILY'},
        {'word': 'પિતा', 'romanization': 'pita', 'meaning': 'Father', 'category': 'FAMILY'},
        {'word': 'એક', 'romanization': 'ek', 'meaning': 'One', 'category': 'NUMBERS'},
        {'word': 'બે', 'romanization': 'be', 'meaning': 'Two', 'category': 'NUMBERS'},
        {'word': 'લાલ', 'romanization': 'laal', 'meaning': 'Red', 'category': 'COLORS'},
    ],
    'PUNJABI': [
        {'word': 'ਸਤ ਸ੍ਰੀ ਅਕਾਲ', 'romanization': 'sat sri akaal', 'meaning': 'Hello', 'category': 'GREETING'},
        {'word': 'ਧੰਨਵਾਦ', 'romanization': 'dhanyavaad', 'meaning': 'Thank you', 'category': 'GREETING'},
        {'word': 'ਮਾਂ', 'romanization': 'maa', 'meaning': 'Mother', 'category': 'FAMILY'},
        {'word': 'ਪਿਓ', 'romanization': 'pio', 'meaning': 'Father', 'category': 'FAMILY'},
    ],
}


class Command(BaseCommand):
    help = 'Seed Peppi Mimic challenges with sample words and generate reference audio'

    def add_arguments(self, parser):
        parser.add_argument(
            '--language',
            type=str,
            help='Specific language to seed (e.g., HINDI, TAMIL)',
        )
        parser.add_argument(
            '--skip-audio',
            action='store_true',
            help='Skip audio generation (faster, for testing)',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Recreate existing challenges',
        )

    def handle(self, *args, **options):
        language = options.get('language')
        skip_audio = options['skip_audio']
        force = options['force']

        if language:
            languages = [language.upper()]
        else:
            languages = list(MIMIC_CHALLENGE_DATA.keys())

        self.stdout.write(f"Seeding mimic challenges for: {', '.join(languages)}")

        total_created = 0
        total_audio = 0
        errors = []

        for lang in languages:
            if lang not in MIMIC_CHALLENGE_DATA:
                self.stdout.write(self.style.WARNING(f"Skipping unknown language: {lang}"))
                continue

            self.stdout.write(f"\n{'='*50}")
            self.stdout.write(f"Processing {lang}")
            self.stdout.write(f"{'='*50}")

            created, audio_count = self._seed_language(
                lang,
                MIMIC_CHALLENGE_DATA[lang],
                skip_audio,
                force,
                errors
            )

            total_created += created
            total_audio += audio_count

        # Summary
        self.stdout.write(f"\n{'='*50}")
        self.stdout.write("SEEDING COMPLETE")
        self.stdout.write(f"{'='*50}")
        self.stdout.write(f"Total challenges created: {total_created}")
        self.stdout.write(f"Total audio generated: {total_audio}")
        
        if errors:
            self.stdout.write(self.style.WARNING(f"\nErrors ({len(errors)}):"))
            for error in errors[:10]:  # Show first 10 errors
                self.stdout.write(f"  - {error}")
            if len(errors) > 10:
                self.stdout.write(f"  ... and {len(errors) - 10} more")

    def _seed_language(self, language, words, skip_audio, force, errors):
        """Seed challenges for a specific language."""
        from django.utils import timezone

        created = 0
        audio_count = 0

        for i, word_data in enumerate(words):
            try:
                with transaction.atomic():
                    # Check if challenge already exists
                    existing = PeppiMimicChallenge.objects.filter(
                        word=word_data['word'],
                        language=language
                    ).first()

                    if existing and not force:
                        self.stdout.write(f"  ⏭ Skipping '{word_data['word']}' (already exists)")
                        continue

                    # Create or update challenge
                    challenge, was_created = PeppiMimicChallenge.objects.update_or_create(
                        word=word_data['word'],
                        language=language,
                        defaults={
                            'romanization': word_data['romanization'],
                            'meaning': word_data['meaning'],
                            'category': word_data['category'],
                            'difficulty': 1,  # Easy for basic words
                            'display_order': i,
                            'peppi_intro': f"Listen carefully and repeat after me: {word_data['word']}",
                            'peppi_perfect': f"MEOW! Perfect! You said '{word_data['word']}' just like a native speaker!",
                            'peppi_good': f"Good try! Listen again and try to match Peppi's pronunciation.",
                            'peppi_try_again': "Let's practice together! Listen to Peppi and try again!",
                            'is_active': True,
                        }
                    )

                    if was_created:
                        created += 1
                        self.stdout.write(f"  ✓ Created: {word_data['word']} ({word_data['meaning']})")
                    elif force:
                        self.stdout.write(f"  ✓ Updated: {word_data['word']}")

                    # Generate reference audio
                    if not skip_audio:
                        audio_result = self._generate_audio(challenge)
                        if audio_result:
                            audio_count += 1
                            self.stdout.write(f"    🎵 Audio generated ({audio_result['duration_ms']}ms)")

            except Exception as e:
                error_msg = f"{language}/{word_data['word']}: {str(e)}"
                errors.append(error_msg)
                self.stdout.write(self.style.ERROR(f"  ✗ Error: {error_msg}"))

        return created, audio_count

    def _generate_audio(self, challenge):
        """Generate and cache TTS audio for a challenge word."""
        try:
            # Generate audio using TTS
            audio_bytes, provider, was_cached = TTSService.get_audio(
                text=challenge.word,
                language=challenge.language,
                voice_profile='kid_friendly',
            )

            if not audio_bytes:
                logger.warning(f"No audio generated for {challenge.word}")
                return None

            # Calculate duration (estimate based on word length)
            # For accurate duration, we'd need to use a library like mutagen
            estimated_duration_ms = len(challenge.word) * 150  # ~150ms per character

            # Get or create audio cache entry
            from django.core.files.base import ContentFile
            import hashlib

            text_hash = hashlib.md5(challenge.word.encode()).hexdigest()
            cache_key = f"mimic:{challenge.language}:{text_hash}"

            audio_cache, _ = AudioCache.objects.get_or_create(
                cache_key=cache_key,
                defaults={
                    'text_content': challenge.word,
                    'text_hash': text_hash,
                    'language': challenge.language,
                    'voice_style': 'kid_friendly',
                    'provider': provider,
                    'audio_size_bytes': len(audio_bytes),
                    'audio_duration_ms': estimated_duration_ms,
                    'content_type': 'mimic',
                    'content_id': str(challenge.id),
                }
            )

            # Save audio file
            if audio_cache.audio_file:
                # File already exists
                pass
            else:
                audio_cache.audio_file.save(
                    f"mimic_{challenge.id}.mp3",
                    ContentFile(audio_bytes),
                    save=True,
                )

            # Link challenge to audio cache
            challenge.audio_cache = audio_cache
            challenge.audio_url = audio_cache.audio_url or f"/media/{audio_cache.audio_file.name}"
            challenge.save(update_fields=['audio_cache', 'audio_url'])

            return {
                'provider': provider,
                'duration_ms': estimated_duration_ms,
                'cached': was_cached,
            }

        except TTSServiceError as e:
            logger.error(f"TTS error for {challenge.word}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error generating audio for {challenge.word}: {e}")
            return None