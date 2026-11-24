#!/usr/bin/env python3
"""news-23 b18 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026.
31 stories, 6 regions. Drawn with PIL; entry.png 1024x1024, < 1 MiB."""
import os, random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (26, 26, 26)
GREY = (90, 90, 86)
RED = (185, 28, 28)
GOLD = (176, 141, 30)
NAVY = (30, 58, 95)
TEAL = (15, 118, 110)
SLATE = (51, 65, 85)

SERIFB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()

def wrap(d, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text_lines(d, x, y, lines, fnt, fill, leading):
    for i, ln in enumerate(lines):
        d.text((x, y + i * leading), ln, font=fnt, fill=fill)
    return y + len(lines) * leading

def chip(d, x_right, y, label, fill):
    f = font(SANSB, 9)
    tw = d.textlength(label, font=f)
    w = int(tw) + 12
    x = x_right - w
    d.rounded_rectangle([x, y, x_right, y + 13], radius=6, fill=fill)
    d.text((x + 6, y + 2), label, font=f, fill=(255, 255, 255))
    return x

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 66], fill=(12, 12, 12))
    d.text((14, 10), "THE WORLD TODAY", font=font(SERIFB, 44), fill=(255, 255, 255))
    d.text((1010, 22), "MONDAY 23 NOVEMBER 2026", font=font(SANSB, 19),
           fill=(212, 175, 55), anchor="ra")

    # ---- kicker ----
    d.text((14, 70), "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  US lead over China at record low  \u00b7  Anthropic IPO $107.3B",
           font=font(SERIFB, 15), fill=RED)

    # ---- number strip ----
    nums = [("\u22123.3%", "KOSPI CLOSES 4,708.54", RED),
            ("5.3", "US\u2013CHINA POWER GAP", NAVY),
            ("11,762", "EBOLA CASES, DRC", (146, 64, 14)),
            ("$450M", "SKUBAL DEAL", (21, 101, 52)),
            ("$107.3B", "ANTHROPIC IPO", (126, 34, 206))]
    cw = 1008 // 5
    for i, (big, small, col) in enumerate(nums):
        x = 8 + i * cw
        if i:
            d.line([x - 3, 94, x - 3, 138], fill=(200, 192, 175), width=1)
        d.text((x + 4, 90), big, font=font(SANSB, 30), fill=col)
        d.text((x + 4, 126), small, font=font(SANSB, 10), fill=INK)
    d.line([8, 146, 1016, 146], fill=(200, 192, 175), width=1)

    # ---- region bar (counts sum to 31; widths sum to 1008) ----
    regs = [("ASIA-PACIFIC 7", 226, (47, 125, 50)), ("AMERICAS 8", 258, (29, 78, 216)),
            ("MIDDLE EAST 6", 194, (180, 83, 9)), ("EUROPE 5", 161, TEAL),
            ("AFRICA 3", 96, (124, 58, 237)), ("WORLD 2", 73, SLATE)]
    x = 8
    for label, w, col in regs:
        d.rectangle([x, 148, x + w - 2, 168], fill=col)
        f = font(SANSB, 11)
        tw = d.textlength(label, font=f)
        d.text((x + (w - 2 - tw) / 2, 153), label, font=f, fill=(255, 255, 255))
        x += w

    # ---- the day in numbers ----
    d.rectangle([8, 170, 1016, 188], fill=(30, 41, 59))
    d.text((14, 174), "THE DAY IN NUMBERS", font=font(SANSB, 11), fill=(212, 175, 55))
    d.text((1010, 174), "\u22125.8% INTRADAY LOW  \u00b7  165 MISSILES IN A WEEK  \u00b7  12,000 CLEARED  \u00b7  264 KG SEIZED  \u00b7  2% TAX BACKED",
           font=font(SANS, 11), fill=(255, 255, 255), anchor="ra")

    # ---- hero scenes ----
    hx = [8, 348, 688]
    hw = 328
    draw_hero_kospi(d, hx[0], 192, hw)
    draw_hero_guterres(d, hx[1], 192, hw)
    draw_hero_bars(d, hx[2], 192, hw)

    heroes = [
        ("1", "AI ROUT HITS ASIA",
         "Kospi \u22123.3% to 4,708.54, sheds 161 pts; intraday \u22125.8%. Samsung \u22123.1%, SK Hynix \u22122.5%.",
         "KOREA EXCHANGE", "REPORTED"),
        ("2", "GUTERRES: REGULATE AI BEFORE IT\u2019S TOO LATE",
         "UN chief urges global AI safety rules at the Bridgetown summit; 150 delegates back a risk framework.",
         "UNITED NATIONS", "REPORTED"),
        ("3", "US LEAD OVER CHINA AT RECORD LOW",
         "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India third at 40.5.",
         "LOWY INSTITUTE", "REPORTED"),
    ]
    for i, (num, head, body, src, ch) in enumerate(heroes):
        x = hx[i]
        d.ellipse([x, 344, x + 22, 366], fill=RED)
        fnum = font(SANSB, 13)
        tw = d.textlength(num, font=fnum)
        d.text((x + (22 - tw) / 2, 346), num, font=fnum, fill=(255, 255, 255))
        hl = wrap(d, head, font(SERIFB, 20), hw - 30)
        text_lines(d, x + 28, 342, hl[:2], font(SERIFB, 20), INK, 22)
        bl = wrap(d, body, font(SANS, 12), hw)
        text_lines(d, x, 392, bl[:3], font(SANS, 12), INK, 15)
        d.text((x, 440), src, font=font(SANS, 9), fill=GREY)
        chip(d, x + hw, 438, ch, NAVY)

    # ---- more of the day header ----
    d.text((8, 458), "MORE OF THE DAY \u2014 10 STORIES", font=font(SANSB, 15), fill=INK)
    d.line([8, 476, 1016, 476], fill=INK, width=2)

    draw_cards(d)
    draw_map_also(d)
    draw_datecheck(d)
    draw_footer(d)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")

