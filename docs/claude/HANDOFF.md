# Claude handoff: Strike vs Guard website

> **How to use this file:** paste it into any Claude conversation (or point Claude Code at the repo,
> whose `CLAUDE.md` links here) to continue the work with full context. Last updated **2 Nov 2026**.

## 1. One-paragraph summary
This repo (`Strike-vs-Guard/Strike-Versus-Guard`) is the website of **Strike vs Guard**, a research
programme on **decentralised multi-drone autonomy** funded by **HTX** and carried out by **ST Engineering**
(lead partner) with **NUS**, **UPenn** and **CMU**. It is an **Astro 7** static site on **GitHub Pages**.
Each partner edits one Markdown file. All edits go to the `development` branch, which publishes a
**test site**. A pull request from `development` into `main` publishes the **live site**. The
programme lead driving the work is Jeremy (ST Engineering).

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
4. **Tokens only:** blue/red belong to the game teams; ST red appears in three places only.
5. **Prove it before pushing:** `npm run check`, plus Playwright screenshots (light, dark, 390px) for
   anything visual.

## 4. Current state (as of this handoff)
**Done and live:**
- Home page: hero, two tracks, the benchmark arena animation, "How it fits together", flights,
  proof so far, milestones, directions, updates.
- Partner pages and an Updates page.
- Schema validation, link and size checks, CI, deploy of main and development together.
- GitHub Pages source set to **GitHub Actions** (done by Jeremy).

**On `development` (test site), not yet merged to `main`:**
- **Annotated drone + connection diagram ("1 + 3")**:
  - Home "How it fits together": "What each layer does" uses `DroneDiagram` (explain mode), then
    "Who works on each layer" uses `ConnectionDiagram`.
  - Every partner page shows the drone with that partner's layers lit.
  - Partner order changed to ST, NUS, UPenn, CMU.
  - UPenn now also on the Drones layer.
- **Drone polish pass (in progress when this file was written):** a spec synthesised from three
  critics (illustration, information design, interaction). It covers:
  - layers stacked 1→4 top to bottom, with Integration as a bracket
  - a redrawn ¾-view airframe
  - a peer-to-peer strategy metaphor, with no central "brain"
  - a "safe distance" marker; "AirStack: plan → flight"
  - one shared selection between the two diagrams (`sys:select` events), fixing a mouse/keyboard bug
  - "Show partners ↓" cues
  - a static partner mode showing each partner's own `work` text
  - shorter layer copy in `content/programme/stack.md`

  Check `git log` on `development` to see whether it has been committed. If it hasn't, the spec is in
  §6 of `docs/claude/jeremy.md`.

## 5. Open items / waiting on people
| Item | Who |
|---|---|
| Delete leftover branches `claude/brave-bell-onicwy`, `gh-pages`, `dependabot/github_actions/actions/checkout-7`, `dependabot/github_actions/actions/setup-node-7`; close PRs #1 and #2 (bot) | Jeremy (Claude's session can't delete branches) |
| Two Word documents (`MR-Strike vs Guard-1.0-OCT29.docx`, `D3-Strike_vs_Guard-FR&PDR-1.2-29July26.docx`) were never received; too large with embedded videos. Asked for .txt/PDF exports | Jeremy |
| UPenn's Drones line "Runs the formal-track strategy on the shared Starling 2 Max drones." is a placeholder | UPenn to confirm |
| Partner pages were drafted from the deck. Each partner should review its page, people list and publications; lab website URLs need verifying | Each partner |
| CODEOWNERS team names (`@Strike-vs-Guard/st-web`, `nus`, `upenn`, `cmu`) are placeholders; the `main` ruleset isn't set up yet | Repo admin (`docs/admin-setup.md`) |
| CMU's separate site `Strike-vs-Guard/svg-website` uses counter-UAS wording ("ground controller for counter-UAS flights", "airspace protection", "intruder") and is linked from the CMU page | Raise with CMU |

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
