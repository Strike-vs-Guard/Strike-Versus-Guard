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
lab: MARMoT Lab                      the partner card on the home page
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
- `logoMark:` (optional) is a square crop of just your emblem, e.g. `./NUS/mark.png`; the Partners menu shows it, or `logo:` if absent.
- `work:` has one line (max 90 characters) for each layer you work on: `strategy`, `safety`, `flight`,
  `localisation`, `drones`, `integration`. These lines put you on the layers of the drone diagram and the connection diagram on the Partners page.
- Dates are `YYYY-MM-DD`.
- `people:`, `open:` and `openLabel:` are explained in sections 1a and 1b below.

Your page is linked from the **Partners** menu in the header and from the Partners page. Your file
is the only place its text lives, and your page says "Maintained by <you>" with an Edit link.

The site has Home, Research (was Programme; `/programme/` redirects), Partners, Flights, Publications, Contribute and Updates. The shared files below
feed them. They are owned by ST Engineering, but anyone may propose changes. The October 2026 monthly
report is approved for publication; please do not publish anything numeric or unpublished from the
other programme reports.

| What | File |
|---|---|
| Top of the home page: the `decisions:` list ("What they decide"), `video:` (the hero clip, in `public/media/`), `gameNote:` (one line about the game) and the Research page head (`pageEyebrow:`, `pageTitle:`) | `content/programme/overview.md` |
| Home "Proof so far" section head and its one-line `note:` | `content/programme/proof.md` |
| Research "In simulation" section (one paragraph, 2–4 clips) | `content/programme/simulation.md` (videos in `public/media/`) |
| Localisation section and its one-line `status:` | `content/programme/localisation.md` |
| Two tracks (NUS / UPenn) | `content/programme/tracks.md` |
| The benchmark game and its four steps | `content/programme/benchmark.md` |
| Layers and "who does what" grid (rows; the cells come from partner files) | `content/programme/stack.md` |
| Flight clips | `content/programme/flights.md`, `content/programme/progress.md` (videos in `public/media/`) |
| Milestones (move `current: true` each year) | `content/programme/milestones.md` |
| Home "At a glance" status lines (`state:` = Done, In progress, Not yet; `note:` is the "as of" date) | `content/programme/glance.md` |
| Home "Research themes" (five rows) | `content/programme/themes.md` |
| Research directions | `content/programme/directions.md` |
| News posts | `content/updates/<partner>/YYYY-MM-DD-short-title.md` (one folder per partner: `st`, `nus`, `upenn`, `cmu`) |
| Site title, footer, programme `start:` / `end:` | `content/site.yml` |

---

### 1a. Add yourself to `people:`

Each partner file lists its team. The partner page shows them as a row with faces.

```yaml
people:
  - name: Jane Tan
    role: PhD student
    photo: ./NUS/people/jane-tan.jpg
  - name: Prof Guillaume Sartoretti
    role: Principal investigator
    photo: ./NUS/people/guillaume-sartoretti.jpg
    lead: true
```

| Field | Rule |
|---|---|
| `name` | As you write it on papers |
| `role` | Your actual role. Leave it out if you are unsure |
| `photo` | 400 px square JPG, 80 KB or less, in `content/partners/<Name>/people/` (e.g. `./NUS/people/jane-tan.jpg`). Optional |
| `lead` | `true` for the principal investigator or lead |
| `group` | Optional, e.g. `Interns`. Grouped people show under their own small heading, after everyone else |
| `bio` | Optional. Two sentences in the third person, 300 characters or fewer: title, lab, what you study, degree. No awards or superlatives. Shown in "About the lab" |
| `link` | Optional profile page for the bio, e.g. your staff page |

Only add people who agree to be named. Photos need the person's consent.

**"About the lab"** sits under the people row. It shows `labBlurb:` (three sentences in "we" voice,
420 characters or fewer: who you are, what you work on, your part in Strike vs Guard) next to the
bios above. ST Engineering drafted the first versions from your lab's website; replace them with your
own words.

```yaml
labBlurb: >-
  We are the Multi-Agent Robotic Motion Laboratory in Mechanical Engineering at NUS. We work on
  decentralised robot teams where each agent decides for itself. In Strike vs Guard we lead the
  learning track.
```

### 1b. The open-problems list

Sections that report results end with what is not solved: `open:` (one line each) and
`openLabel:` (e.g. "What we haven't solved yet"). It is in `localisation.md` and `simulation.md`. Write what did not work or is still open, in plain words, with a number if you have one.

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

Each partner has its own folder of updates: `content/updates/st/`, `content/updates/nus/`,
`content/updates/upenn/` and `content/updates/cmu/`. Create a file in yours, e.g.
`content/updates/nus/2026-11-15-first-outdoor-test.md`, with photos in `content/updates/nus/images/`:

```markdown
---
title: First outdoor test
date: 2026-11-15
partner: nus            # one of: htx, st, cmu, upenn, nus
author: Jane Tan        # the person who wrote it
summary: One or two sentences shown on the home page.
image: ./images/outdoor.jpg     # optional, relative to this file
imageAlt: Three drones over a field
draft: false            # true keeps it off the live site
gallery:                # optional strip of photos, relative to this file
  - src: ./images/team.jpg
    alt: Five people beside the flight cage
    caption: The team after the last flight.
link: https://arxiv.org/abs/0000.00000   # optional paper, poster or code link
linkLabel: Read the paper
---

The full post in Markdown.
```

