---
name: svg-panel
description: Use before changing the layout, look or structure of any page on the Strike vs Guard website, or when the user asks "what should this look like". Runs a small panel of agents, reconciles, shows a draft, and builds only after the user picks.
---

# Panel, draft, pick, build

Layout and visual decisions are not made by one agent in one pass. The pattern that has worked
every time (`docs/claude/AGENTS_AND_SKILLS.md`):

## 1. Brief three agents in parallel, one lens each
Pick from `.claude/agents/` (or write a one-off brief in the same shape):

| Question | Agents |
|---|---|
| A page's top, length, navigation | `svg-ux-panel-first-screen`, `-layout`, `-navigation` |
| Does it read as human-made | `svg-humanise-panel-editor`, `-art-director`, `-outsider` |
| Site-wide look, fonts, hero | `svg-redesign-panel-design-system`, `-content-architecture`, `-drone-interaction` |
| Which clip or photo where | `svg-media-panel-producer`, `-science-comms`, `-web-performance` |
| Several layouts to compare | 3–4 × `svg-proposal-designer`, one direction each |

Every brief contains: the goal; what the user already rejected (HANDOFF §4, AGENTS_AND_SKILLS
"rejected"); the hard rules (STANDARDS §2 wording, §3 tokens, partner order, both themes, 390 px
phones, no defence tone); the exact files to read; the report format (ranked list, under 550 words).
Agents are read-only on the repo. They never commit.

## 2. Reconcile
Findings two agents share come first. Conflicts go to the user as a choice, not a verdict.
Write the decision in one short message with reasons.

## 3. Show a draft before building
A clickable page the user can open: one HTML file with switches for the options (A/B/C), published
as an artifact or served locally, plus a badge with the page height in screens. The user flips the
switches and picks. Do not build the site version first "to save time".

## 4. Build only what was picked
Then `svg-change` §3–§7. Record the pick and the rejected options in `docs/claude/HANDOFF.md` §4
so the next session does not propose them again, and in `docs/claude/jeremy.md` (one paragraph:
ask, panel, picks).
