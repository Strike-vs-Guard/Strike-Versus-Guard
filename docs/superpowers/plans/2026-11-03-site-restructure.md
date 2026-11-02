# Site restructure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Pure-black single theme, a fifth system layer (Localisation), a hero that explains what the drones decide, and the one long home page split into Home, Programme, Partners and Flights.

**Architecture:** Astro 7 static site; copy lives in `content/`, templates in `src/`. Home-page sections become small components under `src/components/sections/` so the new pages reuse them. The two diagrams read layers from `stack.md` and partner `work:` lines, so the new layer is mostly data plus one drawing group and one marker.

**Tech Stack:** Astro 7.4.4, Node 24 (installed at `~/.local/bin`; `export PATH=~/.local/bin:$PATH`), vanilla JS, Playwright (scratchpad only, channel `chrome`).

**Spec:** `docs/superpowers/specs/2026-11-03-site-restructure-design.md`

## Global Constraints

- Branch: all work on `development`; never create another branch (STANDARDS §7).
- Wording: STANDARDS §2 table. Never: intruder, attacker, defender, enemy, threat, swarm, counter-UAS, target, "under mocap". No number, date, paper status or vendor from the confidential reports (spec §7).
- Partner order everywhere: ST Engineering, NUS, UPenn, CMU. HTX is "Funded by".
- Tokens only; no new colours or fonts. `--guard` and `--strike` only for the game teams. `--accent` only in the wordmark, the hero rule and the "We are here" marker.
- Never hard-code the base path; use `url()` from `src/lib/url.ts`.
- Component CSS is scoped or globally prefixed (`.pd-*`, `.pc-*`); component JS finds its root via `document.currentScript.closest(...)`.
- Done for every task: `npm run check` passes, no console errors, no horizontal overflow at 390 px, keyboard works where the mouse works.
- Verification harness: `/tmp/claude-1000/-home-jeremychia/6357cc58-b2db-4b9b-93b6-b4eea2452f70/scratchpad/verify/shot.mjs` (Task 0) builds with `BASE_PATH=/`, serves `dist/` and screenshots a page at 1280 and 390, printing overflow width and console errors.

## Review Focus

1. A partner file with no `localisation:` line must still build and still render its drone with four or five lit layers as before (Task 3 test: build passes with NUS.md and UPenn.md untouched).
2. `/partners/#layer-localisation` opened cold must select that layer in the connection diagram, and an unknown hash must select nothing (Task 3 test).
3. The old anchors `#programme`, `#partners`, `#flights` linked from the hero buttons, the nav and partner pages must all still resolve on the new pages, and `npm run check` must find no broken internal link (Task 4 test).
4. At 390 px the "What they decide" strip, the five-callout drone and the six-row connection diagram must not overflow (Tasks 2, 3 tests).
5. With the light theme gone, the `track__fig` white panel, the logo wells and the preview banner must still be readable on pure black (Task 1 test: screenshot of `/` and `/preview/`-style banner at 1280).

---

### Task 0: Verification harness (orchestrator)

**Files:**
- Create (outside repo): `scratchpad/verify/package.json`, `scratchpad/verify/shot.mjs`

- [ ] **Step 1: `npm i playwright@latest` in `scratchpad/verify`** (no browser download; use `channel: 'chrome'`).
- [ ] **Step 2: Write `shot.mjs <path> <outPrefix>`**: starts `python3 -m http.server` on `dist/` (built with `BASE_PATH=/`), opens `http://127.0.0.1:<port><path>` at 1280×900 and 390×844, waits for fonts, prints `overflow=<scrollWidth-clientWidth>` and every console error, saves `<outPrefix>-1280.png` and `<outPrefix>-390.png` (full page).
- [ ] **Step 3: Run it on the current site**: Expected `overflow=0` on both widths, no console errors.

### Task 1: Pure-black single theme

**Files:**
- Modify: `src/styles/global.css:6-71` (tokens), `src/layouts/Base.astro:126-133` (preview banner), `src/pages/index.astro:449-451` (`.track__fig`), `STANDARDS.md` §3 and §8.
- Do **not** touch `DroneDiagram.astro` (Task 3 removes its colour-scheme block).

