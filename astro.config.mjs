// @ts-check
import { defineConfig } from 'astro/config';

/**
 * BASE_PATH lets the same site be built for three places:
 *   - the live site:   https://strike-vs-guard.github.io/Strike-Versus-Guard/
 *   - a PR preview:    .../Strike-Versus-Guard/pr-preview/pr-<N>/
 *   - local dev:       http://localhost:4321/Strike-Versus-Guard/
 * The GitHub workflows set it; you never need to set it by hand.
 * If the site moves to its own domain, change the default to '/'.
 */
const base = process.env.BASE_PATH || '/Strike-Versus-Guard/';

export default defineConfig({
  site: process.env.SITE_URL || 'https://strike-vs-guard.github.io',
  base,
  trailingSlash: 'always',
  build: { format: 'directory' },
});
