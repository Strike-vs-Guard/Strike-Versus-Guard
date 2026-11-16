"""track_fig8.py - per-drone tracks for fig8_twodrones_light.mp4 (fixed ceiling CCTV, 3840x2160, 20 fps, 47.5 s)
and the sync to the ground-station recording Fig8_CBF_two_drones_thermal_ui.mp4. Strike vs Guard video panel.

Run (venv with opencv-python-headless numpy pillow scipy):
    python track_fig8.py              # everything: frames (if missing) -> background -> detect -> track ->
                                      # ground station (gs_fig8.py) -> sync -> events.json -> proof images
Outputs in this folder: tracks.csv, gs-tracks.csv, events.json, first-frame.jpg, traj.png, sheet-a.jpg, sheet-b.jpg,
crossings.jpg.

Method
  * Frames decoded sequentially at full 4K (src/f0001.jpg = frame 0). Background = median of frames 149..899 step 6
    (the drones never hover in one place there, so they vanish from the median).
  * Two cues per frame inside x 900-3400, y 0-1150 (the clock is masked):
      LED  - the drone's green LEDs: G well above R and B, and NOT green in the background (excludes green floor
             tiles). This is what finds the drone against the desks/monitors/people where the dark body vanishes.
      BODY - pixels that differ from the background by > 38 (the dark body/props on the white wall, blur streaks),
             opened 3x3 and dilated 11x11. Body blobs that contain an LED are dropped (the LED stands for them);
             body blobs in the seated-people zone are ignored (people move); one static green light at the far desk
             (x 1093, y 512, appears from ~30 s) is ignored.
  * Assignment: Hungarian, one detection per identity; constant-velocity prediction; gate 45 px + 0.8 x speed
    (px/frame) + 20 px per missed frame; LED preferred over body (body costs +12 px). Coast 6 frames, then hold.
  * Seeds (checked by eye on frame 0, drones on the floor): drone_1 = LEFT (1195, 858), drone_2 = RIGHT (2505, 935).
  * Positions are raw detections (no smoothing): x, y in full 4K pixels; seen = 1 when a detection was assigned.
"""
import cv2, numpy as np, os, sys, csv, json, pickle, glob, subprocess
from multiprocessing import Pool
from scipy.optimize import linear_sum_assignment
from PIL import Image, ImageDraw, ImageFont
S = os.path.dirname(os.path.abspath(__file__))
CAM = os.path.expanduser("~/AirStack-starling-max2/videos/fig8_twodrones_light.mp4")
GSV = os.path.expanduser("~/AirStack-starling-max2/videos/Fig8_CBF_two_drones_thermal_ui.mp4")
FPS = 20.0
SEEDS = [("drone_1", 1195.0, 858.0), ("drone_2", 2505.0, 935.0)]
X0, X1, Y0, Y1 = 900, 3400, 0, 1150
STATIC_LEDS = [(1093, 512, 18)]
PZ = (990, 1250, 380, 640)              # seated people at the far desk
BAND = (760, 2960, 20, 940)             # x0, x1, y0, y1 of the clip band
COL = {"drone_1": (255, 140, 0), "drone_2": (0, 170, 255)}     # RGB: orange, blue
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# ---------------------------------------------------------------- frames, background, detection
def frames():
    os.makedirs(f"{S}/src", exist_ok=True)
    if not glob.glob(f"{S}/src/f*.jpg"):
        subprocess.run(["ffmpeg", "-v", "error", "-i", CAM, "-q:v", "2", f"{S}/src/f%04d.jpg"], check=True)
    if not glob.glob(f"{S}/gs/g*.jpg"):
        os.makedirs(f"{S}/gs", exist_ok=True)
        subprocess.run(["ffmpeg", "-v", "error", "-i", GSV, "-q:v", "2", f"{S}/gs/g%04d.jpg"], check=True)
    if not os.path.exists(f"{S}/bg_flight.png"):
        fs = [cv2.imread(f"{S}/src/f{i:04d}.jpg") for i in range(150, 900, 6)]
        cv2.imwrite(f"{S}/bg_flight.png", np.median(np.stack(fs), axis=0).astype(np.uint8))
    return len(glob.glob(f"{S}/src/f*.jpg"))

