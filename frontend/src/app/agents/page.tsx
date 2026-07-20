'use client'

import { useState } from 'react'

const mockAgents = [
  {
    id: '1',
    name: 'SEO Analyzer',
    model: 'Claude 3.5 Sonnet',
    status: 'active',
    description: 'Analyzes competitor pages and identifies SEO opportunities',
    capabilities: ['web-search', 'data-analysis', 'report-generation'],
    runs: 45,
    successRate: 98,
    avgDuration: '2.5 min',
    tokensUsed: 250000,
    cost: 2.50,
    lastRun: '2 min ago',
    config: {
      temperature: 0.7,
      maxTokens: 4096,
      tools: ['web_search', 'data_analysis'],
    },
  },
  {
    id: '2',
    name: 'Content Writer',
    model: 'Claude 3.5 Sonnet',
    status: 'active',
    description: 'Generates high-quality blog posts and articles',
    capabilities: ['text-generation', 'seo-optimization', 'editing'],
    runs: 32,
    successRate: 95,
    avgDuration: '5.0 min',
    tokensUsed: 180000,
    cost: 1.80,
    lastRun: '5 min ago',
    config: {
      temperature: 0.8,
      maxTokens: 8192,
      tools: ['file_write', 'web_search'],
    },
  },
  {
    id: '3',
    name: 'Keyword Researcher',
    model: 'GPT-4',
    status: 'active',
    description: 'Finds profitable keywords and analyzes search intent',
    capabilities: ['web-search', 'data-analysis', 'keyword-research'],
    runs: 28,
    successRate: 100,
    avgDuration: '3.0 min',
    tokensUsed: 120000,
    cost: 1.20,
    lastRun: '12 min ago',
    config: {
      temperature: 0.5,
      maxTokens: 4096,
      tools: ['web_search', 'gsc_api'],
    },
  },
  {
    id: '4',
    name: 'Outreach Bot',
    model: 'Claude 3.5 Sonnet',
    status: 'error',
    description: 'Manages email outreach campaigns',
    capabilities: ['email', 'personalization', 'scheduling'],
    runs: 15,
    successRate: 87,
    avgDuration: '1.5 min',
    tokensUsed: 45000,
    cost: 0.45,
    lastRun: '1 hour ago',
    error: 'Rate limit exceeded for email API',
    config: {
      temperature: 0.6,
      maxTokens: 2048,
      tools: ['email_api', 'crm_api'],
    },
  },
  {
    id: '5',
    name: 'Report Generator',
    model: 'GPT-4',
    status: 'inactive',
    description: 'Creates comprehensive analytics reports',
    capabilities: ['data-analysis', 'visualization', 'reporting'],
    runs: 22,
    successRate: 100,
    avgDuration: '4.0 min',
    tokensUsed: 88000,
    cost: 0.88,
    lastRun: '3 hours ago',
    config: {
      temperature: 0.3,
      maxTokens: 4096,
      tools: ['data_analysis', 'chart_generation'],
    },
  },
]

export default function AgentsPage() {
  const [selectedAgent, setSelectedAgent] = useState<any>(null)
  const [view, setView] = useState<'grid' | 'list'>('grid')

  return (
    <div className="space-y-6 animate-slide-in">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Agents</h1>
          <p className="text-slate-400">Manage your AI agents and their configurations</p>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex bg-slate-700 rounded-lg p-1">
            <button
              onClick={() => setView('grid')}
              className={`px-3 py-1 rounded text-sm ${view === 'grid' ? 'bg-slate-600' : ''}`}
            >
              Grid
            </button>
            <button
              onClick={() => setView('list')}
              className={`px-3 py-1 rounded text-sm ${view === 'list' ? 'bg-slate-600' : ''}`}
            >
              List
            </button>
          </div>
          <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors">
            + Create Agent
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="flex items-center gap-4">
        <div className="flex gap-2">
          <button className="px-3 py-1 bg-blue-600 text-white rounded-full text-sm">All (5)</button>
          <button className="px-3 py-1 bg-slate-700 hover:bg-slate-600 rounded-full text-sm">Active (3)</button>
          <button className="px-3 py-1 bg-slate-700 hover:bg-slate-600 rounded-full text-sm">Error (1)</button>
          <button className="px-3 py-1 bg-slate-700 hover:bg-slate-600 rounded-full text-sm">Inactive (1)</button>
        </div>
      </div>

      {/* Agent Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {mockAgents.map((agent) => (
          <AgentCard
            key={agent.id}
            agent={agent}
            onClick={() => setSelectedAgent(agent)}
          />
        ))}
      </div>

      {/* Agent Detail Modal */}
      {selectedAgent && (
        <AgentDetailModal
          agent={selectedAgent}
          onClose={() => setSelectedAgent(null)}
        />
      )}
    </div>
  )
}

