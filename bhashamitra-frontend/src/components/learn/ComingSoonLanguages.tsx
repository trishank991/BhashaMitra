'use client';

import { ComingSoonCard } from '@/components/ui/ComingSoonCard';
import { Globe } from 'lucide-react';

const upcomingLanguages = [
  {
    code: 'TAMIL',
    name: 'Tamil',
    nativeName: 'தமிழ்',
    description: 'Learn Tamil with Peppi! Same fun games, different language.',
    color: '#e74c3c',
    peppiMessage: 'வணக்கம்! Vanakkam! I\'m learning Tamil too!',
    flag: '🇮🇳',
  },
  {
    code: 'GUJARATI',
    name: 'Gujarati',
    nativeName: 'ગુજરાતી',
    description: 'Explore Gujarati with stories, songs, and games.',
    color: '#e67e22',
    peppiMessage: 'નમસ્તે! Namaste in Gujarati!',
    flag: '🇮🇳',
  },
  {
    code: 'PUNJABI',
    name: 'Punjabi',
    nativeName: 'ਪੰਜਾਬੀ',
    description: 'Learn Punjabi with Bhangra beats and fun!',
    color: '#3498db',
    peppiMessage: 'ਸਤ ਸ੍ਰੀ ਅਕਾਲ! Sat Sri Akaal!',
    flag: '🇮🇳',
  },
  {
    code: 'BENGALI',
    name: 'Bengali',
    nativeName: 'বাংলা',
    description: 'Discover Bengali language and culture.',
    color: '#1abc9c',
    peppiMessage: 'নমস্কার! Nomoshkar!',
    flag: '🇮🇳',
  },
];

interface ComingSoonLanguagesProps {
  onWaitlistClick?: (languageCode: string) => void;
  className?: string;
}

export function ComingSoonLanguages({ onWaitlistClick, className }: ComingSoonLanguagesProps) {
  return (
    <div className={className}>
      <div className="text-center mb-8">
        <div className="flex items-center justify-center gap-3 mb-2">
          <Globe className="w-8 h-8 text-purple-500" />
          <h2 className="text-2xl font-bold text-gray-800">More Languages Coming!</h2>
        </div>
        <p className="text-gray-600">
          PeppiAcademy will soon support more Indian languages!
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {upcomingLanguages.map((language) => (
          <ComingSoonCard
            key={language.code}
            title={`${language.name} ${language.flag}`}
            titleHindi={language.nativeName}
            description={language.description}
            peppiMessage={language.peppiMessage}
            releaseHint="Coming 2025"
            type="language"
            icon={<Globe className="w-10 h-10" style={{ color: language.color }} />}
            color={language.color}
            showWaitlist
            onWaitlistClick={() => onWaitlistClick?.(language.code)}
          />
        ))}
      </div>

      {/* Additional Info */}
      <div className="mt-12 text-center">
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-3xl p-8 border-2 border-blue-200">
          <h3 className="text-xl font-bold text-gray-800 mb-3">
            And more languages coming!
          </h3>
          <p className="text-gray-600 mb-4">
            We&apos;re working to bring all 22 official Indian languages to PeppiAcademy.
          </p>
          <p className="text-sm text-gray-500">
            Telugu, Marathi, Kannada, Malayalam, Odia, Assamese and more!
          </p>
        </div>
      </div>
    </div>
  );
}

export default ComingSoonLanguages;
