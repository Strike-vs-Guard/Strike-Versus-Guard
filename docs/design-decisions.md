# Design decisions

Three advisers each proposed one part of the site: content and structure, the technical stack and
editing workflow, and the visual design. The decisions below reconcile their proposals.

## Positioning

- The site presents a **research programme on decentralised multi-drone autonomy**. *Strike vs Guard*
  is the benchmark game used to test it, not the programme's purpose. The opening text is the
  programme's own positioning statement, word for word.
- No counter-UAS or defence framing. A word list in `CONTRIBUTING.md` (§5) keeps partner edits on
  tone. Images were checked for wording baked into them, and the NUS figure was cropped to remove
  its "red intruders" caption.
- "Strike" and "Guard" are used only as team names in the game, in red and blue as on the poster.

## Structure

- Four pages plus Updates (restructured 3 Nov 2026): **Home**, **Programme** (`/programme/`),
  **Partners** (`/partners/`, with a page per partner) and **Flights** (`/flights/`). The first
  single long home page had grown too long; each question a visitor asks now has a page.
- Nav: Programme · Partners ▾ · Flights · Updates. The Partners menu lists each partner's page.
- Home page order (round 2, 3 Nov 2026): hero with flight clip and game note → the game and what the
  drones decide → proof bar and clips → compact drone → updates → team photo and colour logo strip.
  Home is about 5 screens at 1280, down from 6.5.
- **UX panel (round 2).** Three reviewers found: the first screen never said what the game is; 36 % of
  a wide screen was empty; footer logos were grey; partner pages existed but nothing led to them.
  Borrowed: CMU AirLab (full-width footage, one sentence, two buttons), TRI and RAI Institute (home
  as a hub of short cards), DeepMind, ETH ASL and UZH RPG (home never repeats a nav page in full).
  Jeremy chose, from a clickable draft: A compact drone on home (full one on Partners), B no
  Benchmark nav item, C looping clip in the hero.
- Five layers: Strategy, Safety, Flight, **Localisation** (ST Engineering leads; CMU provides the
  simulator and technical advice), Drones, plus Integration across all.
- The reports behind the localisation work are confidential. They are used for context only, and
  nothing numeric or unpublished from them is on the site.
- **One Markdown file per partner** (`content/partners/NUS.md`, `UPenn.md`, `CMU.md`, `ST.md`).
  Front matter feeds the card on the home page; the body becomes the partner page.
- HTX has a small file that drives its sponsor card. It has no separate page, because a sponsor page
  would sit empty.
- Shared sections are separate Markdown files in `content/programme/`, so text changes never touch
  templates.

## Technology

- **Astro** static site. Chosen because it **validates every content file against a schema at build
  time**: a missing field, an over-long summary or a missing image fails the build with the file and
  field named, before anything reaches the live site. It also gives full control of a custom landing
  page.
  - Considered and set aside: Hugo (no validation), Eleventy (no validation), Jekyll (Ruby setup,
    restricted plugins), MkDocs (looks like documentation).
- Pinned to **Astro 7.4.4** because `npm audit` reports advisories for all earlier releases. It
  requires Node.js ≥ 22.23.4, so `.nvmrc` pins Node 24 LTS (a plain "22" let CI pick 22.23.3, which Astro rejects), and a Codespaces dev container covers
  partners who can't install it.
- **Two branches only:** `main` is the live site and `development` is where edits happen. Each deploy
  builds both branches and publishes them together through GitHub Pages' Actions deployment: `main` at
  the root and `development` at `/preview/`, with a "Test site" banner and `noindex`.
  - This replaced an earlier design with a `gh-pages` branch and per-pull-request previews.
  - Previews per pull request would need a branch per change, and the programme wants at most two branches.
  - There is no Dependabot for the same reason.
- No third-party hosting accounts.
- **CODEOWNERS** plus a protected `main`: on the `development` → `main` pull request, each partner
  approves changes to their own files; ST Engineering owns layout, workflows and shared text.
- A dependency-free link checker (`scripts/check-links.mjs`) runs in CI. External links are not
  fetched, to keep CI reliable.

## Visual design: "lab notebook, not mission control"

- Calm: one pure-black theme (no light mode, no toggle; decided by Jeremy, 3 Nov 2026), graph-paper dot grid, IBM Plex Sans / Condensed / Mono.
- Colour comes from the two teams and the partner logos only. ST red appears in three places: the
  wordmark, one short rule under the hero title, and the "We are here" milestone marker. It is never
  used for buttons, banners or backgrounds. Buttons are ink-coloured.
- The two strategy tracks are never coloured blue/red, because those colours mean the game's teams.
- Partner logos sit in equal white wells, in colour (Jeremy, 3 Nov 2026; the greyscale rule is
  withdrawn). The footer groups them "Funded by | Partners".
- Content width is 1320 px with a fluid gutter, so wide screens are used. Photos and video get a 1 px
  edge.
- Signature visual: an animated diagram of the game in four beats (Divide, Share, Adapt, Recover),
  drawn in SVG. Each beat is synced to a clickable caption. It pauses off-screen and does not auto-play
  for visitors who prefer reduced motion. Teams differ by shape (filled vs outlined rotors), not
  colour alone.
- Flight clips are click-to-play (`preload="none"`), muted, with poster frames.
- Layout is checked at 390 px wide with no horizontal
  scroll.

## Relationship to CMU's `svg-website`

CMU maintains a separate site, [`Strike-vs-Guard/svg-website`](https://github.com/Strike-vs-Guard/svg-website),
served at https://strike-vs-guard.github.io/svg-website/. It is the technical project page and developer
documentation for the SVG ground-control software in AirStack. It is built with React and Vite, and its docs
are synced from AirStack with Zensical. The two sites have different jobs:

| | This site (`Strike-Versus-Guard`) | CMU's `svg-website` |
|---|---|---|
| Audience | Sponsors, visitors, researchers, all partners | Developers and operators of the ground controller |
| Content | Programme, both strategy tracks, benchmark, partners, news | CBF filter, geofence, scenarios, experiments C1–C5, setup docs |
| Editing | Markdown per partner, PR previews | TypeScript data files plus docs synced from AirStack |

This site links to CMU's from the CMU partner page. Ideas adopted from it:
- a size budget in `npm run check`
- poster frames with `preload="none"` video
- deriving the base path from the repository name in the workflows
- deploying with GitHub Pages' Actions source

Both sites deploy to GitHub Pages from separate repositories, so their Pages settings don't interfere.
