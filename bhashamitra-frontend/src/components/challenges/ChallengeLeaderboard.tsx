'use client';

import { motion } from 'framer-motion';
import { ChallengeLeaderboardResponse } from '@/lib/api';

interface ChallengeLeaderboardProps {
  leaderboard: ChallengeLeaderboardResponse;
  myAttemptId?: string;
  onBack: () => void;
}

export function ChallengeLeaderboard({ leaderboard, myAttemptId, onBack }: ChallengeLeaderboardProps) {
  // Safe access to leaderboard array
  const entries = leaderboard?.leaderboard ?? [];

  const getRankBadge = (rank: number) => {
    if (rank === 1) return { emoji: '🥇', color: 'from-yellow-400 to-yellow-600' };
    if (rank === 2) return { emoji: '🥈', color: 'from-gray-300 to-gray-500' };
    if (rank === 3) return { emoji: '🥉', color: 'from-orange-400 to-orange-600' };
    return { emoji: `#${rank}`, color: 'from-purple-400 to-purple-600' };
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-purple-100 to-pink-100 p-4">
      <div className="max-w-lg mx-auto">
        {/* Header */}
        <div className="flex items-center gap-4 mb-6">
          <button
            onClick={onBack}
            className="p-2 rounded-full bg-white shadow-md hover:bg-gray-50"
          >
            <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Leaderboard</h1>
            <p className="text-gray-500">{leaderboard?.challenge_title ?? 'Challenge'}</p>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 gap-4 mb-6">
          <div className="bg-white rounded-xl p-4 shadow-md text-center">
            <div className="text-2xl font-bold text-purple-600">{leaderboard?.total_participants ?? 0}</div>
            <div className="text-sm text-gray-500">Players</div>
          </div>
          <div className="bg-white rounded-xl p-4 shadow-md text-center">
            <div className="text-2xl font-bold text-pink-600">{(leaderboard?.average_score ?? 0).toFixed(0)}%</div>
            <div className="text-sm text-gray-500">Avg Score</div>
          </div>
        </div>

        {/* Top 3 Podium */}
        {entries.length >= 3 && (
          <div className="flex items-end justify-center gap-2 mb-6">
            {/* 2nd place */}
            <motion.div
              initial={{ y: 50, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.2 }}
              className="text-center"
            >
              <div className="text-4xl mb-2">🥈</div>
              <div className="bg-gradient-to-b from-gray-200 to-gray-300 rounded-t-lg p-3 w-24 h-20">
                <div className="text-sm font-bold text-gray-800 truncate">
                  {entries[1]?.participant_name || '-'}
                </div>
                <div className="text-lg font-bold text-gray-700">
                  {entries[1]?.percentage || 0}%
                </div>
              </div>
            </motion.div>

            {/* 1st place */}
            <motion.div
              initial={{ y: 50, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.1 }}
              className="text-center"
            >
              <div className="text-5xl mb-2">🥇</div>
              <div className="bg-gradient-to-b from-yellow-300 to-yellow-500 rounded-t-lg p-3 w-28 h-28">
                <div className="text-sm font-bold text-yellow-900 truncate">
                  {entries[0]?.participant_name || '-'}
                </div>
                <div className="text-2xl font-bold text-yellow-900">
                  {entries[0]?.percentage || 0}%
                </div>
              </div>
            </motion.div>

            {/* 3rd place */}
            <motion.div
              initial={{ y: 50, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.3 }}
              className="text-center"
            >
              <div className="text-4xl mb-2">🥉</div>
              <div className="bg-gradient-to-b from-orange-200 to-orange-400 rounded-t-lg p-3 w-24 h-16">
                <div className="text-sm font-bold text-orange-900 truncate">
                  {entries[2]?.participant_name || '-'}
                </div>
                <div className="text-lg font-bold text-orange-800">
                  {entries[2]?.percentage || 0}%
                </div>
              </div>
            </motion.div>
          </div>
        )}

        {/* Full List */}
        <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
          <div className="p-4 border-b bg-gray-50">
            <h2 className="font-semibold text-gray-700">All Players</h2>
          </div>
          <div className="divide-y">
            {entries.map((entry, index) => {
              const badge = getRankBadge(entry.rank);
              const isMe = entry.id === myAttemptId;

              return (
                <motion.div
                  key={entry.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.05 }}
                  className={`flex items-center gap-4 p-4 ${isMe ? 'bg-purple-50' : ''}`}
                >
                  {/* Rank */}
                  <div className={`w-10 h-10 rounded-full bg-gradient-to-br ${badge.color} flex items-center justify-center text-white font-bold`}>
                    {entry.rank <= 3 ? badge.emoji : entry.rank}
                  </div>

                  {/* Name */}
                  <div className="flex-1 min-w-0">
                    <div className="font-semibold text-gray-900 truncate flex items-center gap-2">
                      {entry.participant_name}
                      {isMe && <span className="text-xs bg-purple-500 text-white px-2 py-0.5 rounded-full">You</span>}
                    </div>
                    {entry.participant_location && (
                      <div className="text-sm text-gray-500">{entry.participant_location}</div>
                    )}
                  </div>

                  {/* Score */}
                  <div className="text-right">
                    <div className="font-bold text-purple-600">{entry.percentage}%</div>
                    <div className="text-xs text-gray-400">
                      {Math.floor(entry.time_taken_seconds / 60)}:{(entry.time_taken_seconds % 60).toString().padStart(2, '0')}
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
