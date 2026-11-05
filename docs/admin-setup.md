# One-time setup for repository admins

These settings can only be changed by an admin of the `Strike-vs-Guard` organisation / repository.

## Branches

The repository keeps exactly two branches:

| Branch | Purpose | Published at |
|---|---|---|
| `main` | Live site | https://strike-vs-guard.github.io/Strike-Versus-Guard/ |
| `development` | Where all edits happen; test site | https://strike-vs-guard.github.io/Strike-Versus-Guard/preview/ |

A push to `main`, or a push to `development` that passes the CI check, runs *Deploy site*
(`.github/workflows/deploy.yml`). It builds **both** branches and publishes them together. No
`gh-pages` branch is used. The development-triggered run executes on `main`'s side (via
`workflow_run`), so the default `github-pages` environment rule ("main only") is fine as it is.

## Settings

1. **GitHub Pages source:** Settings → Pages → *Build and deployment* → Source: **GitHub Actions**.
   (Not "Deploy from a branch".)
2. If you see a failing **"pages build and deployment"** job (a Jekyll error about `.astro` files),
   the Pages source is still set to "Deploy from a branch". Switch it to **GitHub Actions** (step 1).
3. **Workflow permissions:** Settings → Actions → General → leave *Read repository contents* as the
   default; the workflows request what they need. If the organisation restricts actions, allow `actions/*`.
4. **Rulesets (done 5 Nov 2026, Settings → Rules → Rulesets):** "main: pull requests only"
   (no deletion, no force push, pull request required with a merge commit, status check
   "Build and check" required) and "only development and main" (branch creation blocked for every
   other name). Re-create them from these descriptions if they are ever removed.
5. **Auto-delete branches (done 5 Nov 2026):** Settings → General → **Automatically delete head
   branches** is on, so any branch that does get created is removed when its pull request is merged.
   The four leftover branches (`claude/…`, two `dependabot/…`, `gh-pages`) were deleted the same day.
6. **Partner teams:** Organisation → Teams: `st-web`, `nus`, `upenn`, `cmu`. Add each partner's
   editors and give every team **Write** access. CODEOWNERS rules are ignored for teams without write
   access. Or replace the team names in [`.github/CODEOWNERS`](../.github/CODEOWNERS) with usernames.
7. **Optional, later:** add "require 1 approval" and "require review from Code Owners" to the
   `main` ruleset once the partner teams (step 6) exist; until then a merged pull request with a
   green "Build and check" is the rule.
8. **Protect `development` lightly (optional):** a second ruleset targeting `development` that only blocks
   force pushes and deletion, so partners can still commit to it directly.
9. **Private repository?** GitHub Pages on a private repo needs a paid plan, and the published site,
   including the test site, is public either way.

## Going live

Open a pull request from `development` into `main` (Pull requests → New → base `main`, compare
`development`). Once approved and merged, the live site updates in a few minutes. Keep the pull
request open while you collect changes if you like: it updates itself as `development` changes.

## Custom domain later

Add the domain under Settings → Pages, then change the default in `astro.config.mjs` from
`'/Strike-Versus-Guard/'` to `'/'`, and `REPO_PATH` in `deploy.yml` to `/`.

## Housekeeping

- There is no automatic dependency bot (it would create extra branches). Every few months, on
  `development`, run `npm outdated` and `npm audit`, update Astro if needed (`npm install astro@latest`),
  and check the test site.
- Large videos: GitHub rejects files over 100 MB and Pages doesn't serve Git LFS. `npm run check`
  fails on clips over 15 MB.
