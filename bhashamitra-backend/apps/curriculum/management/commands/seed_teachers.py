"""Seed teachers (Peppi and Gyan)."""
from django.core.management.base import BaseCommand
from apps.curriculum.models.teacher import Teacher


class Command(BaseCommand):
    help = 'Seed teachers Peppi (L1-L5) and Gyan (L6-L10)'

    def handle(self, *args, **options):
        teachers_data = [
            {
                'name': 'Peppi',
                'name_hindi': 'पेप्पी',
                'character_type': 'CAT',
                'breed': 'Ragdoll Cat',
                'personality': 'Warm, playful, encouraging, patient, friendly',
                'voice_style': 'Soft, friendly, gentle, uses simple words',
                'intro_message': 'नमस्ते! मैं पेप्पी हूँ! तुम्हारी नई दोस्त! आओ साथ में हिंदी सीखें!',
                'encouragement_phrases': [
                    'वाह! बहुत अच्छे!', 'शाबाश!', 'तुम तो स्टार हो!',
                    'कमाल कर दिया!', 'बिल्कुल सही!', 'मुझे तुम पर गर्व है!'
                ],
            },
            {
                'name': 'Gyan',
                'name_hindi': 'ज्ञान',
                'character_type': 'OWL',
                'breed': 'Great Horned Owl',
                'personality': 'Wise, patient, scholarly, encouraging, thoughtful',
                'voice_style': 'Deep, calm, authoritative but kind',
                'intro_message': 'नमस्ते विद्यार्थी! मैं ज्ञान हूँ। अब हम मिलकर हिंदी में माहिर बनेंगे!',
                'encouragement_phrases': [
                    'उत्तम!', 'बहुत बढ़िया!', 'ज्ञान की राह पर आगे बढ़ो!',
                    'शानदार प्रगति!', 'तुम सही दिशा में जा रहे हो!'
                ],
            },
        ]

        created_count = 0
        updated_count = 0

        for data in teachers_data:
            teacher, created = Teacher.objects.update_or_create(
                name=data['name'],
                defaults=data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created teacher: {teacher.name}')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Updated teacher: {teacher.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nCompleted! Created: {created_count}, Updated: {updated_count}'
            )
        )
