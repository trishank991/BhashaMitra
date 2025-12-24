'use client';

import { useState } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { Button, Input, Card } from '@/components/ui';
import { PeppiMascot } from '@/components/peppi';
import { fadeInUp } from '@/lib/constants';
import api from '@/lib/api';

type FormStatus = 'idle' | 'loading' | 'success' | 'error';

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [status, setStatus] = useState<FormStatus>('idle');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!email) {
      setStatus('error');
      setMessage('Please enter your email address.');
      return;
    }

    setStatus('loading');

    const result = await api.requestPasswordReset(email);

    if (result.success) {
      setStatus('success');
      setMessage('If an account exists with this email, we\'ve sent a password reset link.');
    } else {
      // Still show success message to prevent email enumeration
      setStatus('success');
      setMessage('If an account exists with this email, we\'ve sent a password reset link.');
    }
  };

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
              speechText={status === 'success' ? "Check your inbox!" : undefined}
            />
          </motion.div>

          <motion.h1
            variants={fadeInUp}
            className="text-2xl font-bold text-center text-gray-900 mb-2"
          >
            Forgot Password?
          </motion.h1>

          <motion.p
            variants={fadeInUp}
            className="text-center text-gray-500 mb-6"
          >
            {status === 'success'
              ? "We've sent you an email with instructions"
              : "Enter your email and we'll send you a reset link"}
          </motion.p>

          <motion.div variants={fadeInUp}>
            <Card>
              {status === 'success' ? (
                <div className="text-center">
                  <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg className="w-8 h-8 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <p className="text-gray-600 mb-6">{message}</p>
                  <p className="text-sm text-gray-500 mb-4">
                    Didn&apos;t receive the email? Check your spam folder or try again.
                  </p>
                  <Button
                    variant="outline"
                    size="lg"
                    className="w-full"
                    onClick={() => {
                      setStatus('idle');
                      setEmail('');
                    }}
                  >
                    Try Again
                  </Button>
                </div>
              ) : (
                <form onSubmit={handleSubmit} className="space-y-4">
                  <Input
                    label="Email"
                    type="email"
                    placeholder="parent@example.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    leftIcon={
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75" />
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
                    Send Reset Link
                  </Button>
                </form>
              )}

              <div className="mt-6 text-center">
                <p className="text-sm text-gray-500">
                  Remember your password?{' '}
                  <Link href="/login" className="text-primary-500 font-semibold hover:underline">
                    Log in
                  </Link>
                </p>
              </div>
            </Card>
          </motion.div>
        </motion.div>
      </main>
    </div>
  );
}
