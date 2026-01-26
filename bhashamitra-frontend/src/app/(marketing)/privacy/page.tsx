'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import { fadeInUp, staggerContainer } from '@/lib/constants';

export default function PrivacyPolicyPage() {
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
            Privacy Policy
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
              PeppiAcademy (&quot;we,&quot; &quot;us,&quot; or &quot;our&quot;) is committed to protecting the privacy of our users,
              especially children. This Privacy Policy explains how we collect, use, disclose, and safeguard
              your information when you use our language learning platform.
            </p>

            <p className="text-gray-700 mb-6">
              <strong>Our Commitment:</strong> We are designed for families with children. We follow strict data
              protection principles in accordance with:
            </p>
            <ul className="list-disc pl-6 mb-6 text-gray-700">
              <li>New Zealand Privacy Act 2020</li>
              <li>Australia Privacy Act 1988 (including the Australian Privacy Principles)</li>
              <li>Children&apos;s Online Privacy Protection Act (COPPA) of the United States</li>
              <li>Upcoming Australia Children&apos;s Online Privacy Code (OAIC)</li>
            </ul>
          </motion.div>

          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8 mb-8">
            <h2 className="text-2xl font-bold text-teal-800 mb-4">1. Information We Collect</h2>

            <h3 className="text-xl font-semibold text-gray-900 mb-3">1.1 Parent/Guardian Account Information</h3>
            <p className="text-gray-700 mb-4">When parents or guardians create an account, we collect:</p>
            <ul className="list-disc pl-6 mb-6 text-gray-700">
              <li>Email address</li>
              <li>Name</li>
              <li>Password (stored securely using encryption)</li>
              <li>Payment information (processed by our payment provider, not stored by us)</li>
            </ul>

            <h3 className="text-xl font-semibold text-gray-900 mb-3">1.2 Child Profile Information</h3>
            <p className="text-gray-700 mb-4">
              For each child profile created by a parent/guardian, we collect:
            </p>
            <ul className="list-disc pl-6 mb-6 text-gray-700">
              <li>First name or nickname (we recommend using a nickname)</li>
              <li>Age range (not exact date of birth)</li>
              <li>Learning language preference</li>
              <li>Avatar selection</li>
            </ul>
            <p className="text-gray-700 mb-6 bg-yellow-50 p-4 rounded-lg">
              <strong>Important:</strong> We do NOT collect children&apos;s email addresses, photos, physical
              addresses, phone numbers, or any other personally identifiable information directly from children.
            </p>

            <h3 className="text-xl font-semibold text-gray-900 mb-3">1.3 Learning Activity Data</h3>
            <p className="text-gray-700 mb-4">To provide our educational service, we automatically collect:</p>
            <ul className="list-disc pl-6 mb-6 text-gray-700">
              <li>Stories read and progress</li>
              <li>Vocabulary words learned</li>
              <li>Game scores and achievements</li>
              <li>Time spent learning</li>
              <li>Learning streaks and badges earned</li>
            </ul>

            <h3 className="text-xl font-semibold text-gray-900 mb-3">1.4 Technical Information</h3>
            <ul className="list-disc pl-6 mb-6 text-gray-700">
              <li>Device type and operating system</li>
              <li>Browser type</li>
              <li>IP address (anonymized for analytics)</li>
              <li>General location (country/region level only)</li>
            </ul>
          </motion.div>

          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8 mb-8">
            <h2 className="text-2xl font-bold text-teal-800 mb-4">2. How We Use Information</h2>
            <p className="text-gray-700 mb-4">We use the collected information to:</p>
            <ul className="list-disc pl-6 mb-6 text-gray-700">
              <li>Provide and personalize the learning experience</li>
              <li>Track learning progress and achievements</li>
              <li>Allow parents to monitor their children&apos;s progress</li>
              <li>Send progress reports to parents (not children)</li>
              <li>Improve our educational content and platform</li>
              <li>Ensure security and prevent fraud</li>
              <li>Comply with legal obligations</li>
            </ul>
            <p className="text-gray-700 mb-6 bg-green-50 p-4 rounded-lg">
              <strong>Data Minimization:</strong> We only collect information that is necessary for providing
              our educational service. We follow the principle of collecting the minimum amount of data needed.
            </p>
          </motion.div>

          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8 mb-8">
            <h2 className="text-2xl font-bold text-teal-800 mb-4">3. Parental Consent</h2>
            <p className="text-gray-700 mb-4">
              In accordance with COPPA and NZ/AU privacy laws:
            </p>
            <ul className="list-disc pl-6 mb-6 text-gray-700">
              <li>Only parents/guardians can create accounts</li>
              <li>Parents must provide verifiable consent before creating child profiles</li>
              <li>Children cannot create their own accounts</li>
              <li>Parents can review, modify, or delete their children&apos;s information at any time</li>
              <li>Parents can withdraw consent and request deletion of their children&apos;s data</li>
            </ul>
            <p className="text-gray-700 mb-6">
              <strong>Consent Verification:</strong> We verify parental consent through our account creation
              process. For additional verification in certain cases, we may use email verification or payment
              method verification.
            </p>
          </motion.div>

          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8 mb-8">
            <h2 className="text-2xl font-bold text-teal-800 mb-4">4. Information Sharing</h2>
            <p className="text-gray-700 mb-4">
              <strong>We do NOT sell, rent, or trade personal information.</strong>
            </p>
            <p className="text-gray-700 mb-4">We may share information only in these limited circumstances:</p>
            <ul className="list-disc pl-6 mb-6 text-gray-700">
              <li><strong>Service Providers:</strong> With trusted third parties who help us operate our platform
                (e.g., hosting, payment processing), under strict confidentiality agreements</li>
              <li><strong>Legal Requirements:</strong> When required by law, court order, or government request</li>
              <li><strong>Safety:</strong> To protect the safety of children, users, or the public</li>
              <li><strong>Business Transfers:</strong> In connection with a merger or acquisition, with the same
                privacy protections maintained</li>
            </ul>
          </motion.div>

          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8 mb-8">
            <h2 className="text-2xl font-bold text-teal-800 mb-4">5. Data Security</h2>
            <p className="text-gray-700 mb-4">We implement robust security measures including:</p>
            <ul className="list-disc pl-6 mb-6 text-gray-700">
              <li>Encryption of data in transit (TLS/SSL) and at rest</li>
              <li>Secure password hashing</li>
              <li>Regular security audits and updates</li>
              <li>Access controls and authentication</li>
              <li>Secure cloud infrastructure (AWS/Cloudflare)</li>
            </ul>
            <p className="text-gray-700 mb-6">
              While we strive to protect your information, no method of transmission over the Internet is
              100% secure. We will notify affected users of any data breach as required by law.
            </p>
          </motion.div>

          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8 mb-8">
            <h2 className="text-2xl font-bold text-teal-800 mb-4">6. Data Retention</h2>
            <ul className="list-disc pl-6 mb-6 text-gray-700">
              <li>Active accounts: Data is retained while the account is active</li>
              <li>Deleted accounts: Personal data is deleted within 30 days of account deletion request</li>
              <li>Learning progress data may be anonymized and retained for educational research</li>
              <li>Legal obligations may require certain data to be retained for specified periods</li>
            </ul>
          </motion.div>

          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8 mb-8" id="cookies">
            <h2 className="text-2xl font-bold text-teal-800 mb-4">7. Cookies and Tracking</h2>
            <p className="text-gray-700 mb-4">We use essential cookies for:</p>
            <ul className="list-disc pl-6 mb-6 text-gray-700">
              <li>Authentication and session management</li>
              <li>Remembering user preferences</li>
              <li>Security purposes</li>
            </ul>
            <p className="text-gray-700 mb-4">We use analytics cookies (with consent) for:</p>
            <ul className="list-disc pl-6 mb-6 text-gray-700">
              <li>Understanding how users interact with our platform</li>
              <li>Improving our educational content</li>
            </ul>
            <p className="text-gray-700 mb-6">
              <strong>No Behavioral Advertising:</strong> We do NOT use cookies for behavioral advertising
              or tracking children across websites.
            </p>
          </motion.div>

          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8 mb-8">
            <h2 className="text-2xl font-bold text-teal-800 mb-4">8. Your Rights</h2>

            <h3 className="text-xl font-semibold text-gray-900 mb-3">New Zealand Residents</h3>
            <p className="text-gray-700 mb-4">Under the Privacy Act 2020, you have the right to:</p>
            <ul className="list-disc pl-6 mb-6 text-gray-700">
              <li>Access your personal information</li>
              <li>Request correction of inaccurate information</li>
              <li>Request deletion of your information</li>
              <li>Lodge a complaint with the Privacy Commissioner</li>
            </ul>

            <h3 className="text-xl font-semibold text-gray-900 mb-3">Australian Residents</h3>
            <p className="text-gray-700 mb-4">Under the Privacy Act 1988, you have the right to:</p>
            <ul className="list-disc pl-6 mb-6 text-gray-700">
              <li>Access your personal information</li>
              <li>Request correction of inaccurate information</li>
              <li>Lodge a complaint with the OAIC</li>
              <li>Opt out of direct marketing</li>
            </ul>

            <h3 className="text-xl font-semibold text-gray-900 mb-3">Parents/Guardians</h3>
            <p className="text-gray-700 mb-4">You have additional rights regarding your children&apos;s data:</p>
            <ul className="list-disc pl-6 mb-6 text-gray-700">
              <li>Review your child&apos;s personal information</li>
              <li>Request deletion of your child&apos;s data</li>
              <li>Refuse further collection of your child&apos;s data</li>
              <li>Withdraw consent at any time</li>
            </ul>
          </motion.div>

          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8 mb-8">
            <h2 className="text-2xl font-bold text-teal-800 mb-4">9. International Data Transfers</h2>
            <p className="text-gray-700 mb-6">
              Our servers are located in Australia and New Zealand. If you access our service from outside
              these countries, your information may be transferred to and processed in these locations.
              We ensure appropriate safeguards are in place for any international data transfers.
            </p>
          </motion.div>

          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8 mb-8">
            <h2 className="text-2xl font-bold text-teal-800 mb-4">10. Changes to This Policy</h2>
            <p className="text-gray-700 mb-6">
              We may update this Privacy Policy from time to time. We will notify you of any material changes
              by posting the new policy on this page and updating the &quot;Last Updated&quot; date. For significant
              changes affecting children&apos;s data, we will seek renewed parental consent where required.
            </p>
          </motion.div>

          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8">
            <h2 className="text-2xl font-bold text-teal-800 mb-4">11. Contact Us</h2>
            <p className="text-gray-700 mb-4">
              If you have questions about this Privacy Policy or wish to exercise your rights, please contact us:
            </p>
            <div className="bg-gray-50 p-6 rounded-lg">
              <p className="text-gray-700 mb-2"><strong>PeppiAcademy Privacy Team</strong></p>
              <p className="text-gray-700 mb-2">Email: privacy@bhashamitra.co.nz</p>
              <p className="text-gray-700 mb-2">Address: Auckland, New Zealand</p>
            </div>
            <p className="text-gray-700 mt-6">
              <strong>For complaints (New Zealand):</strong><br />
              Office of the Privacy Commissioner<br />
              Website: privacy.org.nz
            </p>
            <p className="text-gray-700 mt-4">
              <strong>For complaints (Australia):</strong><br />
              Office of the Australian Information Commissioner (OAIC)<br />
              Website: oaic.gov.au
            </p>
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
