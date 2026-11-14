"""Labelling scheme from label-spec.md, as a drop-in draw() for track.py.

draw(frame_bgr, tracks, t, state=None) -> frame_bgr (full 1920x1080, overlays drawn; caller crops rows 75-960)
  tracks: list of dicts {name, cls in Guard/Strike/DJI, x, y, seen}; optional key 'tagged_at' (s) overrides TAGS.
  state:  pass the same dict every frame in a video for label stickiness; None = stateless (mock frames).

Run as a script to render the mock frames: mock-<frame>.jpg and mock-sheet.jpg.
"""
import math, os
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_LAB = ImageFont.truetype(FONT, 28)      # on-video words
F_BAN = ImageFont.truetype(FONT, 30)      # banner + legend
F_CAP = ImageFont.truetype(FONT, 34)      # bottom caption (unchanged)

# colours (RGB). Team colours = site colours; legibility comes from the dark halo, not from the hue.
GUARD = (59, 130, 246); STRIKE = (235, 60, 60); ZONE = (255, 255, 255); HALO = (12, 12, 12)
TEAM = {"Guard": GUARD, "Strike": STRIKE, "DJI": ZONE}
WORD = {"Guard": "Guard", "Strike": "Strike", "DJI": "VIP drone"}

# geometry, px at 1920 wide
RING_R, RING_W, HALO_W, HALO_A = 17, 4, 8, 170          # Crazyflie ring: radius to stroke centre, stroke, halo stroke, halo alpha
ZONE_HALF, ZONE_ARM, ZONE_W = 42, 18, 4                 # the zone: corner brackets (box half-size, arm length, stroke)
PAD_X, PAD_Y, PILL_R, PILL_OUT = 10, 5, 8, 2            # word pill
LEAD_W, LEAD_HALO = 3, 7                                # leader line
GAP = 6                                                 # min clear gap between a pill and any mark or other pill
SAFE = (12, 140, 1908, 866)                             # pills must stay inside (below banner, above caption bar)
INSET = (1340, 640, 1920, 960)                          # ground-station inset in the final clip: keep out
DASH_DEG, GAP_DEG = 25, 20                              # tagged ring: 8 dashes
LEADS, LEADS_FAR = (20, 55, 100), (150, 210)            # leader lengths tried, px from the mark's edge (FAR: tag pills + the zone)

# timings, seconds
WORDS_ALL = (0.0, 12.0); STRIKE_WORDS = (14.0, 17.0); END_WORDS = (27.5, 99.0); FADE = 0.4
POP_S, TAG_PILL_S = 0.5, 2.0
# tag times for the mocks = when the source video's own burned-in tag captions appear (cf11 25.1 s, cf10 25.3 s, cf12 27.0 s),
# with cf10/11/12 = S1/S2/S3 ASSUMED from the start layout in the inset. Take the real ones from the match log.
TAGS = {"S2": 25.1, "S1": 25.3, "S3": 27.0}


def _win(t, a, b, fade=FADE):
    """alpha 0..1 for a window [a,b] with linear fade-in/out of `fade` s (no fade-in at t=0)."""
    if t < a or t > b: return 0.0
    fin = 1.0 if a <= 0 else min(1.0, (t - a) / fade)
    return max(0.0, min(fin, (b - t) / fade))


def _a(rgb, alpha):
    return (*rgb, int(max(0, min(255, alpha))))


def _ring(dr, x, y, r, col, alpha=1.0, dashed=False, w=RING_W):
    box = [x - r, y - r, x + r, y + r]
    segs = [(a0, a0 + DASH_DEG) for a0 in range(0, 360, DASH_DEG + GAP_DEG)] if dashed else [(0, 360)]
    for a0, a1 in segs:
        dr.arc([box[0] - (HALO_W - w) / 2, box[1] - (HALO_W - w) / 2, box[2] + (HALO_W - w) / 2, box[3] + (HALO_W - w) / 2],
               a0, a1, fill=_a(HALO, HALO_A * alpha), width=HALO_W)
    for a0, a1 in segs:
        dr.arc(box, a0, a1, fill=_a(col, 255 * alpha), width=w)


