"""news-23 b132 front-page-dense: render entry.png (1024x1024) with PIL.

THE WORLD TODAY — Monday 23 November 2026. 31 stories: 3 hero scenes,
10 cards, 18 ALSO items, world map with 13 numbered pins, DATE CHECK box.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 242, 231)
INK = (20, 20, 20)
GOLD = (154, 123, 0)
RED = (139, 26, 26)
NAVY = (31, 56, 100)
GREEN = (30, 122, 52)
GRAY = (90, 90, 90)
BLOB = (201, 221, 176)
PIN = (178, 34, 34)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if fnt.getlength(t) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text(d, xy, s, fnt, fill=INK, anchor="la"):
    d.text(xy, s, font=fnt, fill=fill, anchor=anchor)


def chip(d, x, y, label, bg=NAVY):
    f = font(SANS_B, 9)
    w = f.getlength(label) + 10
    d.rounded_rectangle([x, y, x + w, y + 13], radius=2, fill=bg)
    d.text((x + w / 2, y + 6.5), label, font=f, fill=(255, 255, 255),
           anchor="mm")
    return w


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    text(d, (16, 4), "THE WORLD TODAY", font(SERIF_B, 46))
    text(d, (1008, 20), "MONDAY 23 NOVEMBER 2026", font(SANS_B, 19),
         fill=GOLD, anchor="ra")
    d.rectangle([16, 58, 1008, 60], fill=GOLD)

    # ---------- kicker ----------
    d.rectangle([0, 64, 1024, 84], fill=RED)
    text(d, (16, 68),
         "AI rout hits Asia   \u00b7   UN chief urges AI rules   \u00b7   "
         "US lead over China at record low   \u00b7   Anthropic IPO $107.3B",
         font(SANS_B, 14), fill=(255, 255, 255))

    # ---------- number strip (2 rows x 5) ----------
    nums = [
        ("-3.3%", "KOSPI"),
        ("5.3", "US-CHINA POWER GAP"),
        ("11,762", "EBOLA CASES, DRC"),
        ("10T won", "SEOUL STABILISATION FUND"),
        ("2%", "BILLIONAIRE TAX IN PARIS"),
        ("$450M", "SKUBAL DEAL"),
        ("165", "RUSSIAN MISSILES/WEEK"),
        ("12,000", "CLEARED IN MANCHESTER"),
        ("264 kg", "EXPLOSIVES SEIZED"),
        ("$107.3B", "ANTHROPIC IPO"),
    ]
    col_w = 992 / 5
    for i, (v, lab) in enumerate(nums):
        cx = 16 + (i % 5) * col_w
        cy = 88 if i < 5 else 120
        text(d, (cx, cy), v, font(SANS_B, 22))
        text(d, (cx, cy + 24), lab, font(SANS, 9), fill=GRAY)

    # ---------- region bar ----------
    regions = [
        ("ASIA-PACIFIC 7", NAVY, 0.23),
        ("AMERICAS 8", (178, 34, 34), 0.25),
        ("MIDDLE EAST 6", (106, 61, 154), 0.19),
        ("EUROPE 5", (46, 125, 107), 0.16),
        ("AFRICA 3", (198, 122, 26), 0.10),
        ("WORLD 2", (85, 85, 85), 0.07),
    ]
    x = 16
    for label, col, frac in regions:
        w = 992 * frac
        d.rectangle([x, 156, x + w - 2, 174], fill=col)
        f = font(SANS_B, 11)
        tw = f.getlength(label)
        d.text((x + (w - 2) / 2, 165), label, font=f,
               fill=(255, 255, 255), anchor="mm")
        x += w

    # ---------- UTC strip ----------
    text(d, (16, 179), "THE DAY IN UTC", font(SANS_B, 10), fill=GRAY)
    text(d, (130, 179),
         "~00:00 Kospi dives    ~05:30 Guterres opens    ~09:00 Power Index"
         "    ~12:00 Paris 2% tax    ~15:00 Kyiv missiles",
         font(SANS, 10), fill=GRAY)
    text(d, (1008, 179), "~ APPROX", font(SANS, 10), fill=GRAY, anchor="ra")

    # ---------- hero scenes ----------
    heroes = [
        dict(x=16, kind="kospi",
             head="AI ROUT HITS ASIA",
             body="Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday "
                  "-5.8%. Samsung -3.1%, SK Hynix -2.5%.",
             src="KOREA EXCHANGE"),
        dict(x=348, kind="guterres",
             head="GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
             body="UN chief urges global AI safety rules at the Bridgetown "
                  "summit; 150 back a risk framework.",
             src="UNITED NATIONS"),
        dict(x=680, kind="power",
             head="US LEAD OVER CHINA AT RECORD LOW",
             body="Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, "
                  "narrowest since 2018. India third at 40.5.",
             src="LOWY INSTITUTE"),
    ]
    for h in heroes:
        x0, y0 = h["x"], 194
        w = 328
        # scene box 190..296
        if h["kind"] == "kospi":
            d.rectangle([x0, y0, x0 + w, y0 + 106], fill=(18, 40, 75))
            # buildings with lit windows
            import random
            rnd = random.Random(7)
            bx = x0 + 8
            while bx < x0 + w - 30:
                bw = rnd.randint(18, 34)
                bh = rnd.randint(28, 62)
                d.rectangle([bx, y0 + 106 - bh, bx + bw, y0 + 106],
                            fill=(24, 52, 96))
                for wy in range(y0 + 106 - bh + 5, y0 + 100, 9):
                    for wx in range(bx + 4, bx + bw - 3, 8):
                        if rnd.random() < 0.55:
                            d.rectangle([wx, wy, wx + 4, wy + 5],
                                        fill=(255, 214, 90))
                bx += bw + 4
            # descending chart line, starting below the big "-3.3%"
            pts = [(x0 + 20 + i * 30, y0 + 32 + i * 5.5 + (i % 2) * 3)
                   for i in range(10)]
            d.line(pts, fill=(255, 140, 40), width=3)
            for px, py in pts:
                d.ellipse([px - 3, py - 3, px + 3, py + 3],
                          fill=(255, 255, 255))
            text(d, (x0 + 10, y0 + 6), "-3.3%", font(SANS_B, 26),
                 fill=(255, 255, 255))
            d.rectangle([x0, y0 + 88, x0 + w, y0 + 106], fill=(10, 26, 52))
            text(d, (x0 + 10, y0 + 92), "KOSPI 4,708.54  \u00b7  -161 PTS",
                 font(SANS_B, 11), fill=(255, 255, 255))
        elif h["kind"] == "guterres":
            d.rectangle([x0, y0, x0 + w, y0 + 106], fill=GREEN)
            text(d, (x0 + 12, y0 + 4), "150", font(SANS_B, 46),
                 fill=(255, 214, 90))
            text(d, (x0 + 12, y0 + 52), "DELEGATES", font(SANS_B, 17),
                 fill=(255, 214, 90))
            text(d, (x0 + 12, y0 + 71), "BACK A RISK", font(SANS_B, 17),
                 fill=(255, 214, 90))
            text(d, (x0 + 12, y0 + 88), "FRAMEWORK", font(SANS_B, 12),
                 fill=(255, 255, 255))
            # globe, right side
            cx, cy, r = x0 + 262, y0 + 53, 42
            d.ellipse([cx - r, cy - r, cx + r, cy + r],
                      fill=(220, 240, 210), outline=(255, 255, 255), width=2)
            d.ellipse([cx - 18, cy - r, cx + 18, cy + r],
                      outline=(120, 170, 120), width=1)
            d.line([cx - r, cy, cx + r, cy], fill=(120, 170, 120), width=1)
            d.arc([cx - r, cy - 20, cx + r, cy + 20], 0, 360,
                  fill=(120, 170, 120), width=1)
        else:  # power bars
            d.rectangle([x0, y0, x0 + w, y0 + 106], fill=(255, 255, 255),
                        outline=(200, 200, 200))
            text(d, (x0 + 10, y0 + 6), "NARROWEST SINCE 2018",
                 font(SANS_B, 13))
            text(d, (x0 + w - 10, y0 + 6), "GAP 5.3", font(SANS_B, 13),
                 fill=RED, anchor="ra")
            bars = [("78.9", "US", NAVY, 250),
                    ("73.6", "CHINA", (178, 34, 34), 232),
                    ("40.5", "INDIA", (198, 150, 20), 128)]
            by = y0 + 32
            for val, name, col, blen in bars:
                text(d, (x0 + 10, by), val, font(SANS_B, 13))
                d.rectangle([x0 + 62, by + 2, x0 + 62 + blen, by + 14],
                            fill=col)
                d.text((x0 + 68, by + 8), name, font=font(SANS_B, 10),
                       fill=(255, 255, 255), anchor="lm")
                by += 22
        # headline (2 lines max), body, source + chip — clear of the strip
        hf = font(SANS_B, 16)
        lines = wrap(h["head"], hf, w)[:2]
        ly = 306
        for ln in lines:
            text(d, (x0, ly), ln, hf)
            ly += 19
        bf = font(SANS, 10)
        blines = wrap(h["body"], bf, w)[:2]
        by = 344
        for ln in blines:
            text(d, (x0, by), ln, bf)
            by += 12
        text(d, (x0, 370), h["src"], font(SANS, 9), fill=GRAY)
        chip(d, x0 + w - 62, 368, "REPORTED")

    # ---------- MORE OF THE DAY strip ----------
    d.rectangle([0, 388, 1024, 406], fill=INK)
    text(d, (16, 392), "MORE OF THE DAY  \u2014  10 STORIES",
         font(SANS_B, 13), fill=(255, 255, 255))

    # ---------- cards (2 rows x 5) ----------
    cards = [
        ("AMERICAS", "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.",
         "WSJ", "REPORTED", NAVY),
        ("AMERICAS", "FBI PROBES NCIC HACK", "NCIC database hacked.",
         "AP", "REPORTED", NAVY),
        ("WHITE HOUSE", "TRUMP: IRAN STRIKES MAY RESUME",
         "May resume in New Year.", "Reuters", "REPORTED", NAVY),
        ("MARKETS", "US FUTURES JUMP 3%", "Holiday rally lifts 3%.",
         "Bloomberg", "REPORTED", NAVY),
        ("SPORT", "SKUBAL'S $450M METS DEAL", "Nine-year, largest ever.",
         "AP", "REPORTED", NAVY),
        ("SPORT", "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice.",
         "ESPN", "REPORTED", NAVY),
        ("LEGAL", "STATES SUE SPACEX", "Ten states sue over AI.",
         "AP", "REPORTED", NAVY),
        ("TECH", "ANTHROPIC IPO: $107.3B", "Raised $83; closes $97.17.",
         "WSJ", "REPORTED", NAVY),
        ("EUROPE", "POLAND: 3 MISSILES CROSSED AIRSPACE",
         "Kyiv: 3 Kh-101s crossed.", "AP", "CLAIM", RED),
        ("SPACE", "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.",
         "Reuters", "CLAIM", RED),
    ]
    cw, ch = 192, 70
    for i, (reg, head, body, src, tag, tagbg) in enumerate(cards):
        cx = 16 + (i % 5) * 200
        cy = 412 + (i // 5) * 76
        text(d, (cx, cy), reg, font(SANS_B, 9), fill=RED)
        text(d, (cx + cw - 2, cy), str(i + 1), font(SANS_B, 11),
             fill=RED, anchor="ra")
        hf = font(SANS_B, 12)
        lines = wrap(head, hf, cw)[:2]
        ly = cy + 13
        for ln in lines:
            text(d, (cx, ly), ln, hf)
            ly += 14
        text(d, (cx, cy + 42), body, font(SANS, 9), fill=GRAY)
        text(d, (cx, cy + 56), src, font(SANS, 8), fill=GRAY)
        chip(d, cx + cw - 62, cy + 55, tag, tagbg)

    # ---------- WHERE IT HAPPENED strip ----------
    d.rectangle([0, 564, 1024, 582], fill=INK)
    text(d, (16, 568), "WHERE IT HAPPENED", font(SANS_B, 13),
         fill=(255, 255, 255))

    # ---------- map blobs ----------
    def blob(points):
        d.polygon(points, fill=BLOB)
    # North America
    blob([(40, 610), (130, 592), (190, 612), (178, 648), (120, 668),
          (58, 656), (34, 628)])
    # South America
    blob([(118, 672), (168, 676), (178, 724), (152, 772), (126, 742),
          (114, 704)])
    # Europe
    blob([(248, 600), (310, 588), (342, 612), (322, 646), (272, 650),
          (244, 622)])
    # Africa
    blob([(258, 664), (320, 658), (346, 702), (322, 762), (286, 768),
          (258, 722)])
    # Asia
    blob([(352, 592), (472, 586), (492, 628), (462, 672), (400, 668),
          (354, 634)])
    pins = [
        (1, 455, 612), (2, 150, 640), (3, 440, 596), (4, 95, 612),
        (5, 130, 600), (6, 318, 598), (7, 282, 618), (8, 258, 600),
        (9, 322, 618), (10, 292, 600), (11, 345, 650), (12, 340, 672),
        (13, 305, 725),
    ]
    pf = font(SANS_B, 10)
    for n, px, py in pins:
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=PIN,
                  outline=(255, 255, 255), width=1)
        d.text((px, py), str(n), font=pf, fill=(255, 255, 255),
               anchor="mm")
    # legend under map
    lf = font(SANS, 9)
    text(d, (16, 786), "Pins 1\u201313:  1 Seoul \u00b7 2 Bridgetown \u00b7 "
         "3 Beijing \u00b7 4 Washington \u00b7 5 New York \u00b7 6 Kyiv \u00b7 "
         "7 Paris", lf)
    text(d, (16, 798), "8 London \u00b7 9 Warsaw \u00b7 10 Manchester \u00b7 "
         "11 Beirut", lf)
    text(d, (16, 810), "12 Gaza \u00b7 13 Khartoum", lf)

    # ---------- ALSO ----------
    text(d, (516, 584), "ALSO ON MONDAY", font(SANS_B, 13))
    also = [
        "14. Paris: 100+ back 2% billionaire tax",
        "15. Manchester: 12,000 cleared",
        "16. Zelenskyy: 165 missiles in a week",
        "17. COP31: the day after Antalya pact rejected",
        "18. Israel unity talks resume",
        "19. Gaza: two killed in Israeli strike",
        "20. West Bank settler attacks",
        "21. Iran war: no deal in sight",
        "22. Lebanon seizes 264 kg explosives",
        "23. Bahrain: strike hits plant, 2 hurt",
        "24. Benghazi: UN demands probe [CLAIM]",
        "25. Sudan: defences down drones [CLAIM]",
        "26. DRC: fighting traps Ebola teams",
        "27. Bangladesh: Hasina jailed if she returns",
        "28. Seoul minister quits in exam row",
        "29. SK Telecom -7.3% as hype cools",
        "30. China eases margin rules",
        "31. Seoul readies 10T-won fund",
    ]
    af = font(SANS, 10)
    for i, item in enumerate(also):
        col = 0 if i < 9 else 1
        ax = 516 if col == 0 else 762
        ay = 604 + (i % 9) * 22
        if "[CLAIM]" in item:
            base, _ = item.rsplit(" [CLAIM]", 1)
            text(d, (ax, ay), base, af)
            bw = af.getlength(base + " ")
            text(d, (ax + bw, ay), "[CLAIM]", font(SANS_B, 10), fill=RED)
        else:
            text(d, (ax, ay), item, af)

    # ---------- DATE CHECK ----------
    d.rectangle([16, 830, 1008, 912], outline=RED, width=2)
    text(d, (26, 838),
         "DATE CHECK  \u2014  READ 23 NOV 2026, 23:59 UTC  \u00b7  "
         "STORIES DATED 23 NOV ONLY", font(SANS_B, 12), fill=RED)
    text(d, (26, 860),
         "LEFT OUT \u2014 NOT 23 NOV:  Dems reach 258 (22 Nov)  \u00b7  "
         "Sparta II fire (22 Nov)  \u00b7  El Chapo Isidro captured (22 Nov)",
         font(SANS, 10))
    text(d, (26, 876),
         "EU\u2013Indonesia pact (21 Nov)  \u00b7  Nigeria boat (21 Nov)  "
         "\u00b7  ICJ Myanmar ruling (19 Nov)", font(SANS, 10))
    text(d, (26, 894),
         "NOT YET \u2014 Dymer search continues (14 missing)  \u00b7  "
         "4 House races uncalled  \u00b7  COP32 venue not set  \u00b7  "
         "WHO evacuating trapped Ebola staff", font(SANS, 10))

    # ---------- footer ----------
    text(d, (16, 920),
         "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap "
         "\u00b7 BBC \u00b7 WSJ \u00b7 ESPN \u00b7 Lowy Institute "
         "(Asia Power Index 2026).", font(SANS, 9), fill=GRAY)
    text(d, (16, 934),
         "CHIPS: REPORTED = confirmed by wires \u00b7 CLAIM = one side's "
         "claim, independently unconfirmed \u00b7 ONGOING = still "
         "developing.", font(SANS, 9), fill=GRAY)
    text(d, (16, 948),
         "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn "
         "illustrations, not photographs.", font(SANS, 9), fill=GRAY)
    text(d, (512, 968),
         "THE WORLD TODAY  \u00b7  Monday 23 November 2026  \u00b7  "
         "31 stories  \u00b7  6 regions", font(SANS_B, 12), fill=GOLD,
         anchor="ma")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out)
    print("saved", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
