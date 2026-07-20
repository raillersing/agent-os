'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

const navigation = [
  { name: 'Dashboard', href: '/', icon: '📊' },
  { name: 'Agents', href: '/agents', icon: '🤖' },
  { name: 'Runs', href: '/runs', icon: '▶️' },
  { name: 'Memory', href: '/memory', icon: '🧠' },
  { name: 'Tools', href: '/tools', icon: '🔧' },
  { name: 'Workflows', href: '/workflows', icon: '⚡' },
  { name: 'Settings', href: '/settings', icon: '⚙️' },
]

export default function Sidebar() {
  const pathname = usePathname()

  return (
    <aside className="w-64 bg-slate-800 border-r border-slate-700 flex flex-col">
      {/* Logo */}
      <div className="p-4 border-b border-slate-700">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
            <span className="text-xl">🚀</span>
          </div>
          <div>
            <h1 className="font-bold text-lg">Agent OS</h1>
            <p className="text-xs text-slate-400">Mission Control</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-1">
        {navigation.map((item) => {
          const isActive = pathname === item.href
          return (
            <Link
              key={item.name}
              href={item.href}
              className={`flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${
                isActive
                  ? 'bg-blue-600 text-white'
                  : 'text-slate-300 hover:bg-slate-700 hover:text-white'
              }`}
            >
              <span className="text-lg">{item.icon}</span>
              <span className="font-medium">{item.name}</span>
            </Link>
          )
        })}
      </nav>

      {/* Status */}
      <div className="p-4 border-t border-slate-700">
        <div className="bg-slate-700/50 rounded-lg p-3">
          <div className="flex items-center gap-2 mb-2">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-sm font-medium">System Online</span>
          </div>
          <div className="text-xs text-slate-400 space-y-1">
            <div className="flex justify-between">
              <span>API</span>
              <span className="text-green-400">Healthy</span>
            </div>
            <div className="flex justify-between">
              <span>Database</span>
              <span className="text-green-400">Connected</span>
            </div>
            <div className="flex justify-between">
              <span>Redis</span>
              <span className="text-green-400">Connected</span>
            </div>
          </div>
        </div>
      </div>
    </aside>
  )
}
