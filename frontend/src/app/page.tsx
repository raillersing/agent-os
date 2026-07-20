'use client'

import { useState, useEffect } from 'react'

// Mock data for demonstration
const mockStats = {
  agents: { total: 5, active: 3, error: 1 },
  runs: { total: 142, running: 2, completed: 135, failed: 5 },
  memory: { entries: 1247, size: '2.4 GB' },
  tokens: { used: 1250000, cost: 12.50 },
}

const mockAgents = [
  { id: '1', name: 'SEO Analyzer', model: 'Claude 3.5', status: 'active', runs: 45, lastRun: '2 min ago' },
  { id: '2', name: 'Content Writer', model: 'Claude 3.5', status: 'active', runs: 32, lastRun: '5 min ago' },
  { id: '3', name: 'Keyword Researcher', model: 'GPT-4', status: 'active', runs: 28, lastRun: '12 min ago' },
  { id: '4', name: 'Outreach Bot', model: 'Claude 3.5', status: 'error', runs: 15, lastRun: '1 hour ago' },
  { id: '5', name: 'Report Generator', model: 'GPT-4', status: 'inactive', runs: 22, lastRun: '3 hours ago' },
]

const mockRuns = [
  { id: 'run-001', agent: 'SEO Analyzer', status: 'running', prompt: 'Analyze competitor keywords...', progress: 65 },
  { id: 'run-002', agent: 'Content Writer', status: 'completed', prompt: 'Write blog post about AI agents...', progress: 100 },
  { id: 'run-003', agent: 'Keyword Researcher', status: 'pending', prompt: 'Find keywords for "agent os"...', progress: 0 },
]

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState('overview')

  return (
    <div className="space-y-6 animate-slide-in">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Mission Control</h1>
          <p className="text-slate-400">Overview of your Agent OS system</p>
        </div>
        <div className="flex items-center gap-3">
          <button className="px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg text-sm transition-colors">
            📊 Reports
          </button>
          <button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-sm font-medium transition-colors">
            ▶️ Quick Run
          </button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Active Agents"
          value={mockStats.agents.active}
          total={mockStats.agents.total}
          icon="🤖"
          color="blue"
          trend="+2 this week"
        />
        <StatCard
          title="Running Tasks"
          value={mockStats.runs.running}
          total={mockStats.runs.total}
          icon="▶️"
          color="green"
          trend="135 completed"
        />
        <StatCard
          title="Memory Entries"
          value={mockStats.memory.entries.toLocaleString()}
          icon="🧠"
          color="purple"
          trend={mockStats.memory.size}
        />
        <StatCard
          title="Tokens Used"
          value={(mockStats.tokens.used / 1000000).toFixed(1) + 'M'}
          icon="🪙"
          color="yellow"
          trend={`$${mockStats.tokens.cost.toFixed(2)} cost`}
        />
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Active Agents */}
        <div className="lg:col-span-2 bg-slate-800 rounded-xl border border-slate-700">
          <div className="p-4 border-b border-slate-700 flex items-center justify-between">
            <h2 className="font-semibold">Active Agents</h2>
            <button className="text-sm text-blue-400 hover:text-blue-300">View All →</button>
          </div>
          <div className="divide-y divide-slate-700">
            {mockAgents.map((agent) => (
              <AgentRow key={agent.id} agent={agent} />
            ))}
          </div>
        </div>

        {/* Recent Runs */}
        <div className="bg-slate-800 rounded-xl border border-slate-700">
          <div className="p-4 border-b border-slate-700 flex items-center justify-between">
            <h2 className="font-semibold">Recent Runs</h2>
            <button className="text-sm text-blue-400 hover:text-blue-300">View All →</button>
          </div>
          <div className="divide-y divide-slate-700">
            {mockRuns.map((run) => (
              <RunRow key={run.id} run={run} />
            ))}
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-slate-800 rounded-xl border border-slate-700 p-4">
        <h2 className="font-semibold mb-4">Quick Actions</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <QuickAction icon="🔍" title="Research Keywords" description="Start keyword research" />
          <QuickAction icon="📝" title="Write Content" description="Generate blog post" />
          <QuickAction icon="📧" title="Send Outreach" description="Email campaign" />
          <QuickAction icon="📊" title="Generate Report" description="Create analytics report" />
        </div>
      </div>

      {/* Activity Feed */}
      <div className="bg-slate-800 rounded-xl border border-slate-700">
        <div className="p-4 border-b border-slate-700">
          <h2 className="font-semibold">Activity Feed</h2>
        </div>
        <div className="p-4 space-y-3">
          <ActivityItem
            icon="🤖"
            title="SEO Analyzer completed analysis"
            description="Analyzed 15 competitor pages for 'agent os' keywords"
            time="2 min ago"
          />
          <ActivityItem
            icon="🧠"
            title="Memory updated"
            description="Added new project context: Agent OS v0.1.0"
            time="5 min ago"
          />
          <ActivityItem
            icon="⚠️"
            title="Approval required"
            description="Content Writer wants to write file: blog-post.md"
            time="8 min ago"
          />
          <ActivityItem
            icon="✅"
            title="Run completed"
            description="Keyword Researcher found 45 target keywords"
            time="12 min ago"
          />
        </div>
      </div>
    </div>
  )
}

