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

## Second example: fast drones (`fig8/`)

`public/media/st-fig8-two-starlings.mp4` (two Starlings on CMU's figure-eight at 2 m/s, 16 November 2026).
What differed from the Crazyflie match, and is now part of the method:

- **Review the footage before editing.** A broadcast-editor agent and a first-time-viewer agent compared
  the lights-on and the infrared night recording. Lights-on won (night mode ghosts fast drones; people
  walking). Contrast and gamma edits did not make the drones visible; a zoom and tracked rings did.
- **4K source, 16:9 crop** (x 760–2960 of 3840): the drones are twice as large on screen with no upscaling.
  The crop must hold every take-off and landing spot; check the track's extent before fixing it.
- **Tracking fast drones** (`track_fig8.py`): at 20 fps and 2 m/s a drone moves far between frames. Detect by
  the green LEDs (colour that is not in the background) as well as the dark body, gate = 45 px + 0.8 × speed
  + 20 px per missed frame, Hungarian assignment, identity cross-checked against the ground station, whose
  markers are named. Decode HEVC CCTV files from the start: input seeking returns grey frames.
- **Sync to the ground station** by fitting one smooth map from its marker positions to the camera tracks
  (`gs_fig8.py`); the clocks are only a first guess (here 0.34 s off).
- **Safety-filter state from the ground station's status text**, not from sphere colour (colour follows the
  mission stage). Shown as a status pill in the top bar and on the close-up panel. The first version drew a
  white outer ring; the owner pointed out it reads as the CBF zone, whose radius it did not match. Removed.
- **Layout** (`render_layout_b.py`, final): footage in a left block, right column with the ground station
  over an always-on 2× close-up of the meeting point. The first version (`render_fig8.py`: inset in the
  middle of the floor, a 2× window popping up at each meeting) was judged distracting by the owner, a
  broadcast-editor agent and a first-time-viewer agent. Five layouts were rendered as samples; the owner chose
  B, plus the half-speed replay from the editor's version (`integrate_layout_b.py`: 1.8 s of source at half
  speed, a 1466 px crop of the 4K frame across the full width, inserted at the hold).
- **Track smoothing** (`smooth_tracks.py`): a hovering drone with its lights off wobbled 20 px; smoothing by
  speed brought frame-to-frame wobble from 7.4 px to 0.1 px there without moving the marks off fast drones.
- **Source 20 fps, output 30 fps:** show source frame ⌊t·20⌋ and put the marks on that frame's position; no
  interpolation.

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
