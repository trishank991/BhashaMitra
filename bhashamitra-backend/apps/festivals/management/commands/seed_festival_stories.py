"""Seed festival stories for multiple festivals."""
from django.core.management.base import BaseCommand
from apps.festivals.models import Festival, FestivalStory
from apps.stories.models import Story, StoryPage


# Holi story - The Story of Prahlad and Holika
HOLI_STORY_PAGES = [
    {
        "page_number": 1,
        "text_content": "बहुत समय पहले, हिरण्यकश्यप नाम का एक राक्षस राजा था। वह बहुत शक्तिशाली था और चाहता था कि सब लोग सिर्फ उसकी पूजा करें। लेकिन उसका बेटा प्रह्लाद भगवान विष्णु का भक्त था।",
    },
    {
        "page_number": 2,
        "text_content": "हिरण्यकश्यप बहुत गुस्सा हुआ। उसने कहा - प्रह्लाद, विष्णु की पूजा बंद करो! लेकिन प्रह्लाद ने कहा - पिताजी, भगवान विष्णु हर जगह हैं। वे सबसे महान हैं। मैं उनकी पूजा करता रहूंगा।",
    },
    {
        "page_number": 3,
        "text_content": "हिरण्यकश्यप की बहन होलिका को एक वरदान मिला था - वह आग में नहीं जलती थी। राजा ने कहा - होलिका, तुम प्रह्लाद को गोद में लेकर आग में बैठ जाओ। प्रह्लाद जल जाएगा!",
    },
    {
        "page_number": 4,
        "text_content": "होलिका प्रह्लाद को लेकर आग में बैठ गई। प्रह्लाद ने आँखें बंद कीं और भगवान विष्णु का नाम लिया। तभी चमत्कार हुआ! होलिका जल गई लेकिन प्रह्लाद बच गया!",
    },
    {
        "page_number": 5,
        "text_content": "भगवान विष्णु ने नरसिंह रूप में प्रकट होकर हिरण्यकश्यप का वध किया। बुराई पर अच्छाई की जीत हुई! तभी से होलिका दहन मनाया जाता है - बुराई के अंत की याद में।",
    },
    {
        "page_number": 6,
        "text_content": "अगले दिन सब लोग खुशी से रंगों से खेलते हैं। यह रंगों का त्योहार है - होली! सब मिलकर गाते हैं, नाचते हैं और गुझिया खाते हैं। होली की शुभकामनाएं!",
    },
]

# Raksha Bandhan story - The Legend of Indra and Sachi
RAKSHA_BANDHAN_STORY_PAGES = [
    {
        "page_number": 1,
        "text_content": "बहुत पुराने समय की बात है। देवताओं के राजा इंद्र और असुरों के बीच बहुत बड़ा युद्ध हुआ। असुर बहुत शक्तिशाली थे और देवता हारने लगे।",
    },
    {
        "page_number": 2,
        "text_content": "इंद्र की पत्नी शची बहुत चिंतित हो गईं। उन्होंने भगवान विष्णु से प्रार्थना की। भगवान विष्णु ने उन्हें एक पवित्र धागा दिया और कहा - इसे इंद्र की कलाई पर बांध दो।",
    },
    {
        "page_number": 3,
        "text_content": "शची ने श्रावण पूर्णिमा के दिन इंद्र की कलाई पर वह पवित्र धागा बांधा। यह धागा रक्षा का प्रतीक था। इसे बांधते समय शची ने इंद्र की सलामती की कामना की।",
    },
    {
        "page_number": 4,
        "text_content": "उस रक्षा धागे की शक्ति से इंद्र ने असुरों को हरा दिया! देवताओं की जीत हुई। तभी से यह परंपरा शुरू हुई - बहनें भाइयों को राखी बांधती हैं।",
    },
    {
        "page_number": 5,
        "text_content": "आज भी रक्षा बंधन के दिन बहनें अपने भाइयों को राखी बांधती हैं। भाई वादा करते हैं कि वे हमेशा अपनी बहनों की रक्षा करेंगे। यह प्यार और विश्वास का बंधन है।",
    },
    {
        "page_number": 6,
        "text_content": "इस दिन परिवार साथ मिलकर मिठाई खाते हैं। बहनें भाइयों को तिलक लगाती हैं और राखी बांधती हैं। भाई बहनों को उपहार देते हैं। रक्षा बंधन की शुभकामनाएं!",
    },
]

