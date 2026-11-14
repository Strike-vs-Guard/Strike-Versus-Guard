# Hangar clip: labelling spec

All sizes are px in the 1920×1080 source. The final clip is ×0.83 (1600 px) and ×0.44 on a landscape phone. Reference implementation: `render_spec.py`, `draw(frame, tracks, t)`.

**Rule.** A mark is always shown on every seen drone. A word appears only when a free spot exists for it, and a word never covers any mark. In the melee, the banner legend names the marks.

## Marks (always on, only while a track is seen; no mark on a coasting or lost track)
| Object | Mark | Numbers |
|---|---|---|
| Guard | full ring, blue `#3B82F6` | radius 17 to stroke centre, stroke 4, under a dark halo stroke 8 (`#0C0C0C`, α 170) |
| Strike | full ring, red `#EB3C3C` | same as Guard |
| the zone (DJI) | 4 white corner brackets, no ring | box half-size 42, arm 18, stroke 4, halo 8 |
| Strike, tagged | dashed ring, red, α 0.8 | stroke 3, 8 dashes of 25° with 20° gaps |

The halo keeps a blue ring visible on a blue tile and a red ring on a red tile. The ring's inner clear radius is 15 px, so it frames the 10 px light and never covers it.

## Words: pills with a leader line
- Pill: DejaVu Sans Bold **28 px**, padding 10×5, radius 8, 2 px outline. Guard and Strike: team-colour fill (α 0.92) with white text. The zone: white fill with black text. Leader: 3 px in the pill colour on a 7 px halo, from the mark's edge to the pill's nearest point.
- Words: `Guard`, `Strike`, `the zone`, `tagged`. Nothing else.
- When words show:

| Window | Words |
|---|---|
| 0–12.0 s | all 8 (fade out 12.0–12.4) |
| 14.0–17.0 s | the 3 Strike only (0.4 s fades) |
| 17–27.5 s | rings only (the owner's idea) |
| from 27.5 s | all seen drones again |
| always | `the zone` |
| tag event | `tagged` |

- **Placement.** Try 12 directions (every 30°, starting straight up) × leader lengths 20 / 55 / 100 px from the mark's edge. Tag pills and the zone also try 150 / 210. Pick the lowest cost: 0.4·length + 4 per 30° away from "up". A candidate is rejected (+1000) if the pill overlaps any mark box (mark + 6 px), another pill (+6 px), the area outside x 12–1908 / y 140–866, or the inset (x ≥ 1340, y ≥ 640). A leader that crosses another mark costs +300. If nothing scores under 1000, the word is dropped and the ring stays. Place in priority order: `tagged` pills, then the zone, then team words.
- **Video only.** Keep the previous slot (+40 to change). Ease the pill toward a new slot over 6 frames.

## Tag event (time T per Strike drone, from the match log)
- T to T+0.5 s: a white "pop" ring expands from r 17 to 45 while its stroke thins from 4 to 1 and its alpha drops from 1 to 0.
- From T on, the ring is dashed (see Marks).
- T to T+2.0 s: a `tagged` pill (white, red text and outline, red leader; 0.2 s in, 0.4 s out).
- From 27.5 s, tagged drones show `Strike` as a dark pill (`#1C1C1C`, red outline, text `#FF9696`).
- The banner tally turns one Strike icon into a dashed ghost, filling from the right.

## Banner (legend and tally) and caption
- Full-width bar y 75–131 (`#0E0E0E`, α 0.92). It also hides the camera timestamp.
- Left: `Strike vs Guard · 6 Nov 2026`. Right: `○○○○ Guard   ○○○ Strike   ⌜⌟ the zone (DJI, flown by hand)`, 30 px. The icons are the on-video marks at r 10 / stroke 4.
- Caption bar: unchanged (y 878–960, 34 px), but auto-shrink to ≥ 26 px so the text ends left of x 1316. At 34 px the 27 s caption runs under the inset.

## Rejected
- **Words on everything, always** (current). Eight 22 px tags in a 400×250 px melee stack up and hide the drones and the DJI. Repelling them just moves the pile.
- **Pure rings, no words ever.** A first-time viewer can't tell blue from red without a key. The intro words plus the banner legend give that key.
- **Numbered rings G1–G4 / S1–S3.** Numbers can't be read at phone size. The viewer doesn't need individual identities, and a tracker ID swap would show a wrong number on screen.
- **Isolation trigger** (a word when a drone is more than X px from the others). Words pop in and out during the fastest action and pull the eye. Fixed windows plus the free-spot test are calmer.
- **Labels pushed to the image edge.** Leaders 600 px long cross the action and other drones.
- **A ring or tag on the DJI.** A ring that fits the 50 px quad looks like a team ring. Brackets read as "this object", the way a camera's focus box does.
- **Fade the tagged drone's mark out.** The viewer loses where it went. A dashed ghost keeps it visible but clearly out.
