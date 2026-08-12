'use client'

import { createContext, useContext, useEffect, useState, useCallback } from 'react'

export type ThemeMode = 'dark' | 'light'

interface ThemeContextValue {
  theme: ThemeMode
  followSystem: boolean
  resolvedTheme: ThemeMode
  setTheme: (mode: ThemeMode) => void
  toggleFollowSystem: () => void
}

const ThemeContext = createContext<ThemeContextValue | null>(null)

const STORAGE_KEY_THEME = 'agentos-theme'
const STORAGE_KEY_FOLLOW = 'agentos-follow-system'

function getSystemTheme(): ThemeMode {
  if (typeof window === 'undefined') return 'dark'
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

function getStoredTheme(): ThemeMode {
  if (typeof window === 'undefined') return 'dark'
  try {
    const raw = localStorage.getItem(STORAGE_KEY_THEME)
    if (raw === 'light') return 'light'
  } catch {}
  return 'dark'
}

function getStoredFollow(): boolean {
  if (typeof window === 'undefined') return false
  try {
    return localStorage.getItem(STORAGE_KEY_FOLLOW) !== 'false'
  } catch {}
  return true // default: follow system
}

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setThemeState] = useState<ThemeMode>('dark')
  const [followSystem, setFollowSystem] = useState(true)
  const [systemTheme, setSystemTheme] = useState<ThemeMode>('dark')
  const [mounted, setMounted] = useState(false)

  // Initialize from localStorage on mount
  useEffect(() => {
    const storedTheme = getStoredTheme()
    const storedFollow = getStoredFollow()
    setSystemTheme(getSystemTheme())
    setThemeState(storedTheme)
    setFollowSystem(storedFollow)
    setMounted(true)
  }, [])

  // Resolve effective theme
  const resolvedTheme: ThemeMode = followSystem ? systemTheme : theme

  // Apply theme to document
  useEffect(() => {
    if (!mounted) return
    try {
      document.documentElement.dataset.theme = resolvedTheme
      // Update meta color-scheme
      const meta = document.querySelector('meta[name="color-scheme"]')
      if (meta) meta.setAttribute('content', resolvedTheme)
    } catch {}
  }, [resolvedTheme, mounted])

  // Listen to OS theme changes (when followSystem is true)
  useEffect(() => {
    if (!mounted || !followSystem) return
    const mq = window.matchMedia('(prefers-color-scheme: dark)')
    const handler = (e: MediaQueryListEvent) => {
      setSystemTheme(e.matches ? 'dark' : 'light')
    }
    mq.addEventListener('change', handler)
    return () => mq.removeEventListener('change', handler)
  }, [followSystem, mounted])

  // Cross-tab sync
  useEffect(() => {
    if (!mounted) return
    const handler = (e: StorageEvent) => {
      if (e.key === STORAGE_KEY_THEME && e.newValue) {
        setThemeState(e.newValue as ThemeMode)
      }
      if (e.key === STORAGE_KEY_FOLLOW) {
        setFollowSystem(e.newValue !== 'false')
      }
    }
    window.addEventListener('storage', handler)
    return () => window.removeEventListener('storage', handler)
  }, [mounted])

  const setTheme = useCallback((mode: ThemeMode) => {
    setThemeState(mode)
    setFollowSystem(false)
    try {
      localStorage.setItem(STORAGE_KEY_THEME, mode)
      localStorage.setItem(STORAGE_KEY_FOLLOW, 'false')
    } catch {}
  }, [])

  const toggleFollowSystem = useCallback(() => {
    const next = !followSystem
    setFollowSystem(next)
    try {
      localStorage.setItem(STORAGE_KEY_FOLLOW, next ? 'true' : 'false')
      if (next) {
        // When enabling follow system, also store current system theme as baseline
        localStorage.setItem(STORAGE_KEY_THEME, getSystemTheme())
      }
    } catch {}
  }, [followSystem])

  return (
    <ThemeContext.Provider value={{ theme, followSystem, resolvedTheme, setTheme, toggleFollowSystem }}>
      {children}
    </ThemeContext.Provider>
  )
}

export function useTheme(): ThemeContextValue {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider')
  }
  return context
}
