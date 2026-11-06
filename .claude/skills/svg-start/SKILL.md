---
name: svg-start
description: Run at the start of every session on the Strike vs Guard website, before any edit, question or investigation. Loads the rules and state, checks the branch and tools, and sets how the session is run.
---

# Start a session on the Strike vs Guard site

Do these in order. Do not skip because the task looks small.

## 1. Read the rules and the state (5 minutes)
1. `CLAUDE.md` (the short version of everything).
2. `STANDARDS.md` §2 (wording table), §4 (content model), §7 (branches), §8 (definition of done).
3. `docs/claude/HANDOFF.md` §4 (current state) and §5 (open items). Something you are about to
   "fix" may already be a deliberate decision recorded there.

## 2. Check the working copy
```bash
git status -sb            # must be on development, clean or with changes you know about
git pull --ff-only        # someone from another lab may have pushed
node -v                   # 22.23.4 or newer (24 preferred)
git config core.hooksPath # ".githooks"; if empty run: npm ci
```
If the branch is `main`: `git switch development`. Never create a branch.

## 3. Know who you are working for
Ask, if not obvious, which partner the user belongs to. That decides which files they own
(CONTRIBUTING §1 and `.github/CODEOWNERS`):

| Partner | Owns |
|---|---|
| NUS / UPenn / CMU | `content/partners/<NAME>.md`, `content/partners/<NAME>/`, `content/updates/<name>/` |
| ST Engineering | everything else (templates, styles, shared programme text, workflows) |

A partner editing another partner's file, or a template, is fine as a proposal but say so in the
commit message and the hand-over so the owner can review it.

## 4. Say what you intend before doing it
One short message: what you understood, which files change, what stays untouched, how you will
verify. Then start. For anything that changes a page's layout or look, use the `svg-panel` skill
instead of building straight away.

## 5. Pick the skill for the task
| Task | Skill |
|---|---|
| Edit content, a template, a style, a field | `svg-change` |
| Something is broken, a build or deploy failed | `svg-debug` |
| Write a news post for a partner | `svg-post` |
| Decide a layout, a visual treatment, a page structure | `svg-panel` |
| Publish development to the live site | `svg-release` |
