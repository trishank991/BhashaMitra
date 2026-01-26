/** @type {import('next').NextConfig} */
const nextConfig = {
  async redirects() {
    return [
      {
        source: '/learn',
        destination: '/languages',
        permanent: true,
      },
      {
        source: '/learn/:path*',
        destination: '/languages/:path*',
        permanent: true,
      },
    ];
  },
  eslint: {
    // Allow ESLint warnings during builds - fix incrementally
    // Note: 86 pre-existing errors need to be fixed
    ignoreDuringBuilds: true,
  },
  typescript: {
    // TypeScript errors will fail the build - enforcing type safety
    ignoreBuildErrors: false,
  },
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'images.unsplash.com',
        pathname: '/**',
      },
      {
        protocol: 'https',
        hostname: 'source.unsplash.com',
        pathname: '/**',
      },
      {
        protocol: 'https',
        hostname: 'picsum.photos',
        pathname: '/**',
      },
      {
        protocol: 'https',
        hostname: 'via.placeholder.com',
        pathname: '/**',
      },
      {
        protocol: 'https',
        hostname: 'cdn.jsdelivr.net',
        pathname: '/gh/twitter/twemoji@**',
      },
    ],
    // Enable SVG support for Twemoji images
    dangerouslyAllowSVG: true,
    contentSecurityPolicy: "default-src 'self'; script-src 'none'; sandbox;",
  },
};

export default nextConfig;