_bg = None
def detect(i):
    global _bg
    if _bg is None:
        b = cv2.imread(f"{S}/bg_flight.png")[Y0:Y1, X0:X1].astype(np.int16)
        _bg = (b, b[:, :, 1] - np.maximum(b[:, :, 0], b[:, :, 2]))
    bg, bgG = _bg
    fr = cv2.imread(f"{S}/src/f{i+1:04d}.jpg")[Y0:Y1, X0:X1].astype(np.int16)
    d = np.abs(fr - bg).max(axis=2); d[:210, :1010 - X0] = 0                 # burned-in clock
    G = fr[:, :, 1] - np.maximum(fr[:, :, 0], fr[:, :, 2])
    led = ((G > 35) & (fr[:, :, 1] > 100) & (d > 25) & (G - bgG > 25)).astype(np.uint8)
    led = cv2.dilate(led, np.ones((5, 5), np.uint8))
    n, lab, st, cen = cv2.connectedComponentsWithStats(led)
    leds = []
    for k in range(1, n):
        x, y, w, h, a = st[k]
        if a < 12 or w > 120 or h > 80: continue
        L = lab[y:y + h, x:x + w] == k
        gg = np.clip(G[y:y + h, x:x + w], 0, None).astype(float) * L
        ys, xs = np.nonzero(gg)
        if len(xs) == 0: continue
        ws = gg[ys, xs].sum()
        leds.append((X0 + x + (xs * gg[ys, xs]).sum() / ws, Y0 + y + (ys * gg[ys, xs]).sum() / ws, int(a), float(G[y:y + h, x:x + w][L].max())))
    m = (d > 38).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    m = cv2.dilate(m, np.ones((11, 11), np.uint8))
    n, lab, st, cen = cv2.connectedComponentsWithStats(m)
    blobs = [(X0 + float(cen[k][0]), Y0 + float(cen[k][1]), int(st[k][4]), int(X0 + st[k][0]), int(Y0 + st[k][1]), int(st[k][2]), int(st[k][3]))
             for k in range(1, n) if st[k][4] >= 250]
    return leds, blobs

# ---------------------------------------------------------------- tracking
def in_pz(x, y): return PZ[0] < x < PZ[1] and PZ[2] < y < PZ[3]

def cands(Di):
    leds = [(x, y, 0.0, "L") for x, y, a, g in Di[0] if not any(abs(x - sx) < r and abs(y - sy) < r for sx, sy, r in STATIC_LEDS)]
    out = list(leds)
    for x, y, a, bx, by, w, h in Di[1]:
        if a > 9000 or w > 300 or h > 200 or in_pz(x, y): continue
        if any(bx - 15 <= l[0] <= bx + w + 15 and by - 15 <= l[1] <= by + h + 15 for l in leds): continue
        out.append((x, y, 12.0, "B"))
    return out

def track(D):
    ids = [dict(name=n, x=x, y=y, vx=0.0, vy=0.0, miss=0, last=(x, y)) for n, x, y in SEEDS]
    rows, cue = [], []
    for i in range(len(D)):
        C_ = cands(D[i]); asg = {}
        if C_:
            C = np.full((2, len(C_) + 2), 1e9)
            for qi, q in enumerate(ids):
                px, py = q["x"] + q["vx"], q["y"] + q["vy"]
                gate = 45 + 0.8 * np.hypot(q["vx"], q["vy"]) + 20 * min(q["miss"], 8)
                for k, (x, y, pen, kind) in enumerate(C_):
                    dd = np.hypot(px - x, py - y)
                    if dd <= gate: C[qi, k] = dd + pen
                C[qi, len(C_) + qi] = gate + 15
            r, c = linear_sum_assignment(C)
            asg = {qi: c[j] for j, qi in enumerate(r) if c[j] < len(C_) and C[qi, c[j]] < 1e8}
        for qi, q in enumerate(ids):
            if qi in asg:
                x, y, pen, kind = C_[asg[qi]]
                n = q["miss"] + 1
                q["vx"] = 0.6 * q["vx"] + 0.4 * (x - q["last"][0]) / n if q["miss"] == 0 else 0.5 * q["vx"] + 0.5 * (x - q["last"][0]) / n
                q["vy"] = 0.6 * q["vy"] + 0.4 * (y - q["last"][1]) / n if q["miss"] == 0 else 0.5 * q["vy"] + 0.5 * (y - q["last"][1]) / n
                q["x"], q["y"] = x, y; q["miss"] = 0; q["last"] = (x, y); seen = 1; cu = kind
            else:
                q["miss"] += 1; seen = 0; cu = "-"
                if q["miss"] <= 6: q["x"] += q["vx"]; q["y"] += q["vy"]
                else: q["vx"] *= 0.5; q["vy"] *= 0.5
            rows.append((i, round(i / FPS, 3), q["name"], round(q["x"], 1), round(q["y"], 1), seen)); cue.append(cu)
    return rows, cue

