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

---

## Review links (private claude.ai pages, owner: Jeremy)
- Partner picker draft (rejected layout): https://claude.ai/artifact/TbmrKo8Y2Z3RzRPnmLwE1w
- Four proposals A–D: https://claude.ai/artifact/EGWt5XGuHB5VdtvLGxF1jC
- Drone placements 1 / 2 / 3: https://claude.ai/artifact/VoZeujn85GU7RWEEKyKjFA