The three newest updates appear on the home page, the Updates page has a filter by partner, and each partner page lists its own updates ("No posts yet. Post one →" until you add one).
`gallery:` is a strip of photos shown under the post (`src:` relative to the post, `alt:` required,
`caption:` optional; same image rules as section 4). `link:` and `linkLabel:` add one external link
(paper, poster PDF, code). Both are optional. Updates are a dated log, so:

- Put your name in `author:`.
- Write in the first person ("we flew…", "I tried…"), with dates and numbers.
- End with what is still open.

---

## 3a. Adding a publication

Publications are listed in your partner file and shown on the **Publications** page (one section per
partner) and in your own page. Add them under `publications:`:

```yaml
publications:
  - title: A paper title
    authors: Zheng, Zang, Amine, Vasile, Mangharam
    venue: IROS 2026
    year: 2026
    status: accepted            # published | accepted | preprint | workshop (default: published)
    link: https://arxiv.org/abs/0000.00000    # optional
    pdf: https://example.org/paper.pdf        # optional
    image: ./UPenn/paper-first-page.jpg       # optional first page or poster, relative to this file
```

| Field | Rule |
|---|---|
| `title`, `authors`, `venue`, `year` | Required. `year` is a number |
| `status` | One of the four words above. Papers under review are not listed |
| `link`, `pdf` | Full `https://` addresses |
| `image` | Optional; same size limits as other images |

With no entries the page shows "None yet (as of <date>)". Check the Publications page on the test site.

## 3b. The Contribute page and the theme

The **Contribute** page (header, last item) shows the same steps as this file in short form: "Which
file is mine?", add a person or photo, post an update, add a publication. Point new colleagues there.

The site has a light and a dark theme, and a sun/moon button in the header switches them. Nothing to
do as a partner. Just check your images look right on both: logos get a white well automatically;
diagrams and figures should work on a white page and on a dark navy page (avoid transparent PNGs with
black text).

## 4. Images and video

- Use JPG for photos and PNG for diagrams. Keep each under ~1 MB, about 2000 px wide at most. The site
  makes smaller, faster copies automatically.
- Always write a description in the square brackets: `![Two Starling drones crossing paths](./CMU/cross.jpg)`.
  It's read aloud by screen readers.
- Posters are frames from the flight footage (the bottom half of the clip), not stock images.
- Video: MP4 (H.264), muted, under ~10 MB, in `public/media/`. Ask ST Engineering if you need help
  compressing a clip.
- Partner-supplied clips carry a "Video: <lab>" credit in the caption (photos: "Photo: <lab>").
- Every clip caption says what to look at, starting with "Watch …": "Watch the gaps between the drones
  as they swap places." Two sentences at most.
- Only publish material you have the right to publish. The test site is public, even before merging.

**Clip ladder (full rules: STANDARDS §9).** Loops 15 s or less and 1 MB or less; lead clips 1080p CRF 26, 8 MB or less; grid clips 720p CRF 28 to 30; posters 100 KB or less; 8 MB per file.
**Credit rule:** partner clips say who made them and the licence, and say "re-encoded" or "cropped" if you changed them. Items take `videoAlt`, `posterAlt`, `altLabel` and `credit` fields for the description, poster description, short label and credit line.

### Adding a simulation clip to your partner page

1. Convert the clip (a GIF works too) to MP4 and grab its first frame as the poster:

   ```bash
   ffmpeg -i in.gif -vf "scale='min(960,iw)':-2" -c:v libx264 -crf 28 -pix_fmt yuv420p -movflags +faststart -an public/media/sim-nus-selfplay.mp4
   ffmpeg -i in.gif -frames:v 1 public/media/sim-nus-selfplay.jpg
   ```

   Name both `sim-<partner>-<slug>` and put them in `public/media/`. Aim for about 3 MB or less
   (add `-t 12` to keep the first 12 seconds); `npm run check` fails anything over 8 MB, or a media folder over 60 MB.
2. Paste this into your `.md` file where the clip should appear, with your file names and a one-line
   caption. Keep the `../../media/` start exactly as written: it works on the live site, the test site
   and your own computer.

   ```html
   <figure class="clip"><video controls muted playsinline preload="none" poster="../../media/sim-nus-selfplay.jpg" aria-label="Simulation clip: the Guard team holds the zone"><source src="../../media/sim-nus-selfplay.mp4" type="video/mp4"></video><figcaption>Five Guard drones (blue) keep three faster Strike drones (red) out of the zone.</figcaption></figure>
   ```

3. Stills from simulation go in your images folder as `sim-<slug>.jpg` or `.png` (about 1400 px wide
   and 400 KB at most) and use the normal image line. Check figures for words baked into them
   (section 5): crop or skip any that use the "Avoid" column.

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

Plain present tense and short sentences work best. Write as "we" on your own page, name people and
dates, give one number per claim, say what did not work, and skip words like "honest" or "robust".
Full list: STANDARDS §2. Use British spelling (behaviour, decentralised).

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
