import type { Metadata } from 'next'
import './globals.css'
import Sidebar from '@/components/Sidebar'
import Header from '@/components/Header'

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
        <script dangerouslySetInnerHTML={{ __html: `(function(){try{var m=localStorage.getItem('agentos-theme');if(m==='light'||m==='dark')document.documentElement.dataset.theme=m;}catch(e){}})()` }} />
      </head>
      <body>
        <div className="app-shell">
          <Sidebar />
          <div className="app-column">
            <Header />
            <main className="app-main">
              {children}
            </main>
          </div>
        </div>
      </body>
    </html>
  )
}
