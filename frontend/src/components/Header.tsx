'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useTheme } from '@/components/ThemeProvider'

const titles: Record<string, string> = {
  '/': 'Home',
  '/missions': 'Mission Control',
  '/workspaces': 'Workspaces',
  '/automations': 'Automations',
  '/agents': 'Agents',
  '/runs': 'Runs',
  '/tools': 'Tools',
  '/memory': 'Memory',
  '/goals': 'Goals',
  '/studio': 'Studio',
  '/settings': 'Settings',
}

export default function Header() {
  const pathname = usePathname()
  const title = titles[pathname] || 'AgentOS'
  const { theme, followSystem, resolvedTheme, setTheme } = useTheme()

  const handleToggle = () => {
    if (followSystem) {
      // If in auto mode, redirect to settings
      window.location.href = '/settings'
      return
    }
    setTheme(theme === 'dark' ? 'light' : 'dark')
  }

  const icon = followSystem ? (resolvedTheme === 'dark' ? '☾' : '☼') : theme === 'dark' ? '☾' : '☼'
  const label = followSystem ? 'Auto' : theme

  return (
    <header className="topbar">
      <div className="context">
        <span className="context-mark">AC</span>
        <span>Acme Studio</span>
        <b>/</b>
        <strong>{title}</strong>
      </div>
      <div className="topbar-actions">
        <button className="search-button">
          <span>⌕</span> Search workspace <kbd>⌘ K</kbd>
        </button>
        <button
          className={`theme-toggle ${followSystem ? 'theme-auto' : ''}`}
          onClick={handleToggle}
          aria-label={followSystem ? 'Theme follows system — click to open settings' : `Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`}
          title={followSystem ? `Auto (${resolvedTheme}) — click to configure` : `${theme} theme — click to switch`}
        >
          <span>{icon}</span>
          <small>{label}</small>
          {followSystem && <span className="auto-badge">SYNC</span>}
        </button>
        <button className="icon-button" aria-label="Notifications">
          <span>◌</span>
          <i></i>
        </button>
        <button className="help-button" aria-label="Help">?</button>
      </div>
    </header>
  )
}
