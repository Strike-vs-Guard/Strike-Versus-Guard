"""Graphics for the lights-on figure-eight clip (16 Nov 2026): spec in fig8-spec.md. House scheme: tools/video/render_spec.py.

draw(src4k, pos, t, events, gs_frame=None, gs_center=None, trails=None, state=None) -> 1920x1080 BGR frame
  src4k     : the camera frame being shown (3840x2160 BGR, fig8_twodrones_light.mp4). At 30 fps output, pass the source
              frame floor(t*20) and the positions OF THAT SAME source frame: marks step with the picture (no interpolation).
  pos       : {"drone_1": (x, y) | None, "drone_2": (x, y) | None} in 4K px; None = not seen -> no mark.
  t         : camera time, s (0 = first frame of the camera file).
  events    : {"crossings": [{"t": t_ca, "mid": (x, y) 4K pair midpoint at t_ca}, ...]   (tracks/events.json)
               "filter": [(t0, t1), ...]  ground-station CBF column 'correcting', camera time
               "eight_start": s, "hold": s, "land": s}                                   (ground-station command log)
  gs_frame  : ground-station frame (1280x720 BGR) at camera t + GS_OFFSET; None = no inset.
  gs_center : (x, y) in ground-station px: 1 s centred moving average of the two drone markers; clamped to the panel.
  trails    : {"drone_1": [(t, x, y), ...], ...} seen positions (4K) from the last TRAIL_S seconds, oldest first.
  state     : the same dict every frame of a video (label stickiness); None for single mock frames.

Run as a script: mock frames mock-*.jpg, mock-sheet.jpg, mock-phone-845.jpg (needs src/ from grab.py + roughtrack.py).
"""
import math, os
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def F(px): return ImageFont.truetype(FONT, px)
F_LAB, F_BAN, F_CAP, F_TTL, F_PILL = F(28), F(30), F(34), F(24), F(22)

# ---- canvas: one 16:9 crop of the 4K camera fills 1920x1080; bars and panels sit on top of it
CX0, CY0, CW = 760, 0, 2200                 # 4K crop x 760-2960, y 0-1237.5 (16:9)
SC = 1920 / CW                              # 0.8727 output px per 4K px
CH = 1080 / SC
TOP = (0, 0, 1920, 56)                      # legend bar
CAP = (0, 998, 1920, 1080)                  # caption bar
INSET = (568, 528, 1304, 982)               # ground-station inset: title strip 40 + picture 736x414 (16:9)
INSET_STRIP = 40
WIN = (1336, 422, 1896, 982)                # crossing window: title strip 40 + picture 560x520 (only during crossings)
WIN_STRIP = 40
ZOOM = 2.0                                  # window magnification relative to the main view
WSC = SC * ZOOM                             # 1.745 window px per 4K px -> the window shows 321x298 4K px
GS_PANEL = (600, 100, 1250, 440)            # ground-station 3D view, inside the panel below its header (1280x720 px)
GS_ZOOM = 1.5                               # inset picture px per ground-station px -> crop 501x282
GS_OFFSET = 19.57                           # ground-station u = camera t + 19.57 s (track/events.json "sync", +-0.07 s)
TS_BOX = (760, 120, 1010, 190)              # 4K box of the burned-in clock (only ':51:13' falls in the crop): inpainted

# ---- colours (RGB)
D1 = (59, 130, 246); D2 = (232, 89, 12); HALO = (12, 12, 12); WHITE = (255, 255, 255)
TEAM = {"drone_1": D1, "drone_2": D2}

