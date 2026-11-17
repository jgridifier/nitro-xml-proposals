#!/usr/bin/env python3
"""Static generator: proposals.json -> index.html + p/<id>.html. Run: python3 build.py"""
import json, html, os
ROOT = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(ROOT, "proposals.json")))
REPO = D["repo"]
E = html.escape
STATUSES = ["New", "Approved", "Building", "Shipped", "Declined"]

def head(title, rel):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="icon" href="{rel}favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="32x32" href="{rel}img/favicon-32.png">
<link rel="apple-touch-icon" href="{rel}img/apple-touch-icon.png"><link rel="manifest" href="{rel}manifest.webmanifest">
<meta name="apple-mobile-web-app-title" content="Nitro Proposals"><meta name="theme-color" content="#0a1b37">
<link rel="stylesheet" href="{rel}style.css"></head><body>
<header class="top"><a class="brand" href="{rel}index.html"><img class="logo" src="{rel}img/icon-192.png" alt="" width="24" height="24">Nitro XML <span class="muted">Proposals</span></a>
<a class="toplink" href="https://github.com/{REPO}">Repo</a></header>"""

def badge(p):
    s = p["status"]
    return f'<span class="badge s-{s.lower()}" data-status-for="{p["issue"] or ""}">{E(s)}</span>'

def note(p):
    """One-line status note; Shipped proposals link the merged PR."""
    pr = p.get("pr")
    if pr:
        return f'<p class="snote">Shipped in <a href="https://github.com/{REPO}/pull/{pr}">PR #{pr}</a>{(" · " + E(p["status_note"])) if p.get("status_note") else ""}</p>'
    if p.get("status_note"):
        return f'<p class="snote">{E(p["status_note"])}</p>'
    return ""

def issue_url(p):
    return f"https://github.com/{REPO}/issues/{p['issue']}" if p.get("issue") else None

def vote(p, big=False):
    u = issue_url(p)
    if not u:
        return '<p class="vote muted">Approval issue coming soon.</p>'
    cls = "vote big" if big else "vote"
    return (f'<div class="{cls}"><a class="btn" href="{u}">Open issue #{p["issue"]} to vote</a>'
            f'<p class="howto"><b>Approve:</b> tap 👍 on the issue · <b>Decline:</b> tap 👎</p></div>')

FOOT = """<footer class="foot"><p>Updated daily. Each proposal links to one GitHub issue: 👍 approves it, 👎 declines it.
Approved proposals go into the nightly build queue. Images labelled <b>MOCKUP</b> are illustrations, not shipped features.</p>
<p class="muted">Design inspired by research-publication sites. Not affiliated with Google.</p></footer>
<script src="{rel}status.js"></script></body></html>"""

def card(p):
    return f"""<article class="card"><a class="cardlink" href="p/{p['id']}.html">
<div class="thumb"><img src="{p.get('thumb_img',p['mock_img'])}" alt="Mockup: {E(p['headline'])}" loading="lazy"><span class="mocktag">MOCKUP</span></div>
<div class="cbody"><div class="meta"><span class="app">{E(p['app'])}</span>{badge(p)}<span class="effort">Effort {p['effort']}</span><span class="added">{E(p['added'])}</span></div>
<h3>{E(p['headline'])}</h3><p class="why1">{E(p['why'].split('. ')[0])}.</p></div></a>
{note(p)}{vote(p)}</article>"""

def index():
    ps = sorted(D["proposals"], key=lambda p: p["added"], reverse=True)
    counts = {s: sum(1 for p in ps if p["status"] == s) for s in STATUSES}
    chips = "".join(f'<span class="chip s-{s.lower()}">{s} · {counts[s]}</span>' for s in STATUSES if counts[s])
    feat = ps[0]
    out = head(D["title"], "") + f"""<main>
<section class="hero"><p class="eyebrow">Edition {E(D['updated'])}</p>
<h1>Enhancement proposals for Nitro XML</h1>
<p class="lede">Each card is one change that brings Nitro closer to Word, Excel and PowerPoint. Look at the picture, then vote on its issue: <b>👍 to approve</b>, <b>👎 to decline</b>. About 30 seconds each.</p>
<div class="chips">{chips}</div></section>
<h2 class="sect">Proposals</h2>
<section class="grid">{''.join(card(p) for p in ps)}</section>
</main>""" + FOOT.replace("{rel}", "")
    open(os.path.join(ROOT, "index.html"), "w").write(out)

def pair(p):
    t = p.get("today_detail_img"); m = p.get("detail_img")
    det = ""
    if t and m:
        det = f"""<h3 class="sub">Close-up of the change</h3><div class="pair">
<figure><figcaption class="lab today">TODAY</figcaption><a href="../{t}"><img src="../{t}" alt="Today close-up"></a></figure>
<figure><figcaption class="lab mock">MOCKUP</figcaption><a href="../{m}"><img src="../{m}" alt="Mockup close-up"></a></figure></div>"""
    full_h = '<h3 class="sub">Full screen</h3>' if det else ''
    return det + full_h + f"""<div class="pair">
<figure><figcaption class="lab today">TODAY · real screenshot</figcaption><a href="../{p['today_img']}"><img src="../{p['today_img']}" alt="{E(p['today_caption'])}"></a><p class="cap">{E(p['today_caption'])}</p></figure>
<figure><figcaption class="lab mock">PROPOSED · MOCKUP</figcaption><a href="../{p['mock_img']}"><img src="../{p['mock_img']}" alt="{E(p['mock_caption'])}"></a><p class="cap">{E(p['mock_caption'])}</p></figure>
</div><p class="hint">Tap an image to open it full size.</p>"""

def detail(p):
    dod = "".join(f"<li>{E(x)}</li>" for x in p["dod"])
    out = head(p["headline"], "../") + f"""<main class="detail">
<p class="crumb"><a href="../index.html">← All proposals</a></p>
<div class="meta"><span class="app">{E(p['app'])}</span>{badge(p)}<span class="muted">Added {E(p['added'])}</span></div>
<h1>{E(p['headline'])}</h1>
{note(p)}{vote(p, big=True)}
{pair(p)}
<h2>Why</h2><p class="body">{E(p['why'])}</p>
<div class="facts">
<div><span class="k">Effort</span><span class="v"><b class="eff">{p['effort']}</b> {E(p.get('effort_note',''))}</span></div>
<div><span class="k">Risk</span><span class="v">{E(p['risk'])}</span></div>
<div><span class="k">Perf / bundle</span><span class="v">{E(p['perf'])}</span></div></div>
<h2>Definition of done</h2><ul class="dod">{dod}</ul>
{vote(p, big=True)}
</main>""" + FOOT.replace("{rel}", "../")
    os.makedirs(os.path.join(ROOT, "p"), exist_ok=True)
    open(os.path.join(ROOT, "p", p["id"] + ".html"), "w").write(out)

index()
for p in D["proposals"]:
    detail(p)
print("built", len(D["proposals"]), "proposals")
