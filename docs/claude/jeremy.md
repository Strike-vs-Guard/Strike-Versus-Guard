# Conversation history: Strike vs Guard website (Jeremy × Claude)

A dated log of the working session that built this site, kept for debugging and continuity. Each entry
gives Jeremy's request (quoted where useful), what Claude did, and the outcome. Session date:
**2 Nov 2026**. All times are approximate and in order.

---

## 1. Kick-off: design the site
**Request:**
> "design a webpage for this project called strike versus guard. use subagents to discuss and decide
> on a suitable project webpage … easily edited by each of the partner universities, like example
> NUS.md, Upenn.md, CMU.md and ST.md … how can one edit the webpage, test it there before pushing …
> Do not frame it as a counter UAS"

The positioning statement was provided (now in `STANDARDS.md` §1). Attachments: the 10-minute deck
(.pptx) and the A0 poster (.pdf). Two Word documents were referenced by Windows path, which Claude
can't reach.

**Done:**
- Extracted the deck text, speaker notes, 45 images and 7 clips. The poster's text is outlined, so it
  was rendered and used visually.
- Ran 3 advisers in parallel (content and structure, technology and workflow, visual design). The lead
  reconciled them into the decisions in `docs/design-decisions.md`.
- **Astro pinned to 7.4.4:** first tried 5.18.2 for wider Node support, but `npm audit` showed
  advisories in every version up to 7.3.1.
- Built the site:
  - schema-validated content, one `.md` per partner, programme sections as Markdown
  - the animated "arena" for the benchmark, clips, milestones, directions, updates and partner pages
- Compressed the clips to 720p. Cropped the "Same red intruders" caption off the NUS figure.
- Wrote CONTRIBUTING, the admin setup, the CI, preview and deploy workflows, and CODEOWNERS.

## 2. Review CMU's site
**Request:**
> "read this webpage code for reference. do NOT edit this code just review how cmu did their webpage
> https://github.com/Strike-vs-Guard/svg-website"

**Done:**
- Cloned it read-only. Running its code was blocked by the sandbox, so it was reviewed by reading the
  source.
- **What it is:** a React/Vite technical project page plus Zensical docs for CMU's ground-control
  software.
