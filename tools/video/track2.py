"""track2.py - per-drone tracker for the Strike-vs-Guard hangar clip (successor of track.py).

Same input (src/f*.jpg, bg.npy) and the same drawing/captions as track.py; writes out3/ and tracks2.csv.
Differences from track.py (see the report for the evidence behind each one):
  * The DJI has its own detector: a wide, flat DARK blob (the airborne DJI is ~55x22 px, 800-1200 px after
    dilation, so track.py's "big blob" test a>1400 never fired after lift-off at t~4.6 s). When the blob is
    missing, a grey-level template (NCC) of the DJI's last good patch is searched around the prediction.
    The escort-centroid fallback is gone: during the match the escorts are up to ~200 px from the DJI.
  * Crazyflie lights are detected on POSITIVE differences only (bright and brighter than the background), so a
    light no longer merges with a dark body next to it (DJI, hover-spot ghost, another drone); the DJI's green
    LEDs and lights inside the DJI outline are ignored.
  * Assignment is Hungarian (one light per identity, one identity per light) in three rounds: identities seen in
    the last 3 frames pick first; identities lost for longer may then take a light nobody wants, with a gate that
    grows with the time lost (up to 135 px); finally dim lights very close to an unmatched identity.
    Raw detection positions (no 50 % smoothing lag), constant-velocity prediction, coast 3 frames then hold.
  * Colour is used one way only during the match: the light's colour is measured on pixels that are both bright
    and changed versus the background (so floor tiles do not count); a clearly red/pink light is penalised for a
    Guard. Blue is NOT evidence for a Guard (S2's light reads cyan; tagged Strike drones show blue power LEDs).
  * Known static light sources at the far end (monitor/table lights) are ignored; a second, relaxed pass picks up
    dim lights (landed Strike drones) only very close to the prediction.
  * Two passes: detections are computed for all frames first (in parallel), then tracked, then frames are drawn.
Run:  venv/bin/python track2.py            (track + draw out3/)
      venv/bin/python track2.py --no-draw  (track only: tracks2.csv)
"""
import cv2, numpy as np, glob, os, sys, csv
from multiprocessing import Pool
from scipy.optimize import linear_sum_assignment
from PIL import Image, ImageDraw, ImageFont
S = os.path.dirname(os.path.abspath(__file__))
files = sorted(glob.glob(f"{S}/src/f*.jpg")); N = len(files)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
f_lab = ImageFont.truetype(FONT, 22); f_ban = ImageFont.truetype(FONT, 26); f_cap = ImageFont.truetype(FONT, 34)
bg = np.load(f"{S}/bg.npy"); bgg = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY).astype(int); bgi = bg.astype(int)
COL = {"Guard": (246, 130, 59), "Strike": (60, 60, 235), "DJI": (30, 30, 30)}
TXT = {"Guard": "Guard escort", "Strike": "Strike", "DJI": "DJI (the zone)"}
def stage(t):
    if t < 14: return "The DJI lifts off; the four Guard escorts hold a ring above it"
    if t < 15: return "Ready"
    if t < 22.5: return "Match on: three Strike drones go for the DJI"
    if t < 25.5: return "A Guard escort tags the first Strike drone"
    if t < 27: return "Two more tags"
    return "Guard team wins: all three Strike drones tagged, the DJI never reached"
SEEDS = [("G1", "Guard", 739, 319), ("G2", "Guard", 1100, 329), ("G3", "Guard", 1303, 439), ("G4", "Guard", 825, 448),
         ("S1", "Strike", 905, 622), ("S2", "Strike", 707, 637), ("S3", "Strike", 473, 641), ("DJI", "DJI", 985, 504)]
MATCH_T = 14.5
# fixed light sources that are not drones (blinking monitor / table lamp at the far end, wall light far left)
STATIC_LIGHTS = [(1046, 256, 14), (393, 235, 14)]
PERSON = (650, 900, 330)          # x0, x1, ymax: the pilot standing at the far end

def paint(fr, t):
    if t >= 22:   # the original finale caption boxes: paint the floor back (as track.py)
        g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY).astype(int)
        for y in range(580, 965):
            dark = (g[y, :1200] < 62) & (bgg[y, :1200] - g[y, :1200] > 35)
            if dark.sum() > 120:
                xr = min(1200, int(np.where(dark)[0].max()) + 14); fr[y, :xr] = bg[y, :xr]
    return fr

