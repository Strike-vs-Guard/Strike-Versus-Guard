# Strike vs Guard website: standards

This file defines what the website is and the rules every change must follow, whether the change is
made by a person or by Claude. If a request conflicts with this file, say so before changing anything.
Precedence: the programme lead's explicit instruction, then this file, then personal taste.

---

## 1. What the site is

- **Subject:** Strike vs Guard is a **research programme on decentralised multi-drone autonomy**:
  teams of drones that coordinate, adapt and make decisions on their own in changing environments,
  with no pilot and no central controller.
- **Funding and partners:** funded by **HTX** and carried out by **ST Engineering** (lead partner,
  AI.R.STC · NEAR Lab) in collaboration with **NUS** (MARMot Lab), **UPenn** (xLab) and **CMU** (AirLab).
- **Two strategy tracks:** NUS leads the **learning-based** track; UPenn leads the **formal** track
  (signal temporal logic). Both run on the same stack, **CMU's AirStack on Starling 2 Max drones**.
- ***Strike vs Guard* is the benchmark game**, not the purpose of the programme: a two-team game that
  forces the drones to plan, communicate and recover from failures in real time.
- **Audience:** sponsors and visitors, researchers, and the partners themselves.
- **Job of the site:** explain the programme, credit each partner fairly, and show real results.

### The positioning statement (use word for word where the programme is introduced)

> This is a research programme, funded by HTX and carried out by ST Engineering in collaboration with
> Carnegie Mellon University, the University of Pennsylvania, and the National University of Singapore,
> working toward decentralised multi-drone autonomy: teams of drones that coordinate, adapt, and make
> decisions on their own in changing environments, with no pilot and no central controller.

---

## 2. Tone and wording

- It is a lab website: plain present tense and short sentences. No marketing language, and no
  mission or defence framing.
- **Never frame it as counter-UAS, counter-drone or defence.**
- British spelling: behaviour, decentralised, programme.

| Avoid | Use instead |
|---|---|
| intruder, threat, enemy, hostile | Strike team, opposing team, other side |
| defend, protect | hold the zone, Guard team |
| neutralise, intercept, engage, kill | tag, reach, score |
| counter-UAS, counter-drone, airspace protection | decentralised multi-drone autonomy |
| target(s) | goal, zone |
| swarm | drone team, team of drones |
| operator screen | ground station |
| central controller / "brain" that commands the team | team skills, shared plan, peer-to-peer |

- Check images for words baked into them, not only the page text. The NUS "learned plays" figure was
  cropped for this reason.
- **Partners are equals.** ST Engineering is the *lead partner* (it coordinates and integrates); NUS,
  UPenn and CMU are *partners* who each lead a core part of the research. Never use "research partner"
  or "programme lead" wording that ranks them. HTX is the **funder**, shown separately ("Funded by HTX").
- **Partner order everywhere:** ST Engineering, NUS, UPenn, CMU (set by `order:` in each partner file).

---

## 3. Visual identity: "lab notebook, not mission control"

All tokens live in `src/styles/global.css`. Do not introduce new colours or fonts.

| Token | Value | Use |
|---|---|---|
| `--bg` | #000000 | page |
| `--surface` | #111417 | cards, alternate sections |
| `--text` | #e6e8eb | text, buttons (ink), selected states |
| `--muted` | #9ba4af | secondary text, labels |
| `--border` | #262b31 | rules, card borders |
| `--accent` (ST red) | #ff4d5e | **only** the wordmark, one rule under the hero title and the "We are here" marker |
| `--guard` (blue) | #6fa3f5 | **only** the Guard team in the game |
| `--strike` (red) | #f2766a | **only** the Strike team in the game |
| `--well` | #ffffff | the white background behind every logo |

- **Fonts:** IBM Plex Sans Condensed 700 for display; IBM Plex Sans 400/600 for body (17px, line
  height 1.6, about 68ch wide); IBM Plex Mono 500 for eyebrows, labels, dates and captions (uppercase,
  0.06em tracking).
- **Never** colour partners, tracks, buttons or banners blue or red. Red never means "alarm".
- No crosshairs, HUD styling, radar sweeps or military imagery.
- Logos always sit in a `--well`. Footer logos are greyscale until hover.
- One theme: pure black background. There is no light mode.

---

## 4. Content model (what people edit)

Everything editable is Markdown or YAML under `content/`. **Templates never hold copy.**

| What | File | Owner |
|---|---|---|
| A partner's card, page and `work:` lines | `content/partners/<NAME>.md` + `content/partners/<NAME>/` images | That partner |
| Funder card | `content/partners/HTX.md` | ST Engineering |
| Page sections | `content/programme/*.md` (one file per section, `order:` sets position) | ST Engineering (+ co-owners in CODEOWNERS) |
| Top of the home page, incl. the `decisions:` list ("What they decide") | `content/programme/overview.md` | ST Engineering |
| Localisation section and its one-line `status:` | `content/programme/localisation.md` | ST Engineering (CMU advises) |
| Layers of the system (drone diagram and connection diagram) | `content/programme/stack.md` (`icon:` is the layer id) | ST Engineering |
| News | `content/updates/YYYY-MM-DD-slug.md` | Any partner |
| Site title, footer | `content/site.yml` | ST Engineering |

- **The schema is the contract:** `src/content.config.ts` validates every file at build time. Add a
  field to the schema before using it. Never weaken a rule to make a broken file pass.
