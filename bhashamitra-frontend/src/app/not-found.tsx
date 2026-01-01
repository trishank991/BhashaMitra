import Link from 'next/link';

export default function NotFound() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-primary-50 via-white to-secondary-50 flex flex-col items-center justify-center px-6">
      <div className="w-full max-w-md text-center">
        {/* 404 Illustration */}
        <div className="text-8xl font-bold text-primary-200 mb-4">404</div>

        {/* Message */}
        <h1 className="text-2xl font-bold text-gray-900 mb-2">
          Page Not Found
        </h1>
        <p className="text-gray-600 mb-8">
          Looks like this page went on an adventure! Let&apos;s get you back on track.
        </p>

        {/* Action Buttons */}
        <div className="space-y-3">
          <Link
            href="/home"
            className="block w-full px-6 py-3 bg-primary-500 text-white font-semibold rounded-xl hover:bg-primary-600 transition-colors"
          >
            Go to Home
          </Link>
          <Link
            href="/help"
            className="block w-full px-6 py-3 border-2 border-gray-200 text-gray-700 font-semibold rounded-xl hover:bg-gray-50 transition-colors"
          >
            Get Help
          </Link>
        </div>
      </div>
    </div>
  );
}
