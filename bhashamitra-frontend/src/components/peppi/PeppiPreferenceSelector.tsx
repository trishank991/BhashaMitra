'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { PeppiAvatar } from './PeppiAvatar';
import type { PeppiAddressing, PeppiGender, LanguageCode } from '@/types';
import { cn } from '@/lib/utils';

interface PeppiPreferenceSelectorProps {
  childId: string;
  currentAddressing: PeppiAddressing;
  currentGender: PeppiGender;
  language: LanguageCode;
  childName: string;
  onUpdate: (addressing: PeppiAddressing, gender: PeppiGender) => void;
}

// Preview messages for each language
const PREVIEW_MESSAGES: Record<LanguageCode, { byName: string; cultural: { male: string; female: string } }> = {
  HINDI: {
    byName: 'नमस्ते {name}! आज हम कहानी सुनेंगे।',
    cultural: {
      male: 'नमस्ते भैया! आज हम कहानी सुनेंगे।',
      female: 'नमस्ते दीदी! आज हम कहानी सुनेंगे।',
    },
  },
  TAMIL: {
    byName: 'வணக்கம் {name}! இன்று நாம் கதை கேட்போம்.',
    cultural: {
      male: 'வணக்கம் அண்ணா! இன்று நாம் கதை கேட்போம்.',
      female: 'வணக்கம் அக்கா! இன்று நாம் கதை கேட்போம்.',
    },
  },
  TELUGU: {
    byName: 'నమస్కారం {name}! ఈరోజు మనం కథ వింటాం.',
    cultural: {
      male: 'నమస్కారం అన్న! ఈరోజు మనం కథ వింటాం.',
      female: 'నమస్కారం అక్క! ఈరోజు మనం కథ వింటాం.',
    },
  },
  GUJARATI: {
    byName: 'નમસ્તે {name}! આજે આપણે વાર્તા સાંભળીશું.',
    cultural: {
      male: 'નમસ્તે ભાઈ! આજે આપણે વાર્તા સાંભળીશું.',
      female: 'નમસ્તે બેન! આજે આપણે વાર્તા સાંભળીશું.',
    },
  },
  PUNJABI: {
    byName: 'ਸਤ ਸ੍ਰੀ ਅਕਾਲ {name}! ਅੱਜ ਅਸੀਂ ਕਹਾਣੀ ਸੁਣਾਂਗੇ।',
    cultural: {
      male: 'ਸਤ ਸ੍ਰੀ ਅਕਾਲ ਵੀਰਜੀ! ਅੱਜ ਅਸੀਂ ਕਹਾਣੀ ਸੁਣਾਂਗੇ।',
      female: 'ਸਤ ਸ੍ਰੀ ਅਕਾਲ ਭੈਣਜੀ! ਅੱਜ ਅਸੀਂ ਕਹਾਣੀ ਸੁਣਾਂਗੇ।',
    },
  },
  MALAYALAM: {
    byName: 'നമസ്കാരം {name}! ഇന്ന് നമുക്ക് കഥ കേൾക്കാം.',
    cultural: {
      male: 'നമസ്കാരം ചേട്ടാ! ഇന്ന് നമുക്ക് കഥ കേൾക്കാം.',
      female: 'നമസ്കാരം ചേച്ചി! ഇന്ന് നമുക്ക് കഥ കേൾക്കാം.',
    },
  },
  BENGALI: {
    byName: 'নমস্কার {name}! আজ আমরা গল্প শুনব।',
    cultural: {
      male: 'নমস্কার দাদা! আজ আমরা গল্প শুনব।',
      female: 'নমস্কার দিদি! আজ আমরা গল্প শুনব।',
    },
  },
  MARATHI: {
    byName: 'नमस्कार {name}! आज आपण गोष्ट ऐकू.',
    cultural: {
      male: 'नमस्कार भाऊ! आज आपण गोष्ट ऐकू.',
      female: 'नमस्कार ताई! आज आपण गोष्ट ऐकू.',
    },
  },
  KANNADA: {
    byName: 'ನಮಸ್ಕಾರ {name}! ಇಂದು ನಾವು ಕಥೆ ಕೇಳೋಣ.',
    cultural: {
      male: 'ನಮಸ್ಕಾರ ಅಣ್ಣಾ! ಇಂದು ನಾವು ಕಥೆ ಕೇಳೋಣ.',
      female: 'ನಮಸ್ಕಾರ ಅಕ್ಕಾ! ಇಂದು ನಾವು ಕಥೆ ಕೇಳೋಣ.',
    },
  },
  ODIA: {
    byName: 'ନମସ୍କାର {name}! ଆଜି ଆମେ କାହାଣୀ ଶୁଣିବା.',
    cultural: {
      male: 'ନମସ୍କାର ଭାଇ! ଆଜି ଆମେ କାହାଣୀ ଶୁଣିବା.',
      female: 'ନମସ୍କାର ଭଉଣୀ! ଆଜି ଆମେ କାହାଣୀ ଶୁଣିବା.',
    },
  },
  ASSAMESE: {
    byName: 'নমস্কাৰ {name}! আজি আমি গল্প শুনিম।',
    cultural: {
      male: 'নমস্কাৰ ভাইটী! আজি আমি গল্প শুনিম।',
      female: 'নমস্কাৰ বহিনী! আজি আমি গল্প শুনিম।',
    },
  },
  URDU: {
    byName: 'السلام علیکم {name}! آج ہم کہانی سنیں گے۔',
    cultural: {
      male: 'السلام علیکم بھائی! آج ہم کہانی سنیں گے۔',
      female: 'السلام علیکم آپا! آج ہم کہانی سنیں گے۔',
    },
  },
};

