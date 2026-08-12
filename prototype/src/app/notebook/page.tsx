'use client';

import { useState } from 'react';
import { Card } from '@/components/Card';
import { Button } from '@/components/Button';
import { notes as mockNotes } from '@/lib/mock-data';
import type { Note } from '@/lib/mock-data';
import { Search, FileText, Folder, Plus, Clock } from 'lucide-react';

function renderMarkdown(text: string): React.ReactNode {
  const lines = text.split('\n');
  const elements: React.ReactNode[] = [];
  let inCodeBlock = false;
  let codeContent: string[] = [];

  lines.forEach((line, idx) => {
    if (line.startsWith('```')) {
      if (!inCodeBlock) {
        inCodeBlock = true;
        codeContent = [];
      } else {
        inCodeBlock = false;
        elements.push(
          <pre key={`code-${idx}`} className="bg-surface-elevated rounded-lg p-3 my-3 overflow-x-auto border border-border">
            <code className="text-xs font-mono text-text-secondary">{codeContent.join('\n')}</code>
          </pre>
        );
      }
      return;
    }
    if (inCodeBlock) {
      codeContent.push(line);
      return;
    }
    if (line.trim() === '') {
      elements.push(<div key={idx} className="h-2" />);
      return;
    }
    if (line.startsWith('# ')) {
      elements.push(<h1 key={idx} className="text-xl font-bold text-text-primary mt-4 mb-2">{line.replace('# ', '')}</h1>);
      return;
    }
    if (line.startsWith('## ')) {
      elements.push(<h2 key={idx} className="text-lg font-semibold text-text-primary mt-3 mb-1.5">{line.replace('## ', '')}</h2>);
      return;
    }
    if (line.startsWith('### ')) {
      elements.push(<h3 key={idx} className="text-sm font-semibold text-text-primary mt-2 mb-1">{line.replace('### ', '')}</h3>);
      return;
    }
    const checkMatch = line.match(/^(\s*)- \[([ x])\] (.+)$/);
    if (checkMatch) {
      const checked = checkMatch[2] === 'x';
      elements.push(
        <div key={idx} className="flex items-center gap-2 py-0.5">
          <div className={`w-3.5 h-3.5 rounded border flex items-center justify-center ${checked ? 'bg-brand-purple border-brand-purple' : 'border-border'}`}>
            {checked && <span className="text-[8px] text-white">✓</span>}
          </div>
          <span className={`text-sm ${checked ? 'text-text-muted line-through' : 'text-text-secondary'}`}>{checkMatch[3]}</span>
        </div>
      );
      return;
    }
    const bulletMatch = line.match(/^(\s*)- (.+)$/);
    if (bulletMatch) {
      elements.push(<li key={idx} className="flex items-start gap-2 py-0.5 ml-4"><span className="w-1 h-1 rounded-full bg-text-muted mt-2 shrink-0" /><span className="text-sm text-text-secondary">{bulletMatch[2]}</span></li>);
      return;
    }
    const numMatch = line.match(/^(\d+)\. (.+)$/);
    if (numMatch) {
      elements.push(<div key={idx} className="flex items-start gap-2 py-0.5 ml-4"><span className="text-xs text-text-muted font-mono mt-0.5">{numMatch[1]}.</span><span className="text-sm text-text-secondary">{numMatch[2]}</span></div>);
      return;
    }
    const wikiRegex = /\[\[(.+?)\]\]/g;
    let lastIndex = 0;
    const parts: React.ReactNode[] = [];
    let match: RegExpExecArray | null;
    let partIdx = 0;
    while ((match = wikiRegex.exec(line)) !== null) {
      if (match.index > lastIndex) parts.push(<span key={`text-${partIdx++}`}>{line.slice(lastIndex, match.index)}</span>);
      parts.push(<button key={`wiki-${partIdx++}`} className="text-brand-purple hover:underline font-medium">{match[1]}</button>);
      lastIndex = match.index + match[0].length;
    }
    if (lastIndex < line.length) parts.push(<span key={`text-${partIdx++}`}>{line.slice(lastIndex)}</span>);
    if (parts.length > 0) {
      elements.push(<p key={idx} className="text-sm text-text-secondary py-0.5">{parts}</p>);
    } else {
      elements.push(<p key={idx} className="text-sm text-text-secondary py-0.5">{line}</p>);
    }
  });

  return elements;
}