# ---- marks, px at 1920 wide
RING_R, RING_W, HALO_W, HALO_A = 44, 4, 8, 170          # encloses a 52-79 px drone
FILT_R, FILT_W, FILT_HALO = 54, 2, 5                    # white outer ring while the safety filter acts
POP_S, POP_R1 = 0.5, 96                                 # white pop ring at the start of each filter interval
TRAIL_S, TRAIL_W0, TRAIL_W1, TRAIL_A = 1.0, 6, 2, 0.85  # trail: 1 s long, 6 px at the drone -> 2 px, alpha 0.85 -> 0
PAD_X, PAD_Y, PILL_R, PILL_OUT, LEAD_W, LEAD_HALO, GAP = 10, 5, 8, 2, 3, 7, 6
LEADS = (20, 55, 100)

# ---- timings, s
WORDS = [(0.0, 11.0), (33.6, 99.0)]   # name pills: take-off to just before the first crossing; hold + landing
FADE = 0.4
WIN_PRE, WIN_POST, WIN_FADE, WIN_MERGE = 0.8, 0.8, 0.2, 0.4
WIN_MAX_DIST = 250                    # 4K px: a crossing gets a window only if the pair is this close in the image


def _a(rgb, al): return (*rgb, int(max(0, min(255, al))))
def o(x, y): return ((x - CX0) * SC, (y - CY0) * SC)          # 4K -> output


def _win(t, a, b, fade=FADE):
    if t < a or t > b: return 0.0
    fin = 1.0 if a <= 0 else min(1.0, (t - a) / fade)
    return max(0.0, min(fin, (b - t) / fade))


def _ring(dr, x, y, r, col, alpha=1.0, w=RING_W, halo=HALO_W, halo_a=HALO_A):
    e = (halo - w) / 2
    dr.ellipse([x - r - e - w / 2, y - r - e - w / 2, x + r + e + w / 2, y + r + e + w / 2], outline=_a(HALO, halo_a * alpha), width=int(halo))
    dr.ellipse([x - r - w / 2, y - r - w / 2, x + r + w / 2, y + r + w / 2], outline=_a(col, 255 * alpha), width=int(w))


def _trail(dr, pts, t, col, head, k=1.0, r_clear=RING_R + 4):
    """pts: [(ti, X, Y)] already mapped to this layer's px. Tapered, fading; nothing inside the ring."""
    segs = []
    for (t0, x0, y0), (t1, x1, y1) in zip(pts, pts[1:]):
        if t1 - t0 > 0.16: continue                                     # gap (track not seen): break the line
        if math.hypot(x1 - head[0], y1 - head[1]) < r_clear * k: continue
        u = max(0.0, 1 - (t - t1) / TRAIL_S)
        if u <= 0: continue
        segs.append(((x0, y0, x1, y1), u))
    for (s, u) in segs:
        dr.line(s, fill=_a(HALO, 90 * u), width=int(round((TRAIL_W1 + (TRAIL_W0 - TRAIL_W1) * u) * k + 4)))
    for (s, u) in segs:
        dr.line(s, fill=_a(col, 255 * TRAIL_A * u), width=int(round((TRAIL_W1 + (TRAIL_W0 - TRAIL_W1) * u) * k)))


def _overlap(a, b):
    w = min(a[2], b[2]) - max(a[0], b[0]); h = min(a[3], b[3]) - max(a[1], b[1])
    return w > 0 and h > 0


def _place(q, w, h, marks, pills, keepout, prev=None):
    """House placement (label-spec.md): 12 directions x 3 leader lengths, lowest cost, >=1000 = no free spot."""
    best = (None, 1e9); base = RING_R + 4
    for k in range(12):
        ang = math.radians(-90 + 30 * k); c, s = math.cos(ang), math.sin(ang)
        for d in [base + L for L in LEADS]:
            ax, ay = q[0] + d * c, q[1] + d * s; cx, cy = ax + c * w / 2, ay + s * h / 2
            r = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
            cost = 0.4 * (d - base) + 4 * min(k, 12 - k)
            if r[0] < 12 or r[2] > 1908 or r[1] < TOP[3] + 8 or r[3] > CAP[1] - 8: cost += 1000
            cost += 1000 * sum(_overlap(r, m) for m in marks + keepout)
            cost += 1000 * sum(_overlap(r, (p[0] - GAP, p[1] - GAP, p[2] + GAP, p[3] + GAP)) for p in pills)
            if prev is not None and (k, d) != prev: cost += 40
            if cost < best[1]: best = ((r, (k, d)), cost)
    return best


