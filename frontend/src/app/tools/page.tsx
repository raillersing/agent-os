'use client'

import { useState } from 'react'

const mockTools = [
  {
    id: 'tool_web_search',
    name: 'Web Search',
    description: 'Search the web for information using Google, Bing, or other search engines',
    category: 'research',
    requiresApproval: false,
    usageCount: 234,
    lastUsed: '5 min ago',
    avgDuration: '2.3s',
    successRate: 99,
    config: {
      searchEngine: 'google',
      maxResults: 10,
      safeSearch: true,
    },
  },
  {
    id: 'tool_code_execute',
    name: 'Execute Code',
    description: 'Execute Python code in a sandboxed environment',
    category: 'development',
    requiresApproval: true,
    usageCount: 89,
    lastUsed: '15 min ago',
    avgDuration: '1.8s',
    successRate: 95,
    config: {
      language: 'python',
      timeout: 30,
      sandbox: true,
    },
  },
  {
    id: 'tool_file_read',
    name: 'Read File',
    description: 'Read contents of files from the filesystem',
    category: 'filesystem',
    requiresApproval: false,
    usageCount: 456,
    lastUsed: '2 min ago',
    avgDuration: '0.1s',
    successRate: 100,
    config: {
      allowedPaths: ['/workspace/*', '/tmp/*'],
      maxFileSize: '10MB',
    },
  },
  {
    id: 'tool_file_write',
    name: 'Write File',
    description: 'Write or modify files on the filesystem',
    category: 'filesystem',
    requiresApproval: true,
    usageCount: 123,
    lastUsed: '30 min ago',
    avgDuration: '0.2s',
    successRate: 100,
    config: {
      allowedPaths: ['/workspace/*'],
      backupEnabled: true,
    },
  },
  {
    id: 'tool_email_send',
    name: 'Send Email',
    description: 'Send emails via SMTP or email API',
    category: 'communication',
    requiresApproval: true,
    usageCount: 45,
    lastUsed: '1 hour ago',
    avgDuration: '2.5s',
    successRate: 98,
    config: {
      provider: 'smtp',
      rateLimit: '10/hour',
      requireRecipientApproval: true,
    },
  },
  {
    id: 'tool_data_analysis',
    name: 'Data Analysis',
    description: 'Analyze data using pandas, numpy, or other data libraries',
    category: 'analytics',
    requiresApproval: false,
    usageCount: 67,
    lastUsed: '45 min ago',
    avgDuration: '3.2s',
    successRate: 97,
    config: {
      libraries: ['pandas', 'numpy', 'matplotlib'],
      maxRows: 1000000,
    },
  },
]

export default function ToolsPage() {
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [selectedTool, setSelectedTool] = useState<any>(null)

  const categories = ['all', 'research', 'development', 'filesystem', 'communication', 'analytics']

  const filteredTools = mockTools.filter(tool => {
    return selectedCategory === 'all' || tool.category === selectedCategory
  })

  return (
    <div className="space-y-6 animate-slide-in">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Tools</h1>
          <p className="text-slate-400">Manage available tools and integrations</p>
        </div>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors">
          + Add Tool
        </button>
      </div>

      {/* Categories */}
      <div className="flex items-center gap-2">
        {categories.map((category) => (
          <button
            key={category}
            onClick={() => setSelectedCategory(category)}
            className={`px-3 py-1 rounded-full text-sm capitalize ${
              selectedCategory === category
                ? 'bg-blue-600 text-white'
                : 'bg-slate-700 hover:bg-slate-600'
            }`}
          >
            {category}
          </button>
        ))}
      </div>

      {/* Stats */}
      <div className="grid grid-cols-4 gap-4">
        <div className="bg-slate-800 rounded-xl border border-slate-700 p-4">
          <p className="text-sm text-slate-400">Total Tools</p>
          <p className="text-2xl font-bold">{mockTools.length}</p>
        </div>
        <div className="bg-slate-800 rounded-xl border border-slate-700 p-4">
          <p className="text-sm text-slate-400">Total Usage</p>
          <p className="text-2xl font-bold">{mockTools.reduce((sum, t) => sum + t.usageCount, 0)}</p>
        </div>
        <div className="bg-slate-800 rounded-xl border border-slate-700 p-4">
          <p className="text-sm text-slate-400">Requires Approval</p>
          <p className="text-2xl font-bold">{mockTools.filter(t => t.requiresApproval).length}</p>
        </div>
        <div className="bg-slate-800 rounded-xl border border-slate-700 p-4">
          <p className="text-sm text-slate-400">Avg Success Rate</p>
          <p className="text-2xl font-bold">
            {(mockTools.reduce((sum, t) => sum + t.successRate, 0) / mockTools.length).toFixed(0)}%
          </p>
        </div>
      </div>

      {/* Tools Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredTools.map((tool) => (
          <ToolCard
            key={tool.id}
            tool={tool}
            onClick={() => setSelectedTool(tool)}
          />
        ))}
      </div>

      {/* Tool Detail Modal */}
      {selectedTool && (
        <ToolDetailModal
          tool={selectedTool}
          onClose={() => setSelectedTool(null)}
        />
      )}
    </div>
  )
}

