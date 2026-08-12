'use client'

import { useEffect, useState } from 'react'
import api from '@/lib/api'

type Agent = { id: string; name: string; description?: string; model: string; status: string; capabilities: string[] }
const initials = (name: string) => name.split(/\s+/).map((part) => part[0]).join('').slice(0, 2).toUpperCase()

export default function Agents() {
  const [agents, setAgents] = useState<Agent[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const refresh = () => api.listAgents().then(setAgents).catch((cause) => setError(cause.message)).finally(() => setLoading(false))
  useEffect(() => { refresh() }, [])
  const create = async () => { try { const agent = await api.createAgent({ name: `Agent ${agents.length + 1}`, model: 'provider-neutral/default', description: 'A bounded AgentOS operator', capabilities: ['workspace-read'] }); setAgents((current) => [...current, agent]); setError('') } catch (cause) { setError(cause instanceof Error ? cause.message : 'Agent could not be saved.') } }
  return <div className="page"><div className="page-heading"><div><p className="eyebrow">Agent registry</p><h1 className="page-title">A team you can understand.</h1><p className="page-subtitle">Every agent has a stored responsibility, replaceable model, declared capability set, and visible operating state.</p></div><button className="primary-button" onClick={create}>＋ Create agent</button></div>{error && <p className="form-error" role="alert">{error}</p>}{loading && <div className="empty-message">Loading persisted agents…</div>}{!loading && !error && !agents.length && <div className="empty-message">No agent has been registered yet. Create an agent before assigning work.</div>}<section className="section collection-grid">{agents.map((agent) => <article className="card collection-card agent-card" key={agent.id}><div className="card-top"><span className="collection-icon">{initials(agent.name)}</span><span className={`status ${agent.status === 'active' ? 'running' : 'complete'}`}>{agent.status}</span></div><h2>{agent.name}</h2><p>{agent.description || 'No responsibility description provided.'}</p><div className="collection-footer"><span>{agent.model}</span><span>{agent.capabilities.length} capabilities</span></div></article>)}</section></div>
}
