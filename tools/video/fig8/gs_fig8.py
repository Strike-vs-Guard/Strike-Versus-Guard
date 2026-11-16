"""gs_fig8.py - follow the two drone markers in the Foxglove 3D view of the ground-station recording
(Fig8_CBF_two_drones_thermal_ui.mp4, 1280x720, 30 fps) and read the colour of the sphere around each.
Frames: gs/g%04d.jpg (ffmpeg -i <gs.mp4> -q:v 2 gs/g%04d.jpg). Writes gs-tracks.csv and gs_raw.pkl.
Marker = the dark drone icon (wider than tall, >= 90 px of dark pixels); the name label above it is thin text and
is ignored. Identity: seeds at the first panel frame (drone_1 near the viewer, lower right; drone_2 far, left),
then nearest-neighbour continuity (the markers move < 15 px per frame); checked by eye against the labels.
Sphere colour: mean colour of a ring 0.55-0.85 x icon width around the icon (dark/label pixels excluded),
classified by hue: green, blue, red, grey.
"""
import cv2, numpy as np, os, csv, pickle, glob
from scipy.optimize import linear_sum_assignment
S = os.path.dirname(os.path.abspath(__file__))
files = sorted(glob.glob(f"{S}/gs/g*.jpg")); N = len(files); FPS = 30.0
RX0, RX1, RY0, RY1 = 595, 1235, 95, 442          # 3D view (toolbar at the right edge excluded)

def panel_on(im):
    r = im[RY0:RY1, RX0:RX1]
    return float((r.min(axis=2) > 225).mean()) > 0.6     # light 3D background, not a terminal

def icons(im):
    r = im[RY0:RY1, RX0:RX1]; g = cv2.cvtColor(r, cv2.COLOR_BGR2GRAY)
    m = cv2.dilate((g < 90).astype(np.uint8), np.ones((3, 3), np.uint8))
    n, lab, st, cen = cv2.connectedComponentsWithStats(m)
    out = []
    for k in range(1, n):
        x, y, w, h, a = st[k]
        if a >= 90 and w >= 16 and w >= 0.9 * h: out.append([RX0 + cen[k][0], RY0 + cen[k][1], float(w), float(a)])
    merged = []                                   # an icon split by its own sphere/shadow: merge parts
    for o in sorted(out, key=lambda o: -o[3]):
        for mm in merged:
            if abs(mm[0] - o[0]) < 25 and abs(mm[1] - o[1]) < 20:
                wt = mm[3] + o[3]; mm[0] = (mm[0] * mm[3] + o[0] * o[3]) / wt; mm[1] = (mm[1] * mm[3] + o[1] * o[3]) / wt
                mm[2] = max(mm[2], o[2], abs(mm[0] - o[0]) + o[2]); mm[3] = wt; break
        else: merged.append(list(o))
    return merged

def sphere_colour(im, x, y, w):
    H, W = im.shape[:2]; r1, r2 = 0.55 * w, 0.85 * w
    yy, xx = np.mgrid[0:H, 0:W]
    y0, y1, x0, x1 = int(max(RY0, y - r2 - 1)), int(min(RY1, y + r2 + 2)), int(max(RX0, x - r2 - 1)), int(min(RX1, x + r2 + 2))
    if y1 <= y0 or x1 <= x0: return None
    sub = im[y0:y1, x0:x1].astype(int); dd = np.hypot(xx[y0:y1, x0:x1] - x, yy[y0:y1, x0:x1] - y)
    sel = (dd >= r1) & (dd <= r2) & (sub.min(axis=2) > 150)
    if sel.sum() < 20: return None
    return sub[sel].mean(axis=0)                  # B, G, R

def classify(c):
    if c is None: return "unknown"
    b, g, r = c
    if r - max(g, b) > 6: return "red"
    if g - max(r, b) > 4: return "green"
    if b - r > 8: return "blue"
    if max(b, g, r) - min(b, g, r) <= 6: return "grey"
    return "other"

if __name__ == "__main__":
    def ok(i):
        im = cv2.imread(files[i]); ic = icons(im)     # two markers, well apart (a dialog box gives two close dark shapes)
        return panel_on(im) and len(ic) == 2 and np.hypot(ic[0][0] - ic[1][0], ic[0][1] - ic[1][1]) > 150
    # seed frame: the first panel frame from which both markers are found for 10 frames in a row
    first = next(i for i in range(N - 10) if all(ok(j) for j in range(i, i + 10)))
    im = cv2.imread(files[first]); ic = icons(im)
    # seeds: drone_1 is the marker nearer the viewer (lower in the view), drone_2 the far one (labels checked by eye)
    ic = sorted(ic, key=lambda o: -o[1])[:2]
    st = {"drone_1": ic[0][:3], "drone_2": ic[1][:3]}; prev = {k: v[:] for k, v in st.items()}
    rows, raw = [], []
    for i in range(N):
        u = i / FPS
        if i < first:
            for nm in ("drone_1", "drone_2"): rows.append((i, round(u, 3), nm, "", "", 0, "no_view", "", "", ""))
            continue
        im = cv2.imread(files[i]); ic = icons(im); names = ["drone_1", "drone_2"]
        C = np.full((2, len(ic) + 2), 1e9)
        for a, nm in enumerate(names):
            for k, o in enumerate(ic):
                d = np.hypot(o[0] - st[nm][0], o[1] - st[nm][1])
                if d < 40: C[a, k] = d
            C[a, len(ic) + a] = 40
        rr, cc = linear_sum_assignment(C)
        for a, k in zip(rr, cc):
            nm = names[a]
            seen = int(k < len(ic) and C[a, k] < 1e8)
            if seen: st[nm] = ic[k][:3]
            x, y, w = st[nm]
            col = sphere_colour(im, x, y, w) if seen else None
            cls = classify(col)
            bgr = ["%.0f" % v for v in col] if col is not None else ["", "", ""]
            rows.append((i, round(u, 3), nm, round(x, 1), round(y, 1), seen, cls, *bgr))
    with open(f"{S}/gs-tracks.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n"); w.writerow(["gs_frame", "u", "name", "x", "y", "seen", "sphere", "B", "G", "R"]); w.writerows(rows)
    print("panel from frame", first, "u=%.2f" % (first / FPS))
