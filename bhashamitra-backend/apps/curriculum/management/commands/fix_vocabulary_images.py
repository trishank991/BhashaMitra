"""
Django management command to fix vocabulary images using Twemoji

This command updates vocabulary words to use consistent, high-quality Twemoji images
instead of random picsum.photos placeholders.

Usage:
    python manage.py fix_vocabulary_images           # Dry run (preview changes)
    python manage.py fix_vocabulary_images --apply   # Apply changes
    python manage.py fix_vocabulary_images --backup  # Create backup before applying
"""

from django.core.management.base import BaseCommand
from apps.curriculum.models import VocabularyWord
import json
from datetime import datetime


# Twemoji CDN base URL
TWEMOJI_BASE = 'https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg'


def emoji_to_twemoji_url(emoji: str) -> str:
    """Convert emoji to Twemoji URL"""
    codepoints = '-'.join(f'{ord(c):x}' for c in emoji)
    return f'{TWEMOJI_BASE}/{codepoints}.svg'


# Translation to emoji mapping (matches frontend vocabularyImages.ts)
VOCABULARY_EMOJI_MAP = {
    # ========== FAMILY ==========
    'mother': '\U0001F469',  # 👩
    'mom': '\U0001F469',
    'father': '\U0001F468',  # 👨
    'papa': '\U0001F468',
    'dad': '\U0001F468',
    'brother': '\U0001F466',  # 👦
    'sister': '\U0001F467',  # 👧
    'grandfather': '\U0001F474',  # 👴
    'grandfather (maternal)': '\U0001F474',
    'grandfather (paternal)': '\U0001F474',
    'grandmother': '\U0001F475',  # 👵
    'grandmother (maternal)': '\U0001F475',
    'grandmother (paternal)': '\U0001F475',
    'uncle': '\U0001F468',
    'uncle (paternal)': '\U0001F468',
    'uncle (maternal)': '\U0001F468',
    "uncle (father's elder brother)": '\U0001F468',
    "uncle (father's younger brother)": '\U0001F468',
    'aunt': '\U0001F469',
    'aunt (paternal)': '\U0001F469',
    'aunt (maternal)': '\U0001F469',
    'aunt (paternal uncle wife)': '\U0001F469',
    "aunt (mother's elder sister)": '\U0001F469',
    "aunt (mother's younger sister)": '\U0001F469',
    'son': '\U0001F466',
    'daughter': '\U0001F467',
    'elder brother': '\U0001F466',
    'elder sister': '\U0001F467',
    'maternal uncle': '\U0001F468',
    'maternal aunt': '\U0001F469',
    'maternal grandfather': '\U0001F474',
    'maternal grandmother': '\U0001F475',
    'paternal uncle': '\U0001F468',
    'paternal aunt': '\U0001F469',

    # ========== COLORS ==========
    'red': '\U0001F534',  # 🔴
    'blue': '\U0001F535',  # 🔵
    'yellow': '\U0001F49B',  # 💛
    'green': '\U0001F49A',  # 💚
    'black': '\U000026AB',  # ⚫
    'white': '\U000026AA',  # ⚪
    'orange': '\U0001F7E0',  # 🟠
    'pink': '\U0001F497',  # 💗
    'purple': '\U0001F7E3',  # 🟣
    'brown': '\U0001F7E4',  # 🟤

    # ========== NUMBERS ==========
    'one': '1\uFE0F\u20E3',  # 1️⃣
    'two': '2\uFE0F\u20E3',  # 2️⃣
    'three': '3\uFE0F\u20E3',  # 3️⃣
    'four': '4\uFE0F\u20E3',  # 4️⃣
    'five': '5\uFE0F\u20E3',  # 5️⃣
    'six': '6\uFE0F\u20E3',  # 6️⃣
    'seven': '7\uFE0F\u20E3',  # 7️⃣
    'eight': '8\uFE0F\u20E3',  # 8️⃣
    'nine': '9\uFE0F\u20E3',  # 9️⃣
    'ten': '\U0001F51F',  # 🔟
    'twenty': '\U0001F522',  # 🔢
    'twenty-one': '\U0001F522',
    'hundred': '\U0001F4AF',  # 💯

    # ========== ANIMALS ==========
    'dog': '\U0001F415',  # 🐕
    'cat': '\U0001F408',  # 🐈
    'cow': '\U0001F404',  # 🐄
    'horse': '\U0001F434',  # 🐴
    'elephant': '\U0001F418',  # 🐘
    'lion': '\U0001F981',  # 🦁
    'tiger': '\U0001F405',  # 🐅
    'monkey': '\U0001F412',  # 🐒
    'bird': '\U0001F426',  # 🐦
    'fish': '\U0001F41F',  # 🐟
    'rabbit': '\U0001F430',  # 🐰
    'crow': '\U0001F426\u200D\U00002B1B',  # 🐦‍⬛
    'butterfly': '\U0001F98B',  # 🦋
    'sparrow': '\U0001F426',
    'parrot': '\U0001F99C',  # 🦜
    'chicken': '\U0001F414',  # 🐔

    # ========== BODY PARTS ==========
    'head': '\U0001F5E3',  # 🗣️
    'eye': '\U0001F441',  # 👁️
    'ear': '\U0001F442',  # 👂
    'nose': '\U0001F443',  # 👃
    'mouth': '\U0001F444',  # 👄
    'hand': '\u270B',  # ✋
    'foot': '\U0001F9B6',  # 🦶
    'leg': '\U0001F9B5',  # 🦵
    'foot/leg': '\U0001F9B6',
    'leg/foot': '\U0001F9B6',
    'stomach': '\U0001FAC3',  # 🫃
    'teeth': '\U0001F9B7',  # 🦷
    'hair': '\U0001F487',  # 💇
    'finger': '\U0001F446',  # 👆

    # ========== FOOD & DRINKS ==========
    'water': '\U0001F4A7',  # 💧
    'milk': '\U0001F95B',  # 🥛
    'bread': '\U0001F35E',  # 🍞
    'bread/roti': '\U0001FAD3',  # 🫓
    'rice': '\U0001F35A',  # 🍚
    'lentils': '\U0001F372',  # 🍲
    'vegetable': '\U0001F96C',  # 🥬
    'fruit': '\U0001F34E',  # 🍎
    'apple': '\U0001F34E',  # 🍎
    'mango': '\U0001F96D',  # 🥭
    'banana': '\U0001F34C',  # 🍌
    'grapes': '\U0001F347',  # 🍇
    'orange fruit': '\U0001F34A',  # 🍊
    'food': '\U0001F37D',  # 🍽️
    'sweets': '\U0001F36C',  # 🍬
    'curry': '\U0001F35B',  # 🍛
    'chutney': '\U0001FAD9',  # 🫙
    'taro': '\U0001F954',  # 🥔
    'fried bread': '\U0001FAD3',  # 🫓
    'puri (fried bread)': '\U0001FAD3',
    'lassi': '\U0001F95B',  # 🥛
    'idli': '\U0001FAD3',  # 🫓
    'cassava': '\U0001F954',  # 🥔
    'kava drink': '\U0001F375',  # 🍵

    # ========== ACTIONS/VERBS ==========
    'to eat': '\U0001F37D',  # 🍽️
    'to drink': '\U0001F964',  # 🥤
    'to sleep': '\U0001F634',  # 😴
    'to read': '\U0001F4D6',  # 📖
    'to read/study': '\U0001F4D6',
    'to write': '\u270D',  # ✍️
    'to play': '\U0001F3AE',  # 🎮
    'to see': '\U0001F440',  # 👀
    'to listen': '\U0001F442',  # 👂
    'to speak': '\U0001F5E3',  # 🗣️
    'to walk': '\U0001F6B6',  # 🚶
    'to run': '\U0001F3C3',  # 🏃
    'to go': '\U0001F6B6',
    'to come': '\U0001F6B6',
    'to wake up': '\u23F0',  # ⏰
    'to do': '\u2705',  # ✅

    # ========== GREETINGS & BASIC ==========
    'hello': '\U0001F44B',  # 👋
    'hello (formal)': '\U0001F64F',  # 🙏
    'hello (fijian)': '\U0001F44B',
    'hello/greetings': '\U0001F64F',
    'thank you': '\U0001F64F',  # 🙏
    'thank you (fijian)': '\U0001F64F',
    'yes': '\u2705',  # ✅
    'no': '\u274C',  # ❌
    'good': '\U0001F44D',  # 👍
    'bad': '\U0001F44E',  # 👎
    'please': '\U0001F64F',  # 🙏
    'sorry/excuse me': '\U0001F647',  # 🙇
    'goodbye': '\U0001F44B',  # 👋
    'welcome': '\U0001F917',  # 🤗
    'how are you': '\u2753',  # ❓
    'fine/ok': '\U0001F44C',  # 👌
    'see you later': '\U0001F44B',
    'good morning': '\U0001F305',  # 🌅
    'good night': '\U0001F319',  # 🌙
    'hey!': '\U0001F44B',

    # ========== TIME ==========
    'today': '\U0001F4C5',  # 📅
    'yesterday/tomorrow': '\U0001F4C6',  # 📆
    'morning': '\U0001F305',  # 🌅
    'evening': '\U0001F306',  # 🌆
    'night': '\U0001F319',  # 🌙
    'week': '\U0001F4C5',
    'month': '\U0001F4C6',
    'year': '\U0001F4C6',

    # ========== PLACES ==========
    'home': '\U0001F3E0',  # 🏠
    'school': '\U0001F3EB',  # 🏫
    'temple': '\U0001F6D5',  # 🛕
    'shop': '\U0001F3EA',  # 🏪
    'market': '\U0001F6D2',  # 🛒
    'village': '\U0001F3D8',  # 🏘️
    'room': '\U0001F6AA',  # 🚪
    'door': '\U0001F6AA',  # 🚪
    'window': '\U0001FA9F',  # 🪟
    'table': '\U0001FA91',  # 🪑
    'chair': '\U0001FA91',  # 🪑

    # ========== NATURE ==========
    'sun': '\u2600\uFE0F',  # ☀️
    'sunshine': '\u2600\uFE0F',
    'moon': '\U0001F319',  # 🌙
    'star': '\u2B50',  # ⭐
    'cloud': '\u2601\uFE0F',  # ☁️
    'rain': '\U0001F327',  # 🌧️
    'wind': '\U0001F4A8',  # 💨
    'cold': '\U0001F976',  # 🥶
    'flower': '\U0001F338',  # 🌸
    'tree': '\U0001F333',  # 🌳

    # ========== EMOTIONS ==========
    'happy': '\U0001F60A',  # 😊
    'sad': '\U0001F622',  # 😢
    'angry': '\U0001F620',  # 😠
    'fear': '\U0001F628',  # 😨
    'love': '\u2764\uFE0F',  # ❤️

    # ========== SIZE/DESCRIPTION ==========
    'big': '\U0001F4CF',  # 📏
    'small': '\U0001F90F',  # 🤏

    # ========== CLOTHING ==========
    'sarong/wrap': '\U0001F454',  # 👔
}


