import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

/**
 * Route protection middleware for PeppiAcademy
 *
 * Handles client-side route protection by checking for auth tokens.
 * Note: This is a lightweight check - actual auth validation happens on the backend.
 */

// Public routes that don't require authentication
const PUBLIC_ROUTES = [
  '/',
  '/login',
  '/register',
  '/verify-email',
  '/terms',
  '/privacy',
  '/help',
  '/childrens-privacy',
  '/forgot-password',
  '/reset-password',
  '/pricing',
];

// Public route prefixes (anyone can access)
const PUBLIC_PREFIXES = [
  '/c/',  // Challenge play pages - viral sharing, no auth needed
];

// Protected route prefixes that require authentication
const PROTECTED_PREFIXES = [
  '/home',
  '/dashboard',
  '/languages',
  '/children',
  '/games',
  '/parent',
  '/profile',
  '/practice',
  '/onboarding',
  '/stories',
  '/festivals',
  '/challenges',
  '/progress',
  '/live-classes',
  '/checkout',
  '/join',
];

// Static assets and API routes to skip
const SKIP_PREFIXES = [
  '/_next',
  '/api',
  '/favicon',
  '/images',
  '/audio',
  '/static',
];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Skip static assets and API routes
  if (SKIP_PREFIXES.some(prefix => pathname.startsWith(prefix))) {
    return NextResponse.next();
  }

  // Skip public routes (exact match)
  if (PUBLIC_ROUTES.includes(pathname)) {
    return NextResponse.next();
  }

  // Skip public prefixes (viral challenge routes, etc.)
  if (PUBLIC_PREFIXES.some(prefix => pathname.startsWith(prefix))) {
    return NextResponse.next();
  }

  // Check if route requires protection
  const isProtectedRoute = PROTECTED_PREFIXES.some(prefix =>
    pathname.startsWith(prefix)
  );

  if (isProtectedRoute) {
    // Check for auth token in cookies
    // Zustand persist stores auth in localStorage, but we can check for session cookie
    // Check for new cookie name first, fall back to legacy
    const authCookie = request.cookies.get('peppi-auth') || request.cookies.get('bhashamitra-auth');

    // For client-side state management, we rely on the client to redirect
    // The middleware provides an additional layer of protection
    // If no auth state cookie exists, redirect to login
    if (!authCookie?.value) {
      // Check if there's a localStorage-based auth (via custom header from client)
      // This is a fallback - primary auth check is client-side via Zustand
      const url = request.nextUrl.clone();
      url.pathname = '/login';
      url.searchParams.set('redirect', pathname);

      // For now, allow the request to proceed - the client-side auth guard
      // in each page will handle the actual redirect
      // This prevents issues with hydration and localStorage-based auth
      return NextResponse.next();
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public folder files
     */
    '/((?!_next/static|_next/image|favicon.ico|.*\\..*|api).*)',
  ],
};
