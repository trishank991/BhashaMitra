'use client';

import { motion } from 'framer-motion';
import { ChallengeResponse } from '@/lib/api';
import { ShareButton } from './ShareButton';

interface ChallengeCardProps {
  challenge: ChallengeResponse;
  onView: (code: string) => void;
}

export function ChallengeCard({ challenge, onView }: ChallengeCardProps) {
  const difficultyColors = {
    easy: 'bg-green-100 text-green-700',
    medium: 'bg-yellow-100 text-yellow-700',
    hard: 'bg-red-100 text-red-700',
  };

  const categoryEmojis: Record<string, string> = {
    alphabet: '🔤',
    vocabulary: '📚',
    numbers: '🔢',
    colors: '🎨',
    animals: '🐾',
    family: '👨‍👩‍👧',
    food: '🍎',
    greetings: '👋',
  };

  return (
    <motion.div
      whileHover={{ y: -4 }}
      className="bg-white rounded-2xl shadow-lg overflow-hidden"
    >
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-500 to-pink-500 p-4">
        <div className="flex items-center justify-between">
          <span className="text-3xl">{categoryEmojis[challenge.category] || '🎯'}</span>
          <span className="bg-white/20 text-white px-3 py-1 rounded-full text-sm font-medium">
            {challenge.code}
          </span>
        </div>
        <h3 className="text-xl font-bold text-white mt-2">{challenge.title}</h3>
        {challenge.title_native && (
          <p className="text-white/80 text-sm">{challenge.title_native}</p>
        )}
      </div>

      {/* Stats */}
      <div className="p-4">
        <div className="flex items-center gap-3 mb-4">
          <span className={`px-3 py-1 rounded-full text-xs font-medium ${difficultyColors[challenge.difficulty as keyof typeof difficultyColors]}`}>
            {challenge.difficulty}
          </span>
          <span className="text-gray-500 text-sm">
            {challenge.question_count} questions
          </span>
          <span className="text-gray-500 text-sm">
            {challenge.language_name}
          </span>
        </div>

        <div className="grid grid-cols-3 gap-3 mb-4">
          <div className="text-center p-2 bg-gray-50 rounded-lg">
            <div className="text-lg font-bold text-purple-600">{challenge.total_completions}</div>
            <div className="text-xs text-gray-500">Completed</div>
          </div>
          <div className="text-center p-2 bg-gray-50 rounded-lg">
            <div className="text-lg font-bold text-pink-600">{challenge.average_score.toFixed(0)}%</div>
            <div className="text-xs text-gray-500">Avg Score</div>
          </div>
          <div className="text-center p-2 bg-gray-50 rounded-lg">
            <div className="text-lg font-bold text-orange-600">{challenge.participant_count}</div>
            <div className="text-xs text-gray-500">Players</div>
          </div>
        </div>

        {/* Expiry warning */}
        {challenge.expires_at && !challenge.is_expired && (
          <div className="text-xs text-amber-600 bg-amber-50 px-3 py-2 rounded-lg mb-4">
            Expires: {new Date(challenge.expires_at).toLocaleDateString()}
          </div>
        )}

        {challenge.is_expired && (
          <div className="text-xs text-red-600 bg-red-50 px-3 py-2 rounded-lg mb-4">
            This challenge has expired
          </div>
        )}

        {/* Actions */}
        <div className="flex gap-2">
          <button
            onClick={() => onView(challenge.code)}
            className="flex-1 py-2 px-4 bg-purple-100 hover:bg-purple-200 text-purple-700 rounded-lg font-medium transition-colors"
          >
            View Details
          </button>
          <ShareButton
            url={challenge.share_url}
            title={challenge.title}
            className="flex-shrink-0"
          />
        </div>
      </div>
    </motion.div>
  );
}
