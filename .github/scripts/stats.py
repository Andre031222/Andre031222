"""Generate GitHub stats and top-languages cards (SVG) for the profile README.

Usage: GITHUB_TOKEN=... python stats.py <username> <out_dir>
Uses only the standard library so the workflow needs no installs.
"""
import json, os, sys, urllib.request
from datetime import datetime, timezone

USER, OUT = sys.argv[1], sys.argv[2]
TOKEN = os.environ["GITHUB_TOKEN"]

QUERY = """
query($login: String!, $cursor: String) {
  user(login: $login) {
    createdAt
    followers { totalCount }
    contributionsCollection {
      totalCommitContributions restrictedContributionsCount
      totalPullRequestContributions totalIssueContributions
      contributionCalendar { totalContributions }
    }
    repositories(ownerAffiliations: OWNER, isFork: false, first: 100, after: $cursor, privacy: PUBLIC) {
      totalCount
      pageInfo { hasNextPage endCursor }
      nodes { stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name color } } } }
    }
  }
}"""


def gql(variables):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json"})
    data = json.load(urllib.request.urlopen(req))
    if "errors" in data:
        raise SystemExit(data["errors"])
    return data["data"]["user"]


cursor, repos, first = None, [], None
while True:
    u = gql({"login": USER, "cursor": cursor})
    first = first or u
    repos += u["repositories"]["nodes"]
    page = u["repositories"]["pageInfo"]
    if not page["hasNextPage"]:
        break
    cursor = page["endCursor"]

cc = first["contributionsCollection"]
stars = sum(r["stargazerCount"] for r in repos)
langs = {}
for r in repos:
    for e in r["languages"]["edges"]:
        n = e["node"]["name"]
        if n in ("Jupyter Notebook", "TeX", "HTML", "CSS", "Makefile", "Dockerfile", "Shell", "Batchfile", "BibTeX Style", "Procfile", "PowerShell", "PostScript", "Roff", "Mustache"):
            continue
        size, color = langs.get(n, (0, e["node"]["color"] or "#8b949e"))
        langs[n] = (size + e["size"], color)

BG, BORDER, TITLE, TEXT, MUTED, GREEN, CYAN, VIOLET = "#0b1630", "#1f3a68", "#e6edf3", "#e6edf3", "#7f97c4", "#00F740", "#58E1FF", "#7B5CFF"
FONT = "'Inter','Segoe UI',-apple-system,BlinkMacSystemFont,Helvetica,Arial,sans-serif"
MONO = "'JetBrains Mono','SFMono-Regular',Consolas,'Liberation Mono',monospace"

# Original line icons drawn for this profile (24x24 grid, stroked).
ICONS = {
    "pulse": '<path d="M3 12h4l2.5-6 5 12 2.5-6H21"/>',
    "commit": '<circle cx="12" cy="12" r="3.5"/><path d="M3 12h5.5M15.5 12H21"/>',
    "merge": '<circle cx="6" cy="6" r="2.2"/><circle cx="6" cy="18" r="2.2"/><circle cx="18" cy="18" r="2.2"/><path d="M6 8.2v7.6M18 15.8V10a3 3 0 0 0-3-3h-4M13 4.5 10.5 7 13 9.5"/>',
    "repo": '<path d="M5 4.5A1.5 1.5 0 0 1 6.5 3H19v15H6.5A1.5 1.5 0 0 0 5 19.5z"/><path d="M5 19.5A1.5 1.5 0 0 0 6.5 21H19M9 7h6"/>',
    "star": '<path d="m12 3 2.7 5.6 6.1.8-4.5 4.2 1.2 6.1L12 16.7l-5.5 3 1.2-6.1-4.5-4.2 6.1-.8z"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c0-3.6 2.9-6 6.5-6s6.5 2.4 6.5 6M16 4.6a3.5 3.5 0 0 1 0 6.8M18 14.3c2.1.7 3.5 2.6 3.5 5.7"/>',
    "chart": '<path d="M4 20V11M10 20V4M16 20v-7M3 20h18"/>',
    "code": '<path d="m8 7-5 5 5 5M16 7l5 5-5 5M13.5 4l-3 16"/>',
}


