'use client'

import { useState } from 'react'

export default function Header() {
  return (
    <header className="h-14 border-b flex items-center justify-between px-6" style={{ background: 'var(--bg-secondary)', borderColor: 'var(--border)' }}>
      {/* Search */}
      <div className="flex-1 max-w-md">
        <div className="relative">
          <input
            type="text"
            placeholder="Search anything..."
            className="w-full rounded-lg px-4 py-2 pl-10 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500/50"
            style={{ background: 'var(--bg-elevated)', border: '1px solid var(--border)' }}
          />
          <svg
            className="absolute left-3 top-2.5 h-4 w-4"
            style={{ color: 'var(--text-muted)' }}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
      </div>

      {/* Right side */}
      <div className="flex items-center gap-4">
        {/* Notifications */}
        <button className="relative p-2 rounded-lg transition-all hover:bg-white/5" style={{ color: 'var(--text-secondary)' }}>
          <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
          </svg>
          <span className="absolute -top-1 -right-1 w-4 h-4 rounded-full text-xs flex items-center justify-center" style={{ background: 'var(--accent-red)' }}>
            3
          </span>
        </button>

        {/* User */}
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold" style={{ background: 'var(--gradient-purple)' }}>
            JG
          </div>
        </div>
      </div>
    </header>
  )
}
