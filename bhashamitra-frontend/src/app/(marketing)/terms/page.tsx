'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import { fadeInUp, staggerContainer } from '@/lib/constants';

export default function TermsOfServicePage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-orange-50 via-white to-pink-50">
      {/* Header */}
      <header className="bg-white/95 backdrop-blur-md shadow-sm py-4 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto flex items-center gap-3">
          <Link href="/" className="text-gray-500 hover:text-gray-700">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </Link>
          <h1 className="text-2xl font-bold bg-gradient-to-r from-orange-600 to-pink-600 bg-clip-text text-transparent">
            Terms of Service
          </h1>
        </div>
      </header>

      {/* Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <motion.div
          variants={staggerContainer}
          initial="initial"
          animate="animate"
          className="prose prose-lg max-w-none"
        >
          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8 mb-8">
            <p className="text-sm text-gray-500 mb-4">
              <strong>Last Updated:</strong> 15 December 2025
            </p>
            <p className="text-sm text-gray-500 mb-6">
              <strong>Effective Date:</strong> 15 December 2025
            </p>

            <p className="text-gray-700 mb-6">
              Welcome to PeppiAcademy! These Terms of Service (&quot;Terms&quot;) govern your use of the PeppiAcademy
              website, mobile applications, and related services (collectively, the &quot;Service&quot;) operated by
              PeppiAcademy (&quot;we,&quot; &quot;us,&quot; or &quot;our&quot;).
            </p>

            <p className="text-gray-700 mb-6 bg-blue-50 p-4 rounded-lg">
              <strong>Important:</strong> PeppiAcademy is designed for families. Parents or legal guardians
              must create accounts on behalf of children. By creating an account, you confirm you are at
              least 18 years old and have legal authority to agree to these Terms on behalf of any children
              who will use the Service.
            </p>
          </motion.div>

          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8 mb-8">
            <h2 className="text-2xl font-bold text-teal-800 mb-4">1. Acceptance of Terms</h2>
            <p className="text-gray-700 mb-4">
              By accessing or using PeppiAcademy, you agree to be bound by these Terms and our Privacy Policy.
              If you do not agree to these Terms, please do not use the Service.
            </p>
            <p className="text-gray-700 mb-6">
              These Terms are governed by the laws of New Zealand. For users in Australia, Australian Consumer
              Law rights also apply and cannot be excluded.
            </p>
          </motion.div>

          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8 mb-8">
            <h2 className="text-2xl font-bold text-teal-800 mb-4">2. Eligibility and Accounts</h2>

            <h3 className="text-xl font-semibold text-gray-900 mb-3">2.1 Account Creation</h3>
            <ul className="list-disc pl-6 mb-6 text-gray-700">
              <li>You must be at least 18 years old to create an account</li>
              <li>You must be a parent or legal guardian to create child profiles</li>
              <li>You are responsible for maintaining the confidentiality of your account</li>
              <li>You must provide accurate and complete information</li>
              <li>You are responsible for all activities under your account</li>
            </ul>

            <h3 className="text-xl font-semibold text-gray-900 mb-3">2.2 Child Profiles</h3>
            <ul className="list-disc pl-6 mb-6 text-gray-700">
              <li>Child profiles can only be created by parents/guardians</li>
              <li>You must have legal authority over any child whose profile you create</li>
              <li>You are responsible for supervising your child&apos;s use of the Service</li>
              <li>Children cannot directly communicate with other users</li>
            </ul>
          </motion.div>

          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8 mb-8">
            <h2 className="text-2xl font-bold text-teal-800 mb-4">3. Service Description</h2>
            <p className="text-gray-700 mb-4">PeppiAcademy provides:</p>
            <ul className="list-disc pl-6 mb-6 text-gray-700">
              <li>Interactive language learning content for Indian languages</li>
              <li>Stories, games, and educational activities</li>
              <li>Progress tracking and achievement systems</li>
              <li>Text-to-speech narration features</li>
              <li>Parent dashboard for monitoring children&apos;s learning</li>
            </ul>
            <p className="text-gray-700 mb-6">
              We may modify, suspend, or discontinue any aspect of the Service at any time. We will
              provide reasonable notice of significant changes.
            </p>
          </motion.div>

          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8 mb-8">
            <h2 className="text-2xl font-bold text-teal-800 mb-4">4. Subscription and Payments</h2>

            <h3 className="text-xl font-semibold text-gray-900 mb-3">4.1 Free Tier</h3>
            <p className="text-gray-700 mb-4">
              We offer a free tier with limited access to content and features.
            </p>

            <h3 className="text-xl font-semibold text-gray-900 mb-3">4.2 Paid Subscriptions</h3>
            <ul className="list-disc pl-6 mb-6 text-gray-700">
              <li>Paid subscriptions are billed monthly or annually as selected</li>
              <li>Prices are displayed in New Zealand Dollars (NZD) or Australian Dollars (AUD)</li>
              <li>Subscriptions auto-renew unless cancelled before the renewal date</li>
              <li>No refunds for partial billing periods (unless required by law)</li>
            </ul>

            <h3 className="text-xl font-semibold text-gray-900 mb-3">4.3 Cancellation</h3>
            <ul className="list-disc pl-6 mb-6 text-gray-700">
              <li>You may cancel your subscription at any time through your account settings</li>
              <li>Cancellation takes effect at the end of the current billing period</li>
              <li>You retain access to paid features until the end of your paid period</li>
            </ul>

            <h3 className="text-xl font-semibold text-gray-900 mb-3">4.4 Australian Consumer Law</h3>
            <p className="text-gray-700 mb-6 bg-green-50 p-4 rounded-lg">
              If you are an Australian consumer, you have statutory rights under the Australian Consumer Law
              that cannot be excluded. These Terms do not limit those rights. You may be entitled to a refund
              if the Service has a major problem.
            </p>
          </motion.div>

          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8 mb-8">
            <h2 className="text-2xl font-bold text-teal-800 mb-4">5. Acceptable Use</h2>
            <p className="text-gray-700 mb-4">You agree NOT to:</p>
            <ul className="list-disc pl-6 mb-6 text-gray-700">
              <li>Use the Service for any unlawful purpose</li>
              <li>Share your account with others or create multiple accounts</li>
              <li>Attempt to gain unauthorized access to the Service</li>
              <li>Copy, modify, or distribute our content without permission</li>
              <li>Interfere with or disrupt the Service or servers</li>
              <li>Use automated systems to access the Service (bots, scrapers)</li>
              <li>Upload any malicious content or viruses</li>
              <li>Impersonate another person or entity</li>
              <li>Collect personal information from other users</li>
            </ul>
          </motion.div>

          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8 mb-8">
            <h2 className="text-2xl font-bold text-teal-800 mb-4">6. Intellectual Property</h2>

            <h3 className="text-xl font-semibold text-gray-900 mb-3">6.1 Our Content</h3>
            <p className="text-gray-700 mb-4">
              The Service and its original content (excluding user content), features, and functionality
              are owned by PeppiAcademy and are protected by copyright, trademark, and other intellectual
              property laws.
            </p>

            <h3 className="text-xl font-semibold text-gray-900 mb-3">6.2 Third-Party Content</h3>
            <p className="text-gray-700 mb-4">
              Some stories and educational content may be sourced from third parties under Creative Commons
              licenses (CC-BY 4.0). Attribution is provided where required.
            </p>

            <h3 className="text-xl font-semibold text-gray-900 mb-3">6.3 License to Use</h3>
            <p className="text-gray-700 mb-6">
              We grant you a limited, non-exclusive, non-transferable license to access and use the Service
              for personal, non-commercial educational purposes.
            </p>
          </motion.div>

          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8 mb-8">
            <h2 className="text-2xl font-bold text-teal-800 mb-4">7. Privacy</h2>
            <p className="text-gray-700 mb-6">
              Your privacy is important to us. Please review our{' '}
              <Link href="/privacy" className="text-primary-600 hover:text-primary-700">
                Privacy Policy
              </Link>{' '}
              and{' '}
              <Link href="/childrens-privacy" className="text-primary-600 hover:text-primary-700">
                Children&apos;s Privacy Policy
              </Link>{' '}
              to understand how we collect, use, and protect your information.
            </p>
          </motion.div>

          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8 mb-8">
            <h2 className="text-2xl font-bold text-teal-800 mb-4">8. Disclaimers and Limitations</h2>

            <h3 className="text-xl font-semibold text-gray-900 mb-3">8.1 Service Availability</h3>
            <p className="text-gray-700 mb-4">
              The Service is provided &quot;as is&quot; and &quot;as available.&quot; We do not guarantee uninterrupted or
              error-free service. We may experience downtime for maintenance or updates.
            </p>

            <h3 className="text-xl font-semibold text-gray-900 mb-3">8.2 Educational Content</h3>
            <p className="text-gray-700 mb-4">
              While we strive to provide accurate language learning content, we do not guarantee that
              using PeppiAcademy will result in specific learning outcomes. Language learning depends on
              individual effort and practice.
            </p>

            <h3 className="text-xl font-semibold text-gray-900 mb-3">8.3 Limitation of Liability</h3>
            <p className="text-gray-700 mb-6">
              To the maximum extent permitted by law, PeppiAcademy shall not be liable for any indirect,
              incidental, special, consequential, or punitive damages arising from your use of the Service.
              Our total liability shall not exceed the amount you paid for the Service in the 12 months
              prior to the claim.
            </p>

            <p className="text-gray-700 mb-6 bg-yellow-50 p-4 rounded-lg">
              <strong>Consumer Guarantees:</strong> Nothing in these Terms excludes or limits any consumer
              rights under the Consumer Guarantees Act 1993 (New Zealand) or Australian Consumer Law that
              cannot be excluded or limited by law.
            </p>
          </motion.div>

          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8 mb-8">
            <h2 className="text-2xl font-bold text-teal-800 mb-4">9. Indemnification</h2>
            <p className="text-gray-700 mb-6">
              You agree to indemnify and hold PeppiAcademy harmless from any claims, damages, losses, or
              expenses (including legal fees) arising from your use of the Service, violation of these
              Terms, or infringement of any third-party rights.
            </p>
          </motion.div>

          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8 mb-8">
            <h2 className="text-2xl font-bold text-teal-800 mb-4">10. Termination</h2>
            <ul className="list-disc pl-6 mb-6 text-gray-700">
              <li>You may terminate your account at any time through account settings</li>
              <li>We may suspend or terminate your account for violation of these Terms</li>
              <li>Upon termination, your right to use the Service ceases immediately</li>
              <li>Provisions that should survive termination will remain in effect</li>
            </ul>
          </motion.div>

          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8 mb-8">
            <h2 className="text-2xl font-bold text-teal-800 mb-4">11. Changes to Terms</h2>
            <p className="text-gray-700 mb-6">
              We may update these Terms from time to time. We will notify you of material changes by
              posting the new Terms on this page and updating the &quot;Last Updated&quot; date. Your continued
              use of the Service after changes constitutes acceptance of the updated Terms.
            </p>
          </motion.div>

          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8 mb-8">
            <h2 className="text-2xl font-bold text-teal-800 mb-4">12. Dispute Resolution</h2>

            <h3 className="text-xl font-semibold text-gray-900 mb-3">12.1 Governing Law</h3>
            <p className="text-gray-700 mb-4">
              These Terms are governed by the laws of New Zealand. For users in Australia, applicable
              Australian laws also apply.
            </p>

            <h3 className="text-xl font-semibold text-gray-900 mb-3">12.2 Informal Resolution</h3>
            <p className="text-gray-700 mb-4">
              Before pursuing formal legal action, you agree to first contact us and attempt to resolve
              the dispute informally for at least 30 days.
            </p>

            <h3 className="text-xl font-semibold text-gray-900 mb-3">12.3 Jurisdiction</h3>
            <p className="text-gray-700 mb-6">
              Any legal proceedings shall be conducted in the courts of Auckland, New Zealand, or in
              your local jurisdiction if required by law.
            </p>
          </motion.div>

          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8 mb-8">
            <h2 className="text-2xl font-bold text-teal-800 mb-4">13. General Provisions</h2>
            <ul className="list-disc pl-6 mb-6 text-gray-700">
              <li><strong>Entire Agreement:</strong> These Terms, along with our Privacy Policy, constitute the entire agreement between you and PeppiAcademy</li>
              <li><strong>Severability:</strong> If any provision is found unenforceable, the remaining provisions remain in effect</li>
              <li><strong>Waiver:</strong> Our failure to enforce any right does not constitute a waiver</li>
              <li><strong>Assignment:</strong> You may not assign your rights without our consent</li>
              <li><strong>Force Majeure:</strong> We are not liable for delays due to circumstances beyond our control</li>
            </ul>
          </motion.div>

          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8">
            <h2 className="text-2xl font-bold text-teal-800 mb-4">14. Contact Us</h2>
            <p className="text-gray-700 mb-4">
              If you have questions about these Terms, please contact us:
            </p>
            <div className="bg-gray-50 p-6 rounded-lg">
              <p className="text-gray-700 mb-2"><strong>PeppiAcademy</strong></p>
              <p className="text-gray-700 mb-2">Email: legal@bhashamitra.co.nz</p>
              <p className="text-gray-700">Address: Auckland, New Zealand</p>
            </div>
          </motion.div>
        </motion.div>
      </main>

      {/* Footer */}
      <footer className="bg-teal-800 text-white py-8 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <p className="text-white/60 text-sm">
            © 2025 PeppiAcademy. Made with care in Auckland, New Zealand
          </p>
          <div className="mt-4 flex justify-center gap-6 text-sm">
            <Link href="/privacy" className="text-white/80 hover:text-yellow-400 transition-colors">
              Privacy Policy
            </Link>
            <Link href="/terms" className="text-white/80 hover:text-yellow-400 transition-colors">
              Terms of Service
            </Link>
            <Link href="/childrens-privacy" className="text-white/80 hover:text-yellow-400 transition-colors">
              Children&apos;s Privacy
            </Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
