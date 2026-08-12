export interface Agent {
  id: string;
  name: string;
  role: string;
  model: string;
  status: 'online' | 'ready' | 'offline' | 'running';
  color: string;
  lastActivity: string;
  skills: string[];
  description: string;
  tasksCompleted: number;
  uptime: string;
}

export interface Task {
  id: string;
  title: string;
  agent: string;
  agentId: string;
  status: 'backlog' | 'ready' | 'in-progress' | 'blocked' | 'done';
  priority: 'urgent' | 'high' | 'medium' | 'low';
  dueDate: string;
  tags: string[];
  description?: string;
  subtasks?: { text: string; done: boolean }[];
  comments?: { author: string; text: string; time: string }[];
}

export interface ChatSession {
  id: string;
  title: string;
  lastMessage: string;
  timestamp: string;
  model: string;
  agentId: string;
  pinned?: boolean;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'agent';
  content: string;
  agentId?: string;
  timestamp: string;
  toolCalls?: { name: string; status: string }[];
  codeBlocks?: { language: string; code: string }[];
}

export interface Note {
  id: string;
  title: string;
  content: string;
  folder: string;
  updatedAt: string;
}

export interface Artifact {
  id: string;
  title: string;
  type: 'image' | 'video' | 'audio' | 'document';
  size: string;
  agent: string;
  agentId: string;
  agentColor: string;
  date: string;
  createdAt: string;
  thumbnail?: string;
  url?: string;
  duration?: string;
}

export interface MediaJob {
  id: string;
  prompt?: string;
  status: 'queued' | 'running' | 'completed' | 'failed';
  progress: number;
  model: string;
  createdAt: string;
  type: 'image' | 'video' | 'speech';
  duration?: string;
  text?: string;
  voice?: string;
}

export const agents: Agent[] = [
  { id: 'claude', name: 'Claude', role: 'Senior Copywriter', model: 'claude-3-7-sonnet', status: 'online', color: '#F97316', lastActivity: '2 min ago', skills: ['Copywriting', 'SEO', 'Content Strategy', 'Technical Writing'], description: 'Expert in persuasive copywriting, SEO optimization, and content strategy.', tasksCompleted: 1247, uptime: '99.9%' },
  { id: 'kimi', name: 'Kimi', role: 'SEO Analyst', model: 'kimi-1.5-pro', status: 'running', color: '#22D3EE', lastActivity: 'Running now', skills: ['Keyword Research', 'SERP Analysis', 'Backlink Audit', 'Rank Tracking'], description: 'Data-driven SEO analyst with deep expertise in keyword research and SERP analysis.', tasksCompleted: 892, uptime: '99.7%' },
  { id: 'grok', name: 'Grok', role: 'Trend Analyst', model: 'grok-3', status: 'ready', color: '#EF4444', lastActivity: '15 min ago', skills: ['Trend Detection', 'Social Listening', 'Viral Content', 'News Analysis'], description: 'Real-time trend analyst monitoring social media, news, and viral content.', tasksCompleted: 634, uptime: '98.5%' },
  { id: 'hermes', name: 'Hermes', role: 'Messenger Bot', model: 'llama-3-hermes', status: 'online', color: '#3B82F6', lastActivity: 'Just now', skills: ['Email Drafting', 'DM Outreach', 'PR Pitching', 'Influencer Outreach'], description: 'Communication specialist for email sequences, direct messages, and PR outreach.', tasksCompleted: 2103, uptime: '99.8%' },
  { id: 'openclaw', name: 'OpenClaw', role: 'Automation Engineer', model: 'openclaw-v2', status: 'offline', color: '#EC4899', lastActivity: '2 hours ago', skills: ['Workflow Automation', 'API Integration', 'Scraping', 'Data Pipeline'], description: 'Automation engineer building custom workflows, API integrations, and data pipelines.', tasksCompleted: 1567, uptime: '97.2%' },
  { id: 'gemini', name: 'Gemini', role: 'Multimodal Analyst', model: 'gemini-2.5-pro', status: 'ready', color: '#10B981', lastActivity: '45 min ago', skills: ['Image Analysis', 'Video Summary', 'Vision QA', 'Data Extraction'], description: 'Multimodal analyst processing images, videos, and documents.', tasksCompleted: 445, uptime: '99.1%' },
  { id: 'antigravity', name: 'Antigravity', role: 'Research Lead', model: 'antigravity-research', status: 'online', color: '#8B5CF6', lastActivity: '5 min ago', skills: ['Deep Research', 'Fact Checking', 'Citation Analysis', 'Academic Writing'], description: 'Research lead conducting deep investigations and fact checking.', tasksCompleted: 721, uptime: '99.6%' },
  { id: 'codex', name: 'Codex', role: 'Code Assistant', model: 'codex-1', status: 'offline', color: '#6B7280', lastActivity: '1 hour ago', skills: ['Code Review', 'Debugging', 'Refactoring', 'API Design'], description: 'Code assistant for review, debugging, refactoring, and API design.', tasksCompleted: 1834, uptime: '96.8%' },
];

