/**
 * Vocabulary Image Mapping using Twemoji
 *
 * This utility provides consistent, high-quality emoji images for vocabulary words
 * using Twitter's Twemoji CDN (open source, cross-platform consistent)
 *
 * CDN: https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/{codepoint}.svg
 */

const TWEMOJI_BASE = 'https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg';

/**
 * Convert emoji to Twemoji URL
 * @param emoji - The emoji character(s)
 * @returns Twemoji CDN URL for the SVG
 */
export function emojiToTwemojiUrl(emoji: string): string {
  // Get codepoints and join with hyphen using Array.from for better ES5 compatibility
  const codepoints = Array.from(emoji)
    .map(char => char.codePointAt(0)?.toString(16))
    .filter(Boolean)
    .join('-');
  return `${TWEMOJI_BASE}/${codepoints}.svg`;
}

/**
 * English translation to emoji mapping
 * Maps vocabulary translations to appropriate emojis
 */
export const VOCABULARY_EMOJI_MAP: Record<string, string> = {
  // ========== FAMILY ==========
  'mother': '👩',
  'mom': '👩',
  'father': '👨',
  'papa': '👨',
  'dad': '👨',
  'brother': '👦',
  'sister': '👧',
  'grandfather': '👴',
  'grandfather (maternal)': '👴',
  'grandfather (paternal)': '👴',
  'grandmother': '👵',
  'grandmother (maternal)': '👵',
  'grandmother (paternal)': '👵',
  'uncle': '👨',
  'uncle (paternal)': '👨',
  'uncle (maternal)': '👨',
  "uncle (father's elder brother)": '👨',
  "uncle (father's younger brother)": '👨',
  'aunt': '👩',
  'aunt (paternal)': '👩',
  'aunt (maternal)': '👩',
  'aunt (paternal uncle wife)': '👩',
  "aunt (mother's elder sister)": '👩',
  "aunt (mother's younger sister)": '👩',
  'son': '👦',
  'daughter': '👧',
  'elder brother': '👦',
  'elder sister': '👧',
  'maternal uncle': '👨',
  'maternal aunt': '👩',
  'maternal grandfather': '👴',
  'maternal grandmother': '👵',
  'paternal uncle': '👨',
  'paternal aunt': '👩',

  // ========== COLORS ==========
  'red': '🔴',
  'blue': '🔵',
  'yellow': '💛',
  'green': '💚',
  'black': '⚫',
  'white': '⚪',
  'orange': '🟠',
  'pink': '💗',
  'purple': '🟣',
  'brown': '🟤',

  // ========== NUMBERS ==========
  'one': '1️⃣',
  'two': '2️⃣',
  'three': '3️⃣',
  'four': '4️⃣',
  'five': '5️⃣',
  'six': '6️⃣',
  'seven': '7️⃣',
  'eight': '8️⃣',
  'nine': '9️⃣',
  'ten': '🔟',
  'twenty': '🔢',
  'twenty-one': '🔢',
  'hundred': '💯',

  // ========== ANIMALS ==========
  'dog': '🐕',
  'cat': '🐈',
  'cow': '🐄',
  'horse': '🐴',
  'elephant': '🐘',
  'lion': '🦁',
  'tiger': '🐅',
  'monkey': '🐒',
  'bird': '🐦',
  'fish': '🐟',
  'rabbit': '🐰',
  'crow': '🐦‍⬛',
  'butterfly': '🦋',
  'sparrow': '🐦',
  'parrot': '🦜',
  'chicken': '🐔',

  // ========== BODY PARTS ==========
  'head': '🗣️',
  'eye': '👁️',
  'ear': '👂',
  'nose': '👃',
  'mouth': '👄',
  'hand': '✋',
  'foot': '🦶',
  'leg': '🦵',
  'foot/leg': '🦶',
  'leg/foot': '🦶',
  'stomach': '🫃',
  'teeth': '🦷',
  'hair': '💇',
  'finger': '👆',

  // ========== FOOD & DRINKS ==========
  'water': '💧',
  'milk': '🥛',
  'bread': '🍞',
  'bread/roti': '🫓',
  'rice': '🍚',
  'lentils': '🍲',
  'vegetable': '🥬',
  'fruit': '🍎',
  'apple': '🍎',
  'mango': '🥭',
  'banana': '🍌',
  'grapes': '🍇',
  'orange fruit': '🍊',
  'food': '🍽️',
  'sweets': '🍬',
  'curry': '🍛',
  'chutney': '🫙',
  'taro': '🥔',
  'fried bread': '🫓',
  'puri (fried bread)': '🫓',
  'lassi': '🥛',
  'idli': '🫓',
  'cassava': '🥔',
  'kava drink': '🍵',

  // ========== ACTIONS/VERBS ==========
  'to eat': '🍽️',
  'to drink': '🥤',
  'to sleep': '😴',
  'to read': '📖',
  'to read/study': '📖',
  'to write': '✍️',
  'to play': '🎮',
  'to see': '👀',
  'to listen': '👂',
  'to speak': '🗣️',
  'to walk': '🚶',
  'to run': '🏃',
  'to go': '🚶',
  'to come': '🚶',
  'to wake up': '⏰',
  'to do': '✅',

  // ========== GREETINGS & BASIC ==========
  'hello': '👋',
  'hello (formal)': '🙏',
  'hello (fijian)': '👋',
  'hello/greetings': '🙏',
  'thank you': '🙏',
  'thank you (fijian)': '🙏',
  'yes': '✅',
  'no': '❌',
  'good': '👍',
  'bad': '👎',
  'please': '🙏',
  'sorry/excuse me': '🙇',
  'goodbye': '👋',
  'welcome': '🤗',
  'how are you': '❓',
  'fine/ok': '👌',
  'see you later': '👋',
  'good morning': '🌅',
  'good night': '🌙',
  'hey!': '👋',

  // ========== TIME ==========
  'today': '📅',
  'yesterday/tomorrow': '📆',
  'morning': '🌅',
  'evening': '🌆',
  'night': '🌙',
  'week': '📅',
  'month': '📆',
  'year': '📆',

  // ========== PLACES ==========
  'home': '🏠',
  'school': '🏫',
  'temple': '🛕',
  'shop': '🏪',
  'market': '🛒',
  'village': '🏘️',
  'room': '🚪',
  'door': '🚪',
  'window': '🪟',
  'table': '🪑',
  'chair': '🪑',

  // ========== NATURE ==========
  'sun': '☀️',
  'sunshine': '☀️',
  'moon': '🌙',
  'star': '⭐',
  'cloud': '☁️',
  'rain': '🌧️',
  'wind': '💨',
  'cold': '🥶',
  'flower': '🌸',
  'tree': '🌳',

  // ========== EMOTIONS ==========
  'happy': '😊',
  'sad': '😢',
  'angry': '😠',
  'fear': '😨',
  'love': '❤️',

  // ========== SIZE/DESCRIPTION ==========
  'big': '📏',
  'small': '🤏',

  // ========== CLOTHING ==========
  'sarong/wrap': '👔',
};

