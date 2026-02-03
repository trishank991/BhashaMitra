'use client';

import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';
import { useAgeConfig } from '@/hooks/useAgeConfig';
import AudioButton from '@/components/ui/AudioButton';

interface LetterCardProps {
  letter: string;
  transliteration: string;
  audioUrl?: string;
  example?: {
    word: string;
    meaning: string;
    audioUrl?: string;
  };
  isSelected?: boolean;
  isCorrect?: boolean;
  isIncorrect?: boolean;
  onClick?: () => void;
  showAudio?: boolean;
  className?: string;
}

export function LetterCard({
  letter,
  transliteration,
  audioUrl,
  example,
  isSelected = false,
  isCorrect = false,
  isIncorrect = false,
  onClick,
  showAudio = true,
  className,
}: LetterCardProps) {
  const ageConfig = useAgeConfig();

  const getStateStyles = () => {
    if (isCorrect) return 'border-green-500 bg-green-50 ring-2 ring-green-300';
    if (isIncorrect) return 'border-red-500 bg-red-50 ring-2 ring-red-300 animate-shake';
    if (isSelected) return 'border-primary-500 bg-primary-50 ring-2 ring-primary-300';
    return 'border-gray-200 bg-white hover:border-primary-300 hover:bg-gray-50';
  };

  return (
    <motion.div
      onClick={onClick}
      className={cn(
        'relative rounded-2xl border-2 cursor-pointer transition-all',
        ageConfig.spacing.padding,
        getStateStyles(),
        ageConfig.animations.bounce && 'hover:scale-[1.02]',
        className
      )}
      whileHover={{ scale: ageConfig.animations.bounce ? 1.02 : 1 }}
      whileTap={{ scale: 0.98 }}
      animate={
        isCorrect
          ? { scale: [1, 1.1, 1], transition: { duration: 0.3 } }
          : isIncorrect
          ? { x: [-5, 5, -5, 5, 0], transition: { duration: 0.4 } }
          : {}
      }
    >
      {/* Main Letter Display */}
      <div className="text-center">
        {ageConfig.showHindiScript && (
          <p className={cn('font-bold text-gray-900', ageConfig.fontSize.heading)}>
            {letter}
          </p>
        )}
        <p
          className={cn(
            'text-primary-600 font-semibold',
            ageConfig.showHindiScript ? ageConfig.fontSize.body : ageConfig.fontSize.heading
          )}
        >
          {transliteration}
        </p>
      </div>

      {/* Example Word (if provided and not junior) */}
      {example && !ageConfig.useSimplifiedUI && (
        <div className="mt-3 pt-3 border-t border-gray-100 text-center">
          <p className={cn('text-gray-700', ageConfig.fontSize.small)}>
            {example.word}
          </p>
          <p className="text-sm text-gray-500">{example.meaning}</p>
        </div>
      )}

      {/* Audio Button */}
      {showAudio && (
        <div className="absolute -top-2 -right-2">
          <AudioButton
            text={letter}
            audioUrl={audioUrl}
            size="sm"
            variant="primary"
          />
        </div>
      )}

      {/* Success/Error indicators */}
      {isCorrect && (
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          className="absolute -top-3 -left-3 w-8 h-8 bg-green-500 rounded-full flex items-center justify-center"
        >
          <span className="text-white text-lg">✓</span>
        </motion.div>
      )}
    </motion.div>
  );
}

export default LetterCard;