def light_colour(fr, dif, x, y, r=12):
    """(R-B, G-max(R,B)) of pixels near (x,y) that are bright AND brighter than the background: the light's own
    colour, so the floor tile under it does not count. Strike deck lights are pink (R-B > 0); the DJI's LEDs are green."""
    y0, y1, x0, x1 = max(0, y - r), y + r + 1, max(0, x - r), x + r + 1
    f = fr[y0:y1, x0:x1].reshape(-1, 3).astype(int); dd = dif[y0:y1, x0:x1].reshape(-1, 3)
    sel = (f.max(axis=1) >= 170) & (dd.max(axis=1) >= 40)
    if sel.sum() < 3: return 0.0, 0.0
    f = f[sel]
    return float((f[:, 2] - f[:, 0]).mean()), float((f[:, 1] - np.maximum(f[:, 0], f[:, 2])).mean())

def merge_close(dets, r=12):
    out = []
    for d in sorted(dets, key=lambda d: -d[3]):
        if all((d[0] - o[0]) ** 2 + (d[1] - o[1]) ** 2 > r * r for o in out): out.append(d)
    return [(d[0], d[1], d[2]) for d in out]

def detect(i):
    t = i / 30.0; fr = paint(cv2.imread(files[i]), t)
    dif = fr.astype(int) - bgi
    # Lights: pixels that are BRIGHT and BRIGHTER than the background. track.py used |frame-bg| and a 7x7 dilation,
    # so a light merged with any dark body next to it (the DJI, a ghost of a hover spot, a second drone) into one
    # blob that was then rejected or mislocated; positive-only differences keep the lights separate.
    up = dif.max(axis=2); vmax = fr.max(axis=2)
    m = ((up > 40) & (vmax >= 140)).astype(np.uint8); m[:230, :] = 0; m[878:, :] = 0
    m = cv2.dilate(m, np.ones((3, 3), np.uint8))
    n, lab, st, cen = cv2.connectedComponentsWithStats(m)
    strong, weak = [], []
    for k in range(1, n):
        x0, y0, w, h, a = st[k]
        if a < 6 or a > 900 or w > 60 or h > 60: continue
        L = lab[y0:y0 + h, x0:x0 + w] == k
        vv = vmax[y0:y0 + h, x0:x0 + w][L]; uu = up[y0:y0 + h, x0:x0 + w][L]
        ys, xs = np.nonzero(L); wgt = np.clip(uu, 0, None).astype(float) + 1.0
        x, y = float(x0 + (xs * wgt).sum() / wgt.sum()), float(y0 + (ys * wgt).sum() / wgt.sum())
        if any(abs(x - sx) < r and abs(y - sy) < r for sx, sy, r in STATIC_LIGHTS): continue
        hot = int((vv >= 200).sum()); peak = int(vv.max())
        red, green = light_colour(fr, dif, int(x), int(y), 6)
        if green > 15: continue                       # the DJI's green LEDs
        if hot >= 6 and peak >= 220: strong.append((x, y, light_colour(fr, dif, int(x), int(y))[0], hot))
        elif peak >= 170 and L.sum() >= 9: weak.append((x, y, 0.0, hot))
    strong, weak = merge_close(strong), merge_close(weak)
    weak = [w for w in weak if all((w[0] - s_[0]) ** 2 + (w[1] - s_[1]) ** 2 > 144 for s_ in strong)]
    # DJI candidates: wide, flat blobs DARKER than the floor (grey body + props), not the pilot
    g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY).astype(int)
    dk = ((bgg - g) > 30).astype(np.uint8); dk[:230, :] = 0; dk[878:, :] = 0
    dk = cv2.dilate(dk, np.ones((7, 7), np.uint8))
    n, lab, st, cen = cv2.connectedComponentsWithStats(dk)
    dji = []
    for k in range(1, n):
        x0, y0, w, h, a = st[k]
        if not (40 <= w <= 85 and 12 <= h <= 48 and w >= 1.4 * h and a >= 400): continue
        x, y = float(cen[k][0]), float(cen[k][1])
        if PERSON[0] < x < PERSON[1] and y < PERSON[2]: continue
        dji.append((x, y, int(w), int(h), int(a)))
    return strong, weak, dji

def gray(i):
    return cv2.cvtColor(paint(cv2.imread(files[i]), i / 30.0), cv2.COLOR_BGR2GRAY)