# ---------------------------------------------------------------- drawing helpers
def font(sz): return ImageFont.truetype(FONT, sz)

def annotate(img_bgr, pts, ox, oy, scale, r=46, fs=30, lw=4):
    """pts: list of (name, x, y, seen) in 4K coords; image already cropped at (ox, oy) and scaled by `scale`."""
    im = Image.fromarray(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)); dr = ImageDraw.Draw(im); f = font(fs)
    for name, x, y, seen in pts:
        X, Y = (x - ox) * scale, (y - oy) * scale; c = COL[name]
        dr.ellipse([X - r, Y - r, X + r, Y + r], outline=c, width=lw)
        if not seen: dr.ellipse([X - r - 6, Y - r - 6, X + r + 6, Y + r + 6], outline=(255, 255, 255), width=1)
        tw = dr.textlength(name, font=f); tx = X - tw / 2; ty = Y - r - fs - 10
        if ty < 2: ty = Y + r + 6
        if ty + fs + 6 > im.height: ty = Y - r - fs - 10
        dr.rectangle([tx - 5, ty - 2, tx + tw + 5, ty + fs + 4], fill=c); dr.text((tx, ty), name, font=f, fill=(255, 255, 255))
    return cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)

def stamp(img, text, fs=28):
    im = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)); dr = ImageDraw.Draw(im); f = font(fs)
    tw = dr.textlength(text, font=f); dr.rectangle([0, 0, tw + 16, fs + 12], fill=(0, 0, 0)); dr.text((8, 4), text, font=f, fill=(255, 255, 255))
    return cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)

def frame(i): return cv2.imread(f"{S}/src/f{i+1:04d}.jpg")

def pts_at(T, i): return [(nm, T[nm][i][0], T[nm][i][1], T[nm][i][2]) for nm in ("drone_1", "drone_2")]

