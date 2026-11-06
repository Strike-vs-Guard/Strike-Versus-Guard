#!/usr/bin/env node
/**
 * Screenshot one page of the built site (dist/) in a real Chrome, and report what a reviewer needs:
 * horizontal overflow (must be 0), console and page errors (must be none) and failed requests.
 *
 *   npm run check                      # build first
 *   npm run shots -- /                 # home, light, 1280 wide
 *   npm run shots -- /partners/ --theme dark --width 390
 *   npm run shots -- /research/ --out /tmp/shots   # where the PNG goes (default: .shots/, git-ignored)
 *   npm run shots -- / --theme dark --system --width 390   # phone in system dark mode, nothing stored
 * Widths under 800 are emulated as a touch phone (so :hover behaves as on a phone).
 *
 * The page is served from dist/ under the site's base path, so links and assets resolve as on
 * GitHub Pages. Needs Chrome: Google Chrome on PATH, or set SVG_BROWSER=/path/to/chrome.
 * One PNG per call: <out>/<page>-<theme>-<width>.png. Exit code 1 if overflow or errors were found.
 */
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright-core';

const args = process.argv.slice(2);
const opt = (name, dflt) => {
  const i = args.indexOf(`--${name}`);
  return i >= 0 && args[i + 1] ? args[i + 1] : dflt;
};
const page = args.find((a) => a.startsWith('/')) ?? '/';
const theme = opt('theme', 'light');
const width = Number(opt('width', '1280'));
const out = opt('out', '.shots');
/** --system: store nothing, so the page follows the emulated system setting (what a first-time phone visitor gets). */
const system = args.includes('--system');
const base = (process.env.BASE_PATH || '/').replace(/\/?$/, '/');
const dist = new URL('../dist/', import.meta.url).pathname;
if (!fs.existsSync(path.join(dist, 'index.html'))) {
  console.error('dist/ is missing or empty. Run `npm run check` first.');
  process.exit(1);
}

const types = {
  '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.mp4': 'video/mp4',
  '.woff2': 'font/woff2', '.json': 'application/json', '.ico': 'image/x-icon',
};
const srv = http
  .createServer((req, res) => {
    let p = decodeURIComponent(req.url.split('?')[0]);
    if (!p.startsWith(base)) { res.writeHead(404); return res.end('outside base path'); }
    let f = path.join(dist, p.slice(base.length));
    if (fs.existsSync(f) && fs.statSync(f).isDirectory()) f = path.join(f, 'index.html');
    if (!fs.existsSync(f)) { res.writeHead(404); return res.end('not found'); }
    res.writeHead(200, { 'content-type': types[path.extname(f)] ?? 'application/octet-stream' });
    fs.createReadStream(f).pipe(res);
  })
  .listen(0);
const port = srv.address().port;

const launch = process.env.SVG_BROWSER ? { executablePath: process.env.SVG_BROWSER } : { channel: 'chrome' };
const browser = await chromium.launch({ ...launch, args: ['--no-sandbox'] });
const phone = width < 800;
const ctx = await browser.newContext({ viewport: { width, height: 900 }, colorScheme: theme, isMobile: phone, hasTouch: phone });
if (!system) await ctx.addInitScript((t) => localStorage.setItem('theme', t), theme);
const tab = await ctx.newPage();
const errors = [];
const failed = [];
tab.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
tab.on('pageerror', (e) => errors.push(String(e)));
tab.on('response', (r) => r.status() >= 400 && failed.push(`${r.status()} ${r.url()}`));
await tab.goto(`http://localhost:${port}${base}${page.replace(/^\//, '')}`, { waitUntil: 'networkidle' });
// Scroll through once so lazy images load, then back to the top.
await tab.evaluate(async () => {
  for (let y = 0; y < document.body.scrollHeight; y += 600) {
    window.scrollTo(0, y);
    await new Promise((r) => setTimeout(r, 60));
  }
  window.scrollTo(0, 0);
});
await tab.evaluate(async () => {
  const imgs = [...document.images];
  imgs.forEach((i) => (i.loading = 'eager'));
  await Promise.all(imgs.map((i) => (i.complete ? 0 : new Promise((r) => { i.onload = i.onerror = r; }))));
});
await tab.waitForTimeout(400);
const overflow = await tab.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
const height = await tab.evaluate(() => document.documentElement.scrollHeight);
fs.mkdirSync(out, { recursive: true });
const name = page === '/' ? 'home' : page.replace(/^\/|\/$/g, '').replace(/\//g, '-');
const file = path.join(out, `${name}-${theme}${system ? '-system' : ''}-${width}.png`);
await tab.screenshot({ path: file, fullPage: true });
await browser.close();
srv.close();

const ok = overflow === 0 && errors.length === 0 && failed.length === 0;
console.log(JSON.stringify({ page, theme, width, overflow, screens: +(height / 900).toFixed(1), errors, failed, file, ok }, null, 2));
process.exit(ok ? 0 : 1);