def get_emoji_for_translation(translation: str) -> str | None:
    """Get emoji for a translation, with fallback partial matching"""
    normalized = translation.lower().strip()

    # Direct match
    if normalized in VOCABULARY_EMOJI_MAP:
        return VOCABULARY_EMOJI_MAP[normalized]

    # Partial match
    for key, emoji in VOCABULARY_EMOJI_MAP.items():
        if normalized in key or key in normalized:
            return emoji

    return None


class Command(BaseCommand):
    help = 'Fix vocabulary images using Twemoji instead of random placeholders'

    def add_arguments(self, parser):
        parser.add_argument(
            '--apply',
            action='store_true',
            help='Actually apply changes (default is dry run)',
        )
        parser.add_argument(
            '--backup',
            action='store_true',
            help='Create backup JSON before applying changes',
        )
        parser.add_argument(
            '--language',
            type=str,
            help='Only fix words for a specific language (e.g., HINDI, TAMIL)',
        )

    def handle(self, *args, **options):
        apply_changes = options['apply']
        create_backup = options['backup']
        language_filter = options.get('language')

        self.stdout.write(self.style.NOTICE('\n' + '=' * 60))
        self.stdout.write(self.style.NOTICE('  Vocabulary Image Fix - Twemoji Migration'))
        self.stdout.write(self.style.NOTICE('=' * 60 + '\n'))

        # Get all vocabulary words
        queryset = VocabularyWord.objects.select_related('theme').all()

        if language_filter:
            queryset = queryset.filter(theme__language=language_filter.upper())
            self.stdout.write(f'Filtering by language: {language_filter.upper()}\n')

        words = list(queryset)
        self.stdout.write(f'Total vocabulary words: {len(words)}\n')

        # Categorize words
        needs_fix = []
        already_good = []
        no_mapping = []

        for word in words:
            translation = word.translation
            current_url = word.image_url

            is_random = current_url and 'picsum.photos/seed/' in current_url
            is_empty = not current_url

            if is_random or is_empty:
                emoji = get_emoji_for_translation(translation)
                if emoji:
                    new_url = emoji_to_twemoji_url(emoji)
                    needs_fix.append({
                        'id': word.id,
                        'word': word.word,
                        'translation': translation,
                        'language': word.theme.language if word.theme else 'unknown',
                        'old_url': current_url,
                        'new_url': new_url,
                        'emoji': emoji,
                    })
                else:
                    no_mapping.append({
                        'id': word.id,
                        'word': word.word,
                        'translation': translation,
                        'language': word.theme.language if word.theme else 'unknown',
                    })
            else:
                already_good.append({
                    'id': word.id,
                    'word': word.word,
                    'translation': translation,
                    'url': current_url,
                })

        # Report
        self.stdout.write('\n' + '-' * 40)
        self.stdout.write(self.style.SUCCESS(f'Words with proper images: {len(already_good)}'))
        self.stdout.write(self.style.WARNING(f'Words needing fix (have mapping): {len(needs_fix)}'))
        self.stdout.write(self.style.ERROR(f'Words without emoji mapping: {len(no_mapping)}'))
        self.stdout.write('-' * 40 + '\n')

        # Show words needing fix
        if needs_fix:
            self.stdout.write(self.style.NOTICE('\nWords to be updated:'))
            for item in needs_fix[:20]:  # Show first 20
                self.stdout.write(
                    f"  [{item['language']}] {item['word']} ({item['translation']}) "
                    f"-> {item['emoji']}"
                )
            if len(needs_fix) > 20:
                self.stdout.write(f'  ... and {len(needs_fix) - 20} more\n')

        # Show words without mapping
        if no_mapping:
            self.stdout.write(self.style.WARNING('\nWords without emoji mapping:'))
            for item in no_mapping:
                self.stdout.write(
                    f"  [{item['language']}] {item['word']} -> {item['translation']}"
                )
            self.stdout.write('')

        if not apply_changes:
            self.stdout.write(self.style.NOTICE(
                '\n*** DRY RUN - No changes made ***\n'
                'Run with --apply to actually update the database.\n'
            ))
            return

        # Create backup if requested
        if create_backup:
            backup_data = {
                'timestamp': datetime.now().isoformat(),
                'words': [
                    {
                        'id': str(w.id),  # Convert UUID to string
                        'word': w.word,
                        'translation': w.translation,
                        'image_url': w.image_url,
                    }
                    for w in words
                ]
            }
            backup_file = f'vocabulary_images_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            with open(backup_file, 'w') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
            self.stdout.write(self.style.SUCCESS(f'Backup created: {backup_file}\n'))

        # Apply changes
        updated_count = 0
        for item in needs_fix:
            VocabularyWord.objects.filter(id=item['id']).update(image_url=item['new_url'])
            updated_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Successfully updated {updated_count} vocabulary word images!\n'
        ))
