'use client';

import React, { useEffect, useState } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { PeppiAvatar } from '@/components/peppi/PeppiAvatar';

interface MimicResult {
  attempt_id: string;
  transcription: string;
  score: number;
  stars: number;
  coach_tip: string;
  points_earned: number;
  is_personal_best: boolean;
  mastered: boolean;
  peppi_feedback: string;
  share_message: string;
  progress: {
    best_score: number;
    best_stars: number;
    total_attempts: number;
    mastered: boolean;
  };
  score_breakdown: {
    stt_confidence: { raw: number; weighted: number; weight: number };
    text_match: { raw: number; weighted: number; weight: number };
    energy: { raw: number; weighted: number; weight: number };
    duration: { raw: number; weighted: number; weight: number };
  };
}

// Mock result for testing when no backend data available
const mockResult: MimicResult = {
  attempt_id: 'mock-id',
  transcription: 'नमस्ते',
  score: 85,
  stars: 3,
  coach_tip: 'Great pronunciation! Try to emphasize the "न" sound a bit more.',
  points_earned: 35,
  is_personal_best: true,
  mastered: true,
  peppi_feedback: "MEOW! That was PURRRFECT! You're a paw-some language star!",
  share_message: '🎉 I got a PERFECT score on PeppiAcademy! Word: नमस्ते Score: ⭐⭐⭐ 85%',
  progress: {
    best_score: 85,
    best_stars: 3,
    total_attempts: 5,
    mastered: true,
  },
  score_breakdown: {
    stt_confidence: { raw: 0.92, weighted: 46, weight: 0.5 },
    text_match: { raw: 90, weighted: 27, weight: 0.3 },
    energy: { raw: 85, weighted: 12.75, weight: 0.15 },
    duration: { raw: 80, weighted: 4, weight: 0.05 },
  },
};

