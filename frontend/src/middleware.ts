import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

/**
 * Protect App Router pages by requiring the httpOnly `access_token` cookie.
 *
 * The cookie value is opaque to browser JavaScript; the middleware only checks
 * its presence. API routes and public pages (/login, /, static assets) are
 * allowed through.
 */
const PUBLIC_PATHS = new Set(['/login', '/'])
const PUBLIC_PREFIXES = ['/api/', '/_next/', '/favicon.ico']

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl

  if (PUBLIC_PATHS.has(pathname) || PUBLIC_PREFIXES.some((prefix) => pathname.startsWith(prefix))) {
    return NextResponse.next()
  }

  const accessToken = request.cookies.get('access_token')?.value
  if (!accessToken) {
    const loginUrl = new URL('/login', request.url)
    loginUrl.searchParams.set('returnTo', pathname)
    return NextResponse.redirect(loginUrl)
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico|sitemap.xml|robots.txt).*)'],
}
