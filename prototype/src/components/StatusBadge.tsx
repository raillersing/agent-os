'use client';

import { cn } from '@/lib/utils';

interface StatusBadgeProps {
  status: 'online' | 'ready' | 'offline' | 'running';
  className?: string;
  size?: 'sm' | 'md';
}

export function StatusBadge({ status, className, size = 'md' }: StatusBadgeProps) {
  const config = {
    online: { dot: 'bg-status-online', text: 'Online', textColor: 'text-status-online' },
    ready: { dot: 'bg-status-ready', text: 'Ready', textColor: 'text-status-ready' },
    offline: { dot: 'bg-status-offline', text: 'Offline', textColor: 'text-status-offline' },
    running: { dot: 'bg-status-running', text: 'Running', textColor: 'text-status-running' },
  };

  const c = config[status];

  return (
    <span
      className={cn(
        'inline-flex items-center gap-1.5 rounded-full font-medium',
        size === 'sm' ? 'px-1.5 py-0.5 text-[10px]' : 'px-2 py-0.5 text-xs',
        status === 'running' && 'bg-status-running/10',
        status === 'online' && 'bg-status-online/10',
        status === 'ready' && 'bg-status-ready/10',
        status === 'offline' && 'bg-status-offline/10',
        className
      )}
    >
      <span className={cn('rounded-full', size === 'sm' ? 'h-1 w-1' : 'h-1.5 w-1.5', c.dot, status === 'running' && 'agent-pulse')} />
      <span className={c.textColor}>{c.text}</span>
    </span>
  );
}
