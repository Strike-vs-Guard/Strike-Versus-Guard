import type { ImageMetadata } from 'astro';
import type { CollectionEntry } from 'astro:content';
import { url } from './url';

/**
 * Logo plates (STANDARDS §3): every logo is shown as one opaque white image, the "plate", made at
 * build time by src/lib/plates.ts and served from /plates/<name>.png (src/pages/plates/[name].png.ts).
 * The white tile is part of the image, so a phone browser that repaints CSS colours (Samsung
 * Internet's dark mode) cannot turn it grey. This file holds the geometry; plates.ts draws it.
 *
 * Sizing by visual weight: logo height = a × k × plate height, k = 1/√(width ÷ height), 0.9× for
 * square tiles, capped at `cap` × plate height and at `wmax` × plate width. A wide wordmark and a
 * square badge then look the same size. Do not size logos by hand: change a recipe here.
 *
 * Every plate is drawn wider than 64 CSS px. Chromium's forced dark mode treats an image drawn at
 * 64 × 64 CSS px or less as an icon and may invert it (white plate turned black); larger images are
 * left alone (measured in Chrome 157, 6 Nov 2026). Hence one image per institution + lab pair, and a
 * chip plate larger than its chip.
 */
type Partner = CollectionEntry<'partners'>;

/** ratio = plate width ÷ height; px = rendered plate height (2× the largest CSS height it is shown at). */
export const RECIPE = {
  /* single logo, 2:1: home row, footer strip, funder tiles */
  wide: { ratio: 2, a: 0.85, cap: 0.7, wmax: 0.86, px: 200 },
  /* institution + lab side by side, 3:1, split by what each logo needs (see pairLayout) */
  pair: { ratio: 3, a: 0.75, cap: 0.8, margin: 0.14, px: 300 },
  /* Partners-menu chip: an 80 px plate, of which the chip shows the centre 36 px (`window`) */
  square: { ratio: 1, a: 0.87, cap: 0.8, wmax: 0.8, px: 160, window: 36 / 80 },
} as const;

/** k = 1/√(aspect ratio), 0.9× for square tiles. */
export const weight = (ar: number) => (Math.abs(ar - 1) < 0.02 ? 0.9 : 1) / Math.sqrt(ar);

/** One logo on a plate, in pixels of the rendered plate. */
export interface Spot {
  logoW: number;
  logoH: number;
  left: number;
  top: number;
}
/** A plate: its rendered size and where each logo goes; `seam` (pairs only): x of the hairline in px. */
export interface Layout {
  plateW: number;
  plateH: number;
  spots: Spot[];
  seam?: number;
}

/** A logo of aspect `ar`, `h` plate heights tall, centred in the band [x0, x1] of a plate `plateH` tall. */
const spot = (x0: number, x1: number, plateH: number, ar: number, h: number): Spot => {
  const logoH = Math.round(h * plateH);
  const logoW = Math.min(x1 - x0, Math.round(logoH * ar));
  return { logoW, logoH, left: x0 + Math.round((x1 - x0 - logoW) / 2), top: Math.round((plateH - logoH) / 2) };
};

/** One logo on a wide or square plate. */
export function singleLayout(img: ImageMetadata, shape: 'wide' | 'square'): Layout {
  const r = RECIPE[shape];
  const ar = img.width / img.height;
  const scale = 'window' in r ? r.window : 1;
  const h = Math.min(r.a * weight(ar), r.cap, (r.wmax * r.ratio) / ar) * scale;
  const plateW = r.ratio * r.px;
  return { plateW, plateH: r.px, spots: [spot(0, plateW, r.px, ar, h)] };
}

/**
 * Institution and lab on one 3:1 plate, with a hairline at the seam (drawn into the image, so no CSS
 * colour is left inside the tile). Each logo is sized by
 * weight; if the two (plus `margin` × height on each side of each logo) do not fit, both shrink by the
 * same factor. The spare width is shared equally, so a long wordmark (ST Engineering, 5.8:1) gets
 * more of the tile than a square badge. Without a lab logo the institution fills the plate.
 */
export function pairLayout(inst: ImageMetadata, lab?: ImageMetadata): Layout {
  const r = RECIPE.pair;
  const plateW = r.ratio * r.px;
  const size = (img: ImageMetadata) => {
    const ar = img.width / img.height;
    const h = Math.min(r.a * weight(ar), r.cap);
    return { ar, h, w: h * ar };
  };
  const a = size(inst);
  if (!lab) return { plateW, plateH: r.px, spots: [spot(0, plateW, r.px, a.ar, Math.min(a.h, (r.ratio - 2 * r.margin) / a.ar))] };
  const b = size(lab);
  const room = r.ratio - 4 * r.margin;
  const s = Math.min(1, room / (a.w + b.w));
  const spare = (room - s * (a.w + b.w)) / 2;
  const seam = Math.round((s * a.w + 2 * r.margin + spare) * r.px);
  return { plateW, plateH: r.px, seam, spots: [spot(0, seam, r.px, a.ar, s * a.h), spot(seam, plateW, r.px, b.ar, s * b.h)] };
}

/** Props for a plate <img>: src, CSS width/height (half the rendered pixels) and alt. */
export interface PlateImg {
  src: string;
  width: number;
  height: number;
  alt: string;
}
const img = (name: string, l: Layout, alt: string): PlateImg => ({
  src: url(`plates/${name}.png`),
  width: l.plateW / 2,
  height: l.plateH / 2,
  alt,
});
const instAlt = (p: Partner) => p.data.logoAlt ?? p.data.institution;

/** The partner's logo on a 2:1 plate. */
export const widePlate = (p: Partner, alt = instAlt(p)) => img(`${p.id}-logo-wide`, singleLayout(p.data.logo, 'wide'), alt);

/** The partner's `logoMark` (else its logo) on an 80 px plate for the 36 px menu chip. */
export const squarePlate = (p: Partner, alt = '') => img(`${p.id}-mark-square`, singleLayout(p.data.logoMark ?? p.data.logo, 'square'), alt);

/** The institution and lab logos on one 3:1 plate with the hairline between them; the alt names both. */
export function pairPlate(p: Partner) {
  const alt = p.data.labLogo && p.data.lab ? `${instAlt(p)} and ${p.data.lab}` : instAlt(p);
  return img(`${p.id}-pair`, pairLayout(p.data.logo, p.data.labLogo), alt);
}
