"""Seed Peppi Mimic pronunciation challenges."""
from django.core.management.base import BaseCommand
from apps.speech.models import PeppiMimicChallenge


# Hindi Mimic Challenges organized by category
HINDI_CHALLENGES = [
    # ========== GREETINGS (5 challenges) ==========
    {
        "word": "नमस्ते",
        "romanization": "Namaste",
        "meaning": "Hello / Greetings",
        "category": "GREETING",
        "difficulty": 1,
        "display_order": 1,
        "points_reward": 20,
        "peppi_intro": "Meow! Let's say hello in Hindi! Listen carefully...",
        "peppi_perfect": "MEOW! 🌟 That was PURRRFECT namaste! You sound like a native speaker! 🙏",
        "peppi_good": "Meow meow! 👏 Almost purrrfect! Your namaste is getting better!",
        "peppi_try_again": "Meow! Good try little cub! Let's practice namaste again - na-mas-te!",
    },
    {
        "word": "धन्यवाद",
        "romanization": "Dhanyavaad",
        "meaning": "Thank you",
        "category": "GREETING",
        "difficulty": 2,
        "display_order": 2,
        "points_reward": 25,
        "peppi_intro": "Time to say thank you! Listen...",
        "peppi_perfect": "AMAZING! Perfect dhanyavaad! So polite! 🌟",
        "peppi_good": "Nice work! Your thank you sounds great!",
        "peppi_try_again": "Good effort! Try again - dhan-ya-vaad!",
    },
    {
        "word": "शुभ प्रभात",
        "romanization": "Shubh Prabhaat",
        "meaning": "Good morning",
        "category": "GREETING",
        "difficulty": 2,
        "display_order": 3,
        "points_reward": 25,
        "peppi_intro": "Let's wish good morning! Listen...",
        "peppi_perfect": "WONDERFUL! Perfect good morning! Start every day like this! ☀️",
        "peppi_good": "Great job! Your morning greeting is lovely!",
        "peppi_try_again": "Nice try! Say it slowly - shubh pra-bhaat!",
    },
    {
        "word": "अलविदा",
        "romanization": "Alvida",
        "meaning": "Goodbye",
        "category": "GREETING",
        "difficulty": 1,
        "display_order": 4,
        "points_reward": 20,
        "peppi_intro": "Let's say goodbye! Listen carefully...",
        "peppi_perfect": "PERFECT! Beautiful goodbye! See you soon! 👋",
        "peppi_good": "Very nice! Your goodbye sounds sweet!",
        "peppi_try_again": "Good try! Practice again - al-vi-da!",
    },
    {
        "word": "कैसे हो",
        "romanization": "Kaise ho",
        "meaning": "How are you",
        "category": "GREETING",
        "difficulty": 1,
        "display_order": 5,
        "points_reward": 20,
        "peppi_intro": "Ask how someone is doing! Listen...",
        "peppi_perfect": "EXCELLENT! Perfect question! Now you can make friends! 💫",
        "peppi_good": "Nice! Your pronunciation is improving!",
        "peppi_try_again": "Good effort! Try again - kai-se ho!",
    },

    # ========== FAMILY (5 challenges) ==========
    {
        "word": "माँ",
        "romanization": "Maa",
        "meaning": "Mother",
        "category": "FAMILY",
        "difficulty": 1,
        "display_order": 1,
        "points_reward": 20,
        "peppi_intro": "Let's say mother in Hindi! Listen...",
        "peppi_perfect": "BEAUTIFUL! Perfect! Your maa will be so happy! ❤️",
        "peppi_good": "Lovely! Keep practicing this sweet word!",
        "peppi_try_again": "Nice try! Say it with love - maa!",
    },
    {
        "word": "पापा",
        "romanization": "Papa",
        "meaning": "Father",
        "category": "FAMILY",
        "difficulty": 1,
        "display_order": 2,
        "points_reward": 20,
        "peppi_intro": "Now let's say father! Listen carefully...",
        "peppi_perfect": "WONDERFUL! Perfect papa! He'll be so proud! 💪",
        "peppi_good": "Great! Your papa sounds perfect!",
        "peppi_try_again": "Good try! Say it again - pa-pa!",
    },
    {
        "word": "दादी",
        "romanization": "Daadi",
        "meaning": "Grandmother (paternal)",
        "category": "FAMILY",
        "difficulty": 1,
        "display_order": 3,
        "points_reward": 20,
        "peppi_intro": "Let's say grandmother! Listen...",
        "peppi_perfect": "AMAZING! Perfect daadi! She'll give you extra sweets! 🍬",
        "peppi_good": "Very good! Grandma would be happy!",
        "peppi_try_again": "Nice effort! Try again - daa-di!",
    },
    {
        "word": "दादा",
        "romanization": "Daada",
        "meaning": "Grandfather (paternal)",
        "category": "FAMILY",
        "difficulty": 1,
        "display_order": 4,
        "points_reward": 20,
        "peppi_intro": "Now grandfather! Listen carefully...",
        "peppi_perfect": "PERFECT! Your daada will tell you extra stories! 📖",
        "peppi_good": "Great job! Grandfather sounds proud!",
        "peppi_try_again": "Good try! Say it slowly - daa-da!",
    },
    {
        "word": "भाई",
        "romanization": "Bhai",
        "meaning": "Brother",
        "category": "FAMILY",
        "difficulty": 1,
        "display_order": 5,
        "points_reward": 20,
        "peppi_intro": "Let's say brother! Listen...",
        "peppi_perfect": "EXCELLENT! Perfect bhai! Great sibling word! 👦",
        "peppi_good": "Nice! Your brother word sounds great!",
        "peppi_try_again": "Good effort! Try again - bh-ai!",
    },

    # ========== NUMBERS (5 challenges) ==========
    {
        "word": "एक",
        "romanization": "Ek",
        "meaning": "One",
        "category": "NUMBERS",
        "difficulty": 1,
        "display_order": 1,
        "points_reward": 15,
        "peppi_intro": "Let's count! Start with one...",
        "peppi_perfect": "PERFECT! Ek is easy for you! 1️⃣",
        "peppi_good": "Great! One down, more to learn!",
        "peppi_try_again": "Good try! Just say - ek!",
    },
    {
        "word": "दो",
        "romanization": "Do",
        "meaning": "Two",
        "category": "NUMBERS",
        "difficulty": 1,
        "display_order": 2,
        "points_reward": 15,
        "peppi_intro": "Now number two! Listen...",
        "peppi_perfect": "WONDERFUL! Perfect do! 2️⃣",
        "peppi_good": "Nice! Two is easy for you!",
        "peppi_try_again": "Good effort! Say - do!",
    },
    {
        "word": "तीन",
        "romanization": "Teen",
        "meaning": "Three",
        "category": "NUMBERS",
        "difficulty": 1,
        "display_order": 3,
        "points_reward": 15,
        "peppi_intro": "Number three now! Listen carefully...",
        "peppi_perfect": "AMAZING! Perfect teen! 3️⃣",
        "peppi_good": "Great! Three sounds good!",
        "peppi_try_again": "Nice try! Say - teen!",
    },
    {
        "word": "चार",
        "romanization": "Chaar",
        "meaning": "Four",
        "category": "NUMBERS",
        "difficulty": 1,
        "display_order": 4,
        "points_reward": 15,
        "peppi_intro": "Now four! Listen...",
        "peppi_perfect": "PERFECT! Chaar is done! 4️⃣",
        "peppi_good": "Very good! Four more!",
        "peppi_try_again": "Good try! Say - chaar!",
    },
    {
        "word": "पाँच",
        "romanization": "Paanch",
        "meaning": "Five",
        "category": "NUMBERS",
        "difficulty": 1,
        "display_order": 5,
        "points_reward": 15,
        "peppi_intro": "Number five! Listen...",
        "peppi_perfect": "EXCELLENT! High five! Perfect paanch! 5️⃣",
        "peppi_good": "Great! You can count to five now!",
        "peppi_try_again": "Good effort! Say - paanch!",
    },

    # ========== COLORS (5 challenges) ==========
    {
        "word": "लाल",
        "romanization": "Laal",
        "meaning": "Red",
        "category": "COLORS",
        "difficulty": 1,
        "display_order": 1,
        "points_reward": 20,
        "peppi_intro": "Let's learn red in Hindi! Listen...",
        "peppi_perfect": "BEAUTIFUL! Perfect laal! Like an apple! 🍎",
        "peppi_good": "Great! Red sounds lovely!",
        "peppi_try_again": "Nice try! Say - laal!",
    },
    {
        "word": "नीला",
        "romanization": "Neela",
        "meaning": "Blue",
        "category": "COLORS",
        "difficulty": 1,
        "display_order": 2,
        "points_reward": 20,
        "peppi_intro": "Now blue! Listen carefully...",
        "peppi_perfect": "WONDERFUL! Perfect neela! Like the sky! 💙",
        "peppi_good": "Nice! Blue is beautiful!",
        "peppi_try_again": "Good try! Say - nee-la!",
    },
    {
        "word": "पीला",
        "romanization": "Peela",
        "meaning": "Yellow",
        "category": "COLORS",
        "difficulty": 1,
        "display_order": 3,
        "points_reward": 20,
        "peppi_intro": "Yellow time! Listen...",
        "peppi_perfect": "SUNNY! Perfect peela! Like sunshine! 🌻",
        "peppi_good": "Great! Yellow sounds bright!",
        "peppi_try_again": "Good effort! Say - pee-la!",
    },
    {
        "word": "हरा",
        "romanization": "Hara",
        "meaning": "Green",
        "category": "COLORS",
        "difficulty": 1,
        "display_order": 4,
        "points_reward": 20,
        "peppi_intro": "Now green! Listen...",
        "peppi_perfect": "PERFECT! Hara like grass and trees! 🌿",
        "peppi_good": "Nice! Green is fresh!",
        "peppi_try_again": "Nice try! Say - ha-ra!",
    },
    {
        "word": "सफेद",
        "romanization": "Safed",
        "meaning": "White",
        "category": "COLORS",
        "difficulty": 1,
        "display_order": 5,
        "points_reward": 20,
        "peppi_intro": "White now! Listen carefully...",
        "peppi_perfect": "EXCELLENT! Perfect safed! Pure like clouds! ☁️",
        "peppi_good": "Great! White sounds clean!",
        "peppi_try_again": "Good try! Say - sa-fed!",
    },

    # ========== ANIMALS (5 challenges) ==========
    {
        "word": "कुत्ता",
        "romanization": "Kutta",
        "meaning": "Dog",
        "category": "ANIMALS",
        "difficulty": 1,
        "display_order": 1,
        "points_reward": 20,
        "peppi_intro": "Let's learn dog! Listen...",
        "peppi_perfect": "WOOF WOOF! Perfect kutta! 🐕",
        "peppi_good": "Great! Dogs are our friends!",
        "peppi_try_again": "Nice try! Say - kut-ta!",
    },
    {
        "word": "बिल्ली",
        "romanization": "Billi",
        "meaning": "Cat",
        "category": "ANIMALS",
        "difficulty": 1,
        "display_order": 2,
        "points_reward": 20,
        "peppi_intro": "Now cat! Listen carefully...",
        "peppi_perfect": "MEOW! Perfect billi! 🐱",
        "peppi_good": "Nice! Cats are cute!",
        "peppi_try_again": "Good try! Say - bil-li!",
    },
    {
        "word": "हाथी",
        "romanization": "Haathi",
        "meaning": "Elephant",
        "category": "ANIMALS",
        "difficulty": 2,
        "display_order": 3,
        "points_reward": 25,
        "peppi_intro": "Big elephant! Listen...",
        "peppi_perfect": "AMAZING! Perfect haathi! So majestic! 🐘",
        "peppi_good": "Great! Elephants are wonderful!",
        "peppi_try_again": "Nice effort! Say - haa-thi!",
    },
    {
        "word": "शेर",
        "romanization": "Sher",
        "meaning": "Lion",
        "category": "ANIMALS",
        "difficulty": 1,
        "display_order": 4,
        "points_reward": 20,
        "peppi_intro": "The king of jungle! Listen...",
        "peppi_perfect": "ROAR! Perfect sher! You're brave! 🦁",
        "peppi_good": "Great! Strong like a lion!",
        "peppi_try_again": "Good try! Say - sher!",
    },
    {
        "word": "मोर",
        "romanization": "Mor",
        "meaning": "Peacock",
        "category": "ANIMALS",
        "difficulty": 1,
        "display_order": 5,
        "points_reward": 20,
        "peppi_intro": "National bird of India! Listen...",
        "peppi_perfect": "BEAUTIFUL! Perfect mor! So colorful! 🦚",
        "peppi_good": "Nice! Peacocks are gorgeous!",
        "peppi_try_again": "Good try! Say - mor!",
    },

    # ========== FOOD (3 challenges) ==========
    {
        "word": "रोटी",
        "romanization": "Roti",
        "meaning": "Bread/Flatbread",
        "category": "FOOD",
        "difficulty": 1,
        "display_order": 1,
        "points_reward": 20,
        "peppi_intro": "Yummy bread! Listen...",
        "peppi_perfect": "DELICIOUS! Perfect roti! Tasty! 🫓",
        "peppi_good": "Great! Roti is yummy!",
        "peppi_try_again": "Good try! Say - ro-ti!",
    },
    {
        "word": "पानी",
        "romanization": "Paani",
        "meaning": "Water",
        "category": "FOOD",
        "difficulty": 1,
        "display_order": 2,
        "points_reward": 20,
        "peppi_intro": "Essential water! Listen...",
        "peppi_perfect": "REFRESHING! Perfect paani! Stay hydrated! 💧",
        "peppi_good": "Nice! Water is important!",
        "peppi_try_again": "Good try! Say - paa-ni!",
    },
    {
        "word": "दूध",
        "romanization": "Doodh",
        "meaning": "Milk",
        "category": "FOOD",
        "difficulty": 1,
        "display_order": 3,
        "points_reward": 20,
        "peppi_intro": "Healthy milk! Listen...",
        "peppi_perfect": "HEALTHY! Perfect doodh! Grow strong! 🥛",
        "peppi_good": "Great! Milk makes you strong!",
        "peppi_try_again": "Nice try! Say - doodh!",
    },

    # ========== FESTIVAL (2 challenges) ==========
    {
        "word": "दीया",
        "romanization": "Diya",
        "meaning": "Lamp",
        "category": "FESTIVAL",
        "difficulty": 1,
        "display_order": 1,
        "points_reward": 25,
        "peppi_intro": "Festival lamp! Listen...",
        "peppi_perfect": "BRIGHT! Perfect diya! Light up the world! 🪔",
        "peppi_good": "Beautiful! Diyas bring light!",
        "peppi_try_again": "Good try! Say - di-ya!",
    },
    {
        "word": "मिठाई",
        "romanization": "Mithai",
        "meaning": "Sweets",
        "category": "FESTIVAL",
        "difficulty": 2,
        "display_order": 2,
        "points_reward": 25,
        "peppi_intro": "Yummy festival sweets! Listen...",
        "peppi_perfect": "SWEET! Perfect mithai! Festival time! 🍬",
        "peppi_good": "Nice! Sweets are festive!",
        "peppi_try_again": "Good try! Say - mi-tha-i!",
    },
]


