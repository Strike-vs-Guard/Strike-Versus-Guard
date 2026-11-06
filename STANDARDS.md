# Strike vs Guard website: standards

This file defines what the website is and the rules every change must follow, whether the change is
made by a person or by Claude. If a request conflicts with this file, say so before changing anything.
Precedence: the site owner's explicit instruction, then this file, then personal taste.

---

## 1. What the site is

- **Subject:** Strike vs Guard is a **research programme on decentralised multi-drone autonomy**:
  teams of drones that coordinate, adapt and make decisions on their own in changing environments,
  with no pilot and no central controller.
- **Funding and partners:** funded by **HTX** and carried out by **ST Engineering** (lead partner,
  AI.R.STC · NEAR Lab) in collaboration with **NUS** (MARMoT Lab), **UPenn** (xLab) and **CMU** (AirLab).
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
| Say what didn't work | Localisation and simulation end with what is still open (`open:`); Flights has none (owner, 4 Nov 2026) |
| No self-praising adjectives | No "honest", "robust", "seamless" |
| Avoid triads | Not three tidy items by habit; use two, or four, or one |
| Clips carry a cue | The caption says what to look at: "Watch the gaps between the drones…" |


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
- Research themes are named by content (learning track, formal track, safety filter, localisation, simulation), not by number or codename.
- **Partner order everywhere:** ST Engineering, NUS, UPenn, CMU (set by `order:` in each partner file).

---

## 3. Visual identity: "lab notebook, not mission control"

All tokens live in `src/styles/global.css`. Do not introduce new colours or fonts. **Light is the
default** (it follows the system setting); **dark** is navy-black, not pure black. A sun/moon toggle in
the header switches them and stores the choice in `localStorage.theme`; an inline script in `Base.astro`
sets `data-theme` before first paint (no flash). If CMU's video overlay is kept, the hero crop must not cut the status card (see §9). Partners need do nothing for it.

| Token | Light | Dark | Use |
|---|---|---|---|
| `--bg` | #FFFFFF | #0B1622 | page |
| `--surface` | #F2F6FA | #12243A | alternate sections, wells behind figures |
| `--text` | #12212F | #E8EDF2 | text, buttons (ink) |
| `--muted` | #5A6470 | #9AAABB | secondary text, labels |
| `--border` | #E3E6EA | #26384D | rules, the 1 px edge on every photo and video |
| brand red | #B3122E | #FF5A6E | **type, rules and bands only**: wordmark, one rule under the hero title, the "We are here" marker |
| brand blue | #1A3E62 | #1A3E62 | bands and links only |
| `--link` | #1A3E62 | `--text` | brand blue as link text in light; plain text colour in dark (guard blue stays in game figures) |
| `--band` / `--band-text` / `--band-muted` / `--band-accent` | #1A3E62 / #E8EDF2 / #B4C2D0 / #FF8A98 | same | bands that stay dark in both themes: footer, partner-page file line (text 9.3:1, muted 6.1:1, accent 4.9:1) |
| `--media` | #0B1622 | #0B1622 | behind and over video only: hero panel, play-button discs |
| `--strike` | #D9542C | #F2766A | **only** the Strike team inside game figures |
| `--guard` | #2D6FD0 | #6FA3F5 | **only** the Guard team inside game figures |
| `--well` / `--well-bg` | #FFFFFF / none | #FFFFFF / `--well` | logos: no background or border in light; a soft white well (no border) in dark and on the footer band |
| `--max` | 75rem | 75rem | content width, with the gutter: 1200 px at root 16 px, 1500 px at root 20 px |

**Fluid scale:** the root font size is `clamp(1rem, 0.75rem + 0.45vw, 1.25rem)`: 16 px on phones,
about 18 px at 1280 wide, 20 px from 1780 wide. Every type step and the content width are in rem, so
the whole page grows with the monitor. Steps: 14 / 16 / 18 (body) / 22 (h3) / 28 / 36 (h2) / 44 / 68 (h1)
at root 16. Text columns are in rem or ch, never px.

Section padding is 96 to 112 px. Corners are 3 px. Rules, not boxed cards. Text columns stay about
68ch wide.

