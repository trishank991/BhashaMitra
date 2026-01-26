'use client';

import { Suspense, useState } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { Button, Input, Card } from '@/components/ui';
import { PeppiMascot } from '@/components/peppi';
import { fadeInUp } from '@/lib/constants';
import api from '@/lib/api';

type FormStatus = 'idle' | 'loading' | 'success' | 'error' | 'no-token';

function ResetPasswordForm() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const token = searchParams.get('token');

  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [status, setStatus] = useState<FormStatus>(token ? 'idle' : 'no-token');
  const [message, setMessage] = useState(token ? '' : 'No reset token provided. Please request a new password reset link.');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!token) {
      setStatus('no-token');
      setMessage('No reset token provided. Please request a new password reset link.');
      return;
    }

    if (!password || !confirmPassword) {
      setStatus('error');
      setMessage('Please fill in all fields.');
      return;
    }

    if (password.length < 8) {
      setStatus('error');
      setMessage('Password must be at least 8 characters.');
      return;
    }

    if (password !== confirmPassword) {
      setStatus('error');
      setMessage('Passwords do not match.');
      return;
    }

    setStatus('loading');

    const result = await api.resetPassword(token, password, confirmPassword);

    if (result.success) {
      setStatus('success');
      setMessage('Your password has been reset successfully!');
    } else {
      setStatus('error');
      setMessage(result.error || 'Failed to reset password. The token may be expired or invalid.');
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
          speechText={status === 'success' ? "All set!" : undefined}
        />
      </motion.div>

      <motion.h1
        variants={fadeInUp}
        className="text-2xl font-bold text-center text-gray-900 mb-2"
      >
        {status === 'success' ? 'Password Reset!' : 'Reset Your Password'}
      </motion.h1>

      <motion.p
        variants={fadeInUp}
        className="text-center text-gray-500 mb-6"
      >
        {status === 'success'
          ? 'You can now log in with your new password'
          : 'Enter your new password below'}
      </motion.p>

      <motion.div variants={fadeInUp}>
        <Card>
          {status === 'success' ? (
            <div className="text-center">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <p className="text-gray-600 mb-6">{message}</p>
              <Button
                size="lg"
                className="w-full"
                onClick={() => router.push('/login')}
              >
                Continue to Login
              </Button>
            </div>
          ) : status === 'no-token' ? (
            <div className="text-center">
              <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
              <p className="text-gray-600 mb-6">{message}</p>
              <Button
                size="lg"
                className="w-full"
                onClick={() => router.push('/forgot-password')}
              >
                Request New Link
              </Button>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4">
              <Input
                label="New Password"
                type="password"
                placeholder="At least 8 characters"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                leftIcon={
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 1 0-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 0 0 2.25-2.25v-6.75a2.25 2.25 0 0 0-2.25-2.25H6.75a2.25 2.25 0 0 0-2.25 2.25v6.75a2.25 2.25 0 0 0 2.25 2.25Z" />
                  </svg>
                }
              />

              <Input
                label="Confirm New Password"
                type="password"
                placeholder="Confirm your password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                leftIcon={
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 1 0-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 0 0 2.25-2.25v-6.75a2.25 2.25 0 0 0-2.25-2.25H6.75a2.25 2.25 0 0 0-2.25 2.25v6.75a2.25 2.25 0 0 0 2.25 2.25Z" />
                  </svg>
                }
              />

              {status === 'error' && (
                <p className="text-error-500 text-sm text-center">{message}</p>
              )}

              <Button
                type="submit"
                size="lg"
                className="w-full"
                isLoading={status === 'loading'}
              >
                Reset Password
              </Button>
            </form>
          )}

          {status !== 'success' && status !== 'no-token' && (
            <div className="mt-6 text-center">
              <p className="text-sm text-gray-500">
                Remember your password?{' '}
                <Link href="/login" className="text-primary-500 font-semibold hover:underline">
                  Log in
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
      <div className="h-8 bg-gray-200 rounded w-3/4 mx-auto mb-4 animate-pulse" />
      <div className="h-4 bg-gray-200 rounded w-1/2 mx-auto mb-6 animate-pulse" />
      <Card>
        <div className="space-y-4">
          <div className="h-12 bg-gray-200 rounded animate-pulse" />
          <div className="h-12 bg-gray-200 rounded animate-pulse" />
          <div className="h-12 bg-gray-200 rounded animate-pulse" />
        </div>
      </Card>
    </div>
  );
}

export default function ResetPasswordPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-primary-50 via-white to-secondary-50 flex flex-col">
      {/* Back button */}
      <header className="p-4">
        <Link href="/login">
          <Button variant="ghost" size="sm" leftIcon={
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5">
              <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
            </svg>
          }>
            Back to Login
          </Button>
        </Link>
      </header>

      <main className="flex-1 flex flex-col items-center justify-center px-6 py-8">
        <Suspense fallback={<LoadingFallback />}>
          <ResetPasswordForm />
        </Suspense>
      </main>
    </div>
  );
}
