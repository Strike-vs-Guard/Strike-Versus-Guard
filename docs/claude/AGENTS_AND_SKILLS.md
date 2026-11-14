# Agents and skills used to build this site

This records every subagent and skill used, what it was for, and how to run it again. The reusable
agents also exist as Claude Code agent definitions in [`.claude/agents/`](../../.claude/agents/),
so in Claude Code you can call them by name (e.g. "use the svg-design-critic agent on the drone diagram").

---

## Skills (the standard process, in `.claude/skills/`)

Every Claude session, from any lab, runs the same steps. Full description: `PROCESS.md`.

| Skill | Use | What it enforces |
|---|---|---|
| `svg-start` | Start of every session | Read CLAUDE.md, STANDARDS §2/§4/§7/§8, HANDOFF §4/§5; on `development`; intent stated before editing |
| `svg-change` | Any edit | Content in `content/`, schema before field, `npm run check`, `npm run shots` ×3, docs row, commit by path, push to `development`, preview URL |
| `svg-debug` | Anything broken | DEBUGGING.md process; never loosen a check |
| `svg-post` | A partner's news post | Right folder, fields, wording, `draft: true` until approved |
| `svg-panel` | Layout or look | Three agents → reconcile → clickable draft → user picks → build |
| `svg-release` | Publish to the live site | PR from `development`; merge only on the owner's say-so with `SVG_ALLOW_MAIN=1`; deploy verified |
| `svg-clip` | An annotated flight clip | First frame checked by the owner → tracking and graphics agents in parallel → integrate → STANDARDS §9 "Annotated clips" checks → push to `development` |

Hooks (`.claude/settings.json`, `scripts/claude/guard.mjs`, `.githooks/`) and GitHub rulesets make
the branch rules mechanical; see `PROCESS.md`.

---

## How the work was organised

The same pattern was used every time: **brief several agents in parallel, each with a different
angle → the lead (main Claude session) reconciles their output into one decision → one implementer
builds it → the lead verifies before committing.** Agents never commit or push; the lead does.

| Phase | Agents (parallel) | Output | Decision taken |
|---|---|---|---|
| 1. Site concept | Content & IA adviser · Tech stack & workflow adviser · Visual design adviser | Three short proposals | Astro + GitHub Pages, one Markdown file per partner, "lab notebook" look (see `docs/design-decisions.md`) |
| 2. Reference review | (Lead, read-only) CMU's `Strike-vs-Guard/svg-website` | Review | Kept separate (technical docs vs programme site). Borrowed the size budget and repo-derived base path. Flagged CMU's counter-UAS wording. |
| 3. "Who does what" section | 4 designer-developers: **A** partner cards · **B** system-flow swimlanes · **C** connection diagram · **D** annotated drone | 4 working HTML drafts, compared in one tabbed page | Client chose **C**, and wanted **D** reused ("looks cool") |
| 4. Drone placement | (Lead) visual draft of 3 placements | Tabbed draft | Client chose **1 + 3**: drone before the connection diagram on the home page, and on every partner page |
| 5. Drone polish | 3 critics: **illustration craft** · **information design** · **interaction / motion / accessibility** | Prioritised critiques | Synthesised into one spec (stack order 1→4, peer-to-peer strategy metaphor, shared selection state, static partner mode, …) |
| 6. Implementation | 1 implementer | Code in `DroneDiagram.astro` / `ConnectionDiagram.astro` | Lead reviews screenshots and tests, then commits to `development` |

Rejected along the way, so don't propose these again without a new reason:
- A layers × partners **table** (too many empty cells).
- Layer "bands" with hover-only highlighting (not obviously interactive).
- A "stacked plates" picker with a side panel.

---

## Agent roster (reusable)