/**
 * Get Twemoji image URL for a vocabulary word's English translation
 * @param translation - English translation of the word
 * @returns Twemoji CDN URL or undefined if no mapping exists
 */
export function getVocabularyImageUrl(translation: string): string | undefined {
  const normalized = translation.toLowerCase().trim();
  const emoji = VOCABULARY_EMOJI_MAP[normalized];

  if (emoji) {
    return emojiToTwemojiUrl(emoji);
  }

  // Try partial matching for compound translations
  for (const [key, emojiVal] of Object.entries(VOCABULARY_EMOJI_MAP)) {
    if (normalized.includes(key) || key.includes(normalized)) {
      return emojiToTwemojiUrl(emojiVal);
    }
  }

  return undefined;
}

/**
 * Get image URL with fallback
 * @param translation - English translation
 * @param existingUrl - Existing image URL (if any)
 * @returns Best available image URL
 */
export function getVocabularyImageWithFallback(
  translation: string,
  existingUrl?: string | null
): string {
  // First try Twemoji mapping
  const twemojiUrl = getVocabularyImageUrl(translation);
  if (twemojiUrl) {
    return twemojiUrl;
  }

  // If existing URL is valid (not picsum random), use it
  if (existingUrl && !existingUrl.includes('picsum.photos/seed/')) {
    return existingUrl;
  }

  // Default fallback - book emoji
  return emojiToTwemojiUrl('📚');
}

/**
 * Check if an image URL is a random placeholder that should be replaced
 */
export function isRandomPlaceholder(url?: string | null): boolean {
  if (!url) return true;
  return url.includes('picsum.photos/seed/');
}

const vocabularyImages = {
  getVocabularyImageUrl,
  getVocabularyImageWithFallback,
  emojiToTwemojiUrl,
  isRandomPlaceholder,
  VOCABULARY_EMOJI_MAP,
};

export default vocabularyImages;
