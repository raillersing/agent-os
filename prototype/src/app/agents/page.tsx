'use client';

import { useState } from 'react';
import { Card, CardContent } from '@/components/Card';
import { Button } from '@/components/Button';
import { AgentIcon } from '@/components/AgentIcon';
import { StatusBadge } from '@/components/StatusBadge';
import { Modal } from '@/components/Modal';
import { agents } from '@/lib/mock-data';
import { MessageSquare, Plus, Search, SlidersHorizontal, X } from 'lucide-react';

export default function AgentsPage() {
  const [selectedAgent, setSelectedAgent] = useState<typeof agents[0] | null>(null);
  const [statusFilter, setStatusFilter] = useState<string | 'all'>('all');
  const [roleFilter, setRoleFilter] = useState<string | 'all'>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [showFilters, setShowFilters] = useState(false);

  const filteredAgents = agents.filter((agent) => {
    const matchesStatus = statusFilter === 'all' || agent.status === statusFilter;
    const matchesRole = roleFilter === 'all' || agent.role.toLowerCase().includes(roleFilter.toLowerCase());
    const matchesSearch = searchQuery === '' ||
      agent.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      agent.role.toLowerCase().includes(searchQuery.toLowerCase()) ||
      agent.model.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesStatus && matchesRole && matchesSearch;
  });

  const uniqueRoles = [...new Set(agents.map((a) => a.role))];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-semibold text-text-primary">Agents Registry</h1>
          <p className="text-sm text-text-muted mt-0.5">Manage and configure your AI agents</p>
        </div>
        <Button variant="primary" size="sm">
          <Plus className="w-3.5 h-3.5 mr-1" />
          Add Agent
        </Button>
      </div>

      {/* Filter Bar */}
      <div className="flex items-center gap-3">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search agents, roles, models..."
            className="w-full pl-9 pr-3 py-2 bg-surface border border-border rounded-lg text-sm text-text-primary placeholder:text-text-muted outline-none focus:border-border-strong transition-colors"
          />
          {searchQuery && (
            <button onClick={() => setSearchQuery('')} className="absolute right-3 top-1/2 -translate-y-1/2 text-text-muted hover:text-text-primary">
              <X className="w-3.5 h-3.5" />
            </button>
          )}
        </div>
        <button
          onClick={() => setShowFilters(!showFilters)}
          className="flex items-center gap-1.5 px-3 py-2 bg-surface border border-border rounded-lg text-sm text-text-secondary hover:text-text-primary hover:border-border-strong transition-colors"
        >
          <SlidersHorizontal className="w-3.5 h-3.5" />
          Filters
        </button>
      </div>

      {showFilters && (
        <div className="flex flex-wrap items-center gap-2 p-3 bg-surface-elevated rounded-lg border border-border">
          <div className="flex items-center gap-1.5">
            <span className="text-xs text-text-muted">Status:</span>
            {(['all', 'online', 'ready', 'offline', 'running'] as const).map((s) => (
              <button
                key={s}
                onClick={() => setStatusFilter(s)}
                className={`px-2.5 py-1 rounded-md text-xs font-medium transition-colors ${
                  statusFilter === s
                    ? 'bg-brand-purple/10 text-brand-purple border border-brand-purple/20'
                    : 'bg-surface text-text-muted border border-border hover:text-text-primary'
                }`}
              >
                {s.charAt(0).toUpperCase() + s.slice(1)}
              </button>
            ))}
          </div>
          <div className="flex items-center gap-1.5">
            <span className="text-xs text-text-muted">Role:</span>
            <button
              onClick={() => setRoleFilter('all')}
              className={`px-2.5 py-1 rounded-md text-xs font-medium transition-colors ${
                roleFilter === 'all'
                  ? 'bg-brand-purple/10 text-brand-purple border border-brand-purple/20'
                  : 'bg-surface text-text-muted border border-border hover:text-text-primary'
              }`}
            >
              All
            </button>
            {uniqueRoles.map((role) => (
              <button
                key={role}
                onClick={() => setRoleFilter(role)}
                className={`px-2.5 py-1 rounded-md text-xs font-medium transition-colors ${
                  roleFilter === role
                    ? 'bg-brand-purple/10 text-brand-purple border border-brand-purple/20'
                    : 'bg-surface text-text-muted border border-border hover:text-text-primary'
                }`}
              >
                {role}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Agent Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
        {filteredAgents.map((agent) => (
          <Card key={agent.id} hover onClick={() => setSelectedAgent(agent)} className="cursor-pointer">
            <CardContent className="py-4">
              <div className="flex items-start gap-3">
                <AgentIcon name={agent.name} color={agent.color} size="lg" showStatus status={agent.status} />
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <h3 className="text-base font-semibold text-text-primary">{agent.name}</h3>
                    <StatusBadge status={agent.status} size="sm" />
                  </div>
                  <p className="text-sm text-text-muted mt-0.5">{agent.role}</p>
                  <p className="text-xs text-text-muted mt-1 font-mono">{agent.model}</p>
                  <div className="flex flex-wrap gap-1.5 mt-3">
                    {agent.skills.slice(0, 3).map((skill) => (
                      <span key={skill} className="px-2 py-0.5 rounded-full bg-surface-elevated border border-border text-[10px] text-text-secondary">
                        {skill}
                      </span>
                    ))}
                    {agent.skills.length > 3 && (
                      <span className="px-2 py-0.5 rounded-full bg-surface-elevated border border-border text-[10px] text-text-muted">
                        +{agent.skills.length - 3}
                      </span>
                    )}
                  </div>
                  <div className="flex items-center gap-2 mt-4 pt-3 border-t border-border">
                    <Button variant="secondary" size="sm" className="flex-1" onClick={(e) => { e.stopPropagation(); }}>
                      <MessageSquare className="w-3 h-3 mr-1" />
                      Chat
                    </Button>
                    <Button variant="primary" size="sm" className="flex-1" onClick={(e) => { e.stopPropagation(); }}>
                      <Plus className="w-3 h-3 mr-1" />
                      Assign Task
                    </Button>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {filteredAgents.length === 0 && (
        <div className="text-center py-12">
          <p className="text-text-muted">No agents match your filters</p>
        </div>
      )}

      <Modal isOpen={!!selectedAgent} onClose={() => setSelectedAgent(null)} title={selectedAgent?.name} size="md">
        {selectedAgent && (
          <div className="space-y-4">
            <div className="flex items-start gap-4">
              <AgentIcon name={selectedAgent.name} color={selectedAgent.color} size="lg" showStatus status={selectedAgent.status} />
              <div>
                <p className="text-sm text-text-secondary">{selectedAgent.role}</p>
                <p className="text-xs text-text-muted font-mono mt-0.5">{selectedAgent.model}</p>
                <div className="mt-2">
                  <StatusBadge status={selectedAgent.status} />
                </div>
              </div>
            </div>
            <p className="text-sm text-text-secondary leading-relaxed">{selectedAgent.description}</p>
            <div className="grid grid-cols-3 gap-3">
              <div className="p-3 rounded-lg bg-surface-elevated border border-border">
                <p className="text-xs text-text-muted">Uptime</p>
                <p className="text-lg font-bold text-text-primary">{selectedAgent.uptime}</p>
              </div>
              <div className="p-3 rounded-lg bg-surface-elevated border border-border">
                <p className="text-xs text-text-muted">Tasks</p>
                <p className="text-lg font-bold text-text-primary">{selectedAgent.tasksCompleted}</p>
              </div>
              <div className="p-3 rounded-lg bg-surface-elevated border border-border">
                <p className="text-xs text-text-muted">Skills</p>
                <p className="text-lg font-bold text-text-primary">{selectedAgent.skills.length}</p>
              </div>
            </div>
            <div>
              <p className="text-xs font-medium text-text-muted uppercase tracking-wider mb-2">Skills</p>
              <div className="flex flex-wrap gap-1.5">
                {selectedAgent.skills.map((skill) => (
                  <span key={skill} className="px-2.5 py-1 rounded-full bg-surface-elevated border border-border text-xs text-text-secondary">{skill}</span>
                ))}
              </div>
            </div>
            <div className="flex items-center gap-2 pt-2">
              <Button variant="primary" className="flex-1">
                <MessageSquare className="w-4 h-4 mr-1.5" />
                Start Chat
              </Button>
              <Button variant="secondary" className="flex-1">
                <Plus className="w-4 h-4 mr-1.5" />
                Assign Task
              </Button>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
}
