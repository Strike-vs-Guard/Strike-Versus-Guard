---
name: svg-clip
description: Make an annotated flight clip for the Strike vs Guard website (labels that follow the drones, legend, stage captions, ground-station inset), the way the Crazyflie match clip of 6 November 2026 was made. Covers footage, tracking, graphics, wording, encoding, checks.
---

# Make an annotated clip

Reference result: `public/media/st-cf-game.mp4` on the ST Engineering page. Tools and lessons:
`tools/video/README.md`. Rules: STANDARDS §9 "Annotated clips". Run `svg-start` first.

## 1. Footage and facts (before any editing)
- Source files, the camera (fixed?), start/end times, who flew what, the date, the result, tag or
  event times from the match log. Which drone is which in frame 1, from the owner.
- Burned-in captions or overlays in the source: list them. They will be repainted away if they use
  words the site avoids (STANDARDS §2) and replaced by our own.
- Decide the cut: the action plus 5 s before and after; under 45 s.

## 2. Show the first frame first
Extract frame 1, label every drone by name and team from the owner's answer, and show it before
tracking. A wrong seed makes every later frame wrong.

## 3. Track, then design (two agents in parallel, then integrate)
- `svg-video-panel-tracking`: per-frame positions, trajectory plot, contact sheets, crops of every
  crossing, a list of frames checked by eye.
- `svg-video-panel-graphics`: label spec with numbers and mock frames; start from
  `tools/video/label-spec.md`.
- Integrate with `tools/video/integrate.py`; inset with `tools/video/inset_follow.py`.

## 4. Wording on screen
Guard, Strike, VIP drone, "flown by hand", tagged. Never attacker, defender, defence, intruder,
target, pilot, operator, swarm. The banner names the teams and the colours; the bottom caption says
what is happening now; nothing claims more than the ledger does.

## 5. Encode and check
- STANDARDS §9 encoding; 1600 px wide; ≤ 8 MB; poster ≤ 100 KB; `public/media` total ≤ 60 MB.
- Contact sheet every 2.5 s: right number of marks per team in every tile; no label on a drone; no
  banned word anywhere on screen (check the inset too).
- Full-resolution frames at the start, the closest moment and the end.
- `npm run check`; `npm run shots -- /<page>/` light and dark, 1280 and 390.

## 6. Hand over
Push to `development` per `svg-change` §6. Tell the owner: the preview URL, what to watch, the
frames you checked, and what the tracker could not resolve. Keep a copy of the clip and the scripts
outside the scratch folder (the scratch folder is wiped).