# ---------------------------------------------------------------- main
if __name__ == "__main__":
    N = frames()
    if "--redetect" in sys.argv or not os.path.exists(f"{S}/dets.pkl"):
        with Pool(12) as p: D = p.map(detect, range(N), chunksize=4)
        pickle.dump(D, open(f"{S}/dets.pkl", "wb"))
    D = pickle.load(open(f"{S}/dets.pkl", "rb"))
    rows, cue = track(D)
    with open(f"{S}/tracks.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n"); w.writerow(["frame", "t", "name", "x", "y", "seen"]); w.writerows(rows)
    T = {nm: np.array([(r[3], r[4], r[5]) for r in rows if r[2] == nm]) for nm in ("drone_1", "drone_2")}
    cueN = {nm: [c for r, c in zip(rows, cue) if r[2] == nm] for nm in T}
    t = np.arange(N) / FPS

    # ---- ground station: markers + sphere colour (gs_fig8.py), CBF text in the agent table
    subprocess.run([sys.executable, f"{S}/gs_fig8.py"], check=True)
    G = list(csv.DictReader(open(f"{S}/gs-tracks.csv")))
    gsN = max(int(r["gs_frame"]) for r in G) + 1; u = np.arange(gsN) / 30.0
    def gser(nm):
        Sx = [r for r in G if r["name"] == nm and r["x"] != ""]
        return np.array([float(r["u"]) for r in Sx]), np.array([float(r["x"]) for r in Sx]), np.array([float(r["y"]) for r in Sx])
    gs = {nm: gser(nm) for nm in T}

    def cbf_cells(p):
        im = cv2.imread(p).astype(int); o = (im[:, :, 2] > 160) & (im[:, :, 2] - im[:, :, 0] > 60)   # orange text
        return int(o[529:544, 455:505].sum()), int(o[546:561, 455:505].sum())
    with Pool(12) as p: cb = np.array(p.map(cbf_cells, sorted(glob.glob(f"{S}/gs/g*.jpg"))))
    def runs(on):
        e = np.diff(np.r_[0, on.astype(int), 0]); return list(zip(np.where(e == 1)[0], np.where(e == -1)[0] - 1))

    # ---- sync: offset that lets ONE smooth map (cubic in the GS view coords) explain both camera tracks
    def feats(gx, gy):
        gx = (gx - 900) / 200; gy = (gy - 250) / 200
        return np.c_[np.ones_like(gx), gx, gy, gx * gx, gx * gy, gy * gy, gx ** 3, gx * gx * gy, gx * gy * gy, gy ** 3]
    def resid(off, a, b, names=("drone_1", "drone_2"), swap=False):
        A, X, Y = [], [], []
        for nm in names:
            g = gs[{"drone_1": "drone_2", "drone_2": "drone_1"}[nm] if swap else nm]; m = (t > a) & (t < b)
            A.append(feats(np.interp(t + off, g[0], g[1]), np.interp(t + off, g[0], g[2]))[m]); X.append(T[nm][m, 0]); Y.append(T[nm][m, 1])
        A = np.vstack(A); X = np.concatenate(X); Y = np.concatenate(Y)
        cx = np.linalg.lstsq(A, X, rcond=None)[0]; cy = np.linalg.lstsq(A, Y, rcond=None)[0]
        return float(np.median(np.hypot(A @ cx - X, A @ cy - Y)))
    offs = np.arange(18.8, 20.21, 0.02); est = {}
    for key, a, b, nm in [("both 2-36 s", 2, 36, ("drone_1", "drone_2")), ("both 9.5-22 s", 9.5, 22, ("drone_1", "drone_2")),
                          ("both 22-34.5 s", 22, 34.5, ("drone_1", "drone_2")), ("drone_1 2-36 s", 2, 36, ("drone_1",)),
                          ("drone_2 2-36 s", 2, 36, ("drone_2",)), ("take-off 2-9 s", 2, 9, ("drone_1", "drone_2"))]:
        r = [resid(o, a, b, nm) for o in offs]; est[key] = round(float(offs[int(np.argmin(r))]), 2)
    OFF = round(float(np.median(list(est.values()))), 2)
    err = round(max(abs(v - OFF) for v in est.values()), 2)
    swapcheck = [(float(w), round(resid(OFF, w, w + 2), 1), round(resid(OFF, w, w + 2, swap=True), 1)) for w in np.arange(10, 34, 2.0)]

    # ---- events (camera time t; u = t + OFF)
    def first_move(nm, th=8):
        p = T[nm][:, :2]; return float(t[np.argmax(np.hypot(*(p - p[0]).T) > th)])
    def touchdown(nm, th=4):
        p = T[nm][:, :2]; far = np.where(np.hypot(*(p - p[-1]).T) > th)[0]; return float(t[far[-1] + 1])
    sp = {nm: np.hypot(*np.gradient(T[nm][:, :2], axis=0).T) * FPS for nm in T}
    from scipy.ndimage import uniform_filter1d
    def first_lateral(nm, a, b, th=150):         # first frame after a with image speed > th px/s for 5 frames in a row
        v = uniform_filter1d(np.hypot(*np.gradient(T[nm][:, :2], axis=0).T) * FPS, 5)
        for i in range(int(a * FPS), int(b * FPS)):
            if (v[i:i + 5] > th).all(): return float(t[i])
    def descent_start(nm, th=20):                # last time before touchdown the drone was within th px of its hover height
        td = int(touchdown(nm) * FPS); p = T[nm][:, :2]
        i = td
        while i > 0 and p[i, 1] - p[int(36.5 * FPS), 1] > th: i -= 1
        return float(t[i])
    dist = np.hypot(*(T["drone_1"][:, :2] - T["drone_2"][:, :2]).T)
    from scipy.signal import argrelmin
    cross = [int(i) for i in argrelmin(dist, order=8)[0] if 9 < t[i] < 35 and dist[i] < 350]
    cbf_u = [(round(a / 30, 2), round(b / 30, 2)) for a, b in runs((cb[:, 0] > 40) | (cb[:, 1] > 40))]
    sph = {}
    for nm in T:
        Sx = [r for r in G if r["name"] == nm]; prev = None; ch = []
        for r in Sx:
            c = r["sphere"]
            if c in ("unknown", "other"): continue
            if c != prev: ch.append((float(r["u"]), c)); prev = c
        sph[nm] = ch
    ev = {
        "camera": "fig8_twodrones_light.mp4 (20 fps; frame k at t = k/20 s)",
        "ground_station": "Fig8_CBF_two_drones_thermal_ui.mp4 (30 fps; frame j at u = j/30 s)",
        "sync": {"formula": "u = t_camera + offset", "offset_s": OFF, "error_s": err,
                 "how": "offset that best lets one smooth map (cubic in the GS 3D-view pixel coords) explain both camera tracks; median of the per-window estimates",
                 "per_window_estimates_s": est,
                 "clocks_first_guess_s": 19.91,
                 "clocks_note": "camera stamp 17:51:01 begins at frame 5 (t=0.25) -> t=0 is 17:51:00.75; GS clock 9:51:40.847 at u=60.0 -> u=0 is 9:50:40.84; equal clocks would give +19.91 s"},
        "take_off": {"drone_2_first_motion_t": first_move("drone_2"), "drone_1_first_motion_t": first_move("drone_1"),
                     "note": "first frame > 8 px from the floor position; the commander's takeoff command is at GS clock 9:50:58 (u 17.2)"},
        "figure_eight": {"start_t": {nm: first_lateral(nm, 8.0, 13.0) for nm in T},
                         "start_gs_status_u": 29.47, "end_hold_gs_status_u": 53.1,
                         "end_t_from_gs": round(53.1 - OFF, 2),
                         "note": "start = first frame with image speed > 150 px/s for 5 frames (the hover jitter of drone_2's body-only detections is 50-100 px/s); GS status turns 'running' (spheres blue) at u 29.47 and to hold/land (spheres red) at u 53.1 (commander log: hold 9:51:33, land 9:51:38). After the hold the drones brake and coast ~2.4 m sideways to their landing spots."},
        "landing": {nm: {"descent_start_t": descent_start(nm), "touchdown_t": touchdown(nm),
                         "spot_xy": [round(float(T[nm][-1, 0])), round(float(T[nm][-1, 1]))]} for nm in T},
        "landing_note": "drones land on the OPPOSITE sides from where they took off (drone_1 right, drone_2 left); the GS view shows the same swap. drone_1's landing spot (y 992) is below the band (y <= 940).",
        "crossings": [{"frame": i, "t": round(float(t[i]), 2), "u": round(float(t[i]) + OFF, 2), "image_distance_px": round(float(dist[i])),
                       "upper": "drone_1" if T["drone_1"][i, 1] < T["drone_2"][i, 1] else "drone_2",
                       "lower": "drone_2" if T["drone_1"][i, 1] < T["drone_2"][i, 1] else "drone_1",
                       "drone_1_xy": [round(float(T["drone_1"][i, 0])), round(float(T["drone_1"][i, 1]))],
                       "drone_2_xy": [round(float(T["drone_2"][i, 0])), round(float(T["drone_2"][i, 1]))]} for i in cross],
        "crossings_note": "local minima (+-8 frames) of the image distance between the two tracks during the eight; the drones never overlap in the image (closest 150 px)",
        "cbf_active_gs": [{"u_start": a, "u_end": b, "t_start": round(a - OFF, 2), "t_end": round(b - OFF, 2)} for a, b in cbf_u],
        "cbf_note": "CBF activity is read from the orange 'correcting' text in the CBF column of the GS Agent State table (both drones, same episodes +-0.2 s). The spheres do NOT change colour with the CBF (mean ring colour differs < 1 grey level between correcting and clear frames); their colour follows the mission phase.",
        "gs_sphere_colour_changes_u": sph,
        "identity_check_vs_gs": {"window_t": [w for w, _, _ in swapcheck], "median_resid_px_as_named": [a for _, a, _ in swapcheck],
                                 "median_resid_px_if_swapped": [b for _, _, b in swapcheck]},
    }
    json.dump(ev, open(f"{S}/events.json", "w"), indent=1)
    print(json.dumps({k: ev[k] for k in ("sync", "take_off", "figure_eight", "landing")}, indent=1))
    for c in ev["crossings"]: print(c)

    # ---- proof images
    bx0, bx1, by0, by1 = BAND
    # first frame (frame 0: both drones on the floor)
    im = frame(0)[by0:by1, bx0:bx1].copy()
    im = annotate(im, pts_at(T, 0), bx0, by0, 1.0, r=60, fs=40, lw=5)
    cv2.imwrite(f"{S}/first-frame.jpg", stamp(im, "frame 0 (t 0.00 s): drone_1 left, drone_2 right, on the floor", 36), [cv2.IMWRITE_JPEG_QUALITY, 92])
    # trajectory
    ty1 = 1060
    bg = cv2.imread(f"{S}/bg_flight.png")[by0:ty1, bx0:bx1].copy()
    bg = (bg * 0.75).astype(np.uint8)
    pim = Image.fromarray(cv2.cvtColor(bg, cv2.COLOR_BGR2RGB)); dr = ImageDraw.Draw(pim); f = font(34)
    for nm in T:
        P = [(x - bx0, y - by0) for x, y, s in T[nm]]
        dr.line(P, fill=COL[nm], width=4)
        for k in range(0, N, 100):
            x, y = P[k]; dr.ellipse([x - 7, y - 7, x + 7, y + 7], fill=COL[nm]); dr.text((x + 9, y - 30), f"{k/FPS:.0f}s", font=font(24), fill=COL[nm])
    for k, nm in enumerate(T):
        dr.rectangle([20, 20 + k * 52, 70, 60 + k * 52], fill=COL[nm]); dr.text((84, 20 + k * 52), nm, font=f, fill=(255, 255, 255))
    dr.line([(0, by1 - by0), (bx1 - bx0, by1 - by0)], fill=(255, 255, 255), width=1)
    dr.text((10, by1 - by0 + 6), "band bottom (y 940)", font=font(22), fill=(255, 255, 255))
    pim.save(f"{S}/traj.png")
    # contact sheets: 12 tiles each, 2.0 s apart; sheet-a t = 1, 3, ..., 23 s; sheet-b t = 25, 27, ..., 47 s
    def sheet(times, out):
        tiles = []
        for tt in times:
            i = min(N - 1, int(round(tt * FPS)))
            im = frame(i)[by0:by1, bx0:bx1].copy(); im = annotate(im, pts_at(T, i), bx0, by0, 1.0, r=55, fs=44, lw=6)
            im = cv2.resize(im, ((bx1 - bx0) // 3, (by1 - by0) // 3), interpolation=cv2.INTER_AREA)
            tiles.append(stamp(im, f"t {i/FPS:.1f} s  f{i}", 22))
        rows_ = [np.hstack(tiles[k:k + 3]) for k in range(0, 12, 3)]
        cv2.imwrite(out, np.vstack(rows_), [cv2.IMWRITE_JPEG_QUALITY, 90])
    sheet([1 + 2 * k for k in range(12)], f"{S}/sheet-a.jpg")
    sheet([25 + 2 * k for k in range(12)], f"{S}/sheet-b.jpg")
    # crossings: 5 consecutive frames at 2x
    CW, CH = 440, 380; rows_ = []
    for c in ev["crossings"]:
        i0 = c["frame"]; cx = (c["drone_1_xy"][0] + c["drone_2_xy"][0]) / 2; cy = (c["drone_1_xy"][1] + c["drone_2_xy"][1]) / 2
        xa, ya = int(cx - CW / 2), int(cy - CH / 2); tl = []
        for i in range(i0 - 2, i0 + 3):
            im = frame(i)[ya:ya + CH, xa:xa + CW].copy(); im = cv2.resize(im, (CW * 2, CH * 2), interpolation=cv2.INTER_CUBIC)
            im = annotate(im, pts_at(T, i), xa, ya, 2.0, r=50, fs=30, lw=4)
            tl.append(stamp(im, f"f{i} t {i/FPS:.2f}" + ("  closest" if i == i0 else ""), 24))
        rows_.append(np.hstack(tl))
    cv2.imwrite(f"{S}/crossings.jpg", np.vstack(rows_), [cv2.IMWRITE_JPEG_QUALITY, 88])
    print("seen fraction", {nm: float(T[nm][:, 2].mean()) for nm in T}, "LED fraction", {nm: cueN[nm].count("L") / N for nm in T})
    print("done")
