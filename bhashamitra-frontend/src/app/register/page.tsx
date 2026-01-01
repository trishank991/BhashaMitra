'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { useAuthStore } from '@/stores';
import { Button, Input, Card } from '@/components/ui';
import { PeppiMascot } from '@/components/peppi';
import { SocialLoginButtons } from '@/components/auth';
import { fadeInUp } from '@/lib/constants';

export default function RegisterPage() {
  const router = useRouter();
  const { register, isLoading } = useAuthStore();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [tosAccepted, setTosAccepted] = useState(false);
  const [error, setError] = useState('');

  // Password validation helpers
  const passwordChecks = {
    minLength: password.length >= 8,
    hasUppercase: /[A-Z]/.test(password),
    hasLowercase: /[a-z]/.test(password),
    hasNumber: /[0-9]/.test(password),
  };

  const passwordStrength = Object.values(passwordChecks).filter(Boolean).length;
  const isPasswordValid = Object.values(passwordChecks).every(Boolean);

  const getPasswordStrengthColor = () => {
    if (passwordStrength <= 1) return 'bg-error-500';
    if (passwordStrength <= 2) return 'bg-warning-500';
    if (passwordStrength <= 3) return 'bg-yellow-500';
    return 'bg-success-500';
  };

  const getPasswordStrengthLabel = () => {
    if (passwordStrength <= 1) return 'Weak';
    if (passwordStrength <= 2) return 'Fair';
    if (passwordStrength <= 3) return 'Good';
    return 'Strong';
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!name || !email || !password || !confirmPassword) {
      setError('Please fill in all fields');
      return;
    }

    if (!isPasswordValid) {
      setError('Password does not meet requirements');
      return;
    }

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (!tosAccepted) {
      setError('Please accept the Terms of Service and Privacy Policy');
      return;
    }

    const result = await register(email, password, confirmPassword, name);

    if (result.success) {
      // Redirect based on onboarding status
      if (result.needsOnboarding) {
        router.push('/onboarding');
      } else {
        router.push('/home');
      }
    } else {
      // Use specific error message from backend if available
      setError(result.error || 'Registration failed. Please try again.');
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
            <PeppiMascot size="sm" showSpeechBubble speechText="Let's get started!" />
          </motion.div>

          <motion.h1
            variants={fadeInUp}
            className="text-2xl font-bold text-center text-gray-900 mb-2"
          >
            Create Account
          </motion.h1>

          <motion.p
            variants={fadeInUp}
            className="text-center text-gray-500 mb-8"
          >
            Start your language learning journey!
          </motion.p>

          {/* Registration Form */}
          <motion.div variants={fadeInUp}>
            <Card>
              <form onSubmit={handleSubmit} className="space-y-4">
                <Input
                  label="Your Name"
                  type="text"
                  placeholder="Enter your name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  leftIcon={
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z" />
                    </svg>
                  }
                />

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

                <div>
                  <Input
                    label="Password"
                    type="password"
                    placeholder="Create a strong password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    leftIcon={
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 1 0-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 0 0 2.25-2.25v-6.75a2.25 2.25 0 0 0-2.25-2.25H6.75a2.25 2.25 0 0 0-2.25 2.25v6.75a2.25 2.25 0 0 0 2.25 2.25Z" />
                      </svg>
                    }
                  />
                  {/* Password Strength Indicator */}
                  {password.length > 0 && (
                    <div className="mt-2">
                      <div className="flex items-center gap-2 mb-2">
                        <div className="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden">
                          <div
                            className={`h-full transition-all duration-300 ${getPasswordStrengthColor()}`}
                            style={{ width: `${(passwordStrength / 4) * 100}%` }}
                          />
                        </div>
                        <span className={`text-xs font-medium ${
                          passwordStrength <= 1 ? 'text-error-500' :
                          passwordStrength <= 2 ? 'text-warning-500' :
                          passwordStrength <= 3 ? 'text-yellow-600' :
                          'text-success-500'
                        }`}>
                          {getPasswordStrengthLabel()}
                        </span>
                      </div>
                      <div className="grid grid-cols-2 gap-1 text-xs">
                        <div className={passwordChecks.minLength ? 'text-success-600' : 'text-gray-400'}>
                          {passwordChecks.minLength ? '\u2713' : '\u2717'} 8+ characters
                        </div>
                        <div className={passwordChecks.hasUppercase ? 'text-success-600' : 'text-gray-400'}>
                          {passwordChecks.hasUppercase ? '\u2713' : '\u2717'} Uppercase letter
                        </div>
                        <div className={passwordChecks.hasLowercase ? 'text-success-600' : 'text-gray-400'}>
                          {passwordChecks.hasLowercase ? '\u2713' : '\u2717'} Lowercase letter
                        </div>
                        <div className={passwordChecks.hasNumber ? 'text-success-600' : 'text-gray-400'}>
                          {passwordChecks.hasNumber ? '\u2713' : '\u2717'} Number
                        </div>
                      </div>
                    </div>
                  )}
                </div>

                <Input
                  label="Confirm Password"
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

                {error && (
                  <p className="text-error-500 text-sm text-center">{error}</p>
                )}

                {/* ToS Checkbox */}
                <div className="flex items-start gap-3">
                  <input
                    type="checkbox"
                    id="tos"
                    checked={tosAccepted}
                    onChange={(e) => setTosAccepted(e.target.checked)}
                    className="mt-1 w-4 h-4 text-primary-500 border-gray-300 rounded focus:ring-primary-500"
                  />
                  <label htmlFor="tos" className="text-sm text-gray-600">
                    I agree to the{' '}
                    <Link href="/terms" className="text-primary-500 font-semibold hover:underline" target="_blank">
                      Terms of Service
                    </Link>
                    {' '}and{' '}
                    <Link href="/privacy" className="text-primary-500 font-semibold hover:underline" target="_blank">
                      Privacy Policy
                    </Link>
                  </label>
                </div>

                <Button
                  type="submit"
                  size="lg"
                  className="w-full"
                  isLoading={isLoading}
                >
                  Create Account
                </Button>
              </form>

              {/* Social Login */}
              <div className="mt-6">
                <SocialLoginButtons
                  mode="register"
                  onError={(err) => setError(err)}
                />
              </div>

              <div className="mt-6 text-center">
                <p className="text-sm text-gray-500">
                  Already have an account?{' '}
                  <Link href="/login" className="text-primary-500 font-semibold hover:underline">
                    Log in
                  </Link>
                </p>
              </div>
            </Card>
          </motion.div>

          {/* Security Note */}
          <motion.p
            variants={fadeInUp}
            className="mt-6 text-center text-xs text-gray-400"
          >
            Your data is encrypted and secure. We never share your information.
          </motion.p>
        </motion.div>
      </main>
    </div>
  );
}
