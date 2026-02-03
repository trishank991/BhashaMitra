"""
Seed L1 Curriculum Modules, Lessons, and Content Linking
Run: python manage.py seed_l1_modules_and_lessons
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.curriculum.models import (
    CurriculumLevel, CurriculumModule, Lesson, LessonContent,
    VocabularyTheme, Letter, Song
)
from apps.stories.models import Story


class Command(BaseCommand):
    help = 'Seed L1 curriculum modules, lessons, and content linking'

    def handle(self, *args, **options):
        self.stdout.write('🚀 Starting L1 Curriculum Seeding...\n')

        # Get L1 level
        try:
            l1 = CurriculumLevel.objects.get(code='L1')
        except CurriculumLevel.DoesNotExist:
            self.stdout.write(self.style.ERROR('❌ L1 level not found. Run seed_curriculum_levels first.'))
            return

        with transaction.atomic():
            modules_created = self.seed_modules(l1)
            lessons_created = self.seed_lessons()
            content_linked = self.link_content()

        # ===== SUMMARY =====
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('🎉 L1 CURRICULUM SEEDING COMPLETE!'))
        self.stdout.write('='*50)
        self.stdout.write(f'''
📊 Summary:
   • Modules created/updated: {modules_created}
   • Lessons created/updated: {lessons_created}
   • Content links created: {content_linked}

📈 Database Totals:
   • Total L1 Modules: {CurriculumModule.objects.filter(level=l1).count()}
   • Total L1 Lessons: {Lesson.objects.filter(module__level=l1).count()}
   • Total LessonContent links: {LessonContent.objects.filter(lesson__module__level=l1).count()}
        ''')

    def seed_modules(self, l1):
        """Create 6 curriculum modules for L1."""
        self.stdout.write('\n📦 Creating Curriculum Modules...')

        modules_data = [
            {
                'code': 'L1_LISTENING',
                'name_english': 'Listening & Understanding',
                'name_hindi': 'सुनना और समझना',
                'name_romanized': 'Sunna aur Samajhna',
                'description': 'Learn to listen and understand Hindi sounds, words, and sentences',
                'module_type': 'LISTENING',
                'emoji': '👂',
                'order': 1,
                'estimated_minutes': 60,
                'peppi_intro': 'नमस्ते बच्चों! आज हम सुनेंगे! कान खोलो और ध्यान से सुनो!',
            },
            {
                'code': 'L1_SPEAKING',
                'name_english': 'Speaking & Pronunciation',
                'name_hindi': 'बोलना और उच्चारण',
                'name_romanized': 'Bolna aur Uchcharan',
                'description': 'Practice speaking Hindi with correct pronunciation',
                'module_type': 'SPEAKING',
                'emoji': '🗣️',
                'order': 2,
                'estimated_minutes': 60,
                'peppi_intro': 'अब बोलने की बारी! मेरे साथ बोलो!',
            },
            {
                'code': 'L1_VOCABULARY',
                'name_english': 'Words & Meanings',
                'name_hindi': 'शब्द और अर्थ',
                'name_romanized': 'Shabd aur Arth',
                'description': 'Build your Hindi vocabulary with everyday words',
                'module_type': 'VOCABULARY',
                'emoji': '📚',
                'order': 3,
                'estimated_minutes': 90,
                'peppi_intro': 'आज हम शब्द सीखेंगे! हर शब्द का मतलब जानो!',
            },
            {
                'code': 'L1_ALPHABET',
                'name_english': 'Hindi Alphabet - Varnamala',
                'name_hindi': 'हिंदी वर्णमाला',
                'name_romanized': 'Hindi Varnamala',
                'description': 'Learn Swar (vowels) and Vyanjan (consonants)',
                'module_type': 'ALPHABET',
                'emoji': '🔤',
                'order': 4,
                'estimated_minutes': 120,
                'peppi_intro': 'आज हम हिंदी अक्षर सीखेंगे! अ आ इ ई!',
            },
            {
                'code': 'L1_SONGS',
                'name_english': 'Songs & Rhymes',
                'name_hindi': 'गाने और कविताएँ',
                'name_romanized': 'Gaane aur Kavitayen',
                'description': 'Learn Hindi through fun songs and nursery rhymes',
                'module_type': 'SONGS',
                'emoji': '🎵',
                'order': 5,
                'estimated_minutes': 45,
                'peppi_intro': 'गाना गाने का समय! मेरे साथ गाओ!',
            },
            {
                'code': 'L1_STORIES',
                'name_english': 'Stories & Tales',
                'name_hindi': 'कहानियाँ',
                'name_romanized': 'Kahaniyan',
                'description': 'Enjoy Hindi stories and learn through storytelling',
                'module_type': 'STORIES',
                'emoji': '📖',
                'order': 6,
                'estimated_minutes': 60,
                'peppi_intro': 'कहानी का समय! सुनो और सीखो!',
            },
        ]

        count = 0
        for mod_data in modules_data:
            module, created = CurriculumModule.objects.update_or_create(
                code=mod_data['code'],
                defaults={
                    'level': l1,
                    **mod_data
                }
            )
            if created:
                count += 1
                self.stdout.write(f'  ✅ Created: {mod_data["name_english"]}')
            else:
                self.stdout.write(f'  ♻️  Updated: {mod_data["name_english"]}')

        return count

    def seed_lessons(self):
        """Create 24 lessons across 6 modules."""
        self.stdout.write('\n📚 Creating Lessons...')

        lessons_data = [
            # ===== Listening Module (4 lessons) =====
            {
                'module_code': 'L1_LISTENING',
                'code': 'L1_LISTEN_01',
                'title_english': 'Hello Sounds!',
                'title_hindi': 'आवाज़ सुनो!',
                'title_romanized': 'Awaaz Suno!',
                'order': 1,
                'estimated_minutes': 15,
                'points_available': 25,
                'mastery_threshold': 60,
                'peppi_intro': 'नमस्ते! आज हम आवाज़ें सुनेंगे!',
                'peppi_success': 'वाह! बहुत अच्छे! तुम सुनने में माहिर हो!',
            },
            {
                'module_code': 'L1_LISTENING',
                'code': 'L1_LISTEN_02',
                'title_english': 'Family Voices',
                'title_hindi': 'परिवार की आवाज़ें',
                'title_romanized': 'Parivaar Ki Awaazein',
                'order': 2,
                'estimated_minutes': 15,
                'points_available': 25,
                'mastery_threshold': 60,
                'peppi_intro': 'अब सुनो परिवार के बारे में! माँ, पापा, दादी!',
                'peppi_success': 'शाबाश! परिवार की आवाज़ें पहचान लीं!',
            },
            {
                'module_code': 'L1_LISTENING',
                'code': 'L1_LISTEN_03',
                'title_english': 'Animal Sounds',
                'title_hindi': 'जानवरों की आवाज़ें',
                'title_romanized': 'Jaanwaron Ki Awaazein',
                'order': 3,
                'estimated_minutes': 15,
                'points_available': 25,
                'mastery_threshold': 60,
                'peppi_intro': 'जानवर कैसे बोलते हैं? कुत्ता भौं भौं! बिल्ली म्याऊं!',
                'peppi_success': 'बहुत बढ़िया! जानवरों की आवाज़ें आ गईं!',
            },
            {
                'module_code': 'L1_LISTENING',
                'code': 'L1_LISTEN_04',
                'title_english': 'Listening Master!',
                'title_hindi': 'सुनने में माहिर!',
                'title_romanized': 'Sunne Mein Maahir!',
                'order': 4,
                'estimated_minutes': 15,
                'points_available': 25,
                'mastery_threshold': 70,
                'peppi_intro': 'अब बड़ा टेस्ट! दिखाओ क्या सीखा!',
                'peppi_success': '🏆 वाह! तुम सुनने में माहिर हो गए!',
            },

            # ===== Speaking Module (4 lessons) =====
            {
                'module_code': 'L1_SPEAKING',
                'code': 'L1_SPEAK_01',
                'title_english': 'Say Namaste!',
                'title_hindi': 'नमस्ते बोलो!',
                'title_romanized': 'Namaste Bolo!',
                'order': 1,
                'estimated_minutes': 15,
                'points_available': 25,
                'mastery_threshold': 60,
                'peppi_intro': 'मेरे साथ बोलो - नमस्ते! ना-मस्-ते!',
                'peppi_success': 'वाह! बहुत सुंदर नमस्ते!',
            },
            {
                'module_code': 'L1_SPEAKING',
                'code': 'L1_SPEAK_02',
                'title_english': 'Family Names',
                'title_hindi': 'परिवार के नाम',
                'title_romanized': 'Parivaar Ke Naam',
                'order': 2,
                'estimated_minutes': 15,
                'points_available': 25,
                'mastery_threshold': 60,
                'peppi_intro': 'माँ बोलो! पापा बोलो! दादी बोलो!',
                'peppi_success': 'शाबाश! परिवार के नाम अच्छे से बोले!',
            },
            {
                'module_code': 'L1_SPEAKING',
                'code': 'L1_SPEAK_03',
                'title_english': 'Color Talk',
                'title_hindi': 'रंगों की बात',
                'title_romanized': 'Rangon Ki Baat',
                'order': 3,
                'estimated_minutes': 15,
                'points_available': 25,
                'mastery_threshold': 60,
                'peppi_intro': 'रंग बोलो! लाल! पीला! नीला! हरा!',
                'peppi_success': 'बहुत खूब! सारे रंग बोल लिए!',
            },
            {
                'module_code': 'L1_SPEAKING',
                'code': 'L1_SPEAK_04',
                'title_english': 'Speaking Star!',
                'title_hindi': 'बोलने का सितारा!',
                'title_romanized': 'Bolne Ka Sitara!',
                'order': 4,
                'estimated_minutes': 15,
                'points_available': 25,
                'mastery_threshold': 70,
                'peppi_intro': 'तुम बहुत अच्छा बोलते हो! अब मुझे दिखाओ!',
                'peppi_success': '⭐ तुम बोलने के सितारे हो!',
            },

            # ===== Vocabulary Module (4 lessons) =====
            {
                'module_code': 'L1_VOCABULARY',
                'code': 'L1_VOCAB_01',
                'title_english': 'Greetings & Basics',
                'title_hindi': 'अभिवादन',
                'title_romanized': 'Abhivaadan',
                'order': 1,
                'estimated_minutes': 20,
                'points_available': 35,
                'mastery_threshold': 60,
                'peppi_intro': 'पहला शब्द - नमस्ते! इसका मतलब है hello!',
                'peppi_success': 'बढ़िया! अभिवादन के शब्द आ गए!',
            },
            {
                'module_code': 'L1_VOCABULARY',
                'code': 'L1_VOCAB_02',
                'title_english': 'My Family',
                'title_hindi': 'मेरा परिवार',
                'title_romanized': 'Mera Parivaar',
                'order': 2,
                'estimated_minutes': 20,
                'points_available': 35,
                'mastery_threshold': 60,
                'peppi_intro': 'परिवार के शब्द! माँ means mother!',
                'peppi_success': 'वाह! पूरा परिवार जान लिया!',
            },
            {
                'module_code': 'L1_VOCABULARY',
                'code': 'L1_VOCAB_03',
                'title_english': 'Colors & Numbers',
                'title_hindi': 'रंग और संख्याएँ',
                'title_romanized': 'Rang aur Sankhyayen',
                'order': 3,
                'estimated_minutes': 25,
                'points_available': 40,
                'mastery_threshold': 60,
                'peppi_intro': 'रंग और गिनती! लाल means red! एक means one!',
                'peppi_success': 'शानदार! रंग और गिनती आ गए!',
            },
            {
                'module_code': 'L1_VOCABULARY',
                'code': 'L1_VOCAB_04',
                'title_english': 'Word Champion!',
                'title_hindi': 'शब्द चैंपियन!',
                'title_romanized': 'Shabd Champion!',
                'order': 4,
                'estimated_minutes': 25,
                'points_available': 40,
                'mastery_threshold': 70,
                'peppi_intro': 'तुम इतने शब्द जानते हो! अब टेस्ट!',
                'peppi_success': '🏆 शब्द चैंपियन! बहुत बढ़िया!',
            },

            # ===== Alphabet Module (4 lessons) =====
            {
                'module_code': 'L1_ALPHABET',
                'code': 'L1_ALPHA_01',
                'title_english': 'Meet the Swar (Vowels)',
                'title_hindi': 'स्वर से मिलो',
                'title_romanized': 'Swar Se Milo',
                'order': 1,
                'estimated_minutes': 30,
                'points_available': 50,
                'mastery_threshold': 60,
                'peppi_intro': 'पहले स्वर - अ आ इ ई उ ऊ! ये vowels हैं!',
                'peppi_success': 'वाह! स्वर सीख लिए!',
            },
            {
                'module_code': 'L1_ALPHABET',
                'code': 'L1_ALPHA_02',
                'title_english': 'Vyanjan Part 1 (क to ङ)',
                'title_hindi': 'व्यंजन भाग १',
                'title_romanized': 'Vyanjan Bhag 1',
                'order': 2,
                'estimated_minutes': 30,
                'points_available': 50,
                'mastery_threshold': 60,
                'peppi_intro': 'अब व्यंजन! क से कबूतर! ख से खरगोश!',
                'peppi_success': 'बढ़िया! क-वर्ग आ गया!',
            },
            {
                'module_code': 'L1_ALPHABET',
                'code': 'L1_ALPHA_03',
                'title_english': 'Vyanjan Part 2 (च to न)',
                'title_hindi': 'व्यंजन भाग २',
                'title_romanized': 'Vyanjan Bhag 2',
                'order': 3,
                'estimated_minutes': 30,
                'points_available': 50,
                'mastery_threshold': 60,
                'peppi_intro': 'और व्यंजन! च से चिड़िया! त से तितली!',
                'peppi_success': 'शाबाश! और व्यंजन आ गए!',
            },
            {
                'module_code': 'L1_ALPHABET',
                'code': 'L1_ALPHA_04',
                'title_english': 'Alphabet Master!',
                'title_hindi': 'वर्णमाला मास्टर!',
                'title_romanized': 'Varnamala Master!',
                'order': 4,
                'estimated_minutes': 30,
                'points_available': 50,
                'mastery_threshold': 70,
                'peppi_intro': 'तुम हिंदी वर्णमाला जानते हो! अब बड़ा टेस्ट!',
                'peppi_success': '🏆 वर्णमाला मास्टर! अद्भुत!',
            },

            # ===== Songs Module (4 lessons) =====
            {
                'module_code': 'L1_SONGS',
                'code': 'L1_SONG_01',
                'title_english': 'Fish is Queen - Machli Jal Ki Rani',
                'title_hindi': 'मछली जल की रानी',
                'title_romanized': 'Machli Jal Ki Rani',
                'order': 1,
                'estimated_minutes': 10,
                'points_available': 20,
                'mastery_threshold': 50,
                'peppi_intro': 'गाना गाने का समय! मछली जल की रानी है!',
                'peppi_success': 'वाह! क्या खूब गाया!',
            },
            {
                'module_code': 'L1_SONGS',
                'code': 'L1_SONG_02',
                'title_english': 'Wooden Horse - Lakdi Ki Kathi',
                'title_hindi': 'लकड़ी की काठी',
                'title_romanized': 'Lakdi Ki Kathi',
                'order': 2,
                'estimated_minutes': 10,
                'points_available': 20,
                'mastery_threshold': 50,
                'peppi_intro': 'लकड़ी की काठी, काठी पे घोड़ा! गाओ!',
                'peppi_success': 'बहुत मज़ा आया! शाबाश!',
            },
            {
                'module_code': 'L1_SONGS',
                'code': 'L1_SONG_03',
                'title_english': 'Uncle Moon - Chanda Mama',
                'title_hindi': 'चंदा मामा दूर के',
                'title_romanized': 'Chanda Mama Door Ke',
                'order': 3,
                'estimated_minutes': 15,
                'points_available': 20,
                'mastery_threshold': 50,
                'peppi_intro': 'चंदा मामा दूर के! गाओ मेरे साथ!',
                'peppi_success': 'क्या सुंदर गाना गाया!',
            },
            {
                'module_code': 'L1_SONGS',
                'code': 'L1_SONG_04',
                'title_english': 'Song Time Fun!',
                'title_hindi': 'गाना मज़ा!',
                'title_romanized': 'Gaana Maza!',
                'order': 4,
                'estimated_minutes': 10,
                'points_available': 15,
                'mastery_threshold': 100,
                'peppi_intro': 'सब गाने साथ में गाओ! मज़ा आएगा!',
                'peppi_success': '🎵 तुम गाने के सुपरस्टार हो!',
            },

            # ===== Stories Module (4 lessons) =====
            {
                'module_code': 'L1_STORIES',
                'code': 'L1_STORY_01',
                'title_english': "Peppi's New Home",
                'title_hindi': 'पेप्पी का नया घर',
                'title_romanized': 'Peppi Ka Naya Ghar',
                'order': 1,
                'estimated_minutes': 15,
                'points_available': 25,
                'mastery_threshold': 60,
                'peppi_intro': 'मैं कहानी सुनाती हूँ! यह मेरी कहानी है!',
                'peppi_success': 'वाह! कहानी समझ गए!',
            },
            {
                'module_code': 'L1_STORIES',
                'code': 'L1_STORY_02',
                'title_english': 'My Dear Mother',
                'title_hindi': 'मेरी प्यारी माँ',
                'title_romanized': 'Meri Pyaari Maa',
                'order': 2,
                'estimated_minutes': 15,
                'points_available': 25,
                'mastery_threshold': 60,
                'peppi_intro': 'परिवार की कहानी सुनो! माँ, पापा सब हैं!',
                'peppi_success': 'बहुत प्यारी कहानी थी!',
            },
            {
                'module_code': 'L1_STORIES',
                'code': 'L1_STORY_03',
                'title_english': 'Fun in the Jungle',
                'title_hindi': 'जंगल में मंगल',
                'title_romanized': 'Jungle Mein Mangal',
                'order': 3,
                'estimated_minutes': 15,
                'points_available': 25,
                'mastery_threshold': 60,
                'peppi_intro': 'जानवरों की मज़ेदार कहानी! शेर, बंदर, हाथी!',
                'peppi_success': 'वाह! जंगल की कहानी आ गई!',
            },
            {
                'module_code': 'L1_STORIES',
                'code': 'L1_STORY_04',
                'title_english': 'Story Champion!',
                'title_hindi': 'कहानी चैंपियन!',
                'title_romanized': 'Kahani Champion!',
                'order': 4,
                'estimated_minutes': 15,
                'points_available': 25,
                'mastery_threshold': 70,
                'peppi_intro': 'तुम कहानी चैंपियन हो! बताओ क्या सीखा!',
                'peppi_success': '🏆 कहानी चैंपियन! शानदार!',
            },
        ]

        count = 0
        for lesson_data in lessons_data:
            module_code = lesson_data.pop('module_code')
            try:
                module = CurriculumModule.objects.get(code=module_code)
                lesson, created = Lesson.objects.update_or_create(
                    code=lesson_data['code'],
                    defaults={
                        'module': module,
                        **lesson_data
                    }
                )
                if created:
                    count += 1
                    self.stdout.write(f'  ✅ {lesson_data["title_english"]}')
            except CurriculumModule.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  ⚠️ Module {module_code} not found'))

        return count

    def link_content(self):
        """Link existing content to lessons."""
        self.stdout.write('\n🔗 Linking Content to Lessons...')

        count = 0

        # Link vocabulary themes to vocabulary lessons
        vocab_links = [
            ('L1_VOCAB_01', 'Greetings', 1),
            ('L1_VOCAB_02', 'Family', 1),
            ('L1_VOCAB_03', 'Colors', 1),
            ('L1_VOCAB_03', 'Numbers', 2),
            ('L1_LISTEN_01', 'Greetings', 1),
            ('L1_LISTEN_02', 'Family', 1),
            ('L1_LISTEN_03', 'Animals', 1),
            ('L1_SPEAK_02', 'Family', 1),
            ('L1_SPEAK_03', 'Colors', 1),
        ]

        for lesson_code, theme_name, seq_order in vocab_links:
            try:
                lesson = Lesson.objects.get(code=lesson_code)
                theme = VocabularyTheme.objects.filter(name__icontains=theme_name).first()
                if theme:
                    _, created = LessonContent.objects.get_or_create(
                        lesson=lesson,
                        content_type='VOCABULARY_THEME',
                        content_id=theme.id,
                        defaults={'sequence_order': seq_order}
                    )
                    if created:
                        count += 1
                        self.stdout.write(f'  ✅ Linked {theme_name} to {lesson_code}')
            except Lesson.DoesNotExist:
                pass

        # Link songs to song lessons
        song_mappings = [
            ('L1_SONG_01', 'मछली'),
            ('L1_SONG_02', 'लकड़ी'),
            ('L1_SONG_03', 'चंदा'),
        ]

        for lesson_code, song_keyword in song_mappings:
            try:
                lesson = Lesson.objects.get(code=lesson_code)
                song = Song.objects.filter(title_hindi__icontains=song_keyword).first()
                if song:
                    _, created = LessonContent.objects.get_or_create(
                        lesson=lesson,
                        content_type='STORY',  # Using STORY as a proxy since Song is not in ContentType choices
                        content_id=song.id,
                        defaults={'sequence_order': 1}
                    )
                    if created:
                        count += 1
                        self.stdout.write(f'  ✅ Linked song to {lesson_code}')
            except Lesson.DoesNotExist:
                pass

        # Link stories to story lessons
        story_mappings = [
            ('L1_STORY_01', "Peppi"),
            ('L1_STORY_02', 'Mother'),
            ('L1_STORY_03', 'Jungle'),
        ]

        for lesson_code, story_keyword in story_mappings:
            try:
                lesson = Lesson.objects.get(code=lesson_code)
                story = Story.objects.filter(title__icontains=story_keyword).first()
                if story:
                    _, created = LessonContent.objects.get_or_create(
                        lesson=lesson,
                        content_type='STORY',
                        content_id=story.id,
                        defaults={'sequence_order': 1}
                    )
                    if created:
                        count += 1
                        self.stdout.write(f'  ✅ Linked story to {lesson_code}')
            except Lesson.DoesNotExist:
                pass

        return count
