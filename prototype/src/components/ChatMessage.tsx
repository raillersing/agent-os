'use client';

import { AgentIcon } from './AgentIcon';
import { agents } from '@/lib/mock-data';
import type { ChatMessage as ChatMessageType } from '@/lib/mock-data';
import { User } from 'lucide-react';

interface ChatMessageProps {
  message: ChatMessageType;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user';
  const agent = message.agentId ? agents.find((a) => a.id === message.agentId) : null;

  return (
    <div className={`flex gap-3 ${isUser ? 'flex-row-reverse' : ''}`}>
      <div className="shrink-0">
        {isUser ? (
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gradient-to-br from-brand-purple to-brand-pink">
            <User size={14} className="text-white" />
          </div>
        ) : agent ? (
          <AgentIcon name={agent.name} color={agent.color} size="md" />
        ) : (
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-surface-hover">
            <span className="text-[10px] text-text-muted">AI</span>
          </div>
        )}
      </div>

      <div className={`max-w-[80%] ${isUser ? 'items-end' : 'items-start'} flex flex-col gap-1`}>
        <div
          className={`rounded-2xl px-4 py-2.5 text-sm leading-relaxed ${
            isUser
              ? 'bg-brand-purple text-white'
              : 'bg-surface-elevated text-text-primary'
          }`}
        >
          {message.content}
        </div>

        {message.toolCalls && message.toolCalls.length > 0 && (
          <div className="w-full space-y-1.5">
            {message.toolCalls.map((tc, i) => (
              <div
                key={i}
                className="flex items-center gap-2 rounded-lg border border-border bg-surface px-3 py-2 text-xs text-text-secondary"
              >
                <div className="h-2 w-2 animate-pulse rounded-full bg-brand-purple" />
                {tc.name}: {tc.status}
              </div>
            ))}
          </div>
        )}

        {message.codeBlocks && message.codeBlocks.length > 0 && (
          <div className="w-full space-y-2">
            {message.codeBlocks.map((cb, i) => (
              <div key={i} className="overflow-hidden rounded-lg border border-border bg-[#0d0d0f]">
                <div className="flex items-center justify-between border-b border-border px-3 py-1.5">
                  <span className="text-[10px] font-mono uppercase text-text-muted">{cb.language}</span>
                </div>
                <pre className="overflow-x-auto p-3 text-xs">
                  <code className="font-mono text-text-primary">{cb.code}</code>
                </pre>
              </div>
            ))}
          </div>
        )}

        <span className="text-[10px] text-text-muted">{message.timestamp}</span>
      </div>
    </div>
  );
}
