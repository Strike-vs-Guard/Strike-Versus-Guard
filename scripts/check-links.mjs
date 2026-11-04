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
  // Ignore inline scripts: they build markup at runtime and contain strings like src="' + x + '".
  const html = readFileSync(file, 'utf8').replace(/<script\b[\s\S]*?<\/script>/g, '');
  const page = file.slice(dist.length - 1);
  for (const m of html.matchAll(/\s(?:href|src|poster|srcset)="([^"]+)"/g)) {
    for (const raw of m[1].split(',').map((s) => s.trim().split(/\s+/)[0])) {
      if (!raw || /^(https?:|mailto:|tel:|data:|#)/.test(raw)) continue;
      checked++;
      // Relative links (e.g. "../../media/clip.mp4" written in a partner's Markdown) are resolved
      // against the page's own address, as a browser would; absolute ones must carry the base.
      const pageUrl = base + page.slice(1).replace(/index\.html$/, '');
      const abs = raw.startsWith('/') ? raw : new URL(raw, 'http://site' + pageUrl).pathname;
      if (!abs.startsWith(base)) {
        problems.push(`${page}: "${raw}" does not start with the site base "${base}". Use a relative path.`);
        continue;
      }
      const path = decodeURIComponent(abs.slice(base.length).split(/[?#]/)[0]);
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
  { dir: 'public/media', max: 8 * 1024 * 1024, what: 'media file', total: 60 * 1024 * 1024 },
];
for (const { dir, max, what, total } of budgets) {
  let sum = 0;
  for (const f of walk(join(root, dir))) {
    const size = statSync(f).size;
    sum += size;
    if (size > max) {
      problems.push(
        `${f.slice(root.length)}: ${what} is ${(size / 1048576).toFixed(1)} MB (limit ${max / 1048576} MB). Please compress it.`,
      );
    }
  }
  if (total && sum > total) {
    problems.push(
      `${dir}/ holds ${(sum / 1048576).toFixed(1)} MB in all (limit ${total / 1048576} MB). Remove clips the site no longer uses, or re-encode the largest ones smaller.`,
    );
  }
}

if (problems.length) {
  console.error(`\n✗ ${problems.length} problem(s):\n`);
  for (const p of [...new Set(problems)]) console.error('  - ' + p);
  console.error('');
  process.exit(1);
}
console.log(`✓ ${checked} internal links and images checked, none broken.`);
