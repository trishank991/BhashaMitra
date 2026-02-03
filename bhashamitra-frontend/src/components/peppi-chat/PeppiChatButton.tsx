'use client';

import { motion } from 'framer-motion';
import { usePeppiChatStore } from '@/stores';

interface PeppiChatButtonProps {
  childId: string;
}

// Mini Peppi head SVG for the chat button
function PeppiHead() {
  return (
    <svg viewBox="0 0 100 100" className="w-10 h-10">
      {/* Ears */}
      <path fill="#F5E6D3" d="M20 40 L10 10 L35 30 Z"/>
      <path fill="#F5E6D3" d="M80 40 L90 10 L65 30 Z"/>
      <path fill="#FFCDB8" d="M22 30 L16 18 L32 28 Z"/>
      <path fill="#FFCDB8" d="M78 30 L84 18 L68 28 Z"/>
      {/* Head */}
      <ellipse fill="#F5E6D3" cx="50" cy="50" rx="38" ry="35"/>
      {/* Eyes */}
      <ellipse fill="white" cx="35" cy="48" rx="12" ry="14"/>
      <ellipse fill="white" cx="65" cy="48" rx="12" ry="14"/>
      <ellipse fill="#4A90D9" cx="35" cy="50" rx="9" ry="11"/>
      <ellipse fill="#4A90D9" cx="65" cy="50" rx="9" ry="11"/>
      <ellipse fill="#1a1a1a" cx="35" cy="51" rx="4" ry="5"/>
      <ellipse fill="#1a1a1a" cx="65" cy="51" rx="4" ry="5"/>
      <circle fill="white" cx="38" cy="45" r="3"/>
      <circle fill="white" cx="68" cy="45" r="3"/>
      {/* Nose */}
      <path fill="#FF7F50" d="M50 58 L46 65 L54 65 Z"/>
      {/* Whiskers */}
      <line stroke="#999" strokeWidth="1" x1="8" y1="52" x2="28" y2="56"/>
      <line stroke="#999" strokeWidth="1" x1="8" y1="60" x2="28" y2="60"/>
      <line stroke="#999" strokeWidth="1" x1="92" y1="52" x2="72" y2="56"/>
      <line stroke="#999" strokeWidth="1" x1="92" y1="60" x2="72" y2="60"/>
      {/* Collar */}
      <ellipse fill="#FF6B35" cx="50" cy="78" rx="22" ry="5"/>
      {/* Bell */}
      <circle fill="#FFD700" cx="50" cy="83" r="5"/>
      <circle fill="#FFF8DC" cx="48" cy="81" r="1.5"/>
    </svg>
  );
}

export function PeppiChatButton({ childId }: PeppiChatButtonProps) {
  const { isOpen, openChat, closeChat } = usePeppiChatStore();

  const handleClick = () => {
    if (isOpen) {
      closeChat();
    } else {
      openChat('GENERAL');
    }
  };

  return (
    <motion.button
      onClick={handleClick}
      className={`fixed bottom-20 right-4 z-50 w-16 h-16 rounded-full shadow-xl
                  flex items-center justify-center transition-all
                  ${isOpen
                    ? 'bg-gray-100 hover:bg-gray-200 border-2 border-gray-300'
                    : 'bg-gradient-to-br from-orange-100 to-amber-100 hover:from-orange-200 hover:to-amber-200 border-2 border-orange-300'
                  }`}
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.95 }}
      animate={{
        y: isOpen ? 0 : [0, -5, 0],
      }}
      transition={{
        y: {
          duration: 2,
          repeat: isOpen ? 0 : Infinity,
          ease: 'easeInOut',
        },
      }}
    >
      {isOpen ? (
        // Close icon
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="h-6 w-6 text-gray-600"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M6 18L18 6M6 6l12 12"
          />
        </svg>
      ) : (
        // Peppi head
        <PeppiHead />
      )}

      {/* AI badge when closed */}
      {!isOpen && (
        <motion.span
          className="absolute -top-1 -right-1 bg-gradient-to-r from-pink-500 to-orange-500 text-white px-2 py-0.5 rounded-full text-[10px] font-bold shadow-lg"
          animate={{ scale: [1, 1.1, 1] }}
          transition={{ duration: 2, repeat: Infinity }}
        >
          AI
        </motion.span>
      )}

      {/* Chat text hint */}
      {!isOpen && (
        <motion.div
          initial={{ opacity: 0, x: 10 }}
          animate={{ opacity: 1, x: 0 }}
          className="absolute right-full mr-2 bg-white px-3 py-1.5 rounded-lg shadow-lg whitespace-nowrap"
        >
          <span className="text-sm font-medium text-gray-700">Chat with Peppi!</span>
          <div className="absolute right-0 top-1/2 -translate-y-1/2 translate-x-1 w-0 h-0 border-t-[6px] border-t-transparent border-b-[6px] border-b-transparent border-l-[6px] border-l-white" />
        </motion.div>
      )}
    </motion.button>
  );
}
