'use client'

import { usePathname } from 'next/navigation'
import { useEffect, useState } from 'react'

const titles: Record<string, string> = {
  '/': 'Home',
  '/missions': 'Mission Control',
  '/workspaces': 'Workspaces',
  '/automations': 'Automations',
  '/agents': 'Agents',
  '/runs': 'Runs',
  '/tools': 'Tools',
  '/memory': 'Memory',
}

export default function Header() {
  const pathname = usePathname()
  const title = titles[pathname] || 'AgentOS'
  const [mode, setMode] = useState<'dark' | 'light' | 'system'>('system')

  useEffect(() => {
    const stored = window.localStorage.getItem('agentos-theme') as 'dark' | 'light' | null
    if (stored === 'light' || stored === 'dark') setMode(stored)
  }, [])

  const changeTheme = () => {
    const next = mode === 'dark' ? 'light' : mode === 'light' ? 'system' : 'dark'
    setMode(next)
    if (next === 'system') {
      document.documentElement.removeAttribute('data-theme')
      window.localStorage.removeItem('agentos-theme')
    } else {
      document.documentElement.dataset.theme = next
      window.localStorage.setItem('agentos-theme', next)
    }
  }

  const themeLabel = mode === 'system' ? 'System theme' : `${mode[0].toUpperCase()}${mode.slice(1)} theme`

  return (
    <header className="topbar">
      <div className="context">
        <span className="context-mark">AC</span><span>Acme Studio</span><b>/</b><strong>{title}</strong>
      </div>
      <div className="topbar-actions">
        <button className="search-button"><span>⌕</span> Search workspace <kbd>⌘ K</kbd></button>
        <button className="theme-toggle" onClick={changeTheme} aria-label={`Change theme, current: ${themeLabel}`} title={themeLabel}><span>{mode === 'light' ? '☼' : mode === 'system' ? '◐' : '☾'}</span><small>{mode}</small></button>
        <button className="icon-button" aria-label="Notifications"><span>◌</span><i></i></button>
        <button className="help-button" aria-label="Help">?</button>
      </div>
    </header>
  )
}
