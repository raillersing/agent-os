'use client'

import { FormEvent, useState } from 'react'
import { useRouter } from 'next/navigation'
import api from '@/lib/api'

export default function LoginPage() {
  const router = useRouter()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [saving, setSaving] = useState(false)

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setSaving(true)
    setError('')
    try {
      await api.login(email, password)
      router.replace('/')
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : 'Unable to sign in.')
    } finally {
      setSaving(false)
    }
  }

  return (
    <main className="login-page">
      <div className="login-aura" aria-hidden="true"><span></span><i></i></div>
      <section className="login-card" aria-labelledby="login-title">
        <div className="brand login-brand"><div className="brand-mark"><span>✦</span><i></i></div><div><strong>AgentOS</strong><small>Mission control</small></div></div>
        <p className="eyebrow">Private control plane</p>
        <h1 id="login-title">Welcome back.</h1>
        <p className="login-copy">Sign in to access your workspaces, missions and evidence.</p>
        <form onSubmit={submit}>
          <label>Email<input type="email" value={email} onChange={(event) => setEmail(event.target.value)} autoComplete="username" required /></label>
          <label>Password<input type="password" value={password} onChange={(event) => setPassword(event.target.value)} autoComplete="current-password" required /></label>
          {error && <p className="form-error" role="alert">{error}</p>}
          <button className="primary-button login-submit" type="submit" disabled={saving}>{saving ? 'Signing in…' : 'Enter control room'} <span>↗</span></button>
        </form>
        <p className="login-footnote">Credentials are supplied by the AgentOS server administrator.</p>
      </section>
    </main>
  )
}
