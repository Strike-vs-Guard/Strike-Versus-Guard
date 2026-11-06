---
name: svg-change
description: The standard way to make any change to the Strike vs Guard website: content, a template, a style, a schema field or media. Covers plan, edit, check, screenshots, commit and push to development.
---

# Make a change

Run `svg-start` first if you have not this session.

## 1. Classify the change
| Kind | Where it lives | Extra rule |
|---|---|---|
| Copy, people, publications, posts | `content/` only | Never put copy in a template |
| New field a partner can fill in | `src/content.config.ts` first, then the content, then the template | Document it in STANDARDS §4 and CONTRIBUTING |
| Look or layout of a page | `src/pages/`, `src/components/`, `src/styles/global.css` | Tokens from STANDARDS §3 only; both themes; run `svg-panel` first if the layout changes |
| Video or image | `public/media/` or `content/partners/<NAME>/` | STANDARDS §9: sizes, credit line, wording |

## 2. Write the intent (one message)
Files that change, files that stay, how you will verify. For wording, check every new sentence
against STANDARDS §2: no defence framing, no "counter-UAS", no "intruder", no "target";
Strike vs Guard is the benchmark game. Partners are equals, in the order ST Engineering, NUS,
UPenn, CMU; HTX is the funder.

## 3. Edit
- Paths: `url('…')` in templates, `./FOLDER/file.jpg` relative paths in content. Never hard-code
  `/Strike-Versus-Guard/`.
- Keep unrelated changes out. One commit per concern.
- Photos: 400 px square JPG, 80 KB or less. Clips: STANDARDS §9 ladder, 8 MB per file.

## 4. Verify (all of it, every time)
```bash
npm run check                                   # build + links + size budget; must pass
npm run shots -- /<page>/                       # for any visible change: light 1280
npm run shots -- /<page>/ --theme dark          # and dark
npm run shots -- /<page>/ --width 390           # and a phone
npm run shots -- /<page>/ --width 390 --theme dark --system   # phone in system dark, nothing stored
```
Each `shots` call must print `"ok": true` (overflow 0, no console errors, no failed requests).
Open the PNGs in `.shots/` and look at them. Fix what looks wrong, at most four rounds.
Interactive parts: test with mouse and keyboard.

## 5. Update the docs the change touches
- New or changed field, page section, rule → STANDARDS (§4 content model, §5 page structure).
- Something a partner will do themselves → CONTRIBUTING.
- A decision, a thing left open, a thing someone must confirm → `docs/claude/HANDOFF.md` §4/§5.
Keep each edit to a sentence or a table row. No new documents.

## 6. Commit and push to development
```bash
git add <the files you changed>                 # by path; never `git add -A` blindly
git commit -m "<area>: <what changed in one line>

<why, two or three lines at most>"
git push origin development
```
The git hooks run `npm run check` again and refuse pushes to `main` or to a new branch. The test
site rebuilds in about two minutes: https://strike-vs-guard.github.io/Strike-Versus-Guard/preview/
For up to ten minutes after a deploy the CDN may serve the old page with new asset names (looks
unstyled); hard-refresh, do not revert.

## 7. Hand over
Tell the user: what changed, the preview URL of the page, what they should look at, and anything a
partner has to confirm. Publishing to the live site is a separate step: `svg-release`.
