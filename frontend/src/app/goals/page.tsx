'use client'

import { useState } from 'react'

const mockGoals = [
  {
    id: 1,
    name: 'SEO Campaign Q1 2026',
    description: 'Rank for 50 target keywords in the AI agent space',
    progress: 78,
    status: 'active',
    tasks: 24,
    completedTasks: 18,
    agents: ['Hermes', 'Claude'],
    deadline: '2026-03-31',
  },
  {
    id: 2,
    name: 'Content Pipeline',
    description: 'Produce 100 high-quality blog posts',
    progress: 92,
    status: 'active',
    tasks: 100,
    completedTasks: 92,
    agents: ['Hermes', 'OpenClaw'],
    deadline: '2026-06-30',
  },
  {
    id: 3,
    name: 'Lead Generation',
    description: 'Generate 1000 qualified leads',
    progress: 45,
    status: 'active',
    tasks: 50,
    completedTasks: 22,
    agents: ['Hermes'],
    deadline: '2026-09-30',
  },
  {
    id: 4,
    name: 'Video Content',
    description: 'Create 50 YouTube videos',
    progress: 30,
    status: 'active',
    tasks: 50,
    completedTasks: 15,
    agents: ['OpenClaw'],
    deadline: '2026-12-31',
  },
]

export default function GoalsPage() {
  const [selectedGoal, setSelectedGoal] = useState<any>(null)

  return (
    <div className="space-y-6 animate-slide-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold gradient-text">Goals</h1>
          <p className="text-sm" style={{ color: 'var(--text-muted)' }}>Track your progress and objectives</p>
        </div>
        <button className="px-4 py-2 rounded-lg text-sm font-medium transition-all hover:opacity-90" style={{ background: 'var(--gradient-purple)' }}>
          + New Goal
        </button>
      </div>

      {/* Goals Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {mockGoals.map((goal) => (
          <div
            key={goal.id}
            className="p-5 rounded-xl border card-hover cursor-pointer"
            style={{ background: 'var(--bg-surface)', borderColor: 'var(--border)' }}
            onClick={() => setSelectedGoal(goal)}
          >
            {/* Header */}
            <div className="flex items-start justify-between mb-4">
              <div>
                <h3 className="font-semibold text-lg">{goal.name}</h3>
                <p className="text-sm mt-1" style={{ color: 'var(--text-muted)' }}>{goal.description}</p>
              </div>
              <span className="text-xs px-2 py-1 rounded-full" style={{ background: 'var(--accent-green)20', color: 'var(--accent-green)' }}>
                {goal.status}
              </span>
            </div>

            {/* Progress */}
            <div className="mb-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm" style={{ color: 'var(--text-secondary)' }}>Progress</span>
                <span className="text-sm font-bold" style={{ color: 'var(--accent-purple)' }}>{goal.progress}%</span>
              </div>
              <div className="h-2 rounded-full overflow-hidden" style={{ background: 'var(--bg-elevated)' }}>
                <div
                  className="h-full rounded-full bg-gradient-to-r from-purple-500 to-pink-500 transition-all duration-500"
                  style={{ width: `${goal.progress}%` }}
                ></div>
              </div>
            </div>

            {/* Stats */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="text-xs" style={{ color: 'var(--text-muted)' }}>Tasks:</span>
                <span className="text-xs font-medium">{goal.completedTasks}/{goal.tasks}</span>
              </div>
              <div className="flex items-center gap-1">
                {goal.agents.map((agent, idx) => (
                  <span
                    key={idx}
                    className="text-xs px-2 py-0.5 rounded-full"
                    style={{ background: 'var(--bg-elevated)', color: 'var(--text-secondary)' }}
                  >
                    {agent}
                  </span>
                ))}
              </div>
            </div>

            {/* Deadline */}
            <div className="mt-4 pt-3 border-t flex items-center justify-between" style={{ borderColor: 'var(--border)' }}>
              <span className="text-xs" style={{ color: 'var(--text-muted)' }}>Deadline</span>
              <span className="text-xs">{goal.deadline}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
