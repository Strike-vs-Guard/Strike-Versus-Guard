#!/usr/bin/env node
/**
 * Checks every internal link and image in the built site (dist/) points at a
 * file that exists. External links are not fetched (they would make CI flaky).
 * Run with: npm run check
 */
import { readFileSync, existsSync, statSync, readdirSync } from 'node:fs';
import { join, extname } from 'node:path';

const dist = new URL('../dist/', import.meta.url).pathname;
const base = (process.env.BASE_PATH || '/Strike-Versus-Guard/').replace(/\/?$/, '/');

function* walk(dir) {
  for (const name of readdirSync(dir)) {
    const p = join(dir, name);
    if (statSync(p).isDirectory()) yield* walk(p);
    else yield p;
  }
}

const problems = [];
let checked = 0;
for (const file of walk(dist)) {
  if (extname(file) !== '.html') continue;
  const html = readFileSync(file, 'utf8');
  const page = file.slice(dist.length - 1);
  for (const m of html.matchAll(/\s(?:href|src|poster|srcset)="([^"]+)"/g)) {
    for (const raw of m[1].split(',').map((s) => s.trim().split(/\s+/)[0])) {
      if (!raw || /^(https?:|mailto:|tel:|data:|#)/.test(raw)) continue;
      checked++;
      if (!raw.startsWith(base)) {
        problems.push(`${page}: "${raw}" does not start with the site base "${base}". Use a relative path.`);
        continue;
      }
      const path = decodeURIComponent(raw.slice(base.length).split(/[?#]/)[0]);
      const target = join(dist, path);
      const ok = existsSync(target) && (statSync(target).isFile() || existsSync(join(target, 'index.html')));
      if (!ok) problems.push(`${page}: broken link "${raw}"`);
    }
  }
}

// Size budget (idea borrowed from CMU's svg-website verify-build): keep pages fast
// and stay well under GitHub's 100 MB file limit.
const root = new URL('../', import.meta.url).pathname;
const budgets = [
  { dir: 'content', max: 5 * 1024 * 1024, what: 'image' },
  { dir: 'public/media', max: 15 * 1024 * 1024, what: 'media file' },
];
for (const { dir, max, what } of budgets) {
  for (const f of walk(join(root, dir))) {
    const size = statSync(f).size;
    if (size > max) {
      problems.push(
        `${f.slice(root.length)}: ${what} is ${(size / 1048576).toFixed(1)} MB (limit ${max / 1048576} MB). Please compress it.`,
      );
    }
  }
}

if (problems.length) {
  console.error(`\n✗ ${problems.length} problem(s):\n`);
  for (const p of [...new Set(problems)]) console.error('  - ' + p);
  console.error('');
  process.exit(1);
}
console.log(`✓ ${checked} internal links and images checked, none broken.`);
