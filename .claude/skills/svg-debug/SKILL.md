---
name: svg-debug
description: Use when anything on the Strike vs Guard website is broken, a build or CI run fails, a deploy looks wrong, or a page misbehaves. Evidence-first debugging that fixes the cause, never the check.
---

# Debug

Full process and the table of known failures: `docs/claude/DEBUGGING.md`. Read it first; most
failures seen so far are in its table. This skill is the checklist.

## 1. Capture the exact failure
- Copy the exact error text. For CI: `gh run list --limit 5`, then `gh run view <id> --log-failed`.
- Which run: `CI` (build + links), `Deploy site` (publishes main **and** development), or
  `pages build and deployment` (GitHub's own Jekyll job: a settings problem, not code).
- Branch, commit, event.

## 2. Reproduce locally
```bash
node -v && npm ci && npm run check
BASE_PATH=/Strike-Versus-Guard/preview/ PREVIEW=1 npm run check     # the test-site build
npm run shots -- /<page>/ [--theme dark] [--width 390]              # visual or interaction bugs
```
Passes locally but fails in CI → compare Node version, base path, env vars, branch, before code.

## 3. One hypothesis at a time
State it in one sentence. Find the log line or code line that proves or disproves it. Discard and
form the next. Do not stack speculative edits.

## 4. Smallest fix at the real cause
Never: disable or loosen a check, weaken `src/content.config.ts`, force-push, delete a branch,
add `.nojekyll`, run `playwright install`. If the fix is a GitHub setting, give the exact clicks.

## 5. Verify the way the failure was seen
Build failure → `npm run check` passes, then the CI run passes. Visual → `npm run shots` is
`"ok": true` and the PNG looks right. Deploy → run conclusion **and** `curl -s <url> | grep <unique>`.

## 6. Record
If the failure was new, add one row to the table in `docs/claude/DEBUGGING.md`: symptom, cause,
fix. Then commit as in `svg-change` §6.

## Looks broken but is not
- **Unstyled page right after a deploy:** the Pages CDN serves old HTML with new CSS names for up
  to ten minutes. Verify with a fresh headless load (`npm run shots` against the live URL is not
  possible; use `curl` to confirm the served HTML references files that exist). Do not revert.
- **Content schema error:** the message names the file and field; fix the content, not the schema.
