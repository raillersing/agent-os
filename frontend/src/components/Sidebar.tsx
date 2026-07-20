'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

const navigation = [
  { name: 'Mission Control', href: '/', icon: '🏠', color: 'from-purple-500 to-pink-500' },
  { name: 'Goals', href: '/goals', icon: '🎯', color: 'from-blue-500 to-cyan-500' },
  { name: 'Workspace', href: '/workspace', icon: '📁', color: 'from-green-500 to-emerald-500' },
  { name: 'Studio', href: '/studio', icon: '🎨', color: 'from-pink-500 to-rose-500' },
  { name: 'Kanban', href: '/kanban', icon: '📋', color: 'from-yellow-500 to-orange-500' },
  { name: 'Memory', href: '/memory', icon: '🧠', color: 'from-indigo-500 to-violet-500' },
  { name: 'Notebook', href: '/notebook', icon: '📝', color: 'from-teal-500 to-cyan-500' },
]

const agents = [
  { name: 'Hermes', status: 'active', color: '#8b5cf6' },
  { name: 'Claude', status: 'active', color: '#3b82f6' },
  { name: 'OpenClaw', status: 'active', color: '#22c55e' },
  { name: 'Gemini', status: 'inactive', color: '#eab308' },
]

export default function Sidebar() {
  const pathname = usePathname()

  return (
    <aside className="w-64 h-screen flex flex-col" style={{ background: 'var(--bg-secondary)' }}>
      {/* Logo */}
      <div className="p-4 border-b" style={{ borderColor: 'var(--border)' }}>
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl flex items-center justify-center" style={{ background: 'var(--gradient-purple)' }}>
            <span className="text-xl">🚀</span>
          </div>
          <div>
            <h1 className="font-bold text-lg gradient-text">Agent OS</h1>
            <p className="text-xs" style={{ color: 'var(--text-muted)' }}>Mission Control</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-3 space-y-1 overflow-auto">
        {navigation.map((item) => {
          const isActive = pathname === item.href
          return (
            <Link
              key={item.name}
              href={item.href}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all ${
                isActive
                  ? 'bg-white/10 text-white'
                  : 'text-gray-400 hover:bg-white/5 hover:text-white'
              }`}
            >
              <span className="text-lg">{item.icon}</span>
              <span className="text-sm font-medium">{item.name}</span>
            </Link>
          )
        })}
      </nav>

      {/* Agents Section */}
      <div className="p-3 border-t" style={{ borderColor: 'var(--border)' }}>
        <div className="flex items-center justify-between mb-3">
          <span className="text-xs font-semibold uppercase tracking-wider" style={{ color: 'var(--text-muted)' }}>
            Agents
          </span>
          <button className="text-xs px-2 py-1 rounded" style={{ background: 'var(--bg-elevated)', color: 'var(--text-secondary)' }}>
            + Add
          </button>
        </div>
        <div className="space-y-2">
          {agents.map((agent) => (
            <div
              key={agent.name}
              className="flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer transition-all hover:bg-white/5"
            >
              <div
                className="w-2 h-2 rounded-full status-pulse"
                style={{ backgroundColor: agent.color }}
              ></div>
              <span className="text-sm" style={{ color: 'var(--text-secondary)' }}>{agent.name}</span>
            </div>
          ))}
        </div>
      </div>

      {/* System Status */}
      <div className="p-3 border-t" style={{ borderColor: 'var(--border)' }}>
        <div className="p-3 rounded-lg" style={{ background: 'var(--bg-elevated)' }}>
          <div className="flex items-center gap-2 mb-2">
            <div className="w-2 h-2 rounded-full bg-green-500 status-pulse"></div>
            <span className="text-xs font-medium">System Online</span>
          </div>
          <div className="text-xs space-y-1" style={{ color: 'var(--text-muted)' }}>
            <div className="flex justify-between">
              <span>Uptime</span>
              <span style={{ color: 'var(--accent-green)' }}>99.9%</span>
            </div>
            <div className="flex justify-between">
              <span>Agents</span>
              <span>3/4 active</span>
            </div>
          </div>
        </div>
      </div>
    </aside>
  )
}