export const tasks: Task[] = [
  { id: 't1', title: 'Write SEO-optimized landing page for SaaS product', agent: 'Claude', agentId: 'claude', status: 'in-progress', priority: 'urgent', dueDate: 'Today', tags: ['copywriting', 'seo', 'landing-page'], description: 'Create a high-converting landing page with keyword integration.', subtasks: [{ text: 'Research competitor landing pages', done: true }, { text: 'Draft headline variants', done: true }, { text: 'Write body copy', done: false }, { text: 'Add social proof section', done: false }], comments: [{ author: 'User', text: 'Make sure to include the pricing table CTA', time: '2h ago' }] },
  { id: 't2', title: 'Audit backlink profile for domain.com', agent: 'Kimi', agentId: 'kimi', status: 'running', priority: 'high', dueDate: 'Tomorrow', tags: ['seo', 'backlinks', 'audit'], description: 'Full backlink audit with toxicity analysis.', subtasks: [{ text: 'Export backlink data', done: true }, { text: 'Run toxicity scoring', done: true }, { text: 'Generate disavow file', done: false }] },
  { id: 't3', title: 'Analyze trending topics for content calendar', agent: 'Grok', agentId: 'grok', status: 'ready', priority: 'medium', dueDate: 'Aug 14', tags: ['trends', 'content-calendar', 'social'] },
  { id: 't4', title: 'Draft PR pitch for product launch', agent: 'Hermes', agentId: 'hermes', status: 'backlog', priority: 'high', dueDate: 'Aug 15', tags: ['pr', 'outreach', 'launch'] },
  { id: 't5', title: 'Fix broken automation for daily report', agent: 'OpenClaw', agentId: 'openclaw', status: 'blocked', priority: 'urgent', dueDate: 'Today', tags: ['automation', 'bug', 'reporting'], description: 'The daily analytics report automation has been failing since the API update.' },
  { id: 't6', title: 'Summarize latest industry whitepapers', agent: 'Gemini', agentId: 'gemini', status: 'in-progress', priority: 'medium', dueDate: 'Aug 16', tags: ['research', 'summary', 'whitepaper'] },
  { id: 't7', title: 'Deep-dive competitive analysis on 3 competitors', agent: 'Antigravity', agentId: 'antigravity', status: 'backlog', priority: 'high', dueDate: 'Aug 18', tags: ['research', 'competitive-analysis'] },
  { id: 't8', title: 'Refactor legacy scraping scripts', agent: 'Codex', agentId: 'codex', status: 'done', priority: 'low', dueDate: 'Aug 10', tags: ['code', 'refactor', 'scraping'] },
  { id: 't9', title: 'Generate hero images for new blog series', agent: 'Gemini', agentId: 'gemini', status: 'in-progress', priority: 'medium', dueDate: 'Aug 14', tags: ['image', 'design', 'blog'] },
  { id: 't10', title: 'Weekly newsletter draft', agent: 'Claude', agentId: 'claude', status: 'backlog', priority: 'medium', dueDate: 'Aug 13', tags: ['newsletter', 'email', 'copywriting'] },
];

export const chatSessions: ChatSession[] = [
  { id: 's1', title: 'SEO Strategy Brainstorm', lastMessage: 'Here is the keyword gap analysis...', timestamp: '2m ago', model: 'Claude', agentId: 'claude', pinned: true },
  { id: 's2', title: 'Landing Page Copy Review', lastMessage: 'The CTA could be stronger.', timestamp: '15m ago', model: 'Claude', agentId: 'claude', pinned: true },
  { id: 's3', title: 'Backlink Audit Questions', lastMessage: 'Found 47 toxic links from PBN networks.', timestamp: '1h ago', model: 'Kimi', agentId: 'kimi' },
  { id: 's4', title: 'Trend Analysis - Q3', lastMessage: 'AI-generated content detection is trending.', timestamp: '3h ago', model: 'Grok', agentId: 'grok' },
  { id: 's5', title: 'PR Outreach Templates', lastMessage: 'Here are 3 personalized pitch templates.', timestamp: 'Yesterday', model: 'Hermes', agentId: 'hermes' },
  { id: 's6', title: 'Automation Debugging', lastMessage: 'The webhook endpoint is returning 403.', timestamp: 'Yesterday', model: 'OpenClaw', agentId: 'openclaw' },
];

