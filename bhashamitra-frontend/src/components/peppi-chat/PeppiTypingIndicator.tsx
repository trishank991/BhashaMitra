'use client';

export function PeppiTypingIndicator() {
  return (
    <div className="flex justify-start mb-3">
      <div className="bg-white border border-orange-100 rounded-2xl rounded-bl-md px-4 py-3 shadow-sm">
        <div className="flex items-center gap-2 mb-2">
          <div className="w-6 h-6 bg-orange-100 rounded-full flex items-center justify-center text-sm animate-bounce">
            🐱
          </div>
          <span className="text-xs font-medium text-orange-600">Peppi</span>
        </div>
        <div className="flex gap-1">
          <span className="w-2 h-2 bg-orange-400 rounded-full animate-bounce [animation-delay:-0.3s]" />
          <span className="w-2 h-2 bg-orange-400 rounded-full animate-bounce [animation-delay:-0.15s]" />
          <span className="w-2 h-2 bg-orange-400 rounded-full animate-bounce" />
        </div>
      </div>
    </div>
  );
}
