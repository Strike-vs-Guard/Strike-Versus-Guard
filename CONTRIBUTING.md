# Editing the Strike vs Guard website

Each partner owns one Markdown file. You edit that file on the **`development`**
branch, check the **test site**, and only when it looks right is it merged
into **`main`**, which is the **live site**.

```
 edit your .md file on development  →  test site updates (~2 min)  →  check it  →  merge development into main  →  live site updates (~2 min)
            (you)                            (automatic)                (you)          (ST Engineering, via PR)          (automatic)
```

| Branch | Site | Address |
|---|---|---|
| `development` | Test site | https://strike-vs-guard.github.io/Strike-Versus-Guard/preview/ |
| `main` | Live site | https://strike-vs-guard.github.io/Strike-Versus-Guard/ |

The repository only has these two branches. Never edit `main` directly; every change goes through
`development` first. The test site shows a yellow "Test site" banner and is hidden from search engines.

---

## 1. Which file is mine?

| Partner | Your page text | Your images |
|---|---|---|
| NUS | `content/partners/NUS.md` | `content/partners/NUS/` |
| UPenn | `content/partners/UPenn.md` | `content/partners/UPenn/` |
| CMU | `content/partners/CMU.md` | `content/partners/CMU/` |
| ST Engineering | `content/partners/ST.md` | `content/partners/ST/` |

Each file has two parts:

```markdown
---
short: NUS                         ← "front matter": short fields that feed
lab: MARMot Lab                      the partner card on the home page
lead: Prof Guillaume Sartoretti
summary: >-
  One or two sentences for the card.
updated: 2026-11-02
---

## Our role in Strike vs Guard      ← "body": normal Markdown that becomes
                                      your partner page, /partners/nus/
Free text, lists, images, links…
```

Edit both parts as you like. A few rules apply to the front matter (the build will tell you if you
break one):

- `contribution` must be 70 characters or fewer; `summary` 320 or fewer.
- `logo:` / `labLogo:` must point at an image that exists, written relative to the file,
  e.g. `./NUS/nus.png`.
- `work:` has one line (max 90 characters) for each layer you work on: `strategy`, `safety`, `flight`,
  `localisation`, `drones`, `integration`. These lines fill the "who does what" grid on the home page.
- Dates are `YYYY-MM-DD`.

Other shared files (owned by ST Engineering, but anyone may propose changes):

| What | File |
|---|---|
| Top of the home page | `content/programme/overview.md` |
| Two tracks (NUS / UPenn) | `content/programme/tracks.md` |
| The benchmark game and its four steps | `content/programme/benchmark.md` |
| Layers and "who does what" grid (rows; the cells come from partner files) | `content/programme/stack.md` |
| Flight clips | `content/programme/flights.md`, `content/programme/progress.md` (videos in `public/media/`) |
| Milestones (move `current: true` each year) | `content/programme/milestones.md` |
| Research directions | `content/programme/directions.md` |
| News posts | `content/updates/YYYY-MM-DD-short-title.md` |
| Site title and footer | `content/site.yml` |

---

## 2a. Edit in the browser (no install needed)

1. On GitHub, use the branch menu (top left, it says `main`) to switch to **`development`**.
2. Open your file, e.g. `content/partners/NUS.md`, and click the **pencil** icon.
3. Make your changes. Use the **Preview** tab to check the Markdown formatting.
4. Click **Commit changes…** → keep **Commit directly to the `development` branch** → **Commit changes**.
5. **Adding images:** still on `development`, go to your images folder (e.g. `content/partners/NUS/`),
   click **Add file → Upload files** and commit. Reference the image from your file as
   `![Description of the photo](./NUS/my-photo.jpg)`.
6. Wait about two minutes, then check:
   - the **Actions** tab: a green tick on *CI* and *Deploy site* means the site built and all links work.
     A red cross: click it. The error names the file and field to fix
     (e.g. `partners → nus … summary: Too big`). Fix it on `development` the same way.
   - the **test site** at https://strike-vs-guard.github.io/Strike-Versus-Guard/preview/.
