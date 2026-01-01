/**
 * Peppi Dialogue Localization System
 * Multi-language dialogues for Peppi the AI cat tutor
 */

import { LanguageCode } from '@/types';

export interface PeppiDialogue {
  text: string;           // English
  textNative: string;     // Native script
  textRomanized: string;  // Romanized version
  emotion: 'happy' | 'excited' | 'encouraging' | 'celebrating' | 'gentle';
  sound?: 'meow' | 'purr';
}

export interface LanguageDialogues {
  correct: PeppiDialogue[];
  incorrect: PeppiDialogue[];
  streaks: {
    day3: PeppiDialogue;
    day7: PeppiDialogue;
    day30: PeppiDialogue;
  };
  greetings: {
    morning: PeppiDialogue;
    afternoon: PeppiDialogue;
    evening: PeppiDialogue;
  };
  encouragement: PeppiDialogue[];
  lessonIntro: PeppiDialogue[];
  lessonComplete: PeppiDialogue[];
  meowSound: { native: string; romanized: string };
}

// Meow sounds for each language
export const MEOW_SOUNDS: Record<LanguageCode, { native: string; romanized: string }> = {
  HINDI: { native: 'म्याऊं!', romanized: 'Myaoon!' },
  TAMIL: { native: 'மியாவ்!', romanized: 'Miyaav!' },
  TELUGU: { native: 'మియావ్!', romanized: 'Miyaav!' },
  GUJARATI: { native: 'મ્યાઉં!', romanized: 'Myaaun!' },
  PUNJABI: { native: 'ਮਿਆਊਂ!', romanized: 'Miaoon!' },
  MALAYALAM: { native: 'മിയാവ്!', romanized: 'Miyaav!' },
  BENGALI: { native: 'মিয়াউ!', romanized: 'Miyau!' },
  KANNADA: { native: 'ಮಿಯಾವ್!', romanized: 'Miyaav!' },
  MARATHI: { native: 'म्याऊ!', romanized: 'Myaau!' },
  ODIA: { native: 'ମିଆଉଁ!', romanized: 'Miaun!' },
  ASSAMESE: { native: 'মিয়াউ!', romanized: 'Miyau!' },
  URDU: { native: 'میاؤں!', romanized: 'Myaoon!' },
  FIJI_HINDI: { native: 'म्याऊं!', romanized: 'Myaoon!' },
};

// Hindi dialogues (comprehensive example)
const HINDI_DIALOGUES: LanguageDialogues = {
  correct: [
    { text: 'Amazing! You got it right!', textNative: 'शाबाश! बिल्कुल सही!', textRomanized: 'Shabash! Bilkul sahi!', emotion: 'celebrating', sound: 'meow' },
    { text: 'Wonderful! Perfect answer!', textNative: 'वाह! बहुत अच्छा!', textRomanized: 'Wah! Bahut accha!', emotion: 'excited', sound: 'purr' },
    { text: 'You are so smart!', textNative: 'तुम बहुत होशियार हो!', textRomanized: 'Tum bahut hoshiyaar ho!', emotion: 'happy' },
    { text: 'Excellent work!', textNative: 'बेहतरीन काम!', textRomanized: 'Behtareen kaam!', emotion: 'celebrating' },
    { text: 'You nailed it!', textNative: 'कमाल कर दिया!', textRomanized: 'Kamaal kar diya!', emotion: 'excited', sound: 'meow' },
  ],
  incorrect: [
    { text: 'Good try! Let\'s try again!', textNative: 'अच्छी कोशिश! फिर से करें!', textRomanized: 'Acchi koshish! Phir se karein!', emotion: 'encouraging' },
    { text: 'Almost there! Try once more!', textNative: 'करीब हो! एक बार और!', textRomanized: 'Kareeb ho! Ek baar aur!', emotion: 'gentle' },
    { text: 'Don\'t worry, you can do it!', textNative: 'चिंता मत करो, तुम कर सकते हो!', textRomanized: 'Chinta mat karo, tum kar sakte ho!', emotion: 'encouraging' },
  ],
  streaks: {
    day3: { text: '3 days in a row! Amazing!', textNative: 'लगातार 3 दिन! कमाल!', textRomanized: 'Lagatar 3 din! Kamaal!', emotion: 'celebrating', sound: 'meow' },
    day7: { text: 'One week streak! Superstar!', textNative: 'एक हफ्ते की लगातार पढ़ाई! सुपरस्टार!', textRomanized: 'Ek hafte ki lagatar padhai! Superstar!', emotion: 'celebrating', sound: 'meow' },
    day30: { text: '30 days! You are a champion!', textNative: '30 दिन! तुम चैंपियन हो!', textRomanized: '30 din! Tum champion ho!', emotion: 'celebrating', sound: 'meow' },
  },
  greetings: {
    morning: { text: 'Good morning, friend!', textNative: 'सुप्रभात दोस्त!', textRomanized: 'Suprabhat dost!', emotion: 'happy', sound: 'purr' },
    afternoon: { text: 'Good afternoon! Ready to learn?', textNative: 'नमस्ते! पढ़ने के लिए तैयार?', textRomanized: 'Namaste! Padhne ke liye taiyaar?', emotion: 'happy' },
    evening: { text: 'Good evening! Let\'s have fun!', textNative: 'शुभ संध्या! मज़े करें!', textRomanized: 'Shubh sandhya! Maze karein!', emotion: 'happy' },
  },
  encouragement: [
    { text: 'You can do it!', textNative: 'तुम कर सकते हो!', textRomanized: 'Tum kar sakte ho!', emotion: 'encouraging' },
    { text: 'Keep going!', textNative: 'आगे बढ़ो!', textRomanized: 'Aage badho!', emotion: 'encouraging' },
    { text: 'I believe in you!', textNative: 'मुझे तुम पर विश्वास है!', textRomanized: 'Mujhe tum par vishwas hai!', emotion: 'gentle' },
  ],
  lessonIntro: [
    { text: 'Let\'s start a new lesson!', textNative: 'चलो नया पाठ शुरू करें!', textRomanized: 'Chalo naya paath shuru karein!', emotion: 'excited', sound: 'meow' },
    { text: 'Today we will learn something fun!', textNative: 'आज हम कुछ मज़ेदार सीखेंगे!', textRomanized: 'Aaj hum kuch mazedaar seekhenge!', emotion: 'happy' },
  ],
  lessonComplete: [
    { text: 'Lesson complete! Great job!', textNative: 'पाठ पूरा! शाबाश!', textRomanized: 'Paath poora! Shabash!', emotion: 'celebrating', sound: 'meow' },
    { text: 'You finished the lesson!', textNative: 'तुमने पाठ पूरा कर लिया!', textRomanized: 'Tumne paath poora kar liya!', emotion: 'celebrating' },
  ],
  meowSound: MEOW_SOUNDS.HINDI,
};

