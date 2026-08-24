'use client'

import { usePathname } from 'next/navigation'
import Sidebar from '@/components/Sidebar'
import Header from '@/components/Header'

export default function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()

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
