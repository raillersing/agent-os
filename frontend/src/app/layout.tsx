import type { Metadata } from 'next'
import './globals.css'
import AppShell from '@/components/AppShell'
import { ThemeProvider } from '@/components/ThemeProvider'

export const metadata: Metadata = {
  title: 'AgentOS — Turn intent into outcomes',
  description: 'A calm control plane for AI agents, missions, and automations',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <meta name="color-scheme" content="dark light" />
        <script dangerouslySetInnerHTML={{ __html: `(function(){try{var f=localStorage.getItem('agentos-follow-system');var t=localStorage.getItem('agentos-theme');var system=window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';var theme=f==='false'&&(t==='light'||t==='dark')?t:system;document.documentElement.dataset.theme=theme;document.querySelector('meta[name="color-scheme"]')?.setAttribute('content',theme);}catch(e){}})()` }} />
      </head>
      <body>
        <ThemeProvider>
          <AppShell>{children}</AppShell>
        </ThemeProvider>
      </body>
    </html>
  )
}
