"""Builds the cdlpermits.com static site from questions.json.
Edit questions.json (or the settings below), then run: python build.py"""
import json, html, datetime

# ---------- Settings you can change ----------
SITE = "https://cdlpermits.com"
MYCDLCOACH = "https://www.mycdlcoach.com/theory-and-endorsements"
LOUNGE = "https://www.mycdlcoach.com/offers/DzKSWbj5/checkout"
SHIELD = "https://otrnews.com/partners/mycdlcoach-shield.webp"
OTRNEWS = "https://otrnews.com"
CONTACT = "news@otrnews.com"
# Ads (same affiliate links and images as OTR News)
ADS = [
    {"name": "Truck Parking Club", "text": "Reserve a safe truck parking spot ahead of time, or earn money listing your own yard.", "cta": "Find parking", "url": "https://truckparkingclubcomllc.sjv.io/c/6864035/2019579/25053?trafsrc=partner_api", "img": "https://otrnews.com/partners/partner-tpc.webp"},
    {"name": "Roadside Masters", "text": "24/7 nationwide roadside assistance for trucks, so a breakdown doesn't leave you stuck.", "cta": "Sign up your truck", "url": "https://www.roadsidemasters.com/signup-truck.php?r=MYCDLCOACH", "img": "https://otrnews.com/partners/partner-roadside.webp"},
    {"name": "DAT Load Board", "text": "Looking for freight once you're driving? Get 10% off a DAT load board subscription.", "cta": "Try DAT", "url": "https://www.dat.com/power/0002438644", "img": "https://www.dat.com/wp-content/uploads/media/images/affiliates/Affiliate_banner_black_blue_O1.png"},
    {"name": "LodoShop", "text": "Big brands, bigger savings. Discount deals on everyday gear, tools and household goods.", "cta": "Shop deals", "url": "https://lodoshop.com?utm_source=cdlpermits&utm_medium=ad", "img": "https://otrnews.com/partners/partner-lodoshop.webp"},
]
# ---------------------------------------------

YEAR = datetime.date.today().year
data = json.load(open("questions.json", encoding="utf-8"))
tests = data["tests"]
e = html.escape
UTM = "utm_source=cdlpermits"

STATES = [
("Alabama","the Alabama Law Enforcement Agency (ALEA)"),("Alaska","the Alaska Division of Motor Vehicles"),("Arizona","the Arizona Department of Transportation Motor Vehicle Division (ADOT MVD)"),
("Arkansas","the Arkansas Office of Motor Vehicle and Arkansas State Police"),("California","the California Department of Motor Vehicles (DMV)"),("Colorado","the Colorado Division of Motor Vehicles"),
("Connecticut","the Connecticut Department of Motor Vehicles"),("Delaware","the Delaware Division of Motor Vehicles"),("District of Columbia","the DC Department of Motor Vehicles"),
("Florida","the Florida Department of Highway Safety and Motor Vehicles (FLHSMV)"),("Georgia","the Georgia Department of Driver Services (DDS)"),("Hawaii","your county's driver licensing office in Hawaii"),
("Idaho","the Idaho Transportation Department DMV"),("Illinois","the Illinois Secretary of State"),("Indiana","the Indiana Bureau of Motor Vehicles (BMV)"),
("Iowa","the Iowa Department of Transportation"),("Kansas","the Kansas Division of Vehicles"),("Kentucky","the Kentucky Transportation Cabinet"),
("Louisiana","the Louisiana Office of Motor Vehicles (OMV)"),("Maine","the Maine Bureau of Motor Vehicles"),("Maryland","the Maryland Motor Vehicle Administration (MVA)"),
("Massachusetts","the Massachusetts Registry of Motor Vehicles (RMV)"),("Michigan","the Michigan Secretary of State"),("Minnesota","Minnesota Driver and Vehicle Services (DVS)"),
("Mississippi","the Mississippi Department of Public Safety"),("Missouri","the Missouri Department of Revenue and Missouri State Highway Patrol"),("Montana","the Montana Motor Vehicle Division"),
("Nebraska","the Nebraska Department of Motor Vehicles"),("Nevada","the Nevada Department of Motor Vehicles"),("New Hampshire","the New Hampshire Division of Motor Vehicles"),
("New Jersey","the New Jersey Motor Vehicle Commission (MVC)"),("New Mexico","the New Mexico Motor Vehicle Division"),("New York","the New York State DMV"),
("North Carolina","the North Carolina DMV"),("North Dakota","the North Dakota Department of Transportation"),("Ohio","the Ohio Bureau of Motor Vehicles (BMV)"),
("Oklahoma","Service Oklahoma"),("Oregon","the Oregon DMV"),("Pennsylvania","PennDOT"),
("Rhode Island","the Rhode Island Division of Motor Vehicles"),("South Carolina","the South Carolina DMV"),("South Dakota","the South Dakota Department of Public Safety"),
("Tennessee","the Tennessee Department of Safety and Homeland Security"),("Texas","the Texas Department of Public Safety (DPS)"),("Utah","the Utah Driver License Division"),
("Vermont","the Vermont DMV"),("Virginia","the Virginia DMV"),("Washington","the Washington State Department of Licensing (DOL)"),
("West Virginia","the West Virginia DMV"),("Wisconsin","the Wisconsin DMV"),("Wyoming","the Wyoming Department of Transportation (WYDOT)"),
]
def sslug(name): return name.lower().replace(" ", "-") + "-cdl-practice-test"

