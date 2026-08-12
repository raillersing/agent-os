'use client';

import { KanbanCard } from './KanbanCard';
import type { Task } from '@/lib/mock-data';
import { Plus } from 'lucide-react';

interface KanbanColumnProps {
  title: string;
  status: string;
  tasks: Task[];
  color: string;
  onTaskClick: (task: Task) => void;
  onAddTask: (status: string) => void;
}

export function KanbanColumn({ title, status, tasks, color, onTaskClick, onAddTask }: KanbanColumnProps) {
  return (
    <div className="flex min-w-[260px] flex-1 flex-col rounded-xl border border-border bg-surface">
      <div className="flex items-center justify-between border-b border-border px-3 py-2.5">
        <div className="flex items-center gap-2">
          <div className="h-2.5 w-2.5 rounded-full" style={{ backgroundColor: color }} />
          <span className="text-xs font-semibold text-text-primary">{title}</span>
          <span className="rounded-full bg-surface-elevated px-1.5 py-0.5 text-[10px] text-text-muted">
            {tasks.length}
          </span>
        </div>
        <button
          onClick={() => onAddTask(status)}
          className="rounded p-1 text-text-muted transition-colors hover:bg-surface-hover hover:text-text-primary"
        >
          <Plus size={14} />
        </button>
      </div>
      <div className="flex flex-col gap-2 overflow-auto p-2">
        {tasks.map((task) => (
          <KanbanCard key={task.id} task={task} onClick={() => onTaskClick(task)} />
        ))}
      </div>
    </div>
  );
}
