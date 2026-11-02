# CLAUDE.md

Website for **Strike vs Guard**, a research programme on decentralised multi-drone autonomy
(HTX-funded; ST Engineering lead partner with NUS, UPenn and CMU). Astro 7 static site on GitHub Pages.

**Read before changing anything:**
1. `STANDARDS.md`: the rules (positioning and banned wording, partner order, design tokens, content
   model, branches, definition of done).
2. `docs/claude/HANDOFF.md`: the current state, open items and how this work is run.
3. `docs/claude/DEBUGGING.md`: the debugging process and the failures already solved.
4. `docs/claude/jeremy.md`: the conversation history and decisions.
5. `docs/claude/AGENTS_AND_SKILLS.md`: reusable agents in `.claude/agents/`.

**Key rules (short version):**
- **Positioning:** never frame the site as counter-UAS or defence. *Strike vs Guard* is the
  benchmark game.
- **Partners:** equals, in the order ST Engineering, NUS, UPenn, CMU. HTX is the funder.
- **Branches:** only `development` (edits; test site at `/preview/`) and `main` (live, via a PR from
  `development`). Never create other branches.
- **Paths:** copy lives in `content/`, never in templates. Never hard-code the base path; use `url()`.
- **Before pushing:** `npm run check`. For visual changes, Playwright screenshots at 1280 light,
  1280 dark and 390px with zero overflow and no console errors.
- **Visual work:** show Jeremy a clickable draft first, then build it into the site.

**Commands:** `npm ci` · `npm run dev` · `npm run check` · `npx astro preview`
