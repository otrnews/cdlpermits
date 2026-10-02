"""Builds the cdlpermits.com static site from questions.json.
Edit questions.json (or the settings below), then run: python build.py"""
import json, html, datetime

# ---------- Settings you can change ----------
SITE = "https://cdlpermits.com"
MYCDLCOACH = "https://mycdlcoach.com"
OTRNEWS = "https://otrnews.com"
CONTACT = "news@otrnews.com"
# Partner ads. Replace each url with your referral link.
PARTNERS = [
    {"name": "DAT", "kind": "Load board", "text": "Looking for freight once you're driving? Get 10% off DAT load board subscriptions.", "cta": "Get 10% off DAT", "url": "https://www.dat.com"},
    {"name": "Truck Parking Club", "kind": "Truck parking", "text": "Find and reserve safe truck parking before you get there.", "cta": "Find parking", "url": "https://truckparkingclub.com"},
    {"name": "OTR News", "kind": "Trucking news", "text": "Daily trucking news, rates and tools for drivers and owner-operators.", "cta": "Read OTR News", "url": "https://otrnews.com"},
]
# ---------------------------------------------

YEAR = datetime.date.today().year
data = json.load(open("questions.json", encoding="utf-8"))
tests = data["tests"]
e = html.escape
UTM = "utm_source=cdlpermits"

def head(title, desc, path):
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}{path}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}{path}">
<meta name="theme-color" content="#2C3E50">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='18' fill='%230F5FF8'/><text x='50' y='64' font-size='38' font-family='Arial' font-weight='bold' fill='white' text-anchor='middle'>CDL</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fira+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css">
</head><body>
<div class="strip">Passed your permit? <a href="{MYCDLCOACH}?{UTM}&utm_medium=strip">Get your ELDT theory certificate with MyCDLCoach</a></div>
<header class="top"><div class="wrap">
<a class="brand" href="/"><span class="shield">CDL</span><span>cdl<span class="hl">permits</span>.com</span></a>
<nav><a href="/#tests">All tests</a></nav>
</div></header>
<main class="wrap">
"""

def partners(title="Tools for your trucking career"):
    h = f'<section class="partners"><h2>{e(title)}</h2><div class="plist">'
    for p in PARTNERS:
        sep = "&" if "?" in p["url"] else "?"
        h += f'''<a class="pcard" href="{e(p["url"])}{sep}{UTM}&utm_medium=partner" rel="sponsored noopener" target="_blank">
<span class="ptag">Partner</span><strong>{e(p["name"])}</strong><span class="pkind">{e(p["kind"])}</span>
<span class="ptext">{e(p["text"])}</span><span class="pcta">{e(p["cta"])}</span></a>'''
    return h + "</div></section>"

def cta():
    return f"""<aside class="cta">
<h2>Passed your permit? Finish your ELDT theory next.</h2>
<p>Before your skills test, federal rules require Entry-Level Driver Training from a registered provider. MyCDLCoach covers the theory portion online, at your own pace.</p>
<a class="btn btn-sign" href="{MYCDLCOACH}?{UTM}&utm_medium=banner">Start ELDT theory with MyCDLCoach</a>
</aside>"""

def foot():
    return f"""</main>
