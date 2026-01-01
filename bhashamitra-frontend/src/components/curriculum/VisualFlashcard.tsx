'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import Image from 'next/image';
import { cn } from '@/lib/utils';
import { SpeakerButton } from '@/components/ui';
import { useAgeConfig } from '@/hooks/useAgeConfig';

interface VisualFlashcardProps {
  word: string;
  romanization: string;
  translation: string;
  imageUrl?: string;
  audioUrl?: string;
  gender?: string;
  partOfSpeech?: string;
  exampleSentence?: string;
  isFlipped: boolean;
  onFlip: () => void;
  onAudioPlay?: (word: string) => void;
  className?: string;
  category?: string;
}

const CATEGORY_ICONS: Record<string, string> = {
  'Family': '👨‍👩‍👧',
  'Colors': '🎨',
  'Numbers': '🔢',
  'Animals': '🐾',
  'Food': '🍎',
  'Body Parts': '🖐️',
  'Greetings': '👋',
  'Actions': '🏃',
  'default': '📚'
};

const CATEGORY_GRADIENTS: Record<string, string> = {
  'Family': 'from-pink-100 via-purple-100 to-indigo-100',
  'Colors': 'from-red-100 via-yellow-100 to-blue-100',
  'Numbers': 'from-cyan-100 via-blue-100 to-indigo-100',
  'Animals': 'from-green-100 via-emerald-100 to-teal-100',
  'Food': 'from-orange-100 via-amber-100 to-yellow-100',
  'Body Parts': 'from-rose-100 via-pink-100 to-fuchsia-100',
  'Greetings': 'from-violet-100 via-purple-100 to-indigo-100',
  'Actions': 'from-lime-100 via-green-100 to-emerald-100',
  'default': 'from-purple-100 to-pink-100'
};

const ImagePlaceholder = ({ category }: { category?: string }) => {
  const gradient = CATEGORY_GRADIENTS[category || 'default'] || CATEGORY_GRADIENTS.default;
  const icon = CATEGORY_ICONS[category || 'default'] || CATEGORY_ICONS.default;

  return (
    <div className={cn(
      'w-full h-48 bg-gradient-to-br rounded-xl flex items-center justify-center',
      gradient
    )}>
      <span className="text-6xl">{icon}</span>
    </div>
  );
};

const GenderBadge = ({ gender }: { gender?: string }) => {
  if (!gender) return null;

  const isMasculine = gender.toLowerCase() === 'masculine' || gender.toLowerCase() === 'm';

  return (
    <span className={cn(
      'px-2 py-1 rounded-full text-xs font-semibold',
      isMasculine
        ? 'bg-blue-100 text-blue-700'
        : 'bg-pink-100 text-pink-700'
    )}>
      {isMasculine ? 'M' : 'F'}
    </span>
  );
};

const PartOfSpeechBadge = ({ partOfSpeech }: { partOfSpeech?: string }) => {
  if (!partOfSpeech) return null;

  return (
    <span className="px-2 py-1 rounded-full text-xs font-semibold bg-gray-100 text-gray-700">
      {partOfSpeech}
    </span>
  );
};

