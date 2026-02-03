'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { usePeppiStore } from '@/stores';
import { PeppiAvatar } from './PeppiAvatar';
import { cn } from '@/lib/utils';

interface PeppiAssistantProps {
  position?: 'bottom-right' | 'bottom-left';
  showOnMount?: boolean;
  autoGreet?: boolean;
}

export function PeppiAssistant({
  position = 'bottom-right',
  showOnMount = true,
  autoGreet = true,
}: PeppiAssistantProps) {
  const router = useRouter();
  const [isVisible] = useState(showOnMount);
  const [isMinimized, setIsMinimized] = useState(false);
  const [showActionMenu, setShowActionMenu] = useState(false);
  const { greet, currentMessage, isTyping, speakWithAnimation } = usePeppiStore();

  useEffect(() => {
    if (autoGreet && isVisible && !isMinimized) {
      const timer = setTimeout(() => {
        greet();
      }, 1000);
      return () => clearTimeout(timer);
    }
  }, [autoGreet, isVisible, isMinimized, greet]);

  const positionClasses = {
    'bottom-right': 'right-4 bottom-20 md:bottom-4',
    'bottom-left': 'left-4 bottom-20 md:bottom-4',
  };

  const handlePeppiClick = () => {
    if (showActionMenu) {
      setShowActionMenu(false);
    } else {
      setShowActionMenu(true);
    }
  };

  const handleStoryTime = async () => {
    setShowActionMenu(false);
    await speakWithAnimation("Let's hear a story! Choose a festival story.", 'greeting');
    router.push('/festivals');
  };

  const handleMinimize = () => {
    setShowActionMenu(false);
    setIsMinimized(true);
  };

  if (!isVisible) return null;

  return (
    <div className={cn('fixed z-40', positionClasses[position])}>
      <AnimatePresence>
        {!isMinimized ? (
          <motion.div
            initial={{ opacity: 0, scale: 0.8, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.8, y: 20 }}
            className="relative"
          >
            {/* Action Menu */}
            <AnimatePresence>
              {showActionMenu && (
                <motion.div
                  initial={{ opacity: 0, y: 10, scale: 0.9 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  exit={{ opacity: 0, y: 10, scale: 0.9 }}
                  className="absolute bottom-full mb-2 right-0 bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden min-w-[160px]"
                >
                  <button
                    onClick={handleStoryTime}
                    className="w-full px-4 py-3 flex items-center gap-3 hover:bg-orange-50 transition-colors text-left"
                  >
                    <span className="text-2xl">📖</span>
                    <div>
                      <p className="font-semibold text-gray-900 text-sm">Story Time</p>
                      <p className="text-xs text-gray-500">Festival Stories</p>
                    </div>
                  </button>
                  <div className="border-t border-gray-100" />
                  <button
                    onClick={handleMinimize}
                    className="w-full px-4 py-2 flex items-center gap-3 hover:bg-gray-50 transition-colors text-left"
                  >
                    <span className="text-lg">💤</span>
                    <p className="text-sm text-gray-600">Hide Peppi</p>
                  </button>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Close/Minimize button */}
            <button
              onClick={handleMinimize}
              className="absolute -top-2 -right-2 z-10 w-6 h-6 bg-gray-200 hover:bg-gray-300 rounded-full flex items-center justify-center text-gray-600 transition-colors"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={2}
                stroke="currentColor"
                className="w-4 h-4"
              >
                <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 12h-15" />
              </svg>
            </button>

            <div onClick={handlePeppiClick} className="cursor-pointer">
              <PeppiAvatar size="lg" showBubble />
            </div>
          </motion.div>
        ) : (
          <motion.button
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
            onClick={() => setIsMinimized(false)}
            className="relative bg-primary-500 hover:bg-primary-600 text-white rounded-full p-3 shadow-lg transition-colors"
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
          >
            {/* Cat icon when minimized */}
            <svg viewBox="0 0 24 24" fill="currentColor" className="w-8 h-8">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" />
            </svg>

            {/* Notification dot if there's a message */}
            {(currentMessage || isTyping) && (
              <motion.div
                className="absolute -top-1 -right-1 w-4 h-4 bg-error-500 rounded-full"
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ duration: 1, repeat: Infinity }}
              />
            )}
          </motion.button>
        )}
      </AnimatePresence>
    </div>
  );
}

export function PeppiChatBubble({
  message,
  type = 'normal',
}: {
  message: string;
  type?: 'greeting' | 'hint' | 'encouragement' | 'celebration' | 'normal';
}) {
  const bgColors = {
    greeting: 'bg-secondary-50 border-secondary-200',
    hint: 'bg-accent-50 border-accent-200',
    encouragement: 'bg-primary-50 border-primary-200',
    celebration: 'bg-warning-50 border-warning-200',
    normal: 'bg-white border-gray-200',
  };

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      className={cn(
        'rounded-2xl rounded-bl-none px-4 py-3 border-2 shadow-sm max-w-xs',
        bgColors[type]
      )}
    >
      <p className="text-sm text-gray-700">{message}</p>
    </motion.div>
  );
}

export default PeppiAssistant;
