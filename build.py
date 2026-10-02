"""Builds the cdlpermits.com static site from questions.json.
Edit questions.json, then run: python build.py"""
import json, html, os, datetime

SITE = "https://cdlpermits.com"
MYCDLCOACH = "https://mycdlcoach.com"
OTRNEWS = "https://otrnews.com"
CONTACT = "news@otrnews.com"
YEAR = datetime.date.today().year

data = json.load(open("questions.json", encoding="utf-8"))
tests = data["tests"]
e = html.escape

def head(title, desc, path):
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}{path}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}{path}">
<meta name="theme-color" content="#2C3E50">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='18' fill='%230F5FF8'/><rect x='8' y='8' width='84' height='84' rx='12' fill='none' stroke='white' stroke-width='6'/><text x='50' y='64' font-size='38' font-family='Arial' font-weight='bold' fill='white' text-anchor='middle'>CDL</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fira+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css">
</head><body>
<div class="strip">Passed your permit? <a href="{MYCDLCOACH}?utm_source=cdlpermits&utm_medium=strip">Get your ELDT theory certificate with MyCDLCoach</a></div>
<header class="top"><div class="wrap">
<a class="brand" href="/"><span class="shield">CDL</span><span>cdl<span class="hl">permits</span>.com</span></a>
<nav><a href="/#tests">All tests</a></nav>
</div></header>
<main class="wrap">
"""

def cta():
    return f"""<aside class="cta">
<h2>Passed your permit? Finish your ELDT theory next.</h2>
<p>Before your skills test, federal rules require Entry-Level Driver Training from a registered provider. MyCDLCoach covers the theory portion online, at your own pace.</p>
<a class="btn btn-dark" href="{MYCDLCOACH}?utm_source=cdlpermits&utm_medium=referral">Start ELDT theory with MyCDLCoach</a>
</aside>"""

def foot():
    return f"""</main>
<footer><div class="wrap">
<p>CDL Permits is a free study site. It is not affiliated with the FMCSA or any state DMV. Questions are based on the federal model CDL manual; always study your own state's CDL manual too, since rules and question counts vary.</p>
<p>Trucking news: <a href="{OTRNEWS}">OTR News</a>. Questions or corrections: <a href="mailto:{CONTACT}">{CONTACT}</a></p>
<p>A free study tool from <a href="{MYCDLCOACH}">MyCDLCoach</a>. &copy; {YEAR} CDL Permits</p>
</div></footer>
<script src="/quiz.js" defer></script>
</body></html>"""

# Home page
h = head("Free CDL Permit Practice Tests (" + str(YEAR) + ") | CDL Permits",
         "Free CDL permit practice tests with answers and explanations: General Knowledge, Air Brakes, Combination, Hazmat, Tanker, Doubles/Triples and Passenger. No sign-up.", "/")
h += """<div class="hero"><div class="sign"><div class="sign-inner">
<h1>CDL permit practice tests</h1>
<p>Free, no sign-up. Every answer explained, based on the CDL manual.</p>
</div></div></div>
<ul class="exits" id="tests">"""
for n, t in enumerate(tests, 1):
    h += f"""<li class="exit"><a href="/{t['slug']}"><span class="tab">EXIT {n}</span><div class="sign"><div class="sign-inner">
<h2>{e(t['name'])}</h2><p>{e(t['who'])}</p>
<div class="meta">{len(t['questions'])} practice questions<span class="best" data-best="{t['slug']}" hidden></span></div>
</div></div></a></li>"""
h += """</ul>
<section class="info">
<h2>How the CDL permit test works</h2>
<p>To get your commercial learner's permit (CLP), you take written knowledge tests at your state's licensing office. Everyone takes General Knowledge. Most drivers also take Air Brakes, and Class A drivers take Combination Vehicles. Endorsements like Hazmat, Tanker, Doubles/Triples and Passenger each have their own test.</p>
<p>Most states require a score of 80% on each test. Start with General Knowledge, then work down the list.</p>
</section>"""
h += cta() + foot()
open("index.html", "w", encoding="utf-8").write(h)

# Test pages
for t in tests:
    qn = len(t["questions"])
    title = f"CDL {t['name']} Practice Test ({YEAR}) | Free, With Answers"
    desc = f"Free CDL {t['name']} practice test: {qn} questions with answers and explanations. {t['who']}"
    p = head(title, desc, f"/{t['slug']}")
    p += f"""<div class="test-head"><h1>CDL {e(t['name'])} practice test</h1>
<p>{e(t['who'])} The real test has {e(t['real'])}. Pick an answer to see if you're right and why.</p></div>
<div class="quiz" id="quiz"><noscript>Turn on JavaScript to take the test, or study every question below.</noscript></div>
<details class="study"><summary>Study all {qn} questions with answers</summary><ol>"""
    for q in t["questions"]:
        p += f"<li><div>{e(q['q'])}</div><div class=\"ans\">{e(q['a'])}</div><div class=\"exp\">{e(q['e'])}</div></li>"
    p += "</ol></details>"
    p += '<h2>Other practice tests</h2><ul class="more">'
    for o in tests:
        if o is not t:
            p += f'<li><a href="/{o["slug"]}">{e(o["name"])}</a></li>'
    p += "</ul>" + cta()
    payload = json.dumps({"slug": t["slug"], "name": t["name"], "questions": t["questions"]}, ensure_ascii=False).replace("</", "<\\/")
    p += f"<script>window.QUIZ={payload};</script>" + foot()
    open(t["slug"] + ".html", "w", encoding="utf-8").write(p)

# Sitemap + robots
today = datetime.date.today().isoformat()
urls = ["/"] + [f"/{t['slug']}" for t in tests]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sm += "".join(f"<url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls) + "</urlset>\n"
open("sitemap.xml", "w").write(sm)
open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
open("CNAME", "w").write("cdlpermits.com\n")
print("Built", len(tests), "tests,", sum(len(t["questions"]) for t in tests), "questions")
