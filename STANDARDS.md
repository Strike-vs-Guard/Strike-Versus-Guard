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
- **Voice rules** (from the humanising panel, round 4; see `docs/claude/AGENTS_AND_SKILLS.md`):

| Rule | In practice |
|---|---|
| A partner speaks as "we" | Partner pages are first person plural, with the partner's own headings |
| Name people and dates | "Jeremy flew it on 28 October", not "the team tested it" |
| One number per claim | Give the number that matters; put the rest in the report |
| Say what didn't work | Every results page ends with what is still open (`open:`) |
| No self-praising adjectives | No "honest", "robust", "seamless" |
| Avoid triads | Not three tidy items by habit; use two, or four, or one |
| Clips carry a cue | The caption says what to look at: "Watch the gaps between the drones…" |

- "Programme lead" is used only as Jeremy's role. Do not use it for anyone else or for ST Engineering.

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
| `--border` | #343b44 | rules, card borders, the 1 px edge on every photo and video |
| `--accent` (ST red) | #ff4d5e | **only** the wordmark, one rule under the hero title and the "We are here" marker |
| `--guard` (blue) | #6fa3f5 | **only** the Guard team in the game |
| `--strike` (red) | #f2766a | **only** the Strike team in the game |
| `--well` | #ffffff | the white background behind every logo |
| `--max` | 1320px | content width (the full page width, with the gutter) |
| `--gutter` | clamp(16px, 4vw, 64px) | side padding |

Section padding is `clamp(64px, 8vw, 128px)`. Photos and video run to the content edges. Text
columns stay about 68ch wide.

- **Fonts:** IBM Plex Sans Condensed 700 for display; IBM Plex Sans 400/600 for body (17px, line
  height 1.6, about 68ch wide); IBM Plex Mono 500 for eyebrows, labels, dates and captions (uppercase,
  0.06em tracking).
- **Never** colour partners, tracks, buttons or banners blue or red. Red never means "alarm".
- No crosshairs, HUD styling, radar sweeps or military imagery.
- Logos always sit in a `--well`, shown **in colour**, in equal white wells. In the footer they are in
  2×2 partner wells (lab logos beside the institution's), with "Funded by" HTX beside them. (The old
  "greyscale until hover" rule is withdrawn, 3 Nov 2026.)
- **Logo sizing is by visual weight** (`src/lib/logo.ts`): height = base × 1/√(width ÷ height), 10 %
  less for square solid-colour tiles, capped at the well's inner height. A wide wordmark and a square
  badge then look the same size. Do not set logo heights by hand. Wells: footer base 60 px (cap 74 px),
  partner card 104 px, partner page 128 px. Always white, always colour.
- The drone drawing has no dot grid and no corner marks. Research directions is a plain numbered list.
- One theme: pure black background. There is no light mode.

---

## 4. Content model (what people edit)

Everything editable is Markdown or YAML under `content/`. **Templates never hold copy.**

| What | File | Owner |
|---|---|---|
| A partner's card, page and `work:` lines | `content/partners/<NAME>.md` + `content/partners/<NAME>/` images | That partner |
| A partner's square emblem for the Partners menu chip: optional `logoMark:` (falls back to `logo:`) | `content/partners/<NAME>.md` + `content/partners/<NAME>/mark.png` | That partner |
| Funder card | `content/partners/HTX.md` | ST Engineering |
| Page sections | `content/programme/*.md` (one file per section, `order:` sets position) | ST Engineering (+ co-owners in CODEOWNERS) |
| Top of the home page, incl. the `decisions:` list ("What they decide"), the hero `video:`, the one-line `gameNote:` and the Programme page head (`pageEyebrow:`, `pageTitle:`) | `content/programme/overview.md` | ST Engineering |
| Home "Proof so far" section head and its `note:`; the Flights page head is `pageEyebrow:`/`pageTitle:` in `flights.md` | `content/programme/proof.md` | ST Engineering |
| Programme "In simulation" section: one short paragraph and 2–4 clips (`video:`/`poster:` in `public/media/`, `partners:`) | `content/programme/simulation.md` | ST Engineering (+ partners for their clips) |
| Programme "How a command travels" strip: one box per item, `passes:` labels the arrow after it | `content/programme/command.md` | ST Engineering (+ CMU) |
| Localisation section: the three questions (`items:`), the rule (`note:`), the plan as targets, the figure, and the one-line `status:` | `content/programme/localisation.md` | ST Engineering (CMU advises) |
| Flights "Test ladder" (`items:` with `state:` chips; the safety order in the body) and "Outdoors" clip | `content/programme/ladder.md`, `content/programme/outdoor.md` | ST Engineering; CMU for `outdoor.md` |
| Layers of the system (drone diagram and connection diagram) | `content/programme/stack.md` (`icon:` is the layer id) | ST Engineering |
| People on a partner's team: `people:` (name, role, photo, `lead`), a row with faces on the partner page | `content/partners/<NAME>.md`, photos in `content/partners/<NAME>/people/` (400 px square, 80 KB or less) | That partner |
| Open problems: `open:` list and `openLabel:` ("What we haven't solved yet"), one line each | `localisation.md`, `simulation.md`, `flights.md` | ST Engineering (+ CMU for flights) |
| Page head overrides: `pageEyebrow:` / `pageTitle:` (when the section also heads its own page) | `overview.md`, `flights.md` | ST Engineering |
| Clips: `video:` + `poster:` on an item; a hero `video:` on a section | `content/programme/*.md`, files in `public/media/` | ST Engineering; CMU for its clips |
| News, a dated log; `author:` names who wrote it, `draft: true` hides it | `content/updates/YYYY-MM-DD-slug.md` | Any partner |
| Site title, footer | `content/site.yml` | ST Engineering |

