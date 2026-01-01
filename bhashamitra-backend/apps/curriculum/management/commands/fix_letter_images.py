"""
Django management command to fix Letter example images using Twemoji

This command adds Twemoji-based images for letters that don't have example images.

Usage:
    python manage.py fix_letter_images           # Dry run (preview changes)
    python manage.py fix_letter_images --apply   # Apply changes
"""

from django.core.management.base import BaseCommand
from apps.curriculum.models import Letter


# Twemoji CDN base URL
TWEMOJI_BASE = 'https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg'


def emoji_to_twemoji_url(emoji: str) -> str:
    """Convert emoji to Twemoji URL"""
    codepoints = '-'.join(f'{ord(c):x}' for c in emoji)
    return f'{TWEMOJI_BASE}/{codepoints}.svg'


# Example word translation to emoji mapping - COMPREHENSIVE
EXAMPLE_WORD_EMOJI_MAP = {
    # Fruits
    'pomegranate': '\U0001F34E',  # 🍎 (red apple as proxy)
    'mango': '\U0001F96D',  # 🥭
    'banana': '\U0001F34C',  # 🍌
    'apple': '\U0001F34E',  # 🍎
    'grapes': '\U0001F347',  # 🍇
    'orange': '\U0001F34A',  # 🍊
    'watermelon': '\U0001F349',  # 🍉
    'lemon': '\U0001F34B',  # 🍋
    'coconut': '\U0001F965',  # 🥥
    'pineapple': '\U0001F34D',  # 🍍
    'tamarind': '\U0001F33F',  # 🌿 (herb as proxy)
    'sugarcane': '\U0001F33E',  # 🌾 (grain as proxy)
    'tomato': '\U0001F345',  # 🍅
    'fruit': '\U0001F34F',  # 🍏

    # Animals
    'lotus': '\U0001F338',  # 🌸
    'elephant': '\U0001F418',  # 🐘
    'camel': '\U0001F42B',  # 🐫
    'rabbit': '\U0001F430',  # 🐰
    'horse': '\U0001F434',  # 🐴
    'deer': '\U0001F98C',  # 🦌
    'crow': '\U0001F426',  # 🐦
    'parrot': '\U0001F99C',  # 🦜
    'peacock': '\U0001F99A',  # 🦚
    'hen': '\U0001F414',  # 🐔
    'fish': '\U0001F41F',  # 🐟
    'butterfly': '\U0001F98B',  # 🦋
    'monkey': '\U0001F412',  # 🐒
    'lion': '\U0001F981',  # 🦁
    'tiger': '\U0001F405',  # 🐅
    'cow': '\U0001F404',  # 🐄
    'goat': '\U0001F410',  # 🐐
    'dog': '\U0001F415',  # 🐕
    'cat': '\U0001F408',  # 🐈
    'snake': '\U0001F40D',  # 🐍
    'ant': '\U0001F41C',  # 🐜
    'bee': '\U0001F41D',  # 🐝
    'frog': '\U0001F438',  # 🐸
    'duck': '\U0001F986',  # 🦆
    'owl': '\U0001F989',  # 🦉
    'swan': '\U0001F9A2',  # 🦢
    'crab': '\U0001F980',  # 🦀
    'turtle': '\U0001F422',  # 🐢
    'bear': '\U0001F43B',  # 🐻
    'bird': '\U0001F426',  # 🐦
    'pigeon': '\U0001F54A',  # 🕊️
    'sparrow': '\U0001F426',  # 🐦
    'rat': '\U0001F400',  # 🐀
    'fly': '\U0001FAB0',  # 🪰

    # Family
    'mother': '\U0001F469',  # 👩
    'father': '\U0001F468',  # 👨
    'brother': '\U0001F466',  # 👦
    'sister': '\U0001F467',  # 👧
    'grandmother': '\U0001F475',  # 👵
    'grandfather': '\U0001F474',  # 👴
    'woman': '\U0001F469',  # 👩
    'friend': '\U0001F46B',  # 👫

    # Nature
    'sun': '\u2600\uFE0F',  # ☀️
    'moon': '\U0001F319',  # 🌙
    'star': '\u2B50',  # ⭐
    'flower': '\U0001F338',  # 🌸
    'rose': '\U0001F339',  # 🌹
    'tree': '\U0001F333',  # 🌳
    'water': '\U0001F4A7',  # 💧
    'stone': '\U0001FAA8',  # 🪨
    'mountain': '\U000026F0',  # ⛰️
    'rain': '\U0001F327',  # 🌧️
    'cloud': '\u2601\uFE0F',  # ☁️
    'dew': '\U0001F4A7',  # 💧

    # Objects
    'pot': '\U0001FAD9',  # 🫙
    'bell': '\U0001F514',  # 🔔
    'lamp': '\U0001F4A1',  # 💡
    'book': '\U0001F4D6',  # 📖
    'pen': '\U0001F58A',  # 🖊️
    'cup': '\U0001F375',  # 🍵
    'house': '\U0001F3E0',  # 🏠
    'door': '\U0001F6AA',  # 🚪
    'window': '\U0001FA9F',  # 🪟
    'chair': '\U0001FA91',  # 🪑
    'table': '\U0001FA91',  # 🪑
    'umbrella': '\u2614',  # ☔
    'clock': '\U0001F550',  # 🕐
    'arrow': '\U0001F3F9',  # 🏹
    'bow': '\U0001F3F9',  # 🏹
    'box': '\U0001F4E6',  # 📦
    'drum': '\U0001F941',  # 🥁
    'fan': '\U0001FA81',  # 🪭
    'kite': '\U0001FA81',  # 🪁
    'plate': '\U0001F37D',  # 🍽️
    'spoon': '\U0001F944',  # 🥄
    'glasses': '\U0001F453',  # 👓
    'spectacles': '\U0001F453',  # 👓
    'bangle': '\U0001F48D',  # 💍
    'tile': '\U0001F9F1',  # 🧱
    'mortar': '\U0001FAD7',  # 🫗
    'plough': '\U0001F33E',  # 🌾
    'trident': '\U0001F531',  # 🔱
    'violin': '\U0001F3BB',  # 🎻
    'tap': '\U0001F6B0',  # 🚰

    # Food
    'food': '\U0001F37D',  # 🍽️
    'bread': '\U0001F35E',  # 🍞
    'rice': '\U0001F35A',  # 🍚
    'milk': '\U0001F95B',  # 🥛
    'vegetable': '\U0001F96C',  # 🥬
    'sweet': '\U0001F36C',  # 🍬
    'laddu sweet': '\U0001F36C',  # 🍬
    'honey': '\U0001F36F',  # 🍯
    'potato': '\U0001F954',  # 🥔
    'lassi': '\U0001F95B',  # 🥛

    # Body parts
    'hand': '\u270B',  # ✋
    'eye': '\U0001F441',  # 👁️
    'ear': '\U0001F442',  # 👂
    'nose': '\U0001F443',  # 👃
    'mouth': '\U0001F444',  # 👄
    'head': '\U0001F5E3',  # 🗣️
    'foot': '\U0001F9B6',  # 🦶
    'body': '\U0001F9CD',  # 🧍
    'limb': '\U0001F4AA',  # 💪
    'tooth': '\U0001F9B7',  # 🦷
    'hair': '\U0001F487',  # 💇

    # Abstract/Other
    'that': '\U0001F449',  # 👉
    'one': '1\uFE0F\u20E3',  # 1️⃣
    'particle': '\u2728',  # ✨
    'letter': '\U0001F4DD',  # 📝
    'knowledge': '\U0001F4DA',  # 📚
    'wisdom': '\U0001F9E0',  # 🧠
    'memory': '\U0001F9E0',  # 🧠
    'journey': '\U0001F6EB',  # 🛫
    'village': '\U0001F3D8',  # 🏘️
    'tune': '\U0001F3B5',  # 🎵
    'sorrow': '\U0001F622',  # 😢
    'cold': '\U0001F976',  # 🥶
    'color': '\U0001F3A8',  # 🎨
    'rare usage': '\U0001F4D6',  # 📖
    'palatal nasal': '\U0001F4AC',  # 💬
    'tamil': '\U0001F4D6',  # 📖
    'hexagon': '\U0001F533',  # 🔳

    # Colors
    'red': '\U0001F534',  # 🔴
    'blue': '\U0001F535',  # 🔵
    'yellow': '\U0001F49B',  # 💛
    'green': '\U0001F49A',  # 💚

    # Religious/Cultural (use appropriate symbols)
    'saraswati': '\U0001F4DA',  # 📚 (books for goddess of knowledge)
    'hari': '\U0001F64F',  # 🙏 (prayer hands)
    'poison': '\u2620\uFE0F',  # ☠️
    'god': '\U0001F64F',  # 🙏
    'goddess': '\U0001F64F',  # 🙏
    'prayer': '\U0001F64F',  # 🙏
    'temple': '\U0001F6D5',  # 🛕
    'shri ram': '\U0001F64F',  # 🙏
    'yoga': '\U0001F9D8',  # 🧘

    # People/Professions
    'king': '\U0001F451',  # 👑
    'warrior': '\U0001F93A',  # 🤺
    'poet': '\U0001F4DD',  # 📝
    'sage': '\U0001F9D4',  # 🧔
    'medicine': '\U0001F48A',  # 💊

    # Actions/Verbs
    'walk': '\U0001F6B6',  # 🚶
    'run': '\U0001F3C3',  # 🏃
    'eat': '\U0001F37D',  # 🍽️
    'drink': '\U0001F964',  # 🥤
    'sleep': '\U0001F634',  # 😴
    'read': '\U0001F4D6',  # 📖
    'to read': '\U0001F4D6',  # 📖
    'write': '\u270D',  # ✍️
    'play': '\U0001F3AE',  # 🎮
    'sing': '\U0001F3A4',  # 🎤
    'dance': '\U0001F483',  # 💃

    # More objects
    'sword': '\U0001F5E1',  # 🗡️
    'shield': '\U0001F6E1',  # 🛡️
    'flag': '\U0001F3F3',  # 🏳️
    'wheel': '\u2699',  # ⚙️
    'key': '\U0001F511',  # 🔑
    'bag': '\U0001F45C',  # 👜
    'rope': '\U0001FAA2',  # 🪢
    'thread': '\U0001F9F5',  # 🧵
    'needle': '\U0001FAA1',  # 🪡
    'scissors': '\u2702\uFE0F',  # ✂️
    'knife': '\U0001F52A',  # 🔪
    'axe': '\U0001FA93',  # 🪓
    'hammer': '\U0001F528',  # 🔨
    'nail': '\U0001F528',  # 🔨 (hammer as proxy)
    'boat': '\u26F5',  # ⛵
    'ship': '\U0001F6A2',  # 🚢
    'cart': '\U0001F6D2',  # 🛒
    'car': '\U0001F697',  # 🚗
    'bus': '\U0001F68C',  # 🚌
    'train': '\U0001F682',  # 🚂
    'airplane': '\u2708\uFE0F',  # ✈️

    # More nature
    'river': '\U0001F30A',  # 🌊
    'sea': '\U0001F30A',  # 🌊
    'ocean': '\U0001F30A',  # 🌊
    'sky': '\u2601\uFE0F',  # ☁️
    'earth': '\U0001F30D',  # 🌍
    'fire': '\U0001F525',  # 🔥
    'air': '\U0001F4A8',  # 💨
    'wind': '\U0001F4A8',  # 💨
    'lightning': '\u26A1',  # ⚡
    'thunder': '\u26A1',  # ⚡
    'snow': '\u2744\uFE0F',  # ❄️
    'ice': '\U0001F9CA',  # 🧊
    'leaf': '\U0001F343',  # 🍃
    'grass': '\U0001F33F',  # 🌿
    'forest': '\U0001F332',  # 🌲

    # More food
    'egg': '\U0001F95A',  # 🥚
    'meat': '\U0001F356',  # 🍖
    'cheese': '\U0001F9C0',  # 🧀
    'salt': '\U0001F9C2',  # 🧂
    'butter': '\U0001F9C8',  # 🧈
    'oil': '\U0001FAD3',  # 🫓 (flatbread proxy)
    'tea': '\U0001F375',  # 🍵
    'coffee': '\u2615',  # ☕
    'cake': '\U0001F370',  # 🍰
    'candy': '\U0001F36C',  # 🍬

    # Body (extended)
    'heart': '\u2764\uFE0F',  # ❤️
    'teeth': '\U0001F9B7',  # 🦷
    'finger': '\U0001F446',  # 👆
    'arm': '\U0001F4AA',  # 💪
    'leg': '\U0001F9B5',  # 🦵

    # Emotions
    'happy': '\U0001F60A',  # 😊
    'sad': '\U0001F622',  # 😢
    'angry': '\U0001F620',  # 😠
    'love': '\u2764\uFE0F',  # ❤️

    # Time
    'day': '\u2600\uFE0F',  # ☀️
    'night': '\U0001F319',  # 🌙
    'morning': '\U0001F305',  # 🌅
    'evening': '\U0001F306',  # 🌆

    # Numbers
    'two': '2\uFE0F\u20E3',  # 2️⃣
    'three': '3\uFE0F\u20E3',  # 3️⃣
    'four': '4\uFE0F\u20E3',  # 4️⃣
    'five': '5\uFE0F\u20E3',  # 5️⃣
    'six': '6\uFE0F\u20E3',  # 6️⃣
    'seven': '7\uFE0F\u20E3',  # 7️⃣
    'eight': '8\uFE0F\u20E3',  # 8️⃣
    'nine': '9\uFE0F\u20E3',  # 9️⃣
    'ten': '\U0001F51F',  # 🔟

    # Materials
    'wool': '\U0001F9F6',  # 🧶
}


