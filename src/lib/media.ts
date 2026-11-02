import { readFileSync } from 'node:fs';
import { join } from 'node:path';

const cache = new Map<string, { width: number; height: number } | null>();

/**
 * Width and height of an MP4 in public/media, read from its video track header (`tkhd`) at build time.
 * Returns null if the file is missing or cannot be read; callers fall back to a fixed frame.
 */
export function videoSize(name: string): { width: number; height: number } | null {
  if (cache.has(name)) return cache.get(name)!;
  let out: { width: number; height: number } | null = null;
  try {
    const buf = readFileSync(join(process.cwd(), 'public', 'media', name));
    const walk = (start: number, end: number): void => {
      let p = start;
      while (p + 8 <= end && !out) {
        let size = buf.readUInt32BE(p);
        const type = buf.toString('latin1', p + 4, p + 8);
        let head = 8;
        if (size === 1) {
          size = Number(buf.readBigUInt64BE(p + 8));
          head = 16;
        } else if (size === 0) size = end - p;
        if (size < head || p + size > end) return;
        if (type === 'moov' || type === 'trak') walk(p + head, p + size);
        else if (type === 'tkhd') {
          const b = p + head;
          const v = buf[b];
          const off = b + (v === 1 ? 4 + 8 + 8 + 4 + 4 + 8 : 4 + 4 + 4 + 4 + 4 + 4) + 8 + 2 + 2 + 2 + 2 + 36;
          const w = buf.readUInt32BE(off) / 65536;
          const h = buf.readUInt32BE(off + 4) / 65536;
          if (w > 0 && h > 0) out = { width: Math.round(w), height: Math.round(h) };
        }
        p += size;
      }
    };
    walk(0, buf.length);
  } catch {
    out = null;
  }
  cache.set(name, out);
  return out;
}
