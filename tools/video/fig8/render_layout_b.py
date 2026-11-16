"""Alternative layouts for the figure-eight clip (owner feedback 16 Nov 2026). Layout A = render_fig8.draw() unchanged.

draw_alt(L, src4k, pos, t, ev, gs_frame, gs_center, trails, state) -> 1920x1080 BGR, L = LAYOUTS["B" | "C" | "D"].
Same marks, trails, colours, banner and captions as render_fig8; only the picture geometry and the panels change.

Run:  python render_alt.py <letter> [t0 t1]   -> alt-<letter>.mp4 (t0..t1, 30 fps, CRF 20), alt-<letter>-takeoff.jpg (3.5 s),
      alt-<letter>-landing.jpg (43.0 s).
"""
import csv, json, math, os, subprocess, sys
import cv2, numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); GFX = os.path.join(os.path.dirname(HERE), "gfx")
sys.path.insert(0, GFX)
import render_fig8 as R

MEET = (1904, 360)   # 4K: mean pair midpoint of the six windowed crossings (events.json); the fixed close-up centre

LAYOUTS = {
    # B: nothing covers the footage. Picture left (1344x942, filled to the bars), column right: ground station over close-up.
    "B": dict(src=(950, 0, 2000), dst=(0, 56, 1344, 998), ring=34,
              panels=[dict(kind="gs", rect=(1360, 72, 1904, 414), strip=60, zoom=1.2, span=None),
                      dict(kind="close", rect=(1360, 430, 1904, 982), strip=40, span=None)],
              stage3="Each time they meet head-on, the safety filter eases them apart. Watch the close-up."),
    # C: the current picture; corner panels over the floor, only during the eight (10.1-33.5 s), 0.4 s fades.
    "C": dict(src=(760, 0, 2200), dst=(0, 0, 1920, 1080), ring=44,
              # the right floor is too shallow during the eight for a 2x view (drones reach y 495 at x 1336-1440),
              # so the close-up goes bottom-left (free below y 470) and the ground station bottom-right
              panels=[dict(kind="close", rect=(24, 476, 584, 982), strip=40, span="eight", meet=(1904, 345)),
                      dict(kind="gs", rect=(1336, 520, 1896, 982), strip=60, zoom=1.3, span="eight")],
              stage3="Each time they meet head-on, the safety filter eases them apart. Watch the close-up."),
    # D: one panel. Ground station bottom right (house size 832x468) during the eight only; no close-up;
    #    a 'safety filter acting' pill next to the pair while the filter acts.
    "D": dict(src=(760, 0, 2200), dst=(0, 0, 1920, 1080), ring=44, pair_pill=True,
              panels=[dict(kind="gs", rect=(1064, 522, 1896, 982), strip=40, zoom=1.5, span="eight")],
              stage3="Each time they meet head-on, the safety filter eases them apart. Watch the white rings."),
}
SPAN_FADE = 0.4
CAM01_BOX = (1730, 1185, 1985, 1255)   # 4K box of the burned-in 'Camera 01' (inside layout B's crop): inpainted


def _cam01(f):
    x0, y0, x1, y1 = CAM01_BOX; roi = f[y0:y1, x0:x1]
    m = (cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY) > 170).astype(np.uint8) * 255
    f[y0:y1, x0:x1] = cv2.inpaint(roi, cv2.dilate(m, np.ones((7, 7), np.uint8)), 7, cv2.INPAINT_TELEA)


def geom(L):
    sx0, sy0, sw = L["src"]; dx0, dy0, dx1, dy1 = L["dst"]; s = (dx1 - dx0) / sw; sh = (dy1 - dy0) / s
    return sx0, sy0, sw, sh, dx0, dy0, dx1, dy1, s


def span_alpha(L, P, t, ev):
    if P["span"] is None: return 1.0
    a, b = ev["eight_start"], ev["hold"]
    return max(0.0, min(1.0, (t - a) / SPAN_FADE, (b - t) / SPAN_FADE))


