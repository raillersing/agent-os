'use client';

import { useState, useEffect, useRef } from 'react';
import { Search, X, Home, LayoutDashboard, MessageSquare, Notebook, Settings, Users, Sparkles } from 'lucide-react';
import Link from 'next/link';

const pages = [
  { name: 'Mission Control', href: '/', icon: Home },
  { name: 'Mission Board', href: '/board', icon: LayoutDashboard },
  { name: 'Chat', href: '/chat', icon: MessageSquare },
  { name: 'Notebook', href: '/notebook', icon: Notebook },
  { name: 'Agents', href: '/agents', icon: Users },
  { name: 'Studio', href: '/studio', icon: Sparkles },
  { name: 'Workspace', href: '/workspace', icon: LayoutDashboard },
  { name: 'Settings', href: '/settings', icon: Settings },
];

const agents = [
  { name: 'Claude', color: '#F97316' },
  { name: 'Kimi', color: '#22D3EE' },
  { name: 'Grok', color: '#EF4444' },
  { name: 'Hermes', color: '#3B82F6' },
];

interface CommandPaletteProps {
  isOpen: boolean;
  onClose: () => void;
}

export function CommandPalette({ isOpen, onClose }: CommandPaletteProps) {
  const [query, setQuery] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);
  const overlayRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        onClose();
      }
      if (e.key === 'Escape') onClose();
    };

    if (isOpen) {
      document.addEventListener('keydown', handleKeyDown);
      setTimeout(() => inputRef.current?.focus(), 50);
      document.body.style.overflow = 'hidden';
    }
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      document.body.style.overflow = '';
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const filteredPages = pages.filter((p) =>
    p.name.toLowerCase().includes(query.toLowerCase())
  );

  const filteredAgents = agents.filter((a) =>
    a.name.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div
      ref={overlayRef}
      className="fixed inset-0 z-50 flex items-start justify-center bg-black/50 pt-[15vh] animate-fade-in"
      onClick={(e) => {
        if (e.target === overlayRef.current) onClose();
      }}
    >
      <div className="w-full max-w-lg overflow-hidden rounded-xl border border-border bg-surface-elevated shadow-2xl">
        <div className="flex items-center gap-3 border-b border-border px-4 py-3">
          <Search size={18} className="text-text-muted" />
          <input
            ref={inputRef}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search pages, agents, tasks..."
            className="flex-1 bg-transparent text-sm text-text-primary outline-none placeholder:text-text-muted"
          />
          <kbd className="rounded border border-border bg-surface px-1.5 py-0.5 text-[10px] text-text-muted">
            ESC
          </kbd>
        </div>

        <div className="max-h-[60vh] overflow-auto p-2">
          {query === '' && (
            <>
              <div className="px-2 py-1.5 text-xs font-medium text-text-muted">Recent Pages</div>
              {pages.slice(0, 4).map((page) => (
                <Link
                  key={page.name}
                  href={page.href}
                  onClick={onClose}
                  className="flex items-center gap-3 rounded-lg px-2 py-2 text-sm text-text-primary hover:bg-surface-hover"
                >
                  <page.icon size={16} className="text-text-muted" />
                  {page.name}
                </Link>
              ))}
              <div className="mt-2 px-2 py-1.5 text-xs font-medium text-text-muted">Agents</div>
              {agents.map((agent) => (
                <div
                  key={agent.name}
                  className="flex items-center gap-3 rounded-lg px-2 py-2 text-sm text-text-primary hover:bg-surface-hover"
                >
                  <span
                    className="h-4 w-4 rounded-full"
                    style={{ backgroundColor: agent.color }}
                  />
                  {agent.name}
                </div>
              ))}
            </>
          )}

          {query !== '' && (
            <>
              {filteredPages.length > 0 && (
                <>
                  <div className="px-2 py-1.5 text-xs font-medium text-text-muted">Pages</div>
                  {filteredPages.map((page) => (
                    <Link
                      key={page.name}
                      href={page.href}
                      onClick={onClose}
                      className="flex items-center gap-3 rounded-lg px-2 py-2 text-sm text-text-primary hover:bg-surface-hover"
                    >
                      <page.icon size={16} className="text-text-muted" />
                      {page.name}
                    </Link>
                  ))}
                </>
              )}
              {filteredAgents.length > 0 && (
                <>
                  <div className="mt-2 px-2 py-1.5 text-xs font-medium text-text-muted">Agents</div>
                  {filteredAgents.map((agent) => (
                    <div
                      key={agent.name}
                      className="flex items-center gap-3 rounded-lg px-2 py-2 text-sm text-text-primary hover:bg-surface-hover"
                    >
                      <span
                        className="h-4 w-4 rounded-full"
                        style={{ backgroundColor: agent.color }}
                      />
                      {agent.name}
                    </div>
                  ))}
                </>
              )}
              {filteredPages.length === 0 && filteredAgents.length === 0 && (
                <div className="px-2 py-4 text-center text-sm text-text-muted">
                  No results found for "{query}"
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
