'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface ShareButtonProps {
  url: string;
  title: string;
  className?: string;
}

export function ShareButton({ url, title, className = '' }: ShareButtonProps) {
  const [copied, setCopied] = useState(false);
  const [showOptions, setShowOptions] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(url);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  const handleWhatsApp = () => {
    const message = encodeURIComponent(`${title}\n\nPlay my challenge: ${url}`);
    window.open(`https://wa.me/?text=${message}`, '_blank');
  };

  const handleNativeShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title,
          text: `Play my ${title} challenge!`,
          url,
        });
      } catch (err) {
        if ((err as Error).name !== 'AbortError') {
          console.error('Share failed:', err);
        }
      }
    } else {
      setShowOptions(true);
    }
  };

  return (
    <div className={`relative ${className}`}>
      <button
        onClick={handleNativeShare}
        className="flex items-center gap-2 px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-full font-semibold transition-colors shadow-lg"
      >
        <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
          <path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92s2.92-1.31 2.92-2.92-1.31-2.92-2.92-2.92z"/>
        </svg>
        Share Challenge
      </button>

      <AnimatePresence>
        {showOptions && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="absolute bottom-full left-0 mb-2 bg-white rounded-xl shadow-xl p-3 min-w-[200px] z-10"
          >
            <button
              onClick={handleWhatsApp}
              className="w-full flex items-center gap-3 px-3 py-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <span className="text-xl">📱</span>
              <span className="font-medium">WhatsApp</span>
            </button>
            <button
              onClick={handleCopy}
              className="w-full flex items-center gap-3 px-3 py-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <span className="text-xl">{copied ? '✅' : '📋'}</span>
              <span className="font-medium">{copied ? 'Copied!' : 'Copy Link'}</span>
            </button>
            <button
              onClick={() => setShowOptions(false)}
              className="w-full text-sm text-gray-400 mt-2"
            >
              Close
            </button>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
