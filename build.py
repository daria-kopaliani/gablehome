#!/usr/bin/env python3
"""gablehome.app static site builder — zero JS, print-friendly, fast.

Outputs to docs/ (GitHub Pages). Every page renders complete without JavaScript.
Run: python3 build.py
"""
import os
import shutil
from tasks import TASKS, SEASONS, MONTH_NAMES

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "docs")
# Until the concept is proven and gablehome.app is bought, the site serves on
# the free GitHub Pages URL (project pages => subpath prefix on every link).
# Domain day: BASE=https://gablehome.app PREFIX= WRITE_CNAME=1 python3 build.py
BASE = os.environ.get("BASE", "https://daria-kopaliani.github.io/gablehome")
PREFIX = os.environ.get("PREFIX", "/gablehome")
WRITE_CNAME = os.environ.get("WRITE_CNAME") == "1"

CSS = """
:root { --pine:#175A44; --pine-lt:#2E8266; --ink:#22281f; --muted:#5f695c;
        --bg:#faf9f4; --card:#ffffff; --line:#e3e2d8; --accent-bg:#eaf2ec; }
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--ink);
       font:17px/1.65 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
main { max-width:44rem; margin:0 auto; padding:1.5rem 1.25rem 4rem; }
header.site { background:var(--pine); }
header.site .inner { max-width:44rem; margin:0 auto; padding:0.9rem 1.25rem;
                     display:flex; align-items:center; gap:0.6rem; }
header.site a { color:#f2efe6; text-decoration:none; font-weight:700; font-size:1.05rem;
                letter-spacing:0.01em; }
header.site svg { display:block; }
h1 { font-size:2rem; line-height:1.2; margin:1.2rem 0 0.5rem; letter-spacing:-0.01em; }
h2 { font-size:1.35rem; margin:2rem 0 0.6rem; }
p.lede { color:var(--muted); font-size:1.1rem; margin:0 0 1.5rem; }
a { color:var(--pine); }
.answer { background:var(--accent-bg); border-left:4px solid var(--pine);
          border-radius:8px; padding:0.9rem 1.1rem; margin:1.2rem 0; font-size:1.1rem; }
.answer strong { color:var(--pine); }
ul.checklist { list-style:none; padding:0; margin:1rem 0; }
ul.checklist li { background:var(--card); border:1px solid var(--line); border-radius:10px;
                  padding:0.9rem 1.1rem 0.9rem 2.7rem; margin:0 0 0.7rem; position:relative; }
ul.checklist li::before { content:""; position:absolute; left:0.95rem; top:1.05rem;
                  width:1.05rem; height:1.05rem; border:2px solid var(--pine);
                  border-radius:6px; }
ul.checklist b { display:block; }
ul.checklist span { color:var(--muted); font-size:0.94rem; }
ul.checklist .freq { color:var(--pine-lt); font-size:0.85rem; font-weight:600;
                     text-transform:uppercase; letter-spacing:0.05em; }
.grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(10.5rem,1fr));
        gap:0.6rem; padding:0; list-style:none; margin:1rem 0; }
.grid a { display:block; background:var(--card); border:1px solid var(--line);
          border-radius:10px; padding:0.7rem 0.9rem; text-decoration:none; color:var(--ink); }
.grid a:hover { border-color:var(--pine); }
.grid .k { color:var(--muted); font-size:0.85rem; display:block; }
.cta { background:var(--pine); color:#f2efe6; border-radius:12px; padding:1.2rem 1.4rem;
       margin:2.5rem 0 0; }
.cta b { font-size:1.1rem; }
.cta p { margin:0.3rem 0 0; color:#d9e4dc; }
.printnote { color:var(--muted); font-size:0.9rem; }
footer { max-width:44rem; margin:0 auto; padding:1.5rem 1.25rem 3rem; color:var(--muted);
         font-size:0.88rem; border-top:1px solid var(--line); }
footer a { color:var(--muted); }
@media print {
  header.site, .cta, footer, .printnote, .related { display:none; }
  body { background:#fff; font-size:12pt; }
  ul.checklist li { border:none; padding-left:2rem; margin-bottom:0.4rem; break-inside:avoid; }
}
"""

LOGO = ('<svg width="26" height="26" viewBox="0 0 100 100" aria-hidden="true">'
        '<path d="M14 52 L50 20 L86 52" stroke="#f2efe6" stroke-width="12" fill="none" '
        'stroke-linecap="round" stroke-linejoin="round"/>'
        '<line x1="28" y1="66" x2="28" y2="84" stroke="#f2efe6" stroke-width="11" stroke-linecap="round"/>'
        '<line x1="72" y1="66" x2="72" y2="84" stroke="#f2efe6" stroke-width="11" stroke-linecap="round"/>'
        '<line x1="50" y1="64" x2="50" y2="84" stroke="#4CC094" stroke-width="11" stroke-linecap="round"/></svg>')


