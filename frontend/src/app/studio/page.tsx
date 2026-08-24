'use client'

import { useEffect, useMemo, useState } from 'react'
import api from '@/lib/api'

type Artifact = { id: string; media_type: string; content: string; created_at: string }

const mediaLabels: Record<string, string> = {
  image: 'image',
  video: 'video',
  voice: 'voice',
  audio: 'audio',
  document: 'document',
}

export default function StudioPage() {
  const [artifacts, setArtifacts] = useState<Artifact[]>([])
  const [workspaceId, setWorkspaceId] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [category, setCategory] = useState('all')

  useEffect(() => {
    async function bootstrap() {
      try {
        const workspaces = await api.listWorkspaces()
        if (!workspaces.length) {
          setLoading(false)
          return
        }
        const firstId = workspaces[0].id
        setWorkspaceId(firstId)
        const data = await api.listArtifacts(firstId)
        setArtifacts(data)
      } catch (cause) {
        setError(cause instanceof Error ? cause.message : 'Artifacts unavailable')
      } finally {
        setLoading(false)
      }
    }
    bootstrap()
  }, [])

  const categories = useMemo(() => ['all', ...Array.from(new Set(artifacts.map((item) => mediaLabels[item.media_type] || item.media_type)))], [artifacts])
  const filtered = useMemo(() => category === 'all' ? artifacts : artifacts.filter((item) => (mediaLabels[item.media_type] || item.media_type) === category), [category, artifacts])

  return <div className="page legacy-page">
    <div className="legacy-header"><div><p className="eyebrow">Artifact workspace</p><h1 className="page-title">A studio for finished work.</h1><p className="page-subtitle">Collect the outputs that matter, inspect their provenance, and keep delivery separate from execution.</p></div><span className="live-badge"><i></i>Persisted API</span></div>
    <section className="studio-hero"><div><p className="eyebrow">Create an artifact</p><h2>Turn a run into something ready to share.</h2><p>Artifacts are produced by execution runs and surfaced from the control plane.</p></div><button className="primary-button" onClick={() => setCategory('all')}>＋ Explore library</button></section>
    {error && <p className="form-error" role="alert">{error}</p>}
    {loading && <div className="empty-message">Loading persisted artifacts…</div>}
    {!loading && !error && !artifacts.length && <div className="empty-message">No artifact yet. Run a D1 execution to produce one.</div>}
    {!loading && !error && artifacts.length > 0 && <>
      <div className="filter-row">{categories.map((item) => <button key={item} className={category === item ? 'filter-active' : ''} onClick={() => setCategory(item)}>{item}</button>)}<span className="filter-result">{filtered.length} artifacts</span></div>
      <section className="artifact-grid">{filtered.map((item) => <article className="artifact-card" key={item.id}>
        <div className={`artifact-preview ${mediaLabels[item.media_type] || 'unknown'}`}><span>{(item.media_type[0] || '◈').toUpperCase()}</span><small>{mediaLabels[item.media_type] || item.media_type}</small></div>
        <div className="artifact-copy"><div><h2>{item.content.slice(0, 60) || 'Untitled artifact'}</h2><p>id {item.id.slice(0, 8)}</p></div><span className="artifact-arrow">↗</span></div>
        <div className="artifact-foot"><span>{item.media_type}</span><span>{new Date(item.created_at).toLocaleString()}</span></div>
      </article>)}</section>
    </>}
  </div>
}
