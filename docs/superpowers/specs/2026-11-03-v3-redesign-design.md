# v3 redesign: light/dark, updates first, lab feedback (round 5)

Date: 3 Nov 2026. Status: **approved by Jeremy (draft https://claude.ai/artifact/Kxx7DfmQ51Hv3EoeFyBgFj); building.**
Lab feedback (9 points) + panel (design system / content architecture / drone interaction) → draft v3 → Jeremy's picks.

## Decisions
- Theme: **light default** (follows system), **dark** = navy-black, sun/moon toggle in header, applied before paint. Replaces "pure black, no toggle".
- Tokens (light / dark): bg #FFFFFF / #0B1622; surface #F2F6FA / #12243A; text #12212F / #E8EDF2; muted #5A6470 / #9AAABB; border #E3E6EA / #26384D; brand-red #B3122E / #FF5A6E; brand-blue #1A3E62 (bands, links); strike #D9542C / #F2766A; guard #2D6FD0 / #6FA3F5. Brand colours = type, rules, bands only. Strike/Guard only inside game figures. Logos in white wells; 1 px border in light mode.
- Fonts: **Archivo 700** headlines; IBM Plex Sans body; IBM Plex Mono only for dates/numbers/labels. Header wordmark larger. Research page: larger, standardised type (h2 = step-4, body step-1).
- Shapes: 3 px corners, rules not boxed cards, sections 96–112 px, content 1200 px, mono labels at page level only, no numbered circles / pill chips, no dot grid.
- Hero: **title above a rounded 2:1 video panel** (supermimic style); best CMU clip at full resolution; poster still; pause button; reduced-motion → still.
- Nav: **Updates · Research · Partners ▾ · Flights · Publications · Contribute** (+ theme toggle). Programme page becomes Research (old /programme/ redirects).
- Home order: hero → logo row (ST, NUS, UPenn, CMU + "Funded by HTX") → updates strip (3 latest) → At a glance + Latest rail (5) → partner cards ("NUS's page · written by NUS →", "Last post") → research themes (5 rows) → **interactive annotated drone** (full explain mode, partner names in callouts, effects) → flights (lead + 3) → publications → people (team photo + names) → footer.
- Drone effects: select lights parts + names; two-way peek; leader lines draw on scroll-in; flight dots march when Flight lit; Strategy pulse; ring drift only while Safety lit; no count-ins. Connection diagram stays on Partners only (drone removed there).
- Timeline: **June 2026 – June 2029**; Year 1 of 3. Ladder M6 (first Starling flight, Singapore) = **done** (Jeremy: Starlings fly in SG).
- Updates: per-partner folders `content/updates/<partner>/`; partner filter on Updates page; "Updates from X" always shown (empty → "No posts yet. Post one →").
- Publications: `publications:` per partner; Publications page lists them by partner; "None yet (as of date)" where empty.
- Contribute page: "Which file is mine?" table, people/photo how-to, update how-to.
- Partners obvious: cards on home; menu heading "Each partner has its own page"; partner page top "This is NUS's own file · Edit"; footer lists files.
- Content additions: UPenn paper STL-SVPIO (arXiv 2603.13333, Zheng, Zang, Amine, Vasile, Mangharam; IROS 2026 per Jeremy); ST posters at IROS 2026 (William Teo "Pairwise Approximation Can Select the Wrong Multi-Robot Plan", IROS 2026 Workshop on Intelligent Information Gathering; Jiaying Chen & Chia Hwe Huang "When Is It Worth Looking Again? Cost-Aware Active Information Gathering for ObjectNav"); the A0 programme poster (21 Oct 2026 demo); NUS workshop paper if findable; photos: IROS 2026 trip + CMU demo booth + cage group photos as update galleries; profile pics for all partners from `profilepics/`.
- Cuts: Partners-page "palm-sized to own lab" repeat; one of the two Partners-page diagrams (drone goes); 0.081 m figure only in Localisation + October post; directions to 3 lines; matched pro/con lines → one trade-off with its case.
- Keep: positioning statement word for word; partner order; HTX funder; people row; open-problem lists; signed updates.
