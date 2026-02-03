'use client';

import { useEffect } from 'react';
import { Button } from '@/components/ui';

interface ErrorPageProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function GamesError({ error, reset }: ErrorPageProps) {
  useEffect(() => {
    // Log error to console in development only
    if (process.env.NODE_ENV === 'development') {
      console.error('[GamesError]', error);
    }
  }, [error]);

  return (
    <div className="min-h-[60vh] flex flex-col items-center justify-center px-6">
      <div className="w-full max-w-md text-center">
        {/* Error Icon */}
        <div className="w-20 h-20 mx-auto mb-6 bg-primary-100 rounded-full flex items-center justify-center">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={1.5}
            stroke="currentColor"
            className="w-10 h-10 text-primary-500"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M14.25 6.087c0-.355.186-.676.401-.959.221-.29.349-.634.349-1.003 0-1.036-1.007-1.875-2.25-1.875s-2.25.84-2.25 1.875c0 .369.128.713.349 1.003.215.283.401.604.401.959v0a.64.64 0 0 1-.657.643 48.39 48.39 0 0 1-4.163-.3c.186 1.613.293 3.25.315 4.907a.656.656 0 0 1-.658.663v0c-.355 0-.676-.186-.959-.401a1.647 1.647 0 0 0-1.003-.349c-1.036 0-1.875 1.007-1.875 2.25s.84 2.25 1.875 2.25c.369 0 .713-.128 1.003-.349.283-.215.604-.401.959-.401v0c.31 0 .555.26.532.57a48.039 48.039 0 0 1-.642 5.056c1.518.19 3.058.309 4.616.354a.64.64 0 0 0 .657-.643v0c0-.355-.186-.676-.401-.959a1.647 1.647 0 0 1-.349-1.003c0-1.035 1.008-1.875 2.25-1.875 1.243 0 2.25.84 2.25 1.875 0 .369-.128.713-.349 1.003-.215.283-.4.604-.4.959v0c0 .333.277.599.61.58a48.1 48.1 0 0 0 4.957-.665 48.228 48.228 0 0 0-.642-5.033.641.641 0 0 1 .532-.57v0c.355 0 .676.186.959.401.29.221.634.349 1.003.349 1.035 0 1.875-1.007 1.875-2.25s-.84-2.25-1.875-2.25c-.369 0-.713.128-1.003.349-.283.215-.604.401-.959.401v0a.656.656 0 0 1-.658-.663 48.422 48.422 0 0 0-.37-5.36c-1.886.342-3.81.574-5.766.689a.578.578 0 0 1-.61-.58v0Z"
            />
          </svg>
        </div>

        {/* Error Message */}
        <h1 className="text-xl font-bold text-gray-900 mb-2">
          Game paused!
        </h1>
        <p className="text-gray-600 mb-6">
          Something went wrong with the game. Let&apos;s try playing again!
        </p>

        {/* Error Details (Development only) */}
        {process.env.NODE_ENV === 'development' && (
          <div className="mb-6 p-4 bg-gray-100 rounded-lg text-left">
            <p className="text-sm font-mono text-gray-700 break-words">
              {error.message}
            </p>
          </div>
        )}

        {/* Action Buttons */}
        <div className="space-y-3">
          <Button size="lg" className="w-full" onClick={reset}>
            Play Again
          </Button>
          <Button
            variant="outline"
            size="lg"
            className="w-full"
            onClick={() => (window.location.href = '/games')}
          >
            Back to Games
          </Button>
        </div>
      </div>
    </div>
  );
}
