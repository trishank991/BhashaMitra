"""Seed themed classrooms for L1-L10."""
from django.core.management.base import BaseCommand
from apps.curriculum.models.classroom import Classroom
from apps.curriculum.models.level import CurriculumLevel


class Command(BaseCommand):
    help = 'Seed themed classrooms for curriculum levels L1-L10'

    def handle(self, *args, **options):
        classrooms_data = [
            {
                'level_code': 'L1',
                'name': 'Garden of Beginnings',
                'name_hindi': 'शुरुआत का बगीचा',
                'theme': 'GARDEN',
                'description': 'A colorful garden where young learners take their first steps in Hindi.',
                'background_color': '#90EE90',
                'elements': ['flowers', 'butterflies', 'sunshine', 'watering_can'],
                'unlock_animation': 'bloom',
                'ambient_sounds': ['birds_chirping', 'gentle_breeze'],
            },
            {
                'level_code': 'L2',
                'name': 'Treehouse Adventure',
                'name_hindi': 'पेड़ का घर',
                'theme': 'TREEHOUSE',
                'description': 'A cozy treehouse where curiosity grows.',
                'background_color': '#8B7355',
                'elements': ['wooden_cabin', 'birds', 'leaves', 'rope_ladder'],
                'unlock_animation': 'swing',
                'ambient_sounds': ['rustling_leaves', 'bird_songs'],
            },
            {
                'level_code': 'L3',
                'name': 'Forest Path',
                'name_hindi': 'वन पथ',
                'theme': 'FOREST',
                'description': 'A magical forest path leading to discovery.',
                'background_color': '#228B22',
                'elements': ['tall_trees', 'mushrooms', 'sunrays', 'forest_animals'],
                'unlock_animation': 'reveal',
                'ambient_sounds': ['forest_sounds', 'water_stream'],
            },
            {
                'level_code': 'L4',
                'name': 'Flower Meadow',
                'name_hindi': 'फूलों का मैदान',
                'theme': 'MEADOW',
                'description': 'A beautiful meadow where creativity blooms.',
                'background_color': '#FFDB58',
                'elements': ['wildflowers', 'butterflies', 'grass', 'rainbow'],
                'unlock_animation': 'flutter',
                'ambient_sounds': ['meadow_breeze', 'bees_buzzing'],
            },
            {
                'level_code': 'L5',
                'name': 'Starry Night Sky',
                'name_hindi': 'तारों भरा आकाश',
                'theme': 'NIGHT_SKY',
                'description': 'Under the stars, dreams become reality.',
                'background_color': '#191970',
                'elements': ['stars', 'moon', 'constellations', 'shooting_stars'],
                'unlock_animation': 'twinkle',
                'ambient_sounds': ['night_sounds', 'gentle_wind'],
            },
            {
                'level_code': 'L6',
                'name': 'Ancient Library',
                'name_hindi': 'प्राचीन पुस्तकालय',
                'theme': 'LIBRARY',
                'description': 'A library full of ancient wisdom and stories.',
                'background_color': '#8B4513',
                'elements': ['bookshelves', 'scrolls', 'candles', 'reading_desk'],
                'unlock_animation': 'page_turn',
                'ambient_sounds': ['page_rustling', 'fireplace'],
            },
            {
                'level_code': 'L7',
                'name': 'Mountain Peak',
                'name_hindi': 'पर्वत शिखर',
                'theme': 'MOUNTAIN',
                'description': 'Reaching new heights of knowledge.',
                'background_color': '#4682B4',
                'elements': ['snow_peak', 'clouds', 'eagles', 'prayer_flags'],
                'unlock_animation': 'soar',
                'ambient_sounds': ['mountain_wind', 'eagle_cry'],
            },
            {
                'level_code': 'L8',
                'name': 'Space Station',
                'name_hindi': 'अंतरिक्ष स्टेशन',
                'theme': 'SPACE',
                'description': 'Exploring the universe of language.',
                'background_color': '#000033',
                'elements': ['planets', 'stars', 'spacecraft', 'nebula'],
                'unlock_animation': 'launch',
                'ambient_sounds': ['space_ambient', 'rocket_hum'],
            },
            {
                'level_code': 'L9',
                'name': 'Crystal Palace',
                'name_hindi': 'क्रिस्टल महल',
                'theme': 'PALACE',
                'description': 'A palace of knowledge and refinement.',
                'background_color': '#E6E6FA',
                'elements': ['crystals', 'gems', 'pillars', 'fountains'],
                'unlock_animation': 'sparkle',
                'ambient_sounds': ['crystal_chimes', 'fountain'],
            },
            {
                'level_code': 'L10',
                'name': 'Royal Court',
                'name_hindi': 'राजदरबार',
                'theme': 'ROYAL_COURT',
                'description': 'The throne of mastery awaits.',
                'background_color': '#FFD700',
                'elements': ['throne', 'crown', 'chandeliers', 'royal_carpet'],
                'unlock_animation': 'crown',
                'ambient_sounds': ['royal_fanfare', 'court_ambiance'],
            },
        ]

        created_count = 0
        updated_count = 0
        errors = 0

        for data in classrooms_data:
            level_code = data.pop('level_code')
            try:
                level = CurriculumLevel.objects.get(code=level_code)
                classroom, created = Classroom.objects.update_or_create(
                    level=level,
                    defaults=data
                )
                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Created classroom: {classroom.name} ({level_code})')
                    )
                else:
                    updated_count += 1
                    self.stdout.write(
                        self.style.WARNING(f'Updated classroom: {classroom.name} ({level_code})')
                    )
            except CurriculumLevel.DoesNotExist:
                errors += 1
                self.stdout.write(
                    self.style.ERROR(f'Level {level_code} not found - skipping classroom')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nCompleted! Created: {created_count}, Updated: {updated_count}, Errors: {errors}'
            )
        )
