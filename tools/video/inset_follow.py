# Two-pass: find the midpoint of the blue and yellow spheres in every frame, smooth with a centred moving average, then crop.
import cv2, numpy as np, sys
SRC = sys.argv[5] if len(sys.argv) > 5 else "ground-station.mp4"   # the ground-station screen recording
OUT = sys.argv[1]; W, H = int(sys.argv[2]), int(sys.argv[3]); OW = int(sys.argv[4]); T0, DUR = 31.78, 42.55   # T0: offset of the camera clip inside the screen recording; DUR: clip length
PANEL = (600, 140, 1250, 440)   # inside the 3D view, below its header (ui-video pixels)
def centroid(mask):
    m = cv2.moments(mask); return (m["m10"] / m["m00"], m["m01"] / m["m00"]) if m["m00"] > 300 else None
def frames():
    cap = cv2.VideoCapture(SRC); cap.set(cv2.CAP_PROP_POS_MSEC, T0 * 1000); n = 0
    while n < int(DUR * 30):
        ok, fr = cap.read()
        if not ok: break
        yield fr; n += 1
mids = []; last = None
for fr in frames():
    x0, y0, x1, y1 = PANEL; hsv = cv2.cvtColor(fr[y0:y1, x0:x1], cv2.COLOR_BGR2HSV)
    pts = [p for p in (centroid(cv2.inRange(hsv, (95, 25, 120), (125, 255, 255))), centroid(cv2.inRange(hsv, (18, 25, 120), (40, 255, 255)))) if p]
    if pts: last = (sum(p[0] for p in pts) / len(pts) + x0, sum(p[1] for p in pts) / len(pts) + y0)
    mids.append(last if last else ((x0 + x1) / 2, (y0 + y1) / 2))
m = np.array(mids); k = 31; pad = np.pad(m, ((k // 2, k // 2), (0, 0)), mode="edge")
sm = np.stack([np.convolve(pad[:, i], np.ones(k) / k, mode="valid") for i in range(2)], axis=1)
OH = int(round(OW * H / W)); wr = cv2.VideoWriter(OUT, cv2.VideoWriter_fourcc(*"mp4v"), 30, (OW, OH))
for fr, (cx, cy) in zip(frames(), sm):
    x0, y0, x1, y1 = PANEL
    left = int(round(min(max(cx - W / 2, x0), x1 - W))); top = int(round(min(max(cy - H / 2, y0), y1 - H)))
    wr.write(cv2.resize(fr[top:top + H, left:left + W], (OW, OH), interpolation=cv2.INTER_LANCZOS4))
wr.release(); print("frames", len(mids), "midpoint x range", int(m[:, 0].min()), int(m[:, 0].max()), "y range", int(m[:, 1].min()), int(m[:, 1].max()))
