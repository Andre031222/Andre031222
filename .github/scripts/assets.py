"""Build the profile's own SVG assets: section headers, tech-stack board, side illustration, footer.

Icons in ICONS are original line drawings made for this profile.
Technology logos come from Simple Icons (CC0 1.0, https://simpleicons.org).
"""
import math, os, re, sys

SI_DIR, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)

FONT = "'Inter','Segoe UI',-apple-system,BlinkMacSystemFont,Helvetica,Arial,sans-serif"
MONO = "'JetBrains Mono','SFMono-Regular',Consolas,'Liberation Mono',monospace"
BG, BORDER, TEXT, MUTED, GREEN, CYAN, VIOLET = "#0b1630", "#1f3a68", "#e6edf3", "#7f97c4", "#00F740", "#58E1FF", "#7B5CFF"

# --- original line icons (24x24 grid, stroked) -------------------------------------------
ICONS = {
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 3.6-6.5 8-6.5s8 2.5 8 6.5"/>',
    "paper": '<path d="M6 3h8l5 5v13H6z"/><path d="M14 3v5h5M9 13h7M9 17h5"/>',
    "repo": '<path d="M5 4.5A1.5 1.5 0 0 1 6.5 3H19v15H6.5A1.5 1.5 0 0 0 5 19.5z"/><path d="M5 19.5A1.5 1.5 0 0 0 6.5 21H19M9 7h6"/>',
    "server": '<rect x="3" y="4" width="18" height="7" rx="2"/><rect x="3" y="13" width="18" height="7" rx="2"/><path d="M7 7.5h.01M7 16.5h.01M11 7.5h6M11 16.5h6"/>',
    "layers": '<path d="M12 3 3 8l9 5 9-5z"/><path d="m3 12.5 9 5 9-5M3 16.5l9 5 9-5"/>',
    "chart": '<path d="M4 20V11M10 20V4M16 20v-7M3 20h18"/>',
    "satellite": '<path d="m10 7.5 6.5 6.5-2.5 2.5L7.5 10z"/><path d="m8.5 5.5-3 3-3-3 3-3zM18.5 15.5l-3 3 3 3 3-3zM7 7l1.6 1.6M17 17l-1.6-1.6"/><path d="M15 3.5A5.5 5.5 0 0 1 20.5 9M15 6.5A2.5 2.5 0 0 1 17.5 9"/>',
    "grid": '<rect x="3" y="3" width="5" height="5" rx="1"/><rect x="10" y="3" width="5" height="5" rx="1"/><rect x="17" y="3" width="4" height="5" rx="1"/><rect x="3" y="10" width="5" height="5" rx="1"/><rect x="10" y="10" width="5" height="5" rx="1"/><rect x="3" y="17" width="5" height="4" rx="1"/>',
    "mountain": '<path d="M2 20 9 8l4 6 3-4 6 10z"/><path d="m7.4 10.7 1.6 1.3 1.5-1.2"/>',
}


def icon(name, x, y, size, color):
    s = size / 24
    return (f'<g transform="translate({x},{y}) scale({s:.4f})" fill="none" stroke="{color}" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</g>')


def contour(w, base, amp, seed, cls="", extra=""):
    pts = [(x, base - amp * math.exp(-((x - w * .75) / (w * .2)) ** 2) - amp * .6 * math.exp(-((x - w * .4) / (w * .15)) ** 2)
            + 3 * math.sin(x / 37 + seed)) for x in range(0, w + 21, 20)]
    return f'<path class="{cls}" {extra} d="M' + " L".join(f"{x},{y:.1f}" for x, y in pts) + '"/>'


# --- section headers -------------------------------------------------------------------
HEADERS = [
    ("about", "user", "01", "About me", "who I am · what I do · how I work"),
    ("research", "paper", "02", "Research", "peer-reviewed work, with code for every paper"),
    ("repos", "repo", "03", "Featured repositories", "open, reproducible, documented"),
    ("systems", "server", "04", "Production systems", "institutional software I design, build & self-host"),
    ("stack", "layers", "05", "Tech stack", "the tools behind the work"),
    ("stats", "chart", "06", "GitHub activity", "refreshed daily by GitHub Actions"),
]
for key, ic, num, title, sub in HEADERS:
    W, H = 1200, 84
    lines = "".join(contour(W, 70 + i * 6, 26, i, "c") for i in range(4))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{title}">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{GREEN}"/><stop offset=".5" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>
