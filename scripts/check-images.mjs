#!/usr/bin/env node
/**
 * Every PNG or WebP under content/ must be opaque (STANDARDS §3, "Phones").
 *
 * Why: Samsung Internet (and other phone browsers that force a dark mode) repaint CSS colours but
 * leave image pixels alone. A logo or figure with a see-through background then sits dark-on-dark
 * and disappears. A white background inside the file cannot be repainted.
 *
 * Fix for a failing file: flatten it onto white, e.g.
 *   node -e "import('sharp').then(s=>s.default('in.png').flatten({background:'#fff'}).removeAlpha().png().toFile('out.png'))"
 */
import { readdirSync } from 'node:fs';
import { join, extname } from 'node:path';
import sharp from 'sharp';

const ROOT = 'content';
const LIMIT = 0.005; // share of pixels that may be see-through (anti-aliased corners)

const files = readdirSync(ROOT, { recursive: true })
  .map((f) => join(ROOT, String(f)))
  .filter((f) => ['.png', '.webp'].includes(extname(f).toLowerCase()));

const bad = [];
for (const f of files) {
  const img = sharp(f);
  const meta = await img.metadata();
  if (!meta.hasAlpha) continue;
  const { data, info } = await img.ensureAlpha().raw().toBuffer({ resolveWithObject: true });
  let clear = 0;
  for (let i = 3; i < data.length; i += 4) if (data[i] < 250) clear++;
  const share = clear / (info.width * info.height);
  if (share > LIMIT) bad.push(`${f}: ${(share * 100).toFixed(1)} % of pixels are see-through`);
}

if (bad.length) {
  console.error('✗ Images with a see-through background (they vanish on phones that force dark mode):');
  for (const b of bad) console.error('  ' + b);
  console.error('  Give each file a white background (see the top of scripts/check-images.mjs).');
  process.exit(1);
}
console.log(`✓ ${files.length} content images checked, none see-through.`);