def draw_hero_kospi(d, x, y, w):
    d.rectangle([x, y, x + w, y + 150], fill=(11, 30, 58))
    rnd = random.Random(23)
    for _ in range(36):
        sx = x + rnd.randint(4, w - 4)
        sy = y + rnd.randint(4, 52)
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
    d.text((x + 12, y + 8), "\u22123.3%", font=font(SANSB, 32), fill=(239, 68, 68))
    # skyline
    bx = x + 6
    while bx < x + w - 20:
        bw = rnd.randint(16, 30)
        bh = rnd.randint(28, 62)
        d.rectangle([bx, y + 150 - 24 - bh, bx + bw, y + 150 - 24], fill=(5, 15, 35))
        for wy in range(y + 150 - 20 - bh, y + 150 - 26, 9):
            for wx in range(bx + 4, bx + bw - 3, 8):
                if rnd.random() < 0.55:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(250, 204, 21))
        bx += bw + 3
    # falling chart line
    pts = [(x + 16, y + 56), (x + 60, y + 62), (x + 104, y + 52), (x + 148, y + 66),
           (x + 192, y + 60), (x + 236, y + 82), (x + 280, y + 92), (x + 312, y + 108)]
    d.line(pts, fill=(239, 68, 68), width=3)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(250, 204, 21))
    d.rectangle([x, y + 126, x + w, y + 150], fill=(0, 0, 0))
    d.text((x + 10, y + 131), "KOSPI 4,708.54  \u00b7  \u2212161 PTS", font=font(SANSB, 13), fill=(255, 255, 255))