<footer><div class="wrap">
<p>CDL Permits is a free study site. It is not affiliated with the FMCSA or any state DMV. Questions are based on the federal model CDL manual; always study your own state's CDL manual too, since rules and question counts vary.</p>
<p>Some links on this site are partner links, and we may earn a commission if you sign up. It never costs you extra.</p>
<p>Trucking news: <a href="{OTRNEWS}">OTR News</a>. Questions or corrections: <a href="mailto:{CONTACT}">{CONTACT}</a></p>
<p>A free study tool from <a href="{MYCDLCOACH}">MyCDLCoach</a>. &copy; {YEAR} CDL Permits</p>
</div></footer>
<canvas id="confetti" aria-hidden="true"></canvas>
<script src="/quiz.js" defer></script>
</body></html>"""

def js(obj):
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")

# ---------- Home ----------
allq = [{"t": t["slug"], "n": t["name"], **q} for t in tests for q in t["questions"]]
h = head(f"Free CDL Permit Practice Tests ({YEAR}) | CDL Permits",
         "Free CDL permit practice tests with answers explained: General Knowledge, Air Brakes, Combination, Hazmat, Tanker, Doubles/Triples, Passenger and School Bus. No sign-up.", "/")
h += """<div class="hero"><div class="sign"><div class="sign-inner">
<h1>CDL permit practice tests</h1>
<p>Free, no sign-up. Every answer explained, based on the CDL manual.</p>
</div></div></div>
<div id="dash" class="dash" hidden></div>
<section class="qotd" id="qotd" aria-labelledby="qotd-h"><div class="diamond" aria-hidden="true"><span>?</span></div>
<div class="qotd-body"><h2 id="qotd-h">Question of the day</h2><div id="qotd-box"><noscript>Turn on JavaScript to answer today's question.</noscript></div></div></section>
<ul class="exits" id="tests">"""
for n, t in enumerate(tests, 1):
    h += f"""<li class="exit"><a href="/{t['slug']}"><span class="tab">EXIT {n}</span><div class="sign"><div class="sign-inner">
<span class="badge" data-badge="{t['slug']}" hidden aria-label="Passed"><span>✓</span></span>
<h2>{e(t['name'])}</h2><p>{e(t['who'])}</p>
<div class="meta">{len(t['questions'])} practice questions<span class="best" data-best="{t['slug']}" hidden></span></div>
</div></div></a></li>"""
h += """</ul>
<section class="info">
<h2>How the CDL permit test works</h2>
<p>To get your commercial learner's permit (CLP), you take written knowledge tests at your state's licensing office. Everyone takes General Knowledge. Most drivers also take Air Brakes, and Class A drivers take Combination Vehicles. Endorsements like Hazmat, Tanker, Doubles/Triples, Passenger and School Bus each have their own test.</p>
<p>Most states require a score of 80% on each test. Start with General Knowledge, then work down the list. Pass a test here and it earns a check mark, so you can see what's left.</p>
</section>"""
h += cta() + partners()
h += f"<script>window.ALLQ={js(allq)};window.TESTS={js([t['slug'] for t in tests])};</script>" + foot()
open("index.html", "w", encoding="utf-8").write(h)

# ---------- Test pages ----------
for t in tests:
    qn = len(t["questions"])
    title = f"CDL {t['name']} Practice Test ({YEAR}) | Free, With Answers"
    desc = f"Free CDL {t['name']} practice test: {qn} questions with answers explained. Practice mode, exam mode and missed-question review. {t['who']}"
    p = head(title, desc, f"/{t['slug']}")
    p += f"""<div class="test-head"><h1>CDL {e(t['name'])} practice test</h1>
<p>{e(t['who'])} The real test has {e(t['real'])}.</p></div>
<div class="quiz" id="quiz"><noscript>Turn on JavaScript to take the test, or study every question below.</noscript></div>
<details class="study"><summary>Study all {qn} questions with answers</summary><ol>"""
    for q in t["questions"]:
        p += f"<li><div>{e(q['q'])}</div><div class=\"ans\">{e(q['a'])}</div><div class=\"exp\">{e(q['e'])}</div></li>"
    p += "</ol></details>"
    p += '<h2 class="more-h">Other practice tests</h2><ul class="more">'
    for o in tests:
        if o is not t:
            p += f'<li><a href="/{o["slug"]}">{e(o["name"])}</a></li>'
    p += "</ul>" + cta() + partners()
    p += f"<script>window.QUIZ={js({'slug': t['slug'], 'name': t['name'], 'questions': t['questions']})};</script>" + foot()
    open(t["slug"] + ".html", "w", encoding="utf-8").write(p)

# ---------- Sitemap, robots, CNAME ----------
today = datetime.date.today().isoformat()
urls = ["/"] + [f"/{t['slug']}" for t in tests]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sm += "".join(f"<url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls) + "</urlset>\n"
open("sitemap.xml", "w").write(sm)
open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
open("CNAME", "w").write("cdlpermits.com\n")
print("Built", len(tests), "tests,", len(allq), "questions")
