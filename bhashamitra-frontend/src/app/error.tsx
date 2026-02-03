'use client';

import { useEffect } from 'react';
import { Button } from '@/components/ui';

interface ErrorPageProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function GlobalError({ error, reset }: ErrorPageProps) {
  useEffect(() => {
    // Log error to console in development only
    if (process.env.NODE_ENV === 'development') {
      console.error('[GlobalError]', error);
    }
  }, [error]);

  return (
    <div className="min-h-screen bg-gradient-to-b from-primary-50 via-white to-secondary-50 flex flex-col items-center justify-center px-6">
      <div className="w-full max-w-md text-center">
        {/* Error Icon */}
        <div className="w-24 h-24 mx-auto mb-6 bg-error-100 rounded-full flex items-center justify-center">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={1.5}
            stroke="currentColor"
            className="w-12 h-12 text-error-500"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z"
            />
          </svg>
        </div>

        {/* Error Message */}
        <h1 className="text-2xl font-bold text-gray-900 mb-2">
          Oops! Something went wrong
        </h1>
        <p className="text-gray-600 mb-6">
          Don&apos;t worry, it&apos;s not your fault. Let&apos;s try again!
        </p>

        {/* Error Details (Development only) */}
        {process.env.NODE_ENV === 'development' && (
          <div className="mb-6 p-4 bg-gray-100 rounded-lg text-left">
            <p className="text-sm font-mono text-gray-700 break-words">
              {error.message}
            </p>
            {error.digest && (
              <p className="text-xs text-gray-500 mt-2">
                Error ID: {error.digest}
              </p>
            )}
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
            onClick={() => (window.location.href = '/home')}
          >
            Go to Home
          </Button>
        </div>

        {/* Help Link */}
        <p className="mt-6 text-sm text-gray-500">
          If this keeps happening,{' '}
          <a href="/help" className="text-primary-600 hover:underline">
            contact support
          </a>
        </p>
      </div>
    </div>
  );
}