# Janmashtami story - Birth of Lord Krishna
JANMASHTAMI_STORY_PAGES = [
    {
        "page_number": 1,
        "text_content": "बहुत समय पहले मथुरा में कंस नाम का एक क्रूर राजा था। उसकी बहन देवकी से एक आकाशवाणी हुई कि देवकी का आठवां पुत्र कंस का वध करेगा।",
    },
    {
        "page_number": 2,
        "text_content": "कंस ने देवकी और उनके पति वसुदेव को कारागार में डाल दिया। रात के समय, अमावस्या के अंधेरे में, देवकी के आठवें पुत्र का जन्म हुआ - भगवान कृष्ण!",
    },
    {
        "page_number": 3,
        "text_content": "कृष्ण जन्म के समय चमत्कार हुए! कारागार के दरवाजे खुल गए। वसुदेव शिशु कृष्ण को टोकरी में रखकर निकले। आकाश में बारिश हो रही थी।",
    },
    {
        "page_number": 4,
        "text_content": "शेषनाग ने अपने फन से कृष्ण को बारिश से बचाया। वसुदेव यमुना नदी पार करने लगे। उफनती नदी ने भी रास्ता दे दिया! वे गोकुल पहुंच गए।",
    },
    {
        "page_number": 5,
        "text_content": "गोकुल में नंद बाबा और यशोदा मैया ने कृष्ण को अपना लिया। कान्हा गोकुल में बड़े हुए। वे माखन चुराते, बांसुरी बजाते और सबको खुश रखते।",
    },
    {
        "page_number": 6,
        "text_content": "आज भी जन्माष्टमी पर हम कान्हा का जन्मदिन मनाते हैं। मंदिरों में झांकियां सजती हैं। दही हांडी फोड़ी जाती है। जन्माष्टमी की शुभकामनाएं! जय श्री कृष्ण!",
    },
]

# Ganesh Chaturthi story - How Ganesha got his elephant head
GANESH_CHATURTHI_STORY_PAGES = [
    {
        "page_number": 1,
        "text_content": "बहुत समय पहले की बात है। माता पार्वती ने स्नान करने से पहले चंदन के उबटन से एक बालक बनाया और उसमें प्राण डाल दिए। उन्होंने उसे द्वार पर पहरा देने को कहा।",
    },
    {
        "page_number": 2,
        "text_content": "जब भगवान शिव वापस आए, तो बालक ने उन्हें रोक दिया। शिव जी ने कहा - मैं इस घर का स्वामी हूं। लेकिन बालक ने माता पार्वती का आदेश माना और शिव जी को नहीं जाने दिया।",
    },
    {
        "page_number": 3,
        "text_content": "भगवान शिव को बहुत क्रोध आया। उन्होंने अपने त्रिशूल से बालक का सिर काट दिया। जब पार्वती जी को पता चला, वे बहुत दुखी हुईं। उन्होंने कहा - यह मेरा पुत्र था!",
    },
    {
        "page_number": 4,
        "text_content": "शिव जी को बहुत पश्चाताप हुआ। उन्होंने अपने गणों से कहा - जाओ, जो पहला प्राणी मिले जो उत्तर दिशा में सिर करके सोया हो, उसका सिर ले आओ।",
    },
    {
        "page_number": 5,
        "text_content": "गणों को एक हाथी मिला जो उत्तर दिशा में सोया था। उन्होंने हाथी का सिर लाकर बालक के धड़ से जोड़ दिया। शिव जी ने उसे जीवित कर दिया और गणेश नाम दिया।",
    },
    {
        "page_number": 6,
        "text_content": "भगवान शिव ने कहा - गणेश सबसे पहले पूजे जाएंगे। आज भी हर शुभ काम से पहले गणेश जी की पूजा होती है। गणेश चतुर्थी पर हम गणपति बप्पा का स्वागत करते हैं। गणपति बप्पा मोरया!",
    },
]

