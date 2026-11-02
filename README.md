# Strike vs Guard: programme website

Source for the website of **Strike vs Guard**, a research programme funded by HTX and carried out by
ST Engineering with Carnegie Mellon University, the University of Pennsylvania and the National
University of Singapore, working toward decentralised multi-drone autonomy.

- **Live site:** https://strike-vs-guard.github.io/Strike-Versus-Guard/
- **Partners editing their page:** read [CONTRIBUTING.md](CONTRIBUTING.md).
- **Repo admins, first-time setup:** read [docs/admin-setup.md](docs/admin-setup.md).
- **Why it's built this way:** [docs/design-decisions.md](docs/design-decisions.md).

## How it fits together

```
content/                     ← everything people edit (Markdown + images)
  partners/NUS.md  NUS/        one file + one image folder per partner
  partners/UPenn.md UPenn/
  partners/CMU.md  CMU/
  partners/ST.md   ST/
  partners/HTX.md  HTX/        sponsor card (no separate page)
  programme/*.md               shared home-page sections (ST-owned)
  updates/*.md                 news posts
  site.yml                     site title, footer
public/media/                ← flight clips (MP4) and their poster frames
src/                         ← layout, styles, components (ST-owned)
  content.config.ts            the rules every content file is checked against
.github/workflows/
  ci.yml                       build + link check on every pull request
  preview.yml                  publishes each pull request to /pr-preview/pr-N/
  deploy.yml                   publishes main to the live site
```

Built with [Astro](https://astro.build) (static output, no server). Hosted on GitHub Pages from the
`gh-pages` branch.

## Commands

| Command | What it does |
|---|---|
| `npm ci` | Install (first time) |
| `npm run dev` | Live preview at http://localhost:4321/Strike-Versus-Guard/ |
| `npm run check` | Build the whole site and check every internal link (same as CI) |
| `npm run preview` | Serve the built site from `dist/` |

Requires Node.js 22 LTS (see `.nvmrc`), or use the included Codespaces / dev container.
