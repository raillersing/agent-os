'use client'

import { useState } from 'react'

const mockRuns = [
  {
    id: 'run-001',
    agent: 'SEO Analyzer',
    agentModel: 'Claude 3.5',
    status: 'running',
    prompt: 'Analyze competitor keywords for "agent os" and identify opportunities',
    startedAt: '2026-07-20T10:30:00Z',
    progress: 65,
    steps: [
      { name: 'Research competitors', status: 'completed', duration: '45s' },
      { name: 'Extract keywords', status: 'completed', duration: '1m 20s' },
      { name: 'Analyze difficulty', status: 'running', duration: '1m 15s' },
      { name: 'Generate report', status: 'pending', duration: '-' },
    ],
    tokensUsed: 12500,
    cost: 0.125,
  },
  {
    id: 'run-002',
    agent: 'Content Writer',
    agentModel: 'Claude 3.5',
    status: 'completed',
    prompt: 'Write a 2000-word blog post about AI agent orchestration',
    startedAt: '2026-07-20T10:15:00Z',
    completedAt: '2026-07-20T10:20:00Z',
    duration: '5m 0s',
    steps: [
      { name: 'Research topic', status: 'completed', duration: '1m 0s' },
      { name: 'Create outline', status: 'completed', duration: '30s' },
      { name: 'Write content', status: 'completed', duration: '3m 0s' },
      { name: 'SEO optimization', status: 'completed', duration: '30s' },
    ],
    tokensUsed: 45000,
    cost: 0.45,
    result: 'Blog post saved to /content/ai-agent-orchestration.md',
  },
  {
    id: 'run-003',
    agent: 'Keyword Researcher',
    agentModel: 'GPT-4',
    status: 'pending',
    prompt: 'Find long-tail keywords for "agent os" with low competition',
    startedAt: '2026-07-20T10:35:00Z',
    progress: 0,
    steps: [
      { name: 'Search Google', status: 'pending', duration: '-' },
      { name: 'Extract keywords', status: 'pending', duration: '-' },
      { name: 'Filter results', status: 'pending', duration: '-' },
    ],
    tokensUsed: 0,
    cost: 0,
  },
  {
    id: 'run-004',
    agent: 'SEO Analyzer',
    agentModel: 'Claude 3.5',
    status: 'failed',
    prompt: 'Analyze backlinks for competitor domain',
    startedAt: '2026-07-20T09:45:00Z',
    failedAt: '2026-07-20T09:46:00Z',
    error: 'API rate limit exceeded',
    steps: [
      { name: 'Fetch backlinks', status: 'completed', duration: '30s' },
      { name: 'Analyze data', status: 'failed', duration: '30s' },
    ],
    tokensUsed: 8000,
    cost: 0.08,
  },
  {
    id: 'run-005',
    agent: 'Outreach Bot',
    agentModel: 'Claude 3.5',
    status: 'completed',
    prompt: 'Send personalized outreach emails to 10 prospects',
    startedAt: '2026-07-20T09:00:00Z',
    completedAt: '2026-07-20T09:15:00Z',
    duration: '15m 0s',
    steps: [
      { name: 'Load prospects', status: 'completed', duration: '1m 0s' },
      { name: 'Personalize emails', status: 'completed', duration: '5m 0s' },
      { name: 'Send emails', status: 'completed', duration: '8m 0s' },
      { name: 'Log results', status: 'completed', duration: '1m 0s' },
    ],
    tokensUsed: 22000,
    cost: 0.22,
    result: '10 emails sent, 2 opened, 0 replied',
  },
]

