'use client';

import { Card, CardContent } from '@/components/Card';
import { AgentIcon } from '@/components/AgentIcon';
import { StatusBadge } from '@/components/StatusBadge';
import { agents, tasks } from '@/lib/mock-data';
import { Users, CheckSquare, AlertCircle, DollarSign, Activity, ArrowUpRight, Clock, Layers } from 'lucide-react';

export default function MissionControlPage() {
  const activeAgents = agents.filter((a) => a.status === 'online' || a.status === 'running').length;
  const pendingTasks = tasks.filter((t) => t.status === 'backlog' || t.status === 'ready').length;
  const approvals = 4;
  const dailyCost = 1.23;

  const healthScore = 92;
  const healthColor = healthScore >= 90 ? 'bg-status-online' : healthScore >= 70 ? 'bg-status-ready' : 'bg-status-offline';

  const recentTasks = tasks.slice(0, 5);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-semibold text-text-primary">Mission Control</h1>
          <p className="text-sm text-text-muted mt-0.5">Overview of your AI workforce and active operations</p>
        </div>
        <div className="flex items-center gap-2 text-xs text-text-muted">
          <Clock className="w-3.5 h-3.5" />
          <span>Updated just now</span>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 md:gap-4">
        <Card>
          <CardContent className="py-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs text-text-muted uppercase tracking-wider">Active Agents</p>
                <p className="text-2xl font-bold text-text-primary mt-1">{activeAgents}</p>
              </div>
              <div className="w-9 h-9 rounded-lg bg-status-online/10 flex items-center justify-center">
                <Users className="w-4 h-4 text-status-online" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="py-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs text-text-muted uppercase tracking-wider">Pending Tasks</p>
                <p className="text-2xl font-bold text-text-primary mt-1">{pendingTasks}</p>
              </div>
              <div className="w-9 h-9 rounded-lg bg-status-ready/10 flex items-center justify-center">
                <CheckSquare className="w-4 h-4 text-status-ready" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="py-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs text-text-muted uppercase tracking-wider">Awaiting Approval</p>
                <p className="text-2xl font-bold text-text-primary mt-1">{approvals}</p>
              </div>
              <div className="w-9 h-9 rounded-lg bg-brand-pink/10 flex items-center justify-center">
                <AlertCircle className="w-4 h-4 text-brand-pink" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="py-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs text-text-muted uppercase tracking-wider">Daily Cost</p>
                <p className="text-2xl font-bold text-text-primary mt-1">${dailyCost.toFixed(2)}</p>
              </div>
              <div className="w-9 h-9 rounded-lg bg-brand-purple/10 flex items-center justify-center">
                <DollarSign className="w-4 h-4 text-brand-purple" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Agent Status Grid */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-semibold text-text-primary">Agent Status</h2>
          <button className="text-xs text-brand-purple hover:text-brand-purple/80 flex items-center gap-1 transition-colors">
            View All
            <ArrowUpRight className="w-3 h-3" />
          </button>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          {agents.map((agent) => (
            <Card key={agent.id} hover className="group">
              <CardContent className="py-4">
                <div className="flex items-start gap-3">
                  <AgentIcon
                    name={agent.name}
                    color={agent.color}
                    size="lg"
                    showStatus
                    status={agent.status}
                  />
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <p className="text-sm font-semibold text-text-primary truncate">{agent.name}</p>
                      <StatusBadge status={agent.status} size="sm" />
                    </div>
                    <p className="text-xs text-text-muted mt-0.5">{agent.role}</p>
                    <div className="flex items-center gap-2 mt-2 text-[10px] text-text-muted">
                      <Layers className="w-3 h-3" />
                      <span className="truncate">{agent.model}</span>
                    </div>
                    <p className="text-[10px] text-text-muted mt-1">Last activity: {agent.lastActivity}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Recent Tasks + System Health */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <Card className="lg:col-span-2">
          <div className="px-4 py-3 border-b border-border flex items-center justify-between">
            <h2 className="text-sm font-semibold text-text-primary">Recent Tasks</h2>
            <button className="text-xs text-brand-purple hover:text-brand-purple/80 transition-colors">View All</button>
          </div>
          <div className="divide-y divide-border">
            {recentTasks.map((task) => (
              <div key={task.id} className="px-4 py-3 flex items-center gap-3 hover:bg-surface-hover transition-colors">
                <AgentIcon name={task.agent} color={agents.find((a) => a.id === task.agentId)?.color || '#6B7280'} size="sm" />
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-text-primary truncate">{task.title}</p>
                  <div className="flex items-center gap-2 mt-0.5">
                    <span className="text-[10px] text-text-muted">{task.agent}</span>
                    <span className="text-text-muted">·</span>
                    <span className={
                      task.priority === 'urgent' ? 'text-status-offline text-[10px]' :
                      task.priority === 'high' ? 'text-status-ready text-[10px]' :
                      'text-text-muted text-[10px]'
                    }>
                      {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
                    </span>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-xs text-text-muted">{task.dueDate}</p>
                  <p className={
                    task.status === 'done' ? 'text-[10px] text-status-online' :
                    task.status === 'blocked' ? 'text-[10px] text-status-offline' :
                    task.status === 'in-progress' ? 'text-[10px] text-status-running' :
                    'text-[10px] text-text-muted'
                  }>
                    {task.status.replace('-', ' ')}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </Card>

        <Card>
          <div className="px-4 py-3 border-b border-border">
            <div className="flex items-center gap-2">
              <Activity className="w-4 h-4 text-status-online" />
              <h2 className="text-sm font-semibold text-text-primary">System Health</h2>
            </div>
          </div>
          <div className="px-4 py-4 space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-text-secondary">Overall Score</span>
              <span className="text-lg font-bold text-status-online">{healthScore}%</span>
            </div>
            <div className="w-full h-2 rounded-full bg-surface-elevated overflow-hidden">
              <div className={`h-full rounded-full transition-all duration-500 ${healthColor}`} style={{ width: `${healthScore}%` }} />
            </div>
            <div className="space-y-2 pt-2">
              {[
                { label: 'API Latency', value: '42ms', status: 'good' as const },
                { label: 'Memory Usage', value: '68%', status: 'good' as const },
                { label: 'Queue Depth', value: '3', status: 'warning' as const },
                { label: 'Error Rate', value: '0.02%', status: 'good' as const },
              ].map((metric) => (
                <div key={metric.label} className="flex items-center justify-between text-sm">
                  <span className="text-text-secondary">{metric.label}</span>
                  <div className="flex items-center gap-2">
                    <span className="text-text-primary font-mono text-xs">{metric.value}</span>
                    <div className={`w-2 h-2 rounded-full ${
                      metric.status === 'good' ? 'bg-status-online' :
                      metric.status === 'warning' ? 'bg-status-ready' :
                      'bg-status-offline'
                    }`} />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}
