# One-time setup for repository admins

These settings can only be changed by an admin of the `Strike-vs-Guard` organisation / repository.

## Branches

The repository keeps exactly two branches:

| Branch | Purpose | Published at |
|---|---|---|
| `main` | Live site | https://strike-vs-guard.github.io/Strike-Versus-Guard/ |
| `development` | Where all edits happen; test site | https://strike-vs-guard.github.io/Strike-Versus-Guard/preview/ |

A push to either branch runs *Deploy site* (`.github/workflows/deploy.yml`), which builds **both**
branches and publishes them together. No `gh-pages` branch is used.

## Settings

1. **GitHub Pages source:** Settings → Pages → *Build and deployment* → Source: **GitHub Actions**.
   (Not "Deploy from a branch".)
2. **Pages environment:** Settings → Environments → `github-pages` → *Deployment branches and tags* →
   allow **`main`** and **`development`**. By default only the default branch may deploy, which would
   make pushes to `development` fail at the deploy step.
3. **Workflow permissions:** Settings → Actions → General → leave *Read repository contents* as the
   default; the workflows request what they need. If the organisation restricts actions, allow `actions/*`.
4. **Auto-delete branches:** Settings → General → tick **Automatically delete head branches**, so that
   any branch someone does create is removed when its pull request is merged.
5. **Partner teams:** Organisation → Teams: `st-web`, `nus`, `upenn`, `cmu`. Add each partner's
   editors and give every team **Write** access. CODEOWNERS rules are ignored for teams without write
   access. Or replace the team names in [`.github/CODEOWNERS`](../.github/CODEOWNERS) with usernames.
6. **Protect `main`:** Settings → Rules → Rulesets → New branch ruleset, targeting `main`:
   - Require a pull request before merging, with 1 approval
   - Require review from Code Owners (the owners of every partner file changed must approve)
   - Require status check **Build and check** (from the CI workflow)
   - Block force pushes and deletions
7. **Protect `development` lightly:** a second ruleset targeting `development` that only blocks
   force pushes and deletion, so partners can still commit to it directly.
8. **Private repository?** GitHub Pages on a private repo needs a paid plan, and the published site,
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
