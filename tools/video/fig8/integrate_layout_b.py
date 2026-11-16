"""Final figure-eight clip: layout B (footage left, ground station over an always-on close-up on the right) plus one
half-speed replay of a meeting, full width, straight after the hold. python integrate_b.py out.mp4"""
import os, subprocess, sys
import cv2
import render_layout_b as B
R = B.R; OUT = sys.argv[1]; V = os.path.expanduser("~/AirStack-starling-max2/videos")
T, EV, G = B.load(); HOLD = EV["hold"]
START, END = 1.0, 45.5
RP0, RP1, RPS = 26.5, 28.3, 0.5                      # replay: source span (the meeting at 27.35 s) and speed
MID = (1898.0, 328.5)                                # pair midpoint at that meeting, 4K px (track/events.json)
RW = 1466; RH = RW * (998 - 56) / 1920               # 4K crop shown across the full width between the bars (1.5x the first cut's scale)
LB = B.LAYOUTS["B"]
LR = dict(src=(int(MID[0] - RW / 2), 0, RW), dst=(0, 56, 1920, 998), ring=66, panels=[], stage3="",
          tag="REPLAY · ½ speed", cap="Replay at half speed: one drone passes above the other.")
last_c = [None]
def gs_center(j):
    m = [(sum(p[0] for p in G[q]) / len(G[q]), sum(p[1] for p in G[q]) / len(G[q])) for q in range(j - 15, j + 16) if q in G]
    if m: last_c[0] = (sum(p[0] for p in m) / len(m), sum(p[1] for p in m) / len(m))
    return last_c[0]
tl = [(START + i / 30, "live") for i in range(int(round((HOLD - START) * 30)))]
tl += [(RP0 + i / 30 * RPS, "replay") for i in range(int(round((RP1 - RP0) / RPS * 30)))]
tl += [(HOLD + i / 30, "live") for i in range(int(round((END - HOLD) * 30)))]
cam = cv2.VideoCapture(f"{V}/fig8_twodrones_light.mp4"); gs = cv2.VideoCapture(f"{V}/Fig8_CBF_two_drones_thermal_ui.mp4")
ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "1920x1080", "-r", "30", "-i", "-",
                       "-an", "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-pix_fmt", "yuv420p", OUT], stdin=subprocess.PIPE)
ci = -1; cframe = None; gi = -1; gframe = None; state = {}; cache = {}; k0, k1 = int(RP0 * 20) - 1, int(RP1 * 20) + 1
for n, (t, mode) in enumerate(tl):
    k = int(t * 20 + 1e-6)
    pos = {nm: (T[nm][k][0], T[nm][k][1]) if T[nm][k][2] else None for nm in T}
    trails = {nm: [(q / 20, T[nm][q][0], T[nm][q][1]) for q in range(max(0, k - 20), k) if T[nm][q][2]] for nm in T}
    if mode == "live":
        while ci < k:
            ok, f = cam.read()
            if not ok: break
            cframe = f; ci += 1
            if k0 <= ci <= k1: cache[ci] = f
        j = int(round((t + R.GS_OFFSET) * 30))
        while gi < j:
            ok, g = gs.read()
            if not ok: break
            gframe = g; gi += 1
        out = B.draw_alt(LB, cframe, pos, t, EV, gframe, gs_center(j), trails, state)
    else:
        out = B.draw_alt(LR, cache[k], pos, t, EV, None, None, trails, {})
    ff.stdin.write(out.tobytes())
    if n % 200 == 0: print(f"out {n / 30:5.1f} s  src {t:5.2f} {mode}", flush=True)
ff.stdin.close(); ff.wait(); print("frames", len(tl), "=", round(len(tl) / 30, 1), "s; replay crop", LR["src"], round(RH))
