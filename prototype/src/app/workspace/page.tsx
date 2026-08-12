'use client';

import { useState } from 'react';
import { ArtifactCard } from '@/components/ArtifactCard';
import { Modal } from '@/components/Modal';
import { Button } from '@/components/Button';
import { AgentIcon } from '@/components/AgentIcon';
import { artifacts, agents } from '@/lib/mock-data';
import type { Artifact } from '@/lib/mock-data';
import { Search, Image, Video, Music, FileText, Download } from 'lucide-react';

const tabs = [
  { key: 'all', label: 'All', icon: Search },
  { key: 'image', label: 'Images', icon: Image },
  { key: 'video', label: 'Videos', icon: Video },
  { key: 'audio', label: 'Audio', icon: Music },
  { key: 'document', label: 'Documents', icon: FileText },
];

export default function WorkspacePage() {
  const [activeTab, setActiveTab] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedArtifact, setSelectedArtifact] = useState<Artifact | null>(null);

  const filtered = artifacts.filter((a) => {
    if (activeTab !== 'all' && a.type !== activeTab) return false;
    if (searchQuery && !a.title.toLowerCase().includes(searchQuery.toLowerCase())) return false;
    return true;
  });

  const iconMap = { image: Image, video: Video, audio: Music, document: FileText };
  const PreviewIcon = selectedArtifact ? iconMap[selectedArtifact.type] : FileText;

  return (
    <div className="space-y-4">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-xl font-bold text-text-primary">Workspace</h1>
          <p className="text-sm text-text-secondary">Browse and manage generated artifacts</p>
        </div>
        <Button variant="secondary" size="sm">
          <Download size={14} className="mr-1" />
          Export Selected
        </Button>
      </div>

      <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
        <div className="flex items-center gap-1 rounded-lg border border-border bg-surface p-1">
          {tabs.map((tab) => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`flex items-center gap-1.5 rounded-md px-3 py-1.5 text-xs font-medium transition-colors ${
                activeTab === tab.key ? 'bg-surface-elevated text-text-primary shadow-sm' : 'text-text-muted hover:text-text-secondary'
              }`}
            >
              <tab.icon size={14} />
              {tab.label}
            </button>
          ))}
        </div>
        <div className="relative flex-1 max-w-xs">
          <Search size={14} className="absolute left-2.5 top-1/2 -translate-y-1/2 text-text-muted" />
          <input
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search artifacts..."
            className="w-full rounded-lg border border-border bg-surface px-3 py-2 pl-8 text-sm text-text-primary outline-none placeholder:text-text-muted focus:border-brand-purple"
          />
        </div>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {filtered.map((artifact) => (
          <ArtifactCard key={artifact.id} artifact={artifact} onClick={() => setSelectedArtifact(artifact)} />
        ))}
      </div>

      {filtered.length === 0 && (
        <div className="py-12 text-center text-sm text-text-muted">No artifacts found.</div>
      )}

      <Modal isOpen={!!selectedArtifact} onClose={() => setSelectedArtifact(null)} title={selectedArtifact?.title}>
        {selectedArtifact && (
          <div className="space-y-4">
            <div className="flex aspect-video items-center justify-center rounded-xl bg-surface-elevated border border-border">
              <PreviewIcon size={48} className="text-text-muted" />
            </div>
            <div className="grid grid-cols-2 gap-3 text-sm">
              <div>
                <div className="text-[10px] uppercase tracking-wider text-text-muted">Type</div>
                <div className="capitalize text-text-primary">{selectedArtifact.type}</div>
              </div>
              <div>
                <div className="text-[10px] uppercase tracking-wider text-text-muted">Size</div>
                <div className="text-text-primary">{selectedArtifact.size}</div>
              </div>
              <div>
                <div className="text-[10px] uppercase tracking-wider text-text-muted">Created</div>
                <div className="text-text-primary">{selectedArtifact.date}</div>
              </div>
              {selectedArtifact.duration && (
                <div>
                  <div className="text-[10px] uppercase tracking-wider text-text-muted">Duration</div>
                  <div className="text-text-primary">{selectedArtifact.duration}</div>
                </div>
              )}
            </div>
            <div className="flex items-center gap-2">
              {(() => {
                const a = agents.find((ag) => ag.id === selectedArtifact.agentId);
                return a ? <AgentIcon name={a.name} color={a.color} size="sm" /> : null;
              })()}
              <span className="text-xs text-text-muted">{selectedArtifact.agent}</span>
            </div>
            {selectedArtifact.type === 'audio' && (
              <div className="rounded-lg border border-border bg-surface p-3">
                <audio controls className="w-full" />
              </div>
            )}
            <div className="flex justify-end gap-2">
              <Button variant="ghost" onClick={() => setSelectedArtifact(null)}>Close</Button>
              <Button variant="primary"><Download size={14} className="mr-1" />Download</Button>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
}