<linearGradient id="bg" x1="0" x2="1"><stop offset="0" stop-color="#081124"/><stop offset="1" stop-color="#0f2a55"/></linearGradient>
<clipPath id="k"><rect width="{W}" height="{H}" rx="16"/></clipPath></defs>
<style>.c{{fill:none;stroke:{CYAN};stroke-opacity:.12;stroke-width:1.2}}</style>
<g clip-path="url(#k)"><rect width="{W}" height="{H}" fill="url(#bg)"/>{lines}</g>
<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="16" fill="none" stroke="{BORDER}" stroke-width="1.5"/>
<rect x="18" y="16" width="52" height="52" rx="14" fill="#0d2350" stroke="url(#g)" stroke-width="2"/>
{icon(ic, 30, 28, 28, "url(#g)")}
<text x="90" y="40" font-family="{FONT}" font-size="26" font-weight="800" fill="{TEXT}">{title}</text>
<text x="90" y="64" font-family="{MONO}" font-size="13.5" fill="{MUTED}"><tspan fill="{GREEN}">// {num}</tspan>  {sub.replace("&", "&amp;")}</text>
</svg>'''
    open(os.path.join(OUT, f"h-{key}.svg"), "w").write(svg)

# --- tech-stack board ------------------------------------------------------------------
def si(slug):
    raw = open(os.path.join(SI_DIR, f"{slug}.svg")).read()
    return re.search(r'<path d="([^"]+)"', raw).group(1)


def readable(hexcolor):
    r, g, b = (int(hexcolor[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return "#e6edf3" if 0.2126 * r + 0.7152 * g + 0.0722 * b < 0.28 else f"#{hexcolor}"

# (label, simple-icons slug | None, brand hex[, monogram]) ; "win" draws an original window glyph
STACK = [
    ("Core languages", True, [("Rust", "rust", "DEA584"), ("Java", "openjdk", "F89820"), ("C++", "cplusplus", "4F9BD9"),
                   ("Node.js", "nodedotjs", "5FA04E"), ("TypeScript", "typescript", "3178C6")]),
    ("Also in my toolbox", False, [("Python", "python", "3776AB"), ("R", "r", "276DC3"), ("C", "c", "A8B9CC"), ("C#", None, "9B4F96", "C#"),
                   ("JavaScript", "javascript", "F7DF1E"), ("PHP", "php", "777BB4"), ("Bash", "gnubash", "4EAA25"), ("LaTeX", "latex", "008080")]),
    ("Backend", False, [("Spring Boot", "springboot", "6DB33F"), ("Jakarta EE", None, "F28D1A", "JE"), (".NET", "dotnet", "8A63F0"),
                   ("Express", "express", "FFFFFF"), ("Django", "django", "44B78B"), ("Laravel", "laravel", "FF2D20"),
                   ("Celery", None, "A9CC54", "Ce"), ("Redis", "redis", "FF4438"), ("PostgreSQL", "postgresql", "4169E1"), ("MySQL", "mysql", "4479A1")]),
    ("Frontend", False, [("React", "react", "61DAFB"), ("Next.js", "nextdotjs", "FFFFFF"), ("Svelte", "svelte", "FF3E00"),
                   ("Vue", "vuedotjs", "4FC08D"), ("Vite", "vite", "9135FF"), ("Tailwind", "tailwindcss", "06B6D4")]),
    ("Cross-platform apps · macOS · Linux · Windows", False, [("macOS", "apple", "FFFFFF"), ("Linux", "linux", "FCC624"), ("Windows", "win", "3A96DD"),
                   ("Avalonia UI", None, "8B44AC", "Av"), ("CustomTkinter", None, "FFD43B", "Tk"), ("Android", "android", "3DDC84")]),
    ("Machine learning & data", False, [("PyTorch", "pytorch", "EE4C2C"), ("TensorFlow", "tensorflow", "FF6F00"), ("Keras", "keras", "D00000"),
                   ("scikit-learn", "scikitlearn", "F7931E"), ("XGBoost", None, "189FDD", "XGB"), ("OpenCV", "opencv", "5C3EE8"),
                   ("pandas", "pandas", "E70488"), ("NumPy", "numpy", "4DABCF"), ("Jupyter", "jupyter", "F37626")]),
    ("Remote sensing & IoT", False, [("Earth Engine", "googleearthengine", "4285F4"), ("QGIS", "qgis", "589632"),
                   ("NASA data", "nasa", "E03C31"), ("ESP32", "espressif", "E7352C"), ("Arduino", "arduino", "00878F")]),
    ("Infrastructure", False, [("Debian", "debian", "D70A53"), ("Arch Linux", "archlinux", "1793D1"), ("Hyprland", "hyprland", "58E1FF"),
                   ("Nginx", "nginx", "009639"), ("Apache", "apache", "D22128"), ("Docker", "docker", "2496ED"), ("Git", "git", "F03C2E"),
                   ("Actions", "githubactions", "2088FF")]),
]
WIN = '<rect x="2.5" y="4" width="19" height="16" rx="2.5"/><path d="M2.5 8.5h19M6 6.3h.01M8.5 6.3h.01M12 8.5V20M2.5 14.2h19"/>'
W, PAD, GAP = 1200, 28, 10
y, body = 30, []
for cat, core, items in STACK:
    TW, TH, LS = (220.8, 118, 2.2) if core else (84, 88, 1.4167)
    body.append(f'<text x="{PAD}" y="{y + 14}" font-family="{MONO}" font-size="13" fill="{GREEN}">// </text>'
                f'<text x="{PAD + 24}" y="{y + 14}" font-family="{FONT}" font-size="15" font-weight="700" fill="{TEXT}">{cat.replace("&", "&amp;")}</text>'
                + (f'<text x="{PAD + 24 + len(cat)*8.6 + 10}" y="{y + 14}" font-family="{MONO}" font-size="12" fill="{MUTED}">— what I reach for first</text>' if core else ""))
    y += 28
    for i, it in enumerate(items):
        label, slug, hexc = it[:3]
        x = PAD + i * (TW + GAP)
        col = readable(hexc)
        isz = 24 * LS
        top = y + (14 if not core else 20)
        if slug == "win":
            logo = f'<g transform="translate({x + TW/2 - isz/2},{top}) scale({LS})" fill="none" stroke="{col}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{WIN}</g>'
        elif slug:
            logo = f'<g transform="translate({x + TW/2 - isz/2},{top}) scale({LS})" fill="{col}"><path d="{si(slug)}"/></g>'
        else:
            mono = it[3]
            fs = (22 if len(mono) <= 2 else 17) * (LS / 1.4167)
            logo = (f'<rect x="{x + TW/2 - isz/2}" y="{top}" width="{isz}" height="{isz}" rx="{isz*.24:.1f}" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-width="1.5"/>'
                    f'<text x="{x + TW/2}" y="{top + isz/2 + fs*.36:.1f}" text-anchor="middle" font-family="{FONT}" font-size="{fs:.1f}" font-weight="800" fill="{col}">{mono}</text>')
        glow = ""
        body.append(
            f'<g><rect x="{x}" y="{y}" width="{TW}" height="{TH}" rx="14" fill="{col}" fill-opacity="{.1 if core else .06}" stroke="{col}" stroke-opacity="{.6 if core else .28}" stroke-width="{1.6 if core else 1}"{glow}/>'
            f'{logo}<text x="{x + TW/2}" y="{y + TH - (16 if core else 13)}" text-anchor="middle" font-family="{FONT}" font-size="{15 if core else 11.5}" font-weight="{800 if core else 600}" fill="{TEXT if core else MUTED}">{label}</text></g>')
    y += TH + 26
H = y - 4
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Tech stack">
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#060d1e"/><stop offset="1" stop-color="#0d2248"/></linearGradient><filter id="gl" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur in="SourceAlpha" stdDeviation="0"/></filter></defs>
<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="18" fill="url(#bg)" stroke="{BORDER}" stroke-width="1.5"/>
{"".join(body)}
<text x="{W - PAD}" y="{H - 14}" text-anchor="end" font-family="{MONO}" font-size="10.5" fill="#3d5683">logos: Simple Icons (CC0)</text>
</svg>'''
open(os.path.join(OUT, "stack.svg"), "w").write(svg)

