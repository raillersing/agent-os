import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Agent OS — Mission Control',
  description: 'Vendor-neutral orchestration, governance, and observability for AI agents',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
