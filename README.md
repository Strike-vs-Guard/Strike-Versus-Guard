# Strike vs Guard: programme website

Source for the website of **Strike vs Guard**, a research programme funded by HTX and carried out by
ST Engineering with the National University of Singapore, the University of Pennsylvania and
Carnegie Mellon University, working toward decentralised multi-drone autonomy.

- **Live site** (branch `main`): https://strike-vs-guard.github.io/Strike-Versus-Guard/
- **Test site** (branch `development`): https://strike-vs-guard.github.io/Strike-Versus-Guard/preview/
- **Editing your lab's page, posting an update or adding a publication:** read
  [CONTRIBUTING.md](CONTRIBUTING.md). It covers the browser editor (no install) and a local clone.
  Field rules: [`src/content.config.ts`](src/content.config.ts); starting file: [docs/partner-template.md](docs/partner-template.md).
- **Repo admins, first-time setup:** read [docs/admin-setup.md](docs/admin-setup.md).
- **Why it's built this way:** [docs/design-decisions.md](docs/design-decisions.md).
- **Rules every change follows:** [STANDARDS.md](STANDARDS.md).
- **Working on this with Claude:** [CLAUDE.md](CLAUDE.md), [handoff](docs/claude/HANDOFF.md), [debugging process](docs/claude/DEBUGGING.md), [agents and skills](docs/claude/AGENTS_AND_SKILLS.md), [conversation history](docs/claude/jeremy.md).

## How it fits together

```
content/                     ← everything people edit (Markdown + images)
  partners/NUS.md  NUS/        one file + one image folder per partner (people/ holds team photos)
  partners/UPenn.md UPenn/
  partners/CMU.md  CMU/
  partners/ST.md   ST/
  partners/HTX.md  HTX/        sponsor card (no separate page)
  programme/*.md               shared page sections (ST-owned), incl. glance.md, themes.md, localisation.md
  updates/<partner>/*.md       news posts, one folder per partner (st, nus, upenn, cmu) + images/
  site.yml                     site title, footer
public/media/                ← flight clips (MP4) and their poster frames (8 MB per file, 60 MB total; STANDARDS §9)
src/                         ← layout, styles, components (ST-owned)
  content.config.ts            the rules every content file is checked against
.github/workflows/
  ci.yml                       build + link check on pull requests and development
  deploy.yml                   publishes main (live) and development (/preview/) together
```

Pages: Home, Updates, Research (`/research/`; `/programme/` redirects), Partners (`/partners/`, also a header menu that lists every partner's page), Flights, Publications and Contribute.
Light theme by default, dark (navy-black) with a toggle in the header. Each partner edits its own Markdown file, including its `people:`, `publications:` and its own update folder `content/updates/<partner>/` (`author:`).

Built with [Astro](https://astro.build) (static output, no server). Hosted on GitHub Pages, deployed by
GitHub Actions. The repository keeps only two branches: `main` (live) and `development` (edits and test site).

## Commands

| Command | What it does |
|---|---|
| `npm ci` | Install (first time). Also installs the git hooks that refuse pushes to `main`, new branches and failing checks |
| `npm run dev` | Live preview at http://localhost:4321/Strike-Versus-Guard/ |
| `npm run check` | Build the whole site; check the schema, every internal link and the size budget (same as CI) |
| `npm run shots -- /<page>/ [--theme dark] [--width 390]` | Screenshot one built page in Google Chrome (or `SVG_BROWSER=/path`); PNG in `.shots/`, must print `"ok": true` |
| `npm run preview` | Serve the built site from `dist/` |

Requires Node.js 24 LTS, or 22.23.4 or newer (see `.nvmrc`), or use the included Codespaces / dev container.
