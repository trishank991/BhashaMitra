'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import { fadeInUp, staggerContainer } from '@/lib/constants';

export default function ChildrensPrivacyPage() {
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
            Children&apos;s Privacy
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
          {/* Hero Banner */}
          <motion.div variants={fadeInUp} className="bg-gradient-to-r from-purple-500 to-pink-500 rounded-3xl p-8 mb-8 text-white text-center">
            <span className="text-6xl mb-4 block">🛡️</span>
            <h2 className="text-3xl font-bold text-white mb-2">Protecting Your Child&apos;s Privacy</h2>
            <p className="text-white/90">
              PeppiAcademy is committed to the safety and privacy of children who use our platform
            </p>
          </motion.div>

          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8 mb-8">
            <p className="text-sm text-gray-500 mb-4">
              <strong>Last Updated:</strong> 15 December 2025
            </p>
            <p className="text-sm text-gray-500 mb-6">
              <strong>Effective Date:</strong> 15 December 2025
            </p>

            <p className="text-gray-700 mb-6">
              This Children&apos;s Privacy Policy supplements our general{' '}
              <Link href="/privacy" className="text-primary-600 hover:text-primary-700">
                Privacy Policy
              </Link>{' '}
              and specifically addresses how we collect, use, and protect information from children under 16
              years of age who use PeppiAcademy.
            </p>

            <div className="bg-blue-50 p-6 rounded-lg mb-6">
              <h3 className="text-lg font-bold text-blue-800 mb-3">Our Compliance Framework</h3>
              <ul className="list-disc pl-6 text-blue-800">
                <li><strong>COPPA</strong> - Children&apos;s Online Privacy Protection Act (United States)</li>
                <li><strong>NZ Privacy Act 2020</strong> - Heightened protections for children&apos;s data (New Zealand)</li>
                <li><strong>AU Privacy Act 1988</strong> - Australian Privacy Principles with children&apos;s considerations</li>
                <li><strong>OAIC Children&apos;s Online Privacy Code</strong> - Upcoming Australian requirements (2026)</li>
              </ul>
            </div>
          </motion.div>

          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8 mb-8">
            <h2 className="text-2xl font-bold text-teal-800 mb-4">1. Our Child-Safe Design Principles</h2>
            <p className="text-gray-700 mb-4">
              PeppiAcademy is designed from the ground up with children&apos;s safety in mind:
            </p>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="bg-green-50 p-4 rounded-lg">
                <span className="text-2xl mb-2 block">👨‍👩‍👧</span>
                <h4 className="font-bold text-green-800">Parent-Controlled Access</h4>
                <p className="text-sm text-green-700">Only parents can create accounts and child profiles</p>
              </div>
              <div className="bg-purple-50 p-4 rounded-lg">
                <span className="text-2xl mb-2 block">🚫</span>
                <h4 className="font-bold text-purple-800">No Social Features</h4>
                <p className="text-sm text-purple-700">Children cannot chat, message, or interact with others</p>
              </div>
              <div className="bg-orange-50 p-4 rounded-lg">
                <span className="text-2xl mb-2 block">🔒</span>
                <h4 className="font-bold text-orange-800">Minimal Data Collection</h4>
                <p className="text-sm text-orange-700">We only collect what&apos;s necessary for learning</p>
              </div>
              <div className="bg-pink-50 p-4 rounded-lg">
                <span className="text-2xl mb-2 block">📵</span>
                <h4 className="font-bold text-pink-800">No Targeted Advertising</h4>
                <p className="text-sm text-pink-700">We never show ads to children or track for advertising</p>
              </div>
            </div>
          </motion.div>

          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8 mb-8">
            <h2 className="text-2xl font-bold text-teal-800 mb-4">2. Information We Collect from Children</h2>

            <h3 className="text-xl font-semibold text-gray-900 mb-3">2.1 What We DO Collect</h3>
            <table className="w-full mb-6">
              <thead>
                <tr className="bg-gray-50">
                  <th className="text-left p-3 font-semibold">Data Type</th>
                  <th className="text-left p-3 font-semibold">Purpose</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-b">
                  <td className="p-3">First name or nickname</td>
                  <td className="p-3">Personalize the learning experience</td>
                </tr>
                <tr className="border-b">
                  <td className="p-3">Age range (e.g., 4-6, 7-9)</td>
                  <td className="p-3">Provide age-appropriate content</td>
                </tr>
                <tr className="border-b">
                  <td className="p-3">Learning language choice</td>
                  <td className="p-3">Show relevant curriculum</td>
                </tr>
                <tr className="border-b">
                  <td className="p-3">Learning progress</td>
                  <td className="p-3">Track achievements, stories read, words learned</td>
                </tr>
                <tr className="border-b">
                  <td className="p-3">Avatar selection</td>
                  <td className="p-3">Visual personalization</td>
                </tr>
              </tbody>
            </table>

            <h3 className="text-xl font-semibold text-gray-900 mb-3">2.2 What We DO NOT Collect from Children</h3>
            <div className="bg-red-50 p-6 rounded-lg mb-6">
              <p className="text-red-800 font-semibold mb-2">We NEVER collect:</p>
              <ul className="list-disc pl-6 text-red-700">
                <li>Full name or surname</li>
                <li>Date of birth (only age range)</li>
                <li>Email address</li>
                <li>Physical address</li>
                <li>Phone number</li>
                <li>Photos or videos</li>
                <li>Location data</li>
                <li>Voice recordings</li>
                <li>Social media handles</li>
                <li>School name or class</li>
              </ul>
            </div>
          </motion.div>

          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8 mb-8">
            <h2 className="text-2xl font-bold text-teal-800 mb-4">3. Parental Consent (COPPA/NZ/AU Compliance)</h2>

            <h3 className="text-xl font-semibold text-gray-900 mb-3">3.1 Verifiable Parental Consent</h3>
            <p className="text-gray-700 mb-4">
              Before any child profile can be created, we require verifiable parental consent:
            </p>
            <ul className="list-disc pl-6 mb-6 text-gray-700">
              <li>Only adults (18+) can create parent accounts</li>
              <li>Email verification confirms adult account holder</li>
              <li>Payment method verification (for paid plans) provides additional consent verification</li>
              <li>Parents explicitly agree to allow child profile creation</li>
            </ul>

            <h3 className="text-xl font-semibold text-gray-900 mb-3">3.2 Enhanced Consent Notice (COPPA 2025)</h3>
            <p className="text-gray-700 mb-4">
              In compliance with COPPA 2025 amendments, we provide clear notice of:
            </p>
            <ul className="list-disc pl-6 mb-6 text-gray-700">
              <li>What information we collect from children</li>
              <li>How we use that information</li>
              <li>Whether information is disclosed to third parties</li>
              <li>Parent&apos;s right to review, delete, and control their child&apos;s information</li>
              <li>Contact information for our privacy team</li>
            </ul>

            <h3 className="text-xl font-semibold text-gray-900 mb-3">3.3 New Zealand Privacy Act 2020 Compliance</h3>
            <p className="text-gray-700 mb-6">
              Under IPP 4, we apply &quot;heightened fairness&quot; standards when collecting information from or
              about children. We ensure collection is fair and reasonable given the child&apos;s age and that
              parents are fully informed.
            </p>
          </motion.div>

          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8 mb-8">
            <h2 className="text-2xl font-bold text-teal-800 mb-4">4. How We Use Children&apos;s Information</h2>
            <p className="text-gray-700 mb-4">Children&apos;s information is used ONLY to:</p>
            <ul className="list-disc pl-6 mb-6 text-gray-700">
              <li>Provide the educational language learning service</li>
              <li>Track learning progress and award achievements</li>
              <li>Display age-appropriate content</li>
              <li>Show progress to parents in the parent dashboard</li>
              <li>Improve our educational content and platform</li>
            </ul>
            <div className="bg-yellow-50 p-4 rounded-lg">
              <p className="text-yellow-800">
                <strong>We do NOT use children&apos;s information for:</strong> Marketing, advertising,
                behavioral tracking, profiling for commercial purposes, or any purpose unrelated to education.
              </p>
            </div>
          </motion.div>

          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8 mb-8">
            <h2 className="text-2xl font-bold text-teal-800 mb-4">5. Information Sharing and Disclosure</h2>

            <h3 className="text-xl font-semibold text-gray-900 mb-3">5.1 We NEVER Share Children&apos;s Data For:</h3>
            <ul className="list-disc pl-6 mb-6 text-gray-700">
              <li>Advertising or marketing purposes</li>
              <li>Commercial sale or rental</li>
              <li>Behavioral targeting</li>
              <li>Social media integration</li>
            </ul>

            <h3 className="text-xl font-semibold text-gray-900 mb-3">5.2 Limited Disclosure Only To:</h3>
            <ul className="list-disc pl-6 mb-6 text-gray-700">
              <li><strong>Parents/Guardians:</strong> Full access to their child&apos;s data via parent dashboard</li>
              <li><strong>Service Providers:</strong> Hosting and infrastructure providers under strict confidentiality agreements (they cannot use data for their own purposes)</li>
              <li><strong>Legal Requirements:</strong> When required by law or to protect safety</li>
            </ul>
          </motion.div>

          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8 mb-8">
            <h2 className="text-2xl font-bold text-teal-800 mb-4">6. Data Security for Children&apos;s Information</h2>
            <p className="text-gray-700 mb-4">
              We implement enhanced security measures for children&apos;s data, including:
            </p>
            <ul className="list-disc pl-6 mb-6 text-gray-700">
              <li>Encryption of all data in transit and at rest</li>
              <li>Strict access controls - limited staff access to children&apos;s data</li>
              <li>Regular security audits and vulnerability assessments</li>
              <li>No public-facing profiles or discoverable user information</li>
              <li>Secure cloud infrastructure with regional data storage (Australia/NZ)</li>
            </ul>
            <p className="text-gray-700 mb-6 bg-green-50 p-4 rounded-lg">
              <strong>COPPA 2025 Compliance:</strong> We maintain a written information security program
              specifically addressing children&apos;s data protection as required by the updated COPPA regulations
              effective June 2025.
            </p>
          </motion.div>

          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8 mb-8">
            <h2 className="text-2xl font-bold text-teal-800 mb-4">7. Parental Rights</h2>
            <p className="text-gray-700 mb-4">As a parent or guardian, you have the right to:</p>

            <div className="space-y-4">
              <div className="border-l-4 border-green-500 pl-4">
                <h4 className="font-bold text-gray-900">Review</h4>
                <p className="text-gray-700">Access all information we have collected about your child through your parent dashboard or by contacting us</p>
              </div>
              <div className="border-l-4 border-blue-500 pl-4">
                <h4 className="font-bold text-gray-900">Correct</h4>
                <p className="text-gray-700">Update or correct any inaccurate information about your child</p>
              </div>
              <div className="border-l-4 border-red-500 pl-4">
                <h4 className="font-bold text-gray-900">Delete</h4>
                <p className="text-gray-700">Request deletion of your child&apos;s profile and all associated data</p>
              </div>
              <div className="border-l-4 border-purple-500 pl-4">
                <h4 className="font-bold text-gray-900">Refuse</h4>
                <p className="text-gray-700">Refuse further collection of your child&apos;s data (which may limit service access)</p>
              </div>
              <div className="border-l-4 border-orange-500 pl-4">
                <h4 className="font-bold text-gray-900">Withdraw Consent</h4>
                <p className="text-gray-700">Withdraw your consent at any time</p>
              </div>
            </div>

            <p className="text-gray-700 mt-6">
              <strong>How to Exercise Your Rights:</strong> Log into your parent account and access the
              &quot;Children&quot; section, or contact our Privacy Team at{' '}
              <a href="mailto:privacy@bhashamitra.co.nz" className="text-primary-600 hover:text-primary-700">
                privacy@bhashamitra.co.nz
              </a>
            </p>
          </motion.div>

          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8 mb-8">
            <h2 className="text-2xl font-bold text-teal-800 mb-4">8. Data Retention</h2>
            <ul className="list-disc pl-6 mb-6 text-gray-700">
              <li><strong>Active Profiles:</strong> Child data is retained while the account is active</li>
              <li><strong>Deleted Profiles:</strong> Upon parent request, child data is deleted within 30 days</li>
              <li><strong>Inactive Accounts:</strong> Accounts inactive for 24 months may be automatically deleted after notice</li>
              <li><strong>Anonymization:</strong> Aggregated, anonymized learning analytics may be retained for educational research</li>
            </ul>
          </motion.div>

          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8 mb-8">
            <h2 className="text-2xl font-bold text-teal-800 mb-4">9. Age-Appropriate Design</h2>
            <p className="text-gray-700 mb-4">
              In anticipation of Australia&apos;s Children&apos;s Online Privacy Code (due December 2026), we implement:
            </p>
            <ul className="list-disc pl-6 mb-6 text-gray-700">
              <li><strong>Default High Privacy:</strong> Most restrictive settings are default for children</li>
              <li><strong>Data Minimization:</strong> Only essential data is collected</li>
              <li><strong>Age-Appropriate Content:</strong> Content is filtered by age range</li>
              <li><strong>No Dark Patterns:</strong> No manipulative design to extract data or engagement</li>
              <li><strong>Transparent Design:</strong> Clear, child-friendly explanations where appropriate</li>
              <li><strong>Parental Controls:</strong> Parents can monitor and control all aspects of their child&apos;s experience</li>
            </ul>
          </motion.div>

          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8 mb-8">
            <h2 className="text-2xl font-bold text-teal-800 mb-4">10. Changes to This Policy</h2>
            <p className="text-gray-700 mb-6">
              If we make material changes to how we collect or use children&apos;s information, we will:
            </p>
            <ul className="list-disc pl-6 mb-6 text-gray-700">
              <li>Update this policy with a new effective date</li>
              <li>Notify parents via email</li>
              <li>Obtain renewed parental consent if required by law</li>
              <li>Provide clear notice of changes before they take effect</li>
            </ul>
          </motion.div>

          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-md p-8">
            <h2 className="text-2xl font-bold text-teal-800 mb-4">11. Contact Us</h2>
            <p className="text-gray-700 mb-4">
              For questions about children&apos;s privacy or to exercise your parental rights:
            </p>
            <div className="bg-gray-50 p-6 rounded-lg mb-6">
              <p className="text-gray-700 mb-2"><strong>PeppiAcademy Privacy Team</strong></p>
              <p className="text-gray-700 mb-2">Email: privacy@bhashamitra.co.nz</p>
              <p className="text-gray-700 mb-2">Subject Line: &quot;Children&apos;s Privacy Inquiry&quot;</p>
              <p className="text-gray-700">Address: Auckland, New Zealand</p>
            </div>

            <div className="grid md:grid-cols-2 gap-4">
              <div className="bg-blue-50 p-4 rounded-lg">
                <h4 className="font-bold text-blue-800 mb-2">New Zealand Privacy Commissioner</h4>
                <p className="text-sm text-blue-700">Website: privacy.org.nz</p>
                <p className="text-sm text-blue-700">For complaints about our privacy practices</p>
              </div>
              <div className="bg-green-50 p-4 rounded-lg">
                <h4 className="font-bold text-green-800 mb-2">Australian Information Commissioner</h4>
                <p className="text-sm text-green-700">Website: oaic.gov.au</p>
                <p className="text-sm text-green-700">For Australian privacy complaints</p>
              </div>
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