def page(title, description, canonical, body):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<style>{CSS}</style>
</head>
<body>
<header class="site"><div class="inner">{LOGO}<a href="{PREFIX}/">Gable</a></div></header>
<main>
{body}
<div class="cta">
<b>Gable keeps this list for you.</b>
<p>The Gable app builds your home's maintenance schedule, reminds you when tasks come due, and keeps the record of everything you've done. Coming soon to iPhone.</p>
</div>
</main>
<footer>
<p>Gable — home maintenance, scheduled and remembered. · <a href="{PREFIX}/">All checklists</a></p>
</footer>
</body>
</html>"""


def checklist_html(tasks, link=True):
    out = ["<ul class=\"checklist\">"]
    for t in tasks:
        name = f"<a href=\"{PREFIX}/how-often/{t['slug']}/\">{t['name']}</a>" if link else t["name"]
        out.append(
            f"<li><span class=\"freq\">{t['interval']}</span><b>{name}</b>"
            f"<span>{t['why'].split('. ')[0]}.</span></li>")
    out.append("</ul>")
    return "\n".join(out)


def write(path, html):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(html)


def month_tasks(m):
    return [t for t in TASKS if m in t["months"]]


urls = []

if os.path.exists(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)

# ---- Index: the master checklist hub ----
season_links = "".join(
    f'<a href="{PREFIX}/{s}/"><b>{SEASONS[s]["title"].replace(" Home Maintenance Checklist", "")}</b>'
    f'<span class="k">{len([t for t in TASKS for m in t["months"] if m in SEASONS[s]["months"]])} tasks</span></a>'
    for s in ["spring", "summer", "fall", "winter"])
month_links = "".join(
    f'<a href="{PREFIX}/{MONTH_NAMES[m].lower()}/"><b>{MONTH_NAMES[m]}</b>'
    f'<span class="k">{len(month_tasks(m))} tasks</span></a>'
    for m in range(1, 13))
body = f"""
<h1>The Home Maintenance Checklist</h1>
<p class="lede">Every task a house actually needs — what to do, how often, and why it matters. Organized by month and season, free to print, written to be done rather than admired.</p>
<h2>By season</h2>
<div class="grid">{season_links}</div>
<h2>By month</h2>
<div class="grid">{month_links}</div>
<h2>How often should you…</h2>
<div class="grid">{"".join(f'<a href="{PREFIX}/how-often/{t["slug"]}/"><b>{t["name"]}</b><span class="k">{t["interval"]}</span></a>' for t in TASKS)}</div>
<p class="printnote">Every page here prints cleanly — press ⌘P (Mac) or Ctrl+P (Windows) for a paper copy.</p>
"""
write("index.html", page(
    "Home Maintenance Checklist — by month, season, and task",
    "The complete home maintenance checklist: monthly and seasonal task lists with how-often answers for every system in the house. Free and printable.",
    f"{BASE}/", body))
urls.append("/")

# ---- Monthly pages ----
for m in range(1, 13):
    name = MONTH_NAMES[m]
    tasks = month_tasks(m)
    body = f"""
<h1>{name} Home Maintenance Checklist</h1>
<p class="lede">{len(tasks)} tasks for {name} — each with the reason it's on the list. Print it, stick it on the fridge, and cross things off.</p>
{checklist_html(tasks)}
<p class="printnote">Press ⌘P (Mac) or Ctrl+P (Windows) to print this checklist.</p>
<p class="related">Nearby: <a href="{PREFIX}/{MONTH_NAMES[m - 1 if m > 1 else 12].lower()}/">{MONTH_NAMES[m - 1 if m > 1 else 12]}</a> · <a href="{PREFIX}/{MONTH_NAMES[m + 1 if m < 12 else 1].lower()}/">{MONTH_NAMES[m + 1 if m < 12 else 1]}</a> · <a href="{PREFIX}/">the full checklist</a></p>
"""
    write(f"{name.lower()}/index.html", page(
        f"{name} Home Maintenance Checklist — {len(tasks)} tasks",
        f"The {name} home maintenance checklist: {len(tasks)} tasks with why each one matters. Printable and free.",
        f"{BASE}/{name.lower()}/", body))
    urls.append(f"/{name.lower()}/")

# ---- Seasonal pages ----
for s, meta in SEASONS.items():
    tasks = [t for t in TASKS if any(m in t["months"] for m in meta["months"])]
    body = f"""
