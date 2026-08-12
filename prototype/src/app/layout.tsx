import type { Metadata } from 'next';
import { Inter, JetBrains_Mono } from 'next/font/google';
import '@/styles/globals.css';
import { Sidebar } from '@/components/Sidebar';
import { Header } from '@/components/Header';
import { MobileTabBar } from '@/components/MobileTabBar';

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' });
const jetbrainsMono = JetBrains_Mono({ subsets: ['latin'], variable: '--font-mono' });

export const metadata: Metadata = {
  title: 'Agent OS v2 — Goldie Edition',
  description: 'The intelligent operating system for AI agents',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.variable} ${jetbrainsMono.variable} font-sans antialiased`}>
        <Header />
        <Sidebar />
        <main className="min-h-screen pt-header lg:pl-sidebar pb-14 lg:pb-0">
          {children}
        </main>
        <MobileTabBar />
      </body>
    </html>
  );
}