def caption(L, t, ev):
    f = ev["filter"]
    if t < ev["eight_start"]: return "Take-off: two Starling 2 Max drones climb to their start points. Nobody is on the sticks."
    if t < f[1][0]: return "CMU's figure-eight at 2.0 m/s, flown in Singapore. Nobody is on the sticks."
    if t < f[3][0]: return "Each time they meet head-on, the safety filter eases them apart. Watch the close-up."
    if t < ev["hold"]: return "The ground station draws each drone's CBF Safety Assist Zone as a sphere."
    if t < ev["land"]: return "The eight ends: both drones brake, hold, then move off to their landing spots."
    return "Landing: watch them swap sides. drone_1 lands on the right, drone_2 on the left."


def _place(q, w, h, marks, pills, bounds, keep, prev=None):
    best = (None, 1e9); base = R.RING_R + 4
    for k in range(12):
        ang = math.radians(-90 + 30 * k); c, s_ = math.cos(ang), math.sin(ang)
        for d in [base + L_ for L_ in R.LEADS]:
            ax, ay = q[0] + d * c, q[1] + d * s_; cx, cy = ax + c * w / 2, ay + s_ * h / 2
            r = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
            cost = 0.4 * (d - base) + 4 * min(k, 12 - k)
            if r[0] < bounds[0] or r[1] < bounds[1] or r[2] > bounds[2] or r[3] > bounds[3]: cost += 1000
            cost += 1000 * sum(R._overlap(r, m) for m in marks + keep)
            cost += 1000 * sum(R._overlap(r, (p[0] - 6, p[1] - 6, p[2] + 6, p[3] + 6)) for p in pills)
            if prev is not None and (k, d) != prev: cost += 40
            if cost < best[1]: best = ((r, (k, d)), cost)
    return best


def _closeup(f, pos, t, trails, filt, pw, ph, zs, ring_main, meet=MEET):
    """Fixed 2x view of the meeting point: zs = window px per 4K px; rings at 2x the main ring."""
    rw, rh = pw / zs, ph / zs; rx0, ry0 = meet[0] - rw / 2, meet[1] - rh / 2
    M = np.float32([[zs, 0, -rx0 * zs], [0, zs, -ry0 * zs]])
    pic = Image.fromarray(cv2.cvtColor(cv2.warpAffine(f, M, (pw, ph), flags=cv2.INTER_LANCZOS4), cv2.COLOR_BGR2RGB)).convert("RGBA")
    wo = Image.new("RGBA", pic.size, (0, 0, 0, 0)); d = ImageDraw.Draw(wo); w4 = lambda x, y: ((x - rx0) * zs, (y - ry0) * zs)
    for n, p in pos.items():
        if p is None: continue
        q = w4(*p); pts = [(ti, *w4(x, y)) for ti, x, y in trails.get(n, []) if t - R.TRAIL_S <= ti <= t]
        R._trail(d, pts + [(t, *q)], t, R.TEAM[n], q, r_clear=2 * ring_main + 4)
    for n, p in pos.items():
        if p is None: continue
        q = w4(*p)
        R._ring(d, *q, 2 * ring_main, R.TEAM[n])
    return Image.alpha_composite(pic, wo)


def _gs_pic(gs_frame, gs_center, pw, ph, zoom):
    cw, ch = pw / zoom, ph / zoom; P = R.GS_PANEL
    gx, gy = gs_center if gs_center else ((P[0] + P[2]) / 2, (P[1] + P[3]) / 2)
    lx = int(round(min(max(gx - cw / 2, P[0]), P[2] - cw))); ty = int(round(min(max(gy - ch / 2, P[1]), P[3] - ch)))
    crop = gs_frame[ty:ty + int(round(ch)), lx:lx + int(round(cw))]
    return Image.fromarray(cv2.cvtColor(cv2.resize(crop, (pw, ph), interpolation=cv2.INTER_LANCZOS4), cv2.COLOR_BGR2RGB)).convert("RGBA")