| Agent file | Role | Use when |
|---|---|---|
| `.claude/agents/svg-content-adviser.md` | Content & information architecture | Adding or reshaping sections, copy, the content model |
| `.claude/agents/svg-visual-designer.md` | Visual direction within the site tokens | New visual treatment, signature graphics |
| `.claude/agents/svg-proposal-designer.md` | Builds ONE self-contained, working HTML draft of a section in a given direction | Exploring several layouts side by side (run 3–4 in parallel, one direction each) |
| `.claude/agents/svg-design-critic.md` | Critiques a draft or component through one lens (illustration / information design / interaction & a11y) | Before polishing anything visual (run 3 in parallel, one lens each) |
| `.claude/agents/svg-ux-panel-first-screen.md` | UX panel: the first screen and the gist | Reviewing a page top (run with the other two panel agents) |
| `.claude/agents/svg-ux-panel-layout.md` | UX panel: page length, width, rhythm, media | Reviewing a page's spacing and length |
| `.claude/agents/svg-ux-panel-navigation.md` | UX panel: nav, findability, partner paths | Reviewing menus and how pages link |
| `.claude/agents/svg-humanise-panel-editor.md` | Humanising panel: voice and copy, AI tells, rewrites | Round-4-style copy review (run with the other two humanise agents) |
| `.claude/agents/svg-humanise-panel-art-director.md` | Humanising panel: visual template tells, hand-made moves, logo sizing | Same round |
| `.claude/agents/svg-humanise-panel-outsider.md` | Humanising panel: robotics professor's cold-read impression test | Same round |
| `.claude/agents/svg-redesign-panel-design-system.md` | Redesign panel: palette, light/dark, fonts, hero spec | Site-wide redesign (run with the other two redesign agents) |
| `.claude/agents/svg-redesign-panel-content-architecture.md` | Redesign panel: site map, updates-first, publications, cuts | Same round |
| `.claude/agents/svg-video-panel-tracking.md` | Video panel: per-drone tracks from a fixed camera, proved with plots and contact sheets | Any annotated clip (run with the graphics agent; `svg-clip`) |
| `.claude/agents/svg-video-panel-graphics.md` | Video panel: labels, insets, banner and captions that never hide a drone | Same clip, in parallel |
| `.claude/agents/svg-redesign-panel-drone-interaction.md` | Redesign panel: ranked drone effects, reduced-motion, HUD risk | Same round |
| `.claude/agents/svg-media-panel-producer.md` | Media panel: shot list and ffmpeg commands | Replacing or adding video (run with the other two media agents) |
| `.claude/agents/svg-media-panel-science-comms.md` | Media panel: what each clip proves, order, captions, credit | Same round |
| `.claude/agents/svg-media-panel-web-performance.md` | Media panel: encoding ladder, budgets, licence; runs test encodes | Same round |
| `.claude/agents/svg-implementer.md` | Implements an agreed spec in the Astro repo and verifies it with Playwright; doesn't commit | After a design decision is made |

## UX panel (added 3 Nov 2026)

Three read-only Opus agents review the live test site, each through one lens: **first screen**,
**layout**, **navigation**. They can fetch reference sites (theairlab.org, asl.ethz.ch,
rpg.ifi.uzh.ch, tri.global, rai-inst.com, deepmind.google, bostondynamics.com).

How to run:
1. Start all three in one message so they run in parallel. Give each the preview URL and where the
   screenshots are.
2. Each returns a ranked list in plain language, under about 550 words.
3. The lead reconciles: findings that two agents share come first; conflicts go to Jeremy.
4. Don't build yet. Show Jeremy a **draft with switches**.

Draft-with-switches pattern: publish one page with `publish_files` that shows the options as toggles
(here A drone size, B nav item, C hero media), plus a badge showing the page height in screens. Jeremy
flips the switches, picks, and the choice goes in the spec.

Every agent brief included:
- the goal
- what the client already rejected
- the hard requirements from `STANDARDS.md`: partner order, both logos, "See more →", tokens only,
  no blue/red for partners, light/dark, 390px phones, no military tone
- the exact files to read and write
- how to render and verify
- a short report format

Keep doing that; an agent knows only what its brief says.

## Humanising panel (round 4, 3 Nov 2026)

Three reviewers read the live test site, each through one lens. Now saved as the `svg-humanise-panel-*` agents.

