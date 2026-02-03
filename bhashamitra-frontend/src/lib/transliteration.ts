/**
 * Transliteration Service
 * Provides utilities for converting Roman/English text to Indian native scripts
 * and vice versa.
 */

import { LanguageCode } from '@/types';

// Language code mapping from BhashaMitra to transliteration library
export const TRANSLITERATION_LANGUAGE_MAP: Record<LanguageCode, string> = {
  HINDI: 'hi',
  TAMIL: 'ta',
  TELUGU: 'te',
  GUJARATI: 'gu',
  PUNJABI: 'pa',
  MALAYALAM: 'ml',
  BENGALI: 'bn',
  MARATHI: 'mr',
  KANNADA: 'kn',
  ODIA: 'or',
  ASSAMESE: 'as',
  URDU: 'ur',
  FIJI_HINDI: 'hi', // Uses Hindi transliteration
};

// Example mappings for common words (to show hints to users)
export const TRANSLITERATION_EXAMPLES: Record<LanguageCode, Array<{ roman: string; native: string }>> = {
  HINDI: [
    { roman: 'namaste', native: 'नमस्ते' },
    { roman: 'dhanyavaad', native: 'धन्यवाद' },
    { roman: 'accha', native: 'अच्छा' },
    { roman: 'pyaar', native: 'प्यार' },
  ],
  TAMIL: [
    { roman: 'vanakkam', native: 'வணக்கம்' },
    { roman: 'nandri', native: 'நன்றி' },
    { roman: 'nalla', native: 'நல்ல' },
  ],
  TELUGU: [
    { roman: 'namaskaram', native: 'నమస్కారం' },
    { roman: 'dhanyavadalu', native: 'ధన్యవాదాలు' },
    { roman: 'manchidi', native: 'మంచిది' },
  ],
  GUJARATI: [
    { roman: 'namaste', native: 'નમસ્તે' },
    { roman: 'aabhar', native: 'આભાર' },
    { roman: 'saru', native: 'સારું' },
  ],
  PUNJABI: [
    { roman: 'sat sri akal', native: 'ਸਤ ਸ੍ਰੀ ਅਕਾਲ' },
    { roman: 'dhannvaad', native: 'ਧੰਨਵਾਦ' },
    { roman: 'changa', native: 'ਚੰਗਾ' },
  ],
  MALAYALAM: [
    { roman: 'namaskaram', native: 'നമസ്കാരം' },
    { roman: 'nanni', native: 'നന്നി' },
    { roman: 'nallathu', native: 'നല്ലത്' },
  ],
  BENGALI: [
    { roman: 'namaskar', native: 'নমস্কার' },
    { roman: 'dhonnobad', native: 'ধন্যবাদ' },
    { roman: 'bhalo', native: 'ভালো' },
  ],
  MARATHI: [
    { roman: 'namaskar', native: 'नमस्कार' },
    { roman: 'dhanyavaad', native: 'धन्यवाद' },
    { roman: 'chaan', native: 'छान' },
  ],
  KANNADA: [
    { roman: 'namaskara', native: 'ನಮಸ್ಕಾರ' },
    { roman: 'dhanyavaadagalu', native: 'ಧನ್ಯವಾದಗಳು' },
    { roman: 'chennagide', native: 'ಚೆನ್ನಾಗಿದೆ' },
  ],
  ODIA: [
    { roman: 'namaskara', native: 'ନମସ୍କାର' },
    { roman: 'dhanyavaad', native: 'ଧନ୍ୟବାଦ' },
    { roman: 'bhala', native: 'ଭଲ' },
  ],
  ASSAMESE: [
    { roman: 'nomoskar', native: 'নমস্কাৰ' },
    { roman: 'dhonnobad', native: 'ধন্যবাদ' },
    { roman: 'bhal', native: 'ভাল' },
  ],
  URDU: [
    { roman: 'assalam alaikum', native: 'السلام علیکم' },
    { roman: 'shukriya', native: 'شکریہ' },
    { roman: 'accha', native: 'اچھا' },
  ],
  FIJI_HINDI: [
    { roman: 'namaste', native: 'नमस्ते' },
    { roman: 'dhanyavaad', native: 'धन्यवाद' },
    { roman: 'accha', native: 'अच्छा' },
  ],
};

// Meow sounds in different languages
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

/**
 * Get transliteration library language code from BhashaMitra language code
 */
export function getTransliterationLanguageCode(language: LanguageCode): string {
  return TRANSLITERATION_LANGUAGE_MAP[language] || 'hi';
}

/**
 * Get example transliterations for a language
 */
export function getExamples(language: LanguageCode): Array<{ roman: string; native: string }> {
  return TRANSLITERATION_EXAMPLES[language] || TRANSLITERATION_EXAMPLES.HINDI;
}

/**
 * Get a random example for a language (for hints)
 */
