# How Claude should debug this project

The goal is **accurate** fixes. Find the real cause from evidence, change the smallest thing that
fixes it, and prove the fix the same way the failure was seen. Do not guess, and do not "fix" by
loosening checks.

---

## The process (follow in order)

### 1. Reproduce and capture the exact failure
- Get the **exact** error text, not a summary. On GitHub Actions, read the failing **job log** and find
  the first `##[error]` and the lines above it. Using the GitHub MCP:
  1. `actions_list` with method `list_workflow_runs` to find the run.
  2. `actions_list` with method `list_workflow_jobs` to find the failed job and **which step** failed.
  3. `get_job_logs` with `job_id` and `tail_lines` to read it.
- Note **which workflow** failed. This repo has three kinds of run, and they mean different things:
  | Run name | Meaning |
  |---|---|
  | `CI` | Build + link check of the branch. |
  | `Deploy site` | Builds main **and** development, then publishes to Pages. |
  | `pages build and deployment` | **GitHub's own Jekyll job, not ours.** It only appears when Settings → Pages → Source is "Deploy from a branch". The fix is a setting, not code (see the table below). |
- Note the **branch, commit SHA and event** (`push`, `pull_request`, `workflow_run`).

### 2. Reproduce locally before changing anything
```bash
node -v                      # must satisfy package.json "engines" (Node 24 LTS, or 22.23.4 or newer)
npm ci
npm run check                # astro build + scripts/check-links.mjs (links + size budget)
```
- For a test-site build, also run:
  `BASE_PATH=/Strike-Versus-Guard/preview/ PREVIEW=1 npm run check`
- If it passes locally but fails in CI, compare **environments** before code: Node version, base
  path, environment variables and which branch was checked out.

### 3. Form one hypothesis and test it directly
- State it in one sentence ("CI picked Node 22.23.3, which Astro rejects").
- Find the line in the log or code that proves or disproves it. If it is disproved, discard it and
  form the next hypothesis. Do not stack speculative changes.

### 4. Make the smallest fix at the real cause
- Fix the cause, not the symptom: pin the Node version rather than deleting the engine check;
  skip `<script>` blocks in the link checker rather than disabling it.
- **Never** skip or disable a check or test, weaken the content schema, force-push, or delete
  branches to make something pass.
- Keep unrelated changes out of the same commit.

### 5. Verify the same way the failure was seen
- **Build failure:** `npm run check` passes locally, then the CI run passes.
- **Visual or interaction bug:** check in a real browser:
  ```bash
  npm run check                                     # builds dist/
  npm run shots -- /<page>/                         # 1280 light; add --theme dark, --width 390
  ```
  Each call prints overflow (must be 0), console errors and failed requests (must be none) and the
  PNG path in `.shots/`. Look at the screenshots. For interactions write a short playwright-core
  script in the scratchpad (see `scripts/shots.mjs` for the launch code) and test **mouse and
  keyboard** (`click()` vs `press('Enter')`).
- **Deploy issue:** after pushing, check the run conclusion **and** fetch the published page
  (`curl -s <url> | grep <something unique to the change>`).

### 6. Report precisely
- Say what failed, the root cause (with the log line), the fix, and how it was verified.
- If something could not be verified (e.g. a setting only an admin can change), say so plainly and give
  the exact clicks.

---

## Known failure modes in this project (check these first)