| Reviewer | Lens: does the site sound like people made it? |
|---|---|
| Editor | Names, dates, first person. Is anything claimed without a person or a number? Tidy triads, filler, self-praising adjectives ("honest") |
| Art director | Looks machine-made: decoration without meaning (dot grids, corner marks), uniform grids, logo sizes, empty faces, captions that only label |
| Outside professor | Cold read as a visiting researcher: what went wrong, what is open, can I tell who did the work, would I trust it |

How to run: start all three in one message; give each the preview URL and the voice rules in
STANDARDS §2; ask for a ranked list under 550 words; the lead reconciles and shows Jeremy before
building. Findings that two share come first.

## Round-5 panel (3 Nov 2026)

Three reviewers, now saved as the `svg-redesign-panel-*` agents, read the test site after the lab's
nine-point feedback. Reuse this brief for a site-wide redesign.

| Reviewer | Lens |
|---|---|
| Design system | Tokens in light and dark, type scale, contrast, logo wells, what brand colour may colour, 390 px |
| Content architecture | Nav and page names, where each question is answered once, per-partner ownership, what a partner edits, empty states |
| Drone interaction | What the interactive drone does and why: each effect must explain a part or a layer; no decoration (no count-ins, no scan sweeps), reduced motion |

How to run: start all three in one message with the preview URL, STANDARDS §2/§3/§5 and the lab's
feedback; ask for a ranked list under 550 words; the lead reconciles into one draft (a private
claude.ai page) and Jeremy picks before anything is built. Result: the v3 spec.

### Draft-building harness used in phase 3
Proposal agents wrote **fragments** (one `<section class="PREFIX">` with scoped CSS and an IIFE
script). They used placeholders `{{DATA_JSON}}`, `{{LOGO_<id>}}` and `{{LAB_<id>}}`, which a small
`render.mjs` replaced. It then wrapped the fragment in a host page carrying the site tokens and
screenshotted it at 1280 light, 1280 dark and 390. A Python assembler put all fragments on one
tabbed comparison page. To recreate it, write:
- `data.json`: the layers and partners, as produced by `src/lib/system.ts`
- `host.html`: the token CSS from `src/styles/global.css`
- `render.mjs`: Playwright screenshots, logging overflow and errors

Use Python or a replacer function for the inlining: JS `String.replace` mangles `$$`.

## Media panel (round 6, 4 Nov 2026)

Three saved agents (`svg-media-panel-producer`, `-science-comms`, `-web-performance`) planned the
replacement of the flight videos with CMU's clips (commit 6167492). Rules that came out of it are in
STANDARDS §9.

## How a panel round runs

1. Three lenses run in parallel (one message), each with the preview URL, the relevant STANDARDS
   sections and the lab's asks.
2. The orchestrator reconciles: findings shared by two lenses first, conflicts to Jeremy.
3. Write one proposal.
4. When layout is at stake, publish a clickable draft with switches.
5. Jeremy picks.
6. Parallel implementers with disjoint file ownership; `npm run check` serialised with `flock`; each
   commits its own paths only.
7. Code review, then a fix wave.
8. Docs (handoff, history, standards).
9. Push to `development`.

---

## Skills and tools used

| Skill / tool | Used for |
|---|---|
| `anthropic-skills:pptx` / `markitdown` | Extracting text and speaker notes from the 10-minute deck |
| `pdftoppm` (poppler) | Rendering the A0 poster (its text is outlined, so it can't be extracted) |
| `ffmpeg` / Pillow | Compressing flight clips to 720p H.264, poster frames, resizing photos, trimming logos, cropping the "red intruders" caption off the NUS figure |
| `artifact-design` skill + **Artifact** tool | Publishing clickable review drafts (single draft, 4-proposal comparison, drone placements) as private claude.ai pages |
| **Agent** tool (`general-purpose`) | All advisers, designers, critics and the implementer above |
| **Playwright** + Chromium | Screenshots (light/dark/phone), overflow and console-error checks, mouse vs keyboard tests |
| GitHub MCP (`actions_list`, `get_job_logs`, `list_pull_requests`) | Reading CI/deploy runs and logs, checking PRs |
| `add_repo` (read-only) | Cloning CMU's `svg-website` for review |
| Astro `npm run check` | Schema validation + build + link/size check before every push |

Skills that were **not** needed: no UI framework, no CMS, no third-party hosting.
