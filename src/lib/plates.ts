/**
 * Draws the logo plates (geometry in src/lib/logo.ts): each logo composited onto an opaque white
 * canvas with sharp (Astro's own image service, so no extra dependency). Used only by the endpoint
 * src/pages/plates/[name].png.ts, which serves them in `astro dev` and writes them to dist/plates/ in
 * `astro build`. Nothing generated is committed.
 */
import { existsSync, readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import type { ImageMetadata } from 'astro';
import { getCollection, type CollectionEntry } from 'astro:content';
import sharp from 'sharp';
import { pairLayout, singleLayout, type Layout } from './logo';

type Partner = CollectionEntry<'partners'>;
type Key = 'logo' | 'logoMark' | 'labLogo';
/** A plate: its name, the source file for each logo (in the order of `at.spots`) and the layout. */
export interface Plate {
  name: string;
  srcs: string[];
  at: Layout;
}

/**
 * The logo file on disk. Astro puts it on the image metadata as a non-enumerable `fsPath`
 * (present in dev and build in Astro 7). If a later Astro drops it, fall back to the path written in
 * the partner's front matter, relative to the partner file.
 */
function sourcePath(p: Partner, key: Key): string {
  const meta = p.data[key] as (ImageMetadata & { fsPath?: string }) | undefined;
  if (meta?.fsPath && existsSync(meta.fsPath)) return meta.fsPath;
  if (p.filePath) {
    const m = readFileSync(p.filePath, 'utf8').match(new RegExp(`^${key}:\\s*['"]?([^'"#\\n]+?)['"]?\\s*$`, 'm'));
    const f = m && resolve(dirname(p.filePath), m[1]);
    if (f && existsSync(f)) return f;
  }
  throw new Error(`Logo plate: cannot find the file for \`${key}\` of ${p.filePath ?? p.id}.`);
}

/** Every plate the site uses: a wide and a square plate per partner, and a pair plate per lab. */
export async function plateList(): Promise<Plate[]> {
  const out: Plate[] = [];
  for (const p of await getCollection('partners')) {
    const d = p.data;
    out.push({ name: `${p.id}-logo-wide`, srcs: [sourcePath(p, 'logo')], at: singleLayout(d.logo, 'wide') });
    out.push({
      name: `${p.id}-mark-square`,
      srcs: [sourcePath(p, d.logoMark ? 'logoMark' : 'logo')],
      at: singleLayout(d.logoMark ?? d.logo, 'square'),
    });
    if (d.role === 'Funding sponsor') continue;
    const srcs = [sourcePath(p, 'logo'), ...(d.labLogo ? [sourcePath(p, 'labLogo')] : [])];
    out.push({ name: `${p.id}-pair`, srcs, at: pairLayout(d.logo, d.labLogo) });
  }
  return out;
}

/** The hairline between institution and lab: --well-rule (#E3E6EA), 1 % of the plate height wide, middle 64 %. */
const RULE = { r: 0xe3, g: 0xe6, b: 0xea };

/** One plate as an opaque PNG: each logo, flattened onto white, placed on a white canvas (plus the hairline). */
export async function renderPlate({ srcs, at }: Plate): Promise<Buffer> {
  const layers: sharp.OverlayOptions[] = await Promise.all(
    at.spots.map(async (s, i) => ({
      input: await sharp(srcs[i]).flatten({ background: '#ffffff' }).resize(s.logoW, s.logoH, { fit: 'fill' }).toBuffer(),
      left: s.left,
      top: s.top,
    })),
  );
  if (at.seam !== undefined) {
    const w = Math.max(2, Math.round(at.plateH / 100));
    const h = Math.round(at.plateH * 0.64);
    layers.push({
      input: { create: { width: w, height: h, channels: 3, background: RULE } },
      left: at.seam - Math.floor(w / 2),
      top: Math.round((at.plateH - h) / 2),
    });
  }
  return sharp({ create: { width: at.plateW, height: at.plateH, channels: 3, background: '#ffffff' } })
    .composite(layers)
    .removeAlpha()
    .png({ compressionLevel: 9 })
    .toBuffer();
}
