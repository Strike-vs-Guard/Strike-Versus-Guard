# Figure-eight clip (lights on, 16 Nov 2026): graphics spec

All px are at 1920×1080 (published ×0.83 at 1600, ×0.44 on a landscape phone). Implementation: `render_fig8.py` `draw()`. House numbers (`tools/video/label-spec.md`) apply where not changed here.

## 1. Canvas
| Rectangle | px (x0, y0, x1, y1) | Notes |
|---|---|---|
| Camera | full canvas = 4K crop x 760–2960, y 0–1237.5 (16:9), scale 0.8727 | holds both take-offs, the eight (top y 110 4K → 114 px), both landings (y 992 4K → 866 px) |
| Legend bar | 0, 0, 1920, 56 | `#0E0E0E` α 0.92 |
| Caption bar | 0, 998, 1920, 1080 | `#141414`, 34 px, auto-shrink to ≥ 26 px, x 44 |
| Ground-station inset | 568, 528, 1304, 982 | strip 40 + picture 736×414; whole clip; over the empty centre floor |
| Crossing window | 1336, 422, 1896, 982 | strip 40 + picture 560×520; only while open; over the right floor, empty in mid-flight |

Checked against every tracked frame: no ring touches either panel or bar (closest: 13 px under the inset at 11.3 s). The right floor holds drone_2's take-off pad and drone_1's landing spot, but the window is shut then (last one closes at 32.0 s, descent starts at 38.0 s). The house bottom-right inset is not used here: it would cover both of those spots.

## 2. Marks
- Ring per seen drone: r 44 (to stroke centre), stroke 4, halo 8 `#0C0C0C` α 170. Inner clear r 40 encloses a 52–79 px drone. drone_1 `#3B82F6`, drone_2 `#E8590C`. No ring on a drone that is not seen.
- Trail: last 1.0 s of seen positions; 6 px at the drone → 2 px, α 0.85 → 0, under a 4 px wider halo at α 0.35. It starts at the ring edge and breaks at gaps over 0.16 s.
- Name pills `drone_1` / `drone_2` (28 px, team fill, house placement with the inset and an open window as keep-outs): 0–11.0 s and from 33.6 s, with 0.4 s fades.
- At 30 fps output, show source frame ⌊t·20⌋ (cadence 2,1,2,1). Rings and trail heads use that same frame's position; they are never interpolated, because a ring 9 px off a 2 m/s drone reads as wrong. Pills ease as in the house scheme.

## 3. Crossing window
- **Opens** for each image crossing in `events.json` with distance ≤ 250 px (4K) inside a ground-station "correcting" episode. That gives one window per episode: 12.3 + 13.9 (merged), 18.05, 21.75, 27.35, 31.15 s. Crossings at 23.2 and 32.55 s are 300+ px apart and do not fit.
- **Timing:** opens at t_ca − 0.8 s and closes at t_ca + 0.8 s, with 0.2 s alpha fades. Windows less than 0.4 s apart merge, and the view eases between the two midpoints over 0.4 s. It is not held for the whole episode: after ±0.5–1.0 s the drones are 550–970 px apart.
- **Content:** a live 2× view of the same source frame (1.745 px per 4K px = 321×298 4K px), fixed on the pair's midpoint at t_ca. Rings (r 88) and trails are drawn at 2× with strokes left at 4 px. Frame, shadow and strip match the inset. Title `Crossing · 2×`.
- **Safety filter acting** (only during the ground-station episodes 11.43–14.56, 16.40–18.80, 21.23–23.80, 25.83–28.20, 30.63–33.16 s): a white pill `safety filter acting` (22 px) on the right of the window strip; a white outer ring (r 54, stroke 2, halo 5 α 120) on both drones; and a white pop ring at each episode start (r 44 → 96 over 0.5 s, stroke 4 → 1, fading out). No distance appears anywhere.

## 4. Words (§2-checked: no pilot, operator, intruder, target, swarm)
- Legend bar, left: `CMU's figure-eight · lights on · 16 Nov 2026`. Right: `◯ drone_1  ◯ drone_2  ◎ safety filter acting` (30 px).
- Inset strip: `Ground station · Sphere = CBF Safety Assist Zone` (24 px).
- Captions, one per stage (shortest 4.4 s):

| t (s) | Caption |
|---|---|
| 0–10.1 | Take-off: two Starling 2 Max drones climb to their start points. Nobody is on the sticks. |
| 10.1–16.4 | CMU's figure-eight at 2.0 m/s, flown in Singapore. Nobody is on the sticks. |
| 16.4–25.8 | Each time they meet head-on, the safety filter eases them apart. Watch the 2× window. |
| 25.8–33.5 | The white outer ring shows while the ground station reports the filter correcting. |
| 33.5–38.0 | The eight ends: both drones brake, hold, then move off to their landing spots. |
| 38.0–end | Landing: watch them swap sides. drone_1 lands on the right, drone_2 on the left. |

## 5. Burned-in text and people
- The clock's cut-off tail (`:51:13`, 4K x 760–1010, y 120–190) is inpainted (dark-pixel mask, dilate 7, Telea r 7). The date is in the banner. `Camera 01` falls under the caption bar.
- The two seated people stay uncovered. A patch would draw the eye, and the caption already says nobody is on the sticks.

## Inset follow
Crop 491×276 ground-station px (zoom 1.5) inside the 3D view below its header (600, 100, 1250, 440), centred on a 1 s centred moving average of the markers' midpoint (`gs-tracks.csv`), clamped to the view. Sync: u = t + 19.57 s.
