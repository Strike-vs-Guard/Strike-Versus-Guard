# Site restructure: dark default, five layers, shorter home page

Date: 3 Nov 2026. Status: **approved by Jeremy 3 Nov 2026; building.**
Source of truth for rules: `STANDARDS.md`. This document changes §3 (theme) and §5 (page structure)
when approved.

## 0. Where the repo stands

- `development` is already fully merged into `main` (PR #5, commit 5281d94). There is nothing to
  merge. The live site is the dev site.
- Leftover branches still exist (`claude/brave-bell-onicwy`, `gh-pages`, two `dependabot/*`).
  Only Jeremy can delete them (HANDOFF §5).
- Node is not installed on this laptop. Step 0 of the build installs Node 24 with nvm (user-level,
  no sudo). Headless Chrome is available for screenshots.
- The two Word documents and the FR&PDR deck, which the previous session never received, have now
  been read. Their extracted text and summaries are kept **outside the repo** (they are confidential
  HTX deliverables) in `~/Documents/GitHub/Strike-Versus-Guard-sources/`. Every claim in §7 is
  checked against those files; nothing from them is committed.

## 1. Intent

Jeremy's eight asks, in his order, and what each becomes:

| # | Ask | What changes |
|---|---|---|
| 1 | Page black by default | Dark theme is the default. Light stays available through a small toggle. |
| 2 | Weird gap between the hero title and the picture | Photo top-aligns with the title block and fills its column; the column gap shrinks. |
| 3 | "make decisions on their own" is not clear | A concrete line under the positioning statement says *which* decisions. |
| 4 | New Layer 4 with ST Engineering and CMU; Drones becomes Layer 5 | Layer 4 **Localisation**: each drone works out where it and its teammates are, proven in simulation first, then on real drones. |
| 5 | Connection diagram columns are not proportionate | Both columns span the same height; six layer cards (5 + Integration) match four partner cards. |
| 6 | Rearrange content; team photo at the bottom | Home page reordered; team photo is the last thing before the footer. |
| 7 | Page too long; split into pages | Four pages: Home (short), Programme, Partners, Flights. Updates stays. |
| 8 | Use the reports | New public-safe content: localisation, the 2 Oct 2026 flights, an October progress update. |

## 2. Goals, non-goals, anti-goals

**Goals:** a home page that fits in about four screens at 1280 px; every layer of the system
visible with its owners; dark by default; new results from the October report on the site.

**Non-goals:** no new colours or fonts; no change to the partner-file editing model; no change to
the two-branch publishing; no React or UI framework.

**Anti-goals (would make it a failure even if it builds):**
- Any counter-UAS, defence, intruder, attacker or defender wording (STANDARDS §2). The reports use
  these words throughout; none of them come across.
- Publishing anything from the FR&PDR, which is marked CO-CONFIDENTIAL, beyond what the poster and
  the live site already show. See §9.
- Targets presented as results. Pass marks, budgets and "done when" lines from the localisation
  brief stay off the site.
- "under mocap" wording for HTX readers; say "camera-only flight test" (per Jeremy's rule).

## 3. Theme (ask 1) — decided 3 Nov: pure black, no toggle

- `:root` carries one dark theme only. `--bg` becomes `#000000`; `--surface`, `--border`, `--grid`
  and `--zone` are re-tuned so cards and the dot grid still read against pure black (surface about
  `#111417`, border about `#262b31`). Text, muted, team and accent tokens stay as the current dark
  values. The `prefers-color-scheme` block and the light token set are removed, and the
  `color-scheme` is `dark`.
- The preview banner (yellow) is restyled to the dark palette.
- Logos keep their white wells (STANDARDS §3).
- STANDARDS §3 token table loses its Light column; "The theme follows the system setting" becomes
  "One theme: pure black background. There is no light mode."
- Screenshot checks drop "1280 light"; the definition of done becomes 1280 dark and 390.

## 4. Hero (asks 2 and 3)

**The gap.** At 1280 px the text column is 568 px wide and the photo is vertically centred against
a taller text block, so empty space sits above and below the photo and the 56 px gutter reads as a
hole. Fix: `align-items: start`, photo top aligned with the wordmark, aspect ratio 4/3 so the photo
ends level with the buttons, gutter 40 px. Verified by screenshot at 1280 and 1440.

**The decisions.** The positioning statement stays word for word (STANDARDS §1). Directly under it,
a short mono-label strip titled "What they decide" with three lines drawn from the benchmark's four
abilities and the October report:

> Which drone goes where. When to change the team's plan, because the other side has changed
> theirs or a teammate has dropped out. How the rest cover for a drone that is lost. A safety
> layer checks every command before it reaches a drone.

Approved by Jeremy 3 Nov ("they can adapt their strategies based on the situation, e.g. one drone
dead"). It lives in `content/programme/overview.md` as a new `decisions:` list so it is editable.

## 5. Layer 4: Localisation (asks 4 and 5)

### 5.1 Content

`content/programme/stack.md` gets six items in this order:

| Label | Title | Text (draft) |
|---|---|---|
| Layer 1 | Strategy | Team skills decide what each drone does. Learned by practice or written as rules. |
| Layer 2 | Safety | Checks every command and blocks any that would cause a collision. |
| Layer 3 | Flight | AirStack turns the team's plan into each drone's flight. |
| **Layer 4** | **Localisation** | Each drone works out where it is and where its teammates are, with its own camera and no motion capture or GPS. Proven in simulation first, then on real drones. |
| Layer 5 | Drones | Starling 2 Max quadcopters, flown in Pittsburgh and Singapore. |
| Across all layers | Integration | Joins layers 1–5 into one system and tests it on real drones. |

Section title becomes "Five layers, four partners, one team".

Name: **Localisation** (British spelling, matches the brief's own title). Alternatives considered
and dropped: "Positioning" (reads as marketing), "Swarm localisation" ("swarm" is banned in §2),
"Simulation" (simulation is a method used by every layer, not a layer).

Partner `work:` lines (max 90 characters):
- ST Engineering, `localisation`: "Leads camera-based localisation: proven in simulation first, then on Starlings."
- CMU, `localisation`: "Provides the AirStack simulator and technical advice from its flight experience."

Confirmed by Jeremy 3 Nov: ST Engineering leads; CMU supplies the simulator and technical advice
drawn from its experience.

### 5.2 Code

- `src/content.config.ts`: `LAYERS` gains `'localisation'` between `flight` and `drones`; the
  `work` schema gains the field.
- `src/lib/system.ts`: `LAYER_IDS` likewise.
- `src/pages/partners/[id].astro`: `layerNames` gains Localisation.
- `src/components/DroneDiagram.astro`: a fifth drawing group and marker.
  - Marker order top to bottom must stay 1 → 5 so leader lines never cross: 1 Strategy (y 72),
    2 Safety (y 237), 3 Flight (y 297), **4 Localisation (y about 350)**, 5 Drones (y 404).
  - Localisation drawing: the front sensor bar of the main airframe with a short dashed
    field-of-view wedge and a small "where am I" position cross beneath it. Label "own camera".
  - Hit area, ARIA description, partner-mode dimming and the `pd-co--localisation` callout follow
    the existing pattern. Marker 4's leader line must not cross the "AirStack: plan → flight" label
    (HANDOFF already lists that label as a known tight spot; this pass fixes it).
- `src/components/ConnectionDiagram.astro`: nothing content-wise (it reads the layers). Layout fix
  for ask 5: `.pc-layers` gets `justify-content: space-between` and each layer card a
  `min-height` so the six cards span the same height as the four partner cards; partner cards show
  the two logos side by side instead of stacked, which cuts their height by about a third. The
  connector lines are recomputed on resize already.

## 6. Pages (asks 6 and 7)

| Page | Path | Content, top to bottom |
|---|---|---|
| Home | `/` | Hero + decisions strip + facts row · Benchmark (arena) · How it fits together: drone diagram only (§6.1) · Flights so far: the four clips as one compact row, "All flights →" · Milestones strip · Latest updates (3) · **Team photo, full width, with "Funded by HTX"** |
| Programme | `/programme/` | Intro (positioning statement) · Two tracks, one stack · **Localisation** (new, §7.1) · Research directions and applications |
| Partners | `/partners/` | "Five layers, four partners, one team" · Four partner cards (ST, NUS, UPenn, CMU) + HTX funder card · Connection diagram · Proof so far (the three steps: Crazyflie → Starling at CMU → Singapore lab) |
| Flights | `/flights/` | The 2 Oct 2026 flight day at CMU (§7.2) with the same four clips, larger · Camera-only localisation in simulation (one number, no figure exists) · What's next (from milestones) |
| Updates | `/updates/` | unchanged, plus one new post (§7.3) |
| Partner pages | `/partners/<id>/` | unchanged layout; drone shows five layers; "Results so far" refreshed from the October report (§7.4) |

Nav: Programme · Benchmark · Partners · Flights · Updates. Benchmark keeps pointing at the home
page anchor because the arena is the site's signature visual and stays on the home page.
"Partners" and "Flights" become real pages. Footer links gain Programme and Flights.

Home page length target: about 4 screens at 1280 × 900 (today it is about 7).

Each new page is one Astro file that reads the same `content/programme/*.md` files. Nothing moves
in `content/`, so partners' editing instructions in CONTRIBUTING stay true. The one new content
file is `content/programme/localisation.md`. `flights.md` keeps its four `items:` (both pages read
them); its body text is rewritten for the Flights page and the home page shows only the title,
the clips and the one-line `note:`.

### 6.1 What a click on the home-page drone does

Today a click scrolls to the connection diagram and selects the layer there. The connection
diagram moves to `/partners/`, so on the home page a click lights the layer and its callout
locally (same as now, minus the scroll), and the callout's cue changes from "Show partners ↓" to
"Who works on it →", a link to `/partners/#layer-<id>`. The connection diagram reads that hash on
load and selects the layer. Partner mode on partner pages is unchanged.

## 7. New content from the reports (ask 8) — decided 3 Nov: reports are context only

Sources read: the localisation brief (22 Oct 2026), the 5-slide localisation deck, the October
monthly report (MR-001, 29 Oct 2026), the D3 FR&PDR deck and report (July 2026), the A0 poster.

**Rule (Jeremy, 3 Nov):** nothing confidential is published. The reports are used only to make the
site's own descriptions accurate. Published facts stay within what the poster and the live site
already show, plus the existence and shape of the localisation work. Specifically **not**
published: any number from the reports (accuracy, trajectory lengths, win rates, training counts,
RTK precision), paper submissions under review, budgets, hardware vendors, pass marks, dates beyond
the three-year milestones, and anything about the other team's drones.

### 7.1 Localisation (Programme page)

Public-safe draft, three short paragraphs:

- **Why.** Today the drone teams fly with motion capture indoors. The programme's third year is
  flight without motion capture or GPS, so each drone must know where it is on its own.
- **How.** Each drone carries a camera and a motion sensor and estimates its own position; teammates
  share only their position and heading so the team keeps one picture. Only a drone's own estimate
  steers it, so a bad message from a teammate can never crash a drone.
- **Status.** Simulation first: the Starling 2 Max now flies in the AirStack simulator, and
  camera-only localisation is being tested there before it goes on a real drone. Real-drone tests
  follow one step behind, in the Singapore lab.

No numbers. The brief's sensor plans (UWB, LiDAR), pass marks and anything about the other team
stay off the site.

### 7.2 Flights page

The October 2026 flight day at CMU's flight cage, three Starling 2 Max, safety filter on
throughout, four scenarios matching the four existing clips: formation change, separate goals,
figure-8 with a hand-flown drone cutting across, and a hand-flown drone pushed at the boundary.
Plus: the NUS policy went from simulation to Crazyflies to three Starlings in the same visit (the
live site already says this). No percentages or measurements.

### 7.3 Update post: "October 2026: what moved"

One post, partner `st`, four bullets, no numbers: the Starling 2 Max now flies in the AirStack
simulator; camera-only localisation has started, simulation first; CMU's October flight day with
three Starlings; the site now has five layers and four pages. Paper submissions and conference plans
are left out until they are public.

### 7.4 Partner page refreshes ("Results so far")

- **CMU:** the October flight day (already shown by the clips) and its localisation `work:` line.
- **NUS:** no change (its results text already matches the poster).
- **UPenn:** no change beyond the existing placeholder, which still needs UPenn's own words.
- **ST Engineering:** add the simulator and localisation work, without numbers.

Every line is checked against the §2 wording table before it lands.

## 8. Build order and who does it

Fable orchestrates and reviews; Opus or Sonnet agents execute. One agent per work package, briefed
per `docs/claude/AGENTS_AND_SKILLS.md`.

| Step | Work package | Files | Agent | Depends on |
|---|---|---|---|---|
| 0 | Node 24 via nvm, `npm ci`, Playwright using the installed Chrome | none in repo | me | — |
| 1 | Theme: pure black, single theme | `global.css`, `Base.astro`, `DroneDiagram.astro` theme block, STANDARDS §3 | Sonnet | 0 |
| 2 | Hero gap + decisions strip | `overview.md`, `content.config.ts`, `index.astro` | Sonnet | 0 |
| 3 | Layer 4 Localisation: schema, data, drone drawing, connection-diagram proportions | §5.2 files | Opus | 0 |
| 4 | Page split + nav + team photo at bottom | `index.astro`, new `programme.astro`, `partners/index.astro`, `flights.astro`, `Base.astro` | Opus | 2, 3 |
| 5 | Content: localisation section, flights story, update post, ST and CMU partner files | `localisation.md`, `flights.md`, update post, `ST.md`, `CMU.md` | Sonnet (writer) | runs in parallel with 1–4 |
| 6 | Verify: `npm run check`, screenshots 1280 and 390; keyboard pass on both diagrams; wording scan against §2; a "no numbers from the reports" scan | — | Sonnet | 1–5 |
| 7 | Review: code review of the diff; a newcomer-reader pass on the four pages | — | Opus | 6 |
| 8 | Docs: STANDARDS §3 §5, design-decisions, HANDOFF, jeremy.md, README nav | docs | Sonnet | 7 |
| 9 | Commit to `development`, push, Jeremy checks `/preview/`, then PR to `main` | — | me, then Jeremy | 8 |

Steps 1, 2, 3 and 5 run in parallel. A clickable draft of the dark home page and the five-layer
drone is shown to Jeremy after step 3 and before step 4, per the repo's "draft first" rule.

Estimated agent runs: 8 to 10.

## 9. Jeremy's answers (3 Nov 2026)

1. **Confidentiality:** nothing confidential is published; the reports are context only (§7).
2. **Layer 4:** Localisation, ST Engineering leads, CMU provides the simulator and technical advice.
3. **Theme:** pure black, no toggle (§3).
4. **Benchmark:** stays on the home page.
5. **The decisions line (§4):** approved; adapting the strategy to the situation (a lost drone) leads.

## 10. Calls I made (check these while reading)

- Partner-owned files (`NUS.md`, `UPenn.md`, `CMU.md`, `work:` lines) are edited in this same
  change and go in the one pull request. CODEOWNERS teams are still placeholders and the `main`
  ruleset is not set up, so nothing blocks it; partners review their pages afterwards, as they did
  for the first launch. If Jeremy wants partner sign-off first, step 5's partner edits become a
  second pull request.
- The localisation status is described in words only; no numbers and no figure.
- The four clips appear on both Home (compact row) and Flights (large, with the story). One
  content file feeds both.

- The team photo appears once, at the bottom of the home page, not on the Partners page.
- "Proof so far" moves to the Partners page, not Flights, because it is about the partners' hand-over.
- Nothing in the drone drawing is removed; the localisation group is added at the airframe's front.
- Partner `work:` lines for localisation are drafted for ST Engineering and CMU only.
- No `contact:` fields, people lists or publication lists are added; those stay with each partner.