def _strip_extra(two_line):
    def ex(d, x0, y0, x1, strip):
        if two_line:   # layout B: the 544 px column is too narrow for the title on one line (618 px at 22 px)
            d.rectangle([x0, y0, x1 - 1, y0 + strip - 1], fill=(14, 14, 14, 255))
            d.text((x0 + 12, y0 + 16), "Ground station", font=R.F(24), fill=(255, 255, 255, 255), anchor="lm")
            d.text((x0 + 12, y0 + 44), "Sphere = CBF Safety Assist Zone", font=R.F(22), fill=(255, 255, 255, 255), anchor="lm")
    return ex


def draw_alt(L, src4k, pos, t, ev, gs_frame=None, gs_center=None, trails=None, state=None):
    st = state if state is not None else {}; trails = trails or {}
    sx0, sy0, sw, sh, dx0, dy0, dx1, dy1, s = geom(L); rr = L["ring"]; k = rr / R.RING_R
    f = src4k.copy(); R._repaint_clock(f)
    if sy0 + sh > 1185: _cam01(f)
    canvas = np.zeros((1080, 1920, 3), np.uint8); canvas[:] = (24, 24, 24)
    canvas[dy0:dy1, dx0:dx1] = cv2.resize(f[int(sy0):int(round(sy0 + sh)), sx0:sx0 + sw], (dx1 - dx0, dy1 - dy0), interpolation=cv2.INTER_AREA)
    im = Image.fromarray(cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)).convert("RGBA")
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); dr = ImageDraw.Draw(ov)
    o = lambda x, y: (dx0 + (x - sx0) * s, dy0 + (y - sy0) * s)
    vis = {n: o(*p) for n, p in pos.items() if p is not None}
    filt = R._in(t, ev["filter"]); f_start = max([a for a, b in ev["filter"] if a <= t] or [-9])
    for n, q in vis.items():
        pts = [(ti, *o(x, y)) for ti, x, y in trails.get(n, []) if t - R.TRAIL_S <= ti <= t]
        R._trail(dr, pts + [(t, *q)], t, R.TEAM[n], q, k=max(k, 0.8), r_clear=rr + 4)
    for n, q in vis.items():
        R._ring(dr, *q, rr, R.TEAM[n])
    # keep-outs: panels while visible; bounds: the picture area between the bars
    act = [(P, span_alpha(L, P, t, ev)) for P in L["panels"]]
    keep = [(P["rect"][0] - 8, P["rect"][1] - 8, P["rect"][2] + 8, P["rect"][3] + 8) for P, a in act if a > 0]
    bounds = (max(12, dx0 + 12), max(R.TOP[3] + 8, dy0 + 8), min(1908, dx1 - 12), min(R.CAP[1] - 8, dy1 - 8))
    marks = [(q[0] - rr - 10, q[1] - rr - 10, q[0] + rr + 10, q[1] + rr + 10) for q in vis.values()]
    pills = []
    for n, q in sorted(vis.items()):
        al = max(R._win(t, a, b) for a, b in R.WORDS)
        if al <= 0: continue
        bb = dr.textbbox((0, 0), n, font=R.F_LAB); w, h = bb[2] - bb[0] + 2 * R.PAD_X, 28 + 2 * R.PAD_Y + 2
        res, cost = _place(q, w, h, marks, pills, bounds, keep, prev=st.get(n))
        if res is None or cost >= 1000: continue
        rect, slot = res; st[n] = slot; pills.append(rect); R._pill(dr, q, rect, n, R.TEAM[n], al)
    if L.get("pair_pill") and filt and len(vis) == 2:
        a_, b_ = next((a, b) for a, b in ev["filter"] if a <= t <= b); al = max(0.0, min(1.0, (t - a_) / 0.2, (b_ - t) / 0.3))
        up = min(vis.values(), key=lambda q: q[1]); txt = "safety filter acting"
        bb = dr.textbbox((0, 0), txt, font=R.F_LAB); w, h = bb[2] - bb[0] + 2 * R.PAD_X, 28 + 2 * R.PAD_Y + 2
        res, cost = _place(up, w, h, marks, pills, bounds, keep, prev=st.get("pair"))
        if res is not None and cost < 1000:
            rect, slot = res; st["pair"] = slot; pills.append(rect)
            R._pill(dr, up, rect, txt, R.WHITE, al, txt=(14, 14, 14))
    # bars (same as render_fig8)
    dr.rectangle(R.TOP, fill=(14, 14, 14, 235))
    dr.text((24, 28), "Two Starlings · CMU's figure-eight · Singapore · 16 Nov 2026", font=R.F_BAN, fill=(255, 255, 255, 255), anchor="lm")
    stxt = "safety filter: correcting" if filt else "safety filter: on"
    sw_ = dr.textlength(stxt, font=R.F(26)) + 28
    items = [("drone_1", R.D1), ("drone_2", R.D2)]
    wd = [34 + 10 + dr.textlength(x, font=R.F_BAN) for x, _ in items]; x = 1920 - 24 - sw_ - 32 - sum(wd) - 32 * (len(items) - 1)
    for (txt, col), w in zip(items, wd):
        cx = x + 17; dr.ellipse([cx - 12, 16, cx + 12, 40], outline=R._a(col, 255), width=4)
        dr.text((x + 44, 28), txt, font=R.F_BAN, fill=(255, 255, 255, 255), anchor="lm"); x += w + 32
    if filt: dr.rounded_rectangle([x, 9, x + sw_, 47], radius=8, fill=(255, 255, 255, 255)); dr.text((x + 14, 28), stxt, font=R.F(26), fill=(14, 14, 14, 255), anchor="lm")
    else: dr.rounded_rectangle([x, 9, x + sw_, 47], radius=8, outline=(150, 150, 150, 255), width=2); dr.text((x + 14, 28), stxt, font=R.F(26), fill=(190, 190, 190, 255), anchor="lm")
    if L.get("tag"):
        tw_ = dr.textlength(L["tag"], font=R.F(30)); dr.rounded_rectangle([24, 76, 24 + tw_ + 36, 128], radius=8, fill=(255, 255, 255, 240)); dr.text((42, 102), L["tag"], font=R.F(30), fill=(14, 14, 14, 255), anchor="lm")
    dr.rectangle(R.CAP, fill=(20, 20, 20, 255))
    cap, fs = (L.get("cap") or caption(L, t, ev)), 34
    while fs > 26 and dr.textlength(cap, font=R.F(fs)) > 1920 - 88: fs -= 2
    dr.text((44, (R.CAP[1] + R.CAP[3]) / 2), cap, font=R.F(fs), fill=(255, 255, 255, 255), anchor="lm")
    im = Image.alpha_composite(im, ov)
    # panels
    for P, a in act:
        if a <= 0: continue
        x0, y0, x1, y1 = P["rect"]; pw, ph = x1 - x0, y1 - y0 - P["strip"]
        if P["kind"] == "gs":
            if gs_frame is None: continue
            pic = _gs_pic(gs_frame, gs_center, pw, ph, P["zoom"])
            im = R._panel(im, P["rect"], P["strip"], "" if P["strip"] == 60 else "Ground station · Sphere = CBF Safety Assist Zone", pic,
                          extra=_strip_extra(P["strip"] == 60), alpha=a)
        else:
            pic = _closeup(f, pos, t, trails, filt, pw, ph, 2 * s, rr, P.get("meet", MEET))
            def tag(d, x0_, y0_, x1_, strip):
                if not filt: return
                txt = "filter correcting"; tw = d.textlength(txt, font=R.F_PILL)
                d.rounded_rectangle([x1_ - 12 - tw - 20, y0_ + 6, x1_ - 12, y0_ + strip - 6], radius=8, fill=(255, 255, 255, 255))
                d.text((x1_ - 12 - tw - 10, y0_ + strip / 2), txt, font=R.F_PILL, fill=(14, 14, 14, 255), anchor="lm")
            im = R._panel(im, P["rect"], P["strip"], "Meeting point · 2×", pic, extra=tag, alpha=a)
    return cv2.cvtColor(np.array(im.convert("RGB")), cv2.COLOR_RGB2BGR)