def _pill(dr, q, rect, text, fill, alpha, font=F_LAB, txt=WHITE):
    x0, y0, x1, y1 = rect
    px, py = min(max(q[0], x0), x1), min(max(q[1], y0), y1); L = math.hypot(px - q[0], py - q[1]); rr = RING_R + 3
    if L > rr + 6:
        sx, sy = q[0] + (px - q[0]) * rr / L, q[1] + (py - q[1]) * rr / L
        dr.line([(sx, sy), (px, py)], fill=_a(HALO, HALO_A * alpha), width=LEAD_HALO)
        dr.line([(sx, sy), (px, py)], fill=_a(fill, 255 * alpha), width=LEAD_W)
    dr.rounded_rectangle(rect, radius=PILL_R, fill=_a(fill, 235 * alpha), outline=_a(HALO, 255 * alpha), width=PILL_OUT)
    bb = dr.textbbox((0, 0), text, font=font)
    dr.text(((x0 + x1) / 2 - (bb[0] + bb[2]) / 2, (y0 + y1) / 2 - (bb[1] + bb[3]) / 2), text, font=font, fill=_a(txt, 255 * alpha))


def _in(t, ivs): return any(a <= t <= b for a, b in ivs)


def windows(events):
    """Crossing-window spans [(open, close, [crossings])]: t_ca-0.8 .. t_ca+0.8, merged when < 0.4 s apart."""
    out = []
    for c in sorted(events.get("crossings", []), key=lambda c: c["t"]):
        a, b = c["t"] - WIN_PRE, c["t"] + WIN_POST
        if out and a - out[-1][1] < WIN_MERGE: out[-1] = (out[-1][0], b, out[-1][2] + [c])
        else: out.append((a, b, [c]))
    return out


def _region_center(t, cs):
    """Window region centre (4K): the pair midpoint at the nearest t_ca, smoothstep-eased over 0.4 s between two."""
    if len(cs) == 1: return cs[0]["mid"]
    for c0, c1 in zip(cs, cs[1:]):
        tm = (c0["t"] + c1["t"]) / 2
        if t <= tm + 0.2:
            u = min(1.0, max(0.0, (t - (tm - 0.2)) / 0.4)); u = u * u * (3 - 2 * u)
            return (c0["mid"][0] + (c1["mid"][0] - c0["mid"][0]) * u, c0["mid"][1] + (c1["mid"][1] - c0["mid"][1]) * u)
    return cs[-1]["mid"]


def caption(t, ev):
    """One caption per stage (>= 4.4 s each), never per meeting: it would flip every 2.3 s."""
    f = ev["filter"]
    if t < ev["eight_start"]: return "Take-off: two Starling 2 Max drones climb to their start points. Nobody is on the sticks."
    if t < f[1][0]: return "CMU's figure-eight at 2.0 m/s, flown in Singapore. Nobody is on the sticks."
    if t < f[3][0]: return "Each time they meet head-on, the safety filter eases them apart. Watch the 2\u00d7 window."
    if t < ev["hold"]: return "A white outer ring marks a drone while the safety filter is correcting its path."
    if t < ev["land"]: return "The eight ends: both drones brake, hold, then move off to their landing spots."
    return "Landing: watch them swap sides. drone_1 lands on the right, drone_2 on the left."


def _repaint_clock(f):
    x0, y0, x1, y1 = TS_BOX; roi = f[y0:y1, x0:x1]
    m = (cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY) < 70).astype(np.uint8) * 255
    m = cv2.dilate(m, np.ones((7, 7), np.uint8))
    f[y0:y1, x0:x1] = cv2.inpaint(roi, m, 7, cv2.INPAINT_TELEA)