| Symptom | Root cause | Fix |
|---|---|---|
| `Node.js v22.23.3 is not supported by Astro! … ">=22.23.4"` | `.nvmrc` said `22`, so setup-node used the runner's cached 22.x | `.nvmrc` = `24` (already done). Never use a bare major version that could resolve below Astro's minimum. |
| Red **"pages build and deployment"** with Jekyll `YAML Exception … .astro` | Pages source is "Deploy from a branch", so GitHub runs Jekyll on raw source | Settings → Pages → Source → **GitHub Actions**. Do **not** add `.nojekyll` to the repo root: that would publish raw source over the site. |
| `Deploy site` from `development` fails at the **deploy** job, with no steps and no log | `github-pages` environment only allows the default branch | Development deploys run via `workflow_run` from main's context (already done). Don't trigger deploy on `push: development`. |
| Link checker reports `"'" does not start with the site base` | It was scanning inline `<script>` strings like `src="' + x + '"` | The checker strips `<script>` blocks first (already done). |
| Images missing in a full-page screenshot | `loading="lazy"` images never scrolled into view | Scroll the page in steps before screenshotting. |
| Sticky header overlapping an element screenshot | Header is `position: sticky` | Inject `.site-header{position:static!important}` in test scripts only. |
| Leader lines in the drone diagram misaligned | Measured while hidden (zero size) or while a callout was lifted by a hover transform | Return early from `draw()` when width is 0; never use `transform` on callouts; ResizeObserver redraws. |
| Diagram state differs between mouse and keyboard | Re-entrant `element.click()` inside a click handler (the browser ignores it for keyboard activation) | Use one shared state and CustomEvents (`sys:select`), never synthetic re-entrant clicks. |
| Text with `$$` or `$&` comes out mangled when inlining a file | JS `String.prototype.replace` treats `$` specially in the replacement string | Use a replacer function, or Python `str.replace`. |
| `pkill -f "astro preview"` kills your own shell (exit 144) | The pattern matches the running bash command line | Run `pkill` as its own command, or use `pkill -f "[a]stro preview"`. |
| Content build error `… does not match collection schema` | Front matter breaks a rule in `src/content.config.ts` | Fix the content file (the error names file and field). Change the schema only if the rule itself is wrong. |
| `Could not find requested image` | Path not relative to the content file, wrong case, or not uploaded to the same branch | Use `./FOLDER/name.jpg`. Paths are case-sensitive. |
| Push to a branch refused with `403` | The session's git proxy allows pushes to specific branches only, and no branch deletion | Ask the user to do it in the GitHub UI. Never work around it. |
| `pre-push: refusing to push to main` / `refusing to push branch` | The repo's git hooks (`.githooks/`, installed by `npm ci`) enforce STANDARDS §7 | Push to `development`. Publishing is a pull request (`svg-release` skill). Not a bug. |
| `BLOCKED by scripts/claude/guard.mjs: …` | The Claude PreToolUse hook stopped a command that breaks §7 | Do what the message says. Never edit the guard to get past it. |
| Home page unstyled for a few minutes after a deploy; a `_astro/*.css` request is 404 | The Pages CDN served the previous HTML with the new build's asset names (`cache-control: max-age=600`) | Wait up to 10 minutes, hard-refresh. Do not revert or redeploy. |
| `development` and the test site vanish right after a pull request is merged into `main` | Settings → General → "Automatically delete head branches" was on; `development` is the head branch of the release PR | Keep the setting off (docs/admin-setup.md step 5). The ruleset "development: no deletion, no force push" now refuses the deletion. To restore: push the last `development` commit again. |
| On an Android phone the light theme looks grey-black and the logos nearly vanish | The browser's forced dark mode ("Darken websites", Samsung Internet dark mode) recolours pages that declare plain `color-scheme: light` | `color-scheme: only light` / `only dark` in `global.css` plus `<meta name="color-scheme" content="light dark">` (done). Test: Chrome with `--enable-features=WebContentsForceDark --force-dark-mode`. |
| Page text shows faintly through the sticky header on Android | The build drops the unprefixed `backdrop-filter`; Chrome ignores `-webkit-backdrop-filter` | Header background is solid `--bg` (done). Do not reintroduce a translucent header. |
| `gh api … rulesets` returns 403 | Only repository admins can change rulesets | Ask an admin (docs/admin-setup.md). |

---

## Environment notes for Claude Code cloud sessions
- Use the GitHub MCP tools (`mcp__github__*`) for runs, logs and PRs. `gh` works only for search.
- `curl` to `api.github.com/repos/.../pages` is blocked by the proxy. Infer the Pages settings from
  which runs appear (see step 1).
- Screenshot and browser checks: `npm run shots` with the Chrome on the machine, or
  `SVG_BROWSER=/path/to/chromium`. Don't run `playwright install`.
- Put throwaway scripts in the session scratchpad, not in the repo.