class Command(BaseCommand):
    """Seed Peppi Mimic pronunciation challenges."""

    help = 'Seeds Hindi pronunciation challenges for Peppi Mimic feature'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing challenges before seeding',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Seeding Peppi Mimic challenges...'))

        if options['clear']:
            deleted_count, _ = PeppiMimicChallenge.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Cleared {deleted_count} existing challenges'))

        created_count = 0
        updated_count = 0
        skipped_count = 0

        for challenge_data in HINDI_CHALLENGES:
            # Use get_or_create with word+language as unique identifier
            challenge, created = PeppiMimicChallenge.objects.update_or_create(
                word=challenge_data['word'],
                language='HINDI',
                defaults={
                    'romanization': challenge_data['romanization'],
                    'meaning': challenge_data['meaning'],
                    'category': challenge_data['category'],
                    'difficulty': challenge_data['difficulty'],
                    'display_order': challenge_data['display_order'],
                    'points_reward': challenge_data['points_reward'],
                    'peppi_intro': challenge_data['peppi_intro'],
                    'peppi_perfect': challenge_data['peppi_perfect'],
                    'peppi_good': challenge_data['peppi_good'],
                    'peppi_try_again': challenge_data['peppi_try_again'],
                    'is_active': True,
                }
            )

            if created:
                created_count += 1
                self.stdout.write(f'  + Created: {challenge.word} ({challenge.romanization})')
            else:
                updated_count += 1
                self.stdout.write(f'  ~ Updated: {challenge.word} ({challenge.romanization})')

        # Summary by category
        self.stdout.write('\n' + self.style.SUCCESS('Challenge summary by category:'))
        for category, label in PeppiMimicChallenge.Category.choices:
            count = PeppiMimicChallenge.objects.filter(category=category, language='HINDI').count()
            if count > 0:
                self.stdout.write(f'  {label}: {count} challenges')

        total = PeppiMimicChallenge.objects.filter(language='HINDI', is_active=True).count()
        self.stdout.write('\n' + self.style.SUCCESS(
            f'Seeding complete!\n'
            f'  Created: {created_count}\n'
            f'  Updated: {updated_count}\n'
            f'  Total Hindi challenges: {total}'
        ))
