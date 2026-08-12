'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import {
  LayoutDashboard,
  Columns3,
  ListChecks,
  Palette,
  Briefcase,
  BookOpen,
  Wrench,
  Bot,
  Brain,
  Activity,
  Settings,
  Zap,
} from 'lucide-react';

const navGroups = [
  {
    label: 'Command',
    items: [
      { label: 'Mission Control', href: '/', icon: LayoutDashboard },
      { label: 'Mission Board', href: '/board', icon: Columns3 },
      { label: 'Tasks', href: '/workspace', icon: ListChecks },
    ],
  },
  {
    label: 'Production',
    items: [
      { label: 'Studio', href: '/studio', icon: Palette },
      { label: 'Workspace', href: '/workspace', icon: Briefcase },
      { label: 'Notebook', href: '/notebook', icon: BookOpen },
      { label: 'Skills', href: '/settings', icon: Wrench },
    ],
  },
  {
    label: 'System',
    items: [
      { label: 'Agents', href: '/agents', icon: Bot },
      { label: 'Memory', href: '/notebook', icon: Brain },
      { label: 'Traces', href: '/chat', icon: Activity },
      { label: 'Settings', href: '/settings', icon: Settings },
    ],
  },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed left-0 top-header bottom-0 w-sidebar bg-surface border-r border-border hidden lg:flex flex-col z-40 overflow-y-auto">
      <div className="flex items-center gap-2 px-4 py-3 border-b border-border">
        <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-brand-purple to-brand-pink flex items-center justify-center">
          <Zap className="w-4 h-4 text-white" />
        </div>
        <span className="text-sm font-semibold text-text-primary">Agent OS</span>
        <span className="text-[10px] font-mono text-text-muted ml-auto px-1.5 py-0.5 rounded bg-surface-elevated border border-border">
          v2.0
        </span>
      </div>

      <div className="flex-1 py-3 px-3 space-y-5">
        {navGroups.map((group) => (
          <div key={group.label}>
            <p className="text-[10px] font-semibold text-text-muted uppercase tracking-wider px-2 mb-1.5">
              {group.label}
            </p>
            <nav className="space-y-0.5">
              {group.items.map((item) => {
                const isActive = pathname === item.href;
                const Icon = item.icon;
                return (
                  <Link
                    key={item.href + item.label}
                    href={item.href}
                    className={cn(
                      'flex items-center gap-2.5 px-2.5 py-1.5 rounded-lg text-sm transition-colors',
                      isActive
                        ? 'bg-brand-purple/10 text-brand-purple font-medium'
                        : 'text-text-secondary hover:text-text-primary hover:bg-surface-hover'
                    )}
                  >
                    <Icon className={cn('w-4 h-4', isActive && 'text-brand-purple')} />
                    {item.label}
                  </Link>
                );
              })}
            </nav>
          </div>
        ))}
      </div>

      <div className="p-3 border-t border-border">
        <div className="flex items-center gap-2.5 px-2.5 py-2 rounded-lg bg-surface-elevated border border-border">
          <div className="w-7 h-7 rounded-full bg-status-online/20 flex items-center justify-center">
            <span className="text-[10px] font-bold text-status-online">3</span>
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-xs font-medium text-text-primary">3 Active Agents</p>
            <p className="text-[10px] text-text-muted">All systems nominal</p>
          </div>
        </div>
      </div>
    </aside>
  );
}