- **Kept separate** from this site and linked from the CMU page.
- **Borrowed:** the size budget and the base path derived from the repo name.
- **Flagged:** its counter-UAS wording ("ground controller for counter-UAS flights", "airspace
  protection", "intruder").

## 3. Windows files and the Word documents
**Asked:** "are u able to access files in my windows files if i give u the file path". **Answer:** no;
the files have to be attached.

**Then:** "the two m word files are too big … there's videos inside". **Advice given:** export to
.txt/PDF, or unzip the .docx (`word/media`) to get the videos. **Status:** still not received.

## 4. Push to main; two-branch rule; GitHub settings
**"push it to the main branch please"**
- Fast-forwarded `main`. The deploy built the site onto `gh-pages`, but Pages was still serving the
  raw `main` branch.

**"why are there so many branches? there should only be two branches … main and development"**
- Redesigned the publishing: deploy with Pages' "GitHub Actions" source and build **both** branches
  into one publish (`main` at `/`, `development` at `/preview/`).
- Removed PR previews and Dependabot. Created `development`.
- Claude's session **cannot delete branches** (403), so Jeremy was asked to delete
  `claude/brave-bell-onicwy`, `gh-pages` and the two `dependabot/*` branches.

## 5. Partners, collaborators and equality
**"should i name it as partners or collaborators? all of us (im from ST) except HTX are actually equal"**
→ Recommended "Partners", with HTX shown separately as the funder.

**"technically we are the main contractor but we dont want to put them down"**
- ST became "**Lead partner**" (coordinates and integrates); the others are "**Partner**".
- "Four partners, one team"; HTX shown as "Funded by". The positioning statement was kept as written.

## 6. The "who does what" section: iterations
| Version | Feedback |
|---|---|
| Separate "Four layers" cards + partner cards | "fused … to allow the user to click into the relevant university's work" |
| Layers × partners **matrix** | "looks not really good because there are so many missing blanks" |
| **Layer bands** + hover highlight (Jeremy merged to main) | Fine, but later: "not very obvious that clicking the sch logos changes smtg" |
| **Stacked plates + partner picker + side panel** (Artifact draft) | Asked for "See more" instead of "See UPenn's page" and lab logos. Then: "i dont really like this layout, can u give me more proposals? Get a panel of ui ux webpage designers and coders" |
| **4 proposals** (A partner cards, B swimlane flow, C connection diagram, D annotated drone), compared on one tabbed Artifact page | "I like C, but i also like the annotated drone in D as it looks fking cool. maybe can we use it for something else? for C layer 4, please connect UPENN to it as well." |
| **3 placements for the drone** (Artifact draft) | "do 1 + 3" (the drone before the connection diagram on the home page, and on every partner page), and "get some agents to discuss how can this annotated drone be improve design visually wise" |

Requirements gathered along the way:
- Partner order **ST Engineering, NUS, UPenn, CMU**.
- Show **both institution and lab logos**.
- The onward link text is "**See more →**".
- UPenn also works on **Drones**. The wording is a placeholder: "Runs the formal-track strategy on the
  shared Starling 2 Max drones."

### Drone polish spec (from 3 critics, given to the implementer)
- **Layout:** one column of callouts **1 Strategy → 4 Drones, top to bottom**. Integration is a
  bracket "Spans layers 1–4". Markers are re-placed so their vertical order matches; there are no
  crossing leader lines. Only corner crop marks are drawn for the frame.
- **Drawing:**
  - ¾-view Starling airframe (deck, sensor bar, battery, legs, shadow)
  - weight on the airframe, not the props; tapered blades; consistent 0.4 ellipse ratio
  - ring with back and front arcs
- **Metaphors:**
  - Strategy is **peer-to-peer**: no central "brain" box; three drones linked in a dashed triangle
    with a small shared-plan glyph.
  - Safety has a teammate outside the ring and a "safe distance" dimension.
  - Flight shows dotted waypoints turning into a solid line, with a proper arrowhead and the label
    "AirStack: plan → flight".
- **Copy** (in `stack.md`):
  - Strategy: "Team skills decide what each drone does. Learned by practice or written as rules."
  - Safety: "Checks every command and blocks any that would cause a collision."
  - Flight: "AirStack turns the team's plan into each drone's flight."
  - Drones: "Starling 2 Max quadcopters, flown in Pittsburgh and Singapore."
  - Integration: "Joins layers 1–4 into one system and tests it on real drones."
  - Intro: "…with a safety layer between the team's decisions and the drones".
- **Interaction:**
  - One shared selection via `sys:select` CustomEvents, replacing the re-entrant `click()` glue (a
    real bug: mouse and keyboard ended in different states).
  - The page scrolls only if needed, clear of the sticky header, with focus moved to the selected
    layer and a one-off echo ring.
  - "Show partners ↓" cue; no hover lift.
  - Two-way hover peek between callouts and parts of the drawing; clickable parts on fine pointers only.
  - ARIA: buttons named by their title; unique ids per instance.
  - The ring drifts slowly, paused off-screen, on hover and under reduced motion.
- **Partner mode:**
  - Static list items, not buttons.
  - Lit layers show that partner's own `work` text with a solid border.
  - Unlit layers have a dashed border and full-contrast text; their drawing groups dim.
  - A visually hidden summary sentence.
- **Connection diagram:**
  - Layer cards drop the description ("Layer N · Title · N partners").
  - Integration moves after layer 4.
  - Glyphs echo the drone metaphors.

## 7. CI and deploy incidents (and fixes)
| When | What Jeremy saw | Cause | Fix |
|---|---|---|---|
| After the first push | Site not updated | Pages source was "Deploy from a branch" | Jeremy switched it to **GitHub Actions** |
| Development pushes | `Deploy site` failed at deploy (no log) | The `github-pages` environment only allows the default branch | Deploy runs via `workflow_run` after CI on development (executes on main's side) |
| Screenshot of a red Jekyll log, "ok something is wrong" | `pages build and deployment` failing on `.astro` | GitHub's built-in Jekyll job still active | The Pages source setting (shown with exact clicks) |
| "i merged. but the website didnt update..?" | `Deploy site` build failed | `.nvmrc` = `22` → the runner used 22.23.3, below Astro's minimum of 22.23.4 | `.nvmrc` = `24`; actions bumped to v5; pushed straight to main and development to stop failure emails |
| "this github failure thing is flooding my email" | (the failures above) | | Fixed the root cause; pointed to GitHub notification settings |
| — | Link checker flagged `"'"` | It was reading inline `<script>` strings | The checker now strips scripts first |

Jeremy's preferences learned:
- "i think you dont need to deploy, just build and push to the repo will do": build locally, push to
  `development`, and don't keep watching deploys.
- Show a visual draft first: "do a visual draft for me to see how it looks like in here".

## 8. Handoff request
> "do a claude handoff .md file … put down the agents and skills used and also the standards.md …
> list down in a .md file on how claude should debug code … also have a .md file that store this chat
> history for debugging (jeremy.md)"

**Files created:**
- `docs/claude/HANDOFF.md`
- `docs/claude/AGENTS_AND_SKILLS.md`
- `.claude/agents/*.md`
- `STANDARDS.md`
- `docs/claude/DEBUGGING.md`
- this file
- `CLAUDE.md`

## 9. Drone polish implemented
The implementer agent delivered the full spec in §6.
- **Changed files:** `DroneDiagram.astro` (rewritten), `ConnectionDiagram.astro`, `stack.md`,
  `index.astro`.
- **Checks:** `npm run check` passes; 25 interaction checks pass (click = Enter = Space; selecting NUS
  lights Strategy and Drones; Escape clears both); 0 overflow; no console errors.
- **Deviations it reported:**
  - Clicking a callout always selects; the selection is cleared from the connection diagram.
  - The small drawing labels are hidden on phones.
  - The airframe uses unscoped `pd-a-*` classes, because Chrome doesn't apply ancestor selectors
    inside `<use>` copies.

Committed to `development`.

## 10. Site restructure (3 Nov 2026)
> Asks: a pure-black theme, a shorter home page, a Localisation layer, and the programme split into pages.

**Answers (spec §9):** nothing confidential is published; layer 4 is Localisation (ST Engineering
leads, CMU provides the simulator and technical advice); pure black with no toggle; the benchmark
stays on Home; the "What they decide" line is approved.

**What was done:**
- Fable orchestrated. Sonnet and Opus agents did tasks 1 to 5 in parallel in one working tree, each
  owning separate files and committing only its own paths.
- Builds were serialised with `flock /tmp/svg-check.lock npm run check`. A scratchpad Playwright
  harness (`shot.mjs`, Chrome channel) screenshots 1280 and 390 and reports overflow and console errors.
- Node 24 is installed under `~/.local` on the laptop (no nvm).
- The reports were read for context only; their text sits in `~/Documents/GitHub/Strike-Versus-Guard-sources/`,
  outside the repo.

**Outcome:** four pages (Home, Programme, Partners, Flights) plus Updates, five layers, one theme.
Docs updated to match. Push to `development` and Jeremy's check come next, then the pull request to `main`.

## 11. Round 2: UX panel, wider layout (3 Nov 2026)
> After seeing the test site: "team photo at the bottom, no lone HTX block"; "home is still too long";
> "a Partners hover menu listing the universities and ST, with links to their pages"; "each uni edits
> its own .md" (already true, now visible); "footer logos in colour"; "use the full page width";
> "a panel of UI/UX experts, with references to top university and corporate labs"; "update code,
> standards and agent docs".

**What was done:**
- Three Opus agents (first screen, layout, navigation) reviewed the site and fetched theairlab.org,
  asl.ethz.ch, rpg.ifi.uzh.ch, tri.global, rai-inst.com, deepmind.google and bostondynamics.com.
- Jeremy saw a clickable draft with three switches
  (https://claude.ai/artifact/2WqQ9uFtSXEzsAdcsJhk6j) and chose A compact drone, B no Benchmark nav
  item, C clip hero ("follow your recommendation").
- Built per `docs/superpowers/specs/2026-11-03-home-redesign-design.md`: new nav and Partners menu,
  shorter home, 1320 px width, colour logos, team photo and logo strip last.
- Panel saved as three agents in `.claude/agents/`; STANDARDS §3, §4, §5, CONTRIBUTING and the other docs updated.

**Outcome:** home about 5 screens (from 6.5). Jeremy checks the test site, merges PR #6, and each partner
reviews its page.

## 12. Simulation work from the monthly report (3 Nov 2026)
> "Put in the simulation stuff from the monthly reports." Then: "Do not put in all the content; make
> something short, led by the visuals."

**What was done:** the October report's figures were mapped to their sections; four GIFs became
clips and one figure a still. Each partner page gained a short "In simulation" section (1–2 visuals,
2–3 sentences; CMU's and UPenn's are text only, as the report has no simulation figures for them).
The Programme page gained "Proven in simulation first" with three clips, and the localisation status
now carries the 0.081 m simulation number. Items that appear only in the FR&PDR were left out.

## 13. More from the FR&PDR and the localisation brief (3 Nov 2026)
> The programme lead approved selected content from the July FR&PDR and the localisation brief, with
> hard exclusions (budgets, IDs, markings, the contact scenario, extra names, papers under review).

**What was done:** Programme gained "How a command travels" (strategy → AirStack → safety filter → PX4,
drawn as boxes, as the deck slide is built from shapes) and a richer localisation section (three
question cards, the rule, a targets table, a simulation figure). Flights gained CMU outdoors and the
M1–M6 test ladder (as of July 2026). Each partner page gained July results with 1–2 visuals; figures
with banned words baked in were cropped or skipped.

## 14. Content from the reports, round 3 (3 Nov 2026)
> The programme lead approved publishing selected content from the October monthly report, then the
> July FR&PDR and the localisation brief: "there's no code involved".

**Exclusions that still hold:** budgets, prices, contract and deliverable IDs, the physical-contact
scenario and kinetic wording, people beyond those named on the site, work under review.

**What was done:**
- An "In simulation" section per partner, with clips made from the reports' GIFs.
- Programme: "We try it in simulation first" and "How a command travels".
- Flights: "Test ladder" (M1–M6, as of July 2026), an outdoor clip, and CMU's three extra clips and
  Starling photo. These came from CMU's public `svg-website` repo, used with CMU's consent and credited
  "Photo/Video: CMU AirLab". That repo was only read.

## 15. Humanising, round 4 (3 Nov 2026)
> The site read as machine-written.

A three-reviewer panel (editor, art director, outside professor; ad-hoc, brief in
`AGENTS_AND_SKILLS.md`) found: no names, no dates, nothing went wrong, tidy triads.

**What was done:**
- `people:` per partner, shown as a row with faces; the team photo caption names everyone left to right.
- Slogans rewritten ("the game we test with", "Who builds which part", "We try it in simulation
  first"). The hero title is unchanged.
- Partner pages in first person, with their own headings.
- `open:`/`openLabel:` lists ("What we haven't solved yet") on Localisation, Simulation and Flights.
- Updates as a dated log with `author:`. Footer note shortened.
- Research directions as a plain numbered list. The drone drawing lost its dot grid and corner marks.
- Flights: lead clip + grid with mono stamps and "watch" cues, plus an annotated Singapore lab photo.
- Logos sized by visual weight (`src/lib/logo.ts`): footer 2×2 partner wells with lab logos, card well
  104 px, partner-page well 128 px.
- STANDARDS §2 now holds the voice rules.

## 16. Round 5: lab feedback, light/dark, Research (3 Nov 2026)
> Nine points from the lab after they saw the test site, then "follow the panel" and picks from the
> draft (https://claude.ai/artifact/Kxx7DfmQ51Hv3EoeFyBgFj).

**What the lab asked for:** a light site (dark as a toggle), a bigger wordmark, updates first on home,
the Programme page called Research, publications, an easier way for partners to contribute, partner
pages that are obviously the partner's own, faces for every partner, and a drone that does something.

**What was done:**
- A three-lens panel (design system, content architecture, drone interaction) fed one draft; Jeremy
  chose from it. Spec: `docs/superpowers/specs/2026-11-03-v3-redesign-design.md`.
- Theme: light default, dark navy-black (not pure black), sun/moon toggle; Archivo 700 headlines;
  brand red/blue only as type, rules and bands; white logo wells with a 1 px border in light.
- Nav is Updates · Research · Partners ▾ · Flights · Publications · Contribute. `/programme/`
  redirects to `/research/`.
- Home: hero (title above a 2:1 clip panel), logo row, updates strip, glance + latest, partner cards,
  five research themes, interactive drone, flights, publications, people.
- Drone effects restored on home; rule: ring drift only while Safety is lit, no count-ins or scan sweeps.
  The Partners page keeps the connection diagram only.
- Content model: `content/updates/<partner>/` (with `gallery:`, `link:`), `publications:` per partner,
  `glance.md`, `themes.md`, site `start`/`end` (June 2026 – June 2029). STANDARDS §4 old updates path fixed.
- Content: people photos for all partners from the labs' profile pictures; IROS 2026 posts and
  posters; UPenn's STL-SVPIO paper; the A0 poster, top half only.
- Wording rule added (STANDARDS §2): research themes are named by content.

**Decisions on gaps:** the NUS workshop paper was not found publicly, so NUS shows none. "Derek" (ST)
is listed without surname or role. The full A0 poster waits for Jeremy.

**Outcome:** Jeremy checks the test site and merges PR #6; partners confirm people, roles and photos.

## 17. Round 6: media replacement (4 Nov 2026)
> Replace the flight videos with CMU's better clips.

**The asks:** use the clips from CMU's `svg-website` (commit 6167492, read-only clone), keep them light
enough for phones, and credit CMU under CC BY-SA 4.0.

**The panel:** producer (shot list, ffmpeg), science-comms (what each clip proves, captions, credit),
web-performance (ladder, budgets, licence); saved as `svg-media-panel-*`.

**The picks:** the encoding ladder and caps, `preload` rules and wording for hand-flown drones are in
STANDARDS §9. Lit and lights-off stay separate runs. CMU's overlay stays except in the cropped hero.

---

## Review links (private claude.ai pages, owner: Jeremy)
- Partner picker draft (rejected layout): https://claude.ai/artifact/TbmrKo8Y2Z3RzRPnmLwE1w
- Four proposals A–D: https://claude.ai/artifact/EGWt5XGuHB5VdtvLGxF1jC
- Drone placements 1 / 2 / 3: https://claude.ai/artifact/VoZeujn85GU7RWEEKyKjFA
