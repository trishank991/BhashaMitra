"""
Management command to pre-generate audio for all curriculum content.
Generates TTS for alphabets, vocabulary, stories, and festival content.

Usage:
    python manage.py prewarm_curriculum_audio --language HINDI
    python manage.py prewarm_curriculum_audio --language HINDI --type alphabet
    python manage.py prewarm_curriculum_audio --language HINDI --type stories
    python manage.py prewarm_curriculum_audio --all
"""
import time
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.speech.models import AudioCache
from apps.speech.services.tts_service import TTSService, TTSServiceError


# NCERT-Verified Hindi Alphabet Content
HINDI_ALPHABET = [
    # Vowels (स्वर)
    {'letter': 'अ', 'transliteration': 'a', 'example_word': 'अनार', 'example_meaning': 'pomegranate'},
    {'letter': 'आ', 'transliteration': 'aa', 'example_word': 'आम', 'example_meaning': 'mango'},
    {'letter': 'इ', 'transliteration': 'i', 'example_word': 'इमली', 'example_meaning': 'tamarind'},
    {'letter': 'ई', 'transliteration': 'ee', 'example_word': 'ईख', 'example_meaning': 'sugarcane'},
    {'letter': 'उ', 'transliteration': 'u', 'example_word': 'उल्लू', 'example_meaning': 'owl'},
    {'letter': 'ऊ', 'transliteration': 'oo', 'example_word': 'ऊन', 'example_meaning': 'wool'},
    {'letter': 'ऋ', 'transliteration': 'ri', 'example_word': 'ऋषि', 'example_meaning': 'sage'},
    {'letter': 'ए', 'transliteration': 'e', 'example_word': 'एड़ी', 'example_meaning': 'heel'},
    {'letter': 'ऐ', 'transliteration': 'ai', 'example_word': 'ऐनक', 'example_meaning': 'glasses'},
    {'letter': 'ओ', 'transliteration': 'o', 'example_word': 'ओखली', 'example_meaning': 'mortar'},
    {'letter': 'औ', 'transliteration': 'au', 'example_word': 'औरत', 'example_meaning': 'woman'},
    {'letter': 'अं', 'transliteration': 'am', 'example_word': 'अंगूर', 'example_meaning': 'grapes'},
    {'letter': 'अः', 'transliteration': 'ah', 'example_word': 'दुःख', 'example_meaning': 'sorrow'},

    # Consonants (व्यंजन) - First Row (क वर्ग)
    {'letter': 'क', 'transliteration': 'ka', 'example_word': 'कमल', 'example_meaning': 'lotus'},
    {'letter': 'ख', 'transliteration': 'kha', 'example_word': 'खरगोश', 'example_meaning': 'rabbit'},
    {'letter': 'ग', 'transliteration': 'ga', 'example_word': 'गमला', 'example_meaning': 'pot'},
    {'letter': 'घ', 'transliteration': 'gha', 'example_word': 'घड़ी', 'example_meaning': 'clock'},
    {'letter': 'ङ', 'transliteration': 'nga', 'example_word': 'रंग', 'example_meaning': 'color'},

    # Second Row (च वर्ग)
    {'letter': 'च', 'transliteration': 'cha', 'example_word': 'चम्मच', 'example_meaning': 'spoon'},
    {'letter': 'छ', 'transliteration': 'chha', 'example_word': 'छतरी', 'example_meaning': 'umbrella'},
    {'letter': 'ज', 'transliteration': 'ja', 'example_word': 'जहाज़', 'example_meaning': 'ship'},
    {'letter': 'झ', 'transliteration': 'jha', 'example_word': 'झंडा', 'example_meaning': 'flag'},
    {'letter': 'ञ', 'transliteration': 'nya', 'example_word': 'प्रज्ञा', 'example_meaning': 'wisdom'},

    # Third Row (ट वर्ग)
    {'letter': 'ट', 'transliteration': 'ta', 'example_word': 'टमाटर', 'example_meaning': 'tomato'},
    {'letter': 'ठ', 'transliteration': 'tha', 'example_word': 'ठेला', 'example_meaning': 'cart'},
    {'letter': 'ड', 'transliteration': 'da', 'example_word': 'डमरू', 'example_meaning': 'drum'},
    {'letter': 'ढ', 'transliteration': 'dha', 'example_word': 'ढोल', 'example_meaning': 'drum'},
    {'letter': 'ण', 'transliteration': 'na', 'example_word': 'गणेश', 'example_meaning': 'Ganesh'},

    # Fourth Row (त वर्ग)
    {'letter': 'त', 'transliteration': 'ta', 'example_word': 'तरबूज़', 'example_meaning': 'watermelon'},
    {'letter': 'थ', 'transliteration': 'tha', 'example_word': 'थाली', 'example_meaning': 'plate'},
    {'letter': 'द', 'transliteration': 'da', 'example_word': 'दवात', 'example_meaning': 'inkpot'},
    {'letter': 'ध', 'transliteration': 'dha', 'example_word': 'धनुष', 'example_meaning': 'bow'},
    {'letter': 'न', 'transliteration': 'na', 'example_word': 'नल', 'example_meaning': 'tap'},

    # Fifth Row (प वर्ग)
    {'letter': 'प', 'transliteration': 'pa', 'example_word': 'पतंग', 'example_meaning': 'kite'},
    {'letter': 'फ', 'transliteration': 'pha', 'example_word': 'फल', 'example_meaning': 'fruit'},
    {'letter': 'ब', 'transliteration': 'ba', 'example_word': 'बतख़', 'example_meaning': 'duck'},
    {'letter': 'भ', 'transliteration': 'bha', 'example_word': 'भालू', 'example_meaning': 'bear'},
    {'letter': 'म', 'transliteration': 'ma', 'example_word': 'मछली', 'example_meaning': 'fish'},

    # Antahstha (अंतःस्थ)
    {'letter': 'य', 'transliteration': 'ya', 'example_word': 'यज्ञ', 'example_meaning': 'ritual'},
    {'letter': 'र', 'transliteration': 'ra', 'example_word': 'रथ', 'example_meaning': 'chariot'},
    {'letter': 'ल', 'transliteration': 'la', 'example_word': 'लड्डू', 'example_meaning': 'laddoo'},
    {'letter': 'व', 'transliteration': 'va', 'example_word': 'वन', 'example_meaning': 'forest'},

    # Ushma (ऊष्म)
    {'letter': 'श', 'transliteration': 'sha', 'example_word': 'शहद', 'example_meaning': 'honey'},
    {'letter': 'ष', 'transliteration': 'sha', 'example_word': 'षट्कोण', 'example_meaning': 'hexagon'},
    {'letter': 'स', 'transliteration': 'sa', 'example_word': 'सेब', 'example_meaning': 'apple'},
    {'letter': 'ह', 'transliteration': 'ha', 'example_word': 'हाथी', 'example_meaning': 'elephant'},
]