export default function RunsPage() {
  const [selectedRun, setSelectedRun] = useState<any>(null)
  const [filter, setFilter] = useState('all')

  const filteredRuns = mockRuns.filter(run => {
    if (filter === 'all') return true
    return run.status === filter
  })

  return (
    <div className="space-y-6 animate-slide-in">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Runs</h1>
          <p className="text-slate-400">Monitor and manage agent execution runs</p>
        </div>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors">
          ▶️ New Run
        </button>
      </div>

      {/* Filters */}
      <div className="flex items-center gap-4">
        <div className="flex gap-2">
          <button
            onClick={() => setFilter('all')}
            className={`px-3 py-1 rounded-full text-sm ${
              filter === 'all' ? 'bg-blue-600 text-white' : 'bg-slate-700 hover:bg-slate-600'
            }`}
          >
            All ({mockRuns.length})
          </button>
          <button
            onClick={() => setFilter('running')}
            className={`px-3 py-1 rounded-full text-sm ${
              filter === 'running' ? 'bg-green-600 text-white' : 'bg-slate-700 hover:bg-slate-600'
            }`}
          >
            Running (1)
          </button>
          <button
            onClick={() => setFilter('completed')}
            className={`px-3 py-1 rounded-full text-sm ${
              filter === 'completed' ? 'bg-blue-600 text-white' : 'bg-slate-700 hover:bg-slate-600'
            }`}
          >
            Completed (2)
          </button>
          <button
            onClick={() => setFilter('pending')}
            className={`px-3 py-1 rounded-full text-sm ${
              filter === 'pending' ? 'bg-yellow-600 text-white' : 'bg-slate-700 hover:bg-slate-600'
            }`}
          >
            Pending (1)
          </button>
          <button
            onClick={() => setFilter('failed')}
            className={`px-3 py-1 rounded-full text-sm ${
              filter === 'failed' ? 'bg-red-600 text-white' : 'bg-slate-700 hover:bg-slate-600'
            }`}
          >
            Failed (1)
          </button>
        </div>
      </div>

      {/* Runs List */}
      <div className="space-y-3">
        {filteredRuns.map((run) => (
          <RunCard
            key={run.id}
            run={run}
            onClick={() => setSelectedRun(run)}
          />
        ))}
      </div>

      {/* Run Detail Modal */}
      {selectedRun && (
        <RunDetailModal
          run={selectedRun}
          onClose={() => setSelectedRun(null)}
        />
      )}
    </div>
  )
}

