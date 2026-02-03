'use client';

import { useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Delete, Globe } from 'lucide-react';
import { cn } from '@/lib/utils';

type LanguageCode = 'HINDI' | 'TAMIL' | 'TELUGU' | 'GUJARATI' | 'PUNJABI' | 'BENGALI' | 'MALAYALAM';

interface KeyboardLayout {
  vowels: string[];
  consonants: string[][];
  matras: string[];
  numbers: string[];
  punctuation: string[];
}

// Keyboard layouts for different Indian languages
const KEYBOARD_LAYOUTS: Record<LanguageCode, KeyboardLayout> = {
  HINDI: {
    vowels: ['अ', 'आ', 'इ', 'ई', 'उ', 'ऊ', 'ऋ', 'ए', 'ऐ', 'ओ', 'औ', 'अं', 'अः'],
    consonants: [
      ['क', 'ख', 'ग', 'घ', 'ङ'],
      ['च', 'छ', 'ज', 'झ', 'ञ'],
      ['ट', 'ठ', 'ड', 'ढ', 'ण'],
      ['त', 'थ', 'द', 'ध', 'न'],
      ['प', 'फ', 'ब', 'भ', 'म'],
      ['य', 'र', 'ल', 'व', 'श', 'ष', 'स', 'ह'],
    ],
    matras: ['ा', 'ि', 'ी', 'ु', 'ू', 'ृ', 'े', 'ै', 'ो', 'ौ', 'ं', 'ः', '्'],
    numbers: ['०', '१', '२', '३', '४', '५', '६', '७', '८', '९'],
    punctuation: ['।', '॥', ',', '.', '?', '!', '-', ' '],
  },
  TAMIL: {
    vowels: ['அ', 'ஆ', 'இ', 'ஈ', 'உ', 'ஊ', 'எ', 'ஏ', 'ஐ', 'ஒ', 'ஓ', 'ஔ'],
    consonants: [
      ['க', 'ங', 'ச', 'ஞ', 'ட'],
      ['ண', 'த', 'ந', 'ப', 'ம'],
      ['ய', 'ர', 'ல', 'வ', 'ழ'],
      ['ள', 'ற', 'ன', 'ஜ', 'ஷ'],
      ['ஸ', 'ஹ', 'க்ஷ', 'ஶ்ரீ'],
    ],
    matras: ['ா', 'ி', 'ீ', 'ு', 'ூ', 'ெ', 'ே', 'ை', 'ொ', 'ோ', 'ௌ', '்'],
    numbers: ['௦', '௧', '௨', '௩', '௪', '௫', '௬', '௭', '௮', '௯'],
    punctuation: [',', '.', '?', '!', '-', ' '],
  },
  TELUGU: {
    vowels: ['అ', 'ఆ', 'ఇ', 'ఈ', 'ఉ', 'ఊ', 'ఋ', 'ఎ', 'ఏ', 'ఐ', 'ఒ', 'ఓ', 'ఔ'],
    consonants: [
      ['క', 'ఖ', 'గ', 'ఘ', 'ఙ'],
      ['చ', 'ఛ', 'జ', 'ఝ', 'ఞ'],
      ['ట', 'ఠ', 'డ', 'ఢ', 'ణ'],
      ['త', 'థ', 'ద', 'ధ', 'న'],
      ['ప', 'ఫ', 'బ', 'భ', 'మ'],
      ['య', 'ర', 'ల', 'వ', 'శ', 'ష', 'స', 'హ'],
    ],
    matras: ['ా', 'ి', 'ీ', 'ు', 'ూ', 'ృ', 'ె', 'ే', 'ై', 'ొ', 'ో', 'ౌ', '్'],
    numbers: ['౦', '౧', '౨', '౩', '౪', '౫', '౬', '౭', '౮', '౯'],
    punctuation: [',', '.', '?', '!', '-', ' '],
  },
  GUJARATI: {
    vowels: ['અ', 'આ', 'ઇ', 'ઈ', 'ઉ', 'ઊ', 'ઋ', 'એ', 'ઐ', 'ઓ', 'ઔ'],
    consonants: [
      ['ક', 'ખ', 'ગ', 'ઘ', 'ઙ'],
      ['ચ', 'છ', 'જ', 'ઝ', 'ઞ'],
      ['ટ', 'ઠ', 'ડ', 'ઢ', 'ણ'],
      ['ત', 'થ', 'દ', 'ધ', 'ન'],
      ['પ', 'ફ', 'બ', 'ભ', 'મ'],
      ['ય', 'ર', 'લ', 'વ', 'શ', 'ષ', 'સ', 'હ'],
    ],
    matras: ['ા', 'િ', 'ી', 'ુ', 'ૂ', 'ૃ', 'ે', 'ૈ', 'ો', 'ૌ', 'ં', 'ઃ', '્'],
    numbers: ['૦', '૧', '૨', '૩', '૪', '૫', '૬', '૭', '૮', '૯'],
    punctuation: [',', '.', '?', '!', '-', ' '],
  },
  PUNJABI: {
    vowels: ['ੳ', 'ਅ', 'ੲ', 'ਆ', 'ਇ', 'ਈ', 'ਉ', 'ਊ', 'ਏ', 'ਐ', 'ਓ', 'ਔ'],
    consonants: [
      ['ਸ', 'ਹ', 'ਕ', 'ਖ', 'ਗ', 'ਘ', 'ਙ'],
      ['ਚ', 'ਛ', 'ਜ', 'ਝ', 'ਞ', 'ਟ', 'ਠ'],
      ['ਡ', 'ਢ', 'ਣ', 'ਤ', 'ਥ', 'ਦ', 'ਧ'],
      ['ਨ', 'ਪ', 'ਫ', 'ਬ', 'ਭ', 'ਮ', 'ਯ'],
      ['ਰ', 'ਲ', 'ਵ', 'ੜ', 'ਸ਼', 'ਖ਼', 'ਗ਼'],
      ['ਜ਼', 'ਫ਼', 'ਲ਼', 'ੴ'],
    ],
    matras: ['ਾ', 'ਿ', 'ੀ', 'ੁ', 'ੂ', 'ੇ', 'ੈ', 'ੋ', 'ੌ', '੍', 'ੰ', 'ੱ', 'ਂ'],
    numbers: ['੦', '੧', '੨', '੩', '੪', '੫', '੬', '੭', '੮', '੯'],
    punctuation: ['।', '॥', ',', '.', '?', '!', '-', ' '],
  },
  BENGALI: {
    vowels: ['অ', 'আ', 'ই', 'ঈ', 'উ', 'ঊ', 'ঋ', 'এ', 'ঐ', 'ও', 'ঔ'],
    consonants: [
      ['ক', 'খ', 'গ', 'ঘ', 'ঙ'],
      ['চ', 'ছ', 'জ', 'ঝ', 'ঞ'],
      ['ট', 'ঠ', 'ড', 'ঢ', 'ণ'],
      ['ত', 'থ', 'দ', 'ধ', 'ন'],
      ['প', 'ফ', 'ব', 'ভ', 'ম'],
      ['য', 'র', 'ল', 'শ', 'ষ', 'স', 'হ'],
    ],
    matras: ['া', 'ি', 'ী', 'ু', 'ূ', 'ৃ', 'ে', 'ৈ', 'ো', 'ৌ', 'ং', 'ঃ', '্'],
    numbers: ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯'],
    punctuation: [',', '.', '?', '!', '-', ' '],
  },
  MALAYALAM: {
    vowels: ['അ', 'ആ', 'ഇ', 'ഈ', 'ഉ', 'ഊ', 'ഋ', 'എ', 'ഏ', 'ഐ', 'ഒ', 'ഓ', 'ഔ'],
    consonants: [
      ['ക', 'ഖ', 'ഗ', 'ഘ', 'ങ'],
      ['ച', 'ഛ', 'ജ', 'ഝ', 'ഞ'],
      ['ട', 'ഠ', 'ഡ', 'ഢ', 'ണ'],
      ['ത', 'ഥ', 'ദ', 'ധ', 'ന'],
      ['പ', 'ഫ', 'ബ', 'ഭ', 'മ'],
      ['യ', 'ര', 'ല', 'വ', 'ശ', 'ഷ', 'സ', 'ഹ'],
    ],
    matras: ['ാ', 'ി', 'ീ', 'ു', 'ൂ', 'ൃ', 'െ', 'േ', 'ൈ', 'ൊ', 'ോ', 'ൌ', '്'],
    numbers: ['൦', '൧', '൨', '൩', '൪', '൫', '൬', '൭', '൮', '൯'],
    punctuation: [',', '.', '?', '!', '-', ' '],
  },
};