def icon(name, x, y, size, color):
    return (f'<g transform="translate({x},{y}) scale({size/24:.4f})" fill="none" stroke="{color}" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</g>')


W, H = 590, 262
DEFS = (f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{GREEN}"/>'
        f'<stop offset=".5" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>'
        f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#060d1e"/><stop offset="1" stop-color="#0d2248"/></linearGradient></defs>')


def card(title, sub, ic, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{title}">
{DEFS}
<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="18" fill="url(#bg)" stroke="{BORDER}" stroke-width="1.5"/>
<rect x="22" y="20" width="40" height="40" rx="11" fill="#0d2350" stroke="url(#g)" stroke-width="1.8"/>
{icon(ic, 31, 29, 22, "url(#g)")}
<text x="76" y="38" font-family="{FONT}" font-size="18" font-weight="800" fill="{TITLE}">{title}</text>
<text x="76" y="56" font-family="{MONO}" font-size="11.5" fill="{MUTED}"><tspan fill="{GREEN}">//</tspan> {sub}</text>
{body}
</svg>'''


year = datetime.now(timezone.utc).year
tiles = [
    ("pulse", "contributions", str(year), cc["contributionCalendar"]["totalContributions"], GREEN),
    ("commit", f"commits {year}", "incl. private", cc["totalCommitContributions"] + cc["restrictedContributionsCount"], CYAN),
    ("code", "languages", "public code", len(langs), VIOLET),
    ("repo", "public repos", "own, non-fork", first["repositories"]["totalCount"], "#FFB300"),
    ("star", "stars", "across public repos", stars, "#FFD43B"),
    ("users", "followers", "on GitHub", first["followers"]["totalCount"], "#FF6B9A"),
]
body = []
for i, (ic, label, hint, value, col) in enumerate(tiles):
    x, y = 22 + (i % 3) * 186, 80 + (i // 3) * 88
    body.append(
        f'<rect x="{x}" y="{y}" width="174" height="78" rx="12" fill="{col}" fill-opacity=".07" stroke="{col}" stroke-opacity=".3"/>'
        f'{icon(ic, x + 14, y + 14, 18, col)}'
        f'<text x="{x + 40}" y="{y + 28}" font-family="{FONT}" font-size="12.5" font-weight="600" fill="{MUTED}">{label}</text>'
        f'<text x="{x + 14}" y="{y + 58}" font-family="{FONT}" font-size="25" font-weight="800" fill="{TEXT}">{value:,}</text>'
        f'<text x="{x + 162}" y="{y + 58}" text-anchor="end" font-family="{MONO}" font-size="9.5" fill="{MUTED}">{hint}</text>')
open(os.path.join(OUT, "stats.svg"), "w").write(card("GitHub stats", f"updated {datetime.now(timezone.utc):%Y-%m-%d}", "chart", "".join(body)))

top = sorted(langs.items(), key=lambda kv: -kv[1][0])[:8]
total = sum(s for _, (s, _) in top) or 1
bw, bar, x = W - 44, [], 22
for name, (size, color) in top:
    w = bw * size / total
    bar.append(f'<rect x="{x:.2f}" y="80" width="{max(w, 0.5):.2f}" height="12" fill="{color}"/>')
    x += w
items = "".join(
    f'<g transform="translate({22 + (i % 2) * 282},{124 + (i // 2) * 34})">'
    f'<rect x="0" y="-15" width="10" height="20" rx="3" fill="{color}"/><text x="20" y="0" font-family="{FONT}" font-size="14" font-weight="600" fill="{TEXT}">{name}</text>'
    f'<text x="262" y="0" text-anchor="end" font-family="{MONO}" font-size="13" fill="{MUTED}">{100*size/total:.1f}%</text></g>'
    for i, (name, (size, color)) in enumerate(top))
body = f'<clipPath id="r"><rect x="22" y="80" width="{bw}" height="12" rx="6"/></clipPath><g clip-path="url(#r)">{"".join(bar)}</g>{items}'
open(os.path.join(OUT, "top-langs.svg"), "w").write(card("Languages by code size", "public repositories · bytes of source", "code", body))
print("ok", len(repos), "repos")
