export default function Loading() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-primary-50 via-white to-secondary-50 flex flex-col items-center justify-center">
      {/* Animated Logo/Spinner */}
      <div className="relative">
        {/* Outer ring */}
        <div className="w-16 h-16 border-4 border-primary-200 rounded-full animate-pulse" />
        {/* Spinning inner ring */}
        <div className="absolute inset-0 w-16 h-16 border-4 border-transparent border-t-primary-500 rounded-full animate-spin" />
      </div>

      {/* Loading Text */}
      <p className="mt-4 text-gray-600 font-medium animate-pulse">
        Loading...
      </p>
    </div>
  );
}