# Navratri story - Goddess Durga and Mahishasura
NAVRATRI_STORY_PAGES = [
    {
        "page_number": 1,
        "text_content": "बहुत समय पहले महिषासुर नाम का एक शक्तिशाली राक्षस था। उसने कठोर तपस्या करके ब्रह्मा जी से वरदान मांगा कि कोई देवता या मनुष्य उसे न मार सके।",
    },
    {
        "page_number": 2,
        "text_content": "महिषासुर ने तीनों लोकों पर कब्जा कर लिया। देवता डर गए। उन्होंने मिलकर अपनी शक्तियां दीं और एक देवी का जन्म हुआ - माँ दुर्गा! दसों हाथों वाली, शेर पर सवार।",
    },
    {
        "page_number": 3,
        "text_content": "हर देवता ने माँ दुर्गा को अपने अस्त्र दिए। शिव ने त्रिशूल, विष्णु ने चक्र, इंद्र ने वज्र दिया। माँ दुर्गा अब बहुत शक्तिशाली थीं।",
    },
    {
        "page_number": 4,
        "text_content": "माँ दुर्गा और महिषासुर के बीच नौ दिन तक भयंकर युद्ध हुआ। महिषासुर बार-बार रूप बदलता था। अंत में वह भैंसे का रूप लेकर लड़ा।",
    },
    {
        "page_number": 5,
        "text_content": "दसवें दिन माँ दुर्गा ने अपने त्रिशूल से महिषासुर का वध किया। बुराई पर अच्छाई की जीत हुई! इसीलिए इस दिन को विजयादशमी कहते हैं।",
    },
    {
        "page_number": 6,
        "text_content": "नवरात्रि के नौ दिन हम माँ दुर्गा के नौ रूपों की पूजा करते हैं। गरबा और डांडिया नृत्य होता है। दसवें दिन विजयादशमी मनाते हैं। जय माता दी!",
    },
]

# Christmas story - Birth of Jesus (simplified for children)
CHRISTMAS_STORY_PAGES = [
    {
        "page_number": 1,
        "text_content": "बहुत समय पहले नाज़रेथ शहर में मरियम नाम की एक दयालु लड़की रहती थी। एक दिन स्वर्ग से एक देवदूत आया और उसने कहा - मरियम, तुम्हें एक विशेष बच्चा होगा।",
    },
    {
        "page_number": 2,
        "text_content": "मरियम और उसके पति यूसुफ को बेथलहम जाना पड़ा। वहां बहुत भीड़ थी। कोई जगह नहीं मिली। आखिर में उन्हें एक अस्तबल में जगह मिली जहां जानवर रहते थे।",
    },
    {
        "page_number": 3,
        "text_content": "उसी रात एक चमत्कार हुआ! मरियम को एक सुंदर बच्चा हुआ - यीशु मसीह। उन्होंने बच्चे को कपड़े में लपेटकर चरनी में सुला दिया।",
    },
    {
        "page_number": 4,
        "text_content": "आसमान में एक बहुत बड़ा तारा चमका। यह तारा दूर देश के तीन बुद्धिमान राजाओं को रास्ता दिखा रहा था। वे बच्चे यीशु को देखने आए और उपहार लाए।",
    },
    {
        "page_number": 5,
        "text_content": "खेतों में चरवाहे अपनी भेड़ों की देखभाल कर रहे थे। देवदूतों ने उन्हें बताया कि एक खास बच्चा पैदा हुआ है। वे भी यीशु को देखने दौड़े आए।",
    },
    {
        "page_number": 6,
        "text_content": "यीशु बड़े होकर सबको प्यार और दया सिखाते। क्रिसमस पर हम यीशु के जन्म का त्योहार मनाते हैं। घर सजाते हैं, केक खाते हैं और उपहार बांटते हैं। मेरी क्रिसमस!",
    },
]