def _brackets(dr, x, y, alpha=1.0):
    h, a = ZONE_HALF, ZONE_ARM
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = x + sx * h, y + sy * h
            pts = [(cx, cy - sy * a), (cx, cy), (cx - sx * a, cy)]
            dr.line(pts, fill=_a(HALO, HALO_A * alpha), width=ZONE_W + 4, joint="curve")
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = x + sx * h, y + sy * h
            dr.line([(cx, cy - sy * a), (cx, cy), (cx - sx * a, cy)], fill=_a(ZONE, 255 * alpha), width=ZONE_W, joint="curve")


def _overlap(a, b):
    w = min(a[2], b[2]) - max(a[0], b[0]); h = min(a[3], b[3]) - max(a[1], b[1])
    return w * h if (w > 0 and h > 0) else 0.0


def _mark_box(q):
    r = ZONE_HALF + ZONE_W if q["cls"] == "DJI" else RING_R + HALO_W / 2
    return (q["x"] - r - GAP, q["y"] - r - GAP, q["x"] + r + GAP, q["y"] + r + GAP)


def _place(q, w, h, marks, pills, prev=None, far=False):
    """Pick a free spot for a w x h pill attached to drone q. Returns (rect, cost); cost >= 1000 means no free spot."""
    best = (None, 1e9)
    base = (ZONE_HALF if q["cls"] == "DJI" else RING_R) + 4       # leader lengths are measured from the mark's edge
    dists = [base + L for L in (LEADS + LEADS_FAR if far else LEADS)]
    for k in range(12):
        ang = math.radians(-90 + 30 * k)
        c, s = math.cos(ang), math.sin(ang)
        for d in dists:
            ax, ay = q["x"] + d * c, q["y"] + d * s                     # nearest point of the pill to the drone
            cx, cy = ax + c * w / 2, ay + s * h / 2
            r = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
            cost = 0.4 * (d - base) + 4 * min(k, 12 - k)                         # prefer close and above
            if r[0] < SAFE[0] or r[1] < SAFE[1] or r[2] > SAFE[2] or r[3] > SAFE[3]: cost += 1000
            if _overlap(r, INSET): cost += 1000
            for m in marks: cost += 1000 if _overlap(r, m) else 0
            for p in pills: cost += 1000 if _overlap(r, (p[0] - GAP, p[1] - GAP, p[2] + GAP, p[3] + GAP)) else 0
            # leader must not pass over another drone's mark
            for m in marks:
                mx, my = (m[0] + m[2]) / 2, (m[1] + m[3]) / 2
                if abs(mx - q["x"]) < 1 and abs(my - q["y"]) < 1: continue
                tt = max(0.0, min(1.0, ((mx - q["x"]) * c + (my - q["y"]) * s) / max(d, 1)))
                px, py = q["x"] + c * d * tt, q["y"] + s * d * tt
                if math.hypot(px - mx, py - my) < (m[2] - m[0]) / 2: cost += 300
            if prev is not None and (k, d) != prev: cost += 40             # stickiness (video only)
            if cost < best[1]: best = ((r, (k, d)), cost)
    return best


