'use client'

import { useState } from 'react'

const mockMemory = [
  {
    key: 'project-context',
    content: 'Agent OS is a provider-neutral control plane for AI agents. MVP focuses on single-agent workflows with durable state.',
    type: 'knowledge',
    source: 'documentation',
    agentId: null,
    createdAt: '2026-07-20T08:00:00Z',
    accessCount: 45,
    lastAccessed: '2 min ago',
  },
  {
    key: 'seo-keywords',
    content: 'Target keywords: agent os, ai agent orchestration, agent control plane, ai workflow automation',
    type: 'data',
    source: 'keyword-researcher',
    agentId: '3',
    createdAt: '2026-07-20T09:30:00Z',
    accessCount: 12,
    lastAccessed: '15 min ago',
  },
  {
    key: 'competitor-analysis',
    content: 'Top competitors: Julian Goldie SEO Agent OS, LangChain, CrewAI, AutoGPT. Key differentiator: vendor-neutral architecture.',
    type: 'analysis',
    source: 'seo-analyzer',
    agentId: '1',
    createdAt: '2026-07-20T10:15:00Z',
    accessCount: 8,
    lastAccessed: '30 min ago',
  },
  {
    key: 'client-context-acme',
    content: 'Acme Corp: SaaS company, 50 employees, target: AI startups, budget: $5000/mo, goal: increase organic traffic 50% in 6 months.',
    type: 'client',
    source: 'manual',
    agentId: null,
    createdAt: '2026-07-19T14:00:00Z',
    accessCount: 23,
    lastAccessed: '1 hour ago',
  },
  {
    key: 'blog-outline-ai-agents',
    content: '# Blog Post: Understanding AI Agent Orchestration\n\n## Outline\n1. What is Agent Orchestration?\n2. Why Control Planes Matter\n3. Key Components\n4. Implementation Patterns\n5. Best Practices',
    type: 'content',
    source: 'content-writer',
    agentId: '2',
    createdAt: '2026-07-20T10:20:00Z',
    accessCount: 5,
    lastAccessed: '45 min ago',
  },
  {
    key: 'outreach-templates',
    content: 'Template 1: Cold outreach - partnership\nTemplate 2: Follow-up - demo offer\nTemplate 3: Re-engagement - case study share',
    type: 'template',
    source: 'outreach-bot',
    agentId: '4',
    createdAt: '2026-07-18T09:00:00Z',
    accessCount: 34,
    lastAccessed: '2 hours ago',
  },
]

export default function MemoryPage() {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedType, setSelectedType] = useState('all')
  const [selectedMemory, setSelectedMemory] = useState<any>(null)
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid')

  const filteredMemory = mockMemory.filter(item => {
    const matchesSearch = item.key.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         item.content.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesType = selectedType === 'all' || item.type === selectedType
    return matchesSearch && matchesType
  })

  const types = ['all', 'knowledge', 'data', 'analysis', 'client', 'content', 'template']

  return (
    <div className="space-y-6 animate-slide-in">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Memory</h1>
          <p className="text-slate-400">Manage agent memory and knowledge base</p>
        </div>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors">
          + Add Memory
        </button>
      </div>

      {/* Search and Filters */}
      <div className="flex items-center gap-4">
        <div className="flex-1 max-w-md">
          <div className="relative">
            <input
              type="text"
              placeholder="Search memory..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 pl-10 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <svg
              className="absolute left-3 top-2.5 h-4 w-4 text-slate-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </div>

        <div className="flex gap-2">
          {types.map((type) => (
            <button
              key={type}
              onClick={() => setSelectedType(type)}
              className={`px-3 py-1 rounded-full text-sm capitalize ${
                selectedType === type
                  ? 'bg-blue-600 text-white'
                  : 'bg-slate-700 hover:bg-slate-600'
              }`}
            >
              {type}
            </button>
          ))}
        </div>

        <div className="flex bg-slate-700 rounded-lg p-1">
          <button
            onClick={() => setViewMode('grid')}
            className={`px-3 py-1 rounded text-sm ${viewMode === 'grid' ? 'bg-slate-600' : ''}`}
          >
            Grid
          </button>
          <button
            onClick={() => setViewMode('list')}
            className={`px-3 py-1 rounded text-sm ${viewMode === 'list' ? 'bg-slate-600' : ''}`}
          >
            List
          </button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-4 gap-4">
        <div className="bg-slate-800 rounded-xl border border-slate-700 p-4">
          <p className="text-sm text-slate-400">Total Entries</p>
          <p className="text-2xl font-bold">{mockMemory.length}</p>
        </div>
        <div className="bg-slate-800 rounded-xl border border-slate-700 p-4">
          <p className="text-sm text-slate-400">Total Access</p>
          <p className="text-2xl font-bold">{mockMemory.reduce((sum, m) => sum + m.accessCount, 0)}</p>
        </div>
        <div className="bg-slate-800 rounded-xl border border-slate-700 p-4">
          <p className="text-sm text-slate-400">Types</p>
          <p className="text-2xl font-bold">{new Set(mockMemory.map(m => m.type)).size}</p>
        </div>
        <div className="bg-slate-800 rounded-xl border border-slate-700 p-4">
          <p className="text-sm text-slate-400">Agents Contributing</p>
          <p className="text-2xl font-bold">{new Set(mockMemory.filter(m => m.agentId).map(m => m.agentId)).size}</p>
        </div>
      </div>

      {/* Memory Grid/List */}
      {viewMode === 'grid' ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredMemory.map((item) => (
            <MemoryCard
              key={item.key}
              item={item}
              onClick={() => setSelectedMemory(item)}
            />
          ))}
        </div>
      ) : (
        <div className="space-y-2">
          {filteredMemory.map((item) => (
            <MemoryRow
              key={item.key}
              item={item}
              onClick={() => setSelectedMemory(item)}
            />
          ))}
        </div>
      )}

      {/* Memory Detail Modal */}
      {selectedMemory && (
        <MemoryDetailModal
          item={selectedMemory}
          onClose={() => setSelectedMemory(null)}
        />
      )}
    </div>
  )
}