**Interfaces:** Produces the token set every other task renders against:
`--bg #000000`, `--surface #111417`, `--text #e6e8eb`, `--muted #9ba4af`, `--border #262b31`, `--grid #1f252b`, `--accent #ff4d5e`, `--guard #6fa3f5`, `--guard-tint rgba(111,163,245,.09)`, `--strike #f2766a`, `--zone rgba(155,164,175,.07)`, `--well #ffffff`, `--shadow none`, `color-scheme: dark`.

- [ ] **Step 1:** Replace the three token blocks in `global.css` (`:root`, the `prefers-color-scheme` block, `:root[data-theme='dark']`) with one `:root` block holding the values above. Update the file's header comment.
- [ ] **Step 2:** Preview banner in `Base.astro`: `background: var(--surface); color: var(--text); border-bottom: 1px solid var(--border)`; keep the text.
- [ ] **Step 3:** `.track__fig` in `index.astro`: keep `background: #fff` (the track figures are light PNGs and need a white well, same rule as logos) and add a comment saying so.
- [ ] **Step 4:** STANDARDS §3: drop the Light column, replace the values, replace "Both themes must be designed. The theme follows the system setting." with "One theme: pure black background. There is no light mode." §8: "1280px light, 1280px dark and 390px" → "1280px and 390px". Same line in `CLAUDE.md`.
- [ ] **Step 5: Verify:** `npm run check` passes; `shot.mjs / theme` → overflow 0, no errors; screenshot shows black page, readable cards, white logo wells, team-colour arena.
- [ ] **Step 6: Commit** `git commit -am "Switch to a single pure-black theme"`.

### Task 2: Hero gap and "What they decide"

**Files:**
- Modify: `content/programme/overview.md`, `src/content.config.ts` (programme schema), `src/pages/index.astro` (hero markup lines 41-72, hero CSS lines 299-345).

**Interfaces:** Produces `overview.data.decisionsLabel: string` and `overview.data.decisions: string[]` on the programme schema (`decisionsLabel: z.string().optional()`, `decisions: z.array(z.string()).default([])`).

- [ ] **Step 1:** Add to `overview.md` front matter:
  ```yaml
  decisionsLabel: What they decide
  decisions:
    - Which drone goes where.
    - When to change the team's plan, because the other side has changed theirs or a teammate has dropped out.
    - How the rest cover for a drone that is lost.
    - A safety layer checks every command before it reaches a drone.
  ```
- [ ] **Step 2:** Add the two schema fields to the `programme` collection.
- [ ] **Step 3:** In the hero, after `.hero__body` and before `.hero__actions`, render `<div class="hero__decide"><p class="eyebrow">{decisionsLabel}</p><ul>…one li per decision…</ul></div>`: a mono eyebrow, then the four lines as a plain list with a 1 px `var(--border)` left rule, `gap 6px`, body font `var(--step-0)`, text colour `var(--text)`.
- [ ] **Step 4:** Hero grid: `.hero__grid { align-items: start }`; `.hero__figure` gets `margin-top: 6px` so the photo top aligns with the wordmark cap line; `.hero__figure img { aspect-ratio: 4 / 3 }`; gap at ≥960 px `40px`. Buttons stay under the decisions.
- [ ] **Step 5: Verify:** `shot.mjs / hero` at 1280: photo top within 12 px of the wordmark top, photo bottom within 24 px of the buttons' bottom; 390: overflow 0.
- [ ] **Step 6: Commit** `"Explain what the drones decide; align the hero photo"`.

### Task 3: Layer 4 Localisation

**Files:**
- Modify: `src/content.config.ts` (`LAYERS`, `work` schema), `src/lib/system.ts` (`LAYER_IDS`), `content/programme/stack.md`, `content/partners/ST.md` and `CMU.md` (`work:` only), `src/pages/partners/[id].astro` (`layerNames`), `src/components/DroneDiagram.astro`, `src/components/ConnectionDiagram.astro`, `CONTRIBUTING.md` §1 layer list.