def colour_pen(cls, red, t):
    # Only one direction is trustworthy: a clearly pink/red light is a Strike drone. Blue does NOT mean Guard:
    # S2's light reads cyan until ~t 21 s, and tagged Strike drones switch the deck light off and show only the
    # two blue power LEDs while they descend (measured on conservative tracklets, see report).
    if t < MATCH_T: return 0.0
    if cls == "Guard" and red > 25: return 60.0
    if cls == "Guard" and red > 12: return 25.0
    return 0.0

def near_dji(d, dj):
    # the DJI's own LEDs sit on its body: ignore lights inside its outline
    return abs(d[0] - dj[2]) <= 24 and abs(d[1] - dj[3]) <= 14

def in_person(d):
    return PERSON[0] < d[0] < PERSON[1] and d[1] < PERSON[2]

def track_cf(D, DJ):
    ids = [dict(name=n, cls=c, x=float(x), y=float(y), vx=0.0, vy=0.0, miss=0) for n, c, x, y in SEEDS if c != "DJI"]
    out = []
    for i in range(N):
        t = i / 30.0
        strong = [d for d in D[i][0] if not near_dji(d, DJ[i])]
        weak = [d for d in D[i][1] if not near_dji(d, DJ[i]) and not in_person(d)]
        # three rounds: (0) identities seen within the last 3 frames get first pick of the strong lights,
        # (1) identities lost for longer may take a strong light nobody else wants, with a gate that grows with
        # the time lost, (2) still-unmatched identities may take a dim light very close to where they are.
        taken = set()
        for tier, pool in ((0, strong), (1, strong), (2, weak)):
            free = [q for q in ids if not q.get("_done") and (tier != 0 or q["miss"] <= 3)]
            if tier == 2: taken = set()
            dets = [d for k, d in enumerate(pool) if k not in taken]; idx = [k for k in range(len(pool)) if k not in taken]
            if not free or not dets: continue
            C = np.full((len(free), len(dets) + len(free)), 1e9)
            for qi, q in enumerate(free):
                px, py = q["x"] + q["vx"] * (1 if q["miss"] == 0 else 0), q["y"] + q["vy"] * (1 if q["miss"] == 0 else 0)
                sp = (q["vx"] ** 2 + q["vy"] ** 2) ** 0.5
                if tier == 0: gate = 35 + 2.0 * sp
                elif tier == 1: gate = min(35 + 2.0 * sp + 4 * min(q["miss"], 25), 135)
                else: gate = 22 + 2.0 * sp
                for di, dd in enumerate(dets):
                    dist = ((px - dd[0]) ** 2 + (py - dd[1]) ** 2) ** 0.5
                    if dist > gate: continue
                    C[qi, di] = dist + (colour_pen(q["cls"], dd[2], t) if tier < 2 else 0)
                C[qi, len(dets) + qi] = gate          # "no detection" option for this identity
            r, c = linear_sum_assignment(C)
            for qi, di in zip(r, c):
                if di >= len(dets) or C[qi, di] >= 1e5: continue
                q = free[qi]; x, y = dets[di][0], dets[di][1]; taken.add(idx[di])
                if q["miss"] > 0:      # re-acquired after a gap: do not invent a velocity from the jump
                    q["vx"], q["vy"] = 0.0, 0.0
                else:
                    q["vx"] = 0.5 * q["vx"] + 0.5 * (x - q["x"]); q["vy"] = 0.5 * q["vy"] + 0.5 * (y - q["y"])
                q["x"], q["y"] = x, y; q["miss"] = 0; q["_done"] = True
        for q in ids:
            if q.pop("_done", False): q["seen"] = 1; continue
            q["seen"] = 0; q["miss"] += 1
            if q["miss"] <= 3: q["x"] += q["vx"]; q["y"] += q["vy"]      # coast briefly, then hold
            q["vx"] *= 0.6; q["vy"] *= 0.6
        out.append([(q["name"], q["cls"], q["x"], q["y"], q["seen"]) for q in ids])
    return out