# Core Vocabulary for Kids (NCERT aligned)
HINDI_VOCABULARY = {
    'family': [
        {'word': 'माँ', 'transliteration': 'maa', 'meaning': 'mother'},
        {'word': 'पापा', 'transliteration': 'papa', 'meaning': 'father'},
        {'word': 'दादी', 'transliteration': 'daadi', 'meaning': 'grandmother (paternal)'},
        {'word': 'दादा', 'transliteration': 'daada', 'meaning': 'grandfather (paternal)'},
        {'word': 'भाई', 'transliteration': 'bhai', 'meaning': 'brother'},
        {'word': 'बहन', 'transliteration': 'behen', 'meaning': 'sister'},
    ],
    'colors': [
        {'word': 'लाल', 'transliteration': 'laal', 'meaning': 'red'},
        {'word': 'नीला', 'transliteration': 'neela', 'meaning': 'blue'},
        {'word': 'हरा', 'transliteration': 'hara', 'meaning': 'green'},
        {'word': 'पीला', 'transliteration': 'peela', 'meaning': 'yellow'},
        {'word': 'सफ़ेद', 'transliteration': 'safed', 'meaning': 'white'},
        {'word': 'काला', 'transliteration': 'kaala', 'meaning': 'black'},
    ],
    'numbers': [
        {'word': 'एक', 'transliteration': 'ek', 'meaning': 'one'},
        {'word': 'दो', 'transliteration': 'do', 'meaning': 'two'},
        {'word': 'तीन', 'transliteration': 'teen', 'meaning': 'three'},
        {'word': 'चार', 'transliteration': 'chaar', 'meaning': 'four'},
        {'word': 'पाँच', 'transliteration': 'paanch', 'meaning': 'five'},
        {'word': 'छह', 'transliteration': 'chhah', 'meaning': 'six'},
        {'word': 'सात', 'transliteration': 'saat', 'meaning': 'seven'},
        {'word': 'आठ', 'transliteration': 'aath', 'meaning': 'eight'},
        {'word': 'नौ', 'transliteration': 'nau', 'meaning': 'nine'},
        {'word': 'दस', 'transliteration': 'das', 'meaning': 'ten'},
    ],
    'animals': [
        {'word': 'बिल्ली', 'transliteration': 'billi', 'meaning': 'cat'},
        {'word': 'कुत्ता', 'transliteration': 'kutta', 'meaning': 'dog'},
        {'word': 'गाय', 'transliteration': 'gaay', 'meaning': 'cow'},
        {'word': 'शेर', 'transliteration': 'sher', 'meaning': 'lion'},
        {'word': 'हाथी', 'transliteration': 'haathi', 'meaning': 'elephant'},
        {'word': 'बंदर', 'transliteration': 'bandar', 'meaning': 'monkey'},
    ],
    'greetings': [
        {'word': 'नमस्ते', 'transliteration': 'namaste', 'meaning': 'hello'},
        {'word': 'धन्यवाद', 'transliteration': 'dhanyavaad', 'meaning': 'thank you'},
        {'word': 'शुभ प्रभात', 'transliteration': 'shubh prabhaat', 'meaning': 'good morning'},
        {'word': 'शुभ रात्रि', 'transliteration': 'shubh raatri', 'meaning': 'good night'},
        {'word': 'कैसे हो', 'transliteration': 'kaise ho', 'meaning': 'how are you'},
    ],
}


