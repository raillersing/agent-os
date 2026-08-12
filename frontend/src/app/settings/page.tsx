'use client'

import { useTheme } from '@/components/ThemeProvider'

const sections = [
  ['appearance', '◐', 'Appearance'],
  ['profile', '◎', 'Profile'],
  ['providers', '◇', 'Providers'],
  ['workspace', '▦', 'Workspace'],
]

export default function SettingsPage() {
  const { theme, followSystem, resolvedTheme, setTheme, toggleFollowSystem } = useTheme()
  const mode = followSystem ? 'system' : theme

  return <div className="page settings-page">
    <div className="settings-heading"><div><p className="eyebrow">Control preferences</p><h1 className="page-title">Settings that stay yours.</h1><p className="page-subtitle">Shape how AgentOS looks and behaves in this workspace.</p></div><span className="settings-state"><i></i>Preferences saved locally</span></div>
    <div className="settings-layout">
      <nav className="settings-nav" aria-label="Settings sections">{sections.map(([id, icon, label]) => <a href={`#${id}`} key={id}><span>{icon}</span>{label}</a>)}</nav>
      <div className="settings-content">
        <section className="settings-panel" id="appearance"><div className="settings-panel-heading"><div><p className="eyebrow">01 · Interface</p><h2>Appearance</h2><p>Choose the visual atmosphere for your control room.</p></div><span className="resolved-theme">{resolvedTheme === 'dark' ? '☾ Dark active' : '☼ Light active'}</span></div><div className="theme-choice-grid"><button className={`theme-choice ${mode === 'system' ? 'active' : ''}`} onClick={() => followSystem || toggleFollowSystem()}><div className="choice-preview system-preview"><span>◐</span></div><div><strong>System</strong><small>Follow your device preference</small></div><span className="choice-radio">{mode === 'system' ? '✓' : ''}</span></button><button className={`theme-choice ${mode === 'dark' ? 'active' : ''}`} onClick={() => setTheme('dark')}><div className="choice-preview dark-preview"><span>☾</span></div><div><strong>Dark</strong><small>Premium night control room</small></div><span className="choice-radio">{mode === 'dark' ? '✓' : ''}</span></button><button className={`theme-choice ${mode === 'light' ? 'active' : ''}`} onClick={() => setTheme('light')}><div className="choice-preview light-preview"><span>☼</span></div><div><strong>Light</strong><small>Warm editorial workspace</small></div><span className="choice-radio">{mode === 'light' ? '✓' : ''}</span></button></div><div className="settings-note"><span>i</span><p>{followSystem ? `AgentOS follows your device. Currently resolved to ${resolvedTheme}.` : `You selected ${theme} mode. This preference is stored in your browser.`}</p></div></section>
        <section className="settings-panel" id="profile"><div className="settings-panel-heading"><div><p className="eyebrow">02 · Identity</p><h2>Profile</h2><p>How your identity appears inside AgentOS.</p></div><span className="preview-badge">Preview only</span></div><div className="settings-form-grid"><label>Display name<input type="text" defaultValue="Eric" placeholder="Your name" /></label><label>Email address<input type="email" defaultValue="eric@acmestudio.com" placeholder="your@email.com" /></label></div><p className="settings-note plain">Profile changes are visual-only in this prototype and are not persisted yet.</p></section>
        <section className="settings-panel" id="providers"><div className="settings-panel-heading"><div><p className="eyebrow">03 · Intelligence</p><h2>Providers</h2><p>Connect model providers used by your agents.</p></div><span className="preview-badge">Preview only</span></div><div className="provider-row"><span className="provider-mark">OR</span><div><strong>OpenRouter</strong><small>Route requests across compatible models</small></div><span className="provider-status">Not connected</span></div><div className="provider-row"><span className="provider-mark anthro">A</span><div><strong>Anthropic</strong><small>Claude models and direct API access</small></div><span className="provider-status">Not connected</span></div><p className="settings-note plain">Provider credentials are not stored by this prototype. Secure provider configuration will be connected to the backend later.</p></section>
        <section className="settings-panel" id="workspace"><div className="settings-panel-heading"><div><p className="eyebrow">04 · Context</p><h2>Workspace</h2><p>The boundary where your missions, agents and evidence live.</p></div><span className="workspace-state"><i></i>Acme Studio</span></div><div className="workspace-summary"><span className="workspace-avatar">AC</span><div><strong>Acme Studio</strong><small>Local workspace · 3 agents connected</small></div><button className="secondary-button">Manage workspace</button></div></section>
      </div>
    </div>
  </div>
}