export default function NotebookPage() {
  const [selectedNote, setSelectedNote] = useState<Note | null>(mockNotes[0]);
  const [noteList, setNoteList] = useState<Note[]>(mockNotes);
  const [searchQuery, setSearchQuery] = useState('');

  const folders = [...new Set(noteList.map((n) => n.folder))];
  const filteredNotes = noteList.filter((note) =>
    note.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    note.content.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleNewNote = () => {
    const newNote: Note = {
      id: String(Date.now()),
      title: 'Untitled Note',
      content: '# New Note\n\nStart writing here...',
      folder: 'Drafts',
      updatedAt: 'Just now',
    };
    setNoteList([newNote, ...noteList]);
    setSelectedNote(newNote);
  };

  return (
    <div className="h-[calc(100vh-theme(spacing.header)-theme(spacing.14))] lg:h-[calc(100vh-theme(spacing.header))] flex">
      <div className="w-64 md:w-72 border-r border-border bg-surface flex flex-col shrink-0">
        <div className="p-3 border-b border-border">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-sm font-semibold text-text-primary">Notebook</h2>
            <Button variant="ghost" size="sm" onClick={handleNewNote}>
              <Plus className="w-4 h-4" />
            </Button>
          </div>
          <div className="relative">
            <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-text-muted" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search notes..."
              className="w-full pl-8 pr-3 py-1.5 bg-canvas border border-border rounded-lg text-xs text-text-primary placeholder:text-text-muted outline-none focus:border-border-strong transition-colors"
            />
          </div>
        </div>
        <div className="flex-1 overflow-y-auto p-2 space-y-1">
          {folders.map((folder) => {
            const folderNotes = filteredNotes.filter((n) => n.folder === folder);
            if (folderNotes.length === 0) return null;
            return (
              <div key={folder}>
                <div className="flex items-center gap-1.5 px-2 py-1.5 text-[10px] font-semibold text-text-muted uppercase tracking-wider">
                  <Folder className="w-3 h-3" />
                  {folder}
                </div>
                <div className="space-y-0.5">
                  {folderNotes.map((note) => (
                    <button
                      key={note.id}
                      onClick={() => setSelectedNote(note)}
                      className={`w-full flex items-start gap-2 px-2 py-1.5 rounded-lg text-left transition-colors ${
                        selectedNote?.id === note.id
                          ? 'bg-brand-purple/10 border border-brand-purple/20'
                          : 'hover:bg-surface-hover border border-transparent'
                      }`}
                    >
                      <FileText className={`w-3.5 h-3.5 mt-0.5 shrink-0 ${selectedNote?.id === note.id ? 'text-brand-purple' : 'text-text-muted'}`} />
                      <div className="flex-1 min-w-0">
                        <p className={`text-xs font-medium truncate ${selectedNote?.id === note.id ? 'text-brand-purple' : 'text-text-primary'}`}>{note.title}</p>
                        <div className="flex items-center gap-1 mt-0.5">
                          <Clock className="w-2.5 h-2.5 text-text-muted" />
                          <span className="text-[10px] text-text-muted">{note.updatedAt}</span>
                        </div>
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            );
          })}
          {filteredNotes.length === 0 && (
            <div className="text-center py-8">
              <Search className="w-8 h-8 text-text-muted mx-auto mb-2" />
              <p className="text-xs text-text-muted">No notes found</p>
            </div>
          )}
        </div>
      </div>
      <div className="flex-1 overflow-y-auto bg-canvas">
        {selectedNote ? (
          <div className="max-w-3xl mx-auto p-6 md:p-8">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h1 className="text-2xl font-bold text-text-primary">{selectedNote.title}</h1>
                <div className="flex items-center gap-2 mt-1">
                  <span className="text-xs text-text-muted">{selectedNote.folder}</span>
                  <span className="text-text-muted">·</span>
                  <span className="text-xs text-text-muted">{selectedNote.updatedAt}</span>
                </div>
              </div>
              <Button variant="secondary" size="sm">Edit</Button>
            </div>
            <div className="prose prose-invert max-w-none">
              {renderMarkdown(selectedNote.content)}
            </div>
          </div>
        ) : (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <FileText className="w-12 h-12 text-text-muted mx-auto mb-3" />
              <p className="text-text-muted">Select a note to view its contents</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