def _pill(dr, q, rect, text, fill, txt, alpha, outline=HALO):
    x0, y0, x1, y1 = rect
    # leader: from ring edge to the pill's nearest point
    px, py = min(max(q["x"], x0), x1), min(max(q["y"], y0), y1)
    L = math.hypot(px - q["x"], py - q["y"])
    rr = (ZONE_HALF if q["cls"] == "DJI" else RING_R) + 3
    if q["cls"] == "DJI":  # leave from the bracket box edge
        k = ZONE_HALF / max(abs(px - q["x"]), abs(py - q["y"]), 1e-6); rr = L * min(k, 1.0) + 3
    if L > rr + 6:
        sx, sy = q["x"] + (px - q["x"]) * rr / L, q["y"] + (py - q["y"]) * rr / L
        dr.line([(sx, sy), (px, py)], fill=_a(HALO, HALO_A * alpha), width=LEAD_HALO)
        dr.line([(sx, sy), (px, py)], fill=_a(outline if outline != HALO else fill, 255 * alpha), width=LEAD_W)
    dr.rounded_rectangle(rect, radius=PILL_R, fill=_a(fill, 235 * alpha), outline=_a(outline, 255 * alpha), width=PILL_OUT)
    bb = dr.textbbox((0, 0), text, font=F_LAB)
    dr.text(((x0 + x1) / 2 - (bb[0] + bb[2]) / 2, (y0 + y1) / 2 - (bb[1] + bb[3]) / 2), text, font=F_LAB, fill=_a(txt, 255 * alpha))


def _pill_size(dr, text):
    bb = dr.textbbox((0, 0), text, font=F_LAB)
    return bb[2] - bb[0] + 2 * PAD_X, 28 + 2 * PAD_Y + 2


def stage(t):
    if t < 14: return "The DJI lifts off; the four Guard escorts hold a ring above it"
    if t < 15: return "Ready"
    if t < 25.1: return "Match on: three Strike drones go for the VIP drone"
    if t < 27.0: return "The Guard escorts tag the Strike drones, one by one"
    return "Guard team wins: all three Strike drones tagged, the VIP drone never reached"


def _banner(dr, t, tags):
    dr.rectangle([0, 75, 1920, 131], fill=(14, 14, 14, 235))
    dr.text((24, 87), "Strike vs Guard  ·  6 Nov 2026", font=F_BAN, fill=(255, 255, 255, 255))
    # legend + tally, right-aligned; the icons are the on-video marks at 0.6 scale
    items = [("Guard", 4, None), ("Strike", 3, tags), ("VIP drone (DJI, flown by hand)", 0, None)]
    widths = []
    for word, n, _ in items:
        widths.append((n * 28 if n else 34) + 10 + dr.textlength(word, font=F_BAN))
    x = 1920 - 24 - sum(widths) - 36 * (len(items) - 1); yc = 103
    for (word, n, tg), wd in zip(items, widths):
        if n:
            for i in range(n):
                cx = x + 11 + i * 28
                ntag = sum(1 for v in (tg or {}).values() if v <= t)
                gone = i >= n - ntag            # tagged Strike icons turn into dashed ghosts, from the right
                col = GUARD if word == "Guard" else STRIKE
                box = [cx - 10, yc - 10, cx + 10, yc + 10]
                if gone:
                    for a0 in range(0, 360, 45): dr.arc(box, a0, a0 + 25, fill=_a(col, 150), width=3)
                else:
                    dr.ellipse(box, outline=_a(col, 255), width=4)
            tx = x + n * 28 + 10
        else:
            h, a = 13, 7
            for sx in (-1, 1):
                for sy in (-1, 1):
                    cx, cy = x + 15 + sx * h, yc + sy * h
                    dr.line([(cx, cy - sy * a), (cx, cy), (cx - sx * a, cy)], fill=_a(ZONE, 255), width=3)
            tx = x + 34 + 10
        dr.text((tx, 87), word, font=F_BAN, fill=(255, 255, 255, 255))
        x += wd + 36


