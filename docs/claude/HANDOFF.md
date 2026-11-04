# Claude handoff: Strike vs Guard website

> **How to use this file:** paste it into any Claude conversation (or point Claude Code at the repo,
> whose `CLAUDE.md` links here) to continue the work with full context. Last updated **3 Nov 2026** (rounds 3 to 5).

## 1. One-paragraph summary
This repo (`Strike-vs-Guard/Strike-Versus-Guard`) is the website of **Strike vs Guard**, a research
programme on **decentralised multi-drone autonomy** funded by **HTX** and carried out by **ST Engineering**
(lead partner) with **NUS**, **UPenn** and **CMU**. It is an **Astro 7** static site on **GitHub Pages**.
Each partner edits one Markdown file. All edits go to the `development` branch, which publishes a
**test site**. A pull request from `development` into `main` publishes the **live site**. The
site owner driving the work is Jeremy (ST Engineering); the ST lead is William Teo.

- Live: https://strike-vs-guard.github.io/Strike-Versus-Guard/
- Test: https://strike-vs-guard.github.io/Strike-Versus-Guard/preview/

## 2. Read these first
| File | Why |
|---|---|
| `STANDARDS.md` | **The rules**: positioning, banned wording, partner order, tokens, content model, branches, definition of done |
| `docs/claude/DEBUGGING.md` | The debugging process and every failure already hit, with its fix |
| `docs/claude/AGENTS_AND_SKILLS.md` | Which agents and skills were used and how to reuse them (`.claude/agents/`) |
| `docs/claude/jeremy.md` | The conversation history: what was asked, decided and changed, in order |
| `docs/design-decisions.md` | Why it is built this way |
| `CONTRIBUTING.md` | How partners edit (browser and local) |
| `docs/admin-setup.md` | Settings only a repo admin can change |

## 3. Non-negotiables (summary of STANDARDS.md)
1. **Not counter-UAS.** It's a research programme; *Strike vs Guard* is the benchmark game. Use the
   wording table in STANDARDS §2.
2. **Partners are equals.** ST Engineering is the lead partner (coordinates and integrates). NUS, UPenn
   and CMU are partners. HTX is the funder ("Funded by HTX"). Order: **ST Engineering, NUS, UPenn, CMU**.
3. **Exactly two branches:** `development` (edit) and `main` (live, via PR only). No feature branches,
   no Dependabot.
4. **Tokens only:** Strike/Guard colours belong to the game figures; brand red/blue are type, rules and bands only. Test light and dark.
5. **Prove it before pushing:** `npm run check`, plus Playwright screenshots (1280 and 390px) for
   anything visual.

## 4. Current state (as of 3 Nov 2026)
**Restructured on `development` (test site), not yet merged to `main`:**
- Four pages plus Updates: Home, Programme, Partners, Flights (see STANDARDS §5). (Superseded by round 5 below.)
- Five layers (Strategy, Safety, Flight, Localisation, Drones, plus Integration). `work:` accepts
  `localisation`; ST Engineering leads it, CMU provides the simulator and technical advice.
- One pure-black theme (superseded by round 5: light default plus dark toggle).
- `decisions:` list in `overview.md` ("What they decide" under the hero photo); `status:` line in
  `content/programme/localisation.md`.
- Spec: `docs/superpowers/specs/2026-11-03-site-restructure-design.md`; plan beside it in `plans/`.

**Round 2 (3 Nov 2026, after Jeremy saw the test site), on `development`, PR #6 open:**
- A three-agent UX panel reviewed the site; Jeremy chose from a draft with switches (compact drone on
  home, no Benchmark nav item, clip in the hero). Spec: `docs/superpowers/specs/2026-11-03-home-redesign-design.md`.
- Nav is now Programme · Partners ▾ · Flights · Updates; the Partners menu lists each partner's page.
- Home is about 5 screens (was 6.5); content width 1320 px; footer logos in colour, grouped
  "Funded by | Partners"; team photo at the bottom; full drone moved to the Partners page.
- `overview.md` gains `video:` and `gameNote:`.
- The panel is saved as `.claude/agents/svg-ux-panel-{first-screen,layout,navigation}.md`.

**Simulation work (3 Nov 2026, on `development`):** from the October monthly report (now approved for
publication), an "In simulation" section on the NUS, UPenn, CMU and ST pages (clips/stills + 2–3
sentences), a Programme "In simulation" section (`simulation.md`, `Simulation.astro` via the
generalised `Clips.astro`), a new localisation `status:` number, and a link checker that resolves
relative paths.

