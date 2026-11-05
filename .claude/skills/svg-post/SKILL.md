---
name: svg-post
description: Write or edit a news post (update) for a partner on the Strike vs Guard website, in that partner's folder, in the site's voice, with the right fields.
---

# Write an update post

Posts are the thing partners add most often. One Markdown file per post, in the partner's folder.

## 1. Ask for the facts, not the prose
Date, what happened, who did it, numbers (with units and conditions), links (paper, poster, code),
photos or clips and their credit. The post is written in the partner's voice; the author is a
named person.

## 2. File
`content/updates/<partner>/YYYY-MM-DD-slug.md` where `<partner>` is `st`, `nus`, `upenn` or
`cmu`, and the `partner:` field matches the folder (the build fails otherwise).

```markdown
---
title: Three Starlings, three days at CMU
date: 2026-10-02
partner: cmu
author: Yikuan Fang
summary: One sentence, under 160 characters, shown in lists.
draft: true                       # remove when the partner has approved the text
link: https://…                   # optional: paper, poster, code
linkLabel: Paper                  # optional
gallery:                          # optional
  - src: ./images/2026-10-02-cage.jpg
    alt: Three Starling drones hovering in the CMU flight cage
    caption: One or two sentences.
---
Body in Markdown. First person plural ("we flew"), plain present or past tense, short sentences.
```
Images: `content/updates/<partner>/images/`, relative paths, alt text always. Clips: STANDARDS §9.

## 3. Wording (STANDARDS §2)
- Name people and dates. "Jeremy flew it on 28 October", not "the team tested it".
- Numbers with conditions. "0.081 m mean error over 3 flights, camera only".
- No "counter-UAS", "intruder", "target", "threat", "neutralise"; no marketing adjectives.
- Hand-flown or teleop results count only with a video the partner has watched.
- Captions: two to four sentences, 400 characters or fewer.

## 4. Verify and hand over
`npm run check`; `npm run shots -- /updates/<partner>/<slug>/`. Commit as in `svg-change` §6 with
`draft: true`. Give the partner the preview URL and ask them to approve the text; then remove
`draft: true` in a second commit.
