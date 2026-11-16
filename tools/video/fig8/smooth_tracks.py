"""Speed-adaptive smoothing of drone tracks (tracks.csv -> tracks_smooth.csv).

A hovering drone whose lights are off is tracked by its dark body only, and the mark wobbles (up to 20 px here).
Slow: median 9 + Savitzky-Golay(41, 2). Fast: median 5 + Savitzky-Golay(9, 2), which keeps the curve of the path.
Blend by speed (smoothstep between 60 and 200 px/s at 20 fps, 4K pixels). Check every meeting by eye afterwards.
"""
import csv, sys
import numpy as np
from scipy.signal import savgol_filter, medfilt
src, dst = sys.argv[1], sys.argv[2]
rows = list(csv.DictReader(open(src))); out = {}
for n in sorted({r["name"] for r in rows}):
    rs = [r for r in rows if r["name"] == n]; xy = np.array([[float(r["x"]), float(r["y"])] for r in rs])
    med5 = np.stack([medfilt(xy[:, i], 5) for i in range(2)], 1); med9 = np.stack([medfilt(xy[:, i], 9) for i in range(2)], 1)
    fast = np.stack([savgol_filter(med5[:, i], 9, 2) for i in range(2)], 1)
    slow = np.stack([savgol_filter(med9[:, i], 41, 2) for i in range(2)], 1)
    v = np.hypot(*np.gradient(slow, axis=0).T) * 20
    u = np.clip((v - 60) / (200 - 60), 0, 1); w = (u * u * (3 - 2 * u))[:, None]
    for r, p in zip(rs, w * fast + (1 - w) * slow): out[(r["frame"], n)] = p
with open(dst, "w", newline="") as fh:
    wr = csv.DictWriter(fh, fieldnames=rows[0].keys()); wr.writeheader()
    for r in rows:
        p = out[(r["frame"], r["name"])]; r = dict(r); r["x"] = f"{p[0]:.1f}"; r["y"] = f"{p[1]:.1f}"; wr.writerow(r)
