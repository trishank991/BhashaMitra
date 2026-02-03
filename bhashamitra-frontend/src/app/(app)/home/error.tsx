'use client';

import { useEffect } from 'react';
import { Button } from '@/components/ui';

interface ErrorPageProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function HomeError({ error, reset }: ErrorPageProps) {
  useEffect(() => {
    // Log error to console in development only
    if (process.env.NODE_ENV === 'development') {
      console.error('[HomeError]', error);
    }
  }, [error]);

  return (
    <div className="min-h-[60vh] flex flex-col items-center justify-center px-6">
      <div className="w-full max-w-md text-center">
        {/* Error Icon */}
        <div className="w-20 h-20 mx-auto mb-6 bg-error-100 rounded-full flex items-center justify-center">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={1.5}
            stroke="currentColor"
            className="w-10 h-10 text-error-500"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z"
            />
          </svg>
        </div>

        {/* Error Message */}
        <h1 className="text-xl font-bold text-gray-900 mb-2">
          Something went wrong
        </h1>
        <p className="text-gray-600 mb-6">
          We couldn&apos;t load your home page. Let&apos;s try again!
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
            Try Again
          </Button>
          <Button
            variant="outline"
            size="lg"
            className="w-full"
            onClick={() => (window.location.href = '/')}
          >
            Go to Welcome Page
          </Button>
        </div>
      </div>
    </div>
  );
}