- **Fonts:** **Archivo 700** for headlines; IBM Plex Sans 400/600 for body (18px at root 16, line height 1.6,
  about 68ch wide); IBM Plex Mono 500 only for dates, numbers and page-level labels. The header
  wordmark is larger than before. The Research page uses larger, standard type (h2 step-4, body step-1).
- No numbered circles, pill chips or dot grid. Mono labels appear at page level only.
- **Never** colour partners, tracks, buttons or banners blue or red. Red never means "alarm".
- No crosshairs, HUD styling, radar sweeps or military imagery.
- Logos are shown **in colour**. In light mode they sit straight on the page (no well, no border; a
  logo's own white background multiplies away). In dark mode, and on the dark footer band in both
  themes, each sits in a soft white `--well` (no border, 3 px corners) of the same size, so nothing
  shifts. "Funded by" HTX gets the same treatment. (4 Nov 2026; greyscale-until-hover withdrawn 3 Nov.)
- **Logo sizing is by visual weight** (`src/lib/logo.ts`): height = base × 1/√(width ÷ height), 10 %
  less for square solid-colour tiles, capped at the well's inner height. A wide wordmark and a square
  badge then look the same size. Do not set logo heights by hand. Bases (box height): home row 72 px (104 px),
  footer 84 px (100 px), partner card 70 px (112 px), partner page 106 px (164 px).
- **Portraits are circles** everywhere (`border-radius: 50%`, `object-fit: cover`, one diameter per
  row); the initials fallback is a circle too.
- The drone drawing has no dot grid and no corner marks. Research directions is a plain numbered list.
- Two themes (light default, dark navy-black). Brand red and blue never colour partners, tracks or buttons; Strike and Guard colours never leave the game figures. (Round 5 replaced the single pure-black theme, 3 Nov 2026.)

---

## 4. Content model (what people edit)

Everything editable is Markdown or YAML under `content/`. **Templates never hold copy.**

| What | File | Owner |
|---|---|---|
| A partner's card, page and `work:` lines | `content/partners/<NAME>.md` + `content/partners/<NAME>/` images | That partner |
| A partner's square emblem for the Partners menu chip: optional `logoMark:` (falls back to `logo:`) | `content/partners/<NAME>.md` + `content/partners/<NAME>/mark.png` | That partner |
| Funder card | `content/partners/HTX.md` | ST Engineering |
| Research page and home sections | `content/programme/*.md` (one file per section, `order:` sets position) | ST Engineering (+ co-owners in CODEOWNERS) |
| Home "At a glance" status lines: `items:` with `state:` (Done, In progress, Not yet) and the "as of" `note:` | `content/programme/glance.md` | ST Engineering |
| Home "Research themes" (five rows: `icon:` is the theme id, `state:`, `partners:`) | `content/programme/themes.md` | ST Engineering |
| Publications of a partner: `publications:` (`title`, `authors`, `venue`, `year`, `status` = published / accepted / preprint / workshop, optional `link`, `pdf`, `image`) | `content/partners/<NAME>.md` | That partner |
| Top of the home page, incl. the `decisions:` list ("What they decide"), the hero `video:`, the one-line `gameNote:` and the Research page head (`pageEyebrow:`, `pageTitle:`) | `content/programme/overview.md` | ST Engineering |
| Home "Proof so far" section head and its `note:`; the Flights page head is `pageEyebrow:`/`pageTitle:` in `flights.md` | `content/programme/proof.md` | ST Engineering |
| Research "In simulation" section: one short paragraph and 2–4 clips (`video:`/`poster:` in `public/media/`, `partners:`) | `content/programme/simulation.md` | ST Engineering (+ partners for their clips) |
| Research "How a command travels" strip: one box per item, `passes:` labels the arrow after it | `content/programme/command.md` | ST Engineering (+ CMU) |
| Localisation section: the three questions (`items:`), the rule (`note:`), the plan as targets, the figure, and the one-line `status:` | `content/programme/localisation.md` | ST Engineering (CMU advises) |
| Flights "Test ladder" (`items:` with `state:` chips; the safety order in the body) and "Outdoors" clip | `content/programme/ladder.md`, `content/programme/outdoor.md` | ST Engineering; CMU for `outdoor.md` |
| Layers of the system (drone diagram and connection diagram) | `content/programme/stack.md` (`icon:` is the layer id) | ST Engineering |
| People on a partner's team: `people:` (name, role, photo, `lead`), a row with faces on the partner page and the people row on home; photos for every partner come from the lab's profile pictures | `content/partners/<NAME>.md`, photos in `content/partners/<NAME>/people/` (400 px square, 80 KB or less) | That partner |
| "About the lab" on the partner page: `labBlurb:` (three sentences in "we" voice, 420 characters or fewer: who you are, what you work on, your part in the programme) and `bio:` on a person (two sentences, third person, 300 or fewer: title, lab, research, degree; no awards) with an optional profile `link:`. Facts come from the lab's own website; a partner approves its own text | `content/partners/<NAME>.md` | That partner (drafted by ST Engineering) |
| Open problems: `open:` list and `openLabel:` ("What we haven't solved yet"), one line each | `localisation.md`, `simulation.md` | ST Engineering |
| Page head overrides: `pageEyebrow:` / `pageTitle:` (when the section also heads its own page) | `overview.md`, `flights.md` | ST Engineering |
| Clips: `video:` + `poster:` on an item; a hero `video:` on a section; optional second take `videoAlt:` + `posterAlt:` with `altLabel:` (the toggle text, e.g. "Lights off") and a `credit:` line; `current: true` marks the active milestone | `content/programme/*.md`, files in `public/media/` | ST Engineering; CMU for its clips |
| News, a dated log, **one folder per partner**; `author:` names who wrote it, `draft: true` hides it; optional `gallery:` (photos with `alt:` and `caption:`) and `link:` / `linkLabel:` (paper, poster, code) | `content/updates/<partner>/YYYY-MM-DD-slug.md` (`st`, `nus`, `upenn`, `cmu`), images in `content/updates/<partner>/images/` | That partner |
| Site title, footer, programme `start:` / `end:` (June 2026 – June 2029, "Year 1 of 3") | `content/site.yml` | ST Engineering |

- **The schema is the contract:** `src/content.config.ts` validates every file at build time. Add a
  field to the schema before using it. Never weaken a rule to make a broken file pass.
- **Layer ids are fixed:** `strategy`, `safety`, `flight`, `localisation`, `drones`, `integration`
  (layers 1 to 5 plus Integration across all; Localisation is layer 4, ST Engineering leads, CMU provides
  the simulator and technical advice). A partner's
  `work.<layer>` line (90 characters or fewer) is what puts that partner on a layer in both diagrams.
- **Sources:** the October 2026 monthly report (29 Oct 2026) is approved for publication by the
  site owner (3 Nov 2026): its simulation figures and numbers may go on the site, translated into
  the §2 wording, with proposals labelled as proposals and nothing under review. The D3 FR&PDR
  (July 2026) is confidential, and the localisation brief (22 Oct 2026) stays context only: nothing
  numeric or unpublished from those two goes on the site.
  **Update, 3 Nov 2026:** the site owner approved publishing selected content from the July FR&PDR
  and the localisation brief. The exclusions still hold: no budgets, prices or cost ceilings; no
  contract or deliverable IDs; no classification markings; nothing about the physical-contact scenario
  and no kinetic wording; no names beyond the three PIs already on the site; no papers under review.
  Every adversarial term is translated per §2, and targets and pass marks stay labelled as targets.
  People: only those named on the site (`people:` lists). Round 3 added CMU's three extra flight clips
  and the Starling photo, taken from CMU's public `svg-website` repo with CMU's consent, credited
  "Photo: <lab>." or "Video: <lab>." (e.g. "Photo: CMU AirLab." in `flights.md`). That repo is never edited.
  Extracted text lives outside the repo, in `~/Documents/GitHub/Strike-Versus-Guard-sources/` on Jeremy's laptop.
- **Sources added in round 5 (3 Nov 2026):** the IROS 2026 posts and posters come from the trip and
  the partners' own papers. The **A0 programme poster is published top half only**: the lower half has
  wording the site avoids (§2). UPenn's STL-SVPIO paper is cited as IROS 2026 (Jeremy). The NUS
  workshop paper was not found publicly, so NUS shows "None yet" until it supplies it. "Derek" (ST) is
  listed without surname or role until he confirms them.
- Images must be referenced **relative to the content file** (`./NUS/photo.jpg`), never as `/images/...`.
- **Size limits:** images 5 MB or less and clips 8 MB or less (H.264 MP4, muted, with a `.jpg`
  poster). Both are enforced by `npm run check`.

---

## 5. Page structure (current)

Nav: **Updates · Research · Partners ▾ · Flights · Publications · Contribute**, then the sun/moon
theme toggle. There is no Benchmark item; the game stays on the Research page. `/programme/` is a
redirect to `/research/` (an `#anchor` is not carried over). Moved addresses are `redirects:` in
`astro.config.mjs`, never redirect pages under `src/pages/`.

**Partners menu:** "Partners" stays a link. The ▾ button opens a panel on hover (120 ms open, 300 ms
close grace), click, or Enter/Space. Escape closes it and returns focus; ArrowDown enters the rows;
it closes on focus-out. Without JS it is just the link. Heading: "Each partner has its own page". Rows:
ST Engineering · NEAR Lab, NUS · MARMoT Lab, UPenn · xLab, CMU · AirLab (logo chip, name,
contribution line), then "Funded by HTX" (→ `/partners/#funder`) and "All partners: who does what →".
On phones the panel opens full width under the header.

**Home (`src/pages/index.astro`), top to bottom:**

| # | Section | What it holds |
|---|---|---|
| 1 | Hero | Title above a rounded 2:1 clip panel (best CMU clip, full resolution, poster still, pause button; reduced motion shows the still) |
| 2 | Logo row | ST, NUS, UPenn, CMU, then "Funded by HTX" |
| 3 | At a glance + Latest | Status lines from `glance.md` (grouped by `state:`) beside a rail of the 5 latest posts |
| 4 | Partner cards | "Partner page →" and, when the partner has posted, "Latest update · <date>" |
| 5 | Research themes | Five rows from `themes.md` |
| 6 | Interactive drone | Full explain mode, partner names in the callouts (effects below) |
| 7 | Flights | Lead clip + 3 |
| 8 | Publications | Teaser of the Publications page |
| 9 | People | Team photo and names, then the footer (colour logo strip, "Four labs, in Singapore, Pittsburgh and Philadelphia. Funded by HTX.") |

**Interactive drone effects:** selecting a part lights it and shows its name (two-way peek with the
connection diagram); leader lines draw on scroll-in; flight dots march while Flight is lit; the
Strategy layer pulses; **ring drift only while Safety is lit**; **no count-ins and no scan sweeps**.
All stop under `prefers-reduced-motion`.

**Research (`/research/`, was Programme):** positioning statement, the two tracks, "How a command
travels" (`command.md`), "We try it in simulation first" (`simulation.md`, with "What we haven't
solved yet"), localisation (three questions, the plan as targets, a figure, `open:`), and directions
as 3 lines. Each theme has an anchor (`#learning`, `#formal`, `#safety`, `#localisation`,
`#simulation`). The 0.081 m figure appears only in Localisation and the October post. Type is larger
and standardised (h2 step-4, body step-1).

**Partners (`/partners/`, h1 "Who does what"):** "Each partner writes and maintains its own page.";
fully clickable partner cards; the HTX card (`id="funder"`); **"Principal investigators"**: one entry per
partner from the person marked `lead: true` with a `bio:` (photo, name linked to the partner page,
`role`, bio, "Profile →"); then the **connection diagram only** (the drone moved to home).

**Partner page (`src/pages/partners/[id].astro`):**
- Top line: "This is NUS's own file · Edit". Header and meta card; "Maintained by <Short> · updated
  <date> · Edit this page" sits in "At a glance".
- People: a row with faces from `people:` (the lead first, tagged "PI"; the meta box says "Principal
  investigator"). The word "Lead" is not used for people.
- "About the lab": `labBlurb:` on the left, the bios of people with `bio:` (lead first, face, role,
  "Profile →") on the right. Skipped when both are empty. Home and cards stay as they are.
- "In the system": `DroneDiagram` in `partner` mode, with that partner's layers lit.
- The Markdown body, in first person with the partner's own headings. It may embed simulation clips as
  `<figure class="clip">` (see CONTRIBUTING §4) and has an "In simulation" section.
- "Updates from <Short>" (always shown; empty reads "No posts yet. Post one →").
- Publications (if any). No chip row to the other partners: the header menu does that.

**Flights (`/flights/`):** the CMU cage photo (credit line), a lead clip at full width and the other
clips in a grid, each with a mono stamp line and a "Watch …" cue; CMU's outdoor clip (`outdoor.md`);
the test ladder M1–M6 (`ladder.md`; **M6, the first Starling flight in Singapore, is done**) with the
annotated Singapore lab photo; the localisation status line; milestones. (No open list on Flights
since 4 Nov 2026.)

**Publications (`/publications/`):** every partner's `publications:`, one section per partner (anchor
= partner id), in partner order. A partner with none shows "None yet (as of <date>)".

**Contribute (`/contribute/`):** "Which file is mine?" table, then add a person or photo, post an
update, add a publication, and a link to CONTRIBUTING.md for the rest.

**Updates (`/updates/`):** a dated log with a partner filter; each post shows its `author:`, its
`gallery:` as a photo strip and its optional `link:`. Posts are `updates/[...id]` (the id includes
the partner folder; the build fails if a post's `partner:` differs from its folder). The two posts that
moved into `updates/st/` keep their old addresses as redirects.

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
- **Tooling in the repo:** `npm run check` (build, schema, links, size budget) and `npm run shots`
  (`scripts/shots.mjs`: one page in real Chrome, reports overflow, console errors and failed
  requests, PNG in `.shots/`). Claude sessions follow `docs/claude/PROCESS.md` and the
  `.claude/skills/svg-*` skills.

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
- Before every push, `npm run check` must pass locally. The git hooks in `.githooks/` (installed
  by `npm ci`) run it and refuse pushes to `main`, to a new branch, or that delete a branch;
  `push.default=current` so a plain `git push` goes to the branch you are on.
- GitHub rulesets: `main` accepts only merged pull requests whose "Build and check" passed, with a
  merge commit; no branch other than `development` and `main` can be created.
- Claude may push to `development`. `main` changes only by merging the pull request, and only when
  the site owner says so in that conversation (`svg-release` skill; the `SVG_ALLOW_MAIN=1` prefix is
  the record of that approval).

---

## 8. Definition of done for any change

- [ ] `npm run check` passes (schema, build, internal links, size budget).
- [ ] `npm run shots -- /<page>/` at 1280 light, 1280 dark and 390 wide, each `"ok": true`
      (no overflow, no console errors, no failed requests), and the PNGs looked at.
- [ ] Wording follows §2; colours and fonts follow §3 (checked in light **and** dark); the partner order is correct.
- [ ] Interactive parts tested by mouse **and** keyboard.
- [ ] Docs updated if the structure or workflow changed (`README.md`, `CONTRIBUTING.md`,
      `docs/design-decisions.md`, this file); decisions and open items in `docs/claude/HANDOFF.md`.
- [ ] Pushed to `development`; the test site checked after the deploy finishes.

---

## 9. Media

Applies to every clip in `public/media/`. `npm run check` enforces the caps.

| Class | Encoding | Limit |
|---|---|---|
| All | H.264 High, yuv420p, 30 fps, `-g 60`, `-movflags +faststart`, no audio | none |
| Hero loop | cropped, CRF 23 | 15 s or less, 1 MB or less |
| Lead clip | 1080p, CRF 26 | 8 MB or less |
| Grid clip | 720p, CRF 28 to 30 | 8 MB or less |
| Poster | jpg | 100 KB or less |

- Caps: 8 MB per file; 60 MB for all of `public/media` together.
- `preload`: hero `none` and started by JS; lead `metadata`; grid `none`. Pause a clip when it is
  off-screen. With reduced motion, show the poster only.
- Keep CMU's on-video overlay (status card, "CORRECTING drone N") in every clip except the cropped
  hero loop. The hero crop must not cut the status card if the overlay is kept (§3).
- **Lit and lights-off are separate runs.** Never splice them; label each clip so.
- Credit line in the caption: "Video: AirLab, Carnegie Mellon University, CC BY-SA 4.0; re-encoded[ and
  cropped]." CMU's site licence is CC BY-SA 4.0; derived files must say they were changed.
- Hand-flown drones: never "striker", "intruder", "pilot" or "operator". Say "the filter does not
  steer the hand-flown drone".
