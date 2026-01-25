"""Seed Diwali festival and story data."""
from django.core.management.base import BaseCommand
from apps.festivals.models import Festival, FestivalStory, Religion
from apps.stories.models import Story, StoryPage


# Authentic Ramayana-based Diwali story in Hindi
DIWALI_STORY_PAGES = [
    {
        "page_number": 1,
        "text_content": "बहुत समय पहले, अयोध्या में राजा दशरथ रहते थे। उनके चार बेटे थे - राम, लक्ष्मण, भरत और शत्रुघ्न। राम सबसे बड़े और सबसे प्यारे थे। एक दिन, राम को चौदह साल के लिए जंगल जाना पड़ा। उनकी पत्नी सीता और भाई लक्ष्मण भी साथ गए।",
    },
    {
        "page_number": 2,
        "text_content": "जंगल में राम, सीता और लक्ष्मण खुशी से रहते थे। लेकिन एक दिन, राक्षस राजा रावण आया। रावण बहुत शक्तिशाली था और लंका का राजा था। उसने सीता माता को चुरा लिया और लंका ले गया। राम और लक्ष्मण बहुत दुखी हुए।",
    },
    {
        "page_number": 3,
        "text_content": "राम और लक्ष्मण सीता को ढूंढने निकले। रास्ते में उन्हें हनुमान जी मिले। हनुमान जी बहुत बहादुर और शक्तिशाली थे। वे बंदरों की सेना के साथ आए। हनुमान जी ने कहा - मैं सीता माता को जरूर ढूंढूंगा!",
    },
    {
        "page_number": 4,
        "text_content": "हनुमान जी ने समुद्र पार करके सीता माता को ढूंढ लिया। फिर राम जी ने वानर सेना के साथ लंका पर चढ़ाई की। बहुत बड़ा युद्ध हुआ - अच्छाई और बुराई के बीच। आखिर में राम जी ने रावण को हरा दिया! सीता माता आजाद हो गईं!",
    },
    {
        "page_number": 5,
        "text_content": "चौदह साल पूरे हो गए। राम, सीता और लक्ष्मण अयोध्या लौटे। पुष्पक विमान में बैठकर वे आकाश में उड़े। अयोध्या के लोग बहुत खुश हुए। सबने कहा - राम जी आ रहे हैं! राम जी आ रहे हैं!",
    },
    {
        "page_number": 6,
        "text_content": "उस रात अंधेरा था - अमावस्या की रात। लोगों ने हजारों दीये जलाए। पूरी अयोध्या रोशनी से जगमगा उठी! घर-घर में खुशियां मनाई गईं। तभी से हर साल दीवाली मनाई जाती है। अच्छाई की जीत और राम जी की वापसी का त्योहार! दीवाली की शुभकामनाएं!",
    },
]


class Command(BaseCommand):
    """Seed Diwali festival and story data."""

    help = 'Seeds Diwali festival and the authentic Ramayana story'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Seeding Diwali festival and story...'))

        # Create Diwali festival
        festival, created = Festival.objects.get_or_create(
            name='Diwali',
            defaults={
                'name_native': 'दीवाली',
                'religion': Religion.HINDU,
                'description': "Festival of Lights celebrating Lord Rama's return to Ayodhya after 14 years of exile. It symbolizes the victory of good over evil, light over darkness.",
                'typical_month': 10,  # October/November (varies by lunar calendar)
                'is_active': True,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created festival: {festival.name}'))
        else:
            self.stdout.write(f'Festival already exists: {festival.name}')

        # Create the Diwali story
        story, story_created = Story.objects.get_or_create(
            storyweaver_id='diwali-ramayana-001',  # Custom ID for festival stories
            defaults={
                'title': 'राम जी की वापसी',
                'title_translit': "Ram Ji Ki Wapsi",
                'language': 'HINDI',
                'synopsis': "The authentic story of Lord Rama's return to Ayodhya from the Ramayana - the origin of Diwali.",
                'level': 1,
                'page_count': len(DIWALI_STORY_PAGES),
                'cover_image_url': 'https://example.com/diwali-story-cover.jpg',  # Placeholder
                'author': 'Traditional (Ramayana)',
            }
        )
        if story_created:
            self.stdout.write(self.style.SUCCESS(f'Created story: {story.title}'))
        else:
            self.stdout.write(f'Story already exists: {story.title}')
            # Clear existing pages to re-create them
            story.pages.all().delete()

        # Create story pages
        for page_data in DIWALI_STORY_PAGES:
            StoryPage.objects.create(
                story=story,
                page_number=page_data['page_number'],
                text_content=page_data['text_content'],
                text_hindi=page_data['text_content'],  # Also set text_hindi for Peppi narration
            )
        self.stdout.write(self.style.SUCCESS(f'Created {len(DIWALI_STORY_PAGES)} story pages'))

        # Link story to festival
        festival_story, fs_created = FestivalStory.objects.get_or_create(
            festival=festival,
            story=story,
            defaults={'is_primary': True}
        )
        if fs_created:
            self.stdout.write(self.style.SUCCESS(f'Linked story to festival'))
        else:
            self.stdout.write(f'Story already linked to festival')

        self.stdout.write(self.style.SUCCESS(
            f'\nDiwali seeding complete!\n'
            f'  Festival: {festival.name} ({festival.name_native})\n'
            f'  Story: {story.title}\n'
            f'  Pages: {len(DIWALI_STORY_PAGES)}'
        ))
