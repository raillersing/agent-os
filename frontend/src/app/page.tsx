'use client'

import { useState } from 'react'

// Mock data
const mockStats = [
  { label: 'Total Runs', value: '1,247', change: '+12%', icon: '▶️', color: 'from-purple-500 to-pink-500' },
  { label: 'Active Agents', value: '4', change: '+1', icon: '🤖', color: 'from-blue-500 to-cyan-500' },
  { label: 'Tokens Used', value: '2.4M', change: '+18%', icon: '🪙', color: 'from-green-500 to-emerald-500' },
  { label: 'Success Rate', value: '98.5%', change: '+0.5%', icon: '✅', color: 'from-yellow-500 to-orange-500' },
]

const mockAgents = [
  { name: 'Hermes', model: 'GPT-4', status: 'active', runs: 456, progress: 78, color: '#8b5cf6' },
  { name: 'Claude', model: 'Claude 3.5', status: 'active', runs: 324, progress: 92, color: '#3b82f6' },
  { name: 'OpenClaw', model: 'Claude 3.5', status: 'active', runs: 287, progress: 65, color: '#22c55e' },
  { name: 'Gemini', model: 'Gemini Pro', status: 'idle', runs: 180, progress: 45, color: '#eab308' },
]

const mockRecentRuns = [
  { agent: 'Hermes', task: 'Generate SEO content', status: 'completed', time: '2m ago' },
  { agent: 'Claude', task: 'Analyze keywords', status: 'running', time: '5m ago' },
  { agent: 'OpenClaw', task: 'Create image', status: 'completed', time: '12m ago' },
  { agent: 'Hermes', task: 'Outreach emails', status: 'pending', time: '15m ago' },
]

const mockGoals = [
  { name: 'SEO Campaign Q1', progress: 78, status: 'active' },
  { name: 'Content Pipeline', progress: 92, status: 'active' },
  { name: 'Lead Generation', progress: 45, status: 'active' },
]

