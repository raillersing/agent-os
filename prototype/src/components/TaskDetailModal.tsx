'use client';

import { useState } from 'react';
import { Modal } from './Modal';
import { AgentIcon } from './AgentIcon';
import { Button } from './Button';
import { agents } from '@/lib/mock-data';
import type { Task } from '@/lib/mock-data';
import { CheckSquare, Square, MessageSquare, Clock } from 'lucide-react';

interface TaskDetailModalProps {
  task: Task | null;
  isOpen: boolean;
  onClose: () => void;
}

export function TaskDetailModal({ task, isOpen, onClose }: TaskDetailModalProps) {
  const [subtasks, setSubtasks] = useState(task?.subtasks || []);

  if (!task) return null;

  const agent = agents.find((a) => a.id === task.agentId);

  const toggleSubtask = (index: number) => {
    setSubtasks((prev) => prev.map((st, i) => (i === index ? { ...st, done: !st.done } : st)));
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={task.title}>
      <div className="space-y-5">
        <div className="flex flex-wrap items-center gap-3 text-xs text-text-muted">
          {agent && (
            <div className="flex items-center gap-1.5">
              <AgentIcon name={agent.name} color={agent.color} size="sm" />
              <span>{agent.name}</span>
            </div>
          )}
          <div className="flex items-center gap-1">
            <Clock size={12} />
            {task.dueDate}
          </div>
          <span
            className="rounded-full px-2 py-0.5 text-[10px] font-medium"
            style={{
              backgroundColor:
                task.priority === 'urgent'
                  ? '#EF444420'
                  : task.priority === 'high'
                    ? '#EAB30820'
                    : task.priority === 'medium'
                      ? '#3B82F620'
                      : '#6B728020',
              color:
                task.priority === 'urgent'
                  ? '#EF4444'
                  : task.priority === 'high'
                    ? '#EAB308'
                    : task.priority === 'medium'
                      ? '#3B82F6'
                      : '#6B7280',
            }}
          >
            {task.priority.toUpperCase()}
          </span>
        </div>

        {task.description && (
          <p className="text-sm leading-relaxed text-text-secondary">{task.description}</p>
        )}

        {subtasks.length > 0 && (
          <div>
            <div className="mb-2 text-xs font-semibold uppercase tracking-wider text-text-muted">Subtasks</div>
            <div className="space-y-1.5">
              {subtasks.map((st, i) => (
                <button
                  key={i}
                  onClick={() => toggleSubtask(i)}
                  className="flex w-full items-start gap-2 rounded-lg px-2 py-1.5 text-left transition-colors hover:bg-surface-hover"
                >
                  {st.done ? (
                    <CheckSquare size={16} className="mt-0.5 shrink-0 text-status-online" />
                  ) : (
                    <Square size={16} className="mt-0.5 shrink-0 text-text-muted" />
                  )}
                  <span className={`text-sm ${st.done ? 'text-text-muted line-through' : 'text-text-primary'}`}>
                    {st.text}
                  </span>
                </button>
              ))}
            </div>
          </div>
        )}

        {task.comments && task.comments.length > 0 && (
          <div>
            <div className="mb-2 text-xs font-semibold uppercase tracking-wider text-text-muted">Activity</div>
            <div className="space-y-2">
              {task.comments.map((c, i) => (
                <div key={i} className="rounded-lg border border-border bg-surface px-3 py-2">
                  <div className="flex items-center gap-2 text-[10px] text-text-muted">
                    <span className="font-medium text-text-secondary">{c.author}</span>
                    <span>{c.time}</span>
                  </div>
                  <div className="mt-1 text-xs text-text-primary">{c.text}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="flex justify-end gap-2 pt-1">
          <Button variant="ghost" onClick={onClose}>
            Close
          </Button>
          <Button variant="primary">
            <MessageSquare size={14} className="mr-1" />
            Comment
          </Button>
        </div>
      </div>
    </Modal>
  );
}
