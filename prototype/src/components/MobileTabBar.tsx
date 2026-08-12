'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import {
  LayoutDashboard,
  Columns3,
  MessageSquare,
  Bot,
  Settings,
} from 'lucide-react';

const tabs = [
  { label: 'Home', href: '/', icon: LayoutDashboard },
  { label: 'Board', href: '/board', icon: Columns3 },
  { label: 'Chat', href: '/chat', icon: MessageSquare },
  { label: 'Agents', href: '/agents', icon: Bot },
  { label: 'Settings', href: '/settings', icon: Settings },
];

export function MobileTabBar() {
  const pathname = usePathname();

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-surface border-t border-border z-50 lg:hidden">
      <div className="flex items-center justify-around h-14">
        {tabs.map((tab) => {
          const isActive = pathname === tab.href;
          const Icon = tab.icon;
          return (
            <Link
              key={tab.href}
              href={tab.href}
              className={cn(
                'flex flex-col items-center gap-0.5 py-1 px-3',
                isActive ? 'text-brand-purple' : 'text-text-muted'
              )}
            >
              <Icon className="w-5 h-5" />
              <span className="text-[10px] font-medium">{tab.label}</span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