def track_dji(D):
    x, y = 985.0, 504.0; vx = vy = 0.0; miss = 0; tmpl = None; out = []
    TW, TH = 36, 18          # template half-size (the DJI is ~60x28 incl. dilation)
    for i in range(N):
        cands = D[i][2]; px, py = x + vx, y + vy; seen = 0
        gate = 45 + 4 * min(miss, 15)
        best = None
        for c in cands:
            dist = ((px - c[0]) ** 2 + (py - c[1]) ** 2) ** 0.5
            if dist < gate and (best is None or dist < best[0]): best = (dist, c)
        g = None
        if best is not None:
            nx, ny = best[1][0], best[1][1]; seen = 1
        elif tmpl is not None:        # no blob: grey-level template search around the prediction
            g = gray(i); R = 40 + 3 * min(miss, 10)
            ys0, xs0 = int(py) - TH - R, int(px) - TW - R
            win = g[max(0, ys0):int(py) + TH + R, max(0, xs0):int(px) + TW + R]
            if win.shape[0] > 2 * TH and win.shape[1] > 2 * TW:
                res = cv2.matchTemplate(win, tmpl, cv2.TM_CCOEFF_NORMED); _, mv, _, ml = cv2.minMaxLoc(res)
                if mv > 0.55:
                    nx, ny = max(0, xs0) + ml[0] + TW, max(0, ys0) + ml[1] + TH; seen = 2
        if seen:
            if miss == 0: vx = 0.6 * vx + 0.4 * (nx - x); vy = 0.6 * vy + 0.4 * (ny - y)
            else: vx = vy = 0.0
            x, y = nx, ny; miss = 0
            if seen == 1:              # refresh the template only on a real dark-blob detection
                g = gray(i) if g is None else g
                if TH <= y < g.shape[0] - TH and TW <= x < g.shape[1] - TW:
                    tmpl = g[int(y) - TH:int(y) + TH, int(x) - TW:int(x) + TW].copy()
        else:
            miss += 1
            if miss <= 5: x += vx; y += vy
            vx *= 0.7; vy *= 0.7
        out.append(("DJI", "DJI", x, y, 1 if seen else 0, seen))
    return out

def draw(args):
    i, states = args
    t = i / 30.0; fr = paint(cv2.imread(files[i]), t)
    im = Image.fromarray(cv2.cvtColor(fr, cv2.COLOR_BGR2RGB)); dr = ImageDraw.Draw(im)
    for name, cls, x, y in states:
        b, gg, r = COL[cls]; col = (r, gg, b)
        rad = 34 if cls == "DJI" else 14
        dr.ellipse([x - rad, y - rad, x + rad, y + rad], outline=col, width=2)
        txt = TXT[cls]; tw = dr.textlength(txt, font=f_lab); bx, by = x - tw / 2, y - rad - 38
        dr.line([x, y - rad, x, by + 28], fill=col, width=2)
        dr.rounded_rectangle([bx - 6, by, bx + tw + 6, by + 28], radius=4, fill=col); dr.text((bx, by + 2), txt, font=f_lab, fill=(255, 255, 255))
    ban = "Strike vs Guard on Crazyflies  ·  6 November 2026  ·  4 Guard escorts (blue) v 3 Strike (red)  ·  the zone is a DJI flown by hand"
    tw = dr.textlength(ban, font=f_ban); dr.rectangle([30, 92, 30 + tw + 24, 132], fill=(20, 20, 20)); dr.text((42, 97), ban, font=f_ban, fill=(255, 255, 255))
    dr.rectangle([0, 878, 1920, 960], fill=(20, 20, 20)); dr.text((44, 900), stage(t), font=f_cap, fill=(255, 255, 255))
    out = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR); cv2.imwrite(f"{S}/out3/f{i+1:04d}.png", out[75:960, :, :])
    return i

if __name__ == "__main__":
    with Pool(min(20, os.cpu_count() or 4)) as p: D = p.map(detect, range(N), chunksize=8)
    dj = track_dji(D); cf = track_cf(D, dj)
    rows = []
    for i in range(N):
        for name, cls, x, y, seen in cf[i] + [dj[i][:5]]:
            rows.append((i + 1, round(i / 30.0, 3), name, round(x, 1), round(y, 1), seen))
    with open(f"{S}/tracks2.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["frame", "t", "name", "x", "y", "seen"]); w.writerows(rows)
    for i in range(0, N, 150):
        print(f"t={i/30:4.1f}", " ".join(f"{n}:({int(x)},{int(y)}){'' if s else '?'}" for n, c, x, y, s in cf[i] + [dj[i][:5]]), flush=True)
    if "--no-draw" not in sys.argv:
        os.makedirs(f"{S}/out3", exist_ok=True)
        jobs = [(i, [(n, c, x, y) for n, c, x, y, s in cf[i] + [dj[i][:5]]]) for i in range(N)]
        with Pool(min(20, os.cpu_count() or 4)) as p: p.map(draw, jobs, chunksize=8)
    print("done")