export const chatMessages: Record<string, ChatMessage[]> = {
  s1: [
    { id: 'm1', role: 'user', content: 'Can you analyze our top 3 competitors and find keyword gaps?', timestamp: '2:34 PM' },
    { id: 'm2', role: 'agent', content: "I'll analyze the keyword gaps for your top competitors. This might take a moment.", agentId: 'claude', timestamp: '2:34 PM', toolCalls: [{ name: 'CompetitorAnalysis', status: 'Running...' }] },
    { id: 'm3', role: 'agent', content: 'Here is the keyword gap analysis for the top 3 competitors. I found 127 high-opportunity keywords.', agentId: 'claude', timestamp: '2:36 PM' },
  ],
  s2: [
    { id: 'm1', role: 'user', content: 'Review this landing page copy and suggest improvements.', timestamp: '1:12 PM' },
    { id: 'm2', role: 'agent', content: 'The CTA could be stronger. Try "Start Your Free Trial" instead.', agentId: 'claude', timestamp: '1:13 PM' },
  ],
  s3: [
    { id: 'm1', role: 'user', content: 'What did the backlink audit reveal?', timestamp: '11:00 AM' },
    { id: 'm2', role: 'agent', content: 'Found 47 toxic links from PBN networks. Recommend disavow.', agentId: 'kimi', timestamp: '11:02 AM' },
  ],
  s4: [
    { id: 'm1', role: 'user', content: 'What are the trending topics for Q3?', timestamp: '9:30 AM' },
    { id: 'm2', role: 'agent', content: 'AI-generated content detection is the fastest-growing topic this week.', agentId: 'grok', timestamp: '9:31 AM' },
  ],
  s5: [
    { id: 'm1', role: 'user', content: 'Draft some PR outreach templates for our product launch.', timestamp: 'Yesterday' },
    { id: 'm2', role: 'agent', content: 'Here are 3 personalized pitch templates for tech journalists.', agentId: 'hermes', timestamp: 'Yesterday' },
  ],
  s6: [
    { id: 'm1', role: 'user', content: 'Why is the daily report automation failing?', timestamp: 'Yesterday' },
    { id: 'm2', role: 'agent', content: 'The webhook endpoint is returning 403. Check the API key.', agentId: 'openclaw', timestamp: 'Yesterday' },
  ],
};

export const notes: Note[] = [
  { id: 'n1', title: 'SEO Audit Process', content: '# SEO Audit Process\n\n## 1. Technical Audit\n- Crawl the site using Screaming Frog\n- Check for broken links and 404s\n- Review robots.txt and sitemap.xml\n\n## 2. On-Page Analysis\n- Title tag optimization\n- Meta description review\n\n## 3. Off-Page Analysis\n- Backlink profile review\n- Anchor text distribution\n\n[[Keyword Research Guide]]\n[[Competitor Analysis Framework]]', folder: 'SOPs', updatedAt: '2 days ago' },
  { id: 'n2', title: 'Content Pipeline SOP', content: '# Content Pipeline SOP\n\n## Stages\n1. **Ideation** — Keyword research + trend analysis\n2. **Brief Creation** — Outline, keywords, angle\n3. **Drafting** — Assigned to Claude or Kimi\n4. **Review** — Human editor check\n5. **Publish** — CMS upload + scheduling\n6. **Distribution** — Social, newsletter, PR\n\n## Agents Involved\n- **Kimi**: Keyword research\n- **Claude**: Drafting\n- **Hermes**: Distribution', folder: 'SOPs', updatedAt: '1 week ago' },
  { id: 'n3', title: 'Daily X Digest Template', content: '# Daily X Digest Template\n\n## Format\n- **Hook**: Bold statement or question\n- **Insight**: 2-3 key takeaways\n- **CTA**: Engagement prompt\n\n## Sources\n- Google Trends\n- Reddit (r/SEO, r/Marketing)\n- Industry newsletters\n\n## Schedule\nPosted daily at 8:00 AM EST.', folder: 'Templates', updatedAt: '3 days ago' },
  { id: 'n4', title: 'Keyword Research Guide', content: '# Keyword Research Guide\n\n## Tools\n- Ahrefs\n- SEMrush\n- Google Keyword Planner\n- Kimi (AI-assisted)\n\n## Metrics to Track\n- Search Volume\n- Keyword Difficulty\n- CPC\n- SERP Features\n\n## Process\n1. Seed keyword expansion\n2. Competitor keyword gap\n3. Intent classification\n4. Priority scoring\n\nSee also: [[SEO Audit Process]]', folder: 'Guides', updatedAt: '5 days ago' },
  { id: 'n5', title: 'Competitor Analysis Framework', content: '# Competitor Analysis Framework\n\n## Dimensions\n- **Content**: What topics do they cover?\n- **SEO**: What keywords do they rank for?\n- **Backlinks**: Who links to them?\n- **Social**: Engagement rates\n\n## Output\nA [[SEO Audit Process]] scorecard with action items.', folder: 'Frameworks', updatedAt: '1 week ago' },
];

