import cv2, numpy as np, csv, os, sys
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_spec as R
S = os.path.dirname(os.path.abspath(__file__))
bg = np.load(f"{S}/bg.npy"); bgg = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY).astype(int)
rows = defaultdict(list)
for r in csv.DictReader(open(f"{S}/tracks2.csv")):
    rows[int(r["frame"])].append(dict(name=r["name"], cls="DJI" if r["name"] == "DJI" else ("Guard" if r["name"][0] == "G" else "Strike"), x=float(r["x"]), y=float(r["y"]), seen=int(r["seen"])))
state = {}
for f in sorted(rows):
    t = (f - 1) / 30.0
    fr = cv2.imread(f"{S}/src/f{f:04d}.jpg")
    if t >= 22:
        g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY).astype(int)
        for y in range(580, 965):
            dark = (g[y, :1200] < 62) & (bgg[y, :1200] - g[y, :1200] > 35)
            if dark.sum() > 120:
                xr = min(1200, int(np.where(dark)[0].max()) + 14); fr[y, :xr] = bg[y, :xr]
    out = R.draw(fr, rows[f], t, state)
    cv2.imwrite(f"{S}/out4/f{f:04d}.png", out[75:960, :, :])
    if f % 240 == 1: print("frame", f, flush=True)
print("done", len(rows))