export function VisualFlashcard({
  word,
  romanization,
  translation,
  imageUrl,
  gender,
  partOfSpeech,
  exampleSentence,
  isFlipped,
  onFlip,
  onAudioPlay,
  className,
  category,
}: VisualFlashcardProps) {
  const ageConfig = useAgeConfig();
  const [imageError, setImageError] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const isLoading = false; // Audio loading handled by parent

  const handleAudioClick = () => {
    if (onAudioPlay) {
      setIsPlaying(!isPlaying);
      onAudioPlay(word);
      // Simulate audio playback duration
      setTimeout(() => setIsPlaying(false), 2000);
    }
  };

  // Age-adaptive sizing
  const sizes = {
    junior: {
      card: 'min-h-[400px]',
      image: 'h-56',
      wordFront: 'text-5xl md:text-6xl',
      wordBack: 'text-3xl md:text-4xl',
      romanization: 'text-xl md:text-2xl',
      translation: 'text-2xl md:text-3xl',
      hint: 'text-base',
    },
    standard: {
      card: 'min-h-[380px]',
      image: 'h-48',
      wordFront: 'text-4xl md:text-5xl',
      wordBack: 'text-2xl md:text-3xl',
      romanization: 'text-lg md:text-xl',
      translation: 'text-xl md:text-2xl',
      hint: 'text-sm',
    },
    teen: {
      card: 'min-h-[340px]',
      image: 'h-40',
      wordFront: 'text-3xl md:text-4xl',
      wordBack: 'text-xl md:text-2xl',
      romanization: 'text-base md:text-lg',
      translation: 'text-lg md:text-xl',
      hint: 'text-xs',
    },
  };

  const currentSizes = sizes[ageConfig.variant];

  return (
    <div className={cn('perspective-1000', className)}>
      <motion.div
        className={cn(
          'relative w-full cursor-pointer preserve-3d',
          currentSizes.card
        )}
        onClick={onFlip}
        initial={false}
        animate={{ rotateY: isFlipped ? 180 : 0 }}
        transition={{
          duration: ageConfig.animations.duration,
          type: ageConfig.animations.bounce ? 'spring' : 'tween',
        }}
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
      >
        {/* Front of Card */}
        <motion.div
          className={cn(
            'absolute inset-0 backface-hidden',
            'bg-white rounded-2xl shadow-xl p-6',
            'flex flex-col items-center justify-center',
            ageConfig.spacing.gap
          )}
          style={{ backfaceVisibility: 'hidden' }}
        >
          {/* Image Area */}
          <div className={cn('w-full', currentSizes.image, 'mb-4')}>
            {imageUrl && !imageError ? (
              <div className="relative w-full h-full rounded-xl overflow-hidden">
                <Image
                  src={imageUrl}
                  alt={word}
                  fill
                  className="object-cover"
                  onError={() => setImageError(true)}
                />
              </div>
            ) : (
              <ImagePlaceholder category={category} />
            )}
          </div>

          {/* Word in Native Script */}
          <p className={cn(
            'font-bold text-gray-900 mb-2 text-center',
            currentSizes.wordFront
          )}>
            {word}
          </p>

          {/* Romanization */}
          <p className={cn(
            'text-purple-600 mb-4 text-center',
            currentSizes.romanization
          )}>
            {romanization}
          </p>

          {/* Audio Button */}
          <div onClick={(e) => e.stopPropagation()}>
            <SpeakerButton
              isPlaying={isPlaying}
              isLoading={isLoading}
              onClick={handleAudioClick}
              size={ageConfig.variant === 'junior' ? 'lg' : 'md'}
            />
          </div>

          {/* Hint */}
          <p className={cn(
            'text-gray-400 mt-4 text-center',
            currentSizes.hint
          )}>
            {ageConfig.variant === 'junior' ? 'Tap to see what it means!' : 'Tap to see meaning'}
          </p>
        </motion.div>

        {/* Back of Card */}
        <motion.div
          className={cn(
            'absolute inset-0 backface-hidden',
            'bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl shadow-xl p-6',
            'flex flex-col items-center justify-center',
            ageConfig.spacing.gap
          )}
          style={{
            backfaceVisibility: 'hidden',
            transform: 'rotateY(180deg)'
          }}
        >
          {/* Smaller Image at Top */}
          {!ageConfig.useSimplifiedUI && (
            <div className="w-24 h-24 mb-3">
              {imageUrl && !imageError ? (
                <div className="relative w-full h-full rounded-lg overflow-hidden">
                  <Image
                    src={imageUrl}
                    alt={word}
                    fill
                    className="object-cover"
                    onError={() => setImageError(true)}
                  />
                </div>
              ) : (
                <div className={cn(
                  'w-full h-full bg-gradient-to-br rounded-lg flex items-center justify-center',
                  CATEGORY_GRADIENTS[category || 'default']
                )}>
                  <span className="text-3xl">{CATEGORY_ICONS[category || 'default']}</span>
                </div>
              )}
            </div>
          )}

          {/* Word + Romanization */}
          <p className={cn(
            'font-bold text-gray-900 text-center',
            currentSizes.wordBack
          )}>
            {word}
          </p>
          <p className={cn(
            'text-purple-600 mb-2 text-center',
            currentSizes.romanization
          )}>
            {romanization}
          </p>

          {/* Divider */}
          <div className="w-16 h-0.5 bg-gray-200 my-2" />

          {/* Translation (Highlighted) */}
          <p className={cn(
            'text-primary-600 font-bold mb-3 text-center',
            currentSizes.translation
          )}>
            {translation}
          </p>

          {/* Badges */}
          <div className="flex items-center gap-2 mb-3">
            <GenderBadge gender={gender} />
            <PartOfSpeechBadge partOfSpeech={partOfSpeech} />
          </div>

          {/* Example Sentence */}
          {exampleSentence && !ageConfig.useSimplifiedUI && (
            <div className="mt-2 p-3 bg-white/60 rounded-lg max-w-sm">
              <p className="text-sm text-gray-600 text-center italic">
                &ldquo;{exampleSentence}&rdquo;
              </p>
            </div>
          )}

          {/* Tap to flip back hint */}
          <p className={cn(
            'text-gray-400 mt-auto text-center',
            currentSizes.hint
          )}>
            {ageConfig.variant === 'junior' ? 'Tap to see the word again!' : 'Tap to flip back'}
          </p>
        </motion.div>
      </motion.div>

      <style jsx global>{`
        .perspective-1000 {
          perspective: 1000px;
        }
        .preserve-3d {
          transform-style: preserve-3d;
        }
        .backface-hidden {
          backface-visibility: hidden;
          -webkit-backface-visibility: hidden;
        }
      `}</style>
    </div>
  );
}

export default VisualFlashcard;