function AgentCard({ agent, onClick }: { agent: any; onClick: () => void }) {
  const statusColors: Record<string, string> = {
    active: 'bg-green-500',
    error: 'bg-red-500',
    inactive: 'bg-slate-500',
  }

  const statusBg: Record<string, string> = {
    active: 'bg-green-500/10 text-green-400',
    error: 'bg-red-500/10 text-red-400',
    inactive: 'bg-slate-500/10 text-slate-400',
  }

  return (
    <div
      onClick={onClick}
      className="bg-slate-800 rounded-xl border border-slate-700 p-4 hover:border-slate-600 transition-all cursor-pointer group"
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center text-xl group-hover:scale-110 transition-transform">
            🤖
          </div>
          <div>
            <h3 className="font-semibold">{agent.name}</h3>
            <p className="text-sm text-slate-400">{agent.model}</p>
          </div>
        </div>
        <span className={`px-2 py-1 rounded-full text-xs ${statusBg[agent.status]}`}>
          {agent.status}
        </span>
      </div>

      {/* Description */}
      <p className="text-sm text-slate-400 mb-4 line-clamp-2">{agent.description}</p>

      {/* Capabilities */}
      <div className="flex flex-wrap gap-1 mb-4">
        {agent.capabilities.slice(0, 3).map((cap: string) => (
          <span key={cap} className="px-2 py-1 bg-slate-700 rounded text-xs text-slate-300">
            {cap}
          </span>
        ))}
        {agent.capabilities.length > 3 && (
          <span className="px-2 py-1 bg-slate-700 rounded text-xs text-slate-400">
            +{agent.capabilities.length - 3}
          </span>
        )}
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-2 text-center">
        <div className="bg-slate-700/50 rounded-lg p-2">
          <p className="text-lg font-bold">{agent.runs}</p>
          <p className="text-xs text-slate-400">Runs</p>
        </div>
        <div className="bg-slate-700/50 rounded-lg p-2">
          <p className="text-lg font-bold text-green-400">{agent.successRate}%</p>
          <p className="text-xs text-slate-400">Success</p>
        </div>
        <div className="bg-slate-700/50 rounded-lg p-2">
          <p className="text-lg font-bold">{agent.avgDuration}</p>
          <p className="text-xs text-slate-400">Avg Time</p>
        </div>
      </div>

      {/* Footer */}
      <div className="mt-4 pt-3 border-t border-slate-700 flex items-center justify-between">
        <span className="text-xs text-slate-400">Last run: {agent.lastRun}</span>
        <span className="text-xs text-slate-400">${agent.cost.toFixed(2)} spent</span>
      </div>
    </div>
  )
}

function AgentDetailModal({ agent, onClose }: { agent: any; onClose: () => void }) {
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-slate-800 rounded-2xl border border-slate-700 w-full max-w-2xl max-h-[90vh] overflow-auto">
        {/* Header */}
        <div className="p-6 border-b border-slate-700 flex items-start justify-between">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center text-3xl">
              🤖
            </div>
            <div>
              <h2 className="text-xl font-bold">{agent.name}</h2>
              <p className="text-slate-400">{agent.model}</p>
              <div className="flex items-center gap-2 mt-1">
                <div className={`w-2 h-2 rounded-full ${
                  agent.status === 'active' ? 'bg-green-500' :
                  agent.status === 'error' ? 'bg-red-500' : 'bg-slate-500'
                }`}></div>
                <span className="text-sm capitalize">{agent.status}</span>
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
            <p>{agent.description}</p>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-4 gap-4">
            <div className="bg-slate-700/50 rounded-lg p-3 text-center">
              <p className="text-2xl font-bold">{agent.runs}</p>
              <p className="text-xs text-slate-400">Total Runs</p>
            </div>
            <div className="bg-slate-700/50 rounded-lg p-3 text-center">
              <p className="text-2xl font-bold text-green-400">{agent.successRate}%</p>
              <p className="text-xs text-slate-400">Success Rate</p>
            </div>
            <div className="bg-slate-700/50 rounded-lg p-3 text-center">
              <p className="text-2xl font-bold">{agent.avgDuration}</p>
              <p className="text-xs text-slate-400">Avg Duration</p>
            </div>
            <div className="bg-slate-700/50 rounded-lg p-3 text-center">
              <p className="text-2xl font-bold">${agent.cost.toFixed(2)}</p>
              <p className="text-xs text-slate-400">Total Cost</p>
            </div>
          </div>

          {/* Capabilities */}
          <div>
            <h3 className="text-sm font-medium text-slate-400 mb-2">Capabilities</h3>
            <div className="flex flex-wrap gap-2">
              {agent.capabilities.map((cap: string) => (
                <span key={cap} className="px-3 py-1 bg-slate-700 rounded-full text-sm">
                  {cap}
                </span>
              ))}
            </div>
          </div>

          {/* Configuration */}
          <div>
            <h3 className="text-sm font-medium text-slate-400 mb-2">Configuration</h3>
            <div className="bg-slate-900 rounded-lg p-4 font-mono text-sm">
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-slate-400">temperature:</span>
                  <span>{agent.config.temperature}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">maxTokens:</span>
                  <span>{agent.config.maxTokens}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">tools:</span>
                  <span>[{agent.config.tools.join(', ')}]</span>
                </div>
              </div>
            </div>
          </div>

          {/* Error (if any) */}
          {agent.error && (
            <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-4">
              <h3 className="text-sm font-medium text-red-400 mb-2">Error</h3>
              <p className="text-sm text-red-300">{agent.error}</p>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-6 border-t border-slate-700 flex items-center justify-between">
          <button className="px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg text-sm transition-colors">
            📝 Edit
          </button>
          <div className="flex gap-3">
            <button className="px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg text-sm transition-colors">
              ▶️ Run
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
