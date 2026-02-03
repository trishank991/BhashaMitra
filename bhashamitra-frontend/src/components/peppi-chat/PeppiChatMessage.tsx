'use client';

import { PeppiChatMessage as MessageType } from '@/types';

interface PeppiChatMessageProps {
  message: MessageType;
}

export function PeppiChatMessage({ message }: PeppiChatMessageProps) {
  const isUser = message.role === 'user';

  return (
    <div
      className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-3`}
    >
      <div
        className={`max-w-[85%] px-4 py-3 rounded-2xl ${
          isUser
            ? 'bg-orange-500 text-white rounded-br-md'
            : 'bg-white border border-orange-100 text-gray-800 rounded-bl-md shadow-sm'
        }`}
      >
        {/* Avatar for Peppi */}
        {!isUser && (
          <div className="flex items-center gap-2 mb-2">
            <div className="w-6 h-6 bg-orange-100 rounded-full flex items-center justify-center text-sm">
              🐱
            </div>
            <span className="text-xs font-medium text-orange-600">Peppi</span>
          </div>
        )}

        {/* Main content */}
        <p className="text-sm leading-relaxed whitespace-pre-wrap">
          {message.content_primary}
        </p>

        {/* Romanized version if available */}
        {message.content_romanized && (
          <p className="text-xs mt-1.5 opacity-70 italic">
            {message.content_romanized}
          </p>
        )}

        {/* Audio playback if available */}
        {message.audio_output_url && (
          <button
            className="mt-2 flex items-center gap-1 text-xs text-orange-500 hover:text-orange-600"
            onClick={() => {
              const audio = new Audio(message.audio_output_url);
              audio.play();
            }}
          >
            <span>🔊</span>
            <span>Play Audio</span>
          </button>
        )}

        {/* Timestamp */}
        <p
          className={`text-[10px] mt-1.5 ${
            isUser ? 'text-orange-100' : 'text-gray-400'
          }`}
        >
          {new Date(message.created_at).toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit',
          })}
        </p>
      </div>
    </div>
  );
}