# Eid story - The Story of Prophet Ibrahim (simplified for children)
EID_STORY_PAGES = [
    {
        "page_number": 1,
        "text_content": "बहुत पुराने समय की बात है। इब्राहीम नाम के एक नेक इंसान थे। वे अल्लाह से बहुत प्यार करते थे और हमेशा सच बोलते थे। सब उन्हें बहुत मानते थे।",
    },
    {
        "page_number": 2,
        "text_content": "इब्राहीम की एक परीक्षा हुई। अल्लाह ने उन्हें सपने में एक कठिन काम करने को कहा। इब्राहीम ने अल्लाह पर भरोसा रखा और कहा - मैं आपका हुक्म मानूंगा।",
    },
    {
        "page_number": 3,
        "text_content": "जब इब्राहीम ने अल्लाह का हुक्म मानने की तैयारी की, तब अल्लाह बहुत खुश हुए। उन्होंने कहा - इब्राहीम, तुमने परीक्षा पास कर ली! तुम सच्चे भक्त हो।",
    },
    {
        "page_number": 4,
        "text_content": "अल्लाह ने इब्राहीम की जगह एक मेंढा भेज दिया। इब्राहीम की श्रद्धा और समर्पण की याद में हर साल ईद-उल-अज़हा मनाई जाती है।",
    },
    {
        "page_number": 5,
        "text_content": "ईद के दिन सब लोग नए कपड़े पहनते हैं। सुबह सब मिलकर नमाज़ पढ़ते हैं। एक दूसरे को गले लगाते हैं और कहते हैं - ईद मुबारक!",
    },
    {
        "page_number": 6,
        "text_content": "ईद पर खूब सेवइयां और मिठाइयां बनती हैं। बच्चों को ईदी मिलती है। गरीबों को दान दिया जाता है। सब मिलकर खुशियां बांटते हैं। ईद मुबारक!",
    },
]


FESTIVAL_STORIES = {
    'Holi': {
        'title': 'प्रह्लाद और होलिका की कथा',
        'title_translit': 'Prahlad aur Holika ki Katha',
        'synopsis': 'The story of Prahlad and Holika - how good triumphed over evil and why we celebrate Holi.',
        'pages': HOLI_STORY_PAGES,
        'storyweaver_id': 'holi-prahlad-001',
    },
    'Raksha Bandhan': {
        'title': 'रक्षा बंधन की कहानी',
        'title_translit': 'Raksha Bandhan ki Kahani',
        'synopsis': 'The legend of how the sacred thread of protection began - the story of Indra and Sachi.',
        'pages': RAKSHA_BANDHAN_STORY_PAGES,
        'storyweaver_id': 'raksha-bandhan-001',
    },
    'Janmashtami': {
        'title': 'कान्हा का जन्म',
        'title_translit': 'Kanha ka Janm',
        'synopsis': 'The miraculous birth of Lord Krishna on a dark night in Mathura.',
        'pages': JANMASHTAMI_STORY_PAGES,
        'storyweaver_id': 'janmashtami-krishna-001',
    },
    'Ganesh Chaturthi': {
        'title': 'गणेश जी की कथा',
        'title_translit': 'Ganesh Ji ki Katha',
        'synopsis': 'How Lord Ganesha got his elephant head - the beloved story of the remover of obstacles.',
        'pages': GANESH_CHATURTHI_STORY_PAGES,
        'storyweaver_id': 'ganesh-chaturthi-001',
    },
    'Navratri': {
        'title': 'माँ दुर्गा और महिषासुर',
        'title_translit': 'Maa Durga aur Mahishasur',
        'synopsis': 'The epic battle between Goddess Durga and the demon Mahishasura.',
        'pages': NAVRATRI_STORY_PAGES,
        'storyweaver_id': 'navratri-durga-001',
    },
    'Christmas': {
        'title': 'यीशु का जन्म',
        'title_translit': 'Yeshu ka Janm',
        'synopsis': 'The story of the birth of Jesus Christ in Bethlehem.',
        'pages': CHRISTMAS_STORY_PAGES,
        'storyweaver_id': 'christmas-jesus-001',
    },
    'Eid ul-Adha': {
        'title': 'ईद की कहानी',
        'title_translit': 'Eid ki Kahani',
        'synopsis': 'The story of Prophet Ibrahim and the meaning of Eid ul-Adha.',
        'pages': EID_STORY_PAGES,
        'storyweaver_id': 'eid-ibrahim-001',
    },
}