7. When it looks right, tell ST Engineering. They open a pull request from `development` into `main`,
   your partner's code owner approves, and it's merged. The live site updates within a few minutes.

> If the build is red, the test site keeps showing the last version that built, and the live site is
> never affected.

## 2b. Edit on your own computer (live preview while you type)

You need [Git](https://git-scm.com/) and [Node.js 24 LTS](https://nodejs.org/) (22.23.4 or newer also works; check with `node -v`).

```bash
git clone https://github.com/Strike-vs-Guard/Strike-Versus-Guard.git
cd Strike-Versus-Guard
npm ci                      # first time only
git switch development
git pull
npm run dev                 # open http://localhost:4321/Strike-Versus-Guard/
```

The page reloads as you save. When you're done:

```bash
npm run check               # builds the whole site and checks every link, same as CI
git add content/partners/NUS.md content/partners/NUS/
git commit -m "NUS: add October results"
git pull --rebase           # pick up other partners' edits first
git push
```

Then continue from step 6 above. Please don't create other branches; the repository keeps only
`main` and `development`.

> **No Node.js?** Click **Code → Codespaces → Create codespace** on GitHub. It opens an editor in the
> browser with everything installed and the preview running.

---

## 3. Adding a news update

Create `content/updates/2026-11-15-first-outdoor-test.md`:

```markdown
---
title: First outdoor test
date: 2026-11-15
partner: nus            # one of: htx, st, cmu, upenn, nus
author: Jane Tan        # optional
summary: One or two sentences shown on the home page.
image: ./images/outdoor.jpg     # optional, relative to this file
imageAlt: Three drones over a field
draft: false            # true keeps it off the live site
---

The full post in Markdown.
```

The three newest updates appear on the home page, and each partner page lists its own updates.

---

## 4. Images and video

- Use JPG for photos and PNG for diagrams. Keep each under ~1 MB, about 2000 px wide at most. The site
  makes smaller, faster copies automatically.
- Always write a description in the square brackets: `![Two Starling drones crossing paths](./CMU/cross.jpg)`.
  It's read aloud by screen readers.
- Video: MP4 (H.264), muted, under ~10 MB, in `public/media/`. Ask ST Engineering if you need help
  compressing a clip.
- Only publish material you have the right to publish. The test site is public, even before merging.

## 5. Writing style

This is a research programme on **decentralised multi-drone autonomy**. *Strike vs Guard* is the name
of the benchmark game, not the purpose of the programme. Please keep the tone of a lab website:

| Avoid | Use instead |
|---|---|
| intruder, threat, enemy, hostile | Strike team, opposing team, other side |
| defend, protect | hold the zone, Guard team |
| neutralise, intercept, engage, kill | tag, reach, score |
| counter-UAS, counter-drone | decentralised multi-drone autonomy |
| target(s) | goal, zone |
| swarm | drone team, team of drones |

Plain present tense and short sentences work best. Use British spelling (behaviour, decentralised).

## 6. If something goes wrong

| You see | It means |
|---|---|
| `… data does not match collection schema. summary: Too big` | The field is too long; shorten it. |
| `… logo: … could not be found` / `Could not find requested image` | The image path is wrong, or the file isn't uploaded to the same branch. Paths are case-sensitive. |
| `broken link "/Strike-Versus-Guard/…"` | A link points at a page that doesn't exist. For links within the site, copy the address from the live site. |
| Test site didn't change | The *Deploy site* run in the Actions tab is red or still running. Open it to see why. |
| "You can't commit to development" | You need write access. Ask ST Engineering to add you to your partner team. |
| `YAMLException` | Usually a `:` inside a front-matter value. Wrap the value in quotes. |

Questions: open an issue in this repository, or contact the ST Engineering NEAR Lab team.
