'use client';

import { useState } from 'react';
import { Card, CardContent } from '@/components/Card';
import { Button } from '@/components/Button';
import { Modal } from '@/components/Modal';
import { mediaJobs } from '@/lib/mock-data';
import { Image, Video, Mic, Plus, Clock, Download, Play } from 'lucide-react';

type Tab = 'images' | 'videos' | 'speech';

export default function StudioPage() {
  const [activeTab, setActiveTab] = useState<Tab>('images');
  const [generateModalOpen, setGenerateModalOpen] = useState(false);
  const [generateType, setGenerateType] = useState<Tab>('images');

  const tabs = [
    { key: 'images' as Tab, label: 'Images', icon: Image },
    { key: 'videos' as Tab, label: 'Videos', icon: Video },
    { key: 'speech' as Tab, label: 'Speech', icon: Mic },
  ];

  const openGenerate = (type: Tab) => {
    setGenerateType(type);
    setGenerateModalOpen(true);
  };

  const filteredJobs = mediaJobs.filter((j) => j.type === activeTab.slice(0, -1) as 'image' | 'video' | 'speech');

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-semibold text-text-primary">Studio</h1>
          <p className="text-sm text-text-muted mt-0.5">Generate and manage media content</p>
        </div>
        <Button variant="primary" size="sm" onClick={() => openGenerate(activeTab)}>
          <Plus className="w-3.5 h-3.5 mr-1" />
          Generate New
        </Button>
      </div>

      <div className="flex items-center gap-1 p-1 bg-surface border border-border rounded-lg w-fit">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`flex items-center gap-1.5 px-4 py-1.5 rounded-md text-sm font-medium transition-colors ${
                activeTab === tab.key ? 'bg-surface-elevated text-text-primary border border-border' : 'text-text-muted hover:text-text-primary'
              }`}
            >
              <Icon className="w-3.5 h-3.5" />
              {tab.label}
            </button>
          );
        })}
      </div>

      {activeTab === 'images' && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {filteredJobs.map((img) => (
            <Card key={img.id} hover className="group">
              <div className="aspect-square bg-gradient-to-br from-brand-purple/20 to-brand-pink/20 rounded-t-lg flex items-center justify-center relative overflow-hidden">
                <Image className="w-8 h-8 text-text-muted" />
                <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-2">
                  <button className="p-2 rounded-full bg-white/10 hover:bg-white/20 text-white transition-colors">
                    <Download className="w-4 h-4" />
                  </button>
                </div>
              </div>
              <CardContent className="py-3">
                <p className="text-xs text-text-secondary line-clamp-2 mb-2">{img.prompt}</p>
                <div className="flex items-center justify-between text-[10px] text-text-muted">
                  <span>{img.model}</span>
                  <span>{img.createdAt}</span>
                </div>
                {img.status === 'running' && (
                  <div className="mt-2">
                    <div className="w-full h-1.5 rounded-full bg-surface-elevated overflow-hidden">
                      <div className="h-full rounded-full bg-brand-purple transition-all" style={{ width: `${img.progress}%` }} />
                    </div>
                    <p className="text-[10px] text-brand-purple mt-1">{img.progress}% - Generating...</p>
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {activeTab === 'videos' && (
        <div className="space-y-3">
          {filteredJobs.map((video) => (
            <Card key={video.id}>
              <CardContent className="py-3">
                <div className="flex items-center gap-4">
                  <div className="w-24 h-16 rounded-lg bg-surface-elevated flex items-center justify-center shrink-0">
                    <Video className="w-5 h-5 text-text-muted" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <h3 className="text-sm font-semibold text-text-primary">{video.model} Generation</h3>
                    <div className="flex items-center gap-2 mt-1 text-xs text-text-muted">
                      <span>{video.duration}</span>
                      <span>·</span>
                      <span>{video.createdAt}</span>
                    </div>
                    {video.status === 'running' && (
                      <div className="mt-2">
                        <div className="w-full h-1.5 rounded-full bg-surface-elevated overflow-hidden">
                          <div className="h-full rounded-full bg-status-running transition-all duration-500" style={{ width: `${video.progress}%` }} />
                        </div>
                        <p className="text-[10px] text-status-running mt-1">{video.progress}% - Generating...</p>
                      </div>
                    )}
                  </div>
                  <div className="flex items-center gap-2">
                    <span className={
                      video.status === 'completed' ? 'text-[10px] font-medium text-status-online' :
                      video.status === 'running' ? 'text-[10px] font-medium text-status-running' :
                      video.status === 'queued' ? 'text-[10px] font-medium text-text-muted' :
                      'text-[10px] font-medium text-status-offline'
                    }>
                      {video.status.charAt(0).toUpperCase() + video.status.slice(1)}
                    </span>
                    <Button variant="ghost" size="sm">
                      <Download className="w-3.5 h-3.5" />
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {activeTab === 'speech' && (
        <div className="space-y-3">
          {filteredJobs.map((job) => (
            <Card key={job.id}>
              <CardContent className="py-3">
                <div className="flex items-start gap-4">
                  <div className="w-10 h-10 rounded-lg bg-surface-elevated border border-border flex items-center justify-center shrink-0">
                    <Mic className="w-4 h-4 text-text-muted" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-text-secondary line-clamp-2">"{job.text}"</p>
                    <div className="flex items-center gap-2 mt-2 text-xs text-text-muted">
                      <span className="font-medium">{job.voice}</span>
                      <span>·</span>
                      <span>{job.duration}</span>
                      <span>·</span>
                      <span>{job.createdAt}</span>
                    </div>
                    {job.status === 'completed' && (
                      <div className="flex items-center gap-2 mt-3">
                        <div className="flex-1 h-8 bg-surface-elevated rounded-lg border border-border flex items-center px-3">
                          <div className="w-full h-1 rounded-full bg-border overflow-hidden">
                            <div className="w-1/3 h-full bg-brand-purple rounded-full" />
                          </div>
                        </div>
                        <Button variant="secondary" size="sm">
                          <Play className="w-3 h-3 mr-1" />
                          Play
                        </Button>
                        <Button variant="ghost" size="sm">
                          <Download className="w-3.5 h-3.5" />
                        </Button>
                      </div>
                    )}
                    {job.status === 'running' && (
                      <div className="mt-2">
                        <div className="flex items-center gap-2">
                          <div className="w-2 h-2 rounded-full bg-status-running animate-pulse" />
                          <span className="text-xs text-status-running">Generating audio...</span>
                        </div>
                      </div>
                    )}
                  </div>
                  <span className={`text-xs font-medium px-2 py-0.5 rounded-full shrink-0 ${
                    job.status === 'completed' ? 'bg-status-online/10 text-status-online' :
                    job.status === 'running' ? 'bg-status-running/10 text-status-running' :
                    'bg-surface-elevated text-text-muted border border-border'
                  }`}>
                    {job.status.charAt(0).toUpperCase() + job.status.slice(1)}
                  </span>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {filteredJobs.length === 0 && (
        <div className="text-center py-12">
          <p className="text-text-muted">No {activeTab} generated yet</p>
        </div>
      )}

      <Modal isOpen={generateModalOpen} onClose={() => setGenerateModalOpen(false)} title={`Generate ${generateType.charAt(0).toUpperCase() + generateType.slice(1)}`} size="md">
        <div className="space-y-4">
          {generateType === 'images' && (
            <>
              <div>
                <label className="block text-sm font-medium text-text-primary mb-1.5">Prompt</label>
                <textarea rows={3} placeholder="Describe the image you want to generate..." className="w-full px-3 py-2 bg-canvas border border-border rounded-lg text-sm text-text-primary placeholder:text-text-muted outline-none focus:border-border-strong transition-colors resize-none" />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-sm font-medium text-text-primary mb-1.5">Model</label>
                  <select className="w-full px-3 py-2 bg-canvas border border-border rounded-lg text-sm text-text-primary outline-none focus:border-border-strong">
                    <option>DALL-E 3</option>
                    <option>Midjourney v6</option>
                    <option>Stable Diffusion XL</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-text-primary mb-1.5">Size</label>
                  <select className="w-full px-3 py-2 bg-canvas border border-border rounded-lg text-sm text-text-primary outline-none focus:border-border-strong">
                    <option>1024x1024</option>
                    <option>1792x1024</option>
                    <option>1024x1792</option>
                  </select>
                </div>
              </div>
            </>
          )}
          {generateType === 'videos' && (
            <>
              <div>
                <label className="block text-sm font-medium text-text-primary mb-1.5">Prompt</label>
                <textarea rows={3} placeholder="Describe the video you want to generate..." className="w-full px-3 py-2 bg-canvas border border-border rounded-lg text-sm text-text-primary placeholder:text-text-muted outline-none focus:border-border-strong transition-colors resize-none" />
              </div>
              <div>
                <label className="block text-sm font-medium text-text-primary mb-1.5">Duration</label>
                <select className="w-full px-3 py-2 bg-canvas border border-border rounded-lg text-sm text-text-primary outline-none focus:border-border-strong">
                  <option>5 seconds</option>
                  <option>10 seconds</option>
                  <option>15 seconds</option>
                </select>
              </div>
            </>
          )}
          {generateType === 'speech' && (
            <>
              <div>
                <label className="block text-sm font-medium text-text-primary mb-1.5">Text</label>
                <textarea rows={4} placeholder="Enter the text you want to convert to speech..." className="w-full px-3 py-2 bg-canvas border border-border rounded-lg text-sm text-text-primary placeholder:text-text-muted outline-none focus:border-border-strong transition-colors resize-none" />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-sm font-medium text-text-primary mb-1.5">Voice</label>
                  <select className="w-full px-3 py-2 bg-canvas border border-border rounded-lg text-sm text-text-primary outline-none focus:border-border-strong">
                    <option>Nova (Natural)</option>
                    <option>Onyx (Professional)</option>
                    <option>Echo (Calm)</option>
                    <option>Fable (Narrative)</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-text-primary mb-1.5">Speed</label>
                  <select className="w-full px-3 py-2 bg-canvas border border-border rounded-lg text-sm text-text-primary outline-none focus:border-border-strong">
                    <option>0.75x (Slow)</option>
                    <option>1.0x (Normal)</option>
                    <option>1.25x (Fast)</option>
                    <option>1.5x (Very Fast)</option>
                  </select>
                </div>
              </div>
            </>
          )}
          <div className="flex items-center justify-end gap-2 pt-2">
            <Button variant="ghost" onClick={() => setGenerateModalOpen(false)}>Cancel</Button>
            <Button variant="primary"><Plus className="w-3.5 h-3.5 mr-1" />Generate</Button>
          </div>
        </div>
      </Modal>
    </div>
  );
}
