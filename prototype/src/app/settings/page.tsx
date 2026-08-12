'use client';

import { useState } from 'react';
import { Card, CardContent } from '@/components/Card';
import { Button } from '@/components/Button';
import { agents } from '@/lib/mock-data';
import { User, Bot, KeyRound, Palette, Shield, Eye, EyeOff, Trash2 } from 'lucide-react';

type SettingsTab = 'profile' | 'agents' | 'providers' | 'appearance' | 'security';

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState<SettingsTab>('profile');
  const [showKeys, setShowKeys] = useState<Record<string, boolean>>({});
  const [agentToggles, setAgentToggles] = useState<Record<string, boolean>>(
    Object.fromEntries(agents.map((a) => [a.id, true]))
  );
  const [density, setDensity] = useState('normal');
  const [fontSize, setFontSize] = useState('medium');
  const [twoFA, setTwoFA] = useState(false);

  const tabs = [
    { key: 'profile' as SettingsTab, label: 'Profile', icon: User },
    { key: 'agents' as SettingsTab, label: 'Agents', icon: Bot },
    { key: 'providers' as SettingsTab, label: 'Providers', icon: KeyRound },
    { key: 'appearance' as SettingsTab, label: 'Appearance', icon: Palette },
    { key: 'security' as SettingsTab, label: 'Security', icon: Shield },
  ];

  const toggleKey = (key: string) => setShowKeys((prev) => ({ ...prev, [key]: !prev[key] }));
  const toggleAgent = (id: string) => setAgentToggles((prev) => ({ ...prev, [id]: !prev[id] }));

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-semibold text-text-primary">Settings</h1>
        <p className="text-sm text-text-muted mt-0.5">Configure your Agent OS workspace</p>
      </div>

      <div className="flex flex-col lg:flex-row gap-6">
        <div className="w-full lg:w-52 shrink-0">
          <div className="flex lg:flex-col gap-1 p-1 bg-surface border border-border rounded-lg overflow-x-auto lg:overflow-visible">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.key}
                  onClick={() => setActiveTab(tab.key)}
                  className={`flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium transition-colors whitespace-nowrap ${
                    activeTab === tab.key ? 'bg-brand-purple/10 text-brand-purple' : 'text-text-secondary hover:text-text-primary hover:bg-surface-hover'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  {tab.label}
                </button>
              );
            })}
          </div>
        </div>

        <div className="flex-1 min-w-0">
          {activeTab === 'profile' && (
            <div className="space-y-4">
              <Card>
                <CardContent className="py-4">
                  <div className="flex items-center gap-4 mb-6">
                    <div className="w-16 h-16 rounded-full bg-gradient-to-br from-brand-purple to-brand-pink flex items-center justify-center text-xl font-bold text-white">JG</div>
                    <div><Button variant="secondary" size="sm">Change Avatar</Button></div>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-text-primary mb-1.5">Full Name</label>
                      <input type="text" defaultValue="Julian Goldie" className="w-full px-3 py-2 bg-canvas border border-border rounded-lg text-sm text-text-primary outline-none focus:border-border-strong" />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-text-primary mb-1.5">Email</label>
                      <input type="email" defaultValue="julian@agentos.ai" className="w-full px-3 py-2 bg-canvas border border-border rounded-lg text-sm text-text-primary outline-none focus:border-border-strong" />
                    </div>
                    <div className="md:col-span-2">
                      <label className="block text-sm font-medium text-text-primary mb-1.5">Workspace Name</label>
                      <input type="text" defaultValue="Goldie Digital" className="w-full px-3 py-2 bg-canvas border border-border rounded-lg text-sm text-text-primary outline-none focus:border-border-strong" />
                    </div>
                  </div>
                  <div className="flex justify-end mt-4">
                    <Button variant="primary">Save Changes</Button>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}

          {activeTab === 'agents' && (
            <div className="space-y-3">
              {agents.map((agent) => (
                <Card key={agent.id}>
                  <CardContent className="py-3">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className={`w-3 h-3 rounded-full ${agentToggles[agent.id] ? 'bg-status-online' : 'bg-text-muted'}`} />
                        <div className="w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold text-white" style={{ backgroundColor: agent.color }}>
                          {agent.name.slice(0, 2).toUpperCase()}
                        </div>
                        <div>
                          <p className="text-sm font-medium text-text-primary">{agent.name}</p>
                          <p className="text-xs text-text-muted">{agent.role}</p>
                        </div>
                      </div>
                      <button onClick={() => toggleAgent(agent.id)} className={`relative w-10 h-5 rounded-full transition-colors ${agentToggles[agent.id] ? 'bg-brand-purple' : 'bg-surface-elevated border border-border'}`}>
                        <div className={`absolute top-0.5 w-4 h-4 rounded-full bg-white transition-transform ${agentToggles[agent.id] ? 'left-5' : 'left-0.5'}`} />
                      </button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}

          {activeTab === 'providers' && (
            <div className="space-y-4">
              {[
                { name: 'Kimi', placeholder: 'sk-kimi-...' },
                { name: 'Claude', placeholder: 'sk-ant-...' },
                { name: 'Grok', placeholder: 'sk-xai-...' },
                { name: 'OpenRouter', placeholder: 'sk-or-...' },
              ].map((provider) => (
                <Card key={provider.name}>
                  <CardContent className="py-4">
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="text-sm font-semibold text-text-primary">{provider.name} API Key</h3>
                      <Button variant="ghost" size="sm">Test Connection</Button>
                    </div>
                    <div className="relative">
                      <input type={showKeys[provider.name] ? 'text' : 'password'} placeholder={provider.placeholder} defaultValue={showKeys[provider.name] ? 'sk-demo-1234567890abcdef' : '••••••••••••••••••••'} className="w-full px-3 py-2 pr-10 bg-canvas border border-border rounded-lg text-sm text-text-primary placeholder:text-text-muted outline-none focus:border-border-strong font-mono" />
                      <button onClick={() => toggleKey(provider.name)} className="absolute right-3 top-1/2 -translate-y-1/2 text-text-muted hover:text-text-primary">
                        {showKeys[provider.name] ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                      </button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}

          {activeTab === 'appearance' && (
            <div className="space-y-4">
              <Card>
                <CardContent className="py-4">
                  <p className="text-sm font-medium text-text-primary mb-3">Theme</p>
                  <div className="flex gap-2">
                    <button className="flex-1 p-3 rounded-lg bg-surface-elevated border-2 border-brand-purple text-center">
                      <div className="w-full h-12 rounded-md bg-canvas border border-border mb-2" />
                      <p className="text-xs font-medium text-text-primary">Dark</p>
                    </button>
                    <button className="flex-1 p-3 rounded-lg bg-surface-elevated border border-border opacity-50 cursor-not-allowed text-center">
                      <div className="w-full h-12 rounded-md bg-gray-100 border border-gray-200 mb-2" />
                      <p className="text-xs font-medium text-text-muted">Light</p>
                    </button>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="py-4">
                  <p className="text-sm font-medium text-text-primary mb-3">Density</p>
                  <div className="flex gap-2">
                    {['compact', 'normal', 'spacious'].map((d) => (
                      <button key={d} onClick={() => setDensity(d)} className={`flex-1 py-2 rounded-lg text-xs font-medium transition-colors border ${density === d ? 'bg-brand-purple/10 text-brand-purple border-brand-purple/30' : 'bg-surface text-text-muted border-border hover:text-text-primary'}`}>{d.charAt(0).toUpperCase() + d.slice(1)}</button>
                    ))}
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="py-4">
                  <p className="text-sm font-medium text-text-primary mb-3">Font Size</p>
                  <div className="flex gap-2">
                    {['small', 'medium', 'large'].map((s) => (
                      <button key={s} onClick={() => setFontSize(s)} className={`flex-1 py-2 rounded-lg text-xs font-medium transition-colors border ${fontSize === s ? 'bg-brand-purple/10 text-brand-purple border-brand-purple/30' : 'bg-surface text-text-muted border-border hover:text-text-primary'}`}>{s.charAt(0).toUpperCase() + s.slice(1)}</button>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          )}

          {activeTab === 'security' && (
            <div className="space-y-4">
              <Card>
                <CardContent className="py-4">
                  <p className="text-sm font-semibold text-text-primary mb-3">Change Password</p>
                  <div className="space-y-3">
                    <input type="password" placeholder="Current password" className="w-full px-3 py-2 bg-canvas border border-border rounded-lg text-sm text-text-primary placeholder:text-text-muted outline-none focus:border-border-strong" />
                    <input type="password" placeholder="New password" className="w-full px-3 py-2 bg-canvas border border-border rounded-lg text-sm text-text-primary placeholder:text-text-muted outline-none focus:border-border-strong" />
                    <input type="password" placeholder="Confirm new password" className="w-full px-3 py-2 bg-canvas border border-border rounded-lg text-sm text-text-primary placeholder:text-text-muted outline-none focus:border-border-strong" />
                  </div>
                  <div className="flex justify-end mt-4"><Button variant="primary">Update Password</Button></div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="py-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-semibold text-text-primary">Two-Factor Authentication</p>
                      <p className="text-xs text-text-muted mt-0.5">Add an extra layer of security to your account</p>
                    </div>
                    <button onClick={() => setTwoFA(!twoFA)} className={`relative w-10 h-5 rounded-full transition-colors ${twoFA ? 'bg-brand-purple' : 'bg-surface-elevated border border-border'}`}>
                      <div className={`absolute top-0.5 w-4 h-4 rounded-full bg-white transition-transform ${twoFA ? 'left-5' : 'left-0.5'}`} />
                    </button>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <div className="px-4 py-3 border-b border-border">
                  <p className="text-sm font-semibold text-text-primary">Active Sessions</p>
                </div>
                <div className="divide-y divide-border">
                  {[
                    { device: 'Chrome on macOS', location: 'New York, US', current: true },
                    { device: 'Safari on iPhone', location: 'New York, US', current: false },
                    { device: 'Firefox on Windows', location: 'London, UK', current: false },
                  ].map((session, idx) => (
                    <div key={idx} className="px-4 py-3 flex items-center justify-between">
                      <div>
                        <p className="text-sm text-text-primary">{session.device} {session.current && <span className="ml-2 px-1.5 py-0.5 rounded bg-status-online/10 text-status-online text-[10px]">Current</span>}</p>
                        <p className="text-xs text-text-muted">{session.location}</p>
                      </div>
                      {!session.current && <Button variant="danger" size="sm"><Trash2 className="w-3 h-3 mr-1" />Revoke</Button>}
                    </div>
                  ))}
                </div>
              </Card>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