function ToolCard({ tool, onClick }: { tool: any; onClick: () => void }) {
  const categoryColors: Record<string, string> = {
    research: 'bg-blue-500/10 text-blue-400',
    development: 'bg-green-500/10 text-green-400',
    filesystem: 'bg-yellow-500/10 text-yellow-400',
    communication: 'bg-purple-500/10 text-purple-400',
    analytics: 'bg-pink-500/10 text-pink-400',
  }

  return (
    <div
      onClick={onClick}
      className="bg-slate-800 rounded-xl border border-slate-700 p-4 hover:border-slate-600 transition-all cursor-pointer"
    >
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 bg-slate-700 rounded-xl flex items-center justify-center text-xl">
            🔧
          </div>
          <div>
            <h3 className="font-semibold">{tool.name}</h3>
            <span className={`px-2 py-1 rounded-full text-xs ${categoryColors[tool.category]}`}>
              {tool.category}
            </span>
          </div>
        </div>
        {tool.requiresApproval && (
          <span className="px-2 py-1 bg-yellow-500/10 text-yellow-400 rounded-full text-xs">
            🔒 Approval
          </span>
        )}
      </div>

      <p className="text-sm text-slate-400 mb-4 line-clamp-2">{tool.description}</p>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-2 text-center">
        <div className="bg-slate-700/50 rounded-lg p-2">
          <p className="text-lg font-bold">{tool.usageCount}</p>
          <p className="text-xs text-slate-400">Uses</p>
        </div>
        <div className="bg-slate-700/50 rounded-lg p-2">
          <p className="text-lg font-bold text-green-400">{tool.successRate}%</p>
          <p className="text-xs text-slate-400">Success</p>
        </div>
        <div className="bg-slate-700/50 rounded-lg p-2">
          <p className="text-lg font-bold">{tool.avgDuration}</p>
          <p className="text-xs text-slate-400">Avg Time</p>
        </div>
      </div>

      {/* Footer */}
      <div className="mt-4 pt-3 border-t border-slate-700 flex items-center justify-between text-xs text-slate-400">
        <span>{tool.id}</span>
        <span>Last used: {tool.lastUsed}</span>
      </div>
    </div>
  )
}

function ToolDetailModal({ tool, onClose }: { tool: any; onClose: () => void }) {
  const categoryColors: Record<string, string> = {
    research: 'bg-blue-500/10 text-blue-400',
    development: 'bg-green-500/10 text-green-400',
    filesystem: 'bg-yellow-500/10 text-yellow-400',
    communication: 'bg-purple-500/10 text-purple-400',
    analytics: 'bg-pink-500/10 text-pink-400',
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-slate-800 rounded-2xl border border-slate-700 w-full max-w-2xl max-h-[90vh] overflow-auto">
        {/* Header */}
        <div className="p-6 border-b border-slate-700 flex items-start justify-between">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 bg-slate-700 rounded-2xl flex items-center justify-center text-3xl">
              🔧
            </div>
            <div>
              <h2 className="text-xl font-bold">{tool.name}</h2>
              <div className="flex items-center gap-2 mt-1">
                <span className={`px-2 py-1 rounded-full text-xs ${categoryColors[tool.category]}`}>
                  {tool.category}
                </span>
                {tool.requiresApproval && (
                  <span className="px-2 py-1 bg-yellow-500/10 text-yellow-400 rounded-full text-xs">
                    🔒 Requires Approval
                  </span>
                )}
              </div>
            </div>
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
          {/* Description */}
          <div>
            <h3 className="text-sm font-medium text-slate-400 mb-2">Description</h3>
            <p>{tool.description}</p>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-4 gap-4">
            <div className="bg-slate-700/50 rounded-lg p-3 text-center">
              <p className="text-2xl font-bold">{tool.usageCount}</p>
              <p className="text-xs text-slate-400">Total Uses</p>
            </div>
            <div className="bg-slate-700/50 rounded-lg p-3 text-center">
              <p className="text-2xl font-bold text-green-400">{tool.successRate}%</p>
              <p className="text-xs text-slate-400">Success Rate</p>
            </div>
            <div className="bg-slate-700/50 rounded-lg p-3 text-center">
              <p className="text-2xl font-bold">{tool.avgDuration}</p>
              <p className="text-xs text-slate-400">Avg Duration</p>
            </div>
            <div className="bg-slate-700/50 rounded-lg p-3 text-center">
              <p className="text-2xl font-bold">{tool.lastUsed}</p>
              <p className="text-xs text-slate-400">Last Used</p>
            </div>
          </div>

          {/* Configuration */}
          <div>
            <h3 className="text-sm font-medium text-slate-400 mb-2">Configuration</h3>
            <div className="bg-slate-900 rounded-lg p-4 font-mono text-sm">
              <pre className="text-slate-300">{JSON.stringify(tool.config, null, 2)}</pre>
            </div>
          </div>

          {/* Security */}
          <div>
            <h3 className="text-sm font-medium text-slate-400 mb-2">Security</h3>
            <div className="bg-slate-900 rounded-lg p-4 space-y-2">
              <div className="flex items-center gap-2">
                <span className={tool.requiresApproval ? 'text-yellow-400' : 'text-green-400'}>
                  {tool.requiresApproval ? '⚠️' : '✓'}
                </span>
                <span className="text-sm">
                  {tool.requiresApproval
                    ? 'Requires human approval before execution'
                    : 'Can execute without approval'}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-6 border-t border-slate-700 flex items-center justify-between">
          <button className="px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg text-sm transition-colors">
            📋 View Docs
          </button>
          <div className="flex gap-3">
            <button className="px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg text-sm transition-colors">
              ✏️ Configure
            </button>
            <button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-sm transition-colors">
              ▶️ Test
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