# --- side illustration: satellite scanning the Andes -----------------------------------
W = H = 320
ridges = "".join(contour(W, 250 + i * 12, 70 - i * 8, i * 2, "rd", f'style="stroke-opacity:{.55 - i*.1:.2f}"') for i in range(4))
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Satellite scanning the Andes">
<defs><radialGradient id="sky" cx=".5" cy=".35" r=".7"><stop offset="0" stop-color="#14306a"/><stop offset="1" stop-color="#060d1e"/></radialGradient>
<linearGradient id="beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GREEN}" stop-opacity=".55"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></linearGradient>
<clipPath id="k"><rect width="{W}" height="{H}" rx="28"/></clipPath>
<path id="o" d="M 40,96 a 120,38 -8 1,0 240,0 a 120,38 -8 1,0 -240,0"/></defs>
<style>.rd{{fill:none;stroke:{CYAN};stroke-width:1.5}} .tw{{animation:t 3s ease-in-out infinite}} @keyframes t{{50%{{opacity:.2}}}}
.sc{{animation:s 3.2s ease-in-out infinite;transform-origin:160px 0}} @keyframes s{{0%,100%{{transform:translateX(-60px)}}50%{{transform:translateX(60px)}}}}</style>
<g clip-path="url(#k)">
<rect width="{W}" height="{H}" fill="url(#sky)"/>
<g fill="#cfe3ff"><circle class="tw" cx="40" cy="40" r="1.4"/><circle class="tw" cx="270" cy="54" r="1.2" style="animation-delay:1s"/><circle class="tw" cx="210" cy="24" r="1" style="animation-delay:2s"/><circle class="tw" cx="96" cy="170" r="1.1" style="animation-delay:.5s"/><circle class="tw" cx="292" cy="180" r="1.3" style="animation-delay:1.6s"/></g>
<use href="#o" fill="none" stroke="{CYAN}" stroke-opacity=".3" stroke-dasharray="4 6"/>
<g class="sc"><path d="M160 112 120 262h80z" fill="url(#beam)"/><path d="M118 262h84" stroke="{GREEN}" stroke-width="2" stroke-linecap="round"/></g>
{icon("satellite", 124, 70, 72, "#e6edf3")}
<circle r="4" fill="{GREEN}"><animateMotion dur="7s" repeatCount="indefinite"><mpath href="#o"/></animateMotion></circle>
{ridges}
<text x="24" y="300" font-family="{MONO}" font-size="11" fill="{MUTED}">S 15.84° · W 70.02° · 3,827 m</text>
</g>
<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="28" fill="none" stroke="{BORDER}" stroke-width="1.5"/>
</svg>'''
open(os.path.join(OUT, "andes-scan.svg"), "w").write(svg)

# --- footer ----------------------------------------------------------------------------
W, H = 1200, 150
ridges = "".join(contour(W, 120 + i * 9, 60 - i * 6, i * 3, "rd", f'style="stroke-opacity:{.45 - i*.08:.2f}"') for i in range(5))
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Take Andean science to the world stage">
<defs><linearGradient id="bg" x1="0" x2="1"><stop offset="0" stop-color="#060d1e"/><stop offset="1" stop-color="#0f2a55"/></linearGradient>
<clipPath id="k"><rect width="{W}" height="{H}" rx="20"/></clipPath></defs>
<style>.rd{{fill:none;stroke:{CYAN};stroke-width:1.4}}</style>
<g clip-path="url(#k)"><rect width="{W}" height="{H}" fill="url(#bg)"/>{ridges}</g>
<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="20" fill="none" stroke="{BORDER}" stroke-width="1.5"/>
<text x="{W/2}" y="58" text-anchor="middle" font-family="{FONT}" font-size="25" font-weight="800" fill="{TEXT}">“Take Andean science to the world stage.”</text>
<text x="{W/2}" y="86" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{MUTED}"><tspan fill="{GREEN}">$</tspan> echo "thanks for visiting" · Puno, Peru</text>
</svg>'''
open(os.path.join(OUT, "footer.svg"), "w").write(svg)
print("assets ok")

