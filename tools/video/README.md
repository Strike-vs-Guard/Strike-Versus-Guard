# Annotated flight clips: the tools behind `st-cf-game.mp4`

The Crazyflie match clip on the ST Engineering page (`public/media/st-cf-game.mp4`, 6 November 2026)
is the reference for every annotated clip on this site. This folder holds the scripts that made it,
so the next clip is made the same way. The rules are in `STANDARDS.md` §9 ("Annotated clips"); the
process is the `svg-clip` skill.

| File | What it does |
|---|---|
| `track2.py` | Follows named drones through a fixed-camera video: background subtraction, lights matched one-to-one (Hungarian) with motion prediction, a dark-blob + template tracker for a larger drone. Seeds (first-frame positions, checked by eye) are at the top. Writes `tracks2.csv` (frame, t, name, x, y, seen). |
| `render_spec.py` | The label scheme (`draw(frame, tracks, t, state)`): halo rings, corner brackets, word pills with leader lines placed where there is free space, tag "pop" and "tagged" pill, banner with legend and tally, caption bar. Numbers in `label-spec.md`. |
| `integrate.py` | Reads `tracks2.csv`, paints out burned-in captions, calls `draw()` per frame, writes PNG frames. |
| `inset_follow.py` | A picture-in-picture crop of a ground-station recording that follows the drones (colour centroids, centred moving average). |
| `label-spec.md` | The graphics spec and the options that were rejected, with reasons. |

## Pipeline

1. **Frames.** `ffmpeg -ss <start> -t <length> -i camera.mp4 -vf fps=30 -q:v 2 src/f%04d.jpg` (1920×1080).
2. **Background.** Median of frames from a stretch where nothing hovers still (see `bg.npy` in `track2.py`).
3. **Seeds.** Open frame 1, write each drone's name, team and pixel position into `track2.py`. Show the labelled first frame to the owner before going further.
4. **Track.** `python track2.py` → `tracks2.csv`, a trajectory plot and two contact sheets. Look at every crossing by eye.
5. **Render.** Set the stage captions and tag times in `render_spec.py` (tag times come from the match log or the source video's own captions), then `python integrate.py` → `out4/`.
6. **Compose.** `ffmpeg -framerate 30 -i out4/f%04d.png -i inset.mp4 -filter_complex "[1:v]scale=832:-2[p];[0:v][p]overlay=W-w-24:H-h-24" …` at the §9 encoding, 1600 px wide, ≤ 8 MB.
7. **Check.** A contact sheet every 2.5 s; counts per team right in every tile; no banned word on screen; `npm run check`; `npm run shots -- /<page>/`.

Python: a venv with `opencv-python-headless numpy pillow scipy`; ffmpeg; DejaVu Sans Bold. Paths in the scripts point at a work folder with `src/`, `bg.npy` and the output folders; change them at the top of each script.

## Lessons that are now rules

- Hand-check the first frame; identity comes from the start position, not from colour. Cameras render LED colours unreliably (red LEDs read pink-white here) and all lights were the same colour before the match.
- A hovering drone blends into a median background; detect only pixels brighter than the background.
- One light, one identity (Hungarian assignment); never let two labels share a light.
- A larger drone (the DJI) is a dark flat blob; track it directly, never infer it from the others.
- Words hide drones: rings always, words only where free, legend in the banner.
- Burned-in captions in the source footage are repainted from the background, never shown: the site's wording rules apply to pixels too.
