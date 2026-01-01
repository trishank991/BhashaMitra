'use client';

import { PeppiChatMode } from '@/types';

interface PeppiChatHeaderProps {
  mode: PeppiChatMode;
  onModeChange: (mode: PeppiChatMode) => void;
  onClose: () => void;
  onEndConversation?: () => void;
  hasActiveConversation: boolean;
}

const MODE_LABELS: Record<PeppiChatMode, { label: string; icon: string }> = {
  GENERAL: { label: 'Chat', icon: '💬' },
  FESTIVAL_STORY: { label: 'Story', icon: '📖' },
  CURRICULUM_HELP: { label: 'Learn', icon: '📚' },
};

// Mini Peppi head SVG for header
function PeppiMiniHead() {
  return (
    <svg viewBox="0 0 100 100" className="w-8 h-8">
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

export function PeppiChatHeader({
  mode,
  onModeChange,
  onClose,
  onEndConversation,
  hasActiveConversation,
}: PeppiChatHeaderProps) {
  return (
    <div className="bg-gradient-to-r from-orange-500 to-amber-500 text-white px-4 py-3 rounded-t-2xl">
      {/* Top row: Title and close */}
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-white/20 rounded-full flex items-center justify-center p-0.5">
            <PeppiMiniHead />
          </div>
          <div>
            <h3 className="font-semibold text-sm">Chat with Peppi</h3>
            <p className="text-[10px] text-orange-100">
              {MODE_LABELS[mode].icon} {MODE_LABELS[mode].label} Mode
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {hasActiveConversation && onEndConversation && (
            <button
              onClick={onEndConversation}
              className="text-xs bg-white/20 hover:bg-white/30 px-2 py-1 rounded transition-colors"
              title="End conversation"
            >
              End Chat
            </button>
          )}
          <button
            onClick={onClose}
            className="w-8 h-8 hover:bg-white/20 rounded-full flex items-center justify-center transition-colors"
            title="Close"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fillRule="evenodd"
                d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                clipRule="evenodd"
              />
            </svg>
          </button>
        </div>
      </div>

      {/* Mode selector - 3 modes: Chat, Story, Learn */}
      <div className="flex gap-1 bg-white/10 rounded-lg p-1">
        {(Object.keys(MODE_LABELS) as PeppiChatMode[]).map((m) => (
          <button
            key={m}
            onClick={() => onModeChange(m)}
            className={`flex-1 text-xs py-1.5 px-2 rounded-md transition-colors ${
              mode === m
                ? 'bg-white text-orange-600 font-medium shadow-sm'
                : 'text-white/80 hover:bg-white/10'
            }`}
          >
            {MODE_LABELS[m].icon} {MODE_LABELS[m].label}
          </button>
        ))}
      </div>
    </div>
  );
}