def _panel(base, rect, strip, title, picture, extra=None, alpha=1.0):
    """Framed panel: soft shadow, 3 px dark frame, title strip, picture. alpha <1 = fading in/out."""
    x0, y0, x1, y1 = rect; W, H = x1 - x0, y1 - y0
    lay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    sh = Image.new("RGBA", base.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle([x0 + 6, y0 + 6, x1 + 6, y1 + 6], fill=(0, 0, 0, 130))
    lay = Image.alpha_composite(lay, sh.filter(ImageFilter.GaussianBlur(8)))
    d = ImageDraw.Draw(lay)
    d.rectangle([x0 - 3, y0 - 3, x1 + 2, y1 + 2], fill=(12, 12, 12, 255))
    lay.paste(picture, (x0, y0 + strip))
    d.rectangle([x0, y0, x1 - 1, y0 + strip - 1], fill=(14, 14, 14, 255))
    fs = 26 if strip == WIN_STRIP and rect == WIN else 24
    fnt = F(fs)
    while d.textlength(title, font=fnt) > W - 24 and fs > 22: fs -= 1; fnt = F(fs)
    d.text((x0 + 12, y0 + strip / 2), title, font=fnt, fill=(255, 255, 255, 255), anchor="lm")
    if extra: extra(d, x0, y0, x1, strip)
    if alpha < 1: lay.putalpha(lay.getchannel("A").point(lambda v: int(v * alpha)))
    return Image.alpha_composite(base, lay)


def draw(src4k, pos, t, events, gs_frame=None, gs_center=None, trails=None, state=None):
    st = state if state is not None else {}
    f = src4k.copy(); _repaint_clock(f)
    main = cv2.resize(f[CY0:int(round(CY0 + CH)), CX0:CX0 + CW], (1920, 1080), interpolation=cv2.INTER_AREA)
    im = Image.fromarray(cv2.cvtColor(main, cv2.COLOR_BGR2RGB)).convert("RGBA")
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); dr = ImageDraw.Draw(ov)
    vis = {n: o(*p) for n, p in pos.items() if p is not None}
    filt = _in(t, events.get("filter", []))
    f_start = max([a for a, b in events.get("filter", []) if a <= t] or [-9])

    # 1) trails, then rings (+ filter ring, pop)
    for n, q in vis.items():
        pts = [(ti, *o(x, y)) for ti, x, y in (trails or {}).get(n, []) if t - TRAIL_S <= ti <= t]
        _trail(dr, pts + [(t, *q)], t, TEAM[n], q)
    for n, q in vis.items():
        if filt: _ring(dr, *q, FILT_R, WHITE, w=FILT_W, halo=FILT_HALO, halo_a=120)
        u = (t - f_start) / POP_S
        if 0 <= u < 1: _ring(dr, *q, RING_R + (POP_R1 - RING_R) * u, WHITE, alpha=1 - u, w=max(1, round(4 - 3 * u)), halo=6)
        _ring(dr, *q, RING_R, TEAM[n])

    # crossing window state (decided before words: an open window is a keep-out)
    wspan = next(((a, b, cs) for a, b, cs in windows(events) if a - WIN_FADE <= t <= b + WIN_FADE), None)
    walpha = 0.0
    if wspan:
        a, b, cs = wspan; walpha = max(0.0, min(1.0, (t - (a - WIN_FADE)) / WIN_FADE, (b + WIN_FADE - t) / WIN_FADE))
        wr = (WIN[0] - 8, WIN[1] - 8, WIN[2] + 8, WIN[3] + 8)
        for n, q in vis.items():   # guard: the window must never cover a drone
            if _overlap(wr, (q[0] - RING_R, q[1] - RING_R, q[0] + RING_R, q[1] + RING_R)): print(f"WARNING t={t:.2f}: window over {n}"); walpha = 0.0

    # 2) words: name pills in their windows, only where free
    keep = [(INSET[0] - 8, INSET[1] - 8, INSET[2] + 8, INSET[3] + 8)] + ([(WIN[0] - 8, WIN[1] - 8, WIN[2] + 8, WIN[3] + 8)] if walpha > 0 else [])
    marks = [(q[0] - RING_R - 4 - GAP, q[1] - RING_R - 4 - GAP, q[0] + RING_R + 4 + GAP, q[1] + RING_R + 4 + GAP) for q in vis.values()]
    pills = []
    for n, q in sorted(vis.items()):
        al = max(_win(t, a, b) for a, b in WORDS)
        if al <= 0: continue
        bb = dr.textbbox((0, 0), n, font=F_LAB); w, h = bb[2] - bb[0] + 2 * PAD_X, 28 + 2 * PAD_Y + 2
        res, cost = _place(q, w, h, marks, pills, keep, prev=st.get(n))
        if res is None or cost >= 1000: continue
        rect, slot = res; st[n] = slot; pills.append(rect); _pill(dr, q, rect, n, TEAM[n], al)

    # 3) legend bar + caption bar
    dr.rectangle(TOP, fill=(14, 14, 14, 235))
    dr.text((24, 28), "Two Starlings · CMU's figure-eight · Singapore · 16 Nov 2026", font=F_BAN, fill=(255, 255, 255, 255), anchor="lm")
    items = [("drone_1", D1, False), ("drone_2", D2, False), ("safety filter acting", WHITE, True)]
    wd = [34 + 10 + dr.textlength(s, font=F_BAN) for s, _, _ in items]
    x = 1920 - 24 - sum(wd) - 32 * (len(items) - 1)
    for (s, col, dbl), w in zip(items, wd):
        cx = x + 17
        if dbl:
            dr.ellipse([cx - 15, 13, cx + 15, 43], outline=(255, 255, 255, 255), width=2)
            dr.ellipse([cx - 9, 19, cx + 9, 37], outline=(170, 170, 170, 255), width=3)
        else:
            dr.ellipse([cx - 12, 16, cx + 12, 40], outline=_a(col, 255), width=4)
        dr.text((x + 44, 28), s, font=F_BAN, fill=(255, 255, 255, 255), anchor="lm"); x += w + 32
    dr.rectangle(CAP, fill=(20, 20, 20, 255))
    cap, fs = caption(t, events), 34
    while fs > 26 and dr.textlength(cap, font=F(fs)) > 1920 - 2 * 44: fs -= 2
    dr.text((44, (CAP[1] + CAP[3]) / 2), cap, font=F(fs), fill=(255, 255, 255, 255), anchor="lm")
    im = Image.alpha_composite(im, ov)

    # 4) ground-station inset (whole clip)
    if gs_frame is not None:
        pw, ph = INSET[2] - INSET[0], INSET[3] - INSET[1] - INSET_STRIP
        cw, ch = pw / GS_ZOOM, ph / GS_ZOOM
        gx, gy = gs_center if gs_center else ((GS_PANEL[0] + GS_PANEL[2]) / 2, (GS_PANEL[1] + GS_PANEL[3]) / 2)
        lx = int(round(min(max(gx - cw / 2, GS_PANEL[0]), GS_PANEL[2] - cw))); ty = int(round(min(max(gy - ch / 2, GS_PANEL[1]), GS_PANEL[3] - ch)))
        crop = gs_frame[ty:ty + int(round(ch)), lx:lx + int(round(cw))]
        pic = Image.fromarray(cv2.cvtColor(cv2.resize(crop, (pw, ph), interpolation=cv2.INTER_LANCZOS4), cv2.COLOR_BGR2RGB)).convert("RGBA")
        im = _panel(im, INSET, INSET_STRIP, "Ground station · Sphere = CBF Safety Assist Zone", pic)

    # 5) crossing window (live 2x of the same source frame, marks drawn at 2x, strokes unscaled)
    if walpha > 0:
        a, b, cs = wspan; mx, my = _region_center(t, cs)
        pw, ph = WIN[2] - WIN[0], WIN[3] - WIN[1] - WIN_STRIP
        rw, rh = pw / WSC, ph / WSC
        rx0 = min(max(mx - rw / 2, 0), 3840 - rw); ry0 = min(max(my - rh / 2, 0), 2160 - rh)
        M = np.float32([[WSC, 0, -rx0 * WSC], [0, WSC, -ry0 * WSC]])
        zoom = cv2.warpAffine(f, M, (pw, ph), flags=cv2.INTER_LANCZOS4)
        pic = Image.fromarray(cv2.cvtColor(zoom, cv2.COLOR_BGR2RGB)).convert("RGBA")
        wo = Image.new("RGBA", pic.size, (0, 0, 0, 0)); wd_ = ImageDraw.Draw(wo)
        w4 = lambda x, y: ((x - rx0) * WSC, (y - ry0) * WSC)
        for n, p in pos.items():
            if p is None: continue
            q = w4(*p); pts = [(ti, *w4(x, y)) for ti, x, y in (trails or {}).get(n, []) if t - TRAIL_S <= ti <= t]
            _trail(wd_, pts + [(t, *q)], t, TEAM[n], q, k=1.0, r_clear=2 * RING_R + 4)
        for n, p in pos.items():
            if p is None: continue
            q = w4(*p)
            if filt: _ring(wd_, *q, 2 * FILT_R, WHITE, w=FILT_W, halo=FILT_HALO, halo_a=120)
            _ring(wd_, *q, 2 * RING_R, TEAM[n])
        pic = Image.alpha_composite(pic, wo)

        def tag(d, x0, y0, x1, strip):
            if not filt: return
            txt = "safety filter acting"; tw = d.textlength(txt, font=F_PILL)
            d.rounded_rectangle([x1 - 12 - tw - 20, y0 + 6, x1 - 12, y0 + strip - 6], radius=8, fill=(255, 255, 255, 255))
            d.text((x1 - 12 - tw - 10, y0 + strip / 2), txt, font=F_PILL, fill=(14, 14, 14, 255), anchor="lm")
        im = _panel(im, WIN, WIN_STRIP, "Crossing · 2×", pic, extra=tag, alpha=walpha)

    return cv2.cvtColor(np.array(im.convert("RGB")), cv2.COLOR_RGB2BGR)


