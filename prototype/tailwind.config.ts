import type { Config } from 'tailwindcss'

const config: Config = {
  content: ['./src/**/*.{js,ts,jsx,tsx,mdx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        canvas: '#0A0A0B',
        surface: '#17171A',
        'surface-elevated': '#1E1E23',
        'surface-hover': '#252530',
        border: '#2A2A35',
        'border-strong': '#3A3A48',
        'text-primary': '#E8E8ED',
        'text-secondary': '#8A8A95',
        'text-muted': '#5A5A68',
        // Agent colors
        'claude': '#F97316',
        'kimi': '#22D3EE',
        'grok': '#EF4444',
        'hermes': '#3B82F6',
        'openclaw': '#EC4899',
        'gemini': '#10B981',
        'antigravity': '#8B5CF6',
        'codex': '#6B7280',
        // Status
        'status-online': '#22C55E',
        'status-ready': '#EAB308',
        'status-offline': '#EF4444',
        'status-running': '#3B82F6',
        // Brand
        'brand-purple': '#A855F7',
        'brand-pink': '#EC4899',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      spacing: {
        'sidebar': '248px',
        'header': '56px',
      },
    },
  },
  plugins: [],
}
export default config
