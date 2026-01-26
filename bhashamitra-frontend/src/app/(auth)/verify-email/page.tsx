'use client';

import { Suspense, useEffect, useState } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { Button, Card } from '@/components/ui';
import { PeppiMascot } from '@/components/peppi';
import { fadeInUp } from '@/lib/constants';
import api from '@/lib/api';

type VerificationStatus = 'loading' | 'success' | 'error' | 'no-token';

function VerifyEmailContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [status, setStatus] = useState<VerificationStatus>('loading');
  const [message, setMessage] = useState('');
  const [email, setEmail] = useState('');

  useEffect(() => {
    const token = searchParams.get('token');

    if (!token) {
      setStatus('no-token');
      setMessage('No verification token provided.');
      return;
    }

    const verifyEmail = async () => {
      const result = await api.verifyEmail(token);

      if (result.success && result.data) {
        setStatus('success');
        setMessage('Your email has been verified successfully!');
        setEmail(result.data.data?.email || '');
      } else {
        setStatus('error');
        setMessage(result.error || 'Failed to verify email. The token may be expired or invalid.');
      }
    };

    verifyEmail();
  }, [searchParams]);

  const getIcon = () => {
    switch (status) {
      case 'loading':
        return (
          <div className="w-16 h-16 border-4 border-primary-200 border-t-primary-500 rounded-full animate-spin" />
        );
      case 'success':
        return (
          <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center">
            <svg className="w-8 h-8 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
        );
      case 'error':
      case 'no-token':
        return (
          <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center">
            <svg className="w-8 h-8 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </div>
        );
    }
  };

  const getTitle = () => {
    switch (status) {
      case 'loading':
        return 'Verifying your email...';
      case 'success':
        return 'Email Verified!';
      case 'error':
        return 'Verification Failed';
      case 'no-token':
        return 'Invalid Link';
    }
  };

  return (
    <motion.div
      initial="initial"
      animate="animate"
      className="w-full max-w-md"
    >
      {/* Peppi greeting */}
      <motion.div
        variants={fadeInUp}
        className="flex justify-center mb-8"
      >
        <PeppiMascot
          size="sm"
          showSpeechBubble={status === 'success'}
          speechText={status === 'success' ? "Welcome aboard!" : undefined}
        />
      </motion.div>

      <motion.div variants={fadeInUp}>
        <Card className="text-center">
          <div className="flex justify-center mb-6">
            {getIcon()}
          </div>

          <h1 className="text-2xl font-bold text-gray-900 mb-2">
            {getTitle()}
          </h1>

          <p className="text-gray-500 mb-6">
            {message}
          </p>

          {email && status === 'success' && (
            <p className="text-sm text-gray-400 mb-6">
              Verified email: <span className="font-medium text-gray-600">{email}</span>
            </p>
          )}

          {status === 'success' && (
            <Button
              size="lg"
              className="w-full"
              onClick={() => router.push('/login')}
            >
              Continue to Login
            </Button>
          )}

          {(status === 'error' || status === 'no-token') && (
            <div className="space-y-3">
              <Button
                size="lg"
                className="w-full"
                onClick={() => router.push('/login')}
              >
                Go to Login
              </Button>
              <p className="text-sm text-gray-500">
                Need a new verification link?{' '}
                <Link href="/login" className="text-primary-500 font-semibold hover:underline">
                  Request one after logging in
                </Link>
              </p>
            </div>
          )}
        </Card>
      </motion.div>
    </motion.div>
  );
}

function LoadingFallback() {
  return (
    <div className="w-full max-w-md">
      <div className="flex justify-center mb-8">
        <div className="w-24 h-24 bg-gray-200 rounded-full animate-pulse" />
      </div>
      <Card className="text-center">
        <div className="flex justify-center mb-6">
          <div className="w-16 h-16 border-4 border-primary-200 border-t-primary-500 rounded-full animate-spin" />
        </div>
        <div className="h-8 bg-gray-200 rounded w-3/4 mx-auto mb-4 animate-pulse" />
        <div className="h-4 bg-gray-200 rounded w-1/2 mx-auto mb-6 animate-pulse" />
      </Card>
    </div>
  );
}

export default function VerifyEmailPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-primary-50 via-white to-secondary-50 flex flex-col">
      {/* Back button */}
      <header className="p-4">
        <Link href="/">
          <Button variant="ghost" size="sm" leftIcon={
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5">
              <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
            </svg>
          }>
            Home
          </Button>
        </Link>
      </header>

      <main className="flex-1 flex flex-col items-center justify-center px-6 py-8">
        <Suspense fallback={<LoadingFallback />}>
          <VerifyEmailContent />
        </Suspense>
      </main>
    </div>
  );
}
