'use client';

import { useState } from 'react';
import { KanbanColumn } from '@/components/KanbanColumn';
import { TaskDetailModal } from '@/components/TaskDetailModal';
import { tasks } from '@/lib/mock-data';
import type { Task } from '@/lib/mock-data';

const columns = [
  { key: 'backlog', label: 'Backlog', color: '#6B7280' },
  { key: 'ready', label: 'Ready', color: '#EAB308' },
  { key: 'in-progress', label: 'In Progress', color: '#3B82F6' },
  { key: 'blocked', label: 'Blocked', color: '#EF4444' },
  { key: 'done', label: 'Done', color: '#22C55E' },
];

export default function BoardPage() {
  const [taskList, setTaskList] = useState<Task[]>(tasks);
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);
  const [filterAgent, setFilterAgent] = useState('all');
  const [filterPriority, setFilterPriority] = useState('all');
  const [addTaskColumn, setAddTaskColumn] = useState<string | null>(null);

  const filtered = taskList.filter((t) => {
    if (filterAgent !== 'all' && t.agentId !== filterAgent) return false;
    if (filterPriority !== 'all' && t.priority !== filterPriority) return false;
    return true;
  });

  const handleAddTask = (status: string) => {
    setAddTaskColumn(status);
  };

  const submitNewTask = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const form = e.currentTarget;
    const title = (form.elements.namedItem('title') as HTMLInputElement).value;
    const agentId = (form.elements.namedItem('agent') as HTMLSelectElement).value;
    const priority = (form.elements.namedItem('priority') as HTMLSelectElement).value;

    if (!title) return;

    const agentNames: Record<string, string> = {
      claude: 'Claude', kimi: 'Kimi', grok: 'Grok', hermes: 'Hermes',
      openclaw: 'OpenClaw', gemini: 'Gemini', antigravity: 'Antigravity', codex: 'Codex'
    };

    const newTask: Task = {
      id: `t-${Date.now()}`,
      title,
      agent: agentNames[agentId] || agentId,
      agentId,
      status: addTaskColumn as Task['status'],
      priority: priority as Task['priority'],
      dueDate: 'Soon',
      tags: [],
    };

    setTaskList([...taskList, newTask]);
    setAddTaskColumn(null);
  };

  return (
    <div className="space-y-4">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-xl font-bold text-text-primary">Mission Board</h1>
          <p className="text-sm text-text-secondary">Kanban view of all tasks and assignments</p>
        </div>
        <div className="flex items-center gap-2">
          <select
            value={filterAgent}
            onChange={(e) => setFilterAgent(e.target.value)}
            className="rounded-lg border border-border bg-surface-elevated px-3 py-1.5 text-xs text-text-primary outline-none"
          >
            <option value="all">All Agents</option>
            <option value="claude">Claude</option>
            <option value="kimi">Kimi</option>
            <option value="grok">Grok</option>
            <option value="hermes">Hermes</option>
            <option value="openclaw">OpenClaw</option>
            <option value="gemini">Gemini</option>
            <option value="antigravity">Antigravity</option>
            <option value="codex">Codex</option>
          </select>
          <select
            value={filterPriority}
            onChange={(e) => setFilterPriority(e.target.value)}
            className="rounded-lg border border-border bg-surface-elevated px-3 py-1.5 text-xs text-text-primary outline-none"
          >
            <option value="all">All Priorities</option>
            <option value="urgent">Urgent</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
          {(filterAgent !== 'all' || filterPriority !== 'all') && (
            <button
              onClick={() => { setFilterAgent('all'); setFilterPriority('all'); }}
              className="text-xs text-text-muted hover:text-text-primary"
            >
              Clear
            </button>
          )}
        </div>
      </div>

      <div className="flex gap-3 overflow-x-auto pb-2">
        {columns.map((col) => (
          <KanbanColumn
            key={col.key}
            title={col.label}
            status={col.key}
            tasks={filtered.filter((t) => t.status === col.key)}
            color={col.color}
            onTaskClick={setSelectedTask}
            onAddTask={handleAddTask}
          />
        ))}
      </div>

      <TaskDetailModal
        task={selectedTask}
        isOpen={!!selectedTask}
        onClose={() => setSelectedTask(null)}
      />

      {/* Add Task Modal */}
      {addTaskColumn && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
          <div className="w-full max-w-md rounded-xl border border-border bg-surface-elevated p-6 shadow-2xl">
            <h2 className="mb-4 text-lg font-semibold text-text-primary">
              Add Task to {columns.find((c) => c.key === addTaskColumn)?.label}
            </h2>
            <form onSubmit={submitNewTask} className="space-y-4">
              <div>
                <label className="mb-1 block text-xs font-medium text-text-secondary">Title</label>
                <input
                  name="title"
                  autoFocus
                  className="w-full rounded-lg border border-border bg-surface px-3 py-2 text-sm text-text-primary outline-none focus:border-brand-purple"
                  placeholder="Task title..."
                />
              </div>
              <div>
                <label className="mb-1 block text-xs font-medium text-text-secondary">Agent</label>
                <select
                  name="agent"
                  className="w-full rounded-lg border border-border bg-surface px-3 py-2 text-sm text-text-primary outline-none"
                >
                  <option value="claude">Claude</option>
                  <option value="kimi">Kimi</option>
                  <option value="grok">Grok</option>
                  <option value="hermes">Hermes</option>
                  <option value="openclaw">OpenClaw</option>
                  <option value="gemini">Gemini</option>
                  <option value="antigravity">Antigravity</option>
                  <option value="codex">Codex</option>
                </select>
              </div>
              <div>
                <label className="mb-1 block text-xs font-medium text-text-secondary">Priority</label>
                <select
                  name="priority"
                  className="w-full rounded-lg border border-border bg-surface px-3 py-2 text-sm text-text-primary outline-none"
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                  <option value="urgent">Urgent</option>
                </select>
              </div>
              <div className="flex justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setAddTaskColumn(null)}
                  className="rounded-lg px-4 py-2 text-sm text-text-secondary hover:bg-surface-hover"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="rounded-lg bg-brand-purple px-4 py-2 text-sm font-medium text-white hover:bg-brand-purple/90"
                >
                  Add Task
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