export const artifacts: Artifact[] = [
  { id: 'a1', title: 'Hero Banner - Analytics Dashboard', type: 'image', size: '2.4 MB', agent: 'Gemini', agentId: 'gemini', agentColor: '#10B981', date: 'Aug 11, 2026', createdAt: 'Aug 11, 2026', thumbnail: 'bg-gradient-to-br from-brand-purple to-brand-pink' },
  { id: 'a2', title: 'Product Demo - Feature Walkthrough', type: 'video', size: '45 MB', agent: 'Gemini', agentId: 'gemini', agentColor: '#10B981', date: 'Aug 10, 2026', createdAt: 'Aug 10, 2026', duration: '2:34' },
  { id: 'a3', title: 'Podcast Intro Voiceover', type: 'audio', size: '3.2 MB', agent: 'Hermes', agentId: 'hermes', agentColor: '#3B82F6', date: 'Aug 9, 2026', createdAt: 'Aug 9, 2026', duration: '0:15' },
  { id: 'a4', title: 'Q3 Content Strategy Brief', type: 'document', size: '124 KB', agent: 'Claude', agentId: 'claude', agentColor: '#F97316', date: 'Aug 8, 2026', createdAt: 'Aug 8, 2026' },
  { id: 'a5', title: 'Social Media Templates Set', type: 'image', size: '8.1 MB', agent: 'Gemini', agentId: 'gemini', agentColor: '#10B981', date: 'Aug 7, 2026', createdAt: 'Aug 7, 2026' },
  { id: 'a6', title: 'Webinar Recording - SEO 2026', type: 'video', size: '120 MB', agent: 'Gemini', agentId: 'gemini', agentColor: '#10B981', date: 'Aug 6, 2026', createdAt: 'Aug 6, 2026', duration: '45:20' },
  { id: 'a7', title: 'Outreach Script - Cold Email', type: 'document', size: '18 KB', agent: 'Hermes', agentId: 'hermes', agentColor: '#3B82F6', date: 'Aug 5, 2026', createdAt: 'Aug 5, 2026' },
  { id: 'a8', title: 'Voice Memo - Meeting Notes', type: 'audio', size: '1.8 MB', agent: 'Hermes', agentId: 'hermes', agentColor: '#3B82F6', date: 'Aug 4, 2026', createdAt: 'Aug 4, 2026', duration: '5:42' },
];

export const mediaJobs: MediaJob[] = [
  { id: 'mj1', prompt: 'A futuristic dashboard interface with neon blue accents, dark background, holographic charts', status: 'completed', progress: 100, model: 'dall-e-3', createdAt: 'Aug 11, 2026', type: 'image' },
  { id: 'mj2', prompt: 'A team of AI agents collaborating in a digital workspace, vibrant colors, high detail', status: 'running', progress: 67, model: 'dall-e-3', createdAt: 'Aug 11, 2026', type: 'image' },
  { id: 'mj3', prompt: 'Product showcase with floating UI elements, purple and pink gradient', status: 'queued', progress: 0, model: 'midjourney-v6', createdAt: 'Aug 11, 2026', type: 'image' },
  { id: 'mj4', status: 'completed', progress: 100, model: 'sora-v1', createdAt: 'Aug 10, 2026', type: 'video', duration: '0:30' },
  { id: 'mj5', status: 'running', progress: 34, model: 'sora-v1', createdAt: 'Aug 11, 2026', type: 'video', duration: '1:00' },
  { id: 'mj6', status: 'queued', progress: 0, model: 'runway-ml', createdAt: 'Aug 11, 2026', type: 'video', duration: '0:15' },
  { id: 'mj7', text: 'Welcome to Agent OS. Your AI workforce is ready to execute.', voice: 'Nova', status: 'completed', progress: 100, model: 'elevenlabs-v3', createdAt: 'Aug 9, 2026', type: 'speech', duration: '0:08' },
  { id: 'mj8', text: 'The future of content creation is autonomous, intelligent, and always on.', voice: 'Onyx', status: 'running', progress: 78, model: 'elevenlabs-v3', createdAt: 'Aug 11, 2026', type: 'speech', duration: '0:12' },
];
