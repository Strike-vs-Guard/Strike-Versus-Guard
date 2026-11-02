import type { ImageMetadata } from 'astro';

/**
 * Logo sizing by visual weight (see .logo-well in global.css).
 * Height = base × 1/√(width ÷ height), 10 % less for square solid-colour tiles,
 * capped at `cap` (the well's inner height). Returns props for <Image>: the
 * `--logo-k` factor (used by the CSS) and the pixel height.
 */
export function logoSize(img: ImageMetadata, base: number, cap: number) {
  const ar = img.width / img.height;
  const k = (Math.abs(ar - 1) < 0.02 ? 0.9 : 1) / Math.sqrt(ar);
  return { style: `--logo-k:${k.toFixed(3)}`, height: Math.ceil(Math.min(base * k, cap)) };
}
