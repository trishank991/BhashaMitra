'use client';

import { useState, useCallback } from 'react';
import { motion } from 'framer-motion';
import { Share2, MessageCircle, Check, Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ShareButtonProps {
  shareMessage: string;
  childName: string;
  word: string;
  stars: number;
  onShareComplete?: () => void;
  variant?: 'primary' | 'secondary' | 'whatsapp';
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

const sizeStyles = {
  sm: 'px-3 py-2 text-sm',
  md: 'px-4 py-2.5 text-base',
  lg: 'px-6 py-3 text-lg',
};

const iconSizes = {
  sm: 16,
  md: 20,
  lg: 24,
};

export function ShareButton({
  shareMessage,
  childName,
  word,
  stars,
  onShareComplete,
  variant = 'whatsapp',
  size = 'md',
  className,
}: ShareButtonProps) {
  const [isSharing, setIsSharing] = useState(false);
  const [isShared, setIsShared] = useState(false);

  const getVariantStyles = () => {
    switch (variant) {
      case 'whatsapp':
        return 'bg-[#25D366] hover:bg-[#20BD5A] text-white';
      case 'primary':
        return 'bg-primary-500 hover:bg-primary-600 text-white';
      case 'secondary':
        return 'bg-gray-100 hover:bg-gray-200 text-gray-700';
      default:
        return 'bg-[#25D366] hover:bg-[#20BD5A] text-white';
    }
  };

  const handleShare = useCallback(async () => {
    if (isSharing || isShared) return;

    setIsSharing(true);

    try {
      // Use Web Share API if available (mobile)
      if (navigator.share) {
        await navigator.share({
          title: `${childName} learned "${word}"!`,
          text: shareMessage,
        });
      } else {
        // Fallback to WhatsApp web link
        const encodedMessage = encodeURIComponent(shareMessage);
        const whatsappUrl = `https://wa.me/?text=${encodedMessage}`;
        window.open(whatsappUrl, '_blank', 'noopener,noreferrer');
      }

      setIsShared(true);
      onShareComplete?.();

      // Reset after a delay
      setTimeout(() => {
        setIsShared(false);
      }, 3000);

    } catch {
      // User cancelled sharing or error occurred - this is expected
    } finally {
      setIsSharing(false);
    }
  }, [shareMessage, childName, word, onShareComplete, isSharing, isShared]);

  const renderIcon = () => {
    if (isSharing) {
      return <Loader2 size={iconSizes[size]} className="animate-spin" />;
    }
    if (isShared) {
      return <Check size={iconSizes[size]} />;
    }
    if (variant === 'whatsapp') {
      return <MessageCircle size={iconSizes[size]} />;
    }
    return <Share2 size={iconSizes[size]} />;
  };

  const renderLabel = () => {
    if (isSharing) return 'Sharing...';
    if (isShared) return 'Shared!';
    if (variant === 'whatsapp') return 'Share on WhatsApp';
    return 'Share with Family';
  };

  return (
    <motion.button
      onClick={handleShare}
      disabled={isSharing}
      whileHover={{ scale: isSharing ? 1 : 1.02 }}
      whileTap={{ scale: isSharing ? 1 : 0.98 }}
      className={cn(
        "flex items-center justify-center gap-2 font-semibold rounded-xl transition-all shadow-md",
        sizeStyles[size],
        getVariantStyles(),
        isSharing && 'opacity-80 cursor-wait',
        isShared && 'bg-green-500 hover:bg-green-500',
        className
      )}
    >
      {renderIcon()}
      <span>{renderLabel()}</span>

      {/* Star decoration for 3-star results */}
      {stars === 3 && !isSharing && !isShared && (
        <span className="ml-1">⭐</span>
      )}
    </motion.button>
  );
}

/**
 * Generate a WhatsApp share URL with pre-filled message.
 * Can be used directly in anchor tags.
 */
export function getWhatsAppShareUrl(message: string): string {
  const encodedMessage = encodeURIComponent(message);
  return `https://wa.me/?text=${encodedMessage}`;
}

/**
 * Generate share message for a mimic attempt.
 */
export function generateShareMessage(
  childName: string,
  word: string,
  romanization: string,
  language: string,
  stars: number,
  score: number
): string {
  const starEmoji = '⭐'.repeat(stars);
  const languageLabel = language.charAt(0) + language.slice(1).toLowerCase();

  if (stars === 3) {
    return `🎉 ${childName} just MASTERED saying "${word}" (${romanization}) in ${languageLabel}! ${starEmoji}\n\nScore: ${Math.round(score)}% - PERFECT!\n\n🎓 Learning languages with PeppiAcademy!`;
  } else if (stars === 2) {
    return `✨ ${childName} is getting great at saying "${word}" (${romanization}) in ${languageLabel}! ${starEmoji}\n\nScore: ${Math.round(score)}%\n\n🎓 Learning languages with PeppiAcademy!`;
  } else {
    return `💪 ${childName} is practicing "${word}" (${romanization}) in ${languageLabel}! ${starEmoji}\n\nScore: ${Math.round(score)}% - Keep it up!\n\n🎓 Learning languages with PeppiAcademy!`;
  }
}

export default ShareButton;