def head(title, desc, path, lang="en"):
    es = lang == "es"
    strip = ('¿Aprobó su permiso? <a href="{u}?{m}&utm_medium=strip">Obtenga su certificado de teoría ELDT con MyCDLCoach</a>' if es
             else 'Passed your permit? <a href="{u}?{m}&utm_medium=strip">Get your ELDT theory certificate with MyCDLCoach</a>').format(u=MYCDLCOACH, m=UTM)
    nav = '<a href="/">English</a>' if es else '<a href="/free-cdl-course">Course</a><a href="/#tests">Tests</a><a href="/examen-cdl-en-espanol" lang="es">Español</a>'
    return f"""<!doctype html>
<html lang="{lang}"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}{path}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#2C3E50">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='18' fill='%230F5FF8'/><text x='50' y='64' font-size='38' font-family='Arial' font-weight='bold' fill='white' text-anchor='middle'>CDL</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fira+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css">
</head><body>
<div class="strip">{strip}</div>
<header class="top"><div class="wrap">
<a class="brand" href="/"><span class="shield">CDL</span><span>cdl<span class="hl">permits</span>.com</span></a>
<nav>{nav}</nav>
</div></header>
<main class="wrap">
"""

def partners(title="Tools for drivers", lang="en"):
    h = f'<section class="partners"><h2>{e(title)}</h2><div class="plist">'
    for p in ADS:
        h += f"""<a class="pcard" href="{e(p["url"])}" rel="sponsored noopener" target="_blank">
<span class="ptag">{"Anuncio" if lang=="es" else "Ad"}</span><span class="pimg"><img src="{e(p["img"])}" alt="{e(p["name"])}" loading="lazy"></span><strong>{e(p["name"])}</strong>
<span class="ptext">{e(p["text"])}</span><span class="pcta">{e(p["cta"])}</span></a>"""
    return h + "</div></section>"

def cta(lang="en"):
    if lang == "es":
        return f"""<aside class="cta"><img class="shield-img" src="{SHIELD}" alt="MyCDLCoach" width="48" height="48">
<h2>¿Aprobó su permiso? Termine su teoría ELDT.</h2>
<p>Antes del examen práctico, la ley federal exige la capacitación ELDT con un proveedor registrado. MyCDLCoach cubre la parte de teoría en línea, a su propio ritmo.</p>
<a class="btn btn-sign" href="{MYCDLCOACH}?{UTM}&utm_medium=banner&utm_campaign=es">Empezar la teoría ELDT con MyCDLCoach</a>
<p class="alt">¿Prefiere empezar gratis? <a href="{LOUNGE}?{UTM}&utm_medium=banner&utm_campaign=es">Únase al Driver's Lounge</a></p>
</aside>"""
    return f"""<aside class="cta"><img class="shield-img" src="{SHIELD}" alt="MyCDLCoach" width="48" height="48">
<h2>Passed your permit? Finish your ELDT theory next.</h2>
<p>Before your skills test, federal rules require Entry-Level Driver Training from a registered provider. MyCDLCoach covers the theory portion online, at your own pace.</p>
<a class="btn btn-sign" href="{MYCDLCOACH}?{UTM}&utm_medium=banner">Start ELDT theory with MyCDLCoach</a>
<p class="alt">Rather start free? <a href="{LOUNGE}?{UTM}&utm_medium=banner">Join the Driver's Lounge</a></p>
</aside>"""

