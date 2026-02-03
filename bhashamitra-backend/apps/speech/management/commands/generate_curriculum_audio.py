"""
Pre-generate TTS audio for curriculum content.
Run this before launch to cache all known content.

Usage:
    python manage.py generate_curriculum_audio --language=HINDI
    python manage.py generate_curriculum_audio --language=HINDI --content-type=alphabet
    python manage.py generate_curriculum_audio --dry-run
"""
import time
from django.core.management.base import BaseCommand
from apps.speech.services.tts_service import TTSService, TTSServiceError


class Command(BaseCommand):
    help = 'Pre-generate TTS audio for curriculum content'

    def add_arguments(self, parser):
        parser.add_argument(
            '--language',
            type=str,
            default='HINDI',
            help='Language to generate (HINDI, TAMIL, etc.)',
        )
        parser.add_argument(
            '--content-type',
            type=str,
            default='all',
            choices=['all', 'alphabet', 'vocabulary', 'phrases'],
            help='Type of content to generate',
        )
        parser.add_argument(
            '--voice-profile',
            type=str,
            default='kid_friendly',
            help='Voice profile to use',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be generated without actually generating',
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=0,
            help='Limit number of items to generate (0 = no limit)',
        )

    def handle(self, *args, **options):
        language = options['language']
        content_type = options['content_type']
        voice_profile = options['voice_profile']
        dry_run = options['dry_run']
        limit = options['limit']

        self.stdout.write(f"\n{'='*60}")
        self.stdout.write(f"Pre-generating {language} audio ({content_type})")
        self.stdout.write(f"Voice profile: {voice_profile}")
        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN - No audio will be generated"))
        self.stdout.write(f"{'='*60}\n")

        # Collect items to generate
        items = self._collect_items(language, content_type)

        if limit > 0:
            items = items[:limit]

        self.stdout.write(f"Found {len(items)} items to generate\n")

        if dry_run:
            for item in items[:20]:
                self.stdout.write(f"  [{item['type']}] {item['text'][:50]}...")
            if len(items) > 20:
                self.stdout.write(f"  ... and {len(items) - 20} more")
            return

        # Generate audio
        generated = 0
        cached = 0
        failed = 0

        for i, item in enumerate(items):
            try:
                self.stdout.write(
                    f"[{i+1}/{len(items)}] {item['type']}: {item['text'][:30]}... ",
                    ending=''
                )

                audio, provider, was_cached = TTSService.get_audio(
                    text=item['text'],
                    language=language,
                    voice_profile=voice_profile,
                )

                if was_cached:
                    cached += 1
                    self.stdout.write(self.style.WARNING('(cached)'))
                else:
                    generated += 1
                    self.stdout.write(self.style.SUCCESS(f'OK ({provider})'))
                    # Rate limiting to avoid overwhelming the TTS service
                    time.sleep(1)

            except TTSServiceError as e:
                failed += 1
                self.stdout.write(self.style.ERROR(f'FAILED: {str(e)[:50]}'))

        # Summary
        self.stdout.write(f"\n{'='*60}")
        self.stdout.write(f"Summary:")
        self.stdout.write(f"  Generated: {generated}")
        self.stdout.write(f"  Already cached: {cached}")
        self.stdout.write(f"  Failed: {failed}")
        self.stdout.write(f"{'='*60}\n")

    def _collect_items(self, language: str, content_type: str) -> list:
        """Collect items to generate from database."""
        items = []

        if content_type in ['all', 'alphabet']:
            items.extend(self._collect_alphabet(language))

        if content_type in ['all', 'vocabulary']:
            items.extend(self._collect_vocabulary(language))

        if content_type in ['all', 'phrases']:
            items.extend(self._collect_phrases(language))

        return items

    def _collect_alphabet(self, language: str) -> list:
        """Collect alphabet letters."""
        items = []

        try:
            from apps.curriculum.models import Letter
            # Letter is linked via category -> script -> language
            letters = Letter.objects.filter(category__script__language=language)

            for letter in letters:
                items.append({
                    'text': letter.character,
                    'type': 'letter',
                    'id': str(letter.id),
                })
                if hasattr(letter, 'pronunciation_text') and letter.pronunciation_text:
                    items.append({
                        'text': letter.pronunciation_text,
                        'type': 'letter_pronunciation',
                        'id': str(letter.id),
                    })
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Could not load alphabet: {e}"))

        return items

    def _collect_vocabulary(self, language: str) -> list:
        """Collect vocabulary words."""
        items = []

        try:
            from apps.curriculum.models import VocabularyWord
            # VocabularyWord is linked via theme -> language
            words = VocabularyWord.objects.filter(theme__language=language)

            for word in words:
                items.append({
                    'text': word.word,
                    'type': 'vocabulary',
                    'id': str(word.id),
                })
                if hasattr(word, 'example_sentence') and word.example_sentence:
                    items.append({
                        'text': word.example_sentence,
                        'type': 'example_sentence',
                        'id': str(word.id),
                    })
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Could not load vocabulary: {e}"))

        return items

    def _collect_phrases(self, language: str) -> list:
        """Collect common phrases."""
        items = []

        # Common greetings and phrases (hardcoded for MVP)
        phrases_map = {
            'HINDI': [
                "नमस्ते",
                "धन्यवाद",
                "कृपया",
                "माफ़ कीजिए",
                "आप कैसे हैं?",
                "मैं ठीक हूँ",
                "शुभ प्रभात",
                "शुभ रात्रि",
                "अलविदा",
                "फिर मिलेंगे",
                "हाँ",
                "नहीं",
                "ठीक है",
                "बहुत अच्छा!",
                "शाबाश!",
            ],
            'TAMIL': [
                "வணக்கம்",
                "நன்றி",
                "தயவுசெய்து",
                "மன்னிக்கவும்",
                "நீங்கள் எப்படி இருக்கிறீர்கள்?",
            ],
            'GUJARATI': [
                "નમસ્તે",
                "આભાર",
                "કૃપા કરીને",
                "માફ કરશો",
            ],
            'PUNJABI': [
                "ਸਤ ਸ੍ਰੀ ਅਕਾਲ",
                "ਧੰਨਵਾਦ",
                "ਕਿਰਪਾ ਕਰਕੇ",
            ],
            'TELUGU': [
                "నమస్కారం",
                "ధన్యవాదాలు",
                "దయచేసి",
            ],
            'MALAYALAM': [
                "നമസ്കാരം",
                "നന്ദി",
                "ദയവായി",
            ],
            'BENGALI': [
                "নমস্কার",
                "ধন্যবাদ",
                "দয়া করে",
            ],
        }

        for phrase in phrases_map.get(language, []):
            items.append({
                'text': phrase,
                'type': 'phrase',
                'id': None,
            })

        return items
