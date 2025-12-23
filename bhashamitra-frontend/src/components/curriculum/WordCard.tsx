'use client';

import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';
import { useAgeConfig } from '@/hooks/useAgeConfig';
import AudioButton from '@/components/ui/AudioButton';

interface WordCardProps {
  word: string;
  transliteration: string;
  meaning: string;
  audioUrl?: string;
  imageUrl?: string;
  category?: string;
  isSelected?: boolean;
  isCorrect?: boolean;
  isIncorrect?: boolean;
  isRevealed?: boolean;
  onClick?: () => void;
  showAudio?: boolean;
  showMeaning?: boolean;
  variant?: 'default' | 'compact' | 'flashcard';
  className?: string;
}

export function WordCard({
  word,
  transliteration,
  meaning,
  audioUrl,
  imageUrl,
  category,
  isSelected = false,
  isCorrect = false,
  isIncorrect = false,
  isRevealed = true,
  onClick,
  showAudio = true,
  showMeaning = true,
  variant = 'default',
  className,
}: WordCardProps) {
  const ageConfig = useAgeConfig();

  const getStateStyles = () => {
    if (isCorrect) return 'border-green-500 bg-green-50 ring-2 ring-green-300';
    if (isIncorrect) return 'border-red-500 bg-red-50 ring-2 ring-red-300';
    if (isSelected) return 'border-primary-500 bg-primary-50 ring-2 ring-primary-300';
    return 'border-gray-200 bg-white hover:border-primary-300 hover:shadow-md';
  };

  const variantStyles = {
    default: 'p-4 md:p-6',
    compact: 'p-3',
    flashcard: 'p-6 min-h-[200px] flex flex-col justify-center',
  };

  return (
    <motion.div
      onClick={onClick}
      className={cn(
        'relative rounded-2xl border-2 cursor-pointer transition-all overflow-hidden',
        variantStyles[variant],
        getStateStyles(),
        className
      )}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      animate={
        isCorrect
          ? { scale: [1, 1.05, 1] }
          : isIncorrect
          ? { x: [-5, 5, -5, 5, 0] }
          : {}
      }
      transition={{ duration: 0.3 }}
    >
      {/* Category badge */}
      {category && (
        <span className="absolute top-2 left-2 text-xs bg-primary-100 text-primary-700 px-2 py-1 rounded-full">
          {category}
        </span>
      )}

      {/* Image (if provided) */}
      {imageUrl && (
        <div className="mb-3 flex justify-center">
          <img
            src={imageUrl}
            alt={meaning}
            className="w-20 h-20 object-cover rounded-xl"
          />
        </div>
      )}

      {/* Word content */}
      <div className="text-center">
        {/* Hindi word */}
        {ageConfig.showHindiScript && (
          <p className={cn('font-bold text-gray-900 mb-1', ageConfig.fontSize.heading)}>
            {word}
          </p>
        )}

        {/* Transliteration */}
        <p
          className={cn(
            'text-primary-600 font-semibold',
            ageConfig.showHindiScript ? ageConfig.fontSize.body : ageConfig.fontSize.heading
          )}
        >
          {transliteration}
        </p>

        {/* Meaning */}
        {showMeaning && isRevealed && (
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className={cn('text-gray-600 mt-2', ageConfig.fontSize.small)}
          >
            {meaning}
          </motion.p>
        )}
      </div>

      {/* Audio Button */}
      {showAudio && (
        <div className="absolute -top-2 -right-2">
          <AudioButton
            text={word}
            audioUrl={audioUrl}
            size="sm"
            variant="primary"
          />
        </div>
      )}

      {/* Flashcard reveal hint */}
      {variant === 'flashcard' && !isRevealed && (
        <p className="absolute bottom-4 left-0 right-0 text-center text-sm text-gray-400">
          Tap to reveal
        </p>
      )}

      {/* Success indicator */}
      {isCorrect && (
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          className="absolute -top-3 -left-3 w-8 h-8 bg-green-500 rounded-full flex items-center justify-center shadow-lg"
        >
          <span className="text-white text-lg">✓</span>
        </motion.div>
      )}
    </motion.div>
  );
}

export default WordCard;
