'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { PeppiMood } from '@/data/peppi-scripts';

interface Props {
  message: string;
  type: 'correct' | 'incorrect' | 'encouragement' | 'celebration' | 'streak' | 'hint';
  mood?: PeppiMood;
  isVisible: boolean;
}

const TYPE_STYLES = {
  correct: 'bg-green-100 border-green-400 text-green-800',
  incorrect: 'bg-orange-100 border-orange-400 text-orange-800',
  encouragement: 'bg-blue-100 border-blue-400 text-blue-800',
  celebration: 'bg-purple-100 border-purple-400 text-purple-800',
  streak: 'bg-yellow-100 border-yellow-400 text-yellow-800',
  hint: 'bg-teal-100 border-teal-400 text-teal-800',
};

const MOOD_ICONS: Record<PeppiMood, string> = {
  happy: '😊',
  excited: '🤩',
  thinking: '🤔',
  encouraging: '💪',
  celebrating: '🎉',
  sleepy: '😴',
};

export function PeppiFeedbackBubble({ message, type, mood = 'happy', isVisible }: Props) {
  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          initial={{ opacity: 0, y: 20, scale: 0.8 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: -20, scale: 0.8 }}
          transition={{ type: 'spring', stiffness: 300, damping: 25 }}
          className="fixed bottom-24 right-4 z-50 max-w-xs"
        >
          <div className={`p-4 rounded-2xl border-2 shadow-lg ${TYPE_STYLES[type]}`}>
            <div className="flex items-start gap-3">
              {/* Peppi mini icon */}
              <div className="flex-shrink-0 text-2xl">
                {MOOD_ICONS[mood]}
              </div>

              {/* Message */}
              <p className="text-lg font-medium flex-1">{message}</p>
            </div>

            {/* Speech bubble tail */}
            <div
              className={`absolute -bottom-2 right-8 w-4 h-4 border-r-2 border-b-2 ${
                TYPE_STYLES[type].split(' ')[1]
              } ${TYPE_STYLES[type].split(' ')[0]} transform rotate-45`}
            />
          </div>

          {/* Celebration particles for special moments */}
          {(type === 'celebration' || type === 'streak') && (
            <div className="absolute inset-0 pointer-events-none">
              {[...Array(6)].map((_, i) => (
                <motion.div
                  key={i}
                  className="absolute text-2xl"
                  initial={{
                    x: 0,
                    y: 0,
                    opacity: 1,
                    rotate: 0,
                  }}
                  animate={{
                    x: Math.cos((i * Math.PI * 2) / 6) * 60,
                    y: Math.sin((i * Math.PI * 2) / 6) * 60,
                    opacity: 0,
                    rotate: 360,
                  }}
                  transition={{
                    duration: 1,
                    ease: 'easeOut',
                    delay: i * 0.05,
                  }}
                  style={{
                    left: '50%',
                    top: '50%',
                  }}
                >
                  {type === 'celebration' ? '🎊' : '🔥'}
                </motion.div>
              ))}
            </div>
          )}
        </motion.div>
      )}
    </AnimatePresence>
  );
}

export default PeppiFeedbackBubble;
