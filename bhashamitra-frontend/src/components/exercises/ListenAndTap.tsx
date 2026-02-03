'use client';

import { useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from '@/lib/utils';
import { useAgeConfig } from '@/hooks/useAgeConfig';
import AudioButton from '@/components/ui/AudioButton';
import LetterCard from '@/components/curriculum/LetterCard';
import WordCard from '@/components/curriculum/WordCard';

interface LetterOption {
  id: string;
  letter: string;
  transliteration: string;
  audioUrl?: string;
}

interface WordOption {
  id: string;
  word: string;
  transliteration: string;
  meaning: string;
  audioUrl?: string;
}

interface ListenAndTapProps {
  type: 'letter' | 'word';
  prompt: string;
  promptAudioUrl?: string;
  correctId: string;
  options: LetterOption[] | WordOption[];
  onCorrect: () => void;
  onIncorrect: () => void;
  onComplete: () => void;
  showHint?: boolean;
  maxAttempts?: number;
  className?: string;
}

export function ListenAndTap({
  type,
  prompt,
  promptAudioUrl,
  correctId,
  options,
  onCorrect,
  onIncorrect,
  onComplete,
  showHint = true,
  maxAttempts = 3,
  className,
}: ListenAndTapProps) {
  const ageConfig = useAgeConfig();
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [isCorrect, setIsCorrect] = useState<boolean | null>(null);
  const [attempts, setAttempts] = useState(0);
  const [showAnswer, setShowAnswer] = useState(false);
  const [hasPlayed, setHasPlayed] = useState(false);

  // Limit options based on age
  const displayOptions = options.slice(0, ageConfig.maxOptionsPerQuestion);

  const handleSelect = useCallback(
    (id: string) => {
      if (isCorrect !== null) return; // Already answered

      setSelectedId(id);
      const correct = id === correctId;
      setIsCorrect(correct);
      setAttempts((prev) => prev + 1);

      if (correct) {
        onCorrect();
        setTimeout(() => {
          onComplete();
        }, 1500);
      } else {
        onIncorrect();
        // Reset for retry after animation
        setTimeout(() => {
          if (attempts + 1 >= maxAttempts) {
            setShowAnswer(true);
            setTimeout(() => onComplete(), 2000);
          } else {
            setSelectedId(null);
            setIsCorrect(null);
          }
        }, 1000);
      }
    },
    [correctId, isCorrect, attempts, maxAttempts, onCorrect, onIncorrect, onComplete]
  );

  // Note: AudioButton handles autoPlay internally via its autoPlay prop
  // The onPlayEnd callback sets hasPlayed to true after audio finishes

  return (
    <div className={cn('flex flex-col items-center', ageConfig.spacing.gap, className)}>
      {/* Prompt Section */}
      <div className="text-center mb-6">
        <p className={cn('text-gray-700 mb-4', ageConfig.fontSize.body)}>
          {prompt}
        </p>

        {/* Main Audio Button */}
        <AudioButton
          text={prompt}
          audioUrl={promptAudioUrl}
          size="lg"
          variant="primary"
          autoPlay={!hasPlayed}
          onPlayEnd={() => setHasPlayed(true)}
        />

        {/* Attempts indicator */}
        {maxAttempts > 1 && (
          <p className="mt-2 text-sm text-gray-500">
            Attempts: {attempts}/{maxAttempts}
          </p>
        )}
      </div>

      {/* Options Grid */}
      <div
        className={cn(
          'grid gap-4 w-full max-w-2xl',
          displayOptions.length <= 2 ? 'grid-cols-2' : 'grid-cols-2 md:grid-cols-4'
        )}
      >
        <AnimatePresence>
          {displayOptions.map((option, index) => (
            <motion.div
              key={option.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              {type === 'letter' ? (
                <LetterCard
                  letter={(option as LetterOption).letter}
                  transliteration={(option as LetterOption).transliteration}
                  audioUrl={(option as LetterOption).audioUrl}
                  isSelected={selectedId === option.id && isCorrect === null}
                  isCorrect={
                    (selectedId === option.id && isCorrect === true) ||
                    (showAnswer && option.id === correctId)
                  }
                  isIncorrect={selectedId === option.id && isCorrect === false}
                  onClick={() => handleSelect(option.id)}
                  showAudio={showHint && attempts > 0}
                />
              ) : (
                <WordCard
                  word={(option as WordOption).word}
                  transliteration={(option as WordOption).transliteration}
                  meaning={(option as WordOption).meaning}
                  audioUrl={(option as WordOption).audioUrl}
                  isSelected={selectedId === option.id && isCorrect === null}
                  isCorrect={
                    (selectedId === option.id && isCorrect === true) ||
                    (showAnswer && option.id === correctId)
                  }
                  isIncorrect={selectedId === option.id && isCorrect === false}
                  onClick={() => handleSelect(option.id)}
                  showAudio={showHint && attempts > 0}
                  showMeaning={showAnswer || isCorrect === true}
                />
              )}
            </motion.div>
          ))}
        </AnimatePresence>
      </div>

      {/* Hint after wrong answers */}
      {showHint && attempts > 0 && isCorrect === null && (
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className={cn('text-center text-gray-500 mt-4', ageConfig.fontSize.small)}
        >
          {ageConfig.variant === 'junior'
            ? 'Tap the speaker to hear again!'
            : 'Listen carefully to each option'}
        </motion.p>
      )}
    </div>
  );
}

export default ListenAndTap;