class Command(BaseCommand):
    """Seed festival stories for multiple festivals."""

    help = 'Seeds stories for major festivals (Holi, Raksha Bandhan, Janmashtami, Ganesh Chaturthi, Navratri, Christmas, Eid)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--festival',
            type=str,
            help='Seed story for a specific festival only (e.g., Holi, Christmas)',
        )

    def handle(self, *args, **options):
        specific_festival = options.get('festival')

        festivals_to_seed = FESTIVAL_STORIES.keys()
        if specific_festival:
            if specific_festival not in FESTIVAL_STORIES:
                self.stdout.write(self.style.ERROR(
                    f'Festival "{specific_festival}" not found. Available: {", ".join(FESTIVAL_STORIES.keys())}'
                ))
                return
            festivals_to_seed = [specific_festival]

        self.stdout.write(self.style.NOTICE(f'Seeding stories for {len(list(festivals_to_seed))} festivals...'))

        for festival_name in festivals_to_seed:
            self.seed_festival_story(festival_name)

        self.stdout.write(self.style.SUCCESS('\nFestival story seeding complete!'))

    def seed_festival_story(self, festival_name: str):
        """Seed a story for a specific festival."""
        story_data = FESTIVAL_STORIES[festival_name]

        # Find the festival
        try:
            festival = Festival.objects.get(name=festival_name)
        except Festival.DoesNotExist:
            self.stdout.write(self.style.WARNING(
                f'Festival "{festival_name}" not found in database. Skipping...'
            ))
            return

        self.stdout.write(f'\nSeeding story for {festival_name}...')

        # Create or update the story
        story, story_created = Story.objects.update_or_create(
            storyweaver_id=story_data['storyweaver_id'],
            defaults={
                'title': story_data['title'],
                'title_translit': story_data['title_translit'],
                'language': 'HINDI',
                'synopsis': story_data['synopsis'],
                'level': 1,
                'page_count': len(story_data['pages']),
                'cover_image_url': '',
                'author': 'Traditional',
                'is_l1_content': True,
                'theme': 'Festival',
                'age_min': 4,
                'age_max': 10,
                'tier': 'free',
                'xp_reward': 15,
                'estimated_minutes': 5,
                'is_active': True,
            }
        )

        if story_created:
            self.stdout.write(self.style.SUCCESS(f'  Created story: {story.title}'))
        else:
            self.stdout.write(f'  Updated story: {story.title}')
            # Clear existing pages to re-create them
            story.pages.all().delete()

        # Create story pages
        for page_data in story_data['pages']:
            StoryPage.objects.create(
                story=story,
                page_number=page_data['page_number'],
                text_content=page_data['text_content'],
                text_hindi=page_data['text_content'],  # Also set text_hindi for Peppi narration
            )
        self.stdout.write(self.style.SUCCESS(f'  Created {len(story_data["pages"])} pages'))

        # Link story to festival
        festival_story, fs_created = FestivalStory.objects.get_or_create(
            festival=festival,
            story=story,
            defaults={'is_primary': True}
        )
        if fs_created:
            self.stdout.write(self.style.SUCCESS(f'  Linked story to festival'))
        else:
            self.stdout.write(f'  Story already linked to festival')