const LANGUAGE_NAMES: Record<LanguageCode, { english: string; native: string }> = {
  HINDI: { english: 'Hindi', native: 'हिंदी' },
  TAMIL: { english: 'Tamil', native: 'தமிழ்' },
  TELUGU: { english: 'Telugu', native: 'తెలుగు' },
  GUJARATI: { english: 'Gujarati', native: 'ગુજરાતી' },
  PUNJABI: { english: 'Punjabi', native: 'ਪੰਜਾਬੀ' },
  BENGALI: { english: 'Bengali', native: 'বাংলা' },
  MALAYALAM: { english: 'Malayalam', native: 'മലയാളം' },
};

type KeyboardTab = 'vowels' | 'consonants' | 'matras' | 'numbers';

interface IndianLanguageKeyboardProps {
  language: LanguageCode;
  onInput: (char: string) => void;
  onDelete: () => void;
  onClose?: () => void;
  onLanguageChange?: (lang: LanguageCode) => void;
  onPlaySound?: (char: string) => void;
  isOpen?: boolean;
  className?: string;
}

export function IndianLanguageKeyboard({
  language,
  onInput,
  onDelete,
  onClose,
  onLanguageChange,
  onPlaySound,
  isOpen = true,
  className,
}: IndianLanguageKeyboardProps) {
  const [activeTab, setActiveTab] = useState<KeyboardTab>('consonants');
  const [showLanguageMenu, setShowLanguageMenu] = useState(false);

  const layout = KEYBOARD_LAYOUTS[language] || KEYBOARD_LAYOUTS.HINDI;
  const langInfo = LANGUAGE_NAMES[language] || LANGUAGE_NAMES.HINDI;

  const handleKeyPress = useCallback((char: string) => {
    onInput(char);
    if (onPlaySound) {
      onPlaySound(char);
    }
  }, [onInput, onPlaySound]);

  const tabs: { id: KeyboardTab; label: string; labelNative: string }[] = [
    { id: 'consonants', label: 'Consonants', labelNative: language === 'HINDI' ? 'व्यंजन' : 'Consonants' },
    { id: 'vowels', label: 'Vowels', labelNative: language === 'HINDI' ? 'स्वर' : 'Vowels' },
    { id: 'matras', label: 'Matras', labelNative: language === 'HINDI' ? 'मात्राएँ' : 'Matras' },
    { id: 'numbers', label: 'Numbers', labelNative: language === 'HINDI' ? 'अंक' : 'Numbers' },
  ];

  const renderKeys = () => {
    switch (activeTab) {
      case 'vowels':
        return (
          <div className="flex flex-wrap justify-center gap-1.5 p-2">
            {layout.vowels.map((char, i) => (
              <KeyButton key={i} char={char} onClick={() => handleKeyPress(char)} />
            ))}
          </div>
        );

      case 'consonants':
        return (
          <div className="space-y-1.5 p-2">
            {layout.consonants.map((row, rowIndex) => (
              <div key={rowIndex} className="flex justify-center gap-1.5">
                {row.map((char, i) => (
                  <KeyButton key={i} char={char} onClick={() => handleKeyPress(char)} />
                ))}
              </div>
            ))}
          </div>
        );

      case 'matras':
        return (
          <div className="flex flex-wrap justify-center gap-1.5 p-2">
            {layout.matras.map((char, i) => (
              <KeyButton
                key={i}
                char={char}
                onClick={() => handleKeyPress(char)}
                isMatra
              />
            ))}
          </div>
        );

      case 'numbers':
        return (
          <div className="space-y-2 p-2">
            <div className="flex flex-wrap justify-center gap-1.5">
              {layout.numbers.map((char, i) => (
                <KeyButton key={i} char={char} onClick={() => handleKeyPress(char)} />
              ))}
            </div>
            <div className="flex flex-wrap justify-center gap-1.5 pt-2 border-t border-gray-200">
              {layout.punctuation.map((char, i) => (
                <KeyButton
                  key={i}
                  char={char === ' ' ? '⎵' : char}
                  displayChar={char === ' ' ? 'Space' : char}
                  onClick={() => handleKeyPress(char)}
                  wide={char === ' '}
                />
              ))}
            </div>
          </div>
        );
    }
  };

  if (!isOpen) return null;

  return (
    <motion.div
      initial={{ y: 300, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      exit={{ y: 300, opacity: 0 }}
      className={cn(
        'bg-gray-100 rounded-t-3xl shadow-2xl border-t border-gray-200',
        className
      )}
    >
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-2 border-b border-gray-200">
        <button
          onClick={() => setShowLanguageMenu(!showLanguageMenu)}
          className="flex items-center gap-2 px-3 py-1.5 bg-white rounded-full shadow-sm hover:bg-gray-50"
        >
          <Globe size={16} className="text-indigo-500" />
          <span className="text-sm font-medium">{langInfo.native}</span>
        </button>

        <div className="flex items-center gap-2">
          <button
            onClick={onDelete}
            className="p-2 bg-white rounded-full shadow-sm hover:bg-red-50 active:bg-red-100"
          >
            <Delete size={20} className="text-red-500" />
          </button>
          {onClose && (
            <button
              onClick={onClose}
              className="p-2 bg-white rounded-full shadow-sm hover:bg-gray-50"
            >
              <X size={20} className="text-gray-500" />
            </button>
          )}
        </div>
      </div>

      {/* Language Menu */}
      <AnimatePresence>
        {showLanguageMenu && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="overflow-hidden bg-white border-b border-gray-200"
          >
            <div className="grid grid-cols-3 gap-2 p-3">
              {(Object.keys(LANGUAGE_NAMES) as LanguageCode[]).map((lang) => (
                <button
                  key={lang}
                  onClick={() => {
                    onLanguageChange?.(lang);
                    setShowLanguageMenu(false);
                  }}
                  className={cn(
                    'p-2 rounded-xl text-center transition-all',
                    language === lang
                      ? 'bg-indigo-100 border-2 border-indigo-500'
                      : 'bg-gray-50 hover:bg-gray-100 border-2 border-transparent'
                  )}
                >
                  <p className="font-medium text-gray-900">{LANGUAGE_NAMES[lang].native}</p>
                  <p className="text-xs text-gray-500">{LANGUAGE_NAMES[lang].english}</p>
                </button>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Tabs */}
      <div className="flex border-b border-gray-200 bg-white">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={cn(
              'flex-1 py-2 text-center text-sm font-medium transition-colors',
              activeTab === tab.id
                ? 'text-indigo-600 border-b-2 border-indigo-600 bg-indigo-50'
                : 'text-gray-500 hover:text-gray-700'
            )}
          >
            {tab.labelNative}
          </button>
        ))}
      </div>

      {/* Keys */}
      <div className="min-h-[180px]">
        {renderKeys()}
      </div>
    </motion.div>
  );
}

interface KeyButtonProps {
  char: string;
  displayChar?: string;
  onClick: () => void;
  isMatra?: boolean;
  wide?: boolean;
}

function KeyButton({ char, displayChar, onClick, isMatra, wide }: KeyButtonProps) {
  return (
    <motion.button
      whileTap={{ scale: 0.9 }}
      onClick={onClick}
      className={cn(
        'flex items-center justify-center rounded-xl font-bold shadow-sm transition-all',
        'bg-white hover:bg-indigo-50 active:bg-indigo-100 border border-gray-200',
        isMatra
          ? 'w-10 h-10 text-lg text-indigo-600'
          : wide
            ? 'px-6 h-10 text-sm'
            : 'w-10 h-10 text-xl text-gray-800'
      )}
    >
      {isMatra ? (
        <span className="relative">
          <span className="opacity-40">क</span>
          <span className="absolute inset-0 flex items-center justify-center text-indigo-600">{char}</span>
        </span>
      ) : (
        displayChar || char
      )}
    </motion.button>
  );
}

export default IndianLanguageKeyboard;
