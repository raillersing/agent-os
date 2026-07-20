'use client'

import { useState } from 'react'

const mockMedia = [
  { id: 1, type: 'image', title: 'AI Agent Infographic', agent: 'OpenClaw', date: '2 min ago', thumbnail: '🎨' },
  { id: 2, type: 'video', title: 'Product Demo Video', agent: 'OpenClaw', date: '15 min ago', thumbnail: '🎬' },
  { id: 3, type: 'voice', title: 'Podcast Episode 12', agent: 'Hermes', date: '1 hour ago', thumbnail: '🎙️' },
  { id: 4, type: 'image', title: 'Social Media Banner', agent: 'OpenClaw', date: '2 hours ago', thumbnail: '🖼️' },
  { id: 5, type: 'video', title: 'Tutorial Walkthrough', agent: 'OpenClaw', date: '3 hours ago', thumbnail: '🎥' },
  { id: 6, type: 'voice', title: 'Voice Note - Ideas', agent: 'Hermes', date: '5 hours ago', thumbnail: '🎤' },
]

const categories = [
  { name: 'All', icon: '📁', count: 24 },
  { name: 'Images', icon: '🎨', count: 12 },
  { name: 'Videos', icon: '🎬', count: 8 },
  { name: 'Voice', icon: '🎙️', count: 4 },
]

export default function StudioPage() {
  const [selectedCategory, setSelectedCategory] = useState('All')

  return (
    <div className="space-y-6 animate-slide-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold gradient-text">Studio</h1>
          <p className="text-sm" style={{ color: 'var(--text-muted)' }}>Generate and manage media content</p>
        </div>
        <button className="px-4 py-2 rounded-lg text-sm font-medium transition-all hover:opacity-90" style={{ background: 'var(--gradient-purple)' }}>
          + Generate New
        </button>
      </div>

      {/* Categories */}
      <div className="flex gap-3">
        {categories.map((cat) => (
          <button
            key={cat.name}
            onClick={() => setSelectedCategory(cat.name)}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
              selectedCategory === cat.name
                ? 'text-white'
                : 'hover:bg-white/5'
            }`}
            style={{
              background: selectedCategory === cat.name ? 'var(--gradient-purple)' : 'var(--bg-surface)',
              border: '1px solid var(--border)',
            }}
          >
            <span>{cat.icon}</span>
            <span>{cat.name}</span>
            <span className="text-xs px-1.5 py-0.5 rounded-full" style={{ background: 'var(--bg-elevated)' }}>
              {cat.count}
            </span>
          </button>
        ))}
      </div>

      {/* Media Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {mockMedia.map((item) => (
          <div
            key={item.id}
            className="rounded-xl border card-hover cursor-pointer overflow-hidden"
            style={{ background: 'var(--bg-surface)', borderColor: 'var(--border)' }}
          >
            {/* Thumbnail */}
            <div className="h-40 flex items-center justify-center" style={{ background: 'var(--bg-elevated)' }}>
              <span className="text-6xl opacity-50">{item.thumbnail}</span>
            </div>

            {/* Info */}
            <div className="p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs px-2 py-0.5 rounded-full capitalize" style={{ background: 'var(--bg-elevated)', color: 'var(--text-secondary)' }}>
                  {item.type}
                </span>
                <span className="text-xs" style={{ color: 'var(--text-muted)' }}>{item.date}</span>
              </div>
              <h3 className="font-medium">{item.title}</h3>
              <p className="text-xs mt-1" style={{ color: 'var(--text-muted)' }}>by {item.agent}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
