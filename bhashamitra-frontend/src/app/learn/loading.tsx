export default function LearnLoading() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-primary-50 via-white to-secondary-50 p-6">
      {/* Header skeleton */}
      <div className="flex items-center gap-4 mb-6">
        <div className="h-10 w-10 bg-gray-200 rounded-full animate-pulse" />
        <div className="h-8 w-48 bg-gray-200 rounded-lg animate-pulse" />
      </div>

      {/* Category tabs skeleton */}
      <div className="flex gap-3 mb-6 overflow-hidden">
        <div className="h-10 w-24 bg-gray-200 rounded-full animate-pulse flex-shrink-0" />
        <div className="h-10 w-28 bg-gray-200 rounded-full animate-pulse flex-shrink-0" />
        <div className="h-10 w-20 bg-gray-200 rounded-full animate-pulse flex-shrink-0" />
      </div>

      {/* Lesson cards skeleton */}
      <div className="space-y-4">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="h-28 bg-gray-200 rounded-2xl animate-pulse" />
        ))}
      </div>
    </div>
  );
}