<h1>{meta['title']}</h1>
<p class="lede">{meta['blurb']}</p>
{checklist_html(tasks)}
<p class="printnote">Press ⌘P (Mac) or Ctrl+P (Windows) to print this checklist.</p>
<p class="related">Month by month: {" · ".join(f'<a href="{PREFIX}/{MONTH_NAMES[m].lower()}/">{MONTH_NAMES[m]}</a>' for m in meta["months"])}</p>
"""
    write(f"{s}/index.html", page(
        f"{meta['title']} ({len(tasks)} tasks, printable)",
        f"{meta['blurb']} {len(tasks)} tasks with the reason behind each.",
        f"{BASE}/{s}/", body))
    urls.append(f"/{s}/")

# ---- How-often pages ----
for t in TASKS:
    months = " and ".join(MONTH_NAMES[m] for m in t["months"]) if len(t["months"]) <= 2 \
        else ", ".join(MONTH_NAMES[m] for m in t["months"])
    related = [x for x in TASKS if x["system"] == t["system"] and x["slug"] != t["slug"]][:4]
    related_html = ""
    if related:
        related_html = ('<h2>Same part of the house</h2><div class="grid related">'
                        + "".join(f'<a href="{PREFIX}/how-often/{r["slug"]}/"><b>{r["name"]}</b>'
                                  f'<span class="k">{r["interval"]}</span></a>' for r in related)
                        + "</div>")
    question = f"How often should you {t['name'][0].lower() + t['name'][1:]}?"
    body = f"""
<h1>{question}</h1>
<div class="answer"><strong>{t['interval']}.</strong> On a calendar: {months}.</div>
<h2>Why it matters</h2>
<p>{t['why']}</p>
<h2>How to do it</h2>
<p>{t['how']}</p>
<h2>Signs you've waited too long</h2>
<p>{t['late']}</p>
{related_html}
"""
    write(f"how-often/{t['slug']}/index.html", page(
        f"{question} ({t['interval'].lower()})",
        f"{t['interval']}. {t['why'].split('. ')[0]}. How to do it and the signs you've waited too long.",
        f"{BASE}/how-often/{t['slug']}/", body))
    urls.append(f"/how-often/{t['slug']}/")

# ---- New homeowner page ----
first_year = [t for t in TASKS if t["system"] in ("Safety", "Plumbing", "Heating & cooling")]
body = f"""
<h1>Home Maintenance for New Homeowners</h1>
<p class="lede">Nobody hands you the manual at closing. Start with safety and the systems that fail expensively, then grow into the full seasonal rhythm.</p>
<h2>Do these first</h2>
{checklist_html(first_year)}
<h2>Then adopt the seasonal rhythm</h2>
<div class="grid">{season_links}</div>
"""
write("new-homeowners/index.html", page(
    "Home Maintenance for New Homeowners — where to start",
    "The new-homeowner maintenance starter list: safety checks and the systems that fail expensively, then the full seasonal rhythm.",
    f"{BASE}/new-homeowners/", body))
urls.append("/new-homeowners/")

# ---- Privacy policy (required by App Review for the paywall + ASC record) ----
body = """
<h1>Privacy Policy</h1>
<p class="lede">Gable is built so that your data stays yours. Short version: everything lives on your device, and we can't see any of it.</p>
<h2>What Gable stores</h2>
<p>Your home profile, maintenance schedule, completed-task history, photos you attach, and costs you record are stored on your device. If iCloud sync is enabled in a future version, that data syncs through your personal iCloud account, encrypted in transit and at rest by Apple — we never have access to it.</p>
<h2>What Gable collects</h2>
<p>Nothing. Gable has no accounts, no sign-in, no analytics SDKs, no advertising identifiers, and no third-party tracking of any kind. We do not collect, transmit, sell, or share any personal data.</p>
<h2>Purchases</h2>
<p>Subscriptions and one-time purchases are processed entirely by Apple through the App Store. We receive no payment details. Apple's handling of that data is described in <a href="https://www.apple.com/legal/privacy/">Apple's Privacy Policy</a>.</p>
<h2>Notifications</h2>
<p>Reminders are scheduled locally on your device. No notification content leaves your phone.</p>
<h2>Changes</h2>
<p>If this policy ever changes, the new version will be posted at this address with an updated date.</p>
<h2>Contact</h2>
<p>Questions about privacy: <a href="mailto:daria.kopaliani@gmail.com">daria.kopaliani@gmail.com</a>.</p>
<p class="printnote">Last updated: 27 August 2026.</p>
"""
write("privacy/index.html", page(
    "Gable Privacy Policy",
    "Gable's privacy policy: all data stays on your device; no accounts, no analytics, no tracking.",
    f"{BASE}/privacy/", body))
urls.append("/privacy/")

# ---- Infrastructure ----
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
      + "\n".join(f"  <url><loc>{BASE}{u}</loc></url>" for u in urls)
      + "\n</urlset>\n")
write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
if WRITE_CNAME:
    with open(os.path.join(OUT, "CNAME"), "w") as f:
        f.write("gablehome.app")

print(f"built {len(urls)} pages -> docs/")
