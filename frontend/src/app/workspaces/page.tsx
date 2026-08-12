'use client'

import { useEffect, useState } from 'react'
import api from '@/lib/api'

type Workspace = { id: string; name: string; description: string; status: string; budget: number }

export default function Workspaces() {
  const [workspaces, setWorkspaces] = useState<Workspace[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    api.listWorkspaces().then(setWorkspaces).catch((cause) => setError(cause.message)).finally(() => setLoading(false))
  }, [])

  const createWorkspace = async () => {
    const workspace = await api.createWorkspace({ name: `Workspace ${workspaces.length + 1}`, description: 'A persistent AgentOS workspace' })
    setWorkspaces((current) => [...current, workspace])
  }

  return (
    <div className="page">
      <div className="page-heading"><div><p className="eyebrow">Workspaces</p><h1 className="page-title">Context that stays together.</h1><p className="page-subtitle">Each workspace keeps its people, agents, knowledge, permissions, missions, and costs safely separated.</p></div><button className="primary-button" onClick={createWorkspace}>＋ New workspace</button></div>
      {loading && <div className="empty-message">Loading persisted workspaces…</div>}
      {error && <p className="form-error" role="alert">Workspaces unavailable: {error}</p>}
      {!loading && !error && !workspaces.length && <div className="empty-message">No workspace yet. Create one to establish a safe context boundary.</div>}
      <section className="section collection-grid">
        {workspaces.map((workspace) => <article className="card collection-card" key={workspace.id}>
          <span className="collection-icon">{workspace.name.charAt(0).toUpperCase()}</span><h2>{workspace.name}</h2><p>{workspace.description || 'No description yet.'}</p>
          <div className="collection-footer"><span>{workspace.status}</span><span>Budget ${workspace.budget.toFixed(0)}</span></div>
        </article>)}
      </section>
    </div>
  )
}
