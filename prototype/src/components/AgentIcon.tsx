'use client';

import { cn } from '@/lib/utils';

interface AgentIconProps {
  name: string;
  color: string;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  showStatus?: boolean;
  status?: 'online' | 'ready' | 'offline' | 'running';
  showPulse?: boolean;
  className?: string;
}

const sizeClasses = {
  sm: 'w-6 h-6 text-[10px]',
  md: 'w-8 h-8 text-xs',
  lg: 'w-10 h-10 text-sm',
  xl: 'w-14 h-14 text-base',
};

const statusColors = {
  online: 'bg-status-online',
  ready: 'bg-status-ready',
  offline: 'bg-status-offline',
  running: 'bg-status-running',
};

export function AgentIcon({ name, color, size = 'md', showStatus = false, status, showPulse = false, className }: AgentIconProps) {
  const initials = name.slice(0, 2).toUpperCase();

  return (
    <div className={cn('relative inline-flex shrink-0', className)}>
      <div
        className={cn(
          'rounded-full flex items-center justify-center font-mono font-bold shrink-0',
          sizeClasses[size],
          showPulse && 'animate-pulse'
        )}
        style={{ backgroundColor: color }}
      >
        <span className="text-white">{initials}</span>
      </div>
      {(showStatus && status) || showPulse ? (
        <span
          className={cn(
            'absolute -bottom-0.5 -right-0.5 block rounded-full border-2 border-surface',
            status === 'running' || showPulse ? 'w-3 h-3' : 'w-2.5 h-2.5',
            status ? statusColors[status] : 'bg-status-running',
            (status === 'running' || showPulse) && 'agent-pulse'
          )}
        />
      ) : null}
    </div>
  );
}

export default AgentIcon;
