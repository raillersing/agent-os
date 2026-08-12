'use client';

import { AgentIcon } from './AgentIcon';
import { agents } from '@/lib/mock-data';
import type { Artifact } from '@/lib/mock-data';
import { Image, Video, Music, FileText, Download } from 'lucide-react';

interface ArtifactCardProps {
  artifact: Artifact;
  onClick?: () => void;
}

export function ArtifactCard({ artifact, onClick }: ArtifactCardProps) {
  const agent = agents.find((a) => a.id === artifact.agentId);

  const iconMap = {
    image: Image,
    video: Video,
    audio: Music,
    document: FileText,
  };

  const Icon = iconMap[artifact.type];

  return (
    <div
      onClick={onClick}
      className="group cursor-pointer overflow-hidden rounded-xl border border-border bg-surface transition-all hover:border-border-strong hover:shadow-lg"
    >
      <div className="relative flex aspect-video items-center justify-center bg-surface-elevated">
        <Icon size={32} className="text-text-muted" />
        <div className="absolute inset-0 flex items-center justify-center bg-black/40 opacity-0 transition-opacity group-hover:opacity-100">
          <Download size={20} className="text-white" />
        </div>
      </div>
      <div className="p-3">
        <div className="mb-1 text-sm font-medium text-text-primary line-clamp-1">{artifact.title}</div>
        <div className="flex items-center justify-between text-[10px] text-text-muted">
          <div className="flex items-center gap-1.5">
            {agent && <AgentIcon name={agent.name} color={agent.color} size="sm" />}
            <span>{agent?.name || 'Unknown'}</span>
          </div>
          <span>{artifact.size}</span>
        </div>
        <div className="mt-1 text-[10px] text-text-muted">{artifact.date}</div>
      </div>
    </div>
  );
}
