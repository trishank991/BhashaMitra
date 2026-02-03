'use client';

import { useState } from 'react';
import { useAuthStore } from '@/stores';
import { Button } from '@/components/ui';
import api from '@/lib/api';

interface EmailVerificationBannerProps {
  className?: string;
}

export function EmailVerificationBanner({ className = '' }: EmailVerificationBannerProps) {
  const { user } = useAuthStore();
  const [isResending, setIsResending] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  // Don't show if user is verified or not logged in
  if (!user || user.email_verified) {
    return null;
  }

  const handleResendVerification = async () => {
    if (!user.email) return;

    setIsResending(true);
    setMessage(null);

    try {
      const response = await api.resendVerification(user.email);
      if (response.success) {
        setMessage({ type: 'success', text: 'Verification email sent! Check your inbox.' });
      } else {
        setMessage({ type: 'error', text: response.error || 'Failed to send verification email' });
      }
    } catch {
      setMessage({ type: 'error', text: 'Something went wrong. Please try again.' });
    } finally {
      setIsResending(false);
    }
  };

  return (
    <div className={`bg-warning-50 border-l-4 border-warning-500 p-4 ${className}`}>
      <div className="flex items-start gap-3">
        <div className="flex-shrink-0">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={1.5}
            stroke="currentColor"
            className="w-5 h-5 text-warning-600"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75"
            />
          </svg>
        </div>
        <div className="flex-1">
          <h3 className="text-sm font-semibold text-warning-800">
            Verify Your Email
          </h3>
          <p className="text-sm text-warning-700 mt-1">
            Please verify your email address to unlock all features.
            We sent a verification link to <strong>{user.email}</strong>.
          </p>
          {message && (
            <p className={`text-sm mt-2 ${
              message.type === 'success' ? 'text-success-600' : 'text-error-600'
            }`}>
              {message.text}
            </p>
          )}
          <div className="mt-3">
            <Button
              variant="outline"
              size="sm"
              onClick={handleResendVerification}
              isLoading={isResending}
            >
              Resend Verification Email
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default EmailVerificationBanner;
