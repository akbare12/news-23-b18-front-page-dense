#!/usr/bin/env python3
"""news-23 b18 front-page-dense: Monday 23 November 2026, 31 stories, 6 regions.
Draws entry.png (1024x1024) with PIL only."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (26, 26, 26)
RED = (163, 30, 30)
DARKRED = (140, 20, 20)
NAVY = (24, 42, 84)
GRAY = (110, 108, 100)
LIGHT = (233, 226, 210)
GREEN = (30, 125, 50)
AMBER = (178, 106, 0)
BLUE = (21, 101, 192)

FDIR = "/usr/share/fonts/truetype/noto/"
def F(name, size):
    return ImageFont.truetype(os.path.join(FDIR, name), size)

SERIF_B = lambda s: F("NotoSerif-Bold.ttf", s)
SERIF = lambda s: F("NotoSerif-Regular.ttf", s)
SERIF_I = lambda s: F("NotoSerif-Italic.ttf", s)
SANS_B = lambda s: F("NotoSans-Bold.ttf", s)
SANS = lambda s: F("NotoSans-Regular.ttf", s)
SANS_I = lambda s: F("NotoSans-Italic.ttf", s)
DISPLAY = lambda s: F("NotoSerifDisplay-Black.ttf", s)

def wrap(draw, text, font, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def fit(draw, text, font, maxw, maxlines):
    """Wrap text, truncating with ellipsis to maxlines."""
    lines = wrap(draw, text, font, maxw)
    if len(lines) > maxlines:
        lines = lines[:maxlines]
        while lines and draw.textlength(lines[-1] + "…", font=font) > maxw:
            lines[-1] = lines[-1][:-1]
        lines[-1] += "…"
    return lines

def chip(draw, x, y, label, fill):
    f = SANS_B(8)
    w = int(draw.textlength(label, font=f)) + 8
    draw.rounded_rectangle([x, y, x + w, y + 12], radius=2, fill=fill)
    draw.text((x + 4, y + 1.5), label, font=f, fill=(255, 255, 255))
    return w

CHIP_FILL = {"REPORTED": GREEN, "CLAIM": AMBER, "DENIAL": RED, "ONGOING": BLUE}

def draw_text(draw, x, y, text, font, fill=INK):
    draw.text((x, y), text, font=font, fill=fill)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- top rule ----
d.rectangle([0, 0, W, 4], fill=RED)

# ---- masthead ----
d.text((14, 8), "THE WORLD TODAY", font=DISPLAY(56), fill=INK)
d.text((1024 - 14 - d.textlength("MONDAY 23 NOVEMBER 2026", font=SANS_B(22)), 16),
       "MONDAY 23 NOVEMBER 2026", font=SANS_B(22), fill=RED)
d.text((1024 - 14 - d.textlength("MONDAY EDITION · ALL TIMES GMT", font=SANS(10)), 44),
       "MONDAY EDITION · ALL TIMES GMT", font=SANS(10), fill=GRAY)

# ---- kicker ----
d.text((14, 72), "AI rout hits Asia  ·  Guterres: regulate AI  ·  US lead at record low",
       font=SERIF_I(15), fill=RED)
# meta line + legend chips
d.text((14, 92), "31 STORIES  ·  6 REGIONS  ·  EVERY ITEM DATED 23 NOV",
       font=SANS_B(11), fill=INK)
cx = 1024 - 14
for lab in reversed(["ONGOING", "DENIAL", "CLAIM", "REPORTED"]):
    f = SANS_B(8)
    w = int(d.textlength(lab, font=f)) + 8
    cx -= w + 6
    d.rounded_rectangle([cx, 91, cx + w, 103], radius=2, fill=CHIP_FILL[lab])
    d.text((cx + 4, 92.5), lab, font=f, fill=(255, 255, 255))

# ---- number strip ----
NUMS = [
    ("-3.3%", "Kospi Monday"),
    ("5.3", "US-China power gap"),
    ("11,762", "Ebola cases, DRC"),
    ("10T won", "Seoul rescue fund"),
    ("2%", "billionaire tax plan"),
    ("$450M", "Skubal's Mets deal"),
    ("165", "Russian missiles / week"),
    ("107.3B", "Anthropic IPO"),
]
y0, y1 = 108, 152
cw = (W - 28) / 8
for i, (n, lab) in enumerate(NUMS):
    x = 14 + i * cw
    if i:
        d.line([x - 4, y0 + 4, x - 4, y1 - 4], fill=(200, 190, 170), width=1)
    nf = SANS_B(26 if len(n) <= 6 else 22)
    d.text((x + cw / 2 - d.textlength(n, font=nf) / 2, y0 + 2), n, font=nf, fill=RED)
    d.text((x + cw / 2 - d.textlength(lab, font=SANS(9)) / 2, y0 + 30), lab, font=SANS(9), fill=INK)
d.line([14, y1, W - 14, y1], fill=INK, width=1)

# ---- region bar ----
REGIONS = [
    ("NORTH AMERICA 8", 8, (31, 93, 168)),
    ("EUROPE 6", 6, (24, 42, 84)),
    ("MIDDLE EAST 7", 7, (176, 92, 32)),
    ("AFRICA 2", 2, (120, 72, 20)),
    ("ASIA-PACIFIC 6", 6, (46, 125, 50)),
    ("WORLD 2", 2, (110, 108, 100)),
]
rb_y, rb_h = 158, 20
x = 14
tot = sum(c for _, c, _ in REGIONS)
for name, c, col in REGIONS:
    w = (W - 28) * c / tot
    d.rectangle([x, rb_y, x + w, rb_y + rb_h], fill=col)
    f = SANS_B(11)
    tw = d.textlength(name, font=f)
    if tw < w - 6:
        d.text((x + (w - tw) / 2, rb_y + 4), name, font=f, fill=(255, 255, 255))
    x += w

# ---- UTC strip ----
d.rectangle([14, 184, W - 14, 202], fill=NAVY)
d.text((20, 187), "THE DAY IN UTC", font=SANS_B(11), fill=(255, 214, 64))
utc = "04:05  Bessent demands answers    ·    09:00  Guterres urges AI rules    ·    12:00  Anthropic IPO debut    ·    16:17  Gaza strike    ·    23:24  Seoul readies fund"
d.text((150, 187), utc, font=SANS(11), fill=(255, 255, 255))

# ---- heroes ----
HEROES = [
    dict(x=14, kicker="MARKETS · SEOUL", chip="REPORTED",
         title="AI ROUT HITS ASIA",
         body="Kospi sheds 161 pts, intraday -5.8%, as the AI sell-off spreads from Wall Street. Samsung -3.1%, SK Hynix -2.5%.",
         src="Korea JoongAng Daily · CNBC · Morningstar", scene="chart",
         big="-3.3%", bigsub="KOSPI closes 4,708.54"),
    dict(x=350, kicker="UNITED NATIONS · BARBADOS", chip="REPORTED",
         title="GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
         body="UN chief urges global AI safety rules at the Bridgetown summit; 150 delegates back a risk framework.",
         src="UN News · UN Web TV", scene="un",
         big=None, bigsub=None),
    dict(x=686, kicker="ASIA POWER INDEX 2026", chip="REPORTED",
         title="US LEAD OVER CHINA AT RECORD LOW",
         body="US diplomatic influence -6 to 76.7. India 3rd at 40.5. Published Sun, reported Mon.",
         src="Lowy Institute", scene="bars",
         big="GAP 5.3", bigsub="narrowest since 2018"),
]
hy, hh, hw = 208, 196, 324
for h in HEROES:
    x = h["x"]
    d.rectangle([x, hy, x + hw, hy + hh], outline=(180, 170, 150), width=1, fill=(255, 255, 255))
    # scene strip
    sx, sy, sw, sh = x, hy, hw, 88
    if h["scene"] == "chart":
        d.rectangle([sx, sy, sx + sw, sy + sh], fill=(26, 35, 64))
        for gy in range(sy + 18, sy + sh, 16):
            d.line([sx + 8, gy, sx + sw - 8, gy], fill=(60, 70, 110), width=1)
        pts = [(sx + 14, sy + 16), (sx + 70, sy + 26), (sx + 120, sy + 22),
               (sx + 180, sy + 44), (sx + 240, sy + 52), (sx + 300, sy + 74)]
        d.line(pts, fill=(230, 60, 60), width=3)
        for px, py in pts:
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 255, 255))
        d.text((sx + 12, sy + sh - 20), "FRI -5.2%  ·  MON -3.3%", font=SANS(10), fill=(200, 200, 210))
    elif h["scene"] == "un":
        d.rectangle([sx, sy, sx + sw, sy + sh], fill=(43, 94, 167))
        # flags row
        cols = [(163, 30, 30), (255, 255, 255), (30, 125, 50), (255, 214, 64), (163, 30, 30)]
        for i, c in enumerate(cols):
            fx = sx + 16 + i * 62
            d.rectangle([fx, sy + 12, fx + 44, sy + 30], fill=c, outline=(255, 255, 255))
        # podium
        d.rectangle([sx + sw / 2 - 34, sy + 52, sx + sw / 2 + 34, sy + sh], fill=(20, 40, 80))
        d.ellipse([sx + sw / 2 - 10, sy + 34, sx + sw / 2 + 10, sy + 54], fill=(240, 230, 210))
        d.rectangle([sx + sw / 2 - 2, sy + 40, sx + sw / 2 + 2, sy + 54], fill=(240, 230, 210))
        d.text((sx + sw - 108, sy + sh - 18), "BRIDGETOWN SUMMIT", font=SANS_B(9), fill=(255, 255, 255))
    else:  # bars
        d.rectangle([sx, sy, sx + sw, sy + sh], fill=(24, 42, 84))
        d.text((sx + 12, sy + 10), "US 78.9", font=SANS_B(12), fill=(255, 255, 255))
        d.rectangle([sx + 76, sy + 10, sx + 76 + 190, sy + 26], fill=(255, 255, 255))
        d.text((sx + 12, sy + 36), "CHINA 73.6", font=SANS_B(12), fill=(255, 214, 64))
        d.rectangle([sx + 96, sy + 36, sx + 96 + 176, sy + 52], fill=(255, 214, 64))
        d.text((sx + 12, sy + 62), "GAP 5.3 — narrowest since 2018", font=SANS_B(11), fill=(255, 255, 255))
    # kicker + chip
    ky = hy + 94
    d.text((x + 8, ky), h["kicker"], font=SANS_B(10), fill=RED)
    chip(d, x + hw - 66, ky - 1, h["chip"], CHIP_FILL[h["chip"]])
    # title
    tf = SERIF_B(19)
    lines = fit(d, h["title"], tf, hw - 16, 2)
    ty = ky + 16
    for ln in lines:
        d.text((x + 8, ty), ln, font=tf, fill=INK)
        ty += 22
    # body (2 lines when the title took 2 lines, else 3)
    bf = SANS(11)
    blines = fit(d, h["body"], bf, hw - 16, 2 if len(lines) == 2 else 3)
    by = ty + 2
    for ln in blines:
        d.text((x + 8, by), ln, font=bf, fill=(60, 58, 52))
        by += 14
    # source
    d.text((x + 8, hy + hh - 16), h["src"], font=SANS(9), fill=GRAY)

# ---- small cards ----
CARDS = [
    ("NORTH AMERICA", "Bessent demands Nvidia answers",
     "Treasury chief wants to know of violations; China.", "Reuters", "REPORTED", (31, 93, 168)),
    ("NORTH AMERICA", "FBI probes hack of police database",
     "NCIC system used by police nationwide.", "AP", "REPORTED", (31, 93, 168)),
    ("NORTH AMERICA", "Trump: Iran strikes may resume in New Year",
     "President is inclined to resume strikes if no deal is reached.", "Bloomberg", "CLAIM", (31, 93, 168)),
    ("NORTH AMERICA", "US futures jump 3% holiday week",
     "Futures rise after Friday's rout; Nasdaq 100 near bear market.", "CNBC", "REPORTED", (31, 93, 168)),
    ("NORTH AMERICA", "Skubal $450M Mets deal",
     "Two-time Cy Young winner signs a record nine-year, $450M deal.", "ESPN", "REPORTED", (31, 93, 168)),
    ("NORTH AMERICA", "Tom Jackson dies at 75",
     "Broncos linebacker turned longtime ESPN analyst.", "ESPN", "REPORTED", (31, 93, 168)),
    ("NORTH AMERICA", "10 States sue SpaceX over AI safety claims",
     "Oregon and Virginia accuse SpaceX of lying about AI safety.", "Reuters", "REPORTED", (31, 93, 168)),
    ("NORTH AMERICA", "Anthropic IPO: $107.3B, largest ever",
     "Claude maker raised a record $107.3B; debut close $97.17.", "Bloomberg", "REPORTED", (31, 93, 168)),
    ("EUROPE", "Poland: 3 Russian missiles crossed airspace",
     "Kyiv says three Kh-101 cruise missiles entered Poland on Friday.", "AP", "REPORTED", (24, 42, 84)),
    ("EUROPE", "Intel claims Russian nuclear satellite",
     "Moscow built a satellite to carry a nuclear warhead, agencies say.", "AP", "CLAIM", (24, 42, 84)),
]
cw2, ch2 = 196, 112
for i, (kick, title, body, src, ch, col) in enumerate(CARDS):
    row, cc = divmod(i, 5)
    x = 14 + cc * (cw2 + 8)
    y = 412 + row * (ch2 + 8)
    d.rectangle([x, y, x + cw2, y + ch2], outline=(180, 170, 150), width=1, fill=(255, 255, 255))
    # illustration strip
    d.rectangle([x, y, x + cw2, y + 26], fill=col)
    # tiny white glyphs
    gx = x + cw2 - 34
    d.ellipse([gx, y + 7, gx + 12, y + 19], outline=(255, 255, 255), width=2)
    d.polygon([(gx + 20, y + 7), (gx + 30, y + 19), (gx + 10, y + 19)], outline=(255, 255, 255))
    d.text((x + 6, y + 7), kick, font=SANS_B(8), fill=(255, 255, 255))
    d.text((x + 6, y + 30), f"#{i + 4}", font=SANS_B(9), fill=RED)
    tf = SANS_B(12)
    lines = fit(d, title, tf, cw2 - 12, 2)
    ty = y + 44
    for ln in lines:
        d.text((x + 6, ty), ln, font=tf, fill=INK)
        ty += 14
    bf = SANS(10)
    blines = fit(d, body, bf, cw2 - 12, 2)
    by = ty + 1
    for ln in blines:
        d.text((x + 6, by), ln, font=bf, fill=(60, 58, 52))
        by += 12
    d.text((x + 6, y + ch2 - 14), src, font=SANS(8), fill=GRAY)
    chip(d, x + cw2 - 62, y + ch2 - 15, ch, CHIP_FILL[ch])

# ---- map + ALSO ----
my = 652
d.text((14, my), "THE WORLD — WHERE IT HAPPENED", font=SANS_B(12), fill=RED)
d.text((14, my + 14), "Red pin = reported  ·  Amber pin = claim", font=SANS(9), fill=GRAY)
d.text((524, my), "ALSO ON MONDAY — 18 MORE STORIES", font=SANS_B(12), fill=RED)

MAP = (14, 676, 504, 896)  # x0,y0,x1,y1
mx0, my0, mx1, my1 = MAP
d.rectangle(MAP, fill=(207, 227, 238), outline=(150, 160, 170), width=1)

def project(lon, lat):
    lat = max(-55, min(75, lat))
    x = mx0 + (lon + 180) / 360 * (mx1 - mx0)
    y = my0 + (75 - lat) / 130 * (my1 - my0)
    return x, y

# rough continent polygons (lon, lat)
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-75, 73), (-60, 62), (-55, 47),
     (-65, 44), (-75, 35), (-80, 26), (-90, 21), (-97, 16), (-105, 20), (-115, 30),
     (-125, 40), (-125, 49), (-140, 60), (-165, 60)],
    # South America
    [(-80, 10), (-75, 5), (-60, 0), (-50, -5), (-35, -8), (-40, -20), (-48, -28),
     (-58, -35), (-65, -45), (-70, -52), (-73, -40), (-72, -20), (-80, -5)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (10, 59), (18, 56),
     (21, 55), (24, 59), (30, 60), (30, 70), (40, 68), (45, 66), (40, 55), (35, 50),
     (30, 46), (28, 41), (23, 36), (19, 40), (12, 44), (3, 42)],
    # Africa
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28), (40, 15),
     (48, 11), (51, 2), (40, -10), (35, -20), (30, -29), (20, -35), (15, -27), (12, -18),
     (10, -5), (8, 4), (-8, 5)],
    # Asia
    [(40, 68), (60, 70), (80, 73), (100, 77), (120, 73), (140, 72), (160, 70),
     (178, 65), (170, 60), (158, 52), (142, 45), (135, 35), (127, 33), (122, 30),
     (115, 22), (108, 12), (105, 8), (100, 6), (95, 15), (90, 22), (85, 20),
     (80, 8), (75, 8), (70, 20), (60, 25), (55, 26), (50, 29), (48, 30), (43, 35),
     (40, 42), (35, 45), (30, 46), (40, 55)],
    # Australia
    [(113, -22), (114, -32), (120, -34), (129, -32), (135, -35), (140, -38),
     (147, -39), (150, -37), (153, -27), (150, -22), (146, -19), (142, -11),
     (136, -12), (132, -12), (126, -14), (122, -17), (117, -20)],
]
for poly in CONTINENTS:
    pts = [project(lon, lat) for lon, lat in poly]
    d.polygon(pts, fill=(232, 220, 195), outline=(170, 155, 125))

# graticule
for lon in range(-150, 181, 30):
    x, _ = project(lon, 0)
    d.line([x, my0, x, my1], fill=(190, 210, 225), width=1)
for lat in range(-40, 76, 20):
    _, y = project(0, lat)
    d.line([mx0, y, mx1, y], fill=(190, 210, 225), width=1)

PINS = [
    # (num, lon, lat, claim?, dx, dy)
    (1, 127.0, 37.5, False, 0, 0),
    (2, -59.6, 13.2, False, 0, 0),
    (3, -77.0, 38.9, True, -22, -14),
    (4, -77.0, 38.9, False, 18, 10),
    (5, -77.0, 38.9, False, -2, 16),
    (6, -77.0, 38.9, False, 22, -10),
    (7, -74.0, 40.7, False, -10, -16),
    (8, -74.0, 40.7, False, 16, 12),
    (9, -105.0, 39.7, False, 0, 0),
    (10, -122.7, 45.5, False, 0, 0),
    (11, -122.4, 37.8, False, 0, 0),
    (12, 21.0, 52.2, False, 0, 0),
    (13, 37.6, 55.7, True, 0, 0),
    (14, 2.35, 48.85, False, 0, 0),
    (15, -2.24, 53.48, False, 0, 0),
    (16, 30.5, 50.45, False, 0, 0),
    (17, 30.7, 36.9, False, 0, 0),
    (18, 20.1, 32.1, True, 0, 0),
    (19, 34.8, 32.1, False, -8, 6),
    (20, 34.5, 31.5, False, 8, 8),
    (21, 35.2, 32.0, False, 0, -10),
    (22, 51.4, 35.7, False, 0, 0),
    (23, 35.5, 33.9, False, 0, 0),
    (24, 50.6, 26.2, False, 0, 0),
    (25, 32.5, 15.6, True, 0, 0),
    (26, 15.3, -4.3, False, 0, 0),
    (27, 90.4, 23.8, False, 0, 0),
    (28, 127.0, 37.5, False, 10, 10),
    (29, 127.0, 37.5, False, -10, 10),
    (30, 116.4, 39.9, False, 0, 0),
    (31, 127.0, 37.5, False, 0, -12),
]
for num, lon, lat, claim, dx, dy in PINS:
    x, y = project(lon, lat)
    x += dx; y += dy
    col = AMBER if claim else RED
    d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=col, outline=(255, 255, 255), width=1)
    t = str(num)
    f = SANS_B(8)
    d.text((x - d.textlength(t, font=f) / 2, y - 5), t, font=f, fill=(255, 255, 255))
d.polygon([(mx0 + 6, my1 - 6), (mx0 + 12, my1 - 6), (mx0 + 9, my1 - 13)], fill=INK)
d.text((mx0 + 15, my1 - 14), "N", font=SANS_B(9), fill=INK)

# ALSO list (two columns of 9)
ALSO = [
    (14, "Paris: Sat+ 100+ back 2% billionaire tax"),
    (15, "Manchester: 12,000 cleared after scare"),
    (16, "Zelenskyy: 165 Russian missiles in a week"),
    (17, "COP31: the day after"),
    (18, "Benghazi: UN probe into port attacks"),
    (19, "Israel unity talks resume after Sunday stall"),
    (20, "Gaza: two killed in Israeli strike"),
    (21, "West Bank: settler attacks hit villages"),
    (22, "Iran war: no deal in sight"),
    (23, "Lebanon seizes 264 kg of explosives"),
    (24, "Bahrain: Iran strike hits plant, 2 hurt"),
    (25, "Sudan downs drones over Khartoum"),
    (26, "DRC: fighting traps Ebola teams"),
    (27, "Bangladesh: Hasina jailed if she returns"),
    (28, "Seoul: minister quits over AI exam chaos"),
    (29, "SK Telecom -7.3% as Anthropic hype cools"),
    (30, "China eases margin rules to calm rout"),
    (31, "Seoul readies 10T-won stabilisation fund"),
]
ax0, ax1 = 524, 1010
colw = (ax1 - ax0) / 2
for i, (num, text) in enumerate(ALSO):
    col, row = divmod(i, 9)
    x = ax0 + col * colw
    y = my + 22 + row * 24
    d.text((x, y), str(num), font=SANS_B(11), fill=RED)
    lines = fit(d, text, SANS(10.5), colw - 24, 1)
    d.text((x + 20, y + 1), lines[0] if lines else "", font=SANS(10.5), fill=INK)

# ---- DATE CHECK ----
dy0, dy1 = 904, 984
d.rectangle([14, dy0, W - 14, dy1], outline=RED, width=2, fill=(253, 240, 236))
d.text((22, dy0 + 6), "DATE CHECK", font=SANS_B(12), fill=RED)
d.text((22 + d.textlength("DATE CHECK  ", font=SANS_B(12)), dy0 + 7),
       "Every story above happened or was first reported on Monday 23 November 2026.",
       font=SANS_B(11), fill=INK)
d.text((W - 14 - d.textlength("WIRES READ UP TO 23:00 UTC", font=SANS_B(10)), dy0 + 7),
       "WIRES READ UP TO 23:00 UTC", font=SANS_B(10), fill=RED)
ex = "EXCLUDED (not 23 Nov):  Democrats reach 258 (22 Nov)  ·  Sparta II fire (22 Nov)  ·  El Chapo Isidro captured (22 Nov)  ·  EU-Indonesia pact (21 Nov)  ·  Nigeria boat (21 Nov)  ·  ICJ Myanmar ruling (19 Nov)"
for j, ln in enumerate(fit(d, ex, SANS(10.5), W - 44, 2)):
    d.text((22, dy0 + 26 + j * 13), ln, font=SANS(10.5), fill=INK)
ny = "NOT YET:  Dymer search continues (14 missing)  ·  4 House races uncalled  ·  COP32 venue not set  ·  WHO evacuating trapped Ebola staff"
for j, ln in enumerate(fit(d, ny, SANS(10.5), W - 44, 2)):
    d.text((22, dy0 + 54 + j * 13), ln, font=SANS(10.5), fill=INK)

# ---- footer ----
fy = 990
d.text((14, fy), "SOURCES: AP · Reuters · CNN · BBC · AFP · UN News · WHO · Lowy Institute · Korea JoongAng Daily · Bloomberg",
       font=SANS(9), fill=GRAY)
d.text((14, fy + 12), "REPORTED = confirmed by its source  ·  CLAIM = one side alleges  ·  DENIAL = disputed  ·  ONGOING = still developing",
       font=SANS(9), fill=GRAY)
d.text((W - 14 - d.textlength("Scenes are drawn illustrations, not photographs.", font=SANS_I(9)), fy + 12),
       "Scenes are drawn illustrations, not photographs.", font=SANS_I(9), fill=GRAY)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, optimize=True)
print("saved", out, os.path.getsize(out), "bytes")
