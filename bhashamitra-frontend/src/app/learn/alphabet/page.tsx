'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { useAuthStore } from '@/stores';
import { MainLayout } from '@/components/layout';
import { Card, Loading, ProgressBar, SpeakerButton } from '@/components/ui';
import { fadeInUp, staggerContainer } from '@/lib/constants';
import { useAudio } from '@/hooks/useAudio';

// Hindi Alphabet Data (Devanagari) with example words for Premium tier
const HINDI_VOWELS = [
  { char: 'अ', roman: 'a', sound: 'a as in about', exampleWord: 'अनार' },
  { char: 'आ', roman: 'aa', sound: 'aa as in father', exampleWord: 'आम' },
  { char: 'इ', roman: 'i', sound: 'i as in bit', exampleWord: 'इमली' },
  { char: 'ई', roman: 'ee', sound: 'ee as in feet', exampleWord: 'ईख' },
  { char: 'उ', roman: 'u', sound: 'u as in put', exampleWord: 'उल्लू' },
  { char: 'ऊ', roman: 'oo', sound: 'oo as in boot', exampleWord: 'ऊन' },
  { char: 'ए', roman: 'e', sound: 'e as in bet', exampleWord: 'एक' },
  { char: 'ऐ', roman: 'ai', sound: 'ai as in bat', exampleWord: 'ऐनक' },
  { char: 'ओ', roman: 'o', sound: 'o as in go', exampleWord: 'ओखली' },
  { char: 'औ', roman: 'au', sound: 'au as in taught', exampleWord: 'औरत' },
];

const HINDI_CONSONANTS = [
  { char: 'क', roman: 'ka', sound: 'k', exampleWord: 'कमल' },
  { char: 'ख', roman: 'kha', sound: 'kh', exampleWord: 'खरगोश' },
  { char: 'ग', roman: 'ga', sound: 'g', exampleWord: 'गाय' },
  { char: 'घ', roman: 'gha', sound: 'gh', exampleWord: 'घर' },
  { char: 'च', roman: 'cha', sound: 'ch', exampleWord: 'चम्मच' },
  { char: 'छ', roman: 'chha', sound: 'chh', exampleWord: 'छाता' },
  { char: 'ज', roman: 'ja', sound: 'j', exampleWord: 'जहाज' },
  { char: 'झ', roman: 'jha', sound: 'jh', exampleWord: 'झंडा' },
  { char: 'ट', roman: 'ta', sound: 't (hard)', exampleWord: 'टमाटर' },
  { char: 'ठ', roman: 'tha', sound: 'th (hard)', exampleWord: 'ठंड' },
  { char: 'ड', roman: 'da', sound: 'd (hard)', exampleWord: 'डमरू' },
  { char: 'ढ', roman: 'dha', sound: 'dh (hard)', exampleWord: 'ढोल' },
  { char: 'ण', roman: 'na', sound: 'n (retroflex)', exampleWord: 'बाण' },
  { char: 'त', roman: 'ta', sound: 't (soft)', exampleWord: 'तारा' },
  { char: 'थ', roman: 'tha', sound: 'th (soft)', exampleWord: 'थाली' },
  { char: 'द', roman: 'da', sound: 'd (soft)', exampleWord: 'दवाई' },
  { char: 'ध', roman: 'dha', sound: 'dh (soft)', exampleWord: 'धनुष' },
  { char: 'न', roman: 'na', sound: 'n', exampleWord: 'नल' },
  { char: 'प', roman: 'pa', sound: 'p', exampleWord: 'पतंग' },
  { char: 'फ', roman: 'pha', sound: 'ph/f', exampleWord: 'फल' },
  { char: 'ब', roman: 'ba', sound: 'b', exampleWord: 'बकरी' },
  { char: 'भ', roman: 'bha', sound: 'bh', exampleWord: 'भालू' },
  { char: 'म', roman: 'ma', sound: 'm', exampleWord: 'मछली' },
  { char: 'य', roman: 'ya', sound: 'y', exampleWord: 'यात्रा' },
  { char: 'र', roman: 'ra', sound: 'r', exampleWord: 'राजा' },
  { char: 'ल', roman: 'la', sound: 'l', exampleWord: 'लड्डू' },
  { char: 'व', roman: 'va', sound: 'v/w', exampleWord: 'वन' },
  { char: 'श', roman: 'sha', sound: 'sh', exampleWord: 'शेर' },
  { char: 'ष', roman: 'sha', sound: 'sh (retroflex)', exampleWord: 'षट्कोण' },
  { char: 'स', roman: 'sa', sound: 's', exampleWord: 'सेब' },
  { char: 'ह', roman: 'ha', sound: 'h', exampleWord: 'हाथी' },
];