def foot(lang="en"):
    if lang == "es":
        txt = f"""<p>CDL Permits es un sitio de estudio gratuito. No está afiliado con la FMCSA ni con ningún DMV estatal. Las preguntas se basan en el manual federal modelo de la CDL; estudie también el manual de su estado.</p>
<p>Los anuncios pueden ser enlaces de afiliado. Podemos ganar una comisión si se registra, sin costo para usted.</p>"""
    else:
        txt = f"""<p>CDL Permits is a free study site. It is not affiliated with the FMCSA or any state DMV. Questions are based on the federal model CDL manual; always study your own state's CDL manual too, since rules and question counts vary.</p>
<p>Ads on this site may be affiliate links. We may earn a commission if you sign up, at no cost to you.</p>"""
    return f"""</main>
<footer><div class="wrap">
{txt}
<p>Trucking news: <a href="{OTRNEWS}">OTR News</a>. Questions or corrections: <a href="mailto:{CONTACT}">{CONTACT}</a></p>
<p><a href="/free-cdl-course">Free CDL course</a> &nbsp; <a href="/states">CDL practice tests by state</a> &nbsp; <a href="/examen-cdl-en-espanol" lang="es">Examen CDL en español</a></p>
<p>A free study tool from <a href="https://www.mycdlcoach.com">MyCDLCoach</a>. &copy; {YEAR} CDL Permits</p>
</div></footer>
<canvas id="confetti" aria-hidden="true"></canvas>
<script src="/quiz.js" defer></script>
</body></html>"""

def js(obj):
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")

def study_list(qs, summary):
    p = f'<details class="study"><summary>{e(summary)}</summary><ol>'
    for q in qs:
        p += f"<li><div>{e(q['q'])}</div><div class=\"ans\">{e(q['a'])}</div><div class=\"exp\">{e(q['e'])}</div></li>"
    return p + "</ol></details>"

