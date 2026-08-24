'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useState } from 'react'
import api from '@/lib/api'

const navigation = [
  { name: 'Home', href: '/', icon: 'home' },
  { name: 'Mission Control', href: '/missions', icon: 'mission' },
  { name: 'Workspaces', href: '/workspaces', icon: 'workspace' },
  { name: 'Automations', href: '/automations', icon: 'automation' },
  { name: 'Agents', href: '/agents', icon: 'agents' },
  { name: 'Goals', href: '/goals', icon: 'goal' },
  { name: 'Studio', href: '/studio', icon: 'studio' },
]

const systemNavigation = [
  { name: 'Runs', href: '/runs', icon: 'runs' },
  { name: 'Tools', href: '/tools', icon: 'tools' },
  { name: 'Memory', href: '/memory', icon: 'memory' },
  { name: 'Settings', href: '/settings', icon: 'settings' },
]

function NavIcon({ name }: { name: string }) {
  const paths: Record<string, React.ReactNode> = {
    home: <><path d="m3 11 9-8 9 8" /><path d="M5 10v10h14V10" /><path d="M9 20v-6h6v6" /></>,
    mission: <><circle cx="12" cy="12" r="8" /><circle cx="12" cy="12" r="3" /><path d="M12 2V0M12 24v-2M2 12H0M24 12h-2" /></>,
    workspace: <><path d="M3 6h7l2 2h9v11H3z" /><path d="M3 6V4h7l2 2" /></>,
    automation: <><path d="M7 7h10v10H7z" /><path d="M12 2v5M12 17v5M2 12h5M17 12h5" /></>,
    agents: <><circle cx="9" cy="8" r="3" /><circle cx="17" cy="10" r="2" /><path d="M3 20c0-4 2-6 6-6s6 2 6 6M15 15c4 0 6 2 6 5" /></>,
    goal: <><path d="M12 3v18M3 12h18" /><circle cx="12" cy="12" r="8" /></>,
    studio: <><path d="m12 3 1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z" /><path d="m19 16 .8 2.2L22 19l-2.2.8L19 22l-.8-2.2L16 19l2.2-.8z" /></>,
    runs: <><path d="M5 5h14v14H5z" /><path d="m9 12 2 2 4-4" /></>,
    tools: <><path d="m14.7 6.3 3-3 3 3-3 3" /><path d="m17.7 9.3-8.4 8.4a2.1 2.1 0 0 1-3-3l8.4-8.4" /><path d="m5 5 4 4" /></>,
    memory: <><path d="M5 5.5A2.5 2.5 0 0 1 7.5 3H20v15H7.5A2.5 2.5 0 0 0 5 20.5z" /><path d="M5 5.5v15M9 7h7M9 10h7" /></>,
    settings: <><circle cx="12" cy="12" r="3" /><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.9l.1.1-1.8 1.8-.1-.1a1.7 1.7 0 0 0-1.9-.3 1.7 1.7 0 0 0-1 1.5v.2h-2.5v-.2a1.7 1.7 0 0 0-1-1.5 1.7 1.7 0 0 0-1.9.3l-.1.1-1.8-1.8.1-.1A1.7 1.7 0 0 0 8 15a1.7 1.7 0 0 0-1.5-1H6v-2.5h.2a1.7 1.7 0 0 0 1.5-1 1.7 1.7 0 0 0-.3-1.9l-.1-.1 1.8-1.8.1.1a1.7 1.7 0 0 0 1.9.3 1.7 1.7 0 0 0 1-1.5v-.2h2.5v.2a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.9-.3l.1-.1 1.8 1.8-.1.1a1.7 1.7 0 0 0-.3 1.9 1.7 1.7 0 0 0 1.5 1h.2V14h-.2a1.7 1.7 0 0 0-1.5 1z" /></>,
  }
  return <svg className="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7">{paths[name]}</svg>
}

export default function Sidebar() {
  const pathname = usePathname()
  const [isLoggingOut, setIsLoggingOut] = useState(false)

  async function handleLogout() {
    setIsLoggingOut(true)
    try {
      await api.logout()
    } finally {
      window.location.href = '/login'
    }
  }

  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-mark"><span>✦</span><i></i></div>
        <div><strong>AgentOS</strong><small>Mission control</small></div>
        <span className="brand-pulse" aria-label="System online"></span>
      </div>

      <button className="workspace-switcher" aria-label="Current workspace"><span className="workspace-avatar">AC</span><span><small>Workspace</small><strong>Acme Studio</strong></span><b>⌄</b></button>

      <nav className="primary-nav" aria-label="Primary navigation">
        <p className="nav-label">Workspace</p>
        {navigation.map((item) => {
          const active = pathname === item.href || (item.href !== '/' && pathname.startsWith(item.href))
          return (
            <Link key={item.name} href={item.href} className={`nav-item ${active ? 'active' : ''}`}>
              <span className="nav-icon-wrap"><NavIcon name={item.icon} /></span>
              <span>{item.name}</span>
              {item.name === 'Mission Control' && <em><i></i>2</em>}
              {active && <b className="nav-active-mark"></b>}
            </Link>
          )
        })}

        <p className="nav-label nav-label-system">Infrastructure</p>
        {systemNavigation.map((item) => (
          <Link key={item.name} href={item.href} className={`nav-item secondary ${pathname.startsWith(item.href) ? 'active' : ''}`}>
            <span className="nav-icon-wrap"><NavIcon name={item.icon} /></span><span>{item.name}</span>
          </Link>
        ))}
      </nav>

      <div className="sidebar-footer">
        <div className="system-health">
          <div className="health-row"><span className="live-dot"></span><strong>System operational</strong><span className="health-code">SYS/01</span></div>
          <p><span>3 agents connected</span><span>1 approval waiting</span></p>
        </div>
        <button className="user-menu" aria-label="Sign out" disabled={isLoggingOut} onClick={handleLogout}>
          <span className="avatar">ER</span>
          <span><strong>Eric</strong><small>Owner</small></span>
          <span className="chevron">{isLoggingOut ? '…' : '⌄'}</span>
        </button>
      </div>
    </aside>
  )
}