# --- link buttons ----------------------------------------------------------------------
ICONS["globe"] = '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z"/>'
ICONS["mail"] = '<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="m4 7 8 6 8-6"/>'
ICONS["id"] = '<rect x="3" y="5" width="18" height="14" rx="2.5"/><circle cx="9" cy="11" r="2.2"/><path d="M5.8 16c.6-1.6 1.8-2.4 3.2-2.4s2.6.8 3.2 2.4M14.5 10h4M14.5 13.5h3"/>'
BUTTONS = [("web", "Website", "andre.net.pe", ("icon", "globe"), CYAN),
           ("mail", "Email", "get in touch", ("icon", "mail"), "#FF6B9A"),
           ("orcid", "ORCID", "0009-0003-2385-5263", ("si", "orcid"), "#A6CE39"),
           ("scopus", "Scopus", "author profile", ("si", "scopus"), "#F28C38"),
           ("cti", "CTI Vitae", "CONCYTEC · Peru", ("icon", "id"), "#4F9BD9")]
for key, title, sub, (kind, ref), col in BUTTONS:
    W, H = 224, 60
    ic = (icon(ref, 16, 16, 28, col) if kind == "icon" else
          f'<g transform="translate(16,16) scale(1.1667)" fill="{col}"><path d="{si(ref)}"/></g>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{title}">
<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="14" fill="#0b1630" stroke="{col}" stroke-opacity=".55" stroke-width="1.5"/>
{ic}<text x="56" y="27" font-family="{FONT}" font-size="15" font-weight="800" fill="{TEXT}">{title}</text>
<text x="56" y="45" font-family="{MONO}" font-size="10.5" fill="{MUTED}">{sub}</text>
<path d="M{W-26} 24l6 6-6 6" fill="none" stroke="{col}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>'''
    open(os.path.join(OUT, f"btn-{key}.svg"), "w").write(svg)
print("buttons ok")