// Sub-components
function StatCard({ title, value, total, icon, color, trend }: {
  title: string
  value: string | number
  total?: number
  icon: string
  color: string
  trend: string
}) {
  const colorClasses: Record<string, string> = {
    blue: 'bg-blue-500/10 text-blue-400',
    green: 'bg-green-500/10 text-green-400',
    purple: 'bg-purple-500/10 text-purple-400',
    yellow: 'bg-yellow-500/10 text-yellow-400',
  }

  return (
    <div className="bg-slate-800 rounded-xl border border-slate-700 p-4 hover:border-slate-600 transition-colors">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-slate-400">{title}</p>
          <p className="text-2xl font-bold mt-1">
            {value}
            {total && <span className="text-sm text-slate-500 font-normal">/{total}</span>}
          </p>
          <p className="text-xs text-slate-500 mt-1">{trend}</p>
        </div>
        <div className={`w-10 h-10 rounded-lg flex items-center justify-center text-xl ${colorClasses[color]}`}>
          {icon}
        </div>
      </div>
    </div>
  )
}

function AgentRow({ agent }: { agent: any }) {
  const statusColors: Record<string, string> = {
    active: 'bg-green-500',
    error: 'bg-red-500',
    inactive: 'bg-slate-500',
  }

  return (
    <div className="p-4 hover:bg-slate-700/50 transition-colors cursor-pointer">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-slate-700 rounded-lg flex items-center justify-center">
            🤖
          </div>
          <div>
            <p className="font-medium">{agent.name}</p>
            <p className="text-sm text-slate-400">{agent.model}</p>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <div className="text-right">
            <p className="text-sm">{agent.runs} runs</p>
            <p className="text-xs text-slate-400">{agent.lastRun}</p>
          </div>
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${statusColors[agent.status]}`}></div>
            <span className="text-sm capitalize">{agent.status}</span>
          </div>
        </div>
      </div>
    </div>
  )
}

function RunRow({ run }: { run: any }) {
  const statusColors: Record<string, string> = {
    running: 'text-green-400',
    completed: 'text-blue-400',
    pending: 'text-yellow-400',
    failed: 'text-red-400',
  }

  return (
    <div className="p-4 hover:bg-slate-700/50 transition-colors cursor-pointer">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-medium">{run.agent}</span>
        <span className={`text-xs ${statusColors[run.status]}`}>{run.status}</span>
      </div>
      <p className="text-sm text-slate-400 truncate">{run.prompt}</p>
      {run.status === 'running' && (
        <div className="mt-2">
          <div className="h-1 bg-slate-700 rounded-full overflow-hidden">
            <div
              className="h-full bg-green-500 transition-all duration-500"
              style={{ width: `${run.progress}%` }}
            ></div>
          </div>
          <p className="text-xs text-slate-500 mt-1">{run.progress}% complete</p>
        </div>
      )}
    </div>
  )
}

function QuickAction({ icon, title, description }: { icon: string; title: string; description: string }) {
  return (
    <button className="p-4 bg-slate-700/50 hover:bg-slate-700 rounded-lg text-left transition-colors group">
      <div className="text-2xl mb-2 group-hover:scale-110 transition-transform">{icon}</div>
      <p className="font-medium text-sm">{title}</p>
      <p className="text-xs text-slate-400">{description}</p>
    </button>
  )
}

function ActivityItem({ icon, title, description, time }: {
  icon: string
  title: string
  description: string
  time: string
}) {
  return (
    <div className="flex items-start gap-3 p-3 hover:bg-slate-700/50 rounded-lg transition-colors">
      <div className="w-8 h-8 bg-slate-700 rounded-full flex items-center justify-center text-sm flex-shrink-0">
        {icon}
      </div>
      <div className="flex-1 min-w-0">
        <p className="font-medium text-sm">{title}</p>
        <p className="text-sm text-slate-400 truncate">{description}</p>
      </div>
      <span className="text-xs text-slate-500 flex-shrink-0">{time}</span>
    </div>
  )
}