export default function MimicResultsPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const challengeId = searchParams.get('id');
  const [result, setResult] = useState<MimicResult | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Try to get actual result from sessionStorage
    const storedResult = sessionStorage.getItem('mimicResult');
    if (storedResult) {
      try {
        const parsedResult = JSON.parse(storedResult);
        setResult(parsedResult);
        setLoading(false);
        // Clear the stored result after retrieving
        sessionStorage.removeItem('mimicResult');
        return;
      } catch (e) {
        console.error('Failed to parse mimic result:', e);
      }
    }

    // Fallback to mock data if no stored result
    setTimeout(() => {
      setResult(mockResult);
      setLoading(false);
    }, 1000);
  }, [challengeId]);

  const getStarEmojis = (stars: number) => {
    return '⭐'.repeat(stars) || '💪';
  };

  const getScoreColor = (score: number) => {
    if (score >= 85) return 'text-green-500';
    if (score >= 65) return 'text-yellow-500';
    return 'text-orange-500';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-primary-50 to-white p-6 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-500 mx-auto mb-4"></div>
          <p className="text-lg text-gray-600">Peppi is evaluating your pronunciation...</p>
        </div>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-primary-50 to-white p-6">
        <div className="max-w-md mx-auto text-center">
          <p className="text-red-500">Failed to load results</p>
          <button onClick={() => router.push('/practice/mimic')} className="mt-4 px-4 py-2 bg-primary-500 text-white rounded">
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-primary-50 to-white p-6">
      <div className="max-w-md mx-auto">
        {/* Peppi Avatar with celebration */}
        <div className="flex justify-center mb-6">
          <PeppiAvatar 
            size="xl" 
            mood={result.stars >= 3 ? 'celebrating' : result.stars >= 2 ? 'happy' : 'encouraging'} 
          />
        </div>

        {/* Peppi's Feedback */}
        <div className="bg-white rounded-2xl shadow-lg p-6 mb-6 border-2 border-primary-200">
          <p className="text-lg text-gray-800 text-center">{result.peppi_feedback}</p>
        </div>

        {/* Score Display */}
        <div className="bg-white rounded-2xl shadow-lg p-6 mb-6 text-center">
          <div className={`text-5xl font-bold mb-2 ${getScoreColor(result.score)}`}>{result.score}%</div>
          <div className="text-3xl mb-2">{getStarEmojis(result.stars)}</div>
          <p className="text-sm text-gray-500">
            {result.is_personal_best && <span className="text-green-500 font-semibold">🎉 Personal Best! </span>}
            {result.points_earned} points earned
          </p>
        </div>

        {/* Score Breakdown */}
        <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
          <h3 className="font-bold text-gray-800 mb-4">Score Breakdown</h3>
          
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">STT Confidence</span>
              <div className="flex items-center gap-2">
                <div className="w-24 h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-primary-500" 
                    style={{ width: `${result.score_breakdown.stt_confidence.raw * 100}%` }}
                  ></div>
                </div>
                <span className="text-sm font-medium w-12 text-right">{result.score_breakdown.stt_confidence.raw.toFixed(2)}</span>
              </div>
            </div>

            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Text Match</span>
              <div className="flex items-center gap-2">
                <div className="w-24 h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-secondary-500" 
                    style={{ width: `${result.score_breakdown.text_match.raw}%` }}
                  ></div>
                </div>
                <span className="text-sm font-medium w-12 text-right">{result.score_breakdown.text_match.raw.toFixed(0)}</span>
              </div>
            </div>

            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Audio Energy</span>
              <div className="flex items-center gap-2">
                <div className="w-24 h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-accent-500" 
                    style={{ width: `${result.score_breakdown.energy.raw}%` }}
                  ></div>
                </div>
                <span className="text-sm font-medium w-12 text-right">{result.score_breakdown.energy.raw.toFixed(0)}</span>
              </div>
            </div>

            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Duration Match</span>
              <div className="flex items-center gap-2">
                <div className="w-24 h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-warning-500" 
                    style={{ width: `${result.score_breakdown.duration.raw}%` }}
                  ></div>
                </div>
                <span className="text-sm font-medium w-12 text-right">{result.score_breakdown.duration.raw.toFixed(0)}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Coach's Tip */}
        {result.coach_tip && (
          <div className="bg-yellow-50 rounded-2xl shadow p-4 mb-6 border border-yellow-200">
            <div className="flex gap-3">
              <span className="text-xl">💡</span>
              <div>
                <p className="text-sm font-medium text-yellow-800">Coach&apos;s Tip</p>
                <p className="text-sm text-yellow-700">{result.coach_tip}</p>
              </div>
            </div>
          </div>
        )}

        {/* What Peppi Heard */}
        <div className="bg-gray-50 rounded-2xl shadow p-4 mb-6">
          <p className="text-sm font-medium text-gray-500 mb-1">Peppi heard:</p>
          <p className="text-xl text-gray-800 font-semibold">{result.transcription || '(No speech detected)'}</p>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-3">
          <button
            onClick={() => router.push(`/practice/mimic/${challengeId}`)}
            className="flex-1 px-4 py-3 bg-primary-500 text-white rounded-xl font-medium hover:bg-primary-600 transition-colors"
          >
            Try Again
          </button>
          <button
            onClick={() => router.push('/practice/mimic')}
            className="flex-1 px-4 py-3 bg-gray-200 text-gray-700 rounded-xl font-medium hover:bg-gray-300 transition-colors"
          >
            Next Word
          </button>
        </div>

        {/* Share */}
        <button
          onClick={() => {
            if (navigator.share) {
              navigator.share({
                title: 'My PeppiAcademy Score',
                text: result.share_message,
              });
            } else {
              navigator.clipboard.writeText(result.share_message);
              alert('Copied to clipboard!');
            }
          }}
          className="w-full mt-4 px-4 py-3 border-2 border-primary-500 text-primary-600 rounded-xl font-medium hover:bg-primary-50 transition-colors"
        >
          📤 Share Your Score
        </button>
      </div>
    </div>
  );
}