// Tamil Alphabet Data with example words for Premium tier
const TAMIL_VOWELS = [
  { char: 'அ', roman: 'a', sound: 'a as in about', exampleWord: 'அம்மா' },
  { char: 'ஆ', roman: 'aa', sound: 'aa as in father', exampleWord: 'ஆடு' },
  { char: 'இ', roman: 'i', sound: 'i as in bit', exampleWord: 'இலை' },
  { char: 'ஈ', roman: 'ee', sound: 'ee as in feet', exampleWord: 'ஈ' },
  { char: 'உ', roman: 'u', sound: 'u as in put', exampleWord: 'உடல்' },
  { char: 'ஊ', roman: 'oo', sound: 'oo as in boot', exampleWord: 'ஊர்' },
  { char: 'எ', roman: 'e', sound: 'e as in bet', exampleWord: 'எலி' },
  { char: 'ஏ', roman: 'e', sound: 'e as in they', exampleWord: 'ஏர்' },
  { char: 'ஐ', roman: 'ai', sound: 'ai as in aisle', exampleWord: 'ஐந்து' },
  { char: 'ஒ', roman: 'o', sound: 'o as in go', exampleWord: 'ஒட்டகம்' },
  { char: 'ஓ', roman: 'o', sound: 'o as in boat', exampleWord: 'ஓடு' },
  { char: 'ஔ', roman: 'au', sound: 'au as in house', exampleWord: 'ஔவை' },
];

const TAMIL_CONSONANTS = [
  { char: 'க', roman: 'ka', sound: 'k/g', exampleWord: 'கல்' },
  { char: 'ங', roman: 'nga', sound: 'ng', exampleWord: 'அங்கு' },
  { char: 'ச', roman: 'cha', sound: 'ch/s', exampleWord: 'சோறு' },
  { char: 'ஞ', roman: 'nya', sound: 'ny', exampleWord: 'ஞானம்' },
  { char: 'ட', roman: 'ta', sound: 't (hard)', exampleWord: 'டம்' },
  { char: 'ண', roman: 'na', sound: 'n (retroflex)', exampleWord: 'பண்' },
  { char: 'த', roman: 'tha', sound: 'th', exampleWord: 'தண்ணீர்' },
  { char: 'ந', roman: 'na', sound: 'n', exampleWord: 'நல்ல' },
  { char: 'ப', roman: 'pa', sound: 'p/b', exampleWord: 'பல்' },
  { char: 'ம', roman: 'ma', sound: 'm', exampleWord: 'மலை' },
  { char: 'ய', roman: 'ya', sound: 'y', exampleWord: 'யானை' },
  { char: 'ர', roman: 'ra', sound: 'r', exampleWord: 'ரோஜா' },
  { char: 'ல', roman: 'la', sound: 'l', exampleWord: 'லட்டு' },
  { char: 'வ', roman: 'va', sound: 'v/w', exampleWord: 'வாழை' },
  { char: 'ழ', roman: 'zha', sound: 'zh (retroflex)', exampleWord: 'தமிழ்' },
  { char: 'ள', roman: 'la', sound: 'l (retroflex)', exampleWord: 'வள்' },
  { char: 'ற', roman: 'ra', sound: 'r (hard)', exampleWord: 'பறவை' },
  { char: 'ன', roman: 'na', sound: 'n (alveolar)', exampleWord: 'பனி' },
];

