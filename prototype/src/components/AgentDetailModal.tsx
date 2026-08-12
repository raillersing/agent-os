'use client';

import { Modal } from './Modal';
import { AgentIcon } from './AgentIcon';
import { StatusBadge } from './StatusBadge';
import { Button } from './Button';
import type { Agent } from '@/lib/mock-data';
import { MessageSquare, Zap, Clock, CheckCircle } from 'lucide-react';

interface AgentDetailModalProps {
  agent: Agent | null;
  isOpen: boolean;
  onClose: () => void;
}

export function AgentDetailModal({ agent, isOpen, onClose }: AgentDetailModalProps) {
  if (!agent) return null;

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={agent.name}>
      <div className="space-y-5">
        <div className="flex items-start gap-4">
          <AgentIcon name={agent.name} color={agent.color} size="lg" showStatus status={agent.status} />
          <div>
            <div className="text-lg font-semibold text-text-primary">{agent.name}</div>
            <div className="text-sm text-text-muted">{agent.role}</div>
            <div className="mt-1">
              <StatusBadge status={agent.status} />
            </div>
          </div>
        </div>

        <p className="text-sm leading-relaxed text-text-secondary">{agent.description}</p>

        <div className="grid grid-cols-3 gap-3">
          <div className="rounded-lg bg-surface p-3 text-center">
            <Zap size={16} className="mx-auto mb-1 text-brand-purple" />
            <div className="text-sm font-semibold text-text-primary">{agent.model}</div>
            <div className="text-[10px] text-text-muted">Model</div>
          </div>
          <div className="rounded-lg bg-surface p-3 text-center">
            <CheckCircle size={16} className="mx-auto mb-1 text-gemini" />
            <div className="text-sm font-semibold text-text-primary">{agent.tasksCompleted}</div>
            <div className="text-[10px] text-text-muted">Tasks Done</div>
          </div>
          <div className="rounded-lg bg-surface p-3 text-center">
            <Clock size={16} className="mx-auto mb-1 text-kimi" />
            <div className="text-sm font-semibold text-text-primary">{agent.uptime}</div>
            <div className="text-[10px] text-text-muted">Uptime</div>
          </div>
        </div>

        <div>
          <div className="mb-2 text-xs font-semibold uppercase tracking-wider text-text-muted">Skills</div>
          <div className="flex flex-wrap gap-1.5">
            {agent.skills.map((skill) => (
              <span key={skill} className="rounded-full border border-border bg-surface-hover px-2.5 py-1 text-xs text-text-secondary">
                {skill}
              </span>
            ))}
          </div>
        </div>

        <div className="flex gap-2 pt-1">
          <Button variant="primary" className="flex-1">
            <MessageSquare size={14} className="mr-1" />
            Start Chat
          </Button>
          <Button variant="secondary" className="flex-1">
            Assign Task
          </Button>
        </div>
      </div>
    </Modal>
  );
}