def draw_hero_guterres(d, x, y, w):
    d.rectangle([x, y, x + w, y + 150], fill=(14, 116, 144))
    d.text((x + 12, y + 8), "150 DELEGATES", font=font(SANSB, 26), fill=(250, 204, 21))
    d.text((x + 12, y + 38), "BACK A RISK FRAMEWORK", font=font(SANSB, 15), fill=(255, 255, 255))
    # flags on poles
    for fx, col in [(x + 34, (220, 38, 38)), (x + 94, (37, 99, 235)), (x + 154, (250, 204, 21))]:
        d.line([fx, y + 66, fx, y + 126], fill=(255, 255, 255), width=2)
        d.polygon([(fx, y + 66), (fx + 34, y + 74), (fx, y + 82)], fill=col)
    # podium
    d.polygon([(x + 12, y + 150), (x + 168, y + 150), (x + 152, y + 112), (x + 28, y + 112)], fill=(120, 72, 20))
    # globe
    cx, cy, r = x + 258, y + 92, 42
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(165, 220, 235), outline=(255, 255, 255), width=2)
    d.ellipse([cx - 18, cy - r + 2, cx + 18, cy + r - 2], outline=(255, 255, 255), width=1)
    d.line([cx - r + 2, cy, cx + r - 2, cy], fill=(255, 255, 255), width=1)
    d.line([cx, cy - r + 2, cx, cy + r - 2], fill=(255, 255, 255), width=1)
    for gx, gy in [(cx - 14, cy - 12), (cx + 12, cy + 4), (cx - 2, cy + 18)]:
        d.ellipse([gx - 5, gy - 5, gx + 5, gy + 5], fill=(34, 139, 34))
    d.rectangle([x, y + 126, x + w, y + 150], fill=(0, 0, 0))
    d.text((x + 10, y + 131), "UN  \u00b7  BRIDGETOWN", font=font(SANSB, 13), fill=(255, 255, 255))

def draw_hero_bars(d, x, y, w):
    d.rectangle([x, y, x + w, y + 150], fill=(255, 255, 255), outline=INK, width=1)
    d.text((x + 10, y + 8), "NARROWEST SINCE 2018", font=font(SANSB, 12), fill=INK)
    d.text((x + w - 10, y + 8), "GAP 5.3", font=font(SANSB, 14), fill=GOLD, anchor="ra")
    base = y + 130
    vals = [("78.9", 100, NAVY), ("73.6", 94, RED), ("40.5", 52, (146, 110, 8))]
    labels = ["US", "CHINA", "INDIA"]
    bw = 62
    start = x + (w - (3 * bw + 2 * 30)) // 2
    for i, (val, hgt, col) in enumerate(vals):
        bx = start + i * (bw + 30)
        d.rectangle([bx, base - hgt, bx + bw, base], fill=col)
        f = font(SANSB, 15)
        tw = d.textlength(val, font=f)
        d.text((bx + (bw - tw) / 2, base - hgt + 8), val, font=f, fill=(255, 255, 255))
        fl = font(SANSB, 12)
        tw = d.textlength(labels[i], font=fl)
        d.text((bx + (bw - tw) / 2, base + 4), labels[i], font=fl, fill=INK)

CARDS = [
    (4, "AMERICAS", (109, 40, 217), "BESSENT: NVIDIA ANSWERS",
     "Treasury chief seeks answers on China sales violations.", "Reuters", "REPORTED"),
    (5, "FBI", (76, 29, 149), "FBI PROBES NCIC HACK",
     "Hackers hit the NCIC system used by police nationwide.", "AP", "REPORTED"),
    (6, "WHITE HOUSE", (146, 64, 14), "TRUMP: IRAN STRIKES MAY RESUME",
     "President says strikes could resume in the New Year.", "Reuters", "REPORTED"),
    (7, "MARKETS", (101, 163, 13), "US FUTURES JUMP 3%",
     "Holiday-week rally lifts Nasdaq futures as the AI rout cools.", "Bloomberg", "REPORTED"),
    (8, "SPORT", (21, 128, 61), "SKUBAL\u2019S $450M METS DEAL",
     "Cy Young winner signs nine years, a record for a pitcher.", "AP", "REPORTED"),
    (9, "SPORT", (21, 128, 61), "TOM JACKSON DIES AT 75",
     "Broncos linebacker turned ESPN voice dies.", "ESPN", "REPORTED"),
    (10, "LEGAL", (126, 34, 206), "STATES SUE SPACEX",
     "Ten states challenge AI safety claims.", "AP", "REPORTED"),
    (11, "TECH", (29, 78, 216), "ANTHROPIC IPO: $107.3B",
     "Claude maker raises at $83 a share; debut closes $97.17.", "WSJ", "REPORTED"),
    (12, "EUROPE", TEAL, "POLAND: 3 RUSSIAN MISSILES CROSSED AIRSPACE",
     "Kyiv says three Kh-101s crossed Polish airspace Friday.", "AP", "CLAIM"),
    (13, "SPACE", SLATE, "RUSSIAN NUCLEAR SATELLITE",
     "Intel claims Moscow built a satellite with a nuclear warhead.", "Reuters", "CLAIM"),
]