- **Layer ids are fixed:** `strategy`, `safety`, `flight`, `localisation`, `drones`, `integration`
  (layers 1 to 5 plus Integration across all; Localisation is layer 4, ST Engineering leads, CMU provides
  the simulator and technical advice). A partner's
  `work.<layer>` line (90 characters or fewer) is what puts that partner on a layer in both diagrams.
- **Confidential sources:** the localisation brief (22 Oct 2026), the monthly report (29 Oct 2026) and
  the D3 FR&PDR (July 2026) are context only. Nothing numeric or unpublished from them goes on the site.
  Extracted text lives outside the repo, in `~/Documents/GitHub/Strike-Versus-Guard-sources/` on Jeremy's laptop.
- Images must be referenced **relative to the content file** (`./NUS/photo.jpg`), never as `/images/...`.
- **Size limits:** images 5 MB or less and clips 15 MB or less (H.264 MP4, muted, with a `.jpg`
  poster). Both are enforced by `npm run check`.

---

## 5. Page structure (current)

Nav: **Programme · Benchmark** (home anchor) **· Partners · Flights · Updates**.

**Home (`src/pages/index.astro`), top to bottom:**
1. Hero: wordmark, positioning statement, flight-cage photo, and the "What they decide" strip under the photo.
2. `#benchmark`: animated arena (Divide · Share · Adapt · Recover).
3. Drone diagram with the five layers (`DroneDiagram`). Clicking the drone lights it locally and links to the Partners page.
4. The four flight clips.
5. Milestones (move `current: true` each year).
6. Latest updates.
7. Team photo last, with "Funded by HTX".

**Programme (`/programme/`):** positioning statement, two tracks, localisation (with its `status:` line),
research directions.

**Partners (`/partners/`):** "Five layers, four partners, one team"; partner cards; the connection
diagram (`ConnectionDiagram`); proof so far.

**Partner page (`src/pages/partners/[id].astro`):**
- Header and meta card.
- "In the system": `DroneDiagram` in `partner` mode, with that partner's layers lit.
- The Markdown body.
- Their updates.

**Flights (`/flights/`):** the October 2026 flight day story with the clips, the localisation status
line, and milestones.

**Updates:** unchanged.

The page sections live as section components under `src/components/sections/`.

**Shared components:**

| Component | What it is |
|---|---|
| `Arena.astro` | Benchmark animation |
| `DroneDiagram.astro` | Annotated drone |
| `ConnectionDiagram.astro` | Partner ↔ layer links |
| `Clip.astro` | Click-to-play video |
| `PartnerChips.astro` | Partner name chips |
| `Icon.astro` | Icons |
| `Wordmark.astro` | Site wordmark |

`DroneDiagram` and `ConnectionDiagram` share one selection through `document` CustomEvents (`sys:select`).

---

## 6. Engineering rules

- **Stack:** Astro 7.4.4 (static), Node **24 LTS** (`.nvmrc`; Astro needs Node 22.23.4 or newer).
  Vanilla JS only; no UI frameworks.
- **Base path:** never hard-code `/Strike-Versus-Guard/`. Use `url()` from `src/lib/url.ts` in
  templates and `import.meta.env.BASE_URL` elsewhere. The same build serves `/`, `/preview/` and local dev.
- Component CSS is scoped, or global with a unique prefix (`.pd-*`, `.pc-*`). Component JS must
  support more than one instance per page (find the root via `document.currentScript.closest(...)`;
  give ids a per-instance suffix).
- **Accessibility:**
  - Interactive things are `<button>` or `<a>`, with a visible focus ring and a pressed or selected
    state that is visible without colour alone.
  - Respect `prefers-reduced-motion`.
  - Phones (390px wide) must have **zero horizontal scroll**.
  - Touch targets must be 44px or larger.
  - Images must have real alt text.
- **Interactivity must look interactive.** Labels such as "Select", "Show partners ↓" and "See more →",
  a pressed state and a cursor. Hover-only discovery is not enough.
- **No empty grids.** If a matrix would be mostly empty, choose another representation.

---

## 7. Branches, review and publishing

| Branch | Purpose | Published at |
|---|---|---|
| `development` | All edits happen here | Test site: https://strike-vs-guard.github.io/Strike-Versus-Guard/preview/ |
| `main` | Live site; changes arrive only via a pull request from `development` | https://strike-vs-guard.github.io/Strike-Versus-Guard/ |

- **Only these two branches exist.** Do not create feature branches. Do not add Dependabot or any
  per-PR preview tooling, because they create branches.
- `.github/workflows/ci.yml` runs build + link check on pull requests and on pushes to `development`.
- `.github/workflows/deploy.yml` builds **both** branches and publishes them together. It runs on a
  push to `main`, and also after CI passes on `development` (via `workflow_run`, because only the
  default branch may publish to Pages).
- **GitHub Pages source must be "GitHub Actions"** (not "Deploy from a branch").
- Before every push, `npm run check` must pass locally.
- Claude may push to `development`. It should push to `main` only when the programme lead says so.

---

## 8. Definition of done for any change

- [ ] `npm run check` passes (schema, build, internal links, size budget).
- [ ] Checked in a real browser (Playwright screenshots) at 1280px and 390px:
      no overflow, no console errors.
- [ ] Wording follows §2; colours and fonts follow §3; the partner order is correct.
- [ ] Interactive parts tested by mouse **and** keyboard.
- [ ] Docs updated if the structure or workflow changed (`README.md`, `CONTRIBUTING.md`,
      `docs/design-decisions.md`, this file).
- [ ] Pushed to `development`; the test site checked after the deploy finishes.
