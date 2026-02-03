'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import dynamic from 'next/dynamic';
import { useAuthStore } from '@/stores';
import { motion } from 'framer-motion';
import type { CredentialResponse } from '@react-oauth/google';

// Dynamically import GoogleLogin to avoid SSR issues
const GoogleLogin = dynamic(
  () => import('@react-oauth/google').then((mod) => mod.GoogleLogin),
  {
    ssr: false,
    loading: () => (
      <div className="w-full py-3 px-4 border border-gray-300 rounded-lg bg-gray-50 text-center">
        <span className="text-gray-400">Loading...</span>
      </div>
    ),
  }
);

interface SocialLoginButtonsProps {
  mode: 'login' | 'register';
  onError?: (error: string) => void;
  onSuccess?: () => void;
}

export function SocialLoginButtons({ mode, onError, onSuccess }: SocialLoginButtonsProps) {
  const router = useRouter();
  const { googleLogin } = useAuthStore();
  const [isLoading, setIsLoading] = useState(false);
  const [isMounted, setIsMounted] = useState(false);

  // Only render Google Login on client side
  useEffect(() => {
    setIsMounted(true);
  }, []);

  const handleGoogleSuccess = async (credentialResponse: CredentialResponse) => {
    if (!credentialResponse.credential) {
      onError?.('No credential received from Google');
      return;
    }

    setIsLoading(true);

    try {
      const result = await googleLogin(credentialResponse.credential);

      if (result.success) {
        onSuccess?.();
        // Redirect based on onboarding status
        if (result.needsOnboarding) {
          router.push('/onboarding');
        } else {
          router.push('/home');
        }
      } else {
        onError?.(result.error || 'Google authentication failed. Please try again.');
      }
    } catch (error) {
      onError?.(error instanceof Error ? error.message : 'An unexpected error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const handleGoogleError = () => {
    onError?.('Google sign-in was cancelled or failed');
  };

  // Don't render anything during SSR
  if (!isMounted) {
    return null;
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2 }}
      className="space-y-4"
    >
      {/* Divider */}
      <div className="relative">
        <div className="absolute inset-0 flex items-center">
          <div className="w-full border-t border-gray-300"></div>
        </div>
        <div className="relative flex justify-center text-sm">
          <span className="px-2 bg-white text-gray-500">
            {mode === 'login' ? 'Or log in with' : 'Or sign up with'}
          </span>
        </div>
      </div>

      {/* Google Sign-In Button */}
      <div className="flex justify-center">
        {isLoading ? (
          <div className="flex items-center justify-center w-full py-3 px-4 border border-gray-300 rounded-lg bg-gray-50">
            <svg
              className="animate-spin h-5 w-5 text-gray-500 mr-2"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
            <span className="text-gray-600">Signing in...</span>
          </div>
        ) : (
          <GoogleLogin
            onSuccess={handleGoogleSuccess}
            onError={handleGoogleError}
            useOneTap={false}
            theme="outline"
            size="large"
            text={mode === 'login' ? 'signin_with' : 'signup_with'}
            shape="rectangular"
            logo_alignment="left"
          />
        )}
      </div>
    </motion.div>
  );
}

export default SocialLoginButtons;