- **The schema is the contract:** `src/content.config.ts` validates every file at build time. Add a
  field to the schema before using it. Never weaken a rule to make a broken file pass.
- **Layer ids are fixed:** `strategy`, `safety`, `flight`, `localisation`, `drones`, `integration`
  (layers 1 to 5 plus Integration across all; Localisation is layer 4, ST Engineering leads, CMU provides
  the simulator and technical advice). A partner's
  `work.<layer>` line (90 characters or fewer) is what puts that partner on a layer in both diagrams.
- **Sources:** the October 2026 monthly report (29 Oct 2026) is approved for publication by the
  programme lead (3 Nov 2026): its simulation figures and numbers may go on the site, translated into
  the §2 wording, with proposals labelled as proposals and nothing under review. The D3 FR&PDR
  (July 2026) is confidential, and the localisation brief (22 Oct 2026) stays context only: nothing
  numeric or unpublished from those two goes on the site.
  **Update, 3 Nov 2026:** the programme lead approved publishing selected content from the July FR&PDR
  and the localisation brief. The exclusions still hold: no budgets, prices or cost ceilings; no
  contract or deliverable IDs; no classification markings; nothing about the physical-contact scenario
  and no kinetic wording; no names beyond the three PIs already on the site; no papers under review.
  Every adversarial term is translated per §2, and targets and pass marks stay labelled as targets.
  People: only those named on the site (`people:` lists). Round 3 added CMU's three extra flight clips
  and the Starling photo, taken from CMU's public `svg-website` repo with CMU's consent, credited
  "Photo: <lab>." or "Video: <lab>." (e.g. "Photo: CMU AirLab." in `flights.md`). That repo is never edited.
  Extracted text lives outside the repo, in `~/Documents/GitHub/Strike-Versus-Guard-sources/` on Jeremy's laptop.
- Images must be referenced **relative to the content file** (`./NUS/photo.jpg`), never as `/images/...`.
- **Size limits:** images 5 MB or less and clips 15 MB or less (H.264 MP4, muted, with a `.jpg`
  poster). Both are enforced by `npm run check`.

---

## 5. Page structure (current)

Nav: **Programme · Partners ▾ · Flights · Updates**. There is no Benchmark item; the game stays on home.

**Partners menu:** "Partners" stays a link. The ▾ button opens a panel on hover (120 ms open, 300 ms
close grace), click, or Enter/Space. Escape closes it and returns focus; ArrowDown enters the rows;
it closes on focus-out. Without JS it is just the link. Rows: ST Engineering · NEAR Lab, NUS ·
MARMot Lab, UPenn · xLab, CMU · AirLab (logo chip, name, contribution line), then "Funded by HTX"
(→ `/partners/#funder`) and "All partners: who does what →". On phones the panel opens full width
under the header.

**Home (`src/pages/index.astro`), top to bottom:**
1. Hero: eyebrow, the title (unchanged), positioning statement, the `gameNote:` ("the game we test
   with"), two buttons; right, the muted looping flight clip with its still photo as poster.
2. The game (Benchmark): the Arena, its four steps, "What they decide", the no-pilot note.
3. Proof so far: one-line progress bar from milestones, the four clips 4-across, "All flights →".
4. Who builds which part (Layers): the compact drone, linking to `/partners/#who`.
5. Latest updates (dated log, newest three).
6. Team photo with a caption naming everyone left to right, then the colour logo strip and footer note
   "Four labs, in Singapore, Pittsburgh and Philadelphia. Funded by HTX."

**Programme (`/programme/`):** positioning statement, two tracks, "How a command travels"
(`command.md`), "We try it in simulation first" (`simulation.md`, with "What we haven't solved yet"),
localisation (three question cards, the plan as targets, a figure, `open:` list), research directions
(a plain numbered list).

**Partners (`/partners/`, h1 "Who does what"):** "Each partner writes and maintains its own page."; fully
clickable partner cards; the full explain-mode drone above the connection diagram; the HTX card
(`id="funder"`).

**Partner page (`src/pages/partners/[id].astro`):**
- Header and meta card. "Maintained by <Short> · updated <date> · Edit this page" sits in "At a glance".
- People: a row with faces from `people:` (the lead first).
- "In the system": `DroneDiagram` in `partner` mode, with that partner's layers lit.
- The Markdown body, in first person with the partner's own headings. It may embed simulation clips as
  `<figure class="clip">` (see CONTRIBUTING §4) and has an "In simulation" section.
- "Updates from <Short>".

Page titles are distinct: Programme h1 "How the programme works"; Flights h1 "Flights so far".

**Flights (`/flights/`):** the CMU cage photo (credit line), a lead clip at full width and the other
clips in a grid, each with a mono stamp line and a "Watch …" cue; CMU's outdoor clip (`outdoor.md`);
the test ladder M1–M6 as of July 2026 (`ladder.md`) with the annotated Singapore lab photo; the
localisation status line; "What went wrong, and what's still open" (`open:` in `flights.md`); milestones.

**Updates:** a dated log; each post shows its `author:`.

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