# ------------------------------------------------------------------------------------------------ driver
def load():
    T = {}
    for r in csv.DictReader(open(f"{GFX}/../track/tracks_smooth.csv")):
        T.setdefault(r["name"], {})[int(r["frame"])] = (float(r["x"]), float(r["y"]), int(float(r["seen"])))
    E = json.load(open(f"{GFX}/../track/events.json"))
    filt = [(c["t_start"], c["t_end"]) for c in E["cbf_active_gs"]]
    xs = [{"t": c["t"], "mid": ((c["drone_1_xy"][0] + c["drone_2_xy"][0]) / 2, (c["drone_1_xy"][1] + c["drone_2_xy"][1]) / 2)}
          for c in E["crossings"] if c["image_distance_px"] <= R.WIN_MAX_DIST and any(a - 0.3 <= c["t"] <= b + 0.3 for a, b in filt)]
    EV = {"crossings": xs, "filter": filt, "eight_start": 10.1, "hold": E["figure_eight"]["end_t_from_gs"], "land": 38.0}
    G = {}
    for r in csv.DictReader(open(f"{GFX}/../track/gs-tracks.csv")):
        if r["seen"] == "1": G.setdefault(int(r["gs_frame"]), []).append((float(r["x"]), float(r["y"])))
    return T, EV, G