def get_emoji_for_example_word(translation: str) -> str | None:
    """Get emoji for an example word translation"""
    if not translation:
        return None

    normalized = translation.lower().strip()

    # Direct match
    if normalized in EXAMPLE_WORD_EMOJI_MAP:
        return EXAMPLE_WORD_EMOJI_MAP[normalized]

    # Partial match
    for key, emoji in EXAMPLE_WORD_EMOJI_MAP.items():
        if key in normalized or normalized in key:
            return emoji

    return None


class Command(BaseCommand):
    help = 'Fix Letter example images using Twemoji'

    def add_arguments(self, parser):
        parser.add_argument(
            '--apply',
            action='store_true',
            help='Actually apply changes (default is dry run)',
        )
        parser.add_argument(
            '--overwrite',
            action='store_true',
            help='Overwrite existing images (default only fills empty)',
        )

    def handle(self, *args, **options):
        apply_changes = options['apply']
        overwrite = options['overwrite']

        self.stdout.write(self.style.NOTICE('\n' + '=' * 60))
        self.stdout.write(self.style.NOTICE('  Letter Example Image Fix - Twemoji'))
        self.stdout.write(self.style.NOTICE('=' * 60 + '\n'))

        letters = Letter.objects.all()
        self.stdout.write(f'Total letters: {letters.count()}\n')

        needs_fix = []
        already_good = []
        no_mapping = []

        for letter in letters:
            has_image = bool(letter.example_image)

            if has_image and not overwrite:
                already_good.append({
                    'character': letter.character,
                    'example_word': letter.example_word_translation,
                    'image': letter.example_image,
                })
                continue

            emoji = get_emoji_for_example_word(letter.example_word_translation)

            if emoji:
                new_url = emoji_to_twemoji_url(emoji)
                needs_fix.append({
                    'id': letter.id,
                    'character': letter.character,
                    'example_word': letter.example_word,
                    'translation': letter.example_word_translation,
                    'old_url': letter.example_image,
                    'new_url': new_url,
                    'emoji': emoji,
                })
            else:
                no_mapping.append({
                    'character': letter.character,
                    'example_word': letter.example_word,
                    'translation': letter.example_word_translation,
                })

        # Report
        self.stdout.write('\n' + '-' * 40)
        self.stdout.write(self.style.SUCCESS(f'Letters with proper images: {len(already_good)}'))
        self.stdout.write(self.style.WARNING(f'Letters needing fix (have mapping): {len(needs_fix)}'))
        self.stdout.write(self.style.ERROR(f'Letters without emoji mapping: {len(no_mapping)}'))
        self.stdout.write('-' * 40 + '\n')

        if needs_fix:
            self.stdout.write(self.style.NOTICE('\nLetters to be updated:'))
            for item in needs_fix[:20]:
                self.stdout.write(
                    f"  {item['character']} ({item['translation']}) -> {item['emoji']}"
                )
            if len(needs_fix) > 20:
                self.stdout.write(f'  ... and {len(needs_fix) - 20} more\n')

        if no_mapping:
            self.stdout.write(self.style.WARNING('\nLetters without emoji mapping:'))
            for item in no_mapping[:10]:
                self.stdout.write(
                    f"  {item['character']} - {item['example_word']} ({item['translation']})"
                )
            if len(no_mapping) > 10:
                self.stdout.write(f'  ... and {len(no_mapping) - 10} more\n')

        if not apply_changes:
            self.stdout.write(self.style.NOTICE(
                '\n*** DRY RUN - No changes made ***\n'
                'Run with --apply to actually update the database.\n'
            ))
            return

        # Apply changes
        updated_count = 0
        for item in needs_fix:
            Letter.objects.filter(id=item['id']).update(example_image=item['new_url'])
            updated_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'\n Updated {updated_count} letter example images!\n'
        ))
