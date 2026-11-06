# Editing the Strike vs Guard website

Each lab owns one Markdown file and one folder of posts. The repository has two branches. You edit
on `development` and check the test site; ST Engineering then merges `development` into `main`, the
live site. You never edit `main`.

| Branch | Site | Address |
|---|---|---|
| `development` | Test site (yellow "Test site" banner, hidden from search engines) | https://strike-vs-guard.github.io/Strike-Versus-Guard/preview/ |
| `main` | Live site | https://strike-vs-guard.github.io/Strike-Versus-Guard/ |

## 0. Quick start

**Option A: in the browser, no install.**

1. Open your lab's page on the test site and click **Edit** at the top. GitHub opens your file on
   `development`. Or on GitHub, switch the branch menu to `development`, open the file, click the pencil.
2. Make your change. The **Preview** tab shows the Markdown formatting.
3. Click **Commit changes…**, keep **Commit directly to the `development` branch**, and commit.
   If GitHub offers only "Create a new branch", you do not have write access yet (section 9).
4. Wait a few minutes, then check the **Actions** tab and the test site (section 5).

**Option B: on your own computer, with a live preview.** You need [Git](https://git-scm.com/) and
[Node.js 24 LTS](https://nodejs.org/) (22.23.4 or newer also works; check with `node -v`).

```bash
git clone https://github.com/Strike-vs-Guard/Strike-Versus-Guard.git
cd Strike-Versus-Guard
npm ci
git switch development
npm run dev
```

`npm ci` installs the site and the git hooks (section 6). `npm run dev` serves the site at
http://localhost:4321/Strike-Versus-Guard/ and reloads it each time you save. No Node.js? On GitHub,
click **Code → Codespaces → Create codespace** for an editor in the browser with everything installed.

When you are done:

```bash
npm run check
git add content/ public/media/
git commit -m "NUS: add October results"
git pull --rebase
git push
```

`git push` goes to the branch you are on (`development`). The hook runs `npm run check` again first.

## 1. Which file is mine?

| Lab | Partner file | Images | Posts |
|---|---|---|---|
| ST Engineering | `content/partners/ST.md` | `content/partners/ST/` | `content/updates/st/` |
| NUS | `content/partners/NUS.md` | `content/partners/NUS/` | `content/updates/nus/` |
| UPenn | `content/partners/UPenn.md` | `content/partners/UPenn/` | `content/updates/upenn/` |
| CMU | `content/partners/CMU.md` | `content/partners/CMU/` | `content/updates/cmu/` |

Your first post creates a posts folder that does not exist yet (section 3). `.github/CODEOWNERS`
lists who reviews which file. ST Engineering keeps `content/partners/HTX.md` (the funder card) and the
shared sections in `content/programme/` and `content/site.yml`; anyone may propose a change to them,
and STANDARDS.md §4 lists which file feeds which section.

## 2. The partner file

The file has two parts. The front matter, between the two `---` lines, holds short fields for the
cards, the people row and the Publications page. The body, after the second `---`, is ordinary
Markdown and becomes your page at `/partners/<id>/` (for example `/partners/nus/`).

### Front-matter fields

`src/content.config.ts` checks every field when the site builds. An unknown field name or a text
over its limit stops the build, with a message naming the file and the field.

| Field | Required | Limit or values | Example |
|---|---|---|---|
| `short` | yes | 24 characters | `NUS` |
| `institution` | yes | text | `National University of Singapore` |
| `lab` | no | text | `MARMoT Lab` |
| `labFull` | no | text; the lab name written out, if `lab` is an acronym | `Multi-Agent Robotic Motion Lab` |
| `labBlurb` | no | 420 characters; "About the lab" text (below) | `We are the …` |
| `lead` | no | text; shown as "Principal investigator" in the page head | `Prof Guillaume Sartoretti` |
| `role` | yes | `Funding sponsor`, `Lead partner` or `Partner` | `Partner` |
| `contribution` | yes | 70 characters; label on your card | `Learning-based strategy track` |
| `summary` | yes | 320 characters; one or two sentences for your card | `The NUS MARMoT Lab leads …` |
| `work` | no | one line per layer, 90 characters each (below) | `strategy: "Leads the …"` |
| `logo` | yes | image path relative to the file; white background, not see-through (section on images) | `./NUS/nus.png` |
| `logoMark` | no | square emblem for the Partners menu; falls back to `logo` | `./NUS/mark.png` |
| `labLogo` | no | lab logo on your page | `./NUS/marmot-lab.png` |
| `logoAlt` | no | logo description; defaults to `institution` | `National University of Singapore` |
| `website` | no | full `https://` address | `https://www.marmotlab.org` |
| `contact` | no | public email address | `lab@example.org` |
| `order` | yes | whole number; fixes the partner order (ST Engineering 2, NUS 3, UPenn 4, CMU 5). Do not change it | `3` |
| `page` | no | `false` shows a card with no page (used for HTX); default `true` | `true` |
| `updated` | yes | `YYYY-MM-DD`; change it when you edit | `2026-11-04` |
| `people` | no | list (below) | |
| `publications` | no | list (below) | `[]` |

`work:` takes one key per layer you work on (`strategy`, `safety`, `flight`, `localisation`,
`drones`, `integration`). Each line puts your lab on that layer in the drone and connection diagrams.

### The body

Write your page as "we", under your own headings. Text, lists, links and images all work. The page
also shows, without any work from you: your people, "About the lab", "Updates from NUS" (your
posts), your publications, and a "Maintained by" line with an Edit link.

### People and "About the lab"

```yaml
people:
  - name: Prof Guillaume Sartoretti
    role: Assistant Professor, Mechanical Engineering
    photo: ./NUS/people/guillaume-sartoretti.jpg
    lead: true
    bio: >-
      Guillaume Sartoretti is an Assistant Professor in Mechanical Engineering at
      NUS and leads the MARMoT Lab. He studies how cooperation emerges in large
      groups of agents making their own choices.
    link: https://www.marmotlab.org/bio.html
  - name: Tanishq Duhan
    photo: ./NUS/people/tanishq-duhan.jpg
```

| Field | Required | Rule |
|---|---|---|
| `name` | yes | As written on papers |
| `role` | no | The actual role. Leave it out if unsure |
| `photo` | no | 400 px square JPG, 80 KB or less, in `content/partners/<NAME>/people/`, named `firstname-lastname.jpg` |
| `lead` | no | `true` for the principal investigator; adds a "PI" tag. Default `false` |
| `group` | no | 40 characters, for example `Interns`. Grouped people appear under their own small heading, after everyone else |
| `bio` | no | 300 characters, third person, two sentences: title, lab, research, degree. No awards or superlatives |
| `link` | no | Full `https://` address of a profile page; shown as "Profile →" |

Only list people who agree to be named. Photos need the person's consent.

**"About the lab"** sits under the people row. It shows `labBlurb:` and every `bio:`, the lead's
first. It is hidden when both are empty. `labBlurb:` is three sentences in "we" voice, 420
characters or fewer: who you are, what you work on, your part in Strike vs Guard. ST Engineering
drafted the first versions from your lab's website; replace them with your own words.

```yaml
labBlurb: >-
  We are the Multi-Agent Robotic Motion Laboratory in Mechanical Engineering at NUS. We work on
  decentralised robot teams where each agent decides for itself. In Strike vs Guard we lead the
  learning track.
```

**"Principal investigators"**, a row on the Partners page, shows from each partner file the first
person with `lead: true` who has a `bio:`, with their photo, `role` and `link`. No bio, no entry.

### Publications

Publications appear on the Publications page and on your own page, newest year first. With no
entries (`publications: []`) the page shows "None yet".

```yaml
publications:
  - title: A paper title
    authors: Zheng, Zang, Amine, Vasile, Mangharam
    venue: IROS 2026
    year: 2026
    status: accepted
    link: https://arxiv.org/abs/2603.13333
```

| Field | Required | Rule |
|---|---|---|
| `title`, `authors`, `venue` | yes | Text |
| `year` | yes | A whole number, no quotes |
| `status` | no | `published` (default), `accepted`, `preprint` or `workshop`. Papers under review are not listed |
| `link`, `pdf` | no | Full `https://` addresses |
| `image` | no | First page or poster, relative to the partner file, for example `./NUS/paper-first-page.jpg` |

## 3. Posts

A post is one Markdown file: `content/updates/<st|nus|upenn|cmu>/YYYY-MM-DD-slug.md`, for example
`content/updates/nus/2026-11-15-first-outdoor-test.md`. Its photos go in
`content/updates/nus/images/`. In the GitHub web editor, use **Add file → Create new file** in
`content/updates/` and type `nus/2026-11-15-first-outdoor-test.md` as the name; the `/` creates
the folder.

```markdown
---
title: First outdoor test
date: 2026-11-15
partner: nus
author: Jane Tan
summary: >-
  One or two sentences shown on the home page and the Updates page.
image: ./images/outdoor.jpg
imageAlt: Three drones over a field
draft: false
gallery:
  - src: ./images/team.jpg
    alt: Five people beside the flight cage
    caption: The team after the last flight.
link: https://arxiv.org/abs/2603.13333
linkLabel: Read the paper
---

The full post in Markdown.
```

| Field | Required | Rule |
|---|---|---|
| `title` | yes | 100 characters |
| `date` | yes | `YYYY-MM-DD` |
| `partner` | yes | `st`, `nus`, `upenn` or `cmu`; must match the folder, or the build stops |
| `author` | no | The person who wrote it. Please fill it in |
| `summary` | yes | 300 characters |
| `image`, `imageAlt` | no | Lead photo relative to the post, and its description |
| `draft` | no | `true` hides the post on both the test site and the live site. Default `false` |
| `gallery` | no | Photo strip: each entry needs `src` and `alt`; `caption` is optional |
| `link`, `linkLabel` | no | One external link (paper, poster PDF, code) and its button text |

Delete the optional lines you do not use. The five newest posts appear on the home page; the
Updates page filters by partner; your partner page lists your own. Write in the first person, with
names, dates and numbers, and end with what is still open.

## 4. Images and clips

**Photos and figures**
- Use JPG for photos and PNG for diagrams. Aim for 1 MB or less and 2000 px wide at most; the build
  refuses any image over 5 MB. The site makes smaller copies itself.
- Paths are relative to the Markdown file and case-sensitive: `./NUS/crazyflie-flight.jpg`, never `/images/…`.
- Insert an image in the body with a description in the brackets, which screen readers read aloud:
  `![Starling 2 Max drones flying in the CMU flight cage](./CMU/starling-flight-cage.jpg)`.
- Check each figure on a white page and on a dark navy page (the header button switches theme).
- **No see-through backgrounds.** Save every PNG (logos included) with a white background. Some
  phone browsers force their own dark mode and repaint the page behind a see-through image, so dark
  artwork disappears. `npm run check` refuses a see-through image and prints the fix.
- Check figures for words baked into them. Crop out wording the site avoids (section 8).
- Credit material from another lab in the caption: "Photo: CMU AirLab." Only publish what you have the
  right to publish. The test site is public too.

**Clips** (full rules: STANDARDS.md §9; `npm run check` enforces the caps)

| Rule | Value |
|---|---|
| Format | MP4, H.264 High, yuv420p, 30 fps, keyframe every 60 frames, `+faststart`, no audio |
| Size | 8 MB or less per file; `public/media/` 60 MB or less in total |
| Poster | JPG, 100 KB or less, same name as the clip |
| Name | `sim-<partner>-<slug>.mp4`, in `public/media/` |
| Caption | Says what to look at ("Watch the gaps between the drones…"), two sentences at most, ends with the credit, for example "Video: AirLab, Carnegie Mellon University, CC BY-SA 4.0; re-encoded." |

To add a simulation clip to your page, convert it (a GIF works as input) and make a poster. Replace
`my-clip.gif` and `sim-nus-myclip` with your own names. Add `-t 12` before the output name to keep
the first 12 seconds.

```bash
ffmpeg -i my-clip.gif -vf "scale='min(1280,iw)':-2,fps=30" -c:v libx264 -profile:v high -crf 28 -pix_fmt yuv420p -g 60 -movflags +faststart -an public/media/sim-nus-myclip.mp4
ffmpeg -i public/media/sim-nus-myclip.mp4 -frames:v 1 -q:v 4 public/media/sim-nus-myclip.jpg
```

Then paste this into your partner file's body where the clip should appear, with your names and
caption. Keep the `../../media/` start: it works on the live site, the test site and your computer.

```html
<figure class="clip"><video controls muted playsinline preload="none" poster="../../media/sim-nus-myclip.jpg" aria-label="Simulation clip: the Guard team holds the zone"><source src="../../media/sim-nus-myclip.mp4" type="video/mp4"></video><figcaption>Watch the five Guard drones (blue) keep three faster Strike drones (red) out of the zone.</figcaption></figure>
```

## 5. Checking your change

**Test site.** Each commit to `development` starts two runs in the **Actions** tab: *CI* (job
"Build and check") and then *Deploy site*. Green ticks on both mean the test site at
https://strike-vs-guard.github.io/Strike-Versus-Guard/preview/ shows your change, a few minutes
after the commit. A red cross: click it, read the message, fix the file on `development`
(section 9). While the build is red, the test site keeps the last version that built. The live site
is never affected.

**`npm run check`** (local clone) builds the whole site the way CI does. It checks every field
against the schema, every internal link and image, the size caps for images and clips, and that no
image under `content/` has a see-through background. It ends with
`✓ … content images checked, none see-through.` when all is well.

**`npm run shots`** takes a screenshot of one page of the built site in a real Chrome. Run
`npm run check` first. It needs Google Chrome installed, or `SVG_BROWSER` set to the path of a
Chrome or Chromium binary.

```bash
npm run check
npm run shots -- /partners/nus/
npm run shots -- /partners/nus/ --theme dark
npm run shots -- /partners/nus/ --width 390
```

The three calls cover desktop light, desktop dark and a phone. Each prints a report and saves a PNG
in `.shots/` (for example `.shots/partners-nus-light-390.png`). The report must end in `"ok": true`:
no sideways overflow, no console errors, no failed requests. Open the PNGs and look at them.

## 6. Publishing

Publishing is one pull request from `development` into `main`. ST Engineering opens and merges it;
tell them when your change looks right on the test site. The live site updates a few minutes after
the merge.

`main` is protected three ways, so a mistake on `development` cannot reach the live site:

| Guard | Installed by | Refuses |
|---|---|---|
| Git hooks (`.githooks/pre-commit`, `.githooks/pre-push`) | `npm ci` (the `prepare` script sets `core.hooksPath=.githooks` and `push.default=current`) | Commits on `main`; pushes to `main`, to a new branch, or that delete a branch; any push where `npm run check` fails |
| Claude Code guard hook (`scripts/claude/guard.mjs`) | `.claude/settings.json`, loaded by Claude Code | The same pushes, plus force pushes, new branches, local merges into `main` and merging a pull request without the site owner's approval |
| GitHub rulesets | Repository settings | Any change to `main` other than a merged pull request whose "Build and check" passed; creating any branch other than `development` and `main` |

Do not create other branches. Only the site owner may override the local hooks; the GitHub
rulesets apply to everyone.

## 7. Using Claude Code on the repository

Open the repository in Claude Code and say "run svg-start". It reads the rules, checks the branch
and asks what you want to do. The skills in `.claude/skills/svg-*` then carry each task:
`svg-change` (any edit), `svg-post` (a post), `svg-debug` (something broken), `svg-panel` (layout or
look) and `svg-release` (publishing, site owner only). The whole process is in
[docs/claude/PROCESS.md](docs/claude/PROCESS.md).

## 8. Writing style

The full rules are in [STANDARDS.md §2](STANDARDS.md). The five that matter most:

1. **Never frame the work as counter-UAS, counter-drone or defence.** The programme is about
   decentralised multi-drone autonomy. *Strike vs Guard* is the name of the benchmark game. Say
   "Strike team" and "Guard team", "hold the zone", "tag" and "drone team", not "intruder", "defend",
   "intercept" or "swarm".
2. **Partners are equals, in the order ST Engineering, NUS, UPenn, CMU.** ST Engineering is the
   lead partner; the others are partners. HTX is the funder, shown separately.
3. **Name people and dates.** "Jeremy flew it on 28 October", not "the team tested it".
4. **Give one number per claim, with its conditions.** "Held the zone in about 20 % of games, two
   Guard drones against one Strike drone, preliminary test", not "promising results".
5. **Say what did not work, and skip self-praise.** No "honest", "robust" or "seamless".

Use plain present tense, short sentences and British spelling (behaviour, decentralised, programme).

## 9. If something goes wrong

| You see | It means | Fix |
|---|---|---|
| `[InvalidContentEntryDataError] partners → nus data does not match collection schema.` followed by a line such as `summary: Too big: expected string to have <=320 characters` or `people.2: Unrecognized key: "bios"` | A field in the named file is too long, misspelled or has the wrong type. `people.2` is the third person (counting starts at 0) | Shorten or correct that field. Check the spelling against the tables in sections 2 and 3 |
| ``[ImageNotFound] Could not find requested image `./NUS/people/Jeric-Lew.jpg`. Does it exist?`` | The path is wrong, the case differs (`Jeric-Lew` is not `jeric-lew`), or the image is not on `development` | Fix the path, or upload the image to the same branch |
| `pre-push: refusing to push to main. Push to development; main changes only via a pull request.` (or `refusing to push branch …`, or `npm run check failed; not pushing.`) | Your local git hook stopped the push | Run `git switch development` and push again. For a failed check, read the lines above the message, fix, commit, push |
| `remote: error: GH013: Repository rule violations found for refs/heads/main.` | GitHub refused a direct change to `main` (or a new branch) | Push to `development` instead. Publishing is a pull request (section 6) |
| The test or live site loads without styling for a few minutes after a deploy | The GitHub Pages cache serves the old page with the new style file names for up to 10 minutes | Wait 10 minutes and hard-refresh (Ctrl+Shift+R). Do not revert or redeploy |

| Other messages | Fix |
|---|---|
| `content/updates/upenn/…md: the post is in the "upenn" folder but says partner: nus. Make them match.` | Set `partner:` to the folder name |
| `Nested mappings are not allowed in compact mappings` (or another YAML error with a line number) | A value contains `: `. Wrap the value in quotes |
| `broken link "/Strike-Versus-Guard/…"` | A link points at a page that does not exist. Copy addresses within the site from the live site |
| `… is 9.1 MB (limit 8 MB). Please compress it.` | Re-encode the clip or shrink the image (section 4) |
| The test site did not change | *Deploy site* in the Actions tab is red or still running. Open it |
| GitHub offers only "Create a new branch" when you commit | You lack write access. Ask ST Engineering to add you to your lab's team |

Questions: open an issue in this repository, or contact the ST Engineering NEAR Lab team.
