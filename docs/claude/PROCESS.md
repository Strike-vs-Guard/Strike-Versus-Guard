# The Claude process for this repository

Four labs edit this site, often with Claude Code. This page is the one process everyone's Claude
follows, so the result looks the same whoever ran it. Everything it needs is **in the repository**:
nothing to install beyond `npm ci`.

## What a session gets automatically

| Piece | Where | What it does |
|---|---|---|
| Orientation | `CLAUDE.md` | The rules in one screen, read by Claude Code at start |
| Session hook | `.claude/settings.json` → `scripts/claude/session.mjs` | Prints branch, Node, hook state and which skill to run first |
| Guard hook | `.claude/settings.json` → `scripts/claude/guard.mjs` | Blocks, before they run: pushes to `main`, force pushes, branch creation or deletion, local merges into `main`, `gh pr merge` without the owner's token, `playwright install`, `git reset --hard` |
| Git hooks | `.githooks/pre-commit`, `.githooks/pre-push`, installed by `npm ci` (`prepare` script) | Refuse commits on `main`, pushes to `main` or to a new branch, and any push that fails `npm run check`. Also set `push.default=current` so a plain `git push` goes to the branch you are on |
| GitHub rulesets | Repository settings → Rules | `main` accepts only merged pull requests whose CI passed; no branch other than `development` and `main` can be created |
| Skills | `.claude/skills/svg-*` | The steps for each kind of task (below) |
| Agents | `.claude/agents/svg-*` | Panels and an implementer for design work (`AGENTS_AND_SKILLS.md`) |
| Screenshots | `npm run shots -- /<page>/ [--theme dark] [--width 390]` | Real-browser check: overflow, console errors, failed requests, a PNG in `.shots/` |

## The skills

| Say | Skill | Outcome |
|---|---|---|
| Start of every session | `svg-start` | Rules and state read, branch checked, intent stated |
| "Change X" | `svg-change` | Edit → `npm run check` → `npm run shots` → docs → commit → push to `development` → preview URL |
| "X is broken" | `svg-debug` | Exact error → reproduce → one hypothesis → smallest fix → verified the same way → table row in `DEBUGGING.md` |
| "Post an update" | `svg-post` | A post in the partner's folder with `draft: true` until approved |
| "What should this look like" | `svg-panel` | Three agents → reconciled → clickable draft → user picks → build |
| "Publish" | `svg-release` | PR from `development`; merge only on the owner's say-so (`SVG_ALLOW_MAIN=1`); deploy verified |

## Rules the process enforces (STANDARDS has the full text)

- Two branches. Edits on `development`; `main` changes by pull request only. Default push target is
  the current branch, so `git push` from `development` never touches `main`.
- Copy lives in `content/`, never in templates. New field: schema first, then docs.
- Wording: STANDARDS §2. No defence framing. Partners equal, in order ST Engineering, NUS, UPenn, CMU.
- Done means: `npm run check` passes, `npm run shots` is `"ok": true` at 1280 light, 1280 dark and
  390, mouse and keyboard tested, docs updated, pushed to `development`.
- Decisions and open items go in `HANDOFF.md`; a one-paragraph log of each round in `jeremy.md`.

## Overriding a guard

Only the site owner. Prefix the command with `SVG_ALLOW_MAIN=1`. The prefix is the record that the
owner approved it in that conversation. The GitHub ruleset still applies: a direct push to `main`
is refused by the server whoever runs it.

## Setting it up on a new machine

```bash
git clone https://github.com/Strike-vs-Guard/Strike-Versus-Guard.git
cd Strike-Versus-Guard
npm ci                      # installs deps and the git hooks
git switch development
claude                      # the session hook prints the state; say "run svg-start"
```
`npm run shots` needs Google Chrome on the machine, or `SVG_BROWSER=/path/to/chrome`.
