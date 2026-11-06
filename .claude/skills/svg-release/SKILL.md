---
name: svg-release
description: Publish the Strike vs Guard test site (development) to the live site (main). Only on the site owner's explicit say-so in the current conversation; opens or merges the pull request and verifies the deploy.
---

# Release development → main

Only ST Engineering's site owner decides when the live site changes. A partner can ask for a
release; the owner says yes. Without that sentence in this conversation, stop at step 2.

## 1. Preconditions
```bash
git switch development && git pull --ff-only
npm run check
gh run list --branch development --limit 3        # latest CI run: success
```
Check the test site by eye once more: https://strike-vs-guard.github.io/Strike-Versus-Guard/preview/
`docs/claude/HANDOFF.md` §4 says what this release contains; add a line if it does not.

## 2. Pull request (anyone may do this)
```bash
gh pr list --base main --head development            # reuse an open one if it exists
gh pr create --base main --head development --title "<what goes live, one line>" --body "<the HANDOFF lines for this round>"
```
Hand the PR URL to the owner. Stop here unless the owner has said to merge.

## 3. Merge (owner's say-so only)
```bash
SVG_ALLOW_MAIN=1 gh pr merge <number> --merge        # merge commit; never squash or rebase
```
The `SVG_ALLOW_MAIN=1` prefix is the record that the owner approved; the guard hook blocks the
command without it. Never push to `main` directly, never force-push, never delete branches.

## 4. Verify the live site
```bash
gh run list --branch main --workflow "Deploy site" --limit 1      # completed success
curl -s "https://strike-vs-guard.github.io/Strike-Versus-Guard/?v=$(date +%s)" | grep -c "<something unique to this release>"
```
For up to ten minutes the CDN may serve the previous HTML with the new asset names (page looks
unstyled). That clears itself; do not revert, do not redeploy.

## 5. Record
`docs/claude/HANDOFF.md`: move the release from "on development" to "live on <date>"; remove the
merge from §5 open items. Commit to development as in `svg-change` §6.
