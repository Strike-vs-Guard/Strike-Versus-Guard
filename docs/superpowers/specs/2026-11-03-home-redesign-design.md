# Home redesign after the UX panel (round 2)

Date: 3 Nov 2026. Status: **approved by Jeremy ("follow your recommendation"); building.**
Draft he approved: https://claude.ai/artifact/2WqQ9uFtSXEzsAdcsJhk6j (private). Round 1 spec:
`2026-11-03-site-restructure-design.md`.

## Panel findings (three reviewers, 3 Nov)
- First screen answered "what is this" twice and never said what the game is; the facts strip sat
  below the fold; the gist arrived 3.5 screens down.
- 36 % of a 1704 px screen was empty: content capped at 1160 px.
- Footer logos were greyscale; a lone "Funded by HTX" well sat above the team photo.
- Partner pages exist (one Markdown file each) but nothing on the site said so or led to them.
- Patterns borrowed: CMU AirLab (full-width hero footage, one sentence, two buttons); TRI and RAI
  Institute (home as a hub of short cards linking out); DeepMind, ETH ASL, UZH RPG (no home
  section repeats what a nav page covers in full).

## Decisions (Jeremy, 3 Nov)
A. Home "who does what" = **compact annotated drone** (drawing + six rows naming the partners), full
   explain-mode drone moves to the Partners page above the connection diagram.
B. Nav = **Programme · Partners ▾ · Flights · Updates** (Benchmark item dropped; the game stays on home).
C. Hero media = **muted looping flight clip** (`formation-change.mp4`), still photo as its poster and
   for reduced-motion users.
No further section cut (home lands at about 5 screens at 1280, from 6.5).

## Home page, top to bottom
1. Hero, 5/7 split: eyebrow, title, positioning statement word for word, one mono line
   "Strike vs Guard is the game we test with: the Guard team holds a zone, the Strike team tries to
   reach it." (`gameNote:` in overview.md), two buttons; right the clip + caption. Facts strip
   inside the first screen at 1280×900.
2. The game: Arena left; right the four steps, the "What they decide" list (moved here from the
   hero), the note "No pilot, no central controller, no scripted opponent."
3. Proof so far: one-line bar "Year 1 of 3 · 2026 to 2027 · We are here · Shared system and first
   teams" with a three-segment progress line (from milestones.md), the four clips 4-across with
   posters cropped to the flight footage, the honest note, "All flights →".
4. How it fits together: compact drone (≤0.8 screen), "Who works on each layer →" to `/partners/#who`.
5. Latest from the programme: cards fill the row, "All updates →".
6. Team photo (wide content width, rounded, caption with place and month), then the colour logo
   strip: "Funded by" HTX · divider · "Partners" ST Engineering, NUS, UPenn, CMU, equal white wells.
   The lone HTX block is deleted.

## Site-wide
- `--max` 1160 → 1320 px; `--gutter` clamp(16px, 4vw, 64px); `.section` padding
  clamp(64px, 8vw, 128px); `--border` #262b31 → #343b44; every photo/video gets a 1 px `--border`
  edge; text columns stay 68ch; Arena capped ~600 px, drone panel ~1200 px.
- Footer logos in colour (STANDARDS §3 rule "greyscale until hover" is withdrawn), grouped as above.
- Partners menu in the header: "Partners" stays a link; a ▾ button opens a panel on hover (120 ms
  open, 300 ms close grace), click, Enter/Space; Escape closes and refocuses; ArrowDown enters the
  rows; closes on focus-out; works without JS (link only). Rows: ST Engineering · NEAR Lab, NUS ·
  MARMot Lab, UPenn · xLab, CMU · AirLab (small logo chip + name + contribution line), divider,
  muted "Funded by HTX" → `/partners/#funder`, "All partners: who does what →". Phones: the ▾ opens
  the panel full width under the header.
- Partners page: intro line "Each partner writes and maintains its own page."; cards fully
  clickable, link text "<Short> page →"; full explain-mode drone above the connection diagram
  (the "1 + 3" pairing from round 1 moves here); HTX card gets `id="funder"`.
- Partner pages: "Maintained by <Short> · updated <date> · Edit this page" moves into the
  "At a glance" box; breadcrumb shows the institution; footer keeps the other-partners chips.
- Distinct page titles: Programme h1 "How the programme works"; Flights h1 "Flights so far"
  (eyebrow "Proof"); home flights section keeps "A team that flies itself" only on Flights, home uses
  "Proof so far" as the h2.
- Dot grid removed from the drone panel (kept on the Arena). Corner crop marks stay (Integration).

## Not changing
Positioning statement; the Arena; partner order; HTX as funder; pure-black theme; content model.

## Docs and agents
STANDARDS §3 §5, design-decisions, HANDOFF, jeremy.md, README, CONTRIBUTING; the three panel
reviewers saved as `.claude/agents/svg-ux-panel-{first-screen,layout,navigation}.md` and listed in
`docs/claude/AGENTS_AND_SKILLS.md`.