// Gender label translations
const GENDER_LABELS: Record<LanguageCode, { male: string; female: string }> = {
  HINDI: { male: 'पेप्पी भैया (लड़का)', female: 'पेप्पी दीदी (लड़की)' },
  TAMIL: { male: 'பெப்பி அண்ணா (ஆண்)', female: 'பெப்பி அக்கா (பெண்)' },
  TELUGU: { male: 'పెప్పి అన్న (అబ్బాయి)', female: 'పెప్పి అక్క (అమ్మాయి)' },
  GUJARATI: { male: 'પેપ્પી ભાઈ (છોકરો)', female: 'પેપ્પી બેન (છોકરી)' },
  PUNJABI: { male: 'ਪੈਪੀ ਵੀਰਜੀ (ਮੁੰਡਾ)', female: 'ਪੈਪੀ ਭੈਣਜੀ (ਕੁੜੀ)' },
  MALAYALAM: { male: 'Peppi Chettan (Boy)', female: 'Peppi Chechi (Girl)' },
  BENGALI: { male: 'Peppi Dada (ছেলে)', female: 'Peppi Didi (মেয়ে)' },
  MARATHI: { male: 'पेप्पी भाऊ (मुलगा)', female: 'पेप्पी ताई (मुलगी)' },
  KANNADA: { male: 'Peppi Anna (ಹುಡುಗ)', female: 'Peppi Akka (ಹುಡುಗಿ)' },
  ODIA: { male: 'Peppi Bhai (ପୁଅ)', female: 'Peppi Bhauni (ଝିଅ)' },
  ASSAMESE: { male: 'Peppi Bhaiti (ল\'ৰা)', female: 'Peppi Bahini (ছোৱালী)' },
  URDU: { male: 'پیپی بھائی (لڑکا)', female: 'پیپی آپا (لڑکی)' },
};

