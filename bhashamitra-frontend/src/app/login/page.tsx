'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { useAuthStore } from '@/stores';
import { Button, Input, Card } from '@/components/ui';
import { PeppiAvatar } from '@/components/peppi';
import { fadeInUp } from '@/lib/constants';

export default function LoginPage() {
  const router = useRouter();
  const { login, isLoading } = useAuthStore();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!email || !password) {
      setError('Please fill in all fields');
      return;
    }

    const success = await login(email, password);

    if (success) {
      router.push('/home');
    } else {
      setError('Invalid email or password');
    }
  };

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
            Back
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
            className="flex justify-center mb-6"
          >
            <PeppiAvatar size="lg" showBubble={false} />
          </motion.div>

          <motion.h1
            variants={fadeInUp}
            className="text-2xl font-bold text-center text-gray-900 mb-2"
          >
            Welcome Back!
          </motion.h1>

          <motion.p
            variants={fadeInUp}
            className="text-center text-gray-500 mb-8"
          >
            Log in to continue learning
          </motion.p>

          {/* Login Form */}
          <motion.div variants={fadeInUp}>
            <Card>
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

                <Input
                  label="Password"
                  type="password"
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  leftIcon={
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 1 0-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 0 0 2.25-2.25v-6.75a2.25 2.25 0 0 0-2.25-2.25H6.75a2.25 2.25 0 0 0-2.25 2.25v6.75a2.25 2.25 0 0 0 2.25 2.25Z" />
                    </svg>
                  }
                />

                {error && (
                  <p className="text-error-500 text-sm text-center">{error}</p>
                )}

                <Button
                  type="submit"
                  size="lg"
                  className="w-full"
                  isLoading={isLoading}
                >
                  Log In
                </Button>
              </form>

              <div className="mt-6 text-center">
                <p className="text-sm text-gray-500">
                  Don&apos;t have an account?{' '}
                  <Link href="/register" className="text-primary-500 font-semibold hover:underline">
                    Sign up
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