function RunCard({ run, onClick }: { run: any; onClick: () => void }) {
  const statusConfig: Record<string, { color: string; bg: string; icon: string }> = {
    running: { color: 'text-green-400', bg: 'bg-green-500/10', icon: '▶️' },
    completed: { color: 'text-blue-400', bg: 'bg-blue-500/10', icon: '✅' },
    pending: { color: 'text-yellow-400', bg: 'bg-yellow-500/10', icon: '⏳' },
    failed: { color: 'text-red-400', bg: 'bg-red-500/10', icon: '❌' },
  }

  const status = statusConfig[run.status]

  return (
    <div
      onClick={onClick}
      className="bg-slate-800 rounded-xl border border-slate-700 p-4 hover:border-slate-600 transition-all cursor-pointer"
    >
      <div className="flex items-start justify-between">
        <div className="flex items-start gap-4">
          <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${status.bg}`}>
            {status.icon}
          </div>
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-1">
              <h3 className="font-semibold">{run.agent}</h3>
              <span className="text-xs text-slate-400">•</span>
              <span className="text-xs text-slate-400">{run.agentModel}</span>
            </div>
            <p className="text-sm text-slate-400 line-clamp-1">{run.prompt}</p>
          </div>
        </div>
        <div className="text-right">
          <span className={`text-sm font-medium ${status.color}`}>{run.status}</span>
          {run.duration && (
            <p className="text-xs text-slate-400 mt-1">{run.duration}</p>
          )}
        </div>
      </div>

      {/* Progress bar for running */}
      {run.status === 'running' && (
        <div className="mt-4">
          <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
            <div
              className="h-full bg-green-500 transition-all duration-500"
              style={{ width: `${run.progress}%` }}
            ></div>
          </div>
          <p className="text-xs text-slate-400 mt-1">{run.progress}% complete</p>
        </div>
      )}

      {/* Error message */}
      {run.error && (
        <div className="mt-3 p-2 bg-red-500/10 rounded-lg">
          <p className="text-xs text-red-400">{run.error}</p>
        </div>
      )}

      {/* Footer */}
      <div className="mt-3 pt-3 border-t border-slate-700 flex items-center justify-between text-xs text-slate-400">
        <span>{run.id}</span>
        <div className="flex items-center gap-4">
          <span>{run.tokensUsed.toLocaleString()} tokens</span>
          <span>${run.cost.toFixed(3)}</span>
        </div>
      </div>
    </div>
  )
}

function RunDetailModal({ run, onClose }: { run: any; onClose: () => void }) {
  const statusConfig: Record<string, { color: string; bg: string; icon: string }> = {
    running: { color: 'text-green-400', bg: 'bg-green-500/10', icon: '▶️' },
    completed: { color: 'text-blue-400', bg: 'bg-blue-500/10', icon: '✅' },
    pending: { color: 'text-yellow-400', bg: 'bg-yellow-500/10', icon: '⏳' },
    failed: { color: 'text-red-400', bg: 'bg-red-500/10', icon: '❌' },
  }

  const status = statusConfig[run.status]

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-slate-800 rounded-2xl border border-slate-700 w-full max-w-2xl max-h-[90vh] overflow-auto">
        {/* Header */}
        <div className="p-6 border-b border-slate-700 flex items-start justify-between">
          <div className="flex items-center gap-4">
            <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${status.bg}`}>
              {status.icon}
            </div>
            <div>
              <h2 className="text-xl font-bold">{run.agent}</h2>
              <p className="text-slate-400">{run.id}</p>
              <span className={`text-sm ${status.color}`}>{run.status}</span>
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
          {/* Prompt */}
          <div>
            <h3 className="text-sm font-medium text-slate-400 mb-2">Prompt</h3>
            <div className="bg-slate-900 rounded-lg p-4">
              <p className="text-sm">{run.prompt}</p>
            </div>
          </div>

          {/* Progress */}
          {run.status === 'running' && (
            <div>
              <h3 className="text-sm font-medium text-slate-400 mb-2">Progress</h3>
              <div className="h-3 bg-slate-700 rounded-full overflow-hidden">
                <div
                  className="h-full bg-green-500 transition-all duration-500"
                  style={{ width: `${run.progress}%` }}
                ></div>
              </div>
              <p className="text-sm text-slate-400 mt-2">{run.progress}% complete</p>
            </div>
          )}

          {/* Steps */}
          <div>
            <h3 className="text-sm font-medium text-slate-400 mb-2">Steps</h3>
            <div className="space-y-2">
              {run.steps.map((step: any, index: number) => (
                <div
                  key={index}
                  className="flex items-center gap-3 p-3 bg-slate-900 rounded-lg"
                >
                  <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs ${
                    step.status === 'completed' ? 'bg-green-500' :
                    step.status === 'running' ? 'bg-yellow-500 animate-pulse' :
                    step.status === 'failed' ? 'bg-red-500' :
                    'bg-slate-600'
                  }`}>
                    {step.status === 'completed' ? '✓' :
                     step.status === 'running' ? '⟳' :
                     step.status === 'failed' ? '✕' : (index + 1)}
                  </div>
                  <div className="flex-1">
                    <p className="text-sm">{step.name}</p>
                  </div>
                  <span className="text-xs text-slate-400">{step.duration}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Result */}
          {run.result && (
            <div>
              <h3 className="text-sm font-medium text-slate-400 mb-2">Result</h3>
              <div className="bg-green-500/10 border border-green-500/20 rounded-lg p-4">
                <p className="text-sm text-green-300">{run.result}</p>
              </div>
            </div>
          )}

          {/* Error */}
          {run.error && (
            <div>
              <h3 className="text-sm font-medium text-slate-400 mb-2">Error</h3>
              <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-4">
                <p className="text-sm text-red-300">{run.error}</p>
              </div>
            </div>
          )}

          {/* Stats */}
          <div className="grid grid-cols-3 gap-4">
            <div className="bg-slate-700/50 rounded-lg p-3 text-center">
              <p className="text-lg font-bold">{run.tokensUsed.toLocaleString()}</p>
              <p className="text-xs text-slate-400">Tokens</p>
            </div>
            <div className="bg-slate-700/50 rounded-lg p-3 text-center">
              <p className="text-lg font-bold">${run.cost.toFixed(3)}</p>
              <p className="text-xs text-slate-400">Cost</p>
            </div>
            <div className="bg-slate-700/50 rounded-lg p-3 text-center">
              <p className="text-lg font-bold">{run.duration || '-'}</p>
              <p className="text-xs text-slate-400">Duration</p>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-6 border-t border-slate-700 flex items-center justify-between">
          <button className="px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg text-sm transition-colors">
            📋 Copy ID
          </button>
          <div className="flex gap-3">
            {run.status === 'running' && (
              <button className="px-4 py-2 bg-red-600 hover:bg-red-700 rounded-lg text-sm transition-colors">
                ⏹️ Cancel
              </button>
            )}
            <button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-sm transition-colors">
              ▶️ Rerun
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
