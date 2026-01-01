'use client';

import { useEffect, useCallback, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { usePeppiStore } from '@/stores';
import { useAgeConfig } from '@/hooks/useAgeConfig';
import { getPeppiScripts, getRandomScript, PeppiScript, PeppiMood } from '@/data/peppi-scripts';
import PeppiAvatar from './PeppiAvatar';
import AudioButton from '@/components/ui/AudioButton';
import { cn } from '@/lib/utils';

interface PeppiSpeechProps {
  trigger?: 'welcome' | 'correct' | 'incorrect' | 'encouragement' | 'lessonComplete' | 'streak' | 'hint' | 'idle' | 'custom';
  customMessage?: string;
  customMood?: PeppiMood;
  customAudioText?: string;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  position?: 'left' | 'center' | 'right';
  autoSpeak?: boolean;
  onSpeakComplete?: () => void;
  className?: string;
}

export function PeppiSpeech({
  trigger = 'idle',
  customMessage,
  customMood,
  customAudioText,
  size = 'md',
  position = 'center',
  autoSpeak = false,
  onSpeakComplete,
  className,
}: PeppiSpeechProps) {
  const { setMood, setCurrentMessage, setTyping } = usePeppiStore();
  const ageConfig = useAgeConfig();
  const [currentScript, setCurrentScript] = useState<PeppiScript | null>(null);
  const [showAudioButton, setShowAudioButton] = useState(false);

  const speak = useCallback((script: PeppiScript) => {
    setTyping(true);
    setMood(script.mood);

    // Simulate typing effect
    setTimeout(() => {
      setTyping(false);
      setCurrentMessage(script.message);
      setCurrentScript(script);
      setShowAudioButton(true);
    }, 500);
  }, [setTyping, setMood, setCurrentMessage]);

  useEffect(() => {
    if (trigger === 'custom' && customMessage) {
      speak({
        message: customMessage,
        mood: customMood || 'happy',
        audioText: customAudioText || customMessage,
      });
    } else if (trigger !== 'custom') {
      const scripts = getPeppiScripts(ageConfig.variant);
      const scriptSet = scripts[trigger];
      if (scriptSet && scriptSet.length > 0) {
        const script = getRandomScript(scriptSet);
        speak(script);
      }
    }
  }, [trigger, customMessage, customMood, customAudioText, ageConfig.variant, speak]);

  const positionStyles = {
    left: 'justify-start',
    center: 'justify-center',
    right: 'justify-end',
  };

  return (
    <div className={cn('flex items-end', positionStyles[position], className)}>
      <div className="relative flex flex-col items-center">
        <PeppiAvatar size={size} showBubble={true} />

        {/* Audio button appears after message */}
        <AnimatePresence>
          {showAudioButton && currentScript?.audioText && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 10 }}
              className="mt-2"
            >
              <AudioButton
                text={currentScript.audioText}
                size="sm"
                variant="secondary"
                autoPlay={autoSpeak}
                onPlayEnd={onSpeakComplete}
              />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

export default PeppiSpeech;