export default function Dashboard() {
  return (
    <div className="space-y-6 animate-slide-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold gradient-text">Mission Control</h1>
          <p className="text-sm" style={{ color: 'var(--text-muted)' }}>Welcome back, Julian</p>
        </div>
        <div className="flex items-center gap-3">
          <button className="px-4 py-2 rounded-lg text-sm font-medium transition-all hover:opacity-90" style={{ background: 'var(--gradient-purple)' }}>
            ▶️ Quick Run
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {mockStats.map((stat, index) => (
          <div
            key={index}
            className="p-4 rounded-xl border card-hover"
            style={{ background: 'var(--bg-surface)', borderColor: 'var(--border)' }}
          >
            <div className="flex items-start justify-between">
              <div>
                <p className="text-xs font-medium" style={{ color: 'var(--text-muted)' }}>{stat.label}</p>
                <p className="text-2xl font-bold mt-1">{stat.value}</p>
                <p className="text-xs mt-1" style={{ color: 'var(--accent-green)' }}>{stat.change}</p>
              </div>
              <div className={`w-10 h-10 rounded-lg flex items-center justify-center bg-gradient-to-br ${stat.color}`}>
                <span className="text-lg">{stat.icon}</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Active Agents */}
        <div className="lg:col-span-2 rounded-xl border" style={{ background: 'var(--bg-surface)', borderColor: 'var(--border)' }}>
          <div className="p-4 border-b flex items-center justify-between" style={{ borderColor: 'var(--border)' }}>
            <h2 className="font-semibold">Active Agents</h2>
            <button className="text-xs" style={{ color: 'var(--accent-purple)' }}>View All →</button>
          </div>
          <div className="p-4 space-y-3">
            {mockAgents.map((agent, index) => (
              <div
                key={index}
                className="flex items-center gap-4 p-3 rounded-lg transition-all hover:bg-white/5"
              >
                <div
                  className="w-10 h-10 rounded-lg flex items-center justify-center"
                  style={{ backgroundColor: `${agent.color}20` }}
                >
                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: agent.color }}></div>
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <span className="font-medium">{agent.name}</span>
                    <span className="text-xs px-2 py-0.5 rounded-full" style={{ background: `${agent.color}20`, color: agent.color }}>
                      {agent.model}
                    </span>
                  </div>
                  <div className="mt-2 h-1.5 rounded-full overflow-hidden" style={{ background: 'var(--bg-elevated)' }}>
                    <div
                      className="h-full rounded-full transition-all duration-500"
                      style={{ width: `${agent.progress}%`, backgroundColor: agent.color }}
                    ></div>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-sm font-medium">{agent.runs}</p>
                  <p className="text-xs" style={{ color: 'var(--text-muted)' }}>runs</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Goals */}
        <div className="rounded-xl border" style={{ background: 'var(--bg-surface)', borderColor: 'var(--border)' }}>
          <div className="p-4 border-b flex items-center justify-between" style={{ borderColor: 'var(--border)' }}>
            <h2 className="font-semibold">Goals</h2>
            <button className="text-xs" style={{ color: 'var(--accent-purple)' }}>View All →</button>
          </div>
          <div className="p-4 space-y-3">
            {mockGoals.map((goal, index) => (
              <div
                key={index}
                className="p-3 rounded-lg transition-all hover:bg-white/5"
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium">{goal.name}</span>
                  <span className="text-xs" style={{ color: 'var(--accent-green)' }}>{goal.progress}%</span>
                </div>
                <div className="h-2 rounded-full overflow-hidden" style={{ background: 'var(--bg-elevated)' }}>
                  <div
                    className="h-full rounded-full bg-gradient-to-r from-purple-500 to-pink-500 transition-all duration-500"
                    style={{ width: `${goal.progress}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Recent Runs & Quick Actions */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Runs */}
        <div className="rounded-xl border" style={{ background: 'var(--bg-surface)', borderColor: 'var(--border)' }}>
          <div className="p-4 border-b flex items-center justify-between" style={{ borderColor: 'var(--border)' }}>
            <h2 className="font-semibold">Recent Runs</h2>
            <button className="text-xs" style={{ color: 'var(--accent-purple)' }}>View All →</button>
          </div>
          <div className="divide-y" style={{ borderColor: 'var(--border)' }}>
            {mockRecentRuns.map((run, index) => (
              <div key={index} className="p-4 flex items-center gap-3 hover:bg-white/5 transition-all">
                <div className={`w-2 h-2 rounded-full ${
                  run.status === 'completed' ? 'bg-green-500' :
                  run.status === 'running' ? 'bg-blue-500 status-pulse' :
                  'bg-yellow-500'
                }`}></div>
                <div className="flex-1">
                  <p className="text-sm font-medium">{run.task}</p>
                  <p className="text-xs" style={{ color: 'var(--text-muted)' }}>{run.agent}</p>
                </div>
                <span className="text-xs" style={{ color: 'var(--text-muted)' }}>{run.time}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="rounded-xl border" style={{ background: 'var(--bg-surface)', borderColor: 'var(--border)' }}>
          <div className="p-4 border-b" style={{ borderColor: 'var(--border)' }}>
            <h2 className="font-semibold">Quick Actions</h2>
          </div>
          <div className="p-4 grid grid-cols-2 gap-3">
            <button className="p-4 rounded-lg text-left transition-all hover:bg-white/5" style={{ background: 'var(--bg-elevated)' }}>
              <span className="text-2xl">🔍</span>
              <p className="text-sm font-medium mt-2">Research</p>
              <p className="text-xs" style={{ color: 'var(--text-muted)' }}>Find keywords</p>
            </button>
            <button className="p-4 rounded-lg text-left transition-all hover:bg-white/5" style={{ background: 'var(--bg-elevated)' }}>
              <span className="text-2xl">📝</span>
              <p className="text-sm font-medium mt-2">Content</p>
              <p className="text-xs" style={{ color: 'var(--text-muted)' }}>Write articles</p>
            </button>
            <button className="p-4 rounded-lg text-left transition-all hover:bg-white/5" style={{ background: 'var(--bg-elevated)' }}>
              <span className="text-2xl">🎨</span>
              <p className="text-sm font-medium mt-2">Studio</p>
              <p className="text-xs" style={{ color: 'var(--text-muted)' }}>Generate media</p>
            </button>
            <button className="p-4 rounded-lg text-left transition-all hover:bg-white/5" style={{ background: 'var(--bg-elevated)' }}>
              <span className="text-2xl">📧</span>
              <p className="text-sm font-medium mt-2">Outreach</p>
              <p className="text-xs" style={{ color: 'var(--text-muted)' }}>Send emails</p>
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
