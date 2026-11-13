"""Build assets/banner.svg: animated hero banner with the embedded photo cutout."""
import base64, math, random, sys

photo_path, out_path = sys.argv[1], sys.argv[2]
photo = base64.b64encode(open(photo_path, "rb").read()).decode()

W, H = 1200, 440
random.seed(7)

# Andes-like contour lines
contours = []
for i in range(9):
    base = 300 + i * 18
    pts = []
    for x in range(-40, W + 41, 40):
        y = base - 70 * math.exp(-((x - 980) / 260) ** 2) - 45 * math.exp(-((x - 640) / 180) ** 2) \
            - 30 * math.exp(-((x - 260) / 220) ** 2) + 6 * math.sin(x / 47 + i)
        pts.append((x, y + i * 4))
    d = "M" + " L".join(f"{x:.0f},{y:.1f}" for x, y in pts)
    contours.append(f'<path d="{d}" class="ct" style="opacity:{0.05 + i * 0.018:.3f}"/>')

stars = "".join(
    f'<circle cx="{random.randint(0, W)}" cy="{random.randint(0, 260)}" r="{random.choice([0.8, 1, 1.3, 1.6])}" '
    f'class="st" style="animation-delay:{random.uniform(0, 4):.2f}s"/>'
    for _ in range(70)
)

chips = [("Remote-sensing ML", "#00F740"), ("Astrophysics", "#58E1FF"),
         ("Full-Stack", "#FFB300"), ("10+ apps self-hosted", "#FF6B9A")]
chip_svg, cx = [], 60
for label, color in chips:
    w = 22 + len(label) * 8.4
    chip_svg.append(
        f'<g transform="translate({cx:.0f},318)"><rect width="{w:.0f}" height="32" rx="16" fill="{color}" fill-opacity=".12" stroke="{color}" stroke-opacity=".55"/>'
        f'<text x="{w/2:.0f}" y="21" text-anchor="middle" class="chip" fill="{color}">{label}</text></g>')
    cx += w + 10

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="R. Andre Vilca-Solorzano — ML Researcher and Full-Stack Engineer">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#040915"/><stop offset=".55" stop-color="#0a1a3a"/><stop offset="1" stop-color="#0f2a55"/>
  </linearGradient>
  <radialGradient id="glow" cx=".5" cy=".5" r=".5">
    <stop offset="0" stop-color="#2f7bff" stop-opacity=".55"/><stop offset=".6" stop-color="#2f7bff" stop-opacity=".12"/><stop offset="1" stop-color="#2f7bff" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="ring" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#00F740"/><stop offset=".5" stop-color="#58E1FF"/><stop offset="1" stop-color="#7B5CFF"/>
  </linearGradient>
  <linearGradient id="name" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#9cc4ff"/>
  </linearGradient>
  <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">
    <stop offset=".78" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <mask id="pm"><rect x="760" y="0" width="440" height="{H}" fill="url(#fade)"/></mask>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="22"/></clipPath>
  <path id="orbit" d="M 840,175 a 150,46 -18 1,0 300,0 a 150,46 -18 1,0 -300,0"/>
</defs>
<style>
  .ct {{ fill:none; stroke:#58E1FF; stroke-width:1.2; }}
  .st {{ fill:#cfe3ff; animation: tw 4s ease-in-out infinite; }}
  @keyframes tw {{ 0%,100% {{ opacity:.15 }} 50% {{ opacity:.9 }} }}
  .mono {{ font-family: 'JetBrains Mono','SFMono-Regular',Consolas,'Liberation Mono',monospace; }}
  .sans {{ font-family: 'Inter','Segoe UI',-apple-system,BlinkMacSystemFont,Helvetica,Arial,sans-serif; }}
  .chip {{ font: 600 13.5px 'Inter','Segoe UI',-apple-system,Helvetica,Arial,sans-serif; }}
  .cur {{ animation: bl 1.1s steps(1) infinite; }}
  @keyframes bl {{ 50% {{ opacity:0 }} }}
  .rise {{ animation: rise .9s ease-out both; }}
  .d1 {{ animation-delay:.15s }} .d2 {{ animation-delay:.3s }} .d3 {{ animation-delay:.45s }} .d4 {{ animation-delay:.6s }}
  @keyframes rise {{ from {{ opacity:0; transform: translateY(14px) }} to {{ opacity:1; transform:none }} }}
  .spin {{ transform-origin: 990px 205px; animation: sp 28s linear infinite; }}
  @keyframes sp {{ to {{ transform: rotate(360deg) }} }}
  .drift {{ animation: dr 14s ease-in-out infinite alternate; }}
  @keyframes dr {{ to {{ transform: translateX(-30px) }} }}
</style>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  {stars}
  <g class="drift">{''.join(contours)}</g>

  <!-- photo -->
  <circle cx="990" cy="205" r="210" fill="url(#glow)"/>
  <g class="spin"><circle cx="990" cy="205" r="168" fill="none" stroke="url(#ring)" stroke-width="2.5" stroke-dasharray="6 10" opacity=".8"/></g>
  <circle cx="990" cy="205" r="150" fill="#0d2350" stroke="url(#ring)" stroke-width="3"/>
  <use href="#orbit" xlink:href="#orbit" fill="none" stroke="#58E1FF" stroke-opacity=".35" stroke-width="1.2"/>
  <image x="770" y="20" width="440" height="440" href="data:image/webp;base64,{photo}" xlink:href="data:image/webp;base64,{photo}" mask="url(#pm)"/>
  <g>
    <circle r="5" fill="#00F740"><animateMotion dur="9s" repeatCount="indefinite" rotate="auto"><mpath href="#orbit" xlink:href="#orbit"/></animateMotion></circle>
    <circle r="12" fill="#00F740" opacity=".18"><animateMotion dur="9s" repeatCount="indefinite"><mpath href="#orbit" xlink:href="#orbit"/></animateMotion></circle>
  </g>

  <!-- text -->
  <text x="60" y="92" class="mono" font-size="19" fill="#00F740">$ whoami<tspan class="cur">▌</tspan></text>
  <text x="58" y="160" class="sans" font-size="54" font-weight="800" fill="url(#name)" letter-spacing="-1">R. Andre</text>
  <text x="58" y="220" class="sans" font-size="54" font-weight="800" fill="url(#name)" letter-spacing="-1">Vilca-Solorzano</text>
  <text x="60" y="264" class="sans" font-size="21" font-weight="500" fill="#c9d8f5">ML Researcher  ·  Full-Stack Engineer</text>
  <text x="60" y="293" class="mono" font-size="14.5" fill="#7f97c4">📍 Puno, Peru · 3,827 m a.s.l. · UNA Puno — FINESI</text>
  <g>{''.join(chip_svg)}</g>
  <text x="60" y="400" class="mono" font-size="13" fill="#4f6a9a">// satellite data → early-warning tools for the Andes</text>
</g>
</svg>'''
open(out_path, "w").write(svg)
print(len(svg))
