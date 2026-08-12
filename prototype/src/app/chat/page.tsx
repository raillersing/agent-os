'use client';

import { useState, useRef, useEffect } from 'react';
import { ChatMessage } from '@/components/ChatMessage';
import { ChatInput } from '@/components/ChatInput';
import { Button } from '@/components/Button';
import { agents, chatSessions, chatMessages } from '@/lib/mock-data';
import type { ChatMessage as ChatMessageType, ChatSession } from '@/lib/mock-data';
import { Search, Pin, Plus } from 'lucide-react';

export default function ChatPage() {
  const [sessions, setSessions] = useState<ChatSession[]>(chatSessions);
  const [activeSessionId, setActiveSessionId] = useState<string>(sessions[0]?.id || '');
  const [messages, setMessages] = useState<ChatMessageType[]>(chatMessages[activeSessionId] || []);
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setMessages(chatMessages[activeSessionId] || []);
  }, [activeSessionId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const handleSend = (text: string, modelId: string) => {
    const userMsg: ChatMessageType = {
      id: `m-${Date.now()}`,
      role: 'user',
      content: text,
      timestamp: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
    };
    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);
    setTimeout(() => {
      const agent = agents.find((a) => a.id === modelId);
      const agentMsg: ChatMessageType = {
        id: `m-${Date.now() + 1}`,
        role: 'agent',
        content: `I've processed your request regarding "${text.slice(0, 40)}...". Here's my analysis and recommendations.`,
        agentId: modelId,
        timestamp: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
        toolCalls: [{ name: 'Analysis', status: 'Completed' }],
      };
      setMessages((prev) => [...prev, agentMsg]);
      setIsLoading(false);
    }, 1500);
  };

  const handleNewSession = () => {
    const newSession: ChatSession = {
      id: `s-${Date.now()}`,
      title: 'New Conversation',
      lastMessage: 'Start chatting...',
      timestamp: 'Just now',
      model: 'Claude',
      agentId: 'claude',
    };
    setSessions([newSession, ...sessions]);
    setActiveSessionId(newSession.id);
    setMessages([]);
  };

  const filteredSessions = sessions.filter((s) =>
    s.title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const activeSession = sessions.find((s) => s.id === activeSessionId);
  const activeAgent = activeSession ? agents.find((a) => a.id === activeSession.agentId) : null;

  return (
    <div className="flex h-[calc(100vh-80px)] gap-0 rounded-xl border border-border bg-surface overflow-hidden">
      {/* Left Sidebar */}
      <div className="flex w-60 flex-col border-r border-border bg-surface md:w-64">
        <div className="flex items-center justify-between border-b border-border px-3 py-2.5">
          <span className="text-sm font-semibold text-text-primary">Conversations</span>
          <button onClick={handleNewSession} className="rounded-lg p-1 text-text-muted transition-colors hover:bg-surface-hover hover:text-text-primary">
            <Plus size={16} />
          </button>
        </div>
        <div className="border-b border-border px-3 py-2">
          <div className="relative">
            <Search size={14} className="absolute left-2.5 top-1/2 -translate-y-1/2 text-text-muted" />
            <input
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search sessions..."
              className="w-full rounded-lg border border-border bg-surface-elevated py-1.5 pl-8 pr-3 text-xs text-text-primary outline-none placeholder:text-text-muted focus:border-brand-purple"
            />
          </div>
        </div>
        <div className="flex-1 overflow-auto py-1">
          {filteredSessions.filter((s) => s.pinned).length > 0 && (
            <div className="px-3 py-1">
              <div className="mb-1 flex items-center gap-1 text-[10px] font-semibold uppercase tracking-wider text-text-muted">
                <Pin size={10} /> Pinned
              </div>
              {filteredSessions.filter((s) => s.pinned).map((s) => (
                <SessionButton key={s.id} session={s} active={activeSessionId === s.id} onClick={() => setActiveSessionId(s.id)} />
              ))}
            </div>
          )}
          <div className="px-3 py-1">
            <div className="mb-1 text-[10px] font-semibold uppercase tracking-wider text-text-muted">Recent</div>
            {filteredSessions.filter((s) => !s.pinned).map((s) => (
              <SessionButton key={s.id} session={s} active={activeSessionId === s.id} onClick={() => setActiveSessionId(s.id)} />
            ))}
          </div>
        </div>
      </div>

      {/* Center Chat */}
      <div className="flex flex-1 flex-col bg-canvas">
        <div className="flex items-center justify-between border-b border-border px-4 py-3">
          <div className="flex items-center gap-2">
            {activeAgent && <div className="h-3 w-3 rounded-full" style={{ backgroundColor: activeAgent.color }} />}
            <span className="text-sm font-medium text-text-primary">{activeSession?.title || 'New Conversation'}</span>
          </div>
          <span className="text-xs text-text-muted">{activeAgent?.model || ''}</span>
        </div>
        <div className="flex-1 overflow-auto px-4 py-4 space-y-4">
          {messages.length === 0 && !isLoading && (
            <div className="flex h-full items-center justify-center text-sm text-text-muted">Start a new conversation...</div>
          )}
          {messages.map((msg) => (
            <ChatMessage key={msg.id} message={msg} />
          ))}
          {isLoading && (
            <div className="flex items-start gap-3">
              <div className="flex h-8 w-8 items-center justify-center rounded-full" style={{ backgroundColor: activeAgent?.color || '#3B82F6' }}>
                <span className="text-[10px] font-bold text-white">{activeAgent?.name.slice(0, 2)}</span>
              </div>
              <div className="rounded-2xl bg-surface-elevated px-4 py-2.5 text-sm text-text-primary">
                <span className="inline-flex items-center gap-1">Thinking<span className="inline-block w-3 thinking-dots" /></span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
        <ChatInput onSend={handleSend} />
      </div>

      {/* Right Sidebar */}
      <div className="hidden w-60 flex-col border-l border-border bg-surface lg:flex">
        <div className="border-b border-border px-3 py-2.5">
          <span className="text-sm font-semibold text-text-primary">Context</span>
        </div>
        <div className="flex-1 space-y-4 overflow-auto p-3">
          {activeAgent && (
            <div className="rounded-lg border border-border bg-surface-elevated p-3">
              <div className="mb-2 text-[10px] font-semibold uppercase tracking-wider text-text-muted">Agent</div>
              <div className="flex items-center gap-2">
                <div className="h-6 w-6 rounded-full" style={{ backgroundColor: activeAgent.color }} />
                <div>
                  <div className="text-xs font-medium text-text-primary">{activeAgent.name}</div>
                  <div className="text-[10px] text-text-muted">{activeAgent.role}</div>
                </div>
              </div>
            </div>
          )}
          <div className="rounded-lg border border-border bg-surface-elevated p-3">
            <div className="mb-2 text-[10px] font-semibold uppercase tracking-wider text-text-muted">Model</div>
            <div className="space-y-1 text-xs text-text-secondary">
              <div className="flex justify-between"><span>Temperature</span><span className="font-mono text-text-primary">0.7</span></div>
              <div className="flex justify-between"><span>Max Tokens</span><span className="font-mono text-text-primary">4K</span></div>
              <div className="flex justify-between"><span>Context</span><span className="font-mono text-text-primary">128K</span></div>
            </div>
          </div>
          <div className="rounded-lg border border-border bg-surface-elevated p-3">
            <div className="mb-2 text-[10px] font-semibold uppercase tracking-wider text-text-muted">Token Usage</div>
            <div className="space-y-1">
              <div className="flex justify-between text-xs"><span className="text-text-secondary">Input</span><span className="font-mono text-text-primary">1,247</span></div>
              <div className="flex justify-between text-xs"><span className="text-text-secondary">Output</span><span className="font-mono text-text-primary">892</span></div>
              <div className="h-px bg-border my-1" />
              <div className="flex justify-between text-xs"><span className="text-text-secondary">Total</span><span className="font-mono text-brand-purple">2,139</span></div>
            </div>
          </div>
          <div className="rounded-lg border border-border bg-surface-elevated p-3">
            <div className="mb-2 text-[10px] font-semibold uppercase tracking-wider text-text-muted">Attached Files</div>
            <div className="text-xs text-text-muted">No files attached</div>
          </div>
        </div>
      </div>
    </div>
  );
}

function SessionButton({ session, active, onClick }: { session: ChatSession; active: boolean; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className={`w-full rounded-lg px-2 py-2 text-left transition-colors ${active ? 'bg-brand-purple/10' : 'hover:bg-surface-hover'}`}
    >
      <div className={`text-xs font-medium ${active ? 'text-brand-purple' : 'text-text-primary'}`}>{session.title}</div>
      <div className="mt-0.5 truncate text-[10px] text-text-muted">{session.lastMessage}</div>
      <div className="mt-0.5 flex items-center justify-between text-[10px] text-text-muted">
        <span>{session.model}</span>
        <span>{session.timestamp}</span>
      </div>
    </button>
  );
}
