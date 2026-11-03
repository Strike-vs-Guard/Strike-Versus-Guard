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
- **Theme:** light by default, dark navy-black with a header toggle; tokens in STANDARDS §3. Brand red/blue are type, rules and bands only; test both themes.
- **Nav:** Updates · Research · Partners ▾ · Flights · Publications · Contribute (STANDARDS §5). `/programme/` redirects to `/research/`.
- **Paths:** copy lives in `content/`, never in templates. Never hard-code the base path; use `url()`.
- **Before pushing:** `npm run check`. For visual changes, Playwright screenshots at 1280 and 390px,
  with zero overflow and no console errors.
- **Visual work:** show Jeremy a clickable draft first, then build it into the site. For page-level
  changes run the UX panel (`svg-ux-panel-*` agents) first; see `docs/claude/AGENTS_AND_SKILLS.md`.

**Commands:** `npm ci` · `npm run dev` · `npm run check` · `npx astro preview`
