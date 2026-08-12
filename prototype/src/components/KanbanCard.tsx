'use client';

import { AgentIcon } from './AgentIcon';
import { agents } from '@/lib/mock-data';
import type { Task } from '@/lib/mock-data';
import { Calendar } from 'lucide-react';

interface KanbanCardProps {
  task: Task;
  onClick?: () => void;
}

export function KanbanCard({ task, onClick }: KanbanCardProps) {
  const agent = agents.find((a) => a.id === task.agentId);

  const priorityConfig = {
    urgent: { border: 'border-l-status-offline', label: 'Urgent' },
    high: { border: 'border-l-status-ready', label: 'High' },
    medium: { border: 'border-l-status-running', label: 'Medium' },
    low: { border: 'border-l-text-muted', label: 'Low' },
  };

  const pc = priorityConfig[task.priority];

  return (
    <div
      onClick={onClick}
      className={`cursor-pointer rounded-lg border border-border ${pc.border} border-l-[3px] bg-surface-elevated p-3 transition-all hover:bg-surface-hover hover:shadow-md`}
    >
      <div className="mb-2 text-xs font-medium text-text-primary">{task.title}</div>

      <div className="mb-2 flex flex-wrap gap-1">
        {task.tags.map((tag) => (
          <span key={tag} className="rounded-full bg-surface px-1.5 py-0.5 text-[9px] text-text-muted">
            {tag}
          </span>
        ))}
      </div>

      <div className="flex items-center justify-between">
        <div className="flex items-center gap-1.5">
          {agent && <AgentIcon name={agent.name} color={agent.color} size="sm" />}
          <span className="text-[10px] text-text-muted">{task.agent}</span>
        </div>
        <div className="flex items-center gap-1 text-[10px] text-text-muted">
          <Calendar size={10} />
          {task.dueDate}
        </div>
      </div>
    </div>
  );
}
