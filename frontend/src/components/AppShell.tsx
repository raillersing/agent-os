'use client'

import { usePathname, useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'
import Sidebar from '@/components/Sidebar'
import Header from '@/components/Header'
import api from '@/lib/api'

export default function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()
  const router = useRouter()
  const [ready, setReady] = useState(pathname === '/login')

  useEffect(() => {
    if (pathname === '/login') {
      setReady(true)
      return
    }
    if (!api.hasToken()) {
      router.replace('/login')
      return
    }
    setReady(true)
  }, [pathname, router])

  if (!ready) {
    return <div className="auth-loading" role="status">Opening your control room…</div>
  }

  if (pathname === '/login') return children

  return (
    <div className="app-shell">
      <Sidebar />
      <div className="app-column">
        <Header />
        <main className="app-main">{children}</main>
      </div>
    </div>
  )
}
