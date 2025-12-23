"""Seed L1 curriculum content - songs, stories, and vocabulary."""
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.curriculum.models import (
    CurriculumLevel,
    VocabularyTheme,
    VocabularyWord,
    Song,
    PeppiPersonality,
)
from apps.stories.models import Story, StoryPage
from apps.children.models import Child


class Command(BaseCommand):
    help = 'Seed L1 (Ankur) curriculum content - songs, stories, vocabulary'

    def handle(self, *args, **options):
        self.stdout.write('Seeding L1 curriculum content...\n')

        # Get L1 level
        try:
            l1_level = CurriculumLevel.objects.get(code='L1')
        except CurriculumLevel.DoesNotExist:
            self.stdout.write(self.style.ERROR('L1 level not found. Run seed_curriculum_levels first.'))
            return

        with transaction.atomic():
            # Seed Peppi personalities
            peppi_count = self.seed_peppi_personalities()

            # Seed songs
            songs_count = self.seed_songs(l1_level)

            # Seed stories
            stories_count = self.seed_stories()

            # Seed additional vocabulary
            vocab_count = self.seed_vocabulary()

        self.stdout.write(
            self.style.SUCCESS(
                f'\nL1 Content Seeded Successfully!\n'
                f'- Peppi Personalities: {peppi_count}\n'
                f'- Songs: {songs_count}\n'
                f'- Stories: {stories_count}\n'
                f'- Vocabulary Words Added: {vocab_count}\n'
            )
        )

    def seed_peppi_personalities(self):
        """Seed Peppi personality profiles."""
        personalities = [
            {
                'age_group': '4-5',
                'greeting_style': 'Warm, playful, and simple',
                'encouragement_phrases': [
                    'Shabash! (Well done!)',
                    'Bahut Accha! (Very good!)',
                    'Waah! (Wow!)',
                    'Kya baat hai! (How wonderful!)',
                ],
                'teaching_style': 'Uses simple words, lots of repetition, songs and games',
                'voice_tone': 'Cheerful and gentle',
                'avatar_expression': 'happy',
            },
            {
                'age_group': '6-8',
                'greeting_style': 'Friendly, encouraging, and clear',
                'encouragement_phrases': [
                    'Badhiya! (Excellent!)',
                    'Behtareen! (Fantastic!)',
                    'Zabardast! (Awesome!)',
                    'Bahut khoob! (Well done!)',
                ],
                'teaching_style': 'Builds on basics, introduces simple grammar, uses stories',
                'voice_tone': 'Energetic and supportive',
                'avatar_expression': 'excited',
            },
            {
                'age_group': '9-11',
                'greeting_style': 'Supportive, knowledgeable, and motivating',
                'encouragement_phrases': [
                    'Uttam! (Outstanding!)',
                    'Kamaal! (Amazing!)',
                    'Bahut khoob! (Well done!)',
                    'Lajawaab! (Incomparable!)',
                ],
                'teaching_style': 'Grammar focus, cultural context, conversational practice',
                'voice_tone': 'Confident and inspiring',
                'avatar_expression': 'proud',
            },
            {
                'age_group': '12-14',
                'greeting_style': 'Respectful, mature, and collaborative',
                'encouragement_phrases': [
                    'Shaan dar! (Splendid!)',
                    'Khoobsurat! (Beautiful!)',
                    'Behtareen koshish! (Excellent effort!)',
                    'Tumhara Hindi bohot sudhar raha hai! (Your Hindi is improving!)',
                ],
                'teaching_style': 'Advanced grammar, literature, cultural deep-dives, debates',
                'voice_tone': 'Thoughtful and encouraging',
                'avatar_expression': 'thoughtful',
            },
        ]

        count = 0
        for personality_data in personalities:
            personality, created = PeppiPersonality.objects.update_or_create(
                age_group=personality_data['age_group'],
                defaults=personality_data
            )
            if created:
                count += 1
                self.stdout.write(f'  Created Peppi personality: {personality.age_group}')
            else:
                self.stdout.write(f'  Updated Peppi personality: {personality.age_group}')

        return count

    def seed_songs(self, level):
        """Seed traditional Hindi songs."""
        songs_data = [
            {
                'title_english': 'Fish is Queen of Water',
                'title_hindi': 'मछली जल की रानी है',
                'title_romanized': 'Machli Jal Ki Rani Hai',
                'lyrics_hindi': '''मछली जल की रानी है
जीवन उसका पानी है
हाथ लगाओ डर जायेगी
बाहर निकालो मर जायेगी''',
                'lyrics_romanized': '''Machli jal ki rani hai
Jeevan uska paani hai
Haath lagao dar jayegi
Bahar nikalo mar jayegi''',
                'lyrics_english': '''Fish is the queen of water
Water is her life
Touch her and she'll get scared
Take her out and she'll die''',
                'age_min': 4,
                'age_max': 6,
                'duration_seconds': 45,
                'category': 'RHYME',
                'actions': [
                    'Make swimming motions with hands',
                    'Wiggle fingers like a fish',
                    'Show scared expression when saying "dar jayegi"',
                    'Pretend to gasp when saying "mar jayegi"',
                ],
                'order': 1,
            },
            {
                'title_english': 'Wooden Horse',
                'title_hindi': 'लकड़ी की काठी',
                'title_romanized': 'Lakdi Ki Kathi',
                'lyrics_hindi': '''लकड़ी की काठी, काठी पे घोड़ा
घोड़े की दुम पर जो मारा हथोड़ा
दौड़ा दौड़ा दौड़ा घोड़ा
दुम उठा के दौड़ा''',
                'lyrics_romanized': '''Lakdi ki kathi, kathi pe ghoda
Ghode ki dum par jo maara hathoda
Dauda dauda dauda ghoda
Dum utha ke dauda''',
                'lyrics_english': '''Wooden saddle, horse on the saddle
Someone hit the horse's tail with a hammer
The horse ran and ran and ran
Ran with its tail up''',
                'age_min': 4,
                'age_max': 6,
                'duration_seconds': 50,
                'category': 'RHYME',
                'actions': [
                    'Pretend to ride a horse',
                    'Gallop in place',
                    'Tap hand like a hammer',
                    'Run in circles',
                ],
                'order': 2,
            },
            {
                'title_english': "Grandma's Peacock",
                'title_hindi': 'नानी तेरी मोरनी',
                'title_romanized': 'Nani Teri Morni',
                'lyrics_hindi': '''नानी तेरी मोरनी को मोर ले गए
बड़े दुःख की बात है रो रो मर गए
दो नानी दो, नानी तेरी जय हो
तू तो प्यारी प्यारी है, मेरी नानी अच्छी है''',
                'lyrics_romanized': '''Nani teri morni ko mor le gaye
Bade dukh ki baat hai ro ro mar gaye
Do nani do, nani teri jai ho
Tu to pyaari pyaari hai, meri nani acchi hai''',
                'lyrics_english': '''Grandma, the peacock took your peahen
Such a sad thing, they cried and cried
Give us grandma, victory to grandma
You are so lovely, my grandma is the best''',
                'age_min': 4,
                'age_max': 6,
                'duration_seconds': 55,
                'category': 'RHYME',
                'actions': [
                    'Spread arms like peacock feathers',
                    'Make sad face and pretend to cry',
                    'Clap hands',
                    'Hug yourself',
                ],
                'order': 3,
            },
            {
                'title_english': 'Uncle Moon Far Away',
                'title_hindi': 'चंदा मामा दूर के',
                'title_romanized': 'Chanda Mama Door Ke',
                'lyrics_hindi': '''चंदा मामा दूर के
पुए पकाएँ बूर के
आप खाएँ थाली में
मुन्ने को दें प्याली में
प्याली गई टूट
मुन्ना गया रूठ''',
                'lyrics_romanized': '''Chanda mama door ke
Pue pakayen boor ke
Aap khayen thali mein
Munne ko dein pyali mein
Pyali gayi toot
Munna gaya rooth''',
                'lyrics_english': '''Uncle moon from far away
Makes sweets from sugar candy
You eat from a plate
Give Munna a small cup
The cup broke
Munna got upset''',
                'age_min': 4,
                'age_max': 6,
                'duration_seconds': 48,
                'category': 'RHYME',
                'actions': [
                    'Point up to the moon',
                    'Pretend to cook',
                    'Pretend to eat from a plate',
                    'Show broken cup gesture',
                    'Make sad face',
                ],
                'order': 4,
            },
            {
                'title_english': 'Potato Song',
                'title_hindi': 'आलू कचालू',
                'title_romanized': 'Aloo Kachaloo',
                'lyrics_hindi': '''आलू कचालू बेटा कहाँ गए थे
बैंगन की टोकरी में सो रहे थे
बैंगन ने लात मारी रो रहे थे
अम्मा ने प्यार किया हँस रहे थे''',
                'lyrics_romanized': '''Aloo kachaloo beta kahan gaye the
Baingan ki tokri mein so rahe the
Baingan ne laat maari ro rahe the
Amma ne pyaar kiya hans rahe the''',
                'lyrics_english': '''Little potato, where did you go?
Sleeping in the eggplant basket
Eggplant kicked him, he was crying
Mother loved him, he was laughing''',
                'age_min': 4,
                'age_max': 6,
                'duration_seconds': 42,
                'category': 'RHYME',
                'actions': [
                    'Walk in place looking around',
                    'Pretend to sleep',
                    'Gentle kick motion',
                    'Rub eyes like crying',
                    'Big smile and laugh',
                ],
                'order': 5,
            },
        ]

        count = 0
        for song_data in songs_data:
            song_data['level'] = level
            song, created = Song.objects.update_or_create(
                title_english=song_data['title_english'],
                level=level,
                defaults=song_data
            )
            if created:
                count += 1
                self.stdout.write(f'  Created song: {song.title_english}')
            else:
                self.stdout.write(f'  Updated song: {song.title_english}')

        return count

    def seed_stories(self):
        """Seed age-appropriate stories for L1."""
        stories_data = [
            {
                'title': "Peppi's New Home",
                'title_hindi': 'पेप्पी का नया घर',
                'title_romanized': 'Peppi Ka Naya Ghar',
                'level': 1,
                'theme': 'settling in new country',
                'pages': [
                    {
                        'text': 'Peppi was moving to a new home in a new country.',
                        'text_hindi': 'पेप्पी एक नए देश में एक नए घर में जा रही थी।',
                        'text_romanized': 'Peppi ek naye desh mein ek naye ghar mein ja rahi thi.',
                    },
                    {
                        'text': 'She felt nervous but also excited.',
                        'text_hindi': 'वह घबराई हुई थी लेकिन उत्साहित भी थी।',
                        'text_romanized': 'Vah ghabrayi hui thi lekin utsaahit bhi thi.',
                    },
                    {
                        'text': 'Her new house had a big red door.',
                        'text_hindi': 'उसके नए घर में एक बड़ा लाल दरवाज़ा था।',
                        'text_romanized': 'Uske naye ghar mein ek bada laal darwaza tha.',
                    },
                    {
                        'text': 'Peppi made new friends and learned to say Namaste.',
                        'text_hindi': 'पेप्पी ने नए दोस्त बनाए और नमस्ते कहना सीखा।',
                        'text_romanized': 'Peppi ne naye dost banaye aur namaste kehna seekha.',
                    },
                ],
            },
            {
                'title': 'Peppi and Colors',
                'title_hindi': 'पेप्पी और रंग',
                'title_romanized': 'Peppi Aur Rang',
                'level': 1,
                'theme': 'learning colors',
                'pages': [
                    {
                        'text': 'Peppi loved colors! Red was laal.',
                        'text_hindi': 'पेप्पी को रंग बहुत पसंद थे! लाल था laal।',
                        'text_romanized': 'Peppi ko rang bahut pasand the! Laal tha laal.',
                    },
                    {
                        'text': 'She saw a blue neela sky.',
                        'text_hindi': 'उसने एक नीला आसमान देखा।',
                        'text_romanized': 'Usne ek neela aasman dekha.',
                    },
                    {
                        'text': 'Green hara grass tickled her toes.',
                        'text_hindi': 'हरी घास ने उसके पैर की उंगलियों को गुदगुदाया।',
                        'text_romanized': 'Hari ghaas ne uske pair ki ungliyon ko gudgudaya.',
                    },
                    {
                        'text': 'Yellow peela flowers made her smile.',
                        'text_hindi': 'पीले फूलों ने उसे मुस्कुराया।',
                        'text_romanized': 'Peele phoolon ne use muskuraya.',
                    },
                ],
            },
            {
                'title': 'My Dear Mother',
                'title_hindi': 'मेरी प्यारी माँ',
                'title_romanized': 'Meri Pyaari Maa',
                'level': 1,
                'theme': 'family love',
                'pages': [
                    {
                        'text': 'My mother is my best friend.',
                        'text_hindi': 'मेरी माँ मेरी सबसे अच्छी दोस्त हैं।',
                        'text_romanized': 'Meri maa meri sabse acchi dost hain.',
                    },
                    {
                        'text': 'She makes yummy food for me.',
                        'text_hindi': 'वह मेरे लिए स्वादिष्ट खाना बनाती हैं।',
                        'text_romanized': 'Vah mere liye swaadisht khaana banati hain.',
                    },
                    {
                        'text': 'She tells me stories at bedtime.',
                        'text_hindi': 'वह सोने से पहले मुझे कहानियाँ सुनाती हैं।',
                        'text_romanized': 'Vah sone se pehle mujhe kahaaniyan sunati hain.',
                    },
                    {
                        'text': 'I love my maa very much!',
                        'text_hindi': 'मैं अपनी माँ से बहुत प्यार करता हूँ!',
                        'text_romanized': 'Main apni maa se bahut pyaar karta hoon!',
                    },
                ],
            },
            {
                'title': 'Fun in the Jungle',
                'title_hindi': 'जंगल में मंगल',
                'title_romanized': 'Jungle Mein Mangal',
                'level': 1,
                'theme': 'animals',
                'pages': [
                    {
                        'text': 'The sher (lion) was sleeping.',
                        'text_hindi': 'शेर सो रहा था।',
                        'text_romanized': 'Sher so raha tha.',
                    },
                    {
                        'text': 'The bandar (monkey) was jumping.',
                        'text_hindi': 'बंदर कूद रहा था।',
                        'text_romanized': 'Bandar kood raha tha.',
                    },
                    {
                        'text': 'The hathi (elephant) was bathing.',
                        'text_hindi': 'हाथी नहा रहा था।',
                        'text_romanized': 'Haathi naha raha tha.',
                    },
                    {
                        'text': 'All animals are friends in the jungle!',
                        'text_hindi': 'जंगल में सभी जानवर दोस्त हैं!',
                        'text_romanized': 'Jungle mein sabhi jaanwar dost hain!',
                    },
                ],
            },
            {
                'title': 'A Little Elephant',
                'title_hindi': 'एक छोटा सा हाथी',
                'title_romanized': 'Ek Chota Sa Hathi',
                'level': 1,
                'theme': 'size concepts',
                'pages': [
                    {
                        'text': 'There was a chota (small) elephant.',
                        'text_hindi': 'एक छोटा हाथी था।',
                        'text_romanized': 'Ek chota haathi tha.',
                    },
                    {
                        'text': 'He wanted to be bada (big) like his papa.',
                        'text_hindi': 'वह अपने पापा की तरह बड़ा होना चाहता था।',
                        'text_romanized': 'Vah apne papa ki tarah bada hona chahta tha.',
                    },
                    {
                        'text': 'He ate lots of food and grew taller.',
                        'text_hindi': 'उसने बहुत सारा खाना खाया और लंबा हो गया।',
                        'text_romanized': 'Usne bahut saara khaana khaya aur lamba ho gaya.',
                    },
                    {
                        'text': 'Now he is a bada elephant!',
                        'text_hindi': 'अब वह एक बड़ा हाथी है!',
                        'text_romanized': 'Ab vah ek bada haathi hai!',
                    },
                ],
            },
            {
                'title': "Grandma's Story",
                'title_hindi': 'दादी की कहानी',
                'title_romanized': 'Dadi Ki Kahani',
                'level': 1,
                'theme': 'family traditions',
                'pages': [
                    {
                        'text': 'Dadi (grandma) told me old stories.',
                        'text_hindi': 'दादी ने मुझे पुरानी कहानियाँ सुनाईं।',
                        'text_romanized': 'Dadi ne mujhe purani kahaaniyan sunaayin.',
                    },
                    {
                        'text': 'She showed me how to make rotis.',
                        'text_hindi': 'उन्होंने मुझे रोटी बनाना सिखाया।',
                        'text_romanized': 'Unhone mujhe roti banana sikhaya.',
                    },
                    {
                        'text': 'We made sweets together.',
                        'text_hindi': 'हमने साथ में मिठाई बनाई।',
                        'text_romanized': 'Humne saath mein mithai banayi.',
                    },
                    {
                        'text': 'I love learning from my dadi!',
                        'text_hindi': 'मुझे अपनी दादी से सीखना पसंद है!',
                        'text_romanized': 'Mujhe apni dadi se seekhna pasand hai!',
                    },
                ],
            },
            {
                'title': 'Rainy Day',
                'title_hindi': 'बारिश का दिन',
                'title_romanized': 'Barish Ka Din',
                'level': 1,
                'theme': 'weather',
                'pages': [
                    {
                        'text': 'The barish (rain) was falling.',
                        'text_hindi': 'बारिश हो रही थी।',
                        'text_romanized': 'Barish ho rahi thi.',
                    },
                    {
                        'text': 'I wore my raincoat and boots.',
                        'text_hindi': 'मैंने अपना रेनकोट और जूते पहने।',
                        'text_romanized': 'Maine apna raincoat aur joote pehne.',
                    },
                    {
                        'text': 'I jumped in puddles - chhap chhap!',
                        'text_hindi': 'मैं पानी के गड्ढों में कूदा - छप छप!',
                        'text_romanized': 'Main paani ke gaddhon mein kooda - chhap chhap!',
                    },
                    {
                        'text': 'Rainy days are so much fun!',
                        'text_hindi': 'बारिश के दिन बहुत मज़ेदार होते हैं!',
                        'text_romanized': 'Barish ke din bahut mazedaar hote hain!',
                    },
                ],
            },
            {
                'title': 'Sweet Shop',
                'title_hindi': 'मिठाई की दुकान',
                'title_romanized': 'Mithai Ki Dukaan',
                'level': 1,
                'theme': 'counting',
                'pages': [
                    {
                        'text': 'I went to the mithai shop with papa.',
                        'text_hindi': 'मैं पापा के साथ मिठाई की दुकान गया।',
                        'text_romanized': 'Main papa ke saath mithai ki dukaan gaya.',
                    },
                    {
                        'text': 'I counted: ek, do, teen laddus!',
                        'text_hindi': 'मैंने गिना: एक, दो, तीन लड्डू!',
                        'text_romanized': 'Maine gina: ek, do, teen laddu!',
                    },
                    {
                        'text': 'Papa bought chaar (four) jalebis.',
                        'text_hindi': 'पापा ने चार जलेबियाँ खरीदीं।',
                        'text_romanized': 'Papa ne chaar jalebiyan khareedeen.',
                    },
                    {
                        'text': 'We shared everything - yum yum!',
                        'text_hindi': 'हमने सब कुछ बाँटा - यम यम!',
                        'text_romanized': 'Humne sab kuch baanta - yum yum!',
                    },
                ],
            },
            {
                'title': 'Diwali Night',
                'title_hindi': 'दिवाली की रात',
                'title_romanized': 'Diwali Ki Raat',
                'level': 1,
                'theme': 'festivals',
                'pages': [
                    {
                        'text': 'It was Diwali, the festival of lights!',
                        'text_hindi': 'दिवाली थी, रोशनी का त्योहार!',
                        'text_romanized': 'Diwali thi, roshni ka tyohaar!',
                    },
                    {
                        'text': 'We lit diyas (lamps) everywhere.',
                        'text_hindi': 'हमने हर जगह दिए जलाए।',
                        'text_romanized': 'Humne har jagah diye jalaye.',
                    },
                    {
                        'text': 'Colorful phuljhadis (sparklers) lit up the sky.',
                        'text_hindi': 'रंग-बिरंगी फुलझड़ियों ने आसमान को रोशन किया।',
                        'text_romanized': 'Rang-birangi phuljhadiyon ne aasman ko roshan kiya.',
                    },
                    {
                        'text': 'Happy Diwali to everyone!',
                        'text_hindi': 'सभी को दिवाली की शुभकामनाएँ!',
                        'text_romanized': 'Sabhi ko Diwali ki shubhkaamnayen!',
                    },
                ],
            },
            {
                'title': 'My First Day',
                'title_hindi': 'मेरा पहला दिन',
                'title_romanized': 'Mera Pehla Din',
                'level': 1,
                'theme': 'school/new experiences',
                'pages': [
                    {
                        'text': 'Today was my first day at school.',
                        'text_hindi': 'आज स्कूल में मेरा पहला दिन था।',
                        'text_romanized': 'Aaj school mein mera pehla din tha.',
                    },
                    {
                        'text': 'I met my shikshak (teacher) Miss Sharma.',
                        'text_hindi': 'मैं अपनी शिक्षिका मिस शर्मा से मिला।',
                        'text_romanized': 'Main apni shikshika Miss Sharma se mila.',
                    },
                    {
                        'text': 'I made a new dost (friend) named Rohan.',
                        'text_hindi': 'मैंने रोहन नाम का एक नया दोस्त बनाया।',
                        'text_romanized': 'Maine Rohan naam ka ek naya dost banaya.',
                    },
                    {
                        'text': 'I cannot wait to go back tomorrow!',
                        'text_hindi': 'मैं कल फिर से जाने का इंतज़ार नहीं कर सकता!',
                        'text_romanized': 'Main kal phir se jaane ka intazaar nahi kar sakta!',
                    },
                ],
            },
        ]

        count = 0
        for idx, story_data in enumerate(stories_data):
            pages = story_data.pop('pages')

            story, created = Story.objects.update_or_create(
                title=story_data['title'],
                defaults={
                    'title_hindi': story_data['title_hindi'],
                    'title_romanized': story_data['title_romanized'],
                    'storyweaver_id': f'L1-{idx + 1}',
                    'language': Child.Language.HINDI,
                    'level': story_data['level'],
                    'page_count': len(pages),
                    'cover_image_url': 'https://via.placeholder.com/300x400',
                    'synopsis': f"L1 story: {story_data['theme']}",
                    'categories': ['L1', 'curriculum', story_data['theme']],
                    'age_min': 4,
                    'age_max': 5,
                    'is_l1_content': True,
                    'theme': story_data['theme'],
                }
            )

            # Create pages
            for page_idx, page_data in enumerate(pages, start=1):
                StoryPage.objects.update_or_create(
                    story=story,
                    page_number=page_idx,
                    defaults={
                        'text_content': page_data['text'],
                        'text_hindi': page_data.get('text_hindi', ''),
                        'text_romanized': page_data.get('text_romanized', ''),
                        'image_url': f'https://via.placeholder.com/400x300?text=Page+{page_idx}',
                    }
                )

            if created:
                count += 1
                self.stdout.write(f'  Created story: {story.title}')
            else:
                self.stdout.write(f'  Updated story: {story.title}')

        return count

    def seed_vocabulary(self):
        """Seed additional 20 vocabulary words for L1."""
        # Get or create themes
        weather_theme, _ = VocabularyTheme.objects.get_or_create(
            language=Child.Language.HINDI,
            name='Weather',
            defaults={
                'name_native': 'मौसम',
                'description': 'Weather-related words',
                'icon': '🌤️',
                'level': 1,
                'order': 6,
            }
        )

        emotions_theme, _ = VocabularyTheme.objects.get_or_create(
            language=Child.Language.HINDI,
            name='Emotions',
            defaults={
                'name_native': 'भावनाएँ',
                'description': 'Feelings and emotions',
                'icon': '😊',
                'level': 1,
                'order': 7,
            }
        )

        actions_theme, _ = VocabularyTheme.objects.get_or_create(
            language=Child.Language.HINDI,
            name='Actions',
            defaults={
                'name_native': 'क्रियाएँ',
                'description': 'Common action verbs',
                'icon': '🏃',
                'level': 1,
                'order': 8,
            }
        )

        time_theme, _ = VocabularyTheme.objects.get_or_create(
            language=Child.Language.HINDI,
            name='Time',
            defaults={
                'name_native': 'समय',
                'description': 'Time-related words',
                'icon': '⏰',
                'level': 1,
                'order': 9,
            }
        )

        words_data = [
            # Weather (5 words)
            {'theme': weather_theme, 'word': 'बारिश', 'romanization': 'Barish', 'translation': 'Rain', 'part_of_speech': 'NOUN', 'order': 1},
            {'theme': weather_theme, 'word': 'धूप', 'romanization': 'Dhoop', 'translation': 'Sunshine', 'part_of_speech': 'NOUN', 'order': 2},
            {'theme': weather_theme, 'word': 'हवा', 'romanization': 'Hawa', 'translation': 'Wind', 'part_of_speech': 'NOUN', 'order': 3},
            {'theme': weather_theme, 'word': 'बादल', 'romanization': 'Baadal', 'translation': 'Cloud', 'part_of_speech': 'NOUN', 'order': 4},
            {'theme': weather_theme, 'word': 'ठंड', 'romanization': 'Thand', 'translation': 'Cold', 'part_of_speech': 'NOUN', 'order': 5},

            # Emotions (5 words)
            {'theme': emotions_theme, 'word': 'खुश', 'romanization': 'Khush', 'translation': 'Happy', 'part_of_speech': 'ADJECTIVE', 'order': 1},
            {'theme': emotions_theme, 'word': 'उदास', 'romanization': 'Udaas', 'translation': 'Sad', 'part_of_speech': 'ADJECTIVE', 'order': 2},
            {'theme': emotions_theme, 'word': 'गुस्सा', 'romanization': 'Gussa', 'translation': 'Angry', 'part_of_speech': 'NOUN', 'order': 3},
            {'theme': emotions_theme, 'word': 'डर', 'romanization': 'Dar', 'translation': 'Fear', 'part_of_speech': 'NOUN', 'order': 4},
            {'theme': emotions_theme, 'word': 'प्यार', 'romanization': 'Pyaar', 'translation': 'Love', 'part_of_speech': 'NOUN', 'order': 5},

            # Actions (5 words)
            {'theme': actions_theme, 'word': 'खाना', 'romanization': 'Khaana', 'translation': 'To eat', 'part_of_speech': 'VERB', 'order': 1},
            {'theme': actions_theme, 'word': 'पीना', 'romanization': 'Peena', 'translation': 'To drink', 'part_of_speech': 'VERB', 'order': 2},
            {'theme': actions_theme, 'word': 'सोना', 'romanization': 'Sona', 'translation': 'To sleep', 'part_of_speech': 'VERB', 'order': 3},
            {'theme': actions_theme, 'word': 'दौड़ना', 'romanization': 'Daudna', 'translation': 'To run', 'part_of_speech': 'VERB', 'order': 4},
            {'theme': actions_theme, 'word': 'खेलना', 'romanization': 'Khelna', 'translation': 'To play', 'part_of_speech': 'VERB', 'order': 5},

            # Time (5 words)
            {'theme': time_theme, 'word': 'आज', 'romanization': 'Aaj', 'translation': 'Today', 'part_of_speech': 'ADVERB', 'order': 1},
            {'theme': time_theme, 'word': 'कल', 'romanization': 'Kal', 'translation': 'Yesterday/Tomorrow', 'part_of_speech': 'ADVERB', 'order': 2},
            {'theme': time_theme, 'word': 'सुबह', 'romanization': 'Subah', 'translation': 'Morning', 'part_of_speech': 'NOUN', 'order': 3},
            {'theme': time_theme, 'word': 'शाम', 'romanization': 'Shaam', 'translation': 'Evening', 'part_of_speech': 'NOUN', 'order': 4},
            {'theme': time_theme, 'word': 'रात', 'romanization': 'Raat', 'translation': 'Night', 'part_of_speech': 'NOUN', 'order': 5},
        ]

        count = 0
        for word_data in words_data:
            word, created = VocabularyWord.objects.update_or_create(
                theme=word_data['theme'],
                word=word_data['word'],
                defaults=word_data
            )
            if created:
                count += 1
                self.stdout.write(f'  Created word: {word.word} ({word.romanization})')

        return count