class Command(BaseCommand):
    help = 'Pre-generate TTS audio for curriculum content'

    def add_arguments(self, parser):
        parser.add_argument(
            '--language',
            type=str,
            default='HINDI',
            help='Language to generate audio for (default: HINDI)'
        )
        parser.add_argument(
            '--type',
            type=str,
            choices=['alphabet', 'vocabulary', 'stories', 'all'],
            default='all',
            help='Content type to generate (default: all)'
        )
        parser.add_argument(
            '--voice-style',
            type=str,
            default='kid_friendly',
            help='Voice style (default: kid_friendly)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be generated without actually generating'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Regenerate even if already cached'
        )

    def handle(self, *args, **options):
        language = options['language']
        content_type = options['type']
        voice_style = options['voice_style']
        dry_run = options['dry_run']
        force = options['force']

        self.stdout.write(f"Pre-warming audio cache for {language}...")
        self.stdout.write(f"Voice style: {voice_style}")
        self.stdout.write(f"Content type: {content_type}")

        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN - No audio will be generated"))

        stats = {
            'total': 0,
            'cached': 0,
            'generated': 0,
            'failed': 0,
        }

        # Generate alphabet audio
        if content_type in ['alphabet', 'all']:
            self.stdout.write("\n=== Generating Alphabet Audio ===")
            alphabet_stats = self._generate_alphabet_audio(
                language, voice_style, dry_run, force
            )
            for key in stats:
                stats[key] += alphabet_stats[key]

        # Generate vocabulary audio
        if content_type in ['vocabulary', 'all']:
            self.stdout.write("\n=== Generating Vocabulary Audio ===")
            vocab_stats = self._generate_vocabulary_audio(
                language, voice_style, dry_run, force
            )
            for key in stats:
                stats[key] += vocab_stats[key]

        # Generate story audio
        if content_type in ['stories', 'all']:
            self.stdout.write("\n=== Generating Story Audio ===")
            story_stats = self._generate_story_audio(
                language, voice_style, dry_run, force
            )
            for key in stats:
                stats[key] += story_stats[key]

        # Summary
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(self.style.SUCCESS(f"Pre-warming complete!"))
        self.stdout.write(f"Total items: {stats['total']}")
        self.stdout.write(f"Already cached: {stats['cached']}")
        self.stdout.write(f"Newly generated: {stats['generated']}")
        if stats['failed'] > 0:
            self.stdout.write(self.style.ERROR(f"Failed: {stats['failed']}"))

    def _generate_alphabet_audio(self, language, voice_style, dry_run, force):
        """Generate audio for all alphabet letters."""
        stats = {'total': 0, 'cached': 0, 'generated': 0, 'failed': 0}

        for item in HINDI_ALPHABET:
            stats['total'] += 1
            letter = item['letter']
            example_word = item['example_word']

            # Generate audio for the letter itself
            self._generate_single(
                text=letter,
                language=language,
                voice_style=voice_style,
                content_type='alphabet_letter',
                content_id=item['transliteration'],
                dry_run=dry_run,
                force=force,
                stats=stats,
            )

            # Generate audio for the example word
            stats['total'] += 1
            self._generate_single(
                text=example_word,
                language=language,
                voice_style=voice_style,
                content_type='alphabet_example',
                content_id=f"{item['transliteration']}_example",
                dry_run=dry_run,
                force=force,
                stats=stats,
            )

        return stats

    def _generate_vocabulary_audio(self, language, voice_style, dry_run, force):
        """Generate audio for all vocabulary words."""
        stats = {'total': 0, 'cached': 0, 'generated': 0, 'failed': 0}

        for category, words in HINDI_VOCABULARY.items():
            self.stdout.write(f"\nCategory: {category}")

            for item in words:
                stats['total'] += 1
                word = item['word']

                self._generate_single(
                    text=word,
                    language=language,
                    voice_style=voice_style,
                    content_type=f'vocabulary_{category}',
                    content_id=item['transliteration'],
                    dry_run=dry_run,
                    force=force,
                    stats=stats,
                )

        return stats

    def _generate_single(
        self,
        text: str,
        language: str,
        voice_style: str,
        content_type: str,
        content_id: str,
        dry_run: bool,
        force: bool,
        stats: dict,
    ):
        """Generate audio for a single text item."""
        from apps.speech.services.tts_service import TTSService

        cache_key = TTSService._generate_cache_key(text, language, voice_style)

        # Check if already cached
        if not force:
            existing = AudioCache.objects.filter(cache_key=cache_key).first()
            if existing and existing.audio_file:
                self.stdout.write(f"  [CACHED] {text[:20]}...")
                stats['cached'] += 1
                return

        if dry_run:
            self.stdout.write(f"  [DRY-RUN] Would generate: {text[:30]}...")
            return

        try:
            # Generate using the TTS service with a mock premium user
            # This uses Google TTS WaveNet for high-quality cached audio
            # The cached audio is then available for Standard/Free tier users
            from unittest.mock import Mock
            mock_user = Mock()
            mock_user.tts_provider = 'google_wavenet'  # Use Google TTS WaveNet for pre-generation

            audio_bytes, provider, was_cached = TTSService.get_audio(
                text=text,
                language=language,
                voice_profile=voice_style,
                user=mock_user,
                force_regenerate=force,
            )

            # Update the cache entry with content type info
            AudioCache.objects.filter(cache_key=cache_key).update(
                content_type=content_type,
                content_id=content_id,
            )

            self.stdout.write(self.style.SUCCESS(f"  [OK] {text[:20]}... ({provider})"))
            stats['generated'] += 1

            # Small delay to not overwhelm the TTS provider
            time.sleep(0.5)

        except TTSServiceError as e:
            self.stdout.write(self.style.ERROR(f"  [FAIL] {text[:20]}... - {e}"))
            stats['failed'] += 1
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  [ERROR] {text[:20]}... - {e}"))
            stats['failed'] += 1

    def _generate_story_audio(self, language, voice_style, dry_run, force):
        """Generate audio for all story pages and vocabulary."""
        from apps.stories.models import Story, StoryPage, StoryVocabulary

        stats = {'total': 0, 'cached': 0, 'generated': 0, 'failed': 0}

        # Get all stories for this language
        stories = Story.objects.filter(language=language, is_active=True)
        self.stdout.write(f"Found {stories.count()} stories for {language}")

        for story in stories:
            self.stdout.write(f"\nStory: {story.title[:50]}...")

            # Generate audio for each story page
            pages = StoryPage.objects.filter(story=story).order_by('page_number')
            for page in pages:
                if not page.text_content or not page.text_content.strip():
                    continue

                stats['total'] += 1
                self._generate_single(
                    text=page.text_content,
                    language=language,
                    voice_style=voice_style,
                    content_type='story_page',
                    content_id=f"{story.id}_page_{page.page_number}",
                    dry_run=dry_run,
                    force=force,
                    stats=stats,
                )

            # Generate audio for story vocabulary
            vocab_items = StoryVocabulary.objects.filter(story=story)
            for vocab in vocab_items:
                if vocab.word_hindi:
                    stats['total'] += 1
                    self._generate_single(
                        text=vocab.word_hindi,
                        language=language,
                        voice_style=voice_style,
                        content_type='story_vocabulary',
                        content_id=f"{story.id}_vocab_{vocab.id}",
                        dry_run=dry_run,
                        force=force,
                        stats=stats,
                    )

        return stats