**Interfaces:**
- Produces layer id `'localisation'` in `LAYERS`/`LAYER_IDS` between `flight` and `drones`; `stack.md` items in the order Strategy, Safety, Flight, Localisation, Drones, Integration (exact copy in spec §5.1; title "Five layers, four partners, one team"; Integration text "Joins layers 1–5 into one system and tests it on real drones.").
- Produces `DroneDiagram` prop `partnersHref?: string`: in explain mode, when set, the callout cue reads "Who works on it →" and is a link to `${partnersHref}#layer-<id>`; `target`/`scrollTo` stay supported for pages that still have both diagrams.
- Produces `ConnectionDiagram` behaviour: on load, if `location.hash` is `#layer-<id>` and the id exists, select that layer and scroll it into view; else no selection.

- [ ] **Step 1: Data.** Add `'localisation'` to both constant arrays and the `work` schema; rewrite `stack.md` items; add the two `work.localisation` lines (ST: "Leads camera-based localisation: proven in simulation first, then on Starlings." CMU: "Provides the AirStack simulator and technical advice from its flight experience."); add Localisation to `layerNames`; add `localisation` to the CONTRIBUTING layer list.
- [ ] **Step 2: Verify data:** `npm run check` passes; the built `/partners/nus/` still lists the same layers for NUS (Review Focus 1).
- [ ] **Step 3: Drone drawing.** In `DroneDiagram.astro` add a group `<g class={`pd-g${on('localisation')}`} data-layer="localisation">` drawn at the main airframe's front sensor bar: a dashed field-of-view wedge (two lines from about (300,300) opening forward-down to about (250,372) and (350,372), `pd-link` dash style), a small position cross below it at about (300,386) (`pd-dim` style), and `<text class="pd-lbl pd-lbl-sm">own camera</text>`. Keep the drawing inside the existing viewBox. Move the existing "Starling 2 Max" label if the two collide.
- [ ] **Step 4: Markers.** Renumber: localisation marker `4` at about (300,350) → must sit strictly between the flight marker (y 297) and the drones marker, which becomes `5` and stays at (318,404). Adjust the drones marker to (250,404) if the leader line from marker 4 would cross the "AirStack: plan → flight" label; the rule is no crossing lines, markers top-to-bottom 1…5. Add a `pd-hit` rect for localisation (about x 240, y 330, w 120, h 60). Extend the ARIA `aria-label` on the SVG with "4, Localisation: the drone's own camera and a position fix beneath it." and renumber Drones to 5.
- [ ] **Step 5: Script.** `NUM` becomes `['strategy','safety','flight','localisation','drones']`; the Integration bracket still spans from `co('strategy')` to `co('drones')`. Add the `partnersHref` option: in `activate()`, when `OPTS.partnersHref` is set and `OPTS.target` is not, do no scrolling and dispatch no `sys:select`. Render the cue as `<a class="pd-cue" href=…>Who works on it <span class="pd-cue-a">→</span></a>` inside the button's label area is invalid HTML (a link inside a button), so render it as a sibling `<a>` after the button inside `.pd-item`, positioned top-right of the callout like the current cue, with an `aria-label="Who works on <title>"`.
- [ ] **Step 6: Remove** the `@media (prefers-color-scheme:dark)` block and the `:root[data-theme='dark']` lines at the bottom of `DroneDiagram.astro`; apply `.pd{--pd-blade:var(--muted)}` and hide `.pd-shadow` unconditionally (dark is the only theme).
- [ ] **Step 7: Connection diagram proportions.** `.pc .pc-layers{justify-content:space-between}` and `.pc .pc-lnode{flex:1 1 0;display:flex}` with `.pc .pc-lbtn{flex:1}` so six cards fill the partner column's height; partner cards: `.pc-well` shows the institution logo and lab logo side by side (`grid-template-columns:1fr 1fr`, height about 64 px) instead of stacked; `.pc-pbtn` grid `minmax(0,1fr) 150px`→ keep text column first. Target at 1280: partner column height and layer column height within 24 px of each other. `SPANS` text already derives "1–5".
- [ ] **Step 8: Hash selection.** At the end of the connection diagram IIFE: `var h = /^#layer-([a-z]+)$/.exec(location.hash); if (h && layerById[h[1]]) { sel = {t:'l', id:h[1]}; apply(false); announce(); root.querySelector('[data-sel="l:' + h[1] + '"]').scrollIntoView({block:'center'}); }`. Give each layer node `id="layer-<id>"`? No: the hash is consumed by script, so do **not** add matching ids (the browser would jump before layout). Verify an unknown hash selects nothing.
- [ ] **Step 9: Verify.** `npm run check`; `shot.mjs / layers` at 1280: five numbered callouts plus Integration, no leader line crosses the flight label (inspect screenshot), connection columns balanced; `shot.mjs /partners/st/ st` shows Localisation lit; keyboard: Tab to each callout, Enter lights it; 390: overflow 0.
- [ ] **Step 10: Commit** `"Add Layer 4 Localisation; Drones becomes Layer 5; balance the connection diagram"`.