**FR&PDR and localisation brief (3 Nov 2026, on `development`):** both approved for selected publication.
Programme: "How a command travels" (`command.md`, `CommandPath.astro`) and localisation as three
question cards, the rule, the plan as targets and a simulation figure. Flights: CMU outdoors
(`outdoor.md`) and the test ladder M1–M6 as of July 2026 (`ladder.md`, `TestLadder.astro`). Partner
pages: July results and 1–2 clips/stills each. Year 1 milestone names the March 2027 CMU demonstration
as a target. New item fields: `passes:`, `state:`.

**Round 3, content from the reports (3 Nov 2026, `development`, PR #6):** see the two paragraphs
above. Extra: Programme "We try it in simulation first" and "How a command travels"; Flights "Test
ladder" (M1–M6, July 2026), outdoor clip, and CMU's three extra clips and Starling photo from CMU's
public `svg-website` repo (with consent, credit "Photo/Video: CMU AirLab"; that repo is never edited).

**Round 4, humanising (3 Nov 2026, `development`, PR #6):** an ad-hoc three-reviewer panel (editor, art
director, outside professor) said the site read as machine-written. Changes: `people:` per partner
(row with faces; team photo caption names everyone); slogans rewritten (hero title unchanged); partner
pages in first person; `open:`/`openLabel:` ("What we haven't solved yet") on Localisation, Simulation
and Flights; updates as a dated log with `author:`; footer note "Four labs, in Singapore, Pittsburgh
and Philadelphia. Funded by HTX."; directions as a plain numbered list; drone drawing without dot grid
or corner marks; Flights = lead clip + grid with stamps and "watch" cues + annotated lab photo; logos
sized by visual weight (`src/lib/logo.ts`). Voice rules: STANDARDS §2. Panel brief:
`docs/claude/AGENTS_AND_SKILLS.md`.

**Round 5, lab feedback (3 Nov 2026, `development`, PR #6):** nine points from the lab, a panel (design
system / content architecture / drone interaction) and an approved draft (private claude.ai page
Kxx7DfmQ51Hv3EoeFyBgFj). Spec: `docs/superpowers/specs/2026-11-03-v3-redesign-design.md`.

| Area | State |
|---|---|
| Theme | Light default, dark navy-black, header toggle; tokens in STANDARDS §3; Archivo 700 headlines; larger wordmark |
| Nav | Updates · Research · Partners ▾ · Flights · Publications · Contribute |
| Pages | Research replaces Programme (`/programme/` redirects); new Publications and Contribute; Partners keeps only the connection diagram |
| Home | Hero (title above a 2:1 clip panel), logo row, updates strip, glance + latest, partner cards, five themes, interactive drone, flights, publications, people |
| Drone | Effects list in STANDARDS §5; ring drift only while Safety is lit; no count-ins or scan sweeps |
| Content model | `content/updates/<partner>/` with `gallery:` and `link:`; `publications:` per partner; `glance.md`; `themes.md`; site `start`/`end` (June 2026 – June 2029) |
| Content added | People photos for all partners; IROS 2026 posts and posters; UPenn STL-SVPIO paper; A0 poster (top half only); ladder M6 done |

**Earlier work, already live or on `development`:**
- Partner pages, Updates, schema/link/size checks, CI, deploy of both branches; Pages source is GitHub Actions.
- Annotated drone + connection diagram, with `sys:select` shared selection and the polish pass.
  Small polish left: the "AirStack: plan → flight" label is crossed by the leader line for marker 4,
  and the "safe distance" label sits tight against its marker.

**Round 6 (4 Nov 2026), media replacement:** flight clips replaced from CMU's repo at commit 6167492
(read-only clone; never edit or push there). Rules in STANDARDS §9; panel agents `svg-media-panel-*`.

## 5. Open items / waiting on people
| Item | Who |
|---|---|
| Check the test site (rounds 2 to 5: light/dark toggle, new home order, Research, Publications, Contribute, people rows, first-person pages), then merge PR #6 (open, `development` into `main`) | Jeremy |
| Confirm your people, roles and photos (photos came from the labs' profile pictures) | Each partner |
| Approve or rewrite your "About the lab" text and your lead's bio (`labBlurb:`, `bio:`, `link:`; drafted 4 Nov from marmotlab.org, xlab.upenn.edu, theairlab.org, nearlab.ai) | Each partner |
| Supply the NUS workshop paper (not found publicly; NUS shows "None yet") | NUS |
| Decide whether the full A0 poster may go up (only the top half is published; the lower half has wording the site avoids) | Jeremy |
| Confirm the captions of CMU's clips used in the hero and Flights | CMU |
| Check your first-person page, your people row and your roles. William Teo's role is unknown (left blank); Chen Jiaying's role was taken from nearlab.ai | ST Engineering, Jeremy |
| Check the spelling of Yikuan Fang and Rahul Mangharam | CMU, UPenn |
| Confirm the captions of CMU's clips and the Starling photo credit | CMU |
| Review your partner page; the Partners menu and cards now lead visitors to it, and "Maintained by" sits in its "At a glance" box | Each partner |
| Review the new Localisation line in your partner file (`work.localisation`, drafted for ST Engineering and CMU only) | Partners |
| The home drone's click now lights locally and links to the Partners page; check it reads well on the test site | Jeremy |
| Delete leftover branches `claude/brave-bell-onicwy`, `gh-pages`, `dependabot/github_actions/actions/checkout-7`, `dependabot/github_actions/actions/setup-node-7`; close PRs #1 and #2 (bot) | Jeremy (Claude's session can't delete branches) |
| Two Word documents (`MR-Strike vs Guard-1.0-OCT29.docx`, `D3-Strike_vs_Guard-FR&PDR-1.2-29July26.docx`) were never received; too large with embedded videos. Asked for .txt/PDF exports | Jeremy |
| UPenn's Drones line "Runs the formal-track strategy on the shared Starling 2 Max drones." is a placeholder | UPenn to confirm |
| Partner pages were drafted from the deck. Each partner should review its page, people list and publications; lab website URLs need verifying | Each partner |
| CODEOWNERS team names (`@Strike-vs-Guard/st-web`, `nus`, `upenn`, `cmu`) are placeholders; the `main` ruleset isn't set up yet | Repo admin (`docs/admin-setup.md`) |
| CMU's separate site `Strike-vs-Guard/svg-website` uses counter-UAS wording ("ground controller for counter-UAS flights", "airspace protection", "intruder") and is linked from the CMU page | Raise with CMU |
| NUS workshop paper | NUS |
| Full A0 poster: decide whether to publish | Jeremy |
| Confirm captions and the drone numbering behind "CORRECTING drone N" in CMU's clips | CMU |
| Merge PR #6 | Jeremy |

## 6. How to continue (process that worked)
1. **Clarify, then explore in parallel.** For anything visual, brief 3–4 agents with different
   directions or lenses (see `.claude/agents/`). Show Jeremy a **clickable draft** (an Artifact page)
   **before** touching the site; he wants to see drafts first.
2. **Reconcile into one spec,** state the decision and the reasons in one short message, then
   implement on `development`.
3. **Verify** (STANDARDS §8), commit to `development` with a clear message, and push. Jeremy checks the
   test site and merges to `main` himself. Don't keep watching deploys after pushing unless asked;
   build locally and push.
4. **Communication style Jeremy prefers:** short and direct, with exact clicks for GitHub settings,
   no jargon. He notices GitHub failure emails, so avoid pushes that will fail.

## 7. Source material
- `SvG_10min_deck_4.pptx` (12 slides with speaker notes): the main content source. Its images and the
  7 flight clips (media1–7) were extracted.
- `StrikeVsGuard_A0_v14_PRINT_outlined.pdf`: the A0 poster. Its text is outlined, so it was used
  visually only.
- The programme positioning statement (in `STANDARDS.md` §1), provided by Jeremy.
- Programme reports: the monthly report (29 Oct 2026) is approved for publication (3 Nov 2026); its
  simulation figures are on the site. Selected content from the July 2026 FR&PDR and the localisation
  brief (22 Oct 2026) was approved the same day, with the exclusions in STANDARDS §4 (no budgets, IDs,
  markings, contact scenario, extra names or papers under review). Extracted text is kept outside the
  repo in `~/Documents/GitHub/Strike-Versus-Guard-sources/` on Jeremy's laptop.
- CMU `svg-website` media (commit 6167492), licence CC BY-SA 4.0: the flight clips, re-encoded and credited per STANDARDS §9.