// Tamil dialogues
const TAMIL_DIALOGUES: LanguageDialogues = {
  correct: [
    { text: 'Amazing! You got it right!', textNative: 'சபாஷ்! சரியான பதில்!', textRomanized: 'Sabash! Sariyaana badhil!', emotion: 'celebrating', sound: 'meow' },
    { text: 'Wonderful! Perfect!', textNative: 'அருமை! மிகச்சிறப்பு!', textRomanized: 'Arumai! Migachirappu!', emotion: 'excited', sound: 'purr' },
    { text: 'You are very smart!', textNative: 'நீ மிகவும் புத்திசாலி!', textRomanized: 'Nee migavum pudisaali!', emotion: 'happy' },
  ],
  incorrect: [
    { text: 'Good try! Try again!', textNative: 'நல்ல முயற்சி! மீண்டும் முயற்சி செய்!', textRomanized: 'Nalla muyarchi! Meendum muyarchi sei!', emotion: 'encouraging' },
    { text: 'Almost! One more time!', textNative: 'கிட்டத்தட்ட! ஒரு முறை மேலும்!', textRomanized: 'Kittathatta! Oru murai melum!', emotion: 'gentle' },
  ],
  streaks: {
    day3: { text: '3 days streak!', textNative: 'தொடர்ந்து 3 நாள்!', textRomanized: 'Thodarndhu 3 naal!', emotion: 'celebrating', sound: 'meow' },
    day7: { text: 'One week streak!', textNative: 'ஒரு வாரம் தொடர்ந்து!', textRomanized: 'Oru vaaram thodarndhu!', emotion: 'celebrating', sound: 'meow' },
    day30: { text: '30 days! Champion!', textNative: '30 நாள்! சாம்பியன்!', textRomanized: '30 naal! Champion!', emotion: 'celebrating', sound: 'meow' },
  },
  greetings: {
    morning: { text: 'Good morning!', textNative: 'காலை வணக்கம்!', textRomanized: 'Kaalai vanakkam!', emotion: 'happy', sound: 'purr' },
    afternoon: { text: 'Good afternoon!', textNative: 'மதிய வணக்கம்!', textRomanized: 'Madhiya vanakkam!', emotion: 'happy' },
    evening: { text: 'Good evening!', textNative: 'மாலை வணக்கம்!', textRomanized: 'Maalai vanakkam!', emotion: 'happy' },
  },
  encouragement: [
    { text: 'You can do it!', textNative: 'உன்னால் முடியும்!', textRomanized: 'Unnaal mudiyum!', emotion: 'encouraging' },
    { text: 'Keep going!', textNative: 'தொடர்!', textRomanized: 'Thodar!', emotion: 'encouraging' },
  ],
  lessonIntro: [
    { text: 'Let\'s start!', textNative: 'ஆரம்பிக்கலாம்!', textRomanized: 'Aarambikkalam!', emotion: 'excited', sound: 'meow' },
  ],
  lessonComplete: [
    { text: 'Lesson complete!', textNative: 'பாடம் முடிந்தது!', textRomanized: 'Paadam mudindhadu!', emotion: 'celebrating', sound: 'meow' },
  ],
  meowSound: MEOW_SOUNDS.TAMIL,
};