### Task 4: Page split

**Files:**
- Create: `src/components/sections/Tracks.astro`, `Benchmark.astro`, `Layers.astro` (drone only), `Clips.astro`, `Progress.astro`, `Milestones.astro`, `Directions.astro`, `UpdatesTeaser.astro`, `TeamPhoto.astro`, `PartnerCards.astro`, `Localisation.astro`; `src/pages/programme.astro`, `src/pages/partners/index.astro`, `src/pages/flights.astro`.
- Modify: `src/pages/index.astro` (becomes a composition of sections), `src/layouts/Base.astro` (nav, footer links), `src/pages/partners/[id].astro` (breadcrumb link → `url('partners/')`), `src/lib/system.ts` unchanged.
- Depends on: Task 2 (hero), Task 3 (`partnersHref`), Task 5 (`localisation.md` exists; if not yet, `Localisation.astro` renders nothing when the entry is missing).

**Interfaces:** Each section component takes no props except where noted and reads its own `content/programme/<id>.md`; `Layers.astro` takes `partnersHref: string`; `UpdatesTeaser.astro` takes `limit = 3`; `TeamPhoto.astro` reads `stack.md`'s `image/imageAlt/caption` and renders the HTX "Funded by" well above the photo.

- [ ] **Step 1:** Cut each home section's markup and its scoped CSS from `index.astro` into the section components, unchanged, keeping section ids `programme`, `benchmark`, `partners`, `flights`, `milestones`, `directions`, `updates` on whichever page now holds them.
- [ ] **Step 2:** Pages, top to bottom (spec §6): Home = Hero, Benchmark, Layers(partnersHref=url('partners/')), Clips (compact row, note, "All flights →" to `url('flights/')`), Milestones, UpdatesTeaser, TeamPhoto. Programme = page head (eyebrow "Programme", positioning statement), Tracks, Localisation, Directions. Partners = page head ("Five layers, four partners, one team" + stack body text), PartnerCards (four cards: both logos in wells, lab, lead, contribution, "See more →"; HTX funder card), ConnectionDiagram, Progress. Flights = page head from `flights.md` (title + body), Clips (large, 2-up), Localisation status paragraph (`localisation.md` third paragraph via a `status` front-matter field, see Task 5), Milestones.
- [ ] **Step 3:** Nav in `Base.astro`: Programme → `url('programme/')`, Benchmark → `url('#benchmark')`, Partners → `url('partners/')`, Flights → `url('flights/')`, Updates unchanged; `aria-current` by path prefix. Footer links: add Programme and Flights. Hero buttons: "How it works" → `url('programme/')`, "Meet the partners" → `url('partners/')`.
- [ ] **Step 4:** Partner page breadcrumb `Partners` → `url('partners/')`.
- [ ] **Step 5: Verify:** `npm run check` (11 pages, no broken links); `shot.mjs` on `/`, `/programme/`, `/partners/`, `/flights/`: overflow 0, no errors; home full-page height at 1280 ≤ 4 × 900 px + 20 %; team photo is the last element before the footer; `grep -c` of each old section id across `dist` is exactly 1.
- [ ] **Step 6: Commit** `"Split the home page into Home, Programme, Partners and Flights; team photo last"`.

### Task 5: Content from the reports (context only)

