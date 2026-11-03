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

- Pages (restructured 3 Nov 2026, extended in round 5): **Home**, **Updates**, **Research** (`/research/`, formerly Programme),
  **Partners** (`/partners/`, with a page per partner) and **Flights** (`/flights/`). The first
  single long home page had grown too long; each question a visitor asks now has a page.
- Nav (round 5): Updates · Research · Partners ▾ · Flights · Publications · Contribute, plus a theme toggle. The Partners menu lists each partner's page.
- Home page order (round 2, 3 Nov 2026): hero with flight clip and game note → the game and what the
  drones decide → proof bar and clips → compact drone → updates → team photo and colour logo strip.
  Home is about 5 screens at 1280, down from 6.5.
- **UX panel (round 2).** Three reviewers found: the first screen never said what the game is; 36 % of
  a wide screen was empty; footer logos were grey; partner pages existed but nothing led to them.
  Borrowed: CMU AirLab (full-width footage, one sentence, two buttons), TRI and RAI Institute (home
  as a hub of short cards), DeepMind, ETH ASL and UZH RPG (home never repeats a nav page in full).
  Jeremy chose, from a clickable draft: A compact drone on home (full one on Partners), B no
  Benchmark nav item, C looping clip in the hero.
- **Reports (round 3, 3 Nov 2026).** The programme lead approved publishing selected content from the
  October monthly report, then the July FR&PDR and the localisation brief ("there's no code
  involved"). Exclusions stay: budgets, prices, contract and deliverable IDs, the physical-contact
  scenario and kinetic wording, people beyond those named on the site, work under review. Added:
  "In simulation" per partner, Programme "We try it in simulation first" and "How a command travels",
  Flights "Test ladder" (M1–M6, July 2026), an outdoor clip, and CMU's extra clips and Starling photo
  (from its public `svg-website` repo, with CMU's consent; never edited).
- **Humanising panel (round 4, 3 Nov 2026).** An editor, an art director and an outside professor
  found the site read as machine-written: no names, no dates, nothing went wrong, tidy triads. We
  changed it: people lists with faces per partner; a team caption naming everyone; first-person
  partner pages; open-problem lists; a dated update log with authors; plainer slogans ("the game we
  test with", "Who builds which part", "We try it in simulation first"); a shorter footer note;
  Research directions as a plain numbered list. The hero title stays as it was. Voice rules are in
  STANDARDS §2.
- **Round 5 (3 Nov 2026), lab feedback.** Nine points from the lab, a three-lens panel (design system,
  content architecture, drone interaction) and an approved draft led to: Programme renamed **Research**
  (`/programme/` redirects); new pages **Publications** and **Contribute**; nav Updates · Research ·
  Partners ▾ · Flights · Publications · Contribute; home reordered updates-first (hero with a 2:1 clip
  panel, logo row, updates strip, glance + latest, partner cards, five research themes, the
  interactive drone, flights, publications, people); the Partners page keeps only the connection
  diagram; updates move to one folder per partner with `gallery:` and `link:`; `publications:` per
  partner; `glance.md` and `themes.md`; people photos for all partners; programme dates June 2026 –
  June 2029. Spec: `docs/superpowers/specs/2026-11-03-v3-redesign-design.md`.
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

- Calm: **light by default, dark navy-black with a header toggle** (round 5, replacing the single pure-black theme), no dot grid, Archivo 700 headlines, IBM Plex Sans body, Plex Mono for dates and numbers only. Brand red and blue are type, rules and bands; Strike and Guard colours stay in game figures. Logos sit in white wells (1 px border in light).
- Colour comes from the two teams (inside game figures) and the partner logos. Brand red appears as type, rules and bands: the wordmark, one short rule under the hero title, the "We are here" marker. It is never used for buttons or alarms. Buttons are ink-coloured.
- The two strategy tracks are never coloured blue/red, because those colours mean the game's teams.
- Partner logos sit in equal white wells, in colour (Jeremy, 3 Nov 2026; the greyscale rule is
  withdrawn). The footer shows 2×2 partner wells with lab logos, beside "Funded by" HTX.
- Logos are sized by visual weight (`src/lib/logo.ts`), not by one height, so wide wordmarks and
  square badges look equal. Wells: card 104 px, partner page 128 px.
- The drone drawing lost its dot grid and corner marks; they added noise, not meaning.
- The Flights page leads with one big clip and a grid of the rest, each with a mono stamp and a
  "watch" cue, plus an annotated photo of the Singapore lab.
- Content width is 1200 px (round 5; was 1320) with a fluid gutter, so wide screens are used. Photos and video get a 1 px
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