export default function AlphabetPage() {
  const router = useRouter();
  const [isHydrated, setIsHydrated] = useState(false);
  const [selectedLetter, setSelectedLetter] = useState<typeof HINDI_VOWELS[0] | null>(null);
  const [activeTab, setActiveTab] = useState<'vowels' | 'consonants'>('vowels');
  const { isAuthenticated, user, activeChild } = useAuthStore();

  // Get current language from active child, default to Hindi
  // Handle both string and object formats from API
  const currentLanguage = activeChild?.language
    ? (typeof activeChild.language === 'string' ? activeChild.language : activeChild.language.code)
    : 'HINDI';

  // Select alphabet data based on language
  const VOWELS = currentLanguage === 'TAMIL' ? TAMIL_VOWELS : HINDI_VOWELS;
  const CONSONANTS = currentLanguage === 'TAMIL' ? TAMIL_CONSONANTS : HINDI_CONSONANTS;

  // Language-specific metadata
  const languageMetadata = {
    HINDI: {
      title: 'Hindi Alphabet',
      subtitle: 'देवनागरी वर्णमाला - Devanagari Script',
      vowelLabel: 'Vowels (स्वर)',
      consonantLabel: 'Consonants (व्यंजन)',
      totalLetters: 41,
      gradientClass: 'from-orange-50 to-red-50',
      primaryColor: 'orange-500',
    },
    TAMIL: {
      title: 'Tamil Alphabet',
      subtitle: 'தமிழ் எழுத்துக்கள் - Tamil Script',
      vowelLabel: 'Vowels (உயிர்)',
      consonantLabel: 'Consonants (மெய்)',
      totalLetters: 30,
      gradientClass: 'from-blue-50 to-indigo-50',
      primaryColor: 'blue-500',
    },
  };

  const metadata = languageMetadata[currentLanguage as keyof typeof languageMetadata] || languageMetadata.HINDI;

  // Check if user is Premium tier for enhanced audio
  const isPremium = user?.subscription_tier === 'PREMIUM';

  // Audio playback hook
  const { isPlaying, isLoading, playAudio, stopAudio, error: audioError } = useAudio({
    language: currentLanguage,
    voiceStyle: 'kid_friendly',
  });

  // Handle playing letter audio
  // Premium users hear "letter + connector + exampleWord" in the appropriate language
  // Other tiers hear just the letter
  const handlePlayLetter = (letter: typeof VOWELS[0], e?: React.MouseEvent) => {
    if (e) {
      e.stopPropagation(); // Prevent opening modal when clicking speaker
    }
    if (isPlaying) {
      stopAudio();
    } else {
      // Construct text based on subscription tier and language
      let textToSpeak = letter.char;
      if (isPremium && letter.exampleWord) {
        // Use language-appropriate connector
        if (currentLanguage === 'TAMIL') {
          // Tamil: "க, உதாரணமாக கல்" (letter, for example, word)
          textToSpeak = `${letter.char}, உதாரணமாக ${letter.exampleWord}`;
        } else {
          // Hindi: "अ से अनार" (letter se word)
          textToSpeak = `${letter.char} से ${letter.exampleWord}`;
        }
      }
      playAudio(textToSpeak);
    }
  };

  useEffect(() => {
    setIsHydrated(true);
  }, []);

  useEffect(() => {
    if (!isHydrated) return;
    if (!isAuthenticated) {
      router.push('/login');
    }
  }, [isHydrated, isAuthenticated, router]);

  if (!isHydrated || !isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <Loading size="lg" text="Loading..." />
      </div>
    );
  }

  const letters = activeTab === 'vowels' ? VOWELS : CONSONANTS;

  return (
    <MainLayout>
      <motion.div
        variants={staggerContainer}
        initial="initial"
        animate="animate"
        className="space-y-6"
      >
        {/* Header */}
        <motion.div variants={fadeInUp} className="flex items-center gap-3">
          <Link href="/learn" className="text-gray-400 hover:text-gray-600">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </Link>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{metadata.title}</h1>
            <p className="text-gray-500">{metadata.subtitle}</p>
          </div>
        </motion.div>

        {/* Progress */}
        <motion.div variants={fadeInUp}>
          <Card className={`bg-gradient-to-r ${metadata.gradientClass}`}>
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-700">Your Progress</span>
              <span className={currentLanguage === 'TAMIL' ? 'text-sm text-blue-500' : 'text-sm text-orange-500'}>
                0 / {metadata.totalLetters} letters
              </span>
            </div>
            <ProgressBar value={0} variant="primary" />
          </Card>
        </motion.div>

        {/* Tabs */}
        <motion.div variants={fadeInUp} className="flex gap-2">
          <button
            onClick={() => setActiveTab('vowels')}
            className={`flex-1 py-3 px-4 rounded-xl font-medium transition-colors ${
              activeTab === 'vowels'
                ? currentLanguage === 'TAMIL'
                  ? 'bg-blue-500 text-white'
                  : 'bg-orange-500 text-white'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            {metadata.vowelLabel}
            <span className="ml-2 text-sm opacity-80">{VOWELS.length}</span>
          </button>
          <button
            onClick={() => setActiveTab('consonants')}
            className={`flex-1 py-3 px-4 rounded-xl font-medium transition-colors ${
              activeTab === 'consonants'
                ? currentLanguage === 'TAMIL'
                  ? 'bg-blue-500 text-white'
                  : 'bg-orange-500 text-white'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            {metadata.consonantLabel}
            <span className="ml-2 text-sm opacity-80">{CONSONANTS.length}</span>
          </button>
        </motion.div>

        {/* Selected Letter Detail */}
        {selectedLetter && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
            onClick={() => setSelectedLetter(null)}
          >
            <Card className="w-full max-w-sm bg-white" onClick={(e) => e.stopPropagation()}>
              <div className="text-center">
                <p className={currentLanguage === 'TAMIL' ? 'text-8xl font-bold text-blue-500 mb-4' : 'text-8xl font-bold text-orange-500 mb-4'}>
                  {selectedLetter.char}
                </p>
                <p className="text-2xl text-gray-700 mb-2">{selectedLetter.roman}</p>
                <p className="text-gray-500 mb-2">{selectedLetter.sound}</p>

                {/* Show example word for Premium users */}
                {isPremium && selectedLetter.exampleWord && (
                  <div className="bg-gradient-to-r from-amber-50 to-yellow-50 rounded-lg px-4 py-2 mb-4">
                    <p className="text-sm text-amber-600 font-medium">
                      {currentLanguage === 'TAMIL'
                        ? `${selectedLetter.char}, உதாரணமாக ${selectedLetter.exampleWord}`
                        : `${selectedLetter.char} से ${selectedLetter.exampleWord}`
                      }
                    </p>
                    <p className="text-xs text-amber-500">
                      {currentLanguage === 'TAMIL'
                        ? 'பிரீமியம்: உதாரணத்துடன் கேளுங்கள்'
                        : 'Premium: Hear with example'
                      }
                    </p>
                  </div>
                )}

                {/* Listen to pronunciation button */}
                <div className="flex flex-col items-center gap-3 mb-4">
                  <SpeakerButton
                    isPlaying={isPlaying}
                    isLoading={isLoading}
                    onClick={() => handlePlayLetter(selectedLetter)}
                    size="lg"
                  />
                  <span className="text-sm text-gray-500">
                    {isLoading ? 'Loading...' : isPlaying ? 'Playing...' : 'Tap to hear'}
                  </span>
                  {audioError && (
                    <span className="text-xs text-red-500">{audioError}</span>
                  )}
                </div>

                <button
                  onClick={() => {
                    stopAudio();
                    setSelectedLetter(null);
                  }}
                  className={currentLanguage === 'TAMIL'
                    ? 'mt-2 px-6 py-2 bg-blue-500 text-white rounded-xl font-medium hover:opacity-90 transition-colors'
                    : 'mt-2 px-6 py-2 bg-orange-500 text-white rounded-xl font-medium hover:opacity-90 transition-colors'
                  }
                >
                  Close
                </button>
              </div>
            </Card>
          </motion.div>
        )}

        {/* Letters Grid */}
        <motion.div variants={fadeInUp}>
          <h2 className="text-lg font-bold text-gray-900 mb-4">
            {activeTab === 'vowels' ? metadata.vowelLabel : metadata.consonantLabel}
          </h2>
          <div className="grid grid-cols-5 gap-2">
            {letters.map((letter, index) => (
              <motion.button
                key={letter.char}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.02 }}
                onClick={() => setSelectedLetter(letter)}
                className={`relative aspect-square bg-gradient-to-br ${
                  currentLanguage === 'TAMIL'
                    ? 'from-blue-100 to-indigo-100 hover:from-blue-200 hover:to-indigo-200'
                    : 'from-orange-100 to-red-100 hover:from-orange-200 hover:to-red-200'
                } rounded-xl flex flex-col items-center justify-center transition-colors shadow-sm hover:shadow-md`}
              >
                {/* Audio indicator */}
                <div className="absolute top-1 right-1">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                    className="w-3 h-3 text-purple-400"
                  >
                    <path d="M10 3.75a.75.75 0 00-1.264-.546L4.703 7H3.167a.75.75 0 00-.7.48A6.985 6.985 0 002 10c0 .887.165 1.737.468 2.52.111.29.39.48.7.48h1.535l4.033 3.796A.75.75 0 0010 16.25V3.75zM15.95 5.05a.75.75 0 00-1.06 1.061 5.5 5.5 0 010 7.778.75.75 0 001.06 1.06 7 7 0 000-9.899z" />
                    <path d="M13.829 7.172a.75.75 0 00-1.061 1.06 2.5 2.5 0 010 3.536.75.75 0 001.06 1.06 4 4 0 000-5.656z" />
                  </svg>
                </div>
                <span className="text-2xl font-bold text-gray-800">{letter.char}</span>
                <span className="text-xs text-gray-500">{letter.roman}</span>
              </motion.button>
            ))}
          </div>
        </motion.div>

        {/* Learning Tip */}
        <motion.div variants={fadeInUp}>
          <Card className="bg-yellow-50 border-2 border-yellow-200">
            <div className="flex items-start gap-3">
              <span className="text-2xl">🔊</span>
              <div>
                <h3 className="font-bold text-yellow-800">Listen & Learn!</h3>
                <p className="text-sm text-yellow-700 mt-1">
                  Tap any letter to see details, then tap the speaker button to hear the correct pronunciation!
                </p>
              </div>
            </div>
          </Card>
        </motion.div>
      </motion.div>
    </MainLayout>
  );
}
