'use client';

import { useState } from 'react';
import { Search, Bell, Command, CheckCircle2 } from 'lucide-react';
import { CommandPalette } from './CommandPalette';
import { cn } from '@/lib/utils';

export function Header() {
  const [cmdOpen, setCmdOpen] = useState(false);
  const [allSystems, setAllSystems] = useState(true);

  return (
    <>
      <header className="fixed top-0 left-0 right-0 h-header bg-canvas/80 backdrop-blur-xl border-b border-border z-50">
        <div className="flex items-center h-full px-4 lg:pl-sidebar">
          <div className="flex items-center gap-3 flex-1">
            <button
              onClick={() => setCmdOpen(true)}
              className={cn(
                'hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-lg',
                'bg-surface border border-border hover:border-border-strong transition-colors',
                'text-text-muted text-sm'
              )}
            >
              <Search className="w-3.5 h-3.5" />
              <span className="text-xs">Search...</span>
              <kbd className="ml-2 px-1.5 py-0.5 rounded bg-surface-elevated text-[10px] font-mono border border-border">
                ⌘K
              </kbd>
            </button>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setAllSystems(!allSystems)}
              className={cn(
                'flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-colors',
                allSystems
                  ? 'bg-status-online/10 text-status-online border border-status-online/20'
                  : 'bg-status-offline/10 text-status-offline border border-status-offline/20'
              )}
            >
              <CheckCircle2 className="w-3.5 h-3.5" />
              {allSystems ? 'ALL SYSTEMS' : 'ISSUES DETECTED'}
            </button>

            <button className="relative p-2 rounded-lg hover:bg-surface-hover text-text-muted hover:text-text-primary transition-colors">
              <Bell className="w-4 h-4" />
              <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-brand-pink" />
            </button>

            <div className="flex items-center gap-2 ml-1 pl-2 border-l border-border">
              <div className="text-right hidden sm:block">
                <p className="text-xs font-medium text-text-primary">Julian Goldie</p>
                <p className="text-[10px] text-text-muted">Admin</p>
              </div>
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-brand-purple to-brand-pink flex items-center justify-center text-xs font-bold text-white">
                JG
              </div>
            </div>
          </div>
        </div>
      </header>

      <CommandPalette isOpen={cmdOpen} onClose={() => setCmdOpen(false)} />
    </>
  );
}