export function getRandomExample(language: LanguageCode): { roman: string; native: string } {
  const examples = getExamples(language);
  return examples[Math.floor(Math.random() * examples.length)];
}

/**
 * Get meow sound for a language
 */
export function getMeowSound(language: LanguageCode): { native: string; romanized: string } {
  return MEOW_SOUNDS[language] || MEOW_SOUNDS.HINDI;
}

/**
 * Check if text contains native script characters
 */
export function hasNativeScript(text: string): boolean {
  // Unicode ranges for major Indic scripts
  const indicRanges = [
    /[\u0900-\u097F]/,  // Devanagari (Hindi, Marathi, etc.)
    /[\u0980-\u09FF]/,  // Bengali, Assamese
    /[\u0A00-\u0A7F]/,  // Gurmukhi (Punjabi)
    /[\u0A80-\u0AFF]/,  // Gujarati
    /[\u0B00-\u0B7F]/,  // Oriya
    /[\u0B80-\u0BFF]/,  // Tamil
    /[\u0C00-\u0C7F]/,  // Telugu
    /[\u0C80-\u0CFF]/,  // Kannada
    /[\u0D00-\u0D7F]/,  // Malayalam
    /[\u0600-\u06FF]/,  // Arabic (Urdu)
  ];

  return indicRanges.some(range => range.test(text));
}

/**
 * Check if text is likely Roman/English
 */
export function isRomanScript(text: string): boolean {
  return /^[a-zA-Z0-9\s.,!?'-]+$/.test(text);
}

/**
 * Detect script type
 */
export function detectScriptType(text: string): 'native' | 'roman' | 'mixed' {
  if (!text.trim()) return 'roman';

  const hasNative = hasNativeScript(text);
  const hasRoman = /[a-zA-Z]/.test(text);

  if (hasNative && hasRoman) return 'mixed';
  if (hasNative) return 'native';
  return 'roman';
}

/**
 * Clean and normalize text for transliteration
 */
export function normalizeForTransliteration(text: string): string {
  return text.trim().replace(/\s+/g, ' ');
}

/**
 * Validate language code
 */
export function isValidLanguageCode(code: string): code is LanguageCode {
  return code in TRANSLITERATION_LANGUAGE_MAP;
}

/**
 * Simple Roman to Devanagari transliteration map
 * This is a basic implementation - can be enhanced with a proper library
 */
const HINDI_TRANSLITERATION_MAP: Record<string, string> = {
  // Vowels
  'a': 'अ', 'aa': 'आ', 'i': 'इ', 'ii': 'ई', 'ee': 'ई',
  'u': 'उ', 'uu': 'ऊ', 'oo': 'ऊ', 'e': 'ए', 'ai': 'ऐ',
  'o': 'ओ', 'au': 'औ', 'ou': 'औ',
  // Consonants
  'ka': 'क', 'kha': 'ख', 'ga': 'ग', 'gha': 'घ', 'nga': 'ङ',
  'cha': 'च', 'chha': 'छ', 'ja': 'ज', 'jha': 'झ', 'nya': 'ञ',
  'ta': 'ट', 'tha': 'ठ', 'da': 'ड', 'dha': 'ढ', 'na': 'न',
  'pa': 'प', 'pha': 'फ', 'ba': 'ब', 'bha': 'भ', 'ma': 'म',
  'ya': 'य', 'ra': 'र', 'la': 'ल', 'va': 'व', 'wa': 'व',
  'sha': 'श', 'sa': 'स', 'ha': 'ह',
  // Common words
  'namaste': 'नमस्ते', 'dhanyavaad': 'धन्यवाद', 'accha': 'अच्छा',
  'bahut': 'बहुत', 'acha': 'अच्छा', 'theek': 'ठीक', 'hai': 'है',
  'main': 'मैं', 'aap': 'आप', 'tum': 'तुम', 'hum': 'हम',
  'kya': 'क्या', 'kaise': 'कैसे', 'kyun': 'क्यों',
  'pyaar': 'प्यार', 'mitra': 'मित्र', 'dost': 'दोस्त',
  'shabash': 'शाबाश', 'wah': 'वाह', 'myaun': 'म्याऊं',
};

/**
 * Simple transliteration function for Hindi
 * For production, use @ai4bharat/indic-transliterate library
 */
export function simpleTransliterate(text: string, language: LanguageCode): string {
  if (language !== 'HINDI' && language !== 'FIJI_HINDI' && language !== 'MARATHI') {
    // Return as-is for languages without basic transliteration support
    return text;
  }

  const words = text.toLowerCase().split(/\s+/);
  const transliterated = words.map(word => {
    // Check if word exists in map
    if (HINDI_TRANSLITERATION_MAP[word]) {
      return HINDI_TRANSLITERATION_MAP[word];
    }
    // Return original if not found
    return word;
  });

  return transliterated.join(' ');
}
