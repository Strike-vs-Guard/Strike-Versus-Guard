// @ts-check
import { defineConfig } from 'astro/config';

/**
 * BASE_PATH lets the same site be built for three places:
 *   - the live site:   https://strike-vs-guard.github.io/Strike-Versus-Guard/
 *   - the test site:   .../Strike-Versus-Guard/preview/  (development branch)
 *   - local dev:       http://localhost:4321/Strike-Versus-Guard/
 * The GitHub workflows set it; you never need to set it by hand.
 * If the site moves to its own domain, change the default to '/'.
 */
const base = process.env.BASE_PATH || '/Strike-Versus-Guard/';
/** `to('research/')` → '/Strike-Versus-Guard/research/': redirect targets need the base written in. */
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
    '/updates/2026-11-02-website-launch/': to('updates/st/2026-11-02-website-launch/'),
    '/updates/2026-11-03-october-progress/': to('updates/st/2026-11-03-october-progress/'),
  },
});
