export default function HomeLoading() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-primary-50 via-white to-secondary-50 p-6">
      {/* Header skeleton */}
      <div className="flex justify-between items-center mb-6">
        <div className="h-8 w-32 bg-gray-200 rounded-lg animate-pulse" />
        <div className="h-10 w-10 bg-gray-200 rounded-full animate-pulse" />
      </div>

      {/* Welcome banner skeleton */}
      <div className="h-32 w-full bg-gray-200 rounded-2xl animate-pulse mb-6" />

      {/* Progress cards skeleton */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="h-24 bg-gray-200 rounded-xl animate-pulse" />
        <div className="h-24 bg-gray-200 rounded-xl animate-pulse" />
      </div>

      {/* Activity cards skeleton */}
      <div className="space-y-4">
        <div className="h-20 bg-gray-200 rounded-xl animate-pulse" />
        <div className="h-20 bg-gray-200 rounded-xl animate-pulse" />
        <div className="h-20 bg-gray-200 rounded-xl animate-pulse" />
      </div>
    </div>
  );
}
