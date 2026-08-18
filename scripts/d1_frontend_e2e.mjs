import { chromium } from 'playwright';

const frontendUrl = process.env.D1_FRONTEND_URL || 'http://127.0.0.1:13080';
const workspaceId = process.env.D1_WORKSPACE_ID;
const token = process.env.D1_API_TOKEN;

if (!workspaceId || !token) {
  throw new Error('D1_WORKSPACE_ID and D1_API_TOKEN are required');
}

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();
await page.addInitScript((accessToken) => {
  window.localStorage.setItem('agentos-access-token', accessToken);
}, token);
await page.goto(`${frontendUrl}/execution-runs`, { waitUntil: 'networkidle' });
await page.getByLabel('Workspace ID').fill(workspaceId);

await page.getByText('Tasks', { exact: true }).waitFor();
await page.getByText('D1 task', { exact: true }).waitFor();
await page.getByRole('heading', { name: 'Runs', exact: true }).waitFor();
await page.locator('article strong').filter({ hasText: 'completed' }).waitFor();
await page.getByText('SIMULATOR', { exact: true }).waitFor();
await page.getByText(/receipt /).waitFor();
await page.getByText(/artifact /).waitFor();
await page.getByRole('button', { name: 'Inspect AI evidence' }).click();
await page.getByText(/Disclosure: local_simulator/).waitFor();

console.log('D1/D2 frontend E2E PASS: simulator disclosure, task, completed run, receipt, artifact and evidence visible');
await browser.close();
