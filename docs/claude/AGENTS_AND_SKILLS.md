# Agents and skills used to build this site

This records every subagent and skill used, what it was for, and how to run it again. The reusable
agents also exist as Claude Code agent definitions in [`.claude/agents/`](../../.claude/agents/),
so in Claude Code you can call them by name (e.g. "use the svg-design-critic agent on the drone diagram").

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
| `.claude/agents/svg-implementer.md` | Implements an agreed spec in the Astro repo and verifies it with Playwright; doesn't commit | After a design decision is made |

Every agent brief included:
- the goal
- what the client already rejected
- the hard requirements from `STANDARDS.md`: partner order, both logos, "See more →", tokens only,
  no blue/red for partners, light/dark, 390px phones, no military tone
- the exact files to read and write
- how to render and verify
- a short report format

Keep doing that; an agent knows only what its brief says.

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