# ------------------------------------------------------------------------------------------------ mock frames
if __name__ == "__main__":
    import csv, json
    S = os.path.dirname(os.path.abspath(__file__)); SRC = f"{S}/src"
    tr = f"{S}/../track/tracks.csv"
    tr = tr if os.path.exists(tr) else f"{SRC}/mock_tracks.csv"      # the tracking engineer's file wins when it exists
    T = {}
    for r in csv.DictReader(open(tr)):
        T.setdefault(r["name"], {})[int(r["frame"])] = (float(r["x"]), float(r["y"]), int(float(r["seen"])))
    E = json.load(open(f"{S}/../track/events.json"))
    filt = [(c["t_start"], c["t_end"]) for c in E["cbf_active_gs"]]
    xs = [{"t": c["t"], "mid": ((c["drone_1_xy"][0] + c["drone_2_xy"][0]) / 2, (c["drone_1_xy"][1] + c["drone_2_xy"][1]) / 2)}
          for c in E["crossings"] if c["image_distance_px"] <= WIN_MAX_DIST and any(a - 0.3 <= c["t"] <= b + 0.3 for a, b in filt)]
    EV = {"crossings": xs, "filter": filt, "eight_start": 10.1,
          "hold": E["figure_eight"]["end_t_from_gs"], "land": 38.0}
    G = {}
    for r in csv.DictReader(open(f"{S}/../track/gs-tracks.csv")):
        if r["seen"] == "1": G.setdefault(int(r["gs_frame"]), []).append((float(r["x"]), float(r["y"])))
    def gs_center(j):   # 1 s centred moving average of the markers' midpoint
        m = [(sum(p[0] for p in G[k]) / len(G[k]), sum(p[1] for p in G[k]) / len(G[k])) for k in range(j - 15, j + 16) if k in G]
        return (sum(p[0] for p in m) / len(m), sum(p[1] for p in m) / len(m)) if m else None
    # mock frames: (source frame, file, ground-station centre by eye in GS px)
    MOCK = [(70, "k0070.png", "take-off"), (246, "k0246.png", "crossing 1 (lower = LED only)"),
            (278, "k0278.png", "crossing 1, 2nd pass"), (436, "k0436.png", "crossing 3"),
            (500, "f0500.jpg", "mid-eight"), (600, "k0600.png", "drone_2 low vs desks"),
            (624, "k0624.png", "crossing 5"), (860, "k0860.png", "landing (sides swapped)")]
    need = {round((fr / 20 + GS_OFFSET) * 30): fr for fr, *_ in MOCK}; GJ = {v: k for k, v in need.items()}; GS = {}
    cap = cv2.VideoCapture(os.path.expanduser("~/AirStack-starling-max2/videos/Fig8_CBF_two_drones_thermal_ui.mp4")); i = 0
    while len(GS) < len(need):
        ok, g = cap.read()
        if not ok: break
        if i in need: GS[need[i]] = g
        i += 1
    tiles = []
    for fr, fn, label in MOCK:
        gc = gs_center(GJ[fr])
        t = fr / 20; src = cv2.imread(f"{SRC}/{fn}")
        pos = {n: (T[n][fr][0], T[n][fr][1]) if T[n][fr][2] else None for n in T}
        trails = {n: [(k / 20, T[n][k][0], T[n][k][1]) for k in range(max(0, fr - 20), fr) if T[n][k][2]] for n in T}
        out = draw(src, pos, t, EV, GS.get(fr), gc, trails)
        cv2.imwrite(f"{S}/mock-{fr:04d}.jpg", out, [cv2.IMWRITE_JPEG_QUALITY, 92])
        tl = cv2.resize(out, (960, 540), interpolation=cv2.INTER_AREA)
        cv2.rectangle(tl, (0, 30), (330, 60), (0, 0, 0), -1)
        cv2.putText(tl, f"f{fr:04d} t={t:4.2f}s {label}", (6, 52), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2); tiles.append(tl)
    # landscape phone: the 1600 px clip shown 845 px wide
    ph = cv2.resize(cv2.resize(cv2.imread(f"{S}/mock-0246.jpg"), (1600, 900), interpolation=cv2.INTER_AREA), (845, 475), interpolation=cv2.INTER_AREA)
    cv2.imwrite(f"{S}/mock-phone-845.jpg", ph, [cv2.IMWRITE_JPEG_QUALITY, 92])
    tile = np.full((540, 960, 3), 40, np.uint8); tile[40:515, 57:902] = ph
    cv2.putText(tile, "f0246 at landscape-phone size (845 px wide, real pixels)", (60, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    tiles.append(tile)
    while len(tiles) % 3: tiles.append(np.zeros_like(tiles[0]))
    cv2.imwrite(f"{S}/mock-sheet.jpg", np.vstack([np.hstack(tiles[k:k + 3]) for k in range(0, len(tiles), 3)]), [cv2.IMWRITE_JPEG_QUALITY, 88])
    print("events:", {k: v for k, v in EV.items() if k != "crossings"}, "\ntracks:", tr, "| windows:", [(round(a, 2), round(b, 2), len(c)) for a, b, c in windows(EV)], "| filter:", filt)