export function PeppiPreferenceSelector({
  childId: _childId,
  currentAddressing,
  currentGender,
  language,
  childName,
  onUpdate,
}: PeppiPreferenceSelectorProps) {
  // childId available for future API integration
  void _childId;
  const [addressing, setAddressing] = useState<PeppiAddressing>(currentAddressing);
  const [gender, setGender] = useState<PeppiGender>(currentGender);
  const [isSaving, setIsSaving] = useState(false);

  const handleSave = async () => {
    setIsSaving(true);
    try {
      await onUpdate(addressing, gender);
    } finally {
      setIsSaving(false);
    }
  };

  const hasChanges = addressing !== currentAddressing || gender !== currentGender;

  // Get preview message
  const previewMessage =
    addressing === 'BY_NAME'
      ? PREVIEW_MESSAGES[language]?.byName.replace('{name}', childName) || `Hello ${childName}! Let's listen to a story today.`
      : PREVIEW_MESSAGES[language]?.cultural[gender] || `Hello! Let's listen to a story today.`;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center">
        <PeppiAvatar size="lg" showBubble={false} className="mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Customize Peppi</h2>
        <p className="text-gray-600">Choose how Peppi should talk to you</p>
      </div>

      {/* Addressing Preference */}
      <div className="space-y-3">
        <label className="block text-sm font-medium text-gray-700">
          How should Peppi address you?
        </label>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <button
            onClick={() => setAddressing('BY_NAME')}
            className={cn(
              "p-4 rounded-xl border-2 transition-all text-left",
              addressing === 'BY_NAME'
                ? "border-purple-500 bg-purple-50"
                : "border-gray-200 hover:border-purple-300"
            )}
          >
            <div className="flex items-center gap-2 mb-2">
              <div className={cn(
                "w-5 h-5 rounded-full border-2 flex items-center justify-center",
                addressing === 'BY_NAME' ? "border-purple-500" : "border-gray-300"
              )}>
                {addressing === 'BY_NAME' && (
                  <div className="w-3 h-3 rounded-full bg-purple-500" />
                )}
              </div>
              <span className="font-semibold text-gray-900">By Name</span>
            </div>
            <p className="text-sm text-gray-600">
              Peppi will call you by your name
            </p>
          </button>

          <button
            onClick={() => setAddressing('CULTURAL')}
            className={cn(
              "p-4 rounded-xl border-2 transition-all text-left",
              addressing === 'CULTURAL'
                ? "border-purple-500 bg-purple-50"
                : "border-gray-200 hover:border-purple-300"
            )}
          >
            <div className="flex items-center gap-2 mb-2">
              <div className={cn(
                "w-5 h-5 rounded-full border-2 flex items-center justify-center",
                addressing === 'CULTURAL' ? "border-purple-500" : "border-gray-300"
              )}>
                {addressing === 'CULTURAL' && (
                  <div className="w-3 h-3 rounded-full bg-purple-500" />
                )}
              </div>
              <span className="font-semibold text-gray-900">Cultural Terms</span>
            </div>
            <p className="text-sm text-gray-600">
              Peppi will use traditional terms (Bhaiya/Didi, Anna/Akka, etc.)
            </p>
          </button>
        </div>
      </div>

      {/* Gender Preference */}
      <div className="space-y-3">
        <label className="block text-sm font-medium text-gray-700">
          Choose Peppi&apos;s voice
        </label>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <button
            onClick={() => setGender('male')}
            className={cn(
              "p-4 rounded-xl border-2 transition-all text-left",
              gender === 'male'
                ? "border-blue-500 bg-blue-50"
                : "border-gray-200 hover:border-blue-300"
            )}
          >
            <div className="flex items-center gap-2 mb-2">
              <div className={cn(
                "w-5 h-5 rounded-full border-2 flex items-center justify-center",
                gender === 'male' ? "border-blue-500" : "border-gray-300"
              )}>
                {gender === 'male' && (
                  <div className="w-3 h-3 rounded-full bg-blue-500" />
                )}
              </div>
              <span className="font-semibold text-gray-900">Male Voice</span>
            </div>
            <p className="text-sm text-gray-600">
              {GENDER_LABELS[language]?.male || 'Peppi Bhaiya (Boy)'}
            </p>
          </button>

          <button
            onClick={() => setGender('female')}
            className={cn(
              "p-4 rounded-xl border-2 transition-all text-left",
              gender === 'female'
                ? "border-pink-500 bg-pink-50"
                : "border-gray-200 hover:border-pink-300"
            )}
          >
            <div className="flex items-center gap-2 mb-2">
              <div className={cn(
                "w-5 h-5 rounded-full border-2 flex items-center justify-center",
                gender === 'female' ? "border-pink-500" : "border-gray-300"
              )}>
                {gender === 'female' && (
                  <div className="w-3 h-3 rounded-full bg-pink-500" />
                )}
              </div>
              <span className="font-semibold text-gray-900">Female Voice</span>
            </div>
            <p className="text-sm text-gray-600">
              {GENDER_LABELS[language]?.female || 'Peppi Didi (Girl)'}
            </p>
          </button>
        </div>
      </div>

      {/* Preview */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl p-4 border-2 border-purple-200"
      >
        <div className="flex items-start gap-3">
          <div className="flex-shrink-0">
            <span className="text-2xl">💬</span>
          </div>
          <div>
            <h4 className="font-semibold text-gray-900 mb-1">Preview</h4>
            <p className="text-gray-700">{previewMessage}</p>
          </div>
        </div>
      </motion.div>

      {/* Save Button */}
      {hasChanges && (
        <motion.button
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          onClick={handleSave}
          disabled={isSaving}
          className="w-full py-3 px-6 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-semibold rounded-xl hover:from-purple-600 hover:to-pink-600 transition-all shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isSaving ? (
            <span className="flex items-center justify-center gap-2">
              <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Saving...
            </span>
          ) : (
            'Save Preferences'
          )}
        </motion.button>
      )}
    </div>
  );
}

export default PeppiPreferenceSelector;
