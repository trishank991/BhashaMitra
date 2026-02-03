"""Seed free tier stories for ages 3-5."""
from django.core.management.base import BaseCommand
from apps.stories.models import Story, StoryPage, StoryVocabulary


class Command(BaseCommand):
    help = 'Seed free tier stories for ages 3-5 (Hindi)'

    def handle(self, *args, **options):
        self.stdout.write('Seeding free tier stories...')

        # Create stories
        self._create_chatur_lomdi()
        self._create_pyaasa_kauwa()
        self._create_sher_aur_chuha()
        self._create_ram_ji_ki_wapsi()

        # Summary
        stories = Story.objects.filter(tier='free', is_l1_content=True)
        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Seeded {stories.count()} free tier stories!'
        ))
        for story in stories:
            pages = story.pages.count()
            vocab = story.vocabulary.count()
            self.stdout.write(f'  • {story.title_hindi} ({story.title}) - {pages} pages, {vocab} words')

    def _create_chatur_lomdi(self):
        """Story 1: The Clever Fox"""
        story, created = Story.objects.update_or_create(
            storyweaver_id='free-chatur-lomdi',
            defaults={
                'slug': 'chatur-lomdi',
                'title': 'The Clever Fox',
                'title_hindi': 'चतुर लोमड़ी',
                'title_romanized': 'Chatur Lomdi',
                'language': 'HINDI',
                'level': 1,
                'page_count': 6,
                'cover_image_url': '',
                'synopsis': 'A story about a clever fox who uses her wisdom to escape trouble.',
                'tier': 'free',
                'age_min': 3,
                'age_max': 5,
                'theme': 'Problem-solving',
                'moral_hindi': 'सोच-समझकर काम करो।',
                'moral_english': 'Think before you act.',
                'xp_reward': 10,
                'estimated_minutes': 3,
                'sort_order': 1,
                'is_active': True,
                'is_featured': True,
                'is_l1_content': True,
            }
        )

        # Delete existing pages and vocabulary
        story.pages.all().delete()
        story.vocabulary.all().delete()

        # Pages
        pages_data = [
            {
                'page_number': 1,
                'text_content': 'A fox lived in a forest.',
                'text_hindi': 'एक जंगल में एक लोमड़ी रहती थी।',
                'text_romanized': 'Ek jungle mein ek lomdi rehti thi.',
                'image_description': 'A cute orange fox standing in a green forest with tall trees. Bright sunny day. Child-friendly cartoon style.',
                'highlight_words': ['जंगल', 'लोमड़ी'],
            },
            {
                'page_number': 2,
                'text_content': 'The fox was very clever.',
                'text_hindi': 'लोमड़ी बहुत चतुर थी।',
                'text_romanized': 'Lomdi bahut chatur thi.',
                'image_description': 'The cute fox with a thoughtful expression, one paw on chin, sparkles around head showing cleverness. Cartoon style.',
                'highlight_words': ['चतुर'],
            },
            {
                'page_number': 3,
                'text_content': 'One day the fox felt hungry.',
                'text_hindi': 'एक दिन लोमड़ी को भूख लगी।',
                'text_romanized': 'Ek din lomdi ko bhookh lagi.',
                'image_description': 'The fox holding her tummy looking hungry, with thought bubble showing food. Cute cartoon style.',
                'highlight_words': ['भूख'],
            },
            {
                'page_number': 4,
                'text_content': 'She saw grapes on a tree.',
                'text_hindi': 'उसने एक पेड़ पर अंगूर देखे।',
                'text_romanized': 'Usne ek ped par angoor dekhe.',
                'image_description': 'Fox looking up at a grapevine with purple grapes hanging high. The fox looks excited. Bright colors.',
                'highlight_words': ['पेड़', 'अंगूर'],
            },
            {
                'page_number': 5,
                'text_content': 'The fox jumped and picked the grapes.',
                'text_hindi': 'लोमड़ी ने कूद कर अंगूर तोड़े।',
                'text_romanized': 'Lomdi ne kood kar angoor tode.',
                'image_description': 'Fox jumping happily, reaching for grapes. Dynamic pose showing movement. Cheerful scene.',
                'highlight_words': ['कूद'],
            },
            {
                'page_number': 6,
                'text_content': 'The fox was happy! Think before you act.',
                'text_hindi': 'लोमड़ी खुश हो गई! सोच-समझकर काम करो।',
                'text_romanized': 'Lomdi khush ho gayi! Soch-samajhkar kaam karo.',
                'image_description': 'Happy fox eating grapes with a big smile. Hearts and stars around. Moral text shown beautifully.',
                'highlight_words': ['खुश'],
            },
        ]

        for page_data in pages_data:
            StoryPage.objects.create(story=story, **page_data)

        # Vocabulary
        vocab_data = [
            {'word_hindi': 'जंगल', 'word_transliteration': 'jungle', 'word_english': 'forest'},
            {'word_hindi': 'लोमड़ी', 'word_transliteration': 'lomdi', 'word_english': 'fox'},
            {'word_hindi': 'चतुर', 'word_transliteration': 'chatur', 'word_english': 'clever'},
            {'word_hindi': 'भूख', 'word_transliteration': 'bhookh', 'word_english': 'hunger'},
            {'word_hindi': 'पेड़', 'word_transliteration': 'ped', 'word_english': 'tree'},
            {'word_hindi': 'अंगूर', 'word_transliteration': 'angoor', 'word_english': 'grapes'},
            {'word_hindi': 'कूद', 'word_transliteration': 'kood', 'word_english': 'jump'},
            {'word_hindi': 'खुश', 'word_transliteration': 'khush', 'word_english': 'happy'},
        ]

        for vocab in vocab_data:
            StoryVocabulary.objects.create(story=story, **vocab)

        action = 'Created' if created else 'Updated'
        self.stdout.write(f'  ✓ {action}: {story.title_hindi}')

    def _create_pyaasa_kauwa(self):
        """Story 2: The Thirsty Crow"""
        story, created = Story.objects.update_or_create(
            storyweaver_id='free-pyaasa-kauwa',
            defaults={
                'slug': 'pyaasa-kauwa',
                'title': 'The Thirsty Crow',
                'title_hindi': 'प्यासा कौआ',
                'title_romanized': 'Pyaasa Kauwa',
                'language': 'HINDI',
                'level': 1,
                'page_count': 6,
                'cover_image_url': '',
                'synopsis': 'A story about a thirsty crow who never gives up.',
                'tier': 'free',
                'age_min': 3,
                'age_max': 5,
                'theme': 'Perseverance',
                'moral_hindi': 'कोशिश करते रहो, हार मत मानो।',
                'moral_english': 'Keep trying, never give up.',
                'xp_reward': 10,
                'estimated_minutes': 3,
                'sort_order': 2,
                'is_active': True,
                'is_featured': False,
                'is_l1_content': True,
            }
        )

        story.pages.all().delete()
        story.vocabulary.all().delete()

        pages_data = [
            {
                'page_number': 1,
                'text_content': 'It was a hot day. A crow was very thirsty.',
                'text_hindi': 'गर्मी का दिन था। एक कौआ बहुत प्यासा था।',
                'text_romanized': 'Garmi ka din tha. Ek kauwa bahut pyaasa tha.',
                'image_description': 'A black crow flying under bright yellow sun. The crow looks tired and thirsty. Hot summer day with dry land below.',
                'highlight_words': ['गर्मी', 'कौआ', 'प्यासा'],
            },
            {
                'page_number': 2,
                'text_content': 'The crow saw a pot.',
                'text_hindi': 'कौए ने एक घड़ा देखा।',
                'text_romanized': 'Kauwe ne ek ghada dekha.',
                'image_description': 'Crow landing near a clay pot (ghada/matka). The crow looks hopeful. Traditional Indian clay pot.',
                'highlight_words': ['घड़ा'],
            },
            {
                'page_number': 3,
                'text_content': 'There was little water in the pot. The crow could not drink.',
                'text_hindi': 'घड़े में थोड़ा पानी था। कौआ पी नहीं सकता था।',
                'text_romanized': 'Ghade mein thoda paani tha. Kauwa pee nahi sakta tha.',
                'image_description': 'Crow looking into pot, water level very low at bottom. Crow looks sad and worried.',
                'highlight_words': ['पानी'],
            },
            {
                'page_number': 4,
                'text_content': 'The crow thought. He found a solution!',
                'text_hindi': 'कौए ने सोचा। उसे एक उपाय मिला!',
                'text_romanized': 'Kauwe ne socha. Use ek upaay mila!',
                'image_description': 'Crow with lightbulb moment, looking at small pebbles on ground. Excited expression. Idea sparkles.',
                'highlight_words': ['सोचा', 'उपाय'],
            },
            {
                'page_number': 5,
                'text_content': 'The crow put pebbles in the pot. The water came up!',
                'text_hindi': 'कौए ने घड़े में कंकड़ डाले। पानी ऊपर आ गया!',
                'text_romanized': 'Kauwe ne ghade mein kankad daale. Paani upar aa gaya!',
                'image_description': 'Crow dropping pebbles into pot, water rising. Multiple pebbles shown. Crow working hard.',
                'highlight_words': ['कंकड़', 'ऊपर'],
            },
            {
                'page_number': 6,
                'text_content': 'The crow drank water. Keep trying!',
                'text_hindi': 'कौए ने पानी पिया। कोशिश करते रहो!',
                'text_romanized': 'Kauwe ne paani piya. Koshish karte raho!',
                'image_description': 'Happy crow drinking water from pot. Water level high. Celebration stars around crow.',
                'highlight_words': ['पिया', 'कोशिश'],
            },
        ]

        for page_data in pages_data:
            StoryPage.objects.create(story=story, **page_data)

        vocab_data = [
            {'word_hindi': 'गर्मी', 'word_transliteration': 'garmi', 'word_english': 'summer/hot'},
            {'word_hindi': 'कौआ', 'word_transliteration': 'kauwa', 'word_english': 'crow'},
            {'word_hindi': 'प्यासा', 'word_transliteration': 'pyaasa', 'word_english': 'thirsty'},
            {'word_hindi': 'घड़ा', 'word_transliteration': 'ghada', 'word_english': 'pot'},
            {'word_hindi': 'पानी', 'word_transliteration': 'paani', 'word_english': 'water'},
            {'word_hindi': 'कंकड़', 'word_transliteration': 'kankad', 'word_english': 'pebbles'},
            {'word_hindi': 'उपाय', 'word_transliteration': 'upaay', 'word_english': 'solution'},
            {'word_hindi': 'कोशिश', 'word_transliteration': 'koshish', 'word_english': 'try/effort'},
        ]

        for vocab in vocab_data:
            StoryVocabulary.objects.create(story=story, **vocab)

        action = 'Created' if created else 'Updated'
        self.stdout.write(f'  ✓ {action}: {story.title_hindi}')

    def _create_sher_aur_chuha(self):
        """Story 3: The Lion and the Mouse"""
        story, created = Story.objects.update_or_create(
            storyweaver_id='free-sher-aur-chuha',
            defaults={
                'slug': 'sher-aur-chuha',
                'title': 'The Lion and the Mouse',
                'title_hindi': 'शेर और चूहा',
                'title_romanized': 'Sher Aur Chuha',
                'language': 'HINDI',
                'level': 1,
                'page_count': 6,
                'cover_image_url': '',
                'synopsis': 'A story about friendship between a lion and a mouse.',
                'tier': 'free',
                'age_min': 3,
                'age_max': 5,
                'theme': 'Kindness',
                'moral_hindi': 'छोटे दोस्त भी बड़े काम कर सकते हैं।',
                'moral_english': 'Small friends can do big things.',
                'xp_reward': 10,
                'estimated_minutes': 3,
                'sort_order': 3,
                'is_active': True,
                'is_featured': False,
                'is_l1_content': True,
            }
        )

        story.pages.all().delete()
        story.vocabulary.all().delete()

        pages_data = [
            {
                'page_number': 1,
                'text_content': 'A big lion was sleeping in the forest.',
                'text_hindi': 'जंगल में एक बड़ा शेर सो रहा था।',
                'text_romanized': 'Jungle mein ek bada sher so raha tha.',
                'image_description': 'A big friendly lion sleeping peacefully under a tree. Cute cartoon style. Green forest background.',
                'highlight_words': ['शेर', 'सो रहा'],
            },
            {
                'page_number': 2,
                'text_content': 'A small mouse climbed on the lion.',
                'text_hindi': 'एक छोटा चूहा शेर पर चढ़ गया।',
                'text_romanized': 'Ek chhota chuha sher par chadh gaya.',
                'image_description': 'Tiny cute mouse climbing on sleeping lions paw. Mouse looks curious. Size contrast shown.',
                'highlight_words': ['छोटा', 'चूहा'],
            },
            {
                'page_number': 3,
                'text_content': 'The lion woke up! The mouse was scared.',
                'text_hindi': 'शेर जाग गया! चूहा डर गया।',
                'text_romanized': 'Sher jaag gaya! Chuha dar gaya.',
                'image_description': 'Lion awake with surprised expression, mouse trembling with fear. Comic style with motion lines.',
                'highlight_words': ['जाग', 'डर'],
            },
            {
                'page_number': 4,
                'text_content': 'The mouse said - "Let me go. I will help you."',
                'text_hindi': 'चूहे ने कहा - "मुझे छोड़ दो। मैं तुम्हारी मदद करूँगा।"',
                'text_romanized': 'Chuhe ne kaha - "Mujhe chhod do. Main tumhari madad karunga."',
                'image_description': 'Mouse with pleading expression talking to lion. Speech bubble showing promise. Lion looking thoughtful.',
                'highlight_words': ['छोड़ दो', 'मदद'],
            },
            {
                'page_number': 5,
                'text_content': 'One day the lion got trapped in a net. The mouse cut the net!',
                'text_hindi': 'एक दिन शेर जाल में फँस गया। चूहे ने जाल काट दिया!',
                'text_romanized': 'Ek din sher jaal mein phas gaya. Chuhe ne jaal kaat diya!',
                'image_description': 'Lion trapped in rope net looking worried. Mouse biting through ropes to free lion. Heroic scene.',
                'highlight_words': ['जाल', 'काट'],
            },
            {
                'page_number': 6,
                'text_content': 'The lion and mouse became friends. Small friends can help too!',
                'text_hindi': 'शेर और चूहा दोस्त बन गए। छोटे दोस्त भी मदद कर सकते हैं!',
                'text_romanized': 'Sher aur chuha dost ban gaye. Chhote dost bhi madad kar sakte hain!',
                'image_description': 'Lion and mouse as friends, mouse sitting on lions head. Both smiling. Hearts and friendship symbols.',
                'highlight_words': ['दोस्त'],
            },
        ]

        for page_data in pages_data:
            StoryPage.objects.create(story=story, **page_data)

        vocab_data = [
            {'word_hindi': 'शेर', 'word_transliteration': 'sher', 'word_english': 'lion'},
            {'word_hindi': 'चूहा', 'word_transliteration': 'chuha', 'word_english': 'mouse'},
            {'word_hindi': 'बड़ा', 'word_transliteration': 'bada', 'word_english': 'big'},
            {'word_hindi': 'छोटा', 'word_transliteration': 'chhota', 'word_english': 'small'},
            {'word_hindi': 'दोस्त', 'word_transliteration': 'dost', 'word_english': 'friend'},
            {'word_hindi': 'मदद', 'word_transliteration': 'madad', 'word_english': 'help'},
            {'word_hindi': 'जाल', 'word_transliteration': 'jaal', 'word_english': 'net/trap'},
            {'word_hindi': 'डर', 'word_transliteration': 'dar', 'word_english': 'fear/scared'},
        ]

        for vocab in vocab_data:
            StoryVocabulary.objects.create(story=story, **vocab)

        action = 'Created' if created else 'Updated'
        self.stdout.write(f'  ✓ {action}: {story.title_hindi}')

    def _create_ram_ji_ki_wapsi(self):
        """Story 4: Lord Ram's Return (Diwali Story)"""
        story, created = Story.objects.update_or_create(
            storyweaver_id='free-ram-ji-ki-wapsi',
            defaults={
                'slug': 'ram-ji-ki-wapsi',
                'title': "Lord Ram's Return",
                'title_hindi': 'राम जी की वापसी',
                'title_romanized': 'Ram Ji Ki Wapsi',
                'language': 'HINDI',
                'level': 1,
                'page_count': 6,
                'cover_image_url': '',
                'synopsis': 'The story of Diwali - Lord Ram returned to Ayodhya.',
                'tier': 'free',
                'age_min': 3,
                'age_max': 5,
                'theme': 'Diwali/Festival',
                'moral_hindi': 'अच्छाई की हमेशा जीत होती है।',
                'moral_english': 'Good always wins over evil.',
                'xp_reward': 15,
                'estimated_minutes': 4,
                'sort_order': 4,
                'is_active': True,
                'is_featured': True,
                'is_l1_content': True,
            }
        )

        story.pages.all().delete()
        story.vocabulary.all().delete()

        pages_data = [
            {
                'page_number': 1,
                'text_content': 'Lord Ram was a very good prince.',
                'text_hindi': 'राम जी बहुत अच्छे राजकुमार थे।',
                'text_romanized': 'Ram ji bahut achhe rajkumar the.',
                'image_description': 'Young Lord Ram in royal Indian clothes, bow and arrow, kind smile. Golden palace in background. Divine glow.',
                'highlight_words': ['राम जी', 'राजकुमार'],
            },
            {
                'page_number': 2,
                'text_content': 'Ram, Sita and Lakshman went to the forest.',
                'text_hindi': 'राम जी, सीता जी और लक्ष्मण जंगल गए।',
                'text_romanized': 'Ram ji, Sita ji aur Lakshman jungle gaye.',
                'image_description': 'Ram, Sita and Lakshman walking into forest together. Simple hut visible. Green forest. Peaceful scene.',
                'highlight_words': ['सीता जी', 'लक्ष्मण', 'जंगल'],
            },
            {
                'page_number': 3,
                'text_content': 'The evil demon Ravan took Sita away.',
                'text_hindi': 'बुरा राक्षस रावण ने सीता जी को ले गया।',
                'text_romanized': 'Bura rakshas Ravan ne Sita ji ko le gaya.',
                'image_description': 'Simplified depiction of Ravan (not scary, cartoon style) taking Sita in flying chariot. Sita looks worried.',
                'highlight_words': ['राक्षस', 'रावण'],
            },
            {
                'page_number': 4,
                'text_content': 'Lord Ram defeated Ravan. Sita came back!',
                'text_hindi': 'राम जी ने रावण को हराया। सीता जी वापस आ गईं!',
                'text_romanized': 'Ram ji ne Ravan ko haraya. Sita ji wapas aa gayin!',
                'image_description': 'Ram victoriously with Sita by his side. Celebration scene. Not violent - focus on happy reunion.',
                'highlight_words': ['हराया', 'वापस'],
            },
            {
                'page_number': 5,
                'text_content': 'Lord Ram returned to Ayodhya. Everyone was happy!',
                'text_hindi': 'राम जी अयोध्या वापस आए। सब लोग खुश थे!',
                'text_romanized': 'Ram ji Ayodhya wapas aaye. Sab log khush the!',
                'image_description': 'Ram, Sita, Lakshman approaching golden city of Ayodhya. Citizens celebrating, waving. Festive atmosphere.',
                'highlight_words': ['अयोध्या', 'खुश'],
            },
            {
                'page_number': 6,
                'text_content': 'People lit lamps. This is Diwali! Good wins over evil.',
                'text_hindi': 'लोगों ने दीये जलाए। यह है दीपावली! अच्छाई की जीत।',
                'text_romanized': 'Logon ne diye jalaye. Yeh hai Deepawali! Acchai ki jeet.',
                'image_description': 'Beautiful Diwali scene with hundreds of diyas (oil lamps) lighting up Ayodhya. Fireworks. Rangoli. Family celebration.',
                'highlight_words': ['दीये', 'दीपावली', 'अच्छाई', 'जीत'],
            },
        ]

        for page_data in pages_data:
            StoryPage.objects.create(story=story, **page_data)

        vocab_data = [
            {'word_hindi': 'राम जी', 'word_transliteration': 'Ram ji', 'word_english': 'Lord Ram'},
            {'word_hindi': 'राजकुमार', 'word_transliteration': 'rajkumar', 'word_english': 'prince'},
            {'word_hindi': 'सीता जी', 'word_transliteration': 'Sita ji', 'word_english': 'Lady Sita'},
            {'word_hindi': 'लक्ष्मण', 'word_transliteration': 'Lakshman', 'word_english': 'Lakshman'},
            {'word_hindi': 'अयोध्या', 'word_transliteration': 'Ayodhya', 'word_english': 'Ayodhya (city)'},
            {'word_hindi': 'दीये', 'word_transliteration': 'diye', 'word_english': 'oil lamps'},
            {'word_hindi': 'दीपावली', 'word_transliteration': 'Deepawali', 'word_english': 'Diwali'},
            {'word_hindi': 'अच्छाई', 'word_transliteration': 'acchai', 'word_english': 'goodness'},
            {'word_hindi': 'जीत', 'word_transliteration': 'jeet', 'word_english': 'victory'},
        ]

        for vocab in vocab_data:
            StoryVocabulary.objects.create(story=story, **vocab)

        action = 'Created' if created else 'Updated'
        self.stdout.write(f'  ✓ {action}: {story.title_hindi}')
