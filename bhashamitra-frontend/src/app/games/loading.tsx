export default function GamesLoading() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-primary-50 via-white to-secondary-50 p-6">
      {/* Header skeleton */}
      <div className="flex items-center gap-4 mb-6">
        <div className="h-10 w-10 bg-gray-200 rounded-full animate-pulse" />
        <div className="h-8 w-32 bg-gray-200 rounded-lg animate-pulse" />
      </div>

      {/* Featured game skeleton */}
      <div className="h-48 w-full bg-gray-200 rounded-2xl animate-pulse mb-6" />

      {/* Game grid skeleton */}
      <div className="grid grid-cols-2 gap-4">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="h-36 bg-gray-200 rounded-xl animate-pulse" />
        ))}
      </div>
    </div>
  );
}
