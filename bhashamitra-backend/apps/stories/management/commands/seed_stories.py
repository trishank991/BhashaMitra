"""
Management command to seed stories for all languages.
Includes regular stories and festival stories.
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.stories.models import Story, StoryPage
from apps.festivals.models import Festival, FestivalStory


class Command(BaseCommand):
    help = 'Seed stories for all languages including festival stories'

    def add_arguments(self, parser):
        parser.add_argument(
            '--language',
            type=str,
            help='Specific language to seed (HINDI, TAMIL, PUNJABI, GUJARATI)',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing stories before seeding',
        )

    def handle(self, *args, **options):
        language = options.get('language')
        clear = options.get('clear', False)

        if clear:
            self.stdout.write(self.style.WARNING('Clearing existing stories...'))
            if language:
                Story.objects.filter(language=language.upper()).delete()
            else:
                Story.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Stories cleared.'))

        languages = [language.upper()] if language else ['HINDI', 'TAMIL', 'PUNJABI', 'GUJARATI']

        for lang in languages:
            self.stdout.write(f'\nSeeding stories for {lang}...')
            try:
                if lang == 'HINDI':
                    self._seed_hindi_stories()
                elif lang == 'TAMIL':
                    self._seed_tamil_stories()
                elif lang == 'PUNJABI':
                    self._seed_punjabi_stories()
                elif lang == 'GUJARATI':
                    self._seed_gujarati_stories()
                self.stdout.write(self.style.SUCCESS(f'  {lang} stories seeded successfully!'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  Error seeding {lang}: {e}'))

        # Summary
        total = Story.objects.count()
        self.stdout.write(self.style.SUCCESS(f'\nTotal stories in database: {total}'))

    def _create_story_with_pages(self, story_data, pages_data):
        """Helper to create a story with its pages."""
        story, created = Story.objects.update_or_create(
            storyweaver_id=story_data['storyweaver_id'],
            defaults=story_data
        )

        if created:
            # Create pages only for new stories
            for page_data in pages_data:
                StoryPage.objects.create(story=story, **page_data)

        return story, created

    def _link_to_festival(self, story, festival_name, is_primary=False):
        """Link a story to a festival."""
        try:
            festival = Festival.objects.get(name__icontains=festival_name)
            FestivalStory.objects.get_or_create(
                festival=festival,
                story=story,
                defaults={'is_primary': is_primary}
            )
            return True
        except Festival.DoesNotExist:
            self.stdout.write(self.style.WARNING(f'    Festival "{festival_name}" not found'))
            return False

    @transaction.atomic
    def _seed_hindi_stories(self):
        """Seed Hindi stories including festival stories."""

        # Story 1: Peppi's New Friend (Peppi Ka Naya Dost)
        story_data = {
            'storyweaver_id': 'bm-hi-001',
            'title': 'पेप्पी का नया दोस्त',
            'title_translit': 'Peppi Ka Naya Dost',
            'language': 'HINDI',
            'level': 1,
            'page_count': 5,
            'synopsis': 'Peppi the parrot makes a new friend in the garden and learns about sharing.',
            'author': 'BhashaMitra Team',
            'categories': ['friendship', 'animals', 'values'],
            'tier': 'FREE',
            'age_min': 3,
            'age_max': 6,
            'is_l1_content': True,
            'is_active': True,
        }
        pages = [
            {'page_number': 1, 'text_content': 'पेप्पी एक हरा तोता है।', 'text_romanized': 'Peppi ek hara tota hai.'},
            {'page_number': 2, 'text_content': 'वह बगीचे में रहता है।', 'text_romanized': 'Vah bagiche mein rehta hai.'},
            {'page_number': 3, 'text_content': 'एक दिन उसने एक गिलहरी देखी।', 'text_romanized': 'Ek din usne ek gilhari dekhi.'},
            {'page_number': 4, 'text_content': '"नमस्ते! मैं पेप्पी हूँ।"', 'text_romanized': '"Namaste! Main Peppi hoon."'},
            {'page_number': 5, 'text_content': 'अब वे अच्छे दोस्त हैं।', 'text_romanized': 'Ab ve achhe dost hain.'},
        ]
        story, created = self._create_story_with_pages(story_data, pages)
        self.stdout.write(f'  {"Created" if created else "Updated"}: {story.title}')

        # Story 2: The Red Apple (Laal Seb)
        story_data = {
            'storyweaver_id': 'bm-hi-002',
            'title': 'लाल सेब',
            'title_translit': 'Laal Seb',
            'language': 'HINDI',
            'level': 1,
            'page_count': 4,
            'synopsis': 'A child finds a red apple and shares it with friends.',
            'author': 'BhashaMitra Team',
            'categories': ['food', 'sharing', 'colors'],
            'tier': 'FREE',
            'age_min': 3,
            'age_max': 5,
            'is_l1_content': True,
            'is_active': True,
        }
        pages = [
            {'page_number': 1, 'text_content': 'पेड़ पर एक सेब है।', 'text_romanized': 'Ped par ek seb hai.'},
            {'page_number': 2, 'text_content': 'सेब लाल है।', 'text_romanized': 'Seb laal hai.'},
            {'page_number': 3, 'text_content': 'राज ने सेब तोड़ा।', 'text_romanized': 'Raj ne seb toda.'},
            {'page_number': 4, 'text_content': 'उसने सबके साथ बाँटा।', 'text_romanized': 'Usne sabke saath baanta.'},
        ]
        story, created = self._create_story_with_pages(story_data, pages)
        self.stdout.write(f'  {"Created" if created else "Updated"}: {story.title}')

        # Story 3: My Family (Mera Parivaar)
        story_data = {
            'storyweaver_id': 'bm-hi-003',
            'title': 'मेरा परिवार',
            'title_translit': 'Mera Parivaar',
            'language': 'HINDI',
            'level': 1,
            'page_count': 6,
            'synopsis': 'A child introduces their loving family members.',
            'author': 'BhashaMitra Team',
            'categories': ['family', 'relationships', 'love'],
            'tier': 'FREE',
            'age_min': 3,
            'age_max': 6,
            'is_l1_content': True,
            'is_active': True,
        }
        pages = [
            {'page_number': 1, 'text_content': 'यह मेरा घर है।', 'text_romanized': 'Yeh mera ghar hai.'},
            {'page_number': 2, 'text_content': 'ये मेरे पापा हैं।', 'text_romanized': 'Ye mere papa hain.'},
            {'page_number': 3, 'text_content': 'ये मेरी माँ हैं।', 'text_romanized': 'Ye meri maa hain.'},
            {'page_number': 4, 'text_content': 'यह मेरी बहन है।', 'text_romanized': 'Yeh meri behen hai.'},
            {'page_number': 5, 'text_content': 'यह मेरा भाई है।', 'text_romanized': 'Yeh mera bhai hai.'},
            {'page_number': 6, 'text_content': 'हम सब साथ रहते हैं।', 'text_romanized': 'Hum sab saath rehte hain.'},
        ]
        story, created = self._create_story_with_pages(story_data, pages)
        self.stdout.write(f'  {"Created" if created else "Updated"}: {story.title}')

        # Story 4: The Thirsty Crow (Pyaasa Kauwa)
        story_data = {
            'storyweaver_id': 'bm-hi-004',
            'title': 'प्यासा कौआ',
            'title_translit': 'Pyaasa Kauwa',
            'language': 'HINDI',
            'level': 2,
            'page_count': 6,
            'synopsis': 'A clever crow finds a way to drink water from a pot.',
            'author': 'BhashaMitra Team',
            'categories': ['classic', 'animals', 'problem-solving'],
            'tier': 'STANDARD',
            'age_min': 4,
            'age_max': 7,
            'is_l1_content': False,
            'is_active': True,
        }
        pages = [
            {'page_number': 1, 'text_content': 'एक कौआ बहुत प्यासा था।', 'text_romanized': 'Ek kauwa bahut pyaasa tha.'},
            {'page_number': 2, 'text_content': 'उसने एक घड़ा देखा।', 'text_romanized': 'Usne ek ghada dekha.'},
            {'page_number': 3, 'text_content': 'पानी बहुत नीचे था।', 'text_romanized': 'Paani bahut neeche tha.'},
            {'page_number': 4, 'text_content': 'कौआ ने सोचा।', 'text_romanized': 'Kauwa ne socha.'},
            {'page_number': 5, 'text_content': 'उसने कंकड़ डाले।', 'text_romanized': 'Usne kankad daale.'},
            {'page_number': 6, 'text_content': 'पानी ऊपर आया!', 'text_romanized': 'Paani upar aaya!'},
        ]
        story, created = self._create_story_with_pages(story_data, pages)
        self.stdout.write(f'  {"Created" if created else "Updated"}: {story.title}')

        # Story 5: The Clever Fox (Chatur Lomdi)
        story_data = {
            'storyweaver_id': 'bm-hi-005',
            'title': 'चतुर लोमड़ी',
            'title_translit': 'Chatur Lomdi',
            'language': 'HINDI',
            'level': 2,
            'page_count': 5,
            'synopsis': 'A fox uses its wit to escape from trouble.',
            'author': 'BhashaMitra Team',
            'categories': ['classic', 'animals', 'wit'],
            'tier': 'STANDARD',
            'age_min': 5,
            'age_max': 8,
            'is_l1_content': False,
            'is_active': True,
        }
        pages = [
            {'page_number': 1, 'text_content': 'जंगल में एक लोमड़ी थी।', 'text_romanized': 'Jungle mein ek lomdi thi.'},
            {'page_number': 2, 'text_content': 'वह बहुत चतुर थी।', 'text_romanized': 'Vah bahut chatur thi.'},
            {'page_number': 3, 'text_content': 'एक दिन शेर आया।', 'text_romanized': 'Ek din sher aaya.'},
            {'page_number': 4, 'text_content': 'लोमड़ी ने तरकीब सोची।', 'text_romanized': 'Lomdi ne tarkeeb sochi.'},
            {'page_number': 5, 'text_content': 'वह सुरक्षित बच गई।', 'text_romanized': 'Vah surakshit bach gayi.'},
        ]
        story, created = self._create_story_with_pages(story_data, pages)
        self.stdout.write(f'  {"Created" if created else "Updated"}: {story.title}')

        # Festival Story: Diwali Lights (Diwali Ki Roshni)
        story_data = {
            'storyweaver_id': 'bm-hi-fest-diwali',
            'title': 'दिवाली की रोशनी',
            'title_translit': 'Diwali Ki Roshni',
            'language': 'HINDI',
            'level': 1,
            'page_count': 5,
            'synopsis': 'Peppi celebrates Diwali with lights and sweets.',
            'author': 'BhashaMitra Team',
            'categories': ['festival', 'diwali', 'celebration'],
            'tier': 'FREE',
            'age_min': 3,
            'age_max': 7,
            'is_l1_content': True,
            'is_active': True,
        }
        pages = [
            {'page_number': 1, 'text_content': 'आज दिवाली है!', 'text_romanized': 'Aaj Diwali hai!'},
            {'page_number': 2, 'text_content': 'पेप्पी बहुत खुश है।', 'text_romanized': 'Peppi bahut khush hai.'},
            {'page_number': 3, 'text_content': 'घर में दीये जले हैं।', 'text_romanized': 'Ghar mein diye jale hain.'},
            {'page_number': 4, 'text_content': 'मिठाई बहुत स्वादिष्ट है।', 'text_romanized': 'Mithai bahut swadisht hai.'},
            {'page_number': 5, 'text_content': 'सबको दिवाली मुबारक!', 'text_romanized': 'Sabko Diwali Mubarak!'},
        ]
        story, created = self._create_story_with_pages(story_data, pages)
        self._link_to_festival(story, 'Diwali', is_primary=True)
        self.stdout.write(f'  {"Created" if created else "Updated"}: {story.title} (Festival)')

        # Festival Story: Holi Colors (Holi Ke Rang)
        story_data = {
            'storyweaver_id': 'bm-hi-fest-holi',
            'title': 'होली के रंग',
            'title_translit': 'Holi Ke Rang',
            'language': 'HINDI',
            'level': 1,
            'page_count': 5,
            'synopsis': 'Friends play with colors during Holi festival.',
            'author': 'BhashaMitra Team',
            'categories': ['festival', 'holi', 'colors'],
            'tier': 'FREE',
            'age_min': 3,
            'age_max': 7,
            'is_l1_content': True,
            'is_active': True,
        }
        pages = [
            {'page_number': 1, 'text_content': 'आज होली है!', 'text_romanized': 'Aaj Holi hai!'},
            {'page_number': 2, 'text_content': 'लाल, पीला, हरा, नीला।', 'text_romanized': 'Laal, peela, hara, neela.'},
            {'page_number': 3, 'text_content': 'सब रंगों से खेलते हैं।', 'text_romanized': 'Sab rangon se khelte hain.'},
            {'page_number': 4, 'text_content': 'पेप्पी भी रंगीन हो गया!', 'text_romanized': 'Peppi bhi rangeen ho gaya!'},
            {'page_number': 5, 'text_content': 'होली मुबारक!', 'text_romanized': 'Holi Mubarak!'},
        ]
        story, created = self._create_story_with_pages(story_data, pages)
        self._link_to_festival(story, 'Holi', is_primary=True)
        self.stdout.write(f'  {"Created" if created else "Updated"}: {story.title} (Festival)')

        # Festival Story: Raksha Bandhan
        story_data = {
            'storyweaver_id': 'bm-hi-fest-rakhi',
            'title': 'राखी का त्योहार',
            'title_translit': 'Rakhi Ka Tyohar',
            'language': 'HINDI',
            'level': 1,
            'page_count': 5,
            'synopsis': 'A sister ties rakhi to her brother with love.',
            'author': 'BhashaMitra Team',
            'categories': ['festival', 'raksha bandhan', 'siblings'],
            'tier': 'FREE',
            'age_min': 3,
            'age_max': 7,
            'is_l1_content': True,
            'is_active': True,
        }
        pages = [
            {'page_number': 1, 'text_content': 'आज रक्षाबंधन है।', 'text_romanized': 'Aaj Raksha Bandhan hai.'},
            {'page_number': 2, 'text_content': 'दीदी ने राखी ली।', 'text_romanized': 'Didi ne rakhi li.'},
            {'page_number': 3, 'text_content': 'भाई की कलाई पर बाँधी।', 'text_romanized': 'Bhai ki kalai par baandhi.'},
            {'page_number': 4, 'text_content': 'भाई ने मिठाई दी।', 'text_romanized': 'Bhai ne mithai di.'},
            {'page_number': 5, 'text_content': 'प्यार का बंधन!', 'text_romanized': 'Pyaar ka bandhan!'},
        ]
        story, created = self._create_story_with_pages(story_data, pages)
        self._link_to_festival(story, 'Raksha Bandhan', is_primary=True)
        self.stdout.write(f'  {"Created" if created else "Updated"}: {story.title} (Festival)')

        count = Story.objects.filter(language='HINDI').count()
        self.stdout.write(f'  Total Hindi stories: {count}')

    @transaction.atomic
    def _seed_tamil_stories(self):
        """Seed Tamil stories including festival stories."""

        # Story 1: Peppi's New Friend
        story_data = {
            'storyweaver_id': 'bm-ta-001',
            'title': 'பெப்பியின் புதிய நண்பன்',
            'title_translit': "Peppiyin Pudhiya Nanban",
            'language': 'TAMIL',
            'level': 1,
            'page_count': 5,
            'synopsis': 'Peppi the parrot makes a new friend in the garden.',
            'author': 'BhashaMitra Team',
            'categories': ['friendship', 'animals', 'values'],
            'tier': 'FREE',
            'age_min': 3,
            'age_max': 6,
            'is_l1_content': True,
            'is_active': True,
        }
        pages = [
            {'page_number': 1, 'text_content': 'பெப்பி ஒரு பச்சை கிளி.', 'text_romanized': 'Peppi oru pachai kili.'},
            {'page_number': 2, 'text_content': 'அது தோட்டத்தில் வாழ்கிறது.', 'text_romanized': 'Adhu thottathil vaazhgiradhu.'},
            {'page_number': 3, 'text_content': 'ஒரு நாள் அணில் வந்தது.', 'text_romanized': 'Oru naal anil vandhadhu.'},
            {'page_number': 4, 'text_content': '"வணக்கம்! நான் பெப்பி."', 'text_romanized': '"Vanakkam! Naan Peppi."'},
            {'page_number': 5, 'text_content': 'இப்போது அவர்கள் நல்ல நண்பர்கள்.', 'text_romanized': 'Ippodhu avargal nalla nanbargal.'},
        ]
        story, created = self._create_story_with_pages(story_data, pages)
        self.stdout.write(f'  {"Created" if created else "Updated"}: {story.title}')

        # Story 2: The Red Apple
        story_data = {
            'storyweaver_id': 'bm-ta-002',
            'title': 'சிவப்பு ஆப்பிள்',
            'title_translit': 'Sivappu Apple',
            'language': 'TAMIL',
            'level': 1,
            'page_count': 4,
            'synopsis': 'A child finds a red apple and shares it with friends.',
            'author': 'BhashaMitra Team',
            'categories': ['food', 'sharing', 'colors'],
            'tier': 'FREE',
            'age_min': 3,
            'age_max': 5,
            'is_l1_content': True,
            'is_active': True,
        }
        pages = [
            {'page_number': 1, 'text_content': 'மரத்தில் ஒரு ஆப்பிள்.', 'text_romanized': 'Marathil oru apple.'},
            {'page_number': 2, 'text_content': 'ஆப்பிள் சிவப்பு நிறம்.', 'text_romanized': 'Apple sivappu niram.'},
            {'page_number': 3, 'text_content': 'ராஜா ஆப்பிள் பறித்தான்.', 'text_romanized': 'Raja apple parithan.'},
            {'page_number': 4, 'text_content': 'எல்லோருக்கும் பகிர்ந்தான்.', 'text_romanized': 'Ellorukum pagirndan.'},
        ]
        story, created = self._create_story_with_pages(story_data, pages)
        self.stdout.write(f'  {"Created" if created else "Updated"}: {story.title}')

        # Story 3: My Family
        story_data = {
            'storyweaver_id': 'bm-ta-003',
            'title': 'என் குடும்பம்',
            'title_translit': 'En Kudumbam',
            'language': 'TAMIL',
            'level': 1,
            'page_count': 6,
            'synopsis': 'A child introduces their loving family members.',
            'author': 'BhashaMitra Team',
            'categories': ['family', 'relationships', 'love'],
            'tier': 'FREE',
            'age_min': 3,
            'age_max': 6,
            'is_l1_content': True,
            'is_active': True,
        }
        pages = [
            {'page_number': 1, 'text_content': 'இது என் வீடு.', 'text_romanized': 'Idhu en veedu.'},
            {'page_number': 2, 'text_content': 'இவர் என் அப்பா.', 'text_romanized': 'Ivar en appa.'},
            {'page_number': 3, 'text_content': 'இவர் என் அம்மா.', 'text_romanized': 'Ivar en amma.'},
            {'page_number': 4, 'text_content': 'இவள் என் தங்கை.', 'text_romanized': 'Ival en thangai.'},
            {'page_number': 5, 'text_content': 'இவன் என் தம்பி.', 'text_romanized': 'Ivan en thambi.'},
            {'page_number': 6, 'text_content': 'நாங்கள் ஒன்றாக வாழ்கிறோம்.', 'text_romanized': 'Naangal ondraaga vaazhgirom.'},
        ]
        story, created = self._create_story_with_pages(story_data, pages)
        self.stdout.write(f'  {"Created" if created else "Updated"}: {story.title}')

        # Story 4: The Thirsty Crow
        story_data = {
            'storyweaver_id': 'bm-ta-004',
            'title': 'தாகமான காகம்',
            'title_translit': 'Thagamana Kagam',
            'language': 'TAMIL',
            'level': 2,
            'page_count': 6,
            'synopsis': 'A clever crow finds a way to drink water.',
            'author': 'BhashaMitra Team',
            'categories': ['classic', 'animals', 'problem-solving'],
            'tier': 'STANDARD',
            'age_min': 4,
            'age_max': 7,
            'is_l1_content': False,
            'is_active': True,
        }
        pages = [
            {'page_number': 1, 'text_content': 'ஒரு காகம் மிகவும் தாகமாக இருந்தது.', 'text_romanized': 'Oru kagam migavum thagamaga irundhadhu.'},
            {'page_number': 2, 'text_content': 'அது ஒரு குடம் கண்டது.', 'text_romanized': 'Adhu oru kudam kandadhu.'},
            {'page_number': 3, 'text_content': 'தண்ணீர் கீழே இருந்தது.', 'text_romanized': 'Thanneer keezhe irundhadhu.'},
            {'page_number': 4, 'text_content': 'காகம் யோசித்தது.', 'text_romanized': 'Kagam yosithadhu.'},
            {'page_number': 5, 'text_content': 'கற்களைப் போட்டது.', 'text_romanized': 'Karkalaip pottadhu.'},
            {'page_number': 6, 'text_content': 'தண்ணீர் மேலே வந்தது!', 'text_romanized': 'Thanneer mele vandhadhu!'},
        ]
        story, created = self._create_story_with_pages(story_data, pages)
        self.stdout.write(f'  {"Created" if created else "Updated"}: {story.title}')

        # Story 5: The Clever Fox
        story_data = {
            'storyweaver_id': 'bm-ta-005',
            'title': 'புத்திசாலி நரி',
            'title_translit': 'Budhisali Nari',
            'language': 'TAMIL',
            'level': 2,
            'page_count': 5,
            'synopsis': 'A fox uses its wit to escape trouble.',
            'author': 'BhashaMitra Team',
            'categories': ['classic', 'animals', 'wit'],
            'tier': 'STANDARD',
            'age_min': 5,
            'age_max': 8,
            'is_l1_content': False,
            'is_active': True,
        }
        pages = [
            {'page_number': 1, 'text_content': 'காட்டில் ஒரு நரி இருந்தது.', 'text_romanized': 'Kaattil oru nari irundhadhu.'},
            {'page_number': 2, 'text_content': 'அது மிகவும் புத்திசாலி.', 'text_romanized': 'Adhu migavum budhisali.'},
            {'page_number': 3, 'text_content': 'ஒரு நாள் சிங்கம் வந்தது.', 'text_romanized': 'Oru naal singam vandhadhu.'},
            {'page_number': 4, 'text_content': 'நரி ஒரு தந்திரம் செய்தது.', 'text_romanized': 'Nari oru thandhiram seidhadhu.'},
            {'page_number': 5, 'text_content': 'அது பத்திரமாக தப்பித்தது.', 'text_romanized': 'Adhu pathiramaga thappithadhu.'},
        ]
        story, created = self._create_story_with_pages(story_data, pages)
        self.stdout.write(f'  {"Created" if created else "Updated"}: {story.title}')

        # Story 6: The Greedy Dog
        story_data = {
            'storyweaver_id': 'bm-ta-006',
            'title': 'பேராசை நாய்',
            'title_translit': 'Perasai Naai',
            'language': 'TAMIL',
            'level': 2,
            'page_count': 5,
            'synopsis': 'A dog learns not to be greedy.',
            'author': 'BhashaMitra Team',
            'categories': ['classic', 'animals', 'morals'],
            'tier': 'STANDARD',
            'age_min': 4,
            'age_max': 7,
            'is_l1_content': False,
            'is_active': True,
        }
        pages = [
            {'page_number': 1, 'text_content': 'ஒரு நாய் ஒரு எலும்பு கொண்டிருந்தது.', 'text_romanized': 'Oru naai oru elumbu kondirundhadu.'},
            {'page_number': 2, 'text_content': 'அது பாலத்தைக் கடந்தது.', 'text_romanized': 'Adhu paalaththaik kadandhadhu.'},
            {'page_number': 3, 'text_content': 'தண்ணீரில் தன் நிழலைப் பார்த்தது.', 'text_romanized': 'Thaneeril than nizhalaip parthadhu.'},
            {'page_number': 4, 'text_content': 'மற்றொரு நாய் என்று நினைத்தது.', 'text_romanized': 'Matroru naai endru ninaithadhu.'},
            {'page_number': 5, 'text_content': 'குரைத்தது, எலும்பு விழுந்தது!', 'text_romanized': 'Kuraithadhu, elumbu vizhundhadhu!'},
        ]
        story, created = self._create_story_with_pages(story_data, pages)
        self.stdout.write(f'  {"Created" if created else "Updated"}: {story.title}')

        # Festival Story: Pongal
        story_data = {
            'storyweaver_id': 'bm-ta-fest-pongal',
            'title': 'பொங்கல் திருநாள்',
            'title_translit': 'Pongal Thirunaal',
            'language': 'TAMIL',
            'level': 1,
            'page_count': 5,
            'synopsis': 'Celebrating Pongal with family.',
            'author': 'BhashaMitra Team',
            'categories': ['festival', 'pongal', 'harvest'],
            'tier': 'FREE',
            'age_min': 3,
            'age_max': 7,
            'is_l1_content': True,
            'is_active': True,
        }
        pages = [
            {'page_number': 1, 'text_content': 'இன்று பொங்கல்!', 'text_romanized': 'Indru Pongal!'},
            {'page_number': 2, 'text_content': 'பானையில் பால் பொங்குகிறது.', 'text_romanized': 'Panaiyil paal pongugiradhu.'},
            {'page_number': 3, 'text_content': 'பொங்கலோ பொங்கல்!', 'text_romanized': 'Pongalo Pongal!'},
            {'page_number': 4, 'text_content': 'கரும்பும் வாழைப்பழமும்.', 'text_romanized': 'Karumbum vaazhaipazhamum.'},
            {'page_number': 5, 'text_content': 'அனைவருக்கும் பொங்கல் நல்வாழ்த்துக்கள்!', 'text_romanized': 'Anaivarukkum Pongal Nalvaazhthukal!'},
        ]
        story, created = self._create_story_with_pages(story_data, pages)
        self._link_to_festival(story, 'Pongal', is_primary=True)
        self.stdout.write(f'  {"Created" if created else "Updated"}: {story.title} (Festival)')

        # Festival Story: Diwali (Tamil)
        story_data = {
            'storyweaver_id': 'bm-ta-fest-diwali',
            'title': 'தீபாவளி ஒளி',
            'title_translit': 'Deepavali Oli',
            'language': 'TAMIL',
            'level': 1,
            'page_count': 5,
            'synopsis': 'Celebrating Diwali with lights and crackers.',
            'author': 'BhashaMitra Team',
            'categories': ['festival', 'diwali', 'lights'],
            'tier': 'FREE',
            'age_min': 3,
            'age_max': 7,
            'is_l1_content': True,
            'is_active': True,
        }
        pages = [
            {'page_number': 1, 'text_content': 'இன்று தீபாவளி!', 'text_romanized': 'Indru Deepavali!'},
            {'page_number': 2, 'text_content': 'வீட்டில் விளக்குகள் எரிகின்றன.', 'text_romanized': 'Veettil vilakkugal erikindrana.'},
            {'page_number': 3, 'text_content': 'புதிய ஆடைகள் அணிகிறோம்.', 'text_romanized': 'Pudhiya aadaigal anigirom.'},
            {'page_number': 4, 'text_content': 'இனிப்புகள் சாப்பிடுகிறோம்.', 'text_romanized': 'Inippugal saappidugirom.'},
            {'page_number': 5, 'text_content': 'தீபாவளி நல்வாழ்த்துக்கள்!', 'text_romanized': 'Deepavali Nalvaazhthukal!'},
        ]
        story, created = self._create_story_with_pages(story_data, pages)
        self._link_to_festival(story, 'Diwali', is_primary=False)
        self.stdout.write(f'  {"Created" if created else "Updated"}: {story.title} (Festival)')

        count = Story.objects.filter(language='TAMIL').count()
        self.stdout.write(f'  Total Tamil stories: {count}')

    @transaction.atomic
    def _seed_punjabi_stories(self):
        """Seed Punjabi stories including festival stories."""

        # Story 1: Peppi's New Friend
        story_data = {
            'storyweaver_id': 'bm-pa-001',
            'title': 'ਪੈੱਪੀ ਦਾ ਨਵਾਂ ਦੋਸਤ',
            'title_translit': 'Peppi Da Nava Dost',
            'language': 'PUNJABI',
            'level': 1,
            'page_count': 5,
            'synopsis': 'Peppi the parrot makes a new friend.',
            'author': 'BhashaMitra Team',
            'categories': ['friendship', 'animals', 'values'],
            'tier': 'FREE',
            'age_min': 3,
            'age_max': 6,
            'is_l1_content': True,
            'is_active': True,
        }
        pages = [
            {'page_number': 1, 'text_content': 'ਪੈੱਪੀ ਇੱਕ ਹਰਾ ਤੋਤਾ ਹੈ।', 'text_romanized': 'Peppi ikk hara tota hai.'},
            {'page_number': 2, 'text_content': 'ਉਹ ਬਗੀਚੇ ਵਿੱਚ ਰਹਿੰਦਾ ਹੈ।', 'text_romanized': 'Oh bagiche vich rehinda hai.'},
            {'page_number': 3, 'text_content': 'ਇੱਕ ਦਿਨ ਉਸਨੇ ਗਿਲਹਰੀ ਦੇਖੀ।', 'text_romanized': 'Ikk din usne gilhari dekhi.'},
            {'page_number': 4, 'text_content': '"ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ! ਮੈਂ ਪੈੱਪੀ ਹਾਂ।"', 'text_romanized': '"Sat Sri Akal! Main Peppi haan."'},
            {'page_number': 5, 'text_content': 'ਹੁਣ ਉਹ ਚੰਗੇ ਦੋਸਤ ਹਨ।', 'text_romanized': 'Hun oh change dost han.'},
        ]
        story, created = self._create_story_with_pages(story_data, pages)
        self.stdout.write(f'  {"Created" if created else "Updated"}: {story.title}')

        # Story 2: The Red Apple
        story_data = {
            'storyweaver_id': 'bm-pa-002',
            'title': 'ਲਾਲ ਸੇਬ',
            'title_translit': 'Laal Seb',
            'language': 'PUNJABI',
            'level': 1,
            'page_count': 4,
            'synopsis': 'A child finds a red apple and shares it.',
            'author': 'BhashaMitra Team',
            'categories': ['food', 'sharing', 'colors'],
            'tier': 'FREE',
            'age_min': 3,
            'age_max': 5,
            'is_l1_content': True,
            'is_active': True,
        }
        pages = [
            {'page_number': 1, 'text_content': 'ਦਰੱਖਤ ਤੇ ਇੱਕ ਸੇਬ ਹੈ।', 'text_romanized': 'Darakht te ikk seb hai.'},
            {'page_number': 2, 'text_content': 'ਸੇਬ ਲਾਲ ਹੈ।', 'text_romanized': 'Seb laal hai.'},
            {'page_number': 3, 'text_content': 'ਰਾਜ ਨੇ ਸੇਬ ਤੋੜਿਆ।', 'text_romanized': 'Raj ne seb todeya.'},
            {'page_number': 4, 'text_content': 'ਉਸਨੇ ਸਭ ਨਾਲ ਵੰਡਿਆ।', 'text_romanized': 'Usne sabh naal vandeya.'},
        ]
        story, created = self._create_story_with_pages(story_data, pages)
        self.stdout.write(f'  {"Created" if created else "Updated"}: {story.title}')

        # Story 3: My Family
        story_data = {
            'storyweaver_id': 'bm-pa-003',
            'title': 'ਮੇਰਾ ਪਰਿਵਾਰ',
            'title_translit': 'Mera Parivaar',
            'language': 'PUNJABI',
            'level': 1,
            'page_count': 6,
            'synopsis': 'A child introduces their loving family.',
            'author': 'BhashaMitra Team',
            'categories': ['family', 'relationships', 'love'],
            'tier': 'FREE',
            'age_min': 3,
            'age_max': 6,
            'is_l1_content': True,
            'is_active': True,
        }
        pages = [
            {'page_number': 1, 'text_content': 'ਇਹ ਮੇਰਾ ਘਰ ਹੈ।', 'text_romanized': 'Ih mera ghar hai.'},
            {'page_number': 2, 'text_content': 'ਇਹ ਮੇਰੇ ਪਾਪਾ ਹਨ।', 'text_romanized': 'Ih mere papa han.'},
            {'page_number': 3, 'text_content': 'ਇਹ ਮੇਰੀ ਮਾਂ ਹੈ।', 'text_romanized': 'Ih meri maa hai.'},
            {'page_number': 4, 'text_content': 'ਇਹ ਮੇਰੀ ਭੈਣ ਹੈ।', 'text_romanized': 'Ih meri bhain hai.'},
            {'page_number': 5, 'text_content': 'ਇਹ ਮੇਰਾ ਭਰਾ ਹੈ।', 'text_romanized': 'Ih mera bhra hai.'},
            {'page_number': 6, 'text_content': 'ਅਸੀਂ ਸਾਰੇ ਇਕੱਠੇ ਰਹਿੰਦੇ ਹਾਂ।', 'text_romanized': 'Aseen saare ikathe rehinde haan.'},
        ]
        story, created = self._create_story_with_pages(story_data, pages)
        self.stdout.write(f'  {"Created" if created else "Updated"}: {story.title}')

        # Story 4: The Thirsty Crow
        story_data = {
            'storyweaver_id': 'bm-pa-004',
            'title': 'ਪਿਆਸਾ ਕਾਂ',
            'title_translit': 'Pyaasa Kaan',
            'language': 'PUNJABI',
            'level': 2,
            'page_count': 6,
            'synopsis': 'A clever crow finds a way to drink water.',
            'author': 'BhashaMitra Team',
            'categories': ['classic', 'animals', 'problem-solving'],
            'tier': 'STANDARD',
            'age_min': 4,
            'age_max': 7,
            'is_l1_content': False,
            'is_active': True,
        }
        pages = [
            {'page_number': 1, 'text_content': 'ਇੱਕ ਕਾਂ ਬਹੁਤ ਪਿਆਸਾ ਸੀ।', 'text_romanized': 'Ikk kaan bahut pyaasa si.'},
            {'page_number': 2, 'text_content': 'ਉਸਨੇ ਇੱਕ ਘੜਾ ਦੇਖਿਆ।', 'text_romanized': 'Usne ikk ghada dekhya.'},
            {'page_number': 3, 'text_content': 'ਪਾਣੀ ਬਹੁਤ ਹੇਠਾਂ ਸੀ।', 'text_romanized': 'Paani bahut hethaan si.'},
            {'page_number': 4, 'text_content': 'ਕਾਂ ਨੇ ਸੋਚਿਆ।', 'text_romanized': 'Kaan ne sochya.'},
            {'page_number': 5, 'text_content': 'ਉਸਨੇ ਕੰਕਰ ਪਾਏ।', 'text_romanized': 'Usne kankar paaye.'},
            {'page_number': 6, 'text_content': 'ਪਾਣੀ ਉੱਪਰ ਆਇਆ!', 'text_romanized': 'Paani upper aaya!'},
        ]
        story, created = self._create_story_with_pages(story_data, pages)
        self.stdout.write(f'  {"Created" if created else "Updated"}: {story.title}')

        # Festival Story: Vaisakhi
        story_data = {
            'storyweaver_id': 'bm-pa-fest-vaisakhi',
            'title': 'ਵਿਸਾਖੀ ਦਾ ਤਿਉਹਾਰ',
            'title_translit': 'Vaisakhi Da Tiohar',
            'language': 'PUNJABI',
            'level': 1,
            'page_count': 5,
            'synopsis': 'Celebrating Vaisakhi with bhangra and joy.',
            'author': 'BhashaMitra Team',
            'categories': ['festival', 'vaisakhi', 'harvest'],
            'tier': 'FREE',
            'age_min': 3,
            'age_max': 7,
            'is_l1_content': True,
            'is_active': True,
        }
        pages = [
            {'page_number': 1, 'text_content': 'ਅੱਜ ਵਿਸਾਖੀ ਹੈ!', 'text_romanized': 'Ajj Vaisakhi hai!'},
            {'page_number': 2, 'text_content': 'ਕਣਕ ਦੀ ਵਾਢੀ ਹੋਈ।', 'text_romanized': 'Kanak di vaadhi hoi.'},
            {'page_number': 3, 'text_content': 'ਭੰਗੜਾ ਪਾਉਂਦੇ ਹਾਂ!', 'text_romanized': 'Bhangra paunde haan!'},
            {'page_number': 4, 'text_content': 'ਢੋਲ ਵੱਜਦਾ ਹੈ।', 'text_romanized': 'Dhol vajjda hai.'},
            {'page_number': 5, 'text_content': 'ਵਿਸਾਖੀ ਦੀਆਂ ਲੱਖ ਲੱਖ ਵਧਾਈਆਂ!', 'text_romanized': 'Vaisakhi diyan lakh lakh vadhaiyan!'},
        ]
        story, created = self._create_story_with_pages(story_data, pages)
        self._link_to_festival(story, 'Vaisakhi', is_primary=True)
        self.stdout.write(f'  {"Created" if created else "Updated"}: {story.title} (Festival)')

        # Festival Story: Diwali (Punjabi)
        story_data = {
            'storyweaver_id': 'bm-pa-fest-diwali',
            'title': 'ਦੀਵਾਲੀ ਦੀਆਂ ਲੋਆਂ',
            'title_translit': 'Diwali Diyan Loan',
            'language': 'PUNJABI',
            'level': 1,
            'page_count': 5,
            'synopsis': 'Celebrating Diwali with lights and family.',
            'author': 'BhashaMitra Team',
            'categories': ['festival', 'diwali', 'lights'],
            'tier': 'FREE',
            'age_min': 3,
            'age_max': 7,
            'is_l1_content': True,
            'is_active': True,
        }
        pages = [
            {'page_number': 1, 'text_content': 'ਅੱਜ ਦੀਵਾਲੀ ਹੈ!', 'text_romanized': 'Ajj Diwali hai!'},
            {'page_number': 2, 'text_content': 'ਦੀਵੇ ਜਗਾਉਂਦੇ ਹਾਂ।', 'text_romanized': 'Deeve jagaunde haan.'},
            {'page_number': 3, 'text_content': 'ਘਰ ਰੌਸ਼ਨੀ ਨਾਲ ਭਰਿਆ।', 'text_romanized': 'Ghar roshni naal bharya.'},
            {'page_number': 4, 'text_content': 'ਮਿਠਾਈ ਬਹੁਤ ਸੁਆਦ ਹੈ।', 'text_romanized': 'Mithai bahut suaad hai.'},
            {'page_number': 5, 'text_content': 'ਸਾਰਿਆਂ ਨੂੰ ਦੀਵਾਲੀ ਮੁਬਾਰਕ!', 'text_romanized': 'Saaryan nu Diwali Mubarak!'},
        ]
        story, created = self._create_story_with_pages(story_data, pages)
        self._link_to_festival(story, 'Diwali', is_primary=False)
        self.stdout.write(f'  {"Created" if created else "Updated"}: {story.title} (Festival)')

        count = Story.objects.filter(language='PUNJABI').count()
        self.stdout.write(f'  Total Punjabi stories: {count}')

    @transaction.atomic
    def _seed_gujarati_stories(self):
        """Seed Gujarati stories including festival stories."""

        # Story 1: Peppi's New Friend
        story_data = {
            'storyweaver_id': 'bm-gu-001',
            'title': 'પેપ્પીનો નવો મિત્ર',
            'title_translit': 'Peppino Navo Mitra',
            'language': 'GUJARATI',
            'level': 1,
            'page_count': 5,
            'synopsis': 'Peppi the parrot makes a new friend.',
            'author': 'BhashaMitra Team',
            'categories': ['friendship', 'animals', 'values'],
            'tier': 'FREE',
            'age_min': 3,
            'age_max': 6,
            'is_l1_content': True,
            'is_active': True,
        }
        pages = [
            {'page_number': 1, 'text_content': 'પેપ્પી એક લીલો પોપટ છે.', 'text_romanized': 'Peppi ek leelo popat chhe.'},
            {'page_number': 2, 'text_content': 'તે બગીચામાં રહે છે.', 'text_romanized': 'Te bagichama rahe chhe.'},
            {'page_number': 3, 'text_content': 'એક દિવસ તેણે ખિસકોલી જોઈ.', 'text_romanized': 'Ek divas tene khiskoli joi.'},
            {'page_number': 4, 'text_content': '"નમસ્તે! હું પેપ્પી છું."', 'text_romanized': '"Namaste! Hu Peppi chhu."'},
            {'page_number': 5, 'text_content': 'હવે તેઓ સારા મિત્રો છે.', 'text_romanized': 'Have teo sara mitro chhe.'},
        ]
        story, created = self._create_story_with_pages(story_data, pages)
        self.stdout.write(f'  {"Created" if created else "Updated"}: {story.title}')

        # Story 2: The Red Apple
        story_data = {
            'storyweaver_id': 'bm-gu-002',
            'title': 'લાલ સફરજન',
            'title_translit': 'Laal Safarjan',
            'language': 'GUJARATI',
            'level': 1,
            'page_count': 4,
            'synopsis': 'A child finds a red apple and shares it.',
            'author': 'BhashaMitra Team',
            'categories': ['food', 'sharing', 'colors'],
            'tier': 'FREE',
            'age_min': 3,
            'age_max': 5,
            'is_l1_content': True,
            'is_active': True,
        }
        pages = [
            {'page_number': 1, 'text_content': 'ઝાડ પર એક સફરજન છે.', 'text_romanized': 'Zaad par ek safarjan chhe.'},
            {'page_number': 2, 'text_content': 'સફરજન લાલ છે.', 'text_romanized': 'Safarjan laal chhe.'},
            {'page_number': 3, 'text_content': 'રાજે સફરજન તોડ્યું.', 'text_romanized': 'Raje safarjan todyu.'},
            {'page_number': 4, 'text_content': 'બધા સાથે વહેંચ્યું.', 'text_romanized': 'Badha sathe vahenchyu.'},
        ]
        story, created = self._create_story_with_pages(story_data, pages)
        self.stdout.write(f'  {"Created" if created else "Updated"}: {story.title}')

        # Story 3: My Family
        story_data = {
            'storyweaver_id': 'bm-gu-003',
            'title': 'મારો પરિવાર',
            'title_translit': 'Maro Parivar',
            'language': 'GUJARATI',
            'level': 1,
            'page_count': 6,
            'synopsis': 'A child introduces their loving family.',
            'author': 'BhashaMitra Team',
            'categories': ['family', 'relationships', 'love'],
            'tier': 'FREE',
            'age_min': 3,
            'age_max': 6,
            'is_l1_content': True,
            'is_active': True,
        }
        pages = [
            {'page_number': 1, 'text_content': 'આ મારું ઘર છે.', 'text_romanized': 'Aa maaru ghar chhe.'},
            {'page_number': 2, 'text_content': 'આ મારા પપ્પા છે.', 'text_romanized': 'Aa mara pappa chhe.'},
            {'page_number': 3, 'text_content': 'આ મારી મમ્મી છે.', 'text_romanized': 'Aa mari mummy chhe.'},
            {'page_number': 4, 'text_content': 'આ મારી બહેન છે.', 'text_romanized': 'Aa mari bahen chhe.'},
            {'page_number': 5, 'text_content': 'આ મારો ભાઈ છે.', 'text_romanized': 'Aa maro bhai chhe.'},
            {'page_number': 6, 'text_content': 'અમે સાથે રહીએ છીએ.', 'text_romanized': 'Ame sathe rahiye chhiye.'},
        ]
        story, created = self._create_story_with_pages(story_data, pages)
        self.stdout.write(f'  {"Created" if created else "Updated"}: {story.title}')

        # Festival Story: Navratri
        story_data = {
            'storyweaver_id': 'bm-gu-fest-navratri',
            'title': 'નવરાત્રીની રાત',
            'title_translit': 'Navratrini Raat',
            'language': 'GUJARATI',
            'level': 1,
            'page_count': 5,
            'synopsis': 'Celebrating Navratri with garba and dandiya.',
            'author': 'BhashaMitra Team',
            'categories': ['festival', 'navratri', 'dance'],
            'tier': 'FREE',
            'age_min': 3,
            'age_max': 7,
            'is_l1_content': True,
            'is_active': True,
        }
        pages = [
            {'page_number': 1, 'text_content': 'આજે નવરાત્રી છે!', 'text_romanized': 'Aaje Navratri chhe!'},
            {'page_number': 2, 'text_content': 'સુંદર ચણિયા ચોળી પહેર્યા.', 'text_romanized': 'Sundar chaniya choli paherya.'},
            {'page_number': 3, 'text_content': 'ગરબા રમીએ છીએ!', 'text_romanized': 'Garba ramiye chhiye!'},
            {'page_number': 4, 'text_content': 'દાંડિયા રાસ રમીએ!', 'text_romanized': 'Dandiya raas ramiye!'},
            {'page_number': 5, 'text_content': 'જય માતાજી!', 'text_romanized': 'Jai Mataji!'},
        ]
        story, created = self._create_story_with_pages(story_data, pages)
        self._link_to_festival(story, 'Navratri', is_primary=True)
        self.stdout.write(f'  {"Created" if created else "Updated"}: {story.title} (Festival)')

        # Festival Story: Diwali (Gujarati)
        story_data = {
            'storyweaver_id': 'bm-gu-fest-diwali',
            'title': 'દિવાળીની રોશની',
            'title_translit': 'Divalini Roshni',
            'language': 'GUJARATI',
            'level': 1,
            'page_count': 5,
            'synopsis': 'Celebrating Diwali with lights and sweets.',
            'author': 'BhashaMitra Team',
            'categories': ['festival', 'diwali', 'lights'],
            'tier': 'FREE',
            'age_min': 3,
            'age_max': 7,
            'is_l1_content': True,
            'is_active': True,
        }
        pages = [
            {'page_number': 1, 'text_content': 'આજે દિવાળી છે!', 'text_romanized': 'Aaje Divali chhe!'},
            {'page_number': 2, 'text_content': 'દીવા પ્રગટાવીએ.', 'text_romanized': 'Diva pragataviye.'},
            {'page_number': 3, 'text_content': 'ઘર રોશનીથી ભરાયું.', 'text_romanized': 'Ghar roshneethi bharayu.'},
            {'page_number': 4, 'text_content': 'મીઠાઈ ખાઈએ છીએ.', 'text_romanized': 'Mithai khaiye chhiye.'},
            {'page_number': 5, 'text_content': 'સૌને દિવાળીની શુભેચ્છા!', 'text_romanized': 'Saune Divalini Shubhechha!'},
        ]
        story, created = self._create_story_with_pages(story_data, pages)
        self._link_to_festival(story, 'Diwali', is_primary=False)
        self.stdout.write(f'  {"Created" if created else "Updated"}: {story.title} (Festival)')

        count = Story.objects.filter(language='GUJARATI').count()
        self.stdout.write(f'  Total Gujarati stories: {count}')
