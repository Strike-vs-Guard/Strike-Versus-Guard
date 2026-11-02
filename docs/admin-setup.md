# One-time setup for repository admins

These settings can only be changed by an admin of the `Strike-vs-Guard` organisation / repository.
Until they are done, the workflows run but nothing is published.

1. **Merge this branch to `main`.** The first push to `main` runs *Deploy live site*, which creates
   the `gh-pages` branch.
2. **Turn on GitHub Pages:** Settings → Pages → *Build and deployment* → Source:
   **Deploy from a branch** → Branch: **`gh-pages`**, folder **`/ (root)`** → Save.
   (Do not choose "GitHub Actions" as the source; PR previews need the branch method.)
3. **Allow the workflows to write:** Settings → Actions → General → *Workflow permissions* →
   **Read and write permissions**. If the organisation restricts which actions may run, allow
   `actions/*`, `rossjrw/pr-preview-action` and `JamesIves/github-pages-deploy-action`.
4. **Create partner teams** (Organisation → Teams): `st-web`, `nus`, `upenn`, `cmu`. Add each
   partner's editors, and give every team **Write** access to this repository. CODEOWNERS
   rules are ignored for teams without write access. If you'd rather use individual usernames,
   edit [`.github/CODEOWNERS`](../.github/CODEOWNERS).
5. **Protect `main`:** Settings → Rules → Rulesets → New branch ruleset, targeting `main`:
   - Require a pull request before merging, with 1 approval
   - Require review from Code Owners
   - Require status check **Build and check** (from the CI workflow)
   - Block force pushes and deletions
6. **Private repository?** GitHub Pages on a private repo needs a paid plan, and the site itself is
   still public. Preview URLs are public too.

## Custom domain later

Add the domain under Settings → Pages, then change the default in `astro.config.mjs` from
`'/Strike-Versus-Guard/'` to `'/'`, and `SITE_URL` to the new domain. In `.github/workflows/*.yml`,
set `BASE_PATH` to `/` (deploy) and `/pr-preview/pr-N/` (preview).

## Housekeeping

- Dependabot opens a monthly pull request to update Astro and the actions. Merge it once CI is green.
- Large videos: GitHub rejects files over 100 MB and Pages doesn't serve Git LFS. Keep clips small,
  or host them elsewhere and link them.