def faq_ld(pairs):
    return '<script type="application/ld+json">' + js({"@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]}) + "</script>"

pages = []
LESSON_FOR = {"general-knowledge": "cdl-basics", "air-brakes": "air-brakes", "combination-vehicles": "combination-vehicles", "hazmat": "endorsements", "tanker": "endorsements", "doubles-triples": "endorsements", "passenger": "endorsements", "school-bus": "endorsements"}
GK = next(t for t in tests if t["slug"] == "general-knowledge")

# ---------- Home ----------
allq = [{"t": t["slug"], "n": t["name"], **q} for t in tests for q in t["questions"]]
h = head(f"Free CDL Permit Practice Tests ({YEAR}) | CDL Permits",
         f"Free CDL permit practice tests: {len(allq)} questions with answers explained. General Knowledge, Air Brakes, Combination, Hazmat, Tanker, Doubles/Triples, Passenger and School Bus. No sign-up.", "/")
h += f"""<div class="hero"><div class="sign"><div class="sign-inner">
<h1>CDL permit practice tests</h1>
<p>Free, no sign-up. {len(allq)} questions, every answer explained.</p>
</div></div></div>
<div id="dash" class="dash" hidden></div>
<section class="qotd" id="qotd" aria-labelledby="qotd-h"><div class="diamond" aria-hidden="true"><span>?</span></div>
<div class="qotd-body"><h2 id="qotd-h">Question of the day</h2><div id="qotd-box"><noscript>Turn on JavaScript to answer today's question.</noscript></div></div></section>
<a class="course-banner" href="/free-cdl-course"><span class="cb-num">12</span><span><strong>New to CDL? Start the free course.</strong> 12 short lessons, each with a quick quiz. Earn a certificate when you finish.</span></a>
<ul class="exits" id="tests">"""
for n, t in enumerate(tests, 1):
    h += f"""<li class="exit"><a href="/{t['slug']}"><span class="tab">EXIT {n}</span><div class="sign"><div class="sign-inner">
<span class="badge" data-badge="{t['slug']}" hidden aria-label="Passed"><span>✓</span></span>
<h2>{e(t['name'])}</h2><p>{e(t['who'])}</p>
<div class="meta">{len(t['questions'])} practice questions<span class="best" data-best="{t['slug']}" hidden></span></div>
</div></div></a></li>"""
h += """</ul>
<section class="info">
<h2>Find your state</h2>
<p>Every state uses the same federal knowledge tests, with its own fees, offices and paperwork. Pick your state for a full-length practice exam and the steps to get your permit there.</p>
<form class="statepick" onsubmit="location.href=this.s.value;return false;"><label for="s">Your state</label>
<select id="s" name="s">""" + "".join(f'<option value="/{sslug(n)}">{e(n)}</option>' for n, _ in STATES) + """</select>
<button class="btn btn-sign" type="submit">Go</button></form>
<p><a href="/examen-cdl-en-espanol" lang="es">¿Prefiere estudiar en español? Examen CDL de práctica en español</a></p>
</section>
<section class="info">
<h2>How the CDL permit test works</h2>
<p>To get your commercial learner's permit (CLP), you take written knowledge tests at your state's licensing office. Everyone takes General Knowledge. Most drivers also take Air Brakes, and Class A drivers take Combination Vehicles. Endorsements like Hazmat, Tanker, Doubles/Triples, Passenger and School Bus each have their own test.</p>
<p>Most states require a score of 80% on each test. Start with General Knowledge, then work down the list. Pass a test here and it earns a check mark, so you can see what's left.</p>
</section>"""
h += cta() + partners()
h += faq_ld([("Are these CDL practice tests free?", "Yes. Every test is free with no sign-up."),
             ("What score do I need to pass the CDL permit test?", "Most states require 80% on each knowledge test."),
             ("Which CDL permit tests do I need?", "Everyone takes General Knowledge. Most drivers also take Air Brakes, and Class A drivers take Combination Vehicles. Endorsements each have their own test.")])
h += f"<script>window.ALLQ={js(allq)};window.TESTS={js([t['slug'] for t in tests])};</script>" + foot()
pages.append(("index.html", h, "/"))

# ---------- Test pages ----------
for t in tests:
    qn = len(t["questions"])
    title = f"CDL {t['name']} Practice Test ({YEAR}) | {qn} Free Questions"
    desc = f"Free CDL {t['name']} practice test: {qn} questions with answers explained. Practice mode, exam mode and missed-question review. {t['who']}"
    p = head(title, desc, f"/{t['slug']}")
    p += f"""<div class="test-head"><h1>CDL {e(t['name'])} practice test</h1>
<p>{e(t['who'])} The real test has {e(t['real'])}.</p>
<p class="studyfirst">Want to learn it first? <a href="/cdl-course-{LESSON_FOR.get(t['slug'],'cdl-basics')}">Take the free lesson</a></p></div>
<div class="quiz" id="quiz"><noscript>Turn on JavaScript to take the test, or study every question below.</noscript></div>"""
    p += study_list(t["questions"], f"Study all {qn} questions with answers")
    p += '<h2 class="more-h">Other practice tests</h2><ul class="more">'
    p += "".join(f'<li><a href="/{o["slug"]}">{e(o["name"])}</a></li>' for o in tests if o is not t)
    p += "</ul>" + cta() + partners()
    p += f"<script>window.QUIZ={js({'slug': t['slug'], 'name': t['name'], 'questions': t['questions']})};</script>" + foot()
    pages.append((t["slug"] + ".html", p, f"/{t['slug']}"))

# ---------- State pages ----------
idx = head(f"CDL Practice Tests by State ({YEAR}) | CDL Permits", "Free CDL permit practice tests for all 50 states and DC, with the steps to get your commercial learner's permit.", "/states")
idx += '<div class="test-head"><h1>CDL practice tests by state</h1><p>Pick your state for a full-length practice exam and the steps to get your permit there.</p></div><ul class="more states">'
idx += "".join(f'<li><a href="/{sslug(n)}">{e(n)}</a></li>' for n, _ in STATES) + "</ul>" + cta() + foot()
pages.append(("states.html", idx, "/states"))
for name, agency in STATES:
    sl = sslug(name)
    title = f"{name} CDL Practice Test ({YEAR}) | Free Permit Exam"
    desc = f"Free {name} CDL permit practice test with answers explained, plus the steps to get your commercial learner's permit through {agency}."
    p = head(title, desc, f"/{sl}")
    p += f"""<div class="test-head"><h1>{e(name)} CDL practice test</h1>
<p>A full-length General Knowledge practice exam, the test every {e(name)} CDL applicant takes. CDL permits in {e(name)} are issued by {e(agency)}.</p></div>
<div class="quiz" id="quiz"><noscript>Turn on JavaScript to take the test.</noscript></div>
<section class="info"><h2>How to get your CDL permit in {e(name)}</h2>
<ol class="steps">
<li><strong>Meet the age rule.</strong> You can drive within {e(name)} at 18 in most cases. You must be 21 to drive across state lines or haul hazmat.</li>
<li><strong>Get a DOT medical card.</strong> Pass a DOT physical with a certified medical examiner. The card lasts up to 24 months.</li>
<li><strong>Pass the knowledge tests.</strong> Take General Knowledge, plus Air Brakes and Combination Vehicles for most Class A jobs, and any endorsements you need. Most states require 80% to pass.</li>
<li><strong>Hold your permit at least 14 days.</strong> That's the federal minimum before you can take the skills test.</li>
<li><strong>Finish ELDT training.</strong> First-time Class A or B drivers, and new Hazmat, Passenger or School Bus endorsements, need Entry-Level Driver Training from a provider on the FMCSA registry.</li>
<li><strong>Pass the skills test.</strong> It covers a vehicle inspection, basic control skills and a road test.</li>
</ol>
<p>Check with {e(agency)} for current fees, office locations, what documents to bring, and the {e(name)} CDL manual.</p></section>
<h2 class="more-h">More {e(name)} CDL practice tests</h2><ul class="more">"""
    p += "".join(f'<li><a href="/{o["slug"]}">{e(o["name"])}</a></li>' for o in tests)
    p += "</ul>" + cta() + partners()
    p += faq_ld([(f"How many questions are on the {name} CDL general knowledge test?", "Most states use 50 questions for General Knowledge. Check your state's CDL manual to confirm."),
                 (f"What score do I need to pass the {name} CDL permit test?", "Most states require 80% on each knowledge test."),
                 (f"Who issues CDL permits in {name}?", f"CDL permits in {name} are issued by {agency}.")])
    p += f"<script>window.QUIZ={js({'slug': 'general-knowledge', 'name': 'General Knowledge', 'limit': 50, 'questions': GK['questions']})};</script>" + foot()
    pages.append((sl + ".html", p, f"/{sl}"))


# ---------- Free course ----------
LESSONS = json.load(open("courses.json", encoding="utf-8"))
ALLQS = [q for t in tests for q in t["questions"]]
def find_q(prefix): return next(q for q in ALLQS if q["q"].startswith(prefix))
total_min = sum(L["min"] for L in LESSONS)
c = head(f"Free CDL Course ({YEAR}) | 12 Lessons With Quizzes", f"Free online CDL permit course: {len(LESSONS)} short lessons with quizzes, from license classes to air brakes and endorsements. Earn a certificate. No sign-up.", "/free-cdl-course")
c += f"""<div class="test-head"><h1>Free CDL permit course</h1>
<p>{len(LESSONS)} short lessons, about {total_min} minutes in all. Each one ends with a quick quiz; score 80% to complete it. Your progress saves on this device.</p></div>
<div class="dash" id="cprog" hidden></div>
<ol class="lessons">"""
for i, L in enumerate(LESSONS, 1):
    c += f"""<li><a href="/cdl-course-{L['slug']}" data-lesson="{L['slug']}"><span class="lnum">{i}</span><span class="ltxt"><strong>{e(L['title'])}</strong><span>{e(L['summary'])} {L['min']} min.</span></span><span class="ldone" hidden aria-label="Completed">✓</span></a></li>"""
c += """</ol>
<section class="cert-wrap" id="certwrap" hidden>
<h2>You finished the course!</h2>
<p>Type your name to print or save your certificate.</p>
<input id="certname" type="text" placeholder="Your full name" autocomplete="name">
<div class="cert" id="cert"><div class="cert-inner">
<div class="diamond" aria-hidden="true"><span>✓</span></div>
<p class="cert-k">Certificate of completion</p>
<p class="cert-name" id="certout">Your name</p>
<p>has completed the 12-lesson CDL Permit Prep Course at cdlpermits.com</p>
<p class="cert-date" id="certdate"></p>
<p class="cert-note">This is a study certificate. It is not an ELDT training certificate.</p>
</div></div>
<button class="btn btn-sign" type="button" id="certprint">Print or save as PDF</button>
</section>"""
c += f"<script>window.LESSONS={js([L['slug'] for L in LESSONS])};</script>"
c += cta() + partners() + foot()
pages.append(("free-cdl-course.html", c, "/free-cdl-course"))
for i, L in enumerate(LESSONS):
    nxt = LESSONS[i + 1] if i + 1 < len(LESSONS) else None
    prv = LESSONS[i - 1] if i > 0 else None
    p = head(f"{L['title']} | Free CDL Course Lesson {i+1}", L["summary"], f"/cdl-course-{L['slug']}")
    p += f"""<nav class="crumb"><a href="/free-cdl-course">Free CDL course</a> &rsaquo; Lesson {i+1} of {len(LESSONS)}</nav>
<div class="lane lesson-lane" aria-hidden="true"><span style="width:{round(i/len(LESSONS)*100)}%"></span></div>
<article class="lesson"><h1>{e(L['title'])}</h1><p class="lmeta">Lesson {i+1} of {len(LESSONS)}. About {L['min']} minutes.</p>"""
    p += "".join(f"<p>{para}</p>" for para in L["body"])
    p += '<aside class="keys"><h2>Remember this</h2><ul>' + "".join(f"<li>{e(k)}</li>" for k in L["keys"]) + "</ul></aside></article>"
    p += '<h2 class="more-h" id="check">Lesson check</h2><div class="quiz" id="quiz"></div>'
    p += '<div class="lnav">' + (f'<a class="btn btn-ghost" href="/cdl-course-{prv["slug"]}">Previous lesson</a>' if prv else '') + \
         (f'<a class="btn btn-ghost" href="/cdl-course-{nxt["slug"]}">Next lesson</a>' if nxt else '<a class="btn btn-ghost" href="/free-cdl-course">Back to the course</a>') + '</div>'
    p += cta() + partners()
    quiz = {"slug": "lesson-" + L["slug"], "name": f"Lesson {i+1}", "questions": [find_q(x) for x in L["quiz"]],
            "lesson": {"slug": L["slug"], "next": ("/cdl-course-" + nxt["slug"]) if nxt else "/free-cdl-course", "nextTitle": nxt["title"] if nxt else None}}
    p += f"<script>window.QUIZ={js(quiz)};</script>" + foot()
    pages.append((f"cdl-course-{L['slug']}.html", p, f"/cdl-course-{L['slug']}"))

# ---------- Spanish ----------
es = json.load(open("questions_es.json", encoding="utf-8"))
p = head(f"Examen de Práctica CDL en Español ({YEAR}) | Gratis", "Examen de práctica CDL gratis en español: conocimientos generales, con respuestas explicadas. Sin registrarse.", "/examen-cdl-en-espanol", "es")
p += f"""<div class="test-head"><h1>Examen de práctica CDL en español</h1>
<p>Conocimientos Generales, el examen que todos presentan para el permiso CDL. {len(es['questions'])} preguntas con la respuesta explicada. Gratis, sin registrarse.</p>
<p>Muchos estados ofrecen el examen de conocimientos en español. Confirme con la oficina de licencias de su estado.</p></div>
<div class="quiz" id="quiz"></div>"""
p += study_list(es["questions"], f"Estudie las {len(es['questions'])} preguntas con respuestas")
p += cta("es") + partners("Herramientas para conductores", "es")
p += f"<script>window.QUIZ={js(es)};</script>" + foot("es")
pages.append(("examen-cdl-en-espanol.html", p, "/examen-cdl-en-espanol"))

for fn, html_, _ in pages:
    open(fn, "w", encoding="utf-8").write(html_)

# ---------- Question of the day: RSS feed (for Zapier) + daily image ----------
today_d = datetime.date.today()
n = (today_d - datetime.date(1970, 1, 1)).days
q = allq[(n * 7) % len(allq)]
img_name = f"qotd-{today_d.isoformat()}.png"

def draw_card(path, title, body, foot_txt, options=None):
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return False
    W = H = 1080
    im = Image.new("RGB", (W, H), "#2C3E50"); d = ImageDraw.Draw(im)
    def font(sz):
        for f in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]:
            try: return ImageFont.truetype(f, sz)
            except Exception: pass
        return ImageFont.load_default()
    d.rounded_rectangle([40, 40, W - 40, H - 40], radius=40, outline="white", width=8)
    d.polygon([(W//2, 110), (W//2 + 70, 180), (W//2, 250), (W//2 - 70, 180)], fill="#F3C300", outline="#1E2A36")
    d.text((W//2, 180), "?", font=font(80), fill="#1E2A36", anchor="mm")
    d.text((W//2, 310), title, font=font(48), fill="#F3C300", anchor="mm")
    import textwrap
    y = 390; f = font(48)
    for line in textwrap.wrap(body, 32)[:5]:
        d.text((W//2, y), line, font=f, fill="white", anchor="mm"); y += 62
    if options:
        y += 20; fo = font(36)
        for k, o in enumerate(options):
            lines = textwrap.wrap(o, 40)[:2]
            d.rounded_rectangle([110, y - 8, W - 110, y + 46 * len(lines) + 4], radius=14, fill="#3B5168")
            for li, line in enumerate(lines):
                d.text((140, y + 2 + li * 46), ("ABCD"[k] + ".  " if li == 0 else "     ") + line, font=fo, fill="white")
            y += 46 * len(lines) + 28
    d.text((W//2, H - 130), foot_txt, font=font(44), fill="white", anchor="mm")
    d.text((W//2, H - 75), "cdlpermits.com", font=font(40), fill="#7FB0FF", anchor="mm")
    im.save(path, optimize=True); return True

import random
opts = [q["a"]] + q["w"]; random.Random(n).shuffle(opts)
has_img = draw_card(img_name, "CDL QUESTION OF THE DAY", q["q"], "Comment your answer below", opts)
if not __import__("os").path.exists("og.png"):
    draw_card("og.png", "FREE CDL PRACTICE TESTS", f"{len(allq)} questions, every answer explained. No sign-up.", "Pass your CDL permit test")
pub = datetime.datetime.combine(today_d, datetime.time(10, 0)).strftime("%a, %d %b %Y %H:%M:%S +0000")
item_desc = f"{q['q']} Answer it and see the explanation at cdlpermits.com"
enc = f'<enclosure url="{SITE}/{img_name}" type="image/png" length="0"/>' if has_img else ""
rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
<title>CDL Question of the Day</title><link>{SITE}/</link><description>A new CDL permit test question every day.</description>
<item><title>CDL question of the day: {e(q['q'])}</title><link>{SITE}/#qotd</link><guid isPermaLink="false">qotd-{today_d.isoformat()}</guid>
<pubDate>{pub}</pubDate><description>{e(item_desc)}</description>{enc}</item>
</channel></rss>
"""
open("feed.xml", "w", encoding="utf-8").write(rss)

# ---------- Sitemap, robots, CNAME ----------
today = today_d.isoformat()
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sm += "".join(f"<url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod></url>\n" for _, _, u in pages) + "</urlset>\n"
open("sitemap.xml", "w").write(sm)
open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
open("CNAME", "w").write("cdlpermits.com\n")
print("Built", len(pages), "pages,", len(allq), "English +", len(es["questions"]), "Spanish questions")
