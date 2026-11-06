// @ts-check
import { defineConfig } from 'astro/config';

/**
 * BASE_PATH lets the same site be built for three places:
 *   - the live site:   https://strike-vs-guard.github.io/           (base "/")
 *   - the test site:   https://strike-vs-guard.github.io/preview/   (development branch)
 *   - local dev:       http://localhost:4321/
 * The deploy workflow works the base out from the repository name ("<org>.github.io" → "/",
 * anything else → "/<name>/") and sets it; you never need to set it by hand.
 */
const base = process.env.BASE_PATH || '/';
/** `to('research/')` → '<base>research/': redirect targets need the base written in. */
const to = (path) => base.replace(/\/?$/, '/') + path;

export default defineConfig({
  site: process.env.SITE_URL || 'https://strike-vs-guard.github.io',
  base,
  trailingSlash: 'always',
  build: { format: 'directory' },
  /**
   * Old addresses that moved. Each becomes a small page that sends visitors on (static hosting has no
   * server redirects). Astro puts the page under the base itself, but not the target, hence `to()`.
   */
  redirects: {
    '/programme/': to('research/'),
    '/contribute/': to(''),
    '/updates/2026-11-02-website-launch/': to('updates/st/2026-11-02-website-launch/'),
    '/updates/2026-11-03-october-progress/': to('updates/st/2026-11-03-october-progress/'),
  },
});
