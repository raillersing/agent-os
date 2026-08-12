'use client';

import { useState } from 'react';
import { Button } from './Button';
import { Send, Paperclip, ChevronDown } from 'lucide-react';
import { agents } from '@/lib/mock-data';

interface ChatInputProps {
  onSend: (message: string, modelId: string) => void;
}

export function ChatInput({ onSend }: ChatInputProps) {
  const [text, setText] = useState('');
  const [modelId, setModelId] = useState('claude');
  const [modelOpen, setModelOpen] = useState(false);

  const selectedAgent = agents.find((a) => a.id === modelId) || agents[0];

  const handleSend = () => {
    if (!text.trim()) return;
    onSend(text.trim(), modelId);
    setText('');
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="border-t border-border bg-surface-elevated p-3">
      <div className="flex items-end gap-2">
        <div className="relative">
          <button
            onClick={() => setModelOpen(!modelOpen)}
            className="flex items-center gap-1.5 rounded-lg border border-border bg-surface px-2.5 py-2 text-xs text-text-primary hover:bg-surface-hover"
          >
            <span className="h-2.5 w-2.5 rounded-full" style={{ backgroundColor: selectedAgent.color }} />
            {selectedAgent.name}
            <ChevronDown size={12} className="text-text-muted" />
          </button>
          {modelOpen && (
            <div className="absolute bottom-full left-0 mb-1 w-40 overflow-hidden rounded-lg border border-border bg-surface-elevated shadow-xl">
              {agents.map((agent) => (
                <button
                  key={agent.id}
                  onClick={() => {
                    setModelId(agent.id);
                    setModelOpen(false);
                  }}
                  className="flex w-full items-center gap-2 px-3 py-2 text-left text-xs text-text-primary hover:bg-surface-hover"
                >
                  <span className="h-2.5 w-2.5 rounded-full" style={{ backgroundColor: agent.color }} />
                  {agent.name}
                </button>
              ))}
            </div>
          )}
        </div>

        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type a message..."
          rows={1}
          className="max-h-32 min-h-[38px] flex-1 resize-none rounded-lg border border-border bg-surface px-3 py-2 text-sm text-text-primary outline-none placeholder:text-text-muted focus:border-brand-purple"
        />

        <button className="rounded-lg p-2 text-text-muted transition-colors hover:bg-surface-hover hover:text-text-primary">
          <Paperclip size={18} />
        </button>

        <Button variant="primary" size="sm" onClick={handleSend} className="px-3">
          <Send size={14} />
        </Button>
      </div>
    </div>
  );
}
