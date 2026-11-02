# Strike vs Guard: programme website

Source for the website of **Strike vs Guard**, a research programme funded by HTX and carried out by
ST Engineering with Carnegie Mellon University, the University of Pennsylvania and the National
University of Singapore, working toward decentralised multi-drone autonomy.

- **Live site** (branch `main`): https://strike-vs-guard.github.io/Strike-Versus-Guard/
- **Test site** (branch `development`): https://strike-vs-guard.github.io/Strike-Versus-Guard/preview/
- **Partners editing their page:** read [CONTRIBUTING.md](CONTRIBUTING.md).
- **Repo admins, first-time setup:** read [docs/admin-setup.md](docs/admin-setup.md).
- **Why it's built this way:** [docs/design-decisions.md](docs/design-decisions.md).
- **Rules every change follows:** [STANDARDS.md](STANDARDS.md).
- **Working on this with Claude:** [CLAUDE.md](CLAUDE.md), [handoff](docs/claude/HANDOFF.md), [debugging process](docs/claude/DEBUGGING.md), [agents and skills](docs/claude/AGENTS_AND_SKILLS.md), [conversation history](docs/claude/jeremy.md).

## How it fits together

```
content/                     ← everything people edit (Markdown + images)
  partners/NUS.md  NUS/        one file + one image folder per partner
  partners/UPenn.md UPenn/
  partners/CMU.md  CMU/
  partners/ST.md   ST/
  partners/HTX.md  HTX/        sponsor card (no separate page)
  programme/*.md               shared page sections (ST-owned), incl. localisation.md
  updates/*.md                 news posts
  site.yml                     site title, footer
public/media/                ← flight clips (MP4) and their poster frames
src/                         ← layout, styles, components (ST-owned)
  content.config.ts            the rules every content file is checked against
.github/workflows/
  ci.yml                       build + link check on pull requests and development
  deploy.yml                   publishes main (live) and development (/preview/) together
```

Pages: Home, Programme (`/programme/`), Partners (`/partners/`, also a header menu that lists every partner's page), Flights (`/flights/`) and Updates.
One pure-black theme. Each partner edits its own Markdown file.

Built with [Astro](https://astro.build) (static output, no server). Hosted on GitHub Pages, deployed by
GitHub Actions. The repository keeps only two branches: `main` (live) and `development` (edits and test site).

## Commands

| Command | What it does |
|---|---|
| `npm ci` | Install (first time) |
| `npm run dev` | Live preview at http://localhost:4321/Strike-Versus-Guard/ |
| `npm run check` | Build the whole site and check every internal link (same as CI) |
| `npm run preview` | Serve the built site from `dist/` |

Requires Node.js 24 LTS, or 22.23.4 or newer (see `.nvmrc`), or use the included Codespaces / dev container.
