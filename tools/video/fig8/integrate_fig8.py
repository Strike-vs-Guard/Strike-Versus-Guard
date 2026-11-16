"""Full render of the figure-eight clip: camera (20 fps) + tracks + ground station (30 fps) -> 1920x1080 at 30 fps, piped to ffmpeg."""
import csv, json, os, subprocess, sys
import cv2, numpy as np
import render_fig8 as R
S = os.path.dirname(os.path.abspath(__file__)); V = os.path.expanduser("~/AirStack-starling-max2/videos")
OUT = sys.argv[1]
T = {}
for r in csv.DictReader(open(f"{S}/../track/tracks.csv")):
    T.setdefault(r["name"], {})[int(r["frame"])] = (float(r["x"]), float(r["y"]), int(float(r["seen"])))
E = json.load(open(f"{S}/../track/events.json"))
filt = [(c["t_start"], c["t_end"]) for c in E["cbf_active_gs"]]
xs = [{"t": c["t"], "mid": ((c["drone_1_xy"][0] + c["drone_2_xy"][0]) / 2, (c["drone_1_xy"][1] + c["drone_2_xy"][1]) / 2)}
      for c in E["crossings"] if c["image_distance_px"] <= R.WIN_MAX_DIST and any(a - 0.3 <= c["t"] <= b + 0.3 for a, b in filt)]
EV = {"crossings": xs, "filter": filt, "eight_start": 10.1, "hold": E["figure_eight"]["end_t_from_gs"], "land": 38.0}
G = {}
for r in csv.DictReader(open(f"{S}/../track/gs-tracks.csv")):
    if r["seen"] == "1": G.setdefault(int(r["gs_frame"]), []).append((float(r["x"]), float(r["y"])))
last_c = [None]
def gs_center(j):
    m = [(sum(p[0] for p in G[k]) / len(G[k]), sum(p[1] for p in G[k]) / len(G[k])) for k in range(j - 15, j + 16) if k in G]
    if m: last_c[0] = (sum(p[0] for p in m) / len(m), sum(p[1] for p in m) / len(m))
    return last_c[0]
cam = cv2.VideoCapture(f"{V}/fig8_twodrones_light.mp4"); gs = cv2.VideoCapture(f"{V}/Fig8_CBF_two_drones_thermal_ui.mp4")
NF = max(max(d) for d in T.values()) + 1
ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "1920x1080", "-r", "30", "-i", "-",
                       "-an", "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-pix_fmt", "yuv420p", OUT], stdin=subprocess.PIPE)
ci = -1; cframe = None; gi = -1; gframe = None; state = {}; n = 0
while True:
    t = n / 30.0; k = int(t * 20 + 1e-6)
    if k >= NF: break
    while ci < k:
        ok, f = cam.read()
        if not ok: break
        cframe = f; ci += 1
    j = int(round((t + R.GS_OFFSET) * 30))
    while gi < j:
        ok, g = gs.read()
        if not ok: break
        gframe = g; gi += 1
    pos = {nm: (T[nm][k][0], T[nm][k][1]) if T[nm][k][2] else None for nm in T}
    trails = {nm: [(q / 20, T[nm][q][0], T[nm][q][1]) for q in range(max(0, k - 20), k) if T[nm][q][2]] for nm in T}
    out = R.draw(cframe, pos, t, EV, gframe, gs_center(j), trails, state)
    ff.stdin.write(out.tobytes())
    if n % 150 == 0: print(f"t={t:5.1f} s cam {k} gs {j}", flush=True)
    n += 1
ff.stdin.close(); ff.wait(); print("frames", n, "windows", [(round(a, 2), round(b, 2)) for a, b, c in R.windows(EV)])
