'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { Button, Card } from '@/components/ui';
import { fadeInUp, staggerContainer } from '@/lib/constants';

interface FAQ {
  question: string;
  answer: string;
}

const faqs: FAQ[] = [
  {
    question: 'What is XP and how do I earn it?',
    answer: 'XP (Experience Points) are earned by completing lessons, playing games, and practicing with Peppi. Each word learned gives you 5 XP, completing games gives 25 XP, and finishing stories gives 50 XP. You need 100 XP to level up!',
  },
  {
    question: 'How do streaks work?',
    answer: 'Streaks track consecutive days of learning. Log in and complete at least one activity each day to maintain your streak. Longer streaks earn you bonus XP and special badges!',
  },
  {
    question: 'What is Mimic and how do I use it?',
    answer: "Mimic is our pronunciation practice feature powered by Peppi. Listen to a phrase, record yourself saying it, and get instant feedback on your pronunciation. It's a fun way to improve your speaking skills!",
  },
  {
    question: 'How do I add another child to my account?',
    answer: "Go to your Profile, look for the 'Add Child' option in the settings section. Each child can have their own learning journey with personalized progress tracking.",
  },
  {
    question: 'Can I change the language my child is learning?',
    answer: 'Yes! Go to Profile > Language Settings to change the learning language. Progress is tracked separately for each language.',
  },
  {
    question: 'What are the subscription tiers?',
    answer: 'FREE tier includes pre-cached content and basic features. STANDARD (NZD $20/month) unlocks unlimited games, full L1-L10 curriculum, and Peppi AI. PREMIUM (NZD $30/month) adds live classes, premium voice narration, and priority support.',
  },
  {
    question: 'How do I cancel or upgrade my subscription?',
    answer: 'Visit the Profile page and click on the Subscription section to manage your plan. You can upgrade, downgrade, or cancel at any time.',
  },
  {
    question: 'Is my child\'s data safe?',
    answer: 'Absolutely! We take privacy seriously. We never share personal data with third parties. All learning progress is encrypted and stored securely.',
  },
];

export default function HelpPage() {
  const router = useRouter();
  const [openFaq, setOpenFaq] = useState<number | null>(null);

  const toggleFaq = (index: number) => {
    setOpenFaq(openFaq === index ? null : index);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-primary-50 via-white to-secondary-50">
      {/* Header */}
      <header className="p-4">
        <Button
          variant="ghost"
          size="sm"
          onClick={() => router.push('/profile')}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={2}
            stroke="currentColor"
            className="w-5 h-5 mr-2"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M15.75 19.5 8.25 12l7.5-7.5"
            />
          </svg>
          Back to Profile
        </Button>
      </header>

      {/* Main Content */}
      <main className="px-6 py-8 max-w-3xl mx-auto">
        <motion.div
          variants={staggerContainer}
          initial="initial"
          animate="animate"
          className="space-y-8"
        >
          {/* Page Title */}
          <motion.div variants={fadeInUp} className="text-center">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Help & Support
            </h1>
            <p className="text-gray-500">Find answers to common questions</p>
          </motion.div>

          {/* FAQ Section */}
          <motion.div variants={fadeInUp}>
            <h2 className="text-xl font-bold text-gray-900 mb-4">
              Frequently Asked Questions
            </h2>
            <div className="space-y-3">
              {faqs.map((faq, index) => (
                <Card
                  key={index}
                  interactive
                  onClick={() => toggleFaq(index)}
                  className="cursor-pointer"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1">
                      <h3 className="font-semibold text-gray-900 mb-1">
                        {faq.question}
                      </h3>
                      {openFaq === index && (
                        <motion.p
                          initial={{ opacity: 0, height: 0 }}
                          animate={{ opacity: 1, height: 'auto' }}
                          exit={{ opacity: 0, height: 0 }}
                          className="text-gray-600 text-sm mt-2"
                        >
                          {faq.answer}
                        </motion.p>
                      )}
                    </div>
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      strokeWidth={2}
                      stroke="currentColor"
                      className={`w-5 h-5 text-gray-400 transition-transform flex-shrink-0 ${
                        openFaq === index ? 'rotate-180' : ''
                      }`}
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="m19.5 8.25-7.5 7.5-7.5-7.5"
                      />
                    </svg>
                  </div>
                </Card>
              ))}
            </div>
          </motion.div>

          {/* Contact Support Section */}
          <motion.div variants={fadeInUp}>
            <h2 className="text-xl font-bold text-gray-900 mb-4">
              Still Need Help?
            </h2>
            <Card className="text-center">
              <div className="text-4xl mb-3">📧</div>
              <h3 className="font-bold text-gray-900 mb-2">
                Contact Our Support Team
              </h3>
              <p className="text-gray-600 text-sm mb-4">
                We&apos;re here to help! Email us and we&apos;ll get back to you
                within 24 hours.
              </p>
              <a
                href="mailto:support@bhashamitra.co.nz"
                className="text-primary-500 font-semibold hover:underline"
              >
                support@bhashamitra.co.nz
              </a>
            </Card>
          </motion.div>

          {/* Legal Links */}
          <motion.div
            variants={fadeInUp}
            className="text-center text-sm text-gray-500 pt-4"
          >
            <Link href="/terms" className="hover:text-primary-500 underline">
              Terms of Service
            </Link>
            <span className="mx-2">•</span>
            <Link href="/privacy" className="hover:text-primary-500 underline">
              Privacy Policy
            </Link>
          </motion.div>
        </motion.div>
      </main>
    </div>
  );
}