def main(letter, t0=9.0, t1=24.0):
    T, EV, G = load(); V = os.path.expanduser("~/AirStack-starling-max2/videos")
    last_c = [None]
    def gs_center(j):
        m = [(sum(p[0] for p in G[q]) / len(G[q]), sum(p[1] for p in G[q]) / len(G[q])) for q in range(j - 15, j + 16) if q in G]
        if m: last_c[0] = (sum(p[0] for p in m) / len(m), sum(p[1] for p in m) / len(m))
        return last_c[0]
    def render(src, k, t, g, j, state):
        pos = {nm: (T[nm][k][0], T[nm][k][1]) if T[nm][k][2] else None for nm in T}
        trails = {nm: [(q / 20, T[nm][q][0], T[nm][q][1]) for q in range(max(0, k - 20), k) if T[nm][q][2]] for nm in T}
        if letter == "A": return R.draw(src, pos, t, EV, g, gs_center(j), trails, state)
        return draw_alt(LAYOUTS[letter], src, pos, t, EV, g, gs_center(j), trails, state)
    # stills (take-off 3.5 s, landing 43.0 s)
    gs = cv2.VideoCapture(f"{V}/Fig8_CBF_two_drones_thermal_ui.mp4"); want = {round((ts + R.GS_OFFSET) * 30): ts for ts in (3.5, 43.0)}; GF = {}; gi = 0
    while len(GF) < 2:
        ok, g = gs.read()
        if not ok: break
        if gi in want: GF[want[gi]] = (g, gi)
        gi += 1
    for ts, name in ((3.5, "takeoff"), (43.0, "landing")):
        k = int(ts * 20); src = cv2.imread(f"{GFX}/src/k{k:04d}.png"); g, j = GF[ts]
        cv2.imwrite(f"{HERE}/alt-{letter}-{name}.jpg", render(src, k, ts, g, j, None), [cv2.IMWRITE_JPEG_QUALITY, 92])
    # clip t0..t1
    cam = cv2.VideoCapture(f"{V}/fig8_twodrones_light.mp4"); gs = cv2.VideoCapture(f"{V}/Fig8_CBF_two_drones_thermal_ui.mp4")
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "1920x1080", "-r", "30", "-i", "-",
                           "-an", "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                           f"{HERE}/fig8-{letter}-master.mp4"], stdin=subprocess.PIPE)
    ci = -1; cframe = None; gi = -1; gframe = None; state = {}; n = int(round(t0 * 30))
    while n / 30.0 < t1:
        t = n / 30.0; k = int(t * 20 + 1e-6); j = int(round((t + R.GS_OFFSET) * 30))
        while ci < k:
            ok, f = cam.read()
            if not ok: break
            cframe = f; ci += 1
        while gi < j:
            ok, g = gs.read()
            if not ok: break
            gframe = g; gi += 1
        ff.stdin.write(render(cframe, k, t, gframe, j, state).tobytes()); n += 1
    ff.stdin.close(); ff.wait(); print(letter, "done")


if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0], *(float(x) for x in a[1:3]))