def draw(frame_bgr, tracks, t, state=None):
    im = Image.fromarray(cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)).convert("RGBA")
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); dr = ImageDraw.Draw(ov)
    vis = [q for q in tracks if q.get("seen", True)]
    tags = {q["name"]: q.get("tagged_at", TAGS.get(q["name"])) for q in tracks if q["cls"] == "Strike"}
    tags = {k: v for k, v in tags.items() if v is not None}
    st = state if state is not None else {}

    # 1) marks (always; never drawn for a track that is not currently seen)
    for q in vis:
        if q["cls"] == "DJI":
            _brackets(dr, q["x"], q["y"]); continue
        col = TEAM[q["cls"]]; T = tags.get(q["name"])
        if q["cls"] == "Strike" and T is not None and t >= T:
            u = (t - T) / POP_S
            if u < 1:   # tag "pop": white ring expanding 17 -> 45 px, fading out
                _ring(dr, q["x"], q["y"], RING_R + 28 * u, (255, 255, 255), alpha=1 - u, w=max(1, round(4 - 3 * u)))
            _ring(dr, q["x"], q["y"], RING_R, col, alpha=0.8, dashed=True, w=3)
        else:
            _ring(dr, q["x"], q["y"], RING_R, col)

    # 2) words. Priority: tag pills > the zone > team words in their time windows.
    marks = [_mark_box(q) for q in vis]
    pills, todo = [], []
    for q in vis:
        T = tags.get(q["name"])
        if T is not None and T <= t < T + TAG_PILL_S:
            a = min(1.0, (t - T) / 0.2, (T + TAG_PILL_S - t) / FADE)
            todo.append((0, q, "tagged", (255, 255, 255), STRIKE, a, True, STRIKE))
    dji = [q for q in vis if q["cls"] == "DJI"]
    for q in dji:
        todo.append((1, q, WORD["DJI"], ZONE, (10, 10, 10), 1.0, True, HALO))
    for q in vis:
        if q["cls"] == "DJI": continue
        a = _win(t, *WORDS_ALL)
        if q["cls"] == "Strike": a = max(a, _win(t, *STRIKE_WORDS))
        a = max(a, _win(t, *END_WORDS))
        T = tags.get(q["name"])
        if T is not None and t >= T and t < T + TAG_PILL_S: a = 0          # the tag pill speaks for it
        if a <= 0: continue
        if T is not None and t >= T:   # out of play: dark pill, red outline, pale-red word
            todo.append((2, q, WORD[q["cls"]], (28, 28, 28), (255, 150, 150), a, False, STRIKE))
        else:
            todo.append((2, q, WORD[q["cls"]], TEAM[q["cls"]], (255, 255, 255), a, False, HALO))
    for pri, q, text, fill, txt, a, far, outl in sorted(todo, key=lambda z: z[0]):
        w, h = _pill_size(dr, text)
        key = (q["name"], text)
        res, cost = _place(q, w, h, marks, pills, prev=st.get(key), far=far)
        if res is None or cost >= 1000: continue          # no free spot: ring only, never cover a drone
        rect, slot = res; st[key] = slot; pills.append(rect)
        _pill(dr, q, rect, text, fill, txt, a, outline=outl)

    # 3) banner (legend + tally) and caption bar
    _banner(dr, t, tags)
    dr.rectangle([0, 878, 1920, 960], fill=(20, 20, 20, 255))
    cap, fs = stage(t), 34
    while fs > 26 and dr.textlength(cap, font=ImageFont.truetype(FONT, fs)) > INSET[0] - 44 - 24: fs -= 2   # must end left of the inset
    dr.text((44, 919 - fs // 2 - 2), cap, font=ImageFont.truetype(FONT, fs), fill=(255, 255, 255, 255))
    out = Image.alpha_composite(im, ov).convert("RGB")
    return cv2.cvtColor(np.array(out), cv2.COLOR_RGB2BGR)


# ---------------------------------------------------------------- mock frames
def _T(G1, G2, G3, G4, S1, S2, S3, DJI):
    out = []
    for n, p in zip(["G1", "G2", "G3", "G4", "S1", "S2", "S3", "DJI"], [G1, G2, G3, G4, S1, S2, S3, DJI]):
        cls = "DJI" if n == "DJI" else ("Guard" if n[0] == "G" else "Strike")
        out.append(dict(name=n, cls=cls, x=p[0] if p else 0, y=p[1] if p else 0, seen=p is not None))
    return out

# positions: Crazyflies from the track.py tracker where its cross sits on a light (checked on 2x zooms);
# the DJI read by eye on every frame after f0001 (the tracker loses it once airborne).
MOCK = {
    1:   _T((739, 319), (1100, 329), (1303, 439), (825, 448), (905, 622), (707, 637), (473, 641), (985, 504)),
    481: _T((729, 333), (1078, 341), (1183, 437), (851, 451), (880, 516), (776, 529), (649, 547), (1022, 363)),
    601: _T((823, 347), (963, 342), (975, 406), (914, 363), (863, 447), (854, 416), (811, 399), (1123, 355)),
    661: _T((829, 397), (1006, 407), (1080, 437), (913, 367), (1009, 505), (904, 454), (735, 352), (1173, 361)),
    721: _T((1040, 397), (1244, 431), (1321, 427), (969, 285), (1220, 490), (1118, 453), (836, 286), (1277, 372)),
    763: _T((1122, 388), (1224, 408), (1299, 409), (1075, 297), (1280, 487), (1155, 446), (978, 283), (1215, 367)),
    781: _T((1100, 381), (1192, 404), (1267, 410), (1063, 304), (1265, 493), (1155, 456), (1015, 285), (1165, 352)),
    901: _T((1055, 367), (1013, 492), (1242, 339), (1015, 375), (1223, 647), (1118, 640), None, (1110, 327)),
}

if __name__ == "__main__":
    S = os.path.dirname(os.path.abspath(__file__))
    cap = cv2.VideoCapture(f"{S}/inset.mp4")
    bg = np.load(f"{S}/bg.npy"); bgg = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY).astype(int)
    tiles = []
    for f, tr in MOCK.items():
        t = (f - 1) / 30.0
        fr = cv2.imread(f"{S}/src/f{f:04d}.jpg")
        if t >= 22:   # same as track.py: paint the floor back over the source's burned-in tag captions (they say "attacker")
            g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY).astype(int)
            for y in range(580, 965):
                dark = (g[y, :1200] < 62) & (bgg[y, :1200] - g[y, :1200] > 35)
                if dark.sum() > 120:
                    xr = min(1200, int(np.where(dark)[0].max()) + 14); fr[y, :xr] = bg[y, :xr]
        fr = draw(fr, tr, t)
        cap.set(cv2.CAP_PROP_POS_FRAMES, f - 1); ok, ins = cap.read()
        if ok:   # the ground-station inset as composited in the final clip (560 px wide, bottom right)
            ins = cv2.resize(ins, (560, 299)); fr[646:945, 1346:1906] = ins
        out = fr[75:960]
        cv2.imwrite(f"{S}/mock-{f:04d}.jpg", out, [cv2.IMWRITE_JPEG_QUALITY, 92])
        tl = cv2.resize(out, (960, 442), interpolation=cv2.INTER_AREA)
        cv2.rectangle(tl, (0, 30), (190, 62), (0, 0, 0), -1)
        cv2.putText(tl, f"f{f:04d} t={t:4.1f}s", (6, 54), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        tiles.append(tl)
    # last tile: f0661 at phone size (final 1600 px clip shown 845 px wide = landscape phone), real pixels, centre crop
    ph = cv2.resize(cv2.imread(f"{S}/mock-0661.jpg"), (845, 390), interpolation=cv2.INTER_AREA)
    tile = np.full((442, 960, 3), 40, np.uint8); tile[26:416, 57:902] = ph
    cv2.putText(tile, "f0661 at landscape-phone size (845 px wide)", (60, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    tiles.append(tile)
    rows = [np.hstack(tiles[i:i + 3]) for i in range(0, len(tiles), 3)]
    cv2.imwrite(f"{S}/mock-sheet.jpg", np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 90])
    print("wrote", len(MOCK), "mocks + sheet")