**Files:**
- Create: `content/programme/localisation.md`, `content/updates/2026-11-03-october-progress.md`.
- Modify: `content/programme/flights.md` (body only), `content/partners/ST.md` (body "What we are working on" + "Results so far"), `content/partners/CMU.md` (body "Results so far": one sentence on the October flight day).
- Sources (read-only, never quoted with numbers): `~/Documents/GitHub/Strike-Versus-Guard-sources/*-SUMMARY.md`.

**Interfaces:** Produces `localisation.md` front matter `eyebrow: Localisation`, `title: Knowing where every drone is`, `order: 9`, `status: <one sentence used on the Flights page>`; body = the three paragraphs of spec §7.1 (Why / How / Status), no numbers. Schema: add `status: z.string().optional()` to the programme collection.

- [ ] **Step 1:** Write `localisation.md` and the schema field.
- [ ] **Step 2:** Rewrite `flights.md` body per spec §7.2 (October 2026, CMU flight cage, three Starling 2 Max, safety filter on throughout, the four scenarios, NUS policy from simulation to Crazyflies to Starlings in the same visit); keep `items:` and `note:`.
- [ ] **Step 3:** Update post per spec §7.3 (four bullets, no numbers, partner `st`, date 2026-11-03).
- [ ] **Step 4:** ST.md: add a "Simulation and localisation" bullet under "What we are working on" and one sentence under "Results so far" (Starling 2 Max flying in the AirStack simulator; camera-only localisation started there). CMU.md: one sentence naming the October flight day.
- [ ] **Step 5: Verify:** `npm run check`; wording scan: `grep -rniE "intruder|attacker|defender|enemy|threat|swarm|counter|target|mocap|under motion capture|[0-9]+(\.[0-9]+)? ?(m|%|Hz|cm)\b" content/programme/localisation.md content/programme/flights.md content/updates/2026-11-03-* content/partners/ST.md content/partners/CMU.md` returns only the pre-existing "20x20"-free lines (expected: no matches except existing ones in CMU.md/ST.md unchanged lines).
- [ ] **Step 6: Commit** `"Add localisation section, October flight story and progress update"`.

### Task 6: Verification pass

- [ ] **Step 1:** `npm run check` on the final tree.
- [ ] **Step 2:** `shot.mjs` on all four pages + `/partners/st/` + `/updates/` at 1280 and 390: overflow 0, no console errors; keep the PNGs in `scratchpad/verify/out/`.
- [ ] **Step 3:** Keyboard pass with Playwright: on `/`, Tab to the drone callouts, Enter on "Localisation" lights it; on `/partners/`, Tab to a partner, Enter selects, Escape clears; open `/partners/#layer-localisation` → the layer is `aria-pressed="true"`.
- [ ] **Step 4:** Wording scan over `content/` and `src/` for the §2 banned list; report any hit.
- [ ] **Step 5:** Home height at 1280 reported in screens of 900 px.

### Task 7: Review

- [ ] **Step 1:** `/code-review medium` on `git diff main...development`.
- [ ] **Step 2:** `panel-newcomer-reader` reads the four built pages (from `dist/`) and reports where it got lost.
- [ ] **Step 3:** Fix what is confirmed; re-run Task 6 steps 1-2.

### Task 8: Docs

**Files:** `STANDARDS.md` §4 §5, `docs/design-decisions.md` (Structure, Visual design), `docs/claude/HANDOFF.md` §4 §5 §7, `docs/claude/jeremy.md` (new dated section 10), `README.md` (layout tree, nav), `CONTRIBUTING.md` shared-files table (+ `localisation.md`, + the Flights/Programme/Partners pages).

- [ ] **Step 1:** Update each file to describe the four pages, five layers, single theme, the `decisions:` and `status:` fields, and the sources folder outside the repo.
- [ ] **Step 2:** Commit `"Docs: four pages, five layers, one theme"`.

### Task 9: Push and hand over (orchestrator)

- [ ] **Step 1:** `git push origin development`; tell Jeremy the test-site URL and what to look at; do not watch the deploy.
- [ ] **Step 2:** Jeremy merges `development` into `main` by pull request.
