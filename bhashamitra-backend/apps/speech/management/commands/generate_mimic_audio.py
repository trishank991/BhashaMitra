#!/usr/bin/env python
"""
Management command to generate audio for all PeppiMimicChallenge words.

This ensures each pronunciation challenge has a reference audio that children
can listen to before attempting to mimic.
"""
import logging
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from apps.speech.models import PeppiMimicChallenge
from apps.speech.services.tts_service import TTSService

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Generate audio for all PeppiMimicChallenge words'

    def add_arguments(self, parser):
        parser.add_argument(
            '--regenerate',
            action='store_true',
            help='Regenerate audio even if already exists',
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=None,
            help='Limit number of challenges to process',
        )
        parser.add_argument(
            '--language',
            type=str,
            default='HINDI',
            help='Language for TTS (default: HINDI)',
        )

    def handle(self, *args, **options):
        regenerate = options['regenerate']
        limit = options['limit']
        language = options['language']

        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('GENERATING MIMIC CHALLENGE AUDIO'))
        self.stdout.write(self.style.SUCCESS('=' * 60))

        # Get challenges
        queryset = PeppiMimicChallenge.objects.filter(is_active=True)

        if language != 'ALL':
            queryset = queryset.filter(language=language)

        if limit:
            queryset = queryset[:limit]

        total = queryset.count()
        self.stdout.write(f'\nTotal challenges to process: {total}')

        success_count = 0
        skip_count = 0
        error_count = 0

        for idx, challenge in enumerate(queryset, 1):
            # Check if audio already exists
            if challenge.audio_url and not regenerate:
                self.stdout.write(
                    f'[{idx}/{total}] SKIP: {challenge.word} - audio already exists'
                )
                skip_count += 1
                continue

            self.stdout.write(f'[{idx}/{total}] Processing: {challenge.word} ({challenge.language})...')

            try:
                # Generate TTS audio
                audio_bytes, provider, was_cached = TTSService.get_audio(
                    text=challenge.word,
                    language=challenge.language,
                    voice_profile='kid_friendly',  # Kid-friendly voice for mimic challenges
                )

                # Save audio file
                filename = f"mimic_reference/{challenge.language.lower()}/{challenge.id}.mp3"
                saved_path = default_storage.save(filename, ContentFile(audio_bytes))

                # Get URL
                if hasattr(default_storage, 'url'):
                    audio_url = default_storage.url(saved_path)
                else:
                    audio_url = f"/media/{saved_path}"

                # Make URL absolute
                if audio_url.startswith('/'):
                    from django.conf import settings
                    base_url = getattr(settings, 'SITE_URL', 'http://localhost:8000')
                    audio_url = f"{base_url.rstrip('/')}{audio_url}"

                # Update challenge
                challenge.audio_url = audio_url
                challenge.save(update_fields=['audio_url'])

                self.stdout.write(
                    self.style.SUCCESS(f'  ✓ Generated: {audio_url[:60]}...')
                )
                success_count += 1

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'  ✗ Error: {str(e)}')
                )
                error_count += 1
                logger.exception(f"Failed to generate audio for {challenge.word}")

        # Summary
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('SUMMARY'))
        self.stdout.write('=' * 60)
        self.stdout.write(f'Total processed: {total}')
        self.stdout.write(self.style.SUCCESS(f'Success: {success_count}'))
        self.stdout.write(self.style.WARNING(f'Skipped (already has audio): {skip_count}'))
        self.stdout.write(self.style.ERROR(f'Errors: {error_count}'))

        # Verify
        remaining = PeppiMimicChallenge.objects.filter(
            is_active=True,
            audio_url='',
        ).exclude(audio_url__isnull=True).count()

        if remaining > 0:
            self.stdout.write(
                self.style.WARNING(f'\n⚠ {remaining} challenges still missing audio')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('\n✓ All challenges have audio!')
            )