def draw_cards(d):
    xs = [8, 210, 412, 614, 816]
    ys = [482, 570]
    for idx, (num, tag, col, title, body, src, ch) in enumerate(CARDS):
        x = xs[idx % 5]
        y = ys[idx // 5]
        d.rectangle([x, y, x + 196, y + 84], fill=(255, 255, 255), outline=(200, 192, 175))
        d.rectangle([x, y, x + 196, y + 15], fill=col)
        d.text((x + 5, y + 2), tag, font=font(SANSB, 10), fill=(255, 255, 255))
        d.text((x + 191, y + 2), str(num), font=font(SANSB, 10), fill=(255, 255, 255), anchor="ra")
        tl = wrap(d, title, font(SANSB, 11), 186)
        text_lines(d, x + 5, y + 19, tl[:2], font(SANSB, 11), INK, 13)
        bl = wrap(d, body, font(SANS, 10), 186)
        text_lines(d, x + 5, y + 48, bl[:2], font(SANS, 10), INK, 12)
        d.text((x + 5, y + 71), src, font=font(SANS, 9), fill=GREY)
        chip(d, x + 191, y + 70, ch, NAVY if ch == "REPORTED" else RED)

def draw_map_also(d):
    # ---- map ----
    mx0, my0, mx1, my1 = 8, 676, 500, 846
    d.rectangle([mx0, my0, mx1, my1], fill=(214, 231, 240))
    for gx in range(mx0, mx1 + 1, 24):
        d.line([gx, my0, gx, my1], fill=(255, 255, 255), width=1)
    for gy in range(my0, my1 + 1, 24):
        d.line([mx0, gy, mx1, gy], fill=(255, 255, 255), width=1)
    continents = [
        [(48, 700), (95, 686), (150, 688), (185, 700), (178, 730), (140, 748), (105, 762), (68, 748), (40, 722)],
        [(200, 688), (222, 684), (228, 696), (205, 700)],
        [(128, 772), (152, 766), (168, 782), (155, 818), (130, 812)],
        [(258, 690), (288, 682), (306, 692), (300, 712), (272, 716), (252, 704)],
        [(258, 722), (300, 716), (316, 742), (298, 786), (266, 772), (252, 742)],
        [(312, 688), (420, 678), (478, 690), (468, 726), (400, 742), (342, 728), (316, 706)],
        [(418, 800), (458, 794), (468, 812), (428, 820)],
    ]
    for poly in continents:
        d.polygon(poly, fill=(143, 174, 107), outline=(90, 120, 70))
    d.text((mx0, 654), "WHERE IT HAPPENED", font=font(SANSB, 15), fill=INK)
    pins = [(1, 438, 706), (2, 172, 742), (3, 408, 690), (4, 128, 716), (5, 146, 706),
            (6, 332, 716), (7, 102, 706), (8, 66, 716), (9, 88, 726), (10, 110, 734),
            (11, 284, 692), (12, 304, 706), (13, 326, 686)]
    for num, px, py in pins:
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
        f = font(SANSB, 9)
        tw = d.textlength(str(num), font=f)
        d.text((px - tw / 2, py - 6), str(num), font=f, fill=(255, 255, 255))
    d.text((8, 850), "Pins 1\u201313: 1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing \u00b7 4 Washington \u00b7 5 New York \u00b7 6 Tehran \u00b7 7 Chicago",
           font=font(SANS, 9), fill=GREY)
    d.text((8, 861), "8 San Francisco \u00b7 9 Denver \u00b7 10 Austin \u00b7 11 Warsaw \u00b7 12 Kyiv \u00b7 13 Moscow",
           font=font(SANS, 9), fill=GREY)
    # ---- ALSO ----
    d.text((508, 654), "ALSO ON MONDAY", font=font(SANSB, 15), fill=INK)
    also = ["Paris: 100+ back 2% billionaire tax", "Manchester: 12,000 cleared",
            "Zelenskyy: 165 missiles in a week", "COP31: the day after pact rejected",
            "Benghazi: UN demands port probe", "Israel unity talks resume",
            "Gaza: two killed in Israeli strike", "West Bank settler attacks",
            "Iran war: no deal in sight", "Lebanon seizes 264 kg explosives",
            "Bahrain: strike hits plant, 2 hurt", "Sudan: defences down drones",
            "DRC: fighting traps Ebola teams", "Bangladesh: Hasina jailed if she returns",
            "Seoul minister quits over exam chaos", "SK Telecom \u22127.3% as hype cools",
            "China eases margin rules", "Seoul readies 10T-won fund"]
    for col_i, col_x in enumerate([508, 766]):
        y = 678
        for j in range(9):
            n = 14 + col_i * 9 + j
            item = also[col_i * 9 + j]
            d.text((col_x, y), f"{n}.", font=font(SANSB, 11), fill=RED)
            il = wrap(d, item, font(SANS, 11), 212)
            text_lines(d, col_x + 26, y, il[:2], font(SANS, 11), INK, 13)
            y += 13 * len(il[:2]) + 7

def draw_datecheck(d):
    d.rectangle([8, 876, 1016, 956], fill=(255, 245, 245), outline=RED, width=2)
    d.text((16, 882), "DATE CHECK", font=font(SANSB, 13), fill=RED)
    d.text((130, 884), "READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY",
           font=font(SANSB, 11), fill=INK)
    left = ("LEFT OUT \u2014 NOT 23 NOV: Democrats reach 258 seats (22 Nov) \u00b7 Sparta II fire (22 Nov) \u00b7 "
            "El Chapo Isidro captured (22 Nov) \u00b7 EU\u2013Indonesia pact (21 Nov) \u00b7 Nigeria boat (21 Nov) \u00b7 "
            "ICJ Myanmar ruling (19 Nov)")
    ll = wrap(d, left, font(SANS, 11), 992)
    text_lines(d, 16, 904, ll, font(SANS, 11), INK, 14)
    d.text((16, 934), "NOT YET: Dymer search continues (14 missing) \u00b7 4 House races uncalled \u00b7 COP32 venue not set \u00b7 WHO evacuating trapped Ebola staff",
           font=font(SANS, 11), fill=INK)

def draw_footer(d):
    d.text((8, 962), "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 NYT \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).",
           font=font(SANS, 10), fill=GREY)
    d.text((8, 974), "CHIPS: REPORTED = confirmed by wires \u00b7 CLAIM = one side\u2019s claim, not independently confirmed \u00b7 ONGOING = still developing",
           font=font(SANS, 10), fill=GREY)
    d.text((8, 986), "Scenes are drawn illustrations, not photographs. \u00b7 THE WORLD TODAY \u2014 Monday 23 November 2026 \u00b7 31 stories \u00b7 6 regions",
           font=font(SANSB, 10), fill=INK)
    d.rectangle([0, 1000, W, H], fill=(12, 12, 12))
    f = font(SANSB, 12)
    msg = "THE WORLD TODAY \u2014 MONDAY 23 NOVEMBER 2026 \u00b7 31 STORIES"
    tw = d.textlength(msg, font=f)
    d.text(((W - tw) / 2, 1006), msg, font=f, fill=(212, 175, 55))


if __name__ == "__main__":
    main()