function MemoryCard({ item, onClick }: { item: any; onClick: () => void }) {
  const typeColors: Record<string, string> = {
    knowledge: 'bg-blue-500/10 text-blue-400',
    data: 'bg-green-500/10 text-green-400',
    analysis: 'bg-purple-500/10 text-purple-400',
    client: 'bg-yellow-500/10 text-yellow-400',
    content: 'bg-pink-500/10 text-pink-400',
    template: 'bg-cyan-500/10 text-cyan-400',
  }

  return (
    <div
      onClick={onClick}
      className="bg-slate-800 rounded-xl border border-slate-700 p-4 hover:border-slate-600 transition-all cursor-pointer"
    >
      <div className="flex items-start justify-between mb-3">
        <span className={`px-2 py-1 rounded-full text-xs ${typeColors[item.type]}`}>
          {item.type}
        </span>
        <span className="text-xs text-slate-400">{item.accessCount} views</span>
      </div>
      <h3 className="font-semibold mb-2">{item.key}</h3>
      <p className="text-sm text-slate-400 line-clamp-3">{item.content}</p>
      <div className="mt-4 pt-3 border-t border-slate-700 flex items-center justify-between text-xs text-slate-400">
        <span>{item.source}</span>
        <span>{item.lastAccessed}</span>
      </div>
    </div>
  )
}

function MemoryRow({ item, onClick }: { item: any; onClick: () => void }) {
  const typeColors: Record<string, string> = {
    knowledge: 'bg-blue-500/10 text-blue-400',
    data: 'bg-green-500/10 text-green-400',
    analysis: 'bg-purple-500/10 text-purple-400',
    client: 'bg-yellow-500/10 text-yellow-400',
    content: 'bg-pink-500/10 text-pink-400',
    template: 'bg-cyan-500/10 text-cyan-400',
  }

  return (
    <div
      onClick={onClick}
      className="bg-slate-800 rounded-xl border border-slate-700 p-4 hover:border-slate-600 transition-all cursor-pointer flex items-center gap-4"
    >
      <span className={`px-2 py-1 rounded-full text-xs ${typeColors[item.type]}`}>
        {item.type}
      </span>
      <div className="flex-1 min-w-0">
        <h3 className="font-semibold truncate">{item.key}</h3>
        <p className="text-sm text-slate-400 truncate">{item.content}</p>
      </div>
      <div className="text-right text-xs text-slate-400">
        <p>{item.accessCount} views</p>
        <p>{item.lastAccessed}</p>
      </div>
    </div>
  )
}

function MemoryDetailModal({ item, onClose }: { item: any; onClose: () => void }) {
  const typeColors: Record<string, string> = {
    knowledge: 'bg-blue-500/10 text-blue-400',
    data: 'bg-green-500/10 text-green-400',
    analysis: 'bg-purple-500/10 text-purple-400',
    client: 'bg-yellow-500/10 text-yellow-400',
    content: 'bg-pink-500/10 text-pink-400',
    template: 'bg-cyan-500/10 text-cyan-400',
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-slate-800 rounded-2xl border border-slate-700 w-full max-w-2xl max-h-[90vh] overflow-auto">
        {/* Header */}
        <div className="p-6 border-b border-slate-700 flex items-start justify-between">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <span className={`px-2 py-1 rounded-full text-xs ${typeColors[item.type]}`}>
                {item.type}
              </span>
              <span className="text-xs text-slate-400">{item.source}</span>
            </div>
            <h2 className="text-xl font-bold">{item.key}</h2>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-slate-700 rounded-lg transition-colors"
          >
            ✕
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Content */}
          <div>
            <h3 className="text-sm font-medium text-slate-400 mb-2">Content</h3>
            <div className="bg-slate-900 rounded-lg p-4">
              <pre className="text-sm whitespace-pre-wrap font-mono">{item.content}</pre>
            </div>
          </div>

          {/* Metadata */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <h3 className="text-sm font-medium text-slate-400 mb-2">Metadata</h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-slate-400">Created:</span>
                  <span>{new Date(item.createdAt).toLocaleString()}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Last accessed:</span>
                  <span>{item.lastAccessed}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Access count:</span>
                  <span>{item.accessCount}</span>
                </div>
              </div>
            </div>
            <div>
              <h3 className="text-sm font-medium text-slate-400 mb-2">Source</h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-slate-400">Source:</span>
                  <span>{item.source}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Agent ID:</span>
                  <span>{item.agentId || 'Manual'}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Related Agents */}
          {item.agentId && (
            <div>
              <h3 className="text-sm font-medium text-slate-400 mb-2">Contributing Agent</h3>
              <div className="flex items-center gap-3 p-3 bg-slate-900 rounded-lg">
                <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                  🤖
                </div>
                <div>
                  <p className="font-medium">Agent {item.agentId}</p>
                  <p className="text-sm text-slate-400">Created this memory entry</p>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-6 border-t border-slate-700 flex items-center justify-between">
          <button className="px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg text-sm transition-colors">
            📋 Copy
          </button>
          <div className="flex gap-3">
            <button className="px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg text-sm transition-colors">
              ✏️ Edit
            </button>
            <button className="px-4 py-2 bg-red-600 hover:bg-red-700 rounded-lg text-sm transition-colors">
              🗑️ Delete
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