// Create a basic template for other languages
const createBasicDialogues = (lang: LanguageCode): LanguageDialogues => ({
  correct: [
    { text: 'Amazing!', textNative: 'Amazing!', textRomanized: 'Amazing!', emotion: 'celebrating', sound: 'meow' },
    { text: 'Great job!', textNative: 'Great job!', textRomanized: 'Great job!', emotion: 'excited' },
  ],
  incorrect: [
    { text: 'Try again!', textNative: 'Try again!', textRomanized: 'Try again!', emotion: 'encouraging' },
  ],
  streaks: {
    day3: { text: '3 day streak!', textNative: '3 day streak!', textRomanized: '3 day streak!', emotion: 'celebrating', sound: 'meow' },
    day7: { text: '7 day streak!', textNative: '7 day streak!', textRomanized: '7 day streak!', emotion: 'celebrating', sound: 'meow' },
    day30: { text: '30 day streak!', textNative: '30 day streak!', textRomanized: '30 day streak!', emotion: 'celebrating', sound: 'meow' },
  },
  greetings: {
    morning: { text: 'Good morning!', textNative: 'Good morning!', textRomanized: 'Good morning!', emotion: 'happy' },
    afternoon: { text: 'Good afternoon!', textNative: 'Good afternoon!', textRomanized: 'Good afternoon!', emotion: 'happy' },
    evening: { text: 'Good evening!', textNative: 'Good evening!', textRomanized: 'Good evening!', emotion: 'happy' },
  },
  encouragement: [
    { text: 'You can do it!', textNative: 'You can do it!', textRomanized: 'You can do it!', emotion: 'encouraging' },
  ],
  lessonIntro: [
    { text: 'Let\'s learn!', textNative: 'Let\'s learn!', textRomanized: 'Let\'s learn!', emotion: 'excited', sound: 'meow' },
  ],
  lessonComplete: [
    { text: 'Lesson complete!', textNative: 'Lesson complete!', textRomanized: 'Lesson complete!', emotion: 'celebrating', sound: 'meow' },
  ],
  meowSound: MEOW_SOUNDS[lang] || MEOW_SOUNDS.HINDI,
});

// Complete dialogues map
export const PEPPI_DIALOGUES: Record<LanguageCode, LanguageDialogues> = {
  HINDI: HINDI_DIALOGUES,
  TAMIL: TAMIL_DIALOGUES,
  TELUGU: createBasicDialogues('TELUGU'),
  GUJARATI: createBasicDialogues('GUJARATI'),
  PUNJABI: createBasicDialogues('PUNJABI'),
  MALAYALAM: createBasicDialogues('MALAYALAM'),
  BENGALI: createBasicDialogues('BENGALI'),
  KANNADA: createBasicDialogues('KANNADA'),
  MARATHI: createBasicDialogues('MARATHI'),
  ODIA: createBasicDialogues('ODIA'),
  ASSAMESE: createBasicDialogues('ASSAMESE'),
  URDU: createBasicDialogues('URDU'),
  FIJI_HINDI: HINDI_DIALOGUES, // Fiji Hindi uses Hindi dialogues
};

// Helper functions
export function getPeppiDialogue(
  language: LanguageCode,
  category: keyof Omit<LanguageDialogues, 'meowSound' | 'streaks' | 'greetings'>
): PeppiDialogue {
  const dialogues = PEPPI_DIALOGUES[language] || PEPPI_DIALOGUES.HINDI;
  const categoryDialogues = dialogues[category] as PeppiDialogue[];
  return categoryDialogues[Math.floor(Math.random() * categoryDialogues.length)];
}

export function getPeppiGreeting(language: LanguageCode): PeppiDialogue {
  const dialogues = PEPPI_DIALOGUES[language] || PEPPI_DIALOGUES.HINDI;
  const hour = new Date().getHours();

  if (hour < 12) return dialogues.greetings.morning;
  if (hour < 17) return dialogues.greetings.afternoon;
  return dialogues.greetings.evening;
}

export function getStreakDialogue(language: LanguageCode, days: number): PeppiDialogue {
  const dialogues = PEPPI_DIALOGUES[language] || PEPPI_DIALOGUES.HINDI;

  if (days >= 30) return dialogues.streaks.day30;
  if (days >= 7) return dialogues.streaks.day7;
  if (days >= 3) return dialogues.streaks.day3;

  // Default for less than 3 days
  return dialogues.encouragement[0];
}

export function getMeowForLanguage(language: LanguageCode): { native: string; romanized: string } {
  return MEOW_SOUNDS[language] || MEOW_SOUNDS.HINDI;
}
