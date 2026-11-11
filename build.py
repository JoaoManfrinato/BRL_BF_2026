#!/usr/bin/env python3
"""
Brazilian Lumber · Black Friday 2026 · Landing page generator.

One template, three branches. Edit the BRANCHES data below and run:
    python3 build.py
It writes <branch>/index.html and <branch>/thank-you.html for each branch.
Shared CSS/JS/images live in ./assets.
"""
from html import escape as e
from pathlib import Path

ROOT = Path(__file__).parent

# --------------------------------------------------------------------------
# Icons
# --------------------------------------------------------------------------
I = {
    "phone": '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>',
    "pin": '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>',
    "clock": '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>',
    "check": '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>',
    "arrow": '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M8 7h9v9"/></svg>',
    "nav": '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m3 11 19-9-9 19-2-8-8-2z"/></svg>',
}

# --------------------------------------------------------------------------
# Shared promo data (identical at every branch)
# --------------------------------------------------------------------------
PW_TIERS = [[2000, 5], [3000, 7], [5000, 10]]
DKT_TIERS = [[2000, 10], [3000, 15], [5000, 20]]

PW_BLOCK = {
    "id": "platinum-woods",
    "logo": ("../assets/logos/platinum-logo.png", "Platinum Woods", ""),
    "flag": "All branches",
    "title": "Platinum Woods Cumaru &amp; Garapa",
    "tagline": "More Hardwood. More Savings. More Possibilities.",
    "items": [
        ("Cumaru 5/4 × 6", "Decking &amp; dock use · SKUs 5464CU–5469CU"),
        ("Garapa 5/4 × 6", "Decking &amp; dock use · SKUs 5467GA, 5468GA, 54610GA–54620GA"),
    ],
    "tiers": PW_TIERS,
    "product": "pw-cumaru",
    "wood": ("#5a2d1a", "#8a4a2a"),
}

FERRETTI = {
    "id": "ferretti", "pct": "41%", "pct_small": "OFF",
    "flag": "All branches", "species": "Ferretti",
    "wood": ("#6d5843", "#a28a6d"), "texture": "wood--planks",
    "title": "Clearance Ferretti Flooring",
    "tag": "New Floors. Huge Black Friday Savings.",
    "prices": [("Classic Oak · Eslavonia · New Smoke", "$1.69", "/SF", "$2.89/SF")],
    "notes": ["Sold by the box (23.64 SF)", "While supplies last", "Contractors &amp; retail customers", "All clearance sales are final"],
    "product": "clr-ferretti",
}
TILES = {
    "id": "deck-tiles", "pct": "25%", "pct_small": "UP TO · OFF",
    "flag": "All branches", "species": "Deck Tiles",
    "wood": ("#3d2414", "#6e4128"), "texture": "wood--tiles",
    "title": "Clearance B-Grade Deck Tiles",
    "tag": "Large Format. Easy DIY Installation. Bigger Savings.",
    "prices": [("Ipe", "$29.95", "/pc", "$36.75/pc"), ("Cumaru Plus", "$24.49", "/pc", "$32.90/pc")],
    "notes": ["B-Grade: may show minor cosmetic marks (pin holes, chalk marks)", "While local supplies last", "Contractors &amp; retail customers", "All clearance sales are final"],
    "product": "clr-tiles",
}

MATRIX_PW = [
    ("pw", "Platinum Woods", "Cumaru 5/4 × 6", "Decking / dock", "5464CU – 5469CU", "5% – 10% OFF", "by order tier", "All branches"),
    ("pw", "Platinum Woods", "Garapa 5/4 × 6", "Decking / dock", "5467GA, 5468GA, 54610GA – 54620GA", "5% – 10% OFF", "by order tier", "All branches"),
]
MATRIX_CLR = [
    ("clr", "Clearance", "Ferretti Flooring", "Classic Oak · Eslavonia · New Smoke", "Box · 23.64 SF", "$1.69/SF", "was $2.89/SF · 41% OFF", "While supplies last"),
    ("clr", "Clearance", "B-Grade Deck Tiles · Ipe", "Large format", "Per piece", "$29.95/pc", "was $36.75/pc", "While local supplies last"),
    ("clr", "Clearance", "B-Grade Deck Tiles · Cumaru Plus", "Large format", "Per piece", "$24.49/pc", "was $32.90/pc · 25% OFF", "While local supplies last"),
]

OPTS_PW = [("pw-cumaru", "Platinum Woods · Cumaru 5/4 × 6"), ("pw-garapa", "Platinum Woods · Garapa 5/4 × 6")]
OPTS_CLR = [("clr-ferretti", "Clearance · Ferretti Flooring"), ("clr-tiles", "Clearance · B-Grade Deck Tiles")]

# --------------------------------------------------------------------------
# Branches
# --------------------------------------------------------------------------
BRANCHES = [
    {
        "slug": "miami",
        "name": "Miami HQ",
        "city": "Miami",
        "state": "FL",
        "tz": "ET",
        "deadline": "2026-12-02T04:59:59Z",  # Dec 1 11:59:59 PM EST
        "phone": "954.404.8011", "tel": "+19544048011",
        "addr1": "777 NW 71st Street", "addr2": "Miami, FL 33150",
        "domain": "brazilianlumber.com",
        "hours": [("Mon – Fri", "8:00 AM – 5:00 PM"), ("Saturday", "8:00 AM – 1:00 PM"), ("Sunday", "Closed")],
        "h1": "Black Friday at Brazilian Lumber Miami: up to 20% off Deckotech Prestige, up to 10% off Platinum Woods hardwoods and FREE Easy Oil",
        "banner_alt": "Up to 20% off Deckotech Prestige and FREE Easy Oil on natural wood orders of $750+. Black Friday deals valid Nov 13 – Dec 1, 2026 at the Miami location.",
        "ticker": ["Up to 20% OFF Deckotech Prestige", "Up to 10% OFF Platinum Woods", "FREE Easy Oil", "33% OFF Cypress #2", "41% OFF Ferretti Flooring", "Up to 25% OFF Deck Tiles"],
        "index": [
            ("#deckotech", "20", "%", "Up to · Off", "Deckotech Prestige", "Ashwood &amp; Silver Gray cladding", None),
            ("#platinum-woods", "10", "%", "Up to · Off", "Platinum Woods", "Cumaru &amp; Garapa 5/4 × 6", None),
            ("#easy-oil", "FREE", "", "Miami exclusive", "Easy Oil", "On natural wood orders $750+", "Miami only"),
            ("#clearance", "41", "%", "Clearance · Off", "Clearance deals", "Cypress · Ferretti · Deck Tiles", None),
        ],
        "dkt": {
            "id": "deckotech",
            "logo": ("../assets/logos/deckotech-logo.svg", "Deckotech", "tier-block__logo--dkt"),
            "flag": "Miami &amp; New Jersey",
            "title": "Deckotech Prestige",
            "tagline": "More Design. More Possibilities. More Savings.",
            "items": [
                ("Grid Cladding 16' · Ashwood", "SKU 1616DEASW"),
                ("Shiplap 16' · Silver Gray", "SKU 1616DECLSLPRSG"),
                ("Trims, corners &amp; finishing profiles included", "Discount applies to the full qualifying order"),
            ],
            "fine": "Royal Teak excluded.",
            "tiers": DKT_TIERS,
            "product": "dkt-ashwood",
            "img": "../assets/img/miami-desktop.jpg",
        },
        "easy_oil": True,
        "clearance": [
            {
                "id": "cypress", "pct": "33%", "pct_small": "OFF",
                "flag": "Miami only", "species": "Cypress #2",
                "wood": ("#8a6a45", "#c2a072"), "texture": "wood--planks",
                "title": "Clearance Cypress #2 · 1×6 T&amp;G",
                "tag": "More Linear Feet. Less to Pay.",
                "prices": [("Cypress #2 · 1×6 T&amp;G", "$1.59", "/SF", "$2.39/SF")],
                "notes": ["Open to all customers", "Pickup or delivery from Miami only", "All clearance sales are final"],
                "product": "clr-cypress",
            },
            FERRETTI, TILES,
        ],
        "matrix": [
            ("dkt", "Deckotech", "Prestige Grid Cladding 16'", "Ashwood", "1616DEASW", "10% – 20% OFF", "by order tier · Royal Teak excluded", "Miami &amp; NJ"),
            ("dkt", "Deckotech", "Prestige Shiplap 16'", "Silver Gray", "1616DECLSLPRSG", "10% – 20% OFF", "by order tier · Royal Teak excluded", "Miami &amp; NJ"),
            *MATRIX_PW,
            ("exc", "Miami exclusive", "Easy Oil", "1 gallon per ~250 SF", "—", "FREE", "on natural wood orders over $750 · not combinable", "Miami only"),
            ("clr", "Clearance", "Cypress #2 · 1×6 T&amp;G", "Tongue &amp; groove", "Per SF", "$1.59/SF", "was $2.39/SF · 33% OFF", "Miami only"),
            *MATRIX_CLR,
        ],
        "options": [("dkt-ashwood", "Deckotech Prestige · Grid Cladding Ashwood"),
                    ("dkt-silvergray", "Deckotech Prestige · Shiplap Silver Gray"),
                    *OPTS_PW,
                    ("easy-oil", "Natural wood order + FREE Easy Oil"),
                    ("clr-cypress", "Clearance · Cypress #2 1×6 T&amp;G"),
                    *OPTS_CLR],
    },
    {
        "slug": "new-jersey",
        "name": "New Jersey",
        "city": "New Jersey",
        "state": "NJ",
        "tz": "ET",
        "deadline": "2026-12-02T04:59:59Z",  # Dec 1 11:59:59 PM EST
        "phone": "(732) 708-6256", "tel": "+17327086256",
        "addr1": "593 Nassau St", "addr2": "North Brunswick Township, NJ 08902",
        "domain": "brazilianlumbernewyork.com",
        "hours": [("Mon – Fri", "8:00 AM – 5:00 PM"), ("Sat – Sun", "Closed")],
        "h1": "Black Friday at Brazilian Lumber New Jersey: up to 20% off Deckotech Prestige and up to 10% off Platinum Woods hardwoods",
        "banner_alt": "Up to 20% off Deckotech Prestige Grid Cladding in Ashwood and Shiplap in Silver Gray. Black Friday deals valid Nov 13 – Dec 1, 2026 at the New Jersey location.",
        "ticker": ["Up to 20% OFF Deckotech Prestige", "Up to 10% OFF Platinum Woods", "41% OFF Ferretti Flooring", "Up to 25% OFF Deck Tiles", "Build bigger, spend smarter"],
        "index": [
            ("#deckotech", "20", "%", "Up to · Off", "Deckotech Prestige", "Ashwood &amp; Silver Gray cladding", None),
            ("#platinum-woods", "10", "%", "Up to · Off", "Platinum Woods", "Cumaru &amp; Garapa 5/4 × 6", None),
            ("#ferretti", "41", "%", "Clearance · Off", "Ferretti Flooring", "$1.69/SF · was $2.89", None),
            ("#deck-tiles", "25", "%", "Up to · Off", "B-Grade Deck Tiles", "Ipe &amp; Cumaru Plus", None),
        ],
        "dkt": {
            "id": "deckotech",
            "logo": ("../assets/logos/deckotech-logo.svg", "Deckotech", "tier-block__logo--dkt"),
            "flag": "Miami &amp; New Jersey",
            "title": "Deckotech Prestige",
            "tagline": "More Design. More Possibilities. More Savings.",
            "items": [
                ("Grid Cladding 16' · Ashwood", "SKU 1616DEASW"),
                ("Shiplap 16' · Silver Gray", "SKU 1616DECLSLPRSG"),
                ("Includes trims &amp; corners of the same color", "Discount applies to the full qualifying order"),
            ],
            "fine": "Royal Teak excluded.",
            "tiers": DKT_TIERS,
            "product": "dkt-ashwood",
            "img": "../assets/img/new-jersey-desktop.jpg",
        },
        "easy_oil": False,
        "clearance": [FERRETTI, TILES],
        "matrix": [
            ("dkt", "Deckotech", "Prestige Grid Cladding 16'", "Ashwood", "1616DEASW", "10% – 20% OFF", "by order tier · Royal Teak excluded", "Miami &amp; NJ"),
            ("dkt", "Deckotech", "Prestige Shiplap 16'", "Silver Gray", "1616DECLSLPRSG", "10% – 20% OFF", "by order tier · Royal Teak excluded", "Miami &amp; NJ"),
            *MATRIX_PW,
            *MATRIX_CLR,
        ],
        "options": [("dkt-ashwood", "Deckotech Prestige · Grid Cladding Ashwood"),
                    ("dkt-silvergray", "Deckotech Prestige · Shiplap Silver Gray"),
                    *OPTS_PW, *OPTS_CLR],
    },
    {
        "slug": "los-angeles",
        "name": "Los Angeles, CA",
        "city": "Los Angeles",
        "state": "CA",
        "tz": "PT",
        "deadline": "2026-12-02T07:59:59Z",  # Dec 1 11:59:59 PM PST
        "phone": "(323) 289-2647", "tel": "+13232892647",
        "addr1": "4629 S Alameda St", "addr2": "Los Angeles, CA 90058",
        "domain": "brazilianlumberlosangeles.com",
        "hours": [("Mon – Fri", "8:00 AM – 5:00 PM"), ("Sat – Sun", "Closed")],
        "h1": "Black Friday at Brazilian Lumber Los Angeles: up to 20% off Deckotech Prestige &amp; Terra and up to 10% off Platinum Woods hardwoods",
        "banner_alt": "Up to 20% off Deckotech Prestige & Terra. Limited stock: White Oak Grid Cladding and Forest Walnut Terra Shiplap. Black Friday deals valid Nov 13 – Dec 1, 2026 at the California location.",
        "ticker": ["Up to 20% OFF Deckotech Prestige &amp; Terra", "Up to 10% OFF Platinum Woods", "41% OFF Ferretti Flooring", "Up to 25% OFF Deck Tiles", "Limited stock · California only"],
        "index": [
            ("#deckotech", "20", "%", "Up to · Off", "Deckotech Prestige &amp; Terra", "White Oak &amp; Forest Walnut", "California only"),
            ("#platinum-woods", "10", "%", "Up to · Off", "Platinum Woods", "Cumaru &amp; Garapa 5/4 × 6", None),
            ("#ferretti", "41", "%", "Clearance · Off", "Ferretti Flooring", "$1.69/SF · was $2.89", None),
            ("#deck-tiles", "25", "%", "Up to · Off", "B-Grade Deck Tiles", "Ipe &amp; Cumaru Plus", None),
        ],
        "dkt": {
            "id": "deckotech",
            "logo": ("../assets/logos/deckotech-logo.svg", "Deckotech", "tier-block__logo--dkt"),
            "flag": "California only · Limited stock",
            "title": "Deckotech Prestige &amp; Terra Cladding",
            "tagline": "More Design. More Possibilities. More Savings.",
            "items": [
                ("Prestige Grid Cladding · White Oak", "1×8×16' · 295 pieces in stock"),
                ("Terra Shiplap Cladding · Forest Walnut", "1×6×16' · 349 pieces in stock"),
                ("Trims, corners &amp; finishing profiles included", "Discount applies to the full qualifying order"),
            ],
            "fine": "Limited stock: while California warehouse supplies last.",
            "tiers": DKT_TIERS,
            "product": "dkt-whiteoak",
            "img": "../assets/img/los-angeles-desktop.jpg",
        },
        "easy_oil": False,
        "clearance": [FERRETTI, TILES],
        "matrix": [
            ("dkt", "Deckotech", "Prestige Grid Cladding", "White Oak · 1×8×16'", "295 pcs in stock", "10% – 20% OFF", "by order tier", "California only"),
            ("dkt", "Deckotech", "Terra Shiplap Cladding", "Forest Walnut · 1×6×16'", "349 pcs in stock", "10% – 20% OFF", "by order tier", "California only"),
            *MATRIX_PW,
            *MATRIX_CLR,
        ],
        "options": [("dkt-whiteoak", "Deckotech Prestige · Grid Cladding White Oak"),
                    ("dkt-forestwalnut", "Deckotech Terra · Shiplap Forest Walnut"),
                    *OPTS_PW, *OPTS_CLR],
    },
]

LEGAL = ("Valid November 13 – December 1, 2026, until 11:59 PM local time at each branch. Discounts apply exclusively to "
         "orders placed and paid in full during the promotional window. Minimum purchase thresholds ($2,000, $3,000, and "
         "$5,000) are calculated before discount, taxes and freight. Discounts apply to the full qualifying order, including trims, "
         "corners and finishing profiles. Promotions cannot be combined with each other. All clearance sales are final. "
         "Campaign operates independently; retroactive discounts cannot be applied to open quotes issued prior to Black "
         "Friday. Shipping is not included. FSC-certified material is excluded. Offers are branch-specific and valid only while "
         "local warehouse stock lasts.")


# --------------------------------------------------------------------------
# Partials
# --------------------------------------------------------------------------
def head(b, title, desc):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#066938">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="../assets/img/{b['slug']}-desktop.jpg">
<link rel="preload" href="../assets/fonts/Archivo-Variable.ttf" as="font" type="font/ttf" crossorigin>
<link rel="stylesheet" href="../assets/css/bf.css">
<!-- TRACKING (Manuel): Meta Pixel + Google tag go here. Branch: {b['slug']} -->
</head>
"""


def countdown(extra=""):
    units = "".join(f'<span class="countdown__unit"><b data-u="{u}">00</b><small>{l}</small></span>'
                    for u, l in (("d", "d"), ("h", "h"), ("m", "m"), ("s", "s")))
    return f'<div class="countdown {extra}" data-countdown aria-live="off">{units}</div>'


def topbar(b):
    return f"""<div class="topbar" role="banner">
  <div class="wrap">
    <div class="topbar__branch"><a class="topbar__logo" href="#top" aria-label="Brazilian Lumber"><img src="../assets/logos/brl-logo-white.svg" alt="Brazilian Lumber" width="96" height="30"></a><span class="tag">{I['pin']} {e(b['name'])}</span></div>
    <div class="topbar__count"><span class="label" data-countdown-label>Black Friday ends in</span>{countdown()}</div>
    <a class="topbar__phone" href="tel:{b['tel']}" aria-label="Call {e(b['name'])} showroom {b['phone']}">{I['phone']}<span class="num">{b['phone']}</span></a>
  </div>
</div>
"""


def header():
    return """<header class="header">
  <div class="wrap">
    <span></span>
    <span class="header__badge">Black Friday <b>2026</b> · Nov 13 – Dec 1</span>
  </div>
</header>
"""


def form(b):
    opts = "".join(f'<option value="{v}">{l}</option>' for v, l in b["options"])
    opts += '<option value="multiple">Multiple products / not sure yet</option>'
    return f"""<form class="form-card" id="lead-form" action="#" method="post" novalidate
      data-crm="salesforce-flowsly" data-branch="{b['slug']}">
  <!-- DEV (Nicolas): set action to the Salesforce / Flowsly endpoint. Leads route by the "branch" field. -->
  <h2 id="quote">Lock in your <em>Black Friday</em> price</h2>
  <p class="sub">Get a fast quote from our {e(b['city'])} team. Offers end Dec 1, 11:59 PM {b['tz']}.</p>

  <input type="hidden" name="branch" value="{b['slug']}">
  <input type="hidden" name="campaign" value="black-friday-2026">
  <input type="hidden" name="landing_page" value="">
  <input type="hidden" name="utm_source"><input type="hidden" name="utm_medium"><input type="hidden" name="utm_campaign">
  <input type="hidden" name="utm_term"><input type="hidden" name="utm_content"><input type="hidden" name="gclid"><input type="hidden" name="fbclid">

  <div class="field">
    <label for="full_name">Full name <span class="req">*</span></label>
    <input id="full_name" name="full_name" type="text" autocomplete="name" placeholder="Jane Smith" required>
    <span class="err">Please enter your full name.</span>
  </div>
  <div class="row-2">
    <div class="field">
      <label for="phone">Phone <span class="req">*</span></label>
      <input id="phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" placeholder="(555) 555-5555" required>
      <span class="err">Enter a valid phone number.</span>
    </div>
    <div class="field">
      <label for="email">Email <span class="req">*</span></label>
      <input id="email" name="email" type="email" autocomplete="email" placeholder="you@email.com" required>
      <span class="err">Enter a valid email.</span>
    </div>
  </div>
  <div class="row-2">
    <div class="field">
      <label for="role">I am a <span class="req">*</span></label>
      <select id="role" name="role" required>
        <option value="" disabled selected>Select role</option>
        <option value="contractor">Contractor</option>
        <option value="architect-designer">Architect / Designer</option>
        <option value="homeowner">Homeowner</option>
      </select>
      <span class="err">Select your role.</span>
    </div>
    <div class="field">
      <label for="approx_sf">Approx. SF <span class="req">*</span></label>
      <input id="approx_sf" name="approx_sf" type="number" min="1" inputmode="numeric" placeholder="e.g. 600" required>
      <span class="err">Enter approximate square feet.</span>
    </div>
  </div>
  <div class="field">
    <label for="product_interest">Product of interest <span class="req">*</span></label>
    <select id="product_interest" name="product_interest" required>
      <option value="" disabled selected>Choose a Black Friday product</option>
      {opts}
    </select>
    <span class="err">Choose a product.</span>
  </div>
  <button class="btn btn--block btn--lg" type="submit">Get my Black Friday quote {I['arrow']}</button>
  <p class="form-note">By submitting, you agree to be contacted by Brazilian Lumber about your request. No spam.</p>
  <div class="form-alt">Prefer to talk? <a href="tel:{b['tel']}">{I['phone']} {b['phone']}</a></div>
</form>
"""


def hero(b):
    return f"""<section class="hero" id="top">
  <h1 class="sr-only">{b['h1']}</h1>
  <div class="hero__media">
    <picture>
      <source media="(max-width: 760px)" srcset="../assets/img/{b['slug']}-mobile.jpg">
      <img src="../assets/img/{b['slug']}-desktop.jpg" alt="{e(b['banner_alt'])}" width="2401" height="1201" fetchpriority="high">
    </picture>
    <a class="hero__link" href="#quote" aria-label="Get it now: request your Black Friday quote" tabindex="-1"></a>
  </div>
  <div class="wrap hero__inner">
    {form(b)}
  </div>
</section>
"""


def ticker(b):
    items = "".join(f'<span class="ticker__item">{t}</span>' for t in b["ticker"])
    return f'<div class="ticker" aria-hidden="true"><div class="ticker__track">{items}{items}{items}{items}</div></div>\n'


def deals_index(b):
    tiles = ""
    for href, num, unit, kicker, name, sub, flag in b["index"]:
        unit_html = f"<small>{unit}</small>" if unit else ""
        flag_html = f'<span class="flag">{flag}</span>' if flag else f'<span class="deal-tile__kicker">{kicker}</span>'
        tiles += f"""<a class="deal-tile reveal" href="{href}">
      <div class="deal-tile__top">{flag_html}<span class="deal-tile__arrow">{I['arrow']}</span></div>
      <div><div class="deal-tile__num display">{num}{unit_html}</div>
      <div class="deal-tile__name">{name}<span>{sub}</span></div></div>
    </a>"""
    return f"""<section class="section" id="deals" style="padding-top: clamp(72px, 9vw, 110px)">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Black Friday at {e(b['name'])}</span>
      <h2 class="h2 display">The bigger the project.<br><em>The bigger the savings.</em></h2>
      <p class="lead">Build bigger, spend smarter. Every deal below is available at our {e(b['city'])} showroom &amp; yard, Nov 13 – Dec 1.</p>
    </div>
    <div class="deals-index">{tiles}</div>
  </div>
</section>
"""


def tier_block(blk, media_html):
    src, alt, cls = blk["logo"]
    tiers_attr = str(blk["tiers"]).replace(" ", "")
    steps = "".join(f'<div class="step"><div class="step__pct display">{p}<small>%</small></div><div class="step__min">${a // 1000}K+ order</div></div>'
                    for a, p in blk["tiers"])
    items = "".join(f"<li>{I['check']}<span>{t}<small>{s}</small></span></li>" for t, s in blk["items"])
    fine = f'<p class="fine">{blk["fine"]}</p>' if blk.get("fine") else ""
    lo, hi = blk["tiers"][0][1], blk["tiers"][-1][1]
    return f"""<article class="tier-block reveal" id="{blk['id']}" data-estimator data-tiers="{tiers_attr}">
    <div class="tier-block__media">
      {media_html}
      <span class="flag">{blk['flag']}</span>
      <img class="tier-block__logo {cls}" src="{src}" alt="{alt}">
    </div>
    <div class="tier-block__body">
      <span class="eyebrow">{lo}% – {hi}% OFF by order size</span>
      <h3 class="tier-block__title">{blk['title']}</h3>
      <p class="tier-block__tagline">{blk['tagline']}</p>
      <ul class="prod-list">{items}</ul>
      <div class="ladder">{steps}</div>
      <div class="estimator">
        <div class="estimator__label"><span>Your project total</span><output data-out="total">$3,000</output></div>
        <input type="range" min="500" max="10000" step="250" value="3000" aria-label="Estimated project total for {alt}">
        <div class="estimator__result"><b data-out="pct"></b><span data-out="save"></span></div>
      </div>
      {fine}
      <a class="btn btn--block" href="#quote" data-product="{blk['product']}">Get my {alt} quote {I['arrow']}</a>
    </div>
  </article>"""


def tiers_section(b):
    dkt = b["dkt"]
    dkt_media = f'<div class="tier-block__photo"><img src="{dkt["img"]}" alt="" loading="lazy"></div>'
    w1, w2 = PW_BLOCK["wood"]
    pw_media = f'<div class="wood wood--planks" style="--w1:{w1};--w2:{w2}"></div>'
    return f"""<section class="section" style="padding-top: 0">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Volume discounts</span>
      <h2 class="h2 display">Spend more. <em>Save more.</em></h2>
      <p class="lead">Hit the next tier and the discount applies to your full qualifying order, trims, corners and finishing profiles included. Tiers are calculated before discount, taxes and freight.</p>
    </div>
    <div class="tiers">
      {tier_block(dkt, dkt_media)}
      {tier_block(PW_BLOCK, pw_media)}
    </div>
  </div>
</section>
"""


def easy_oil(b):
    if not b["easy_oil"]:
        return ""
    li = "".join(f"<li>{I['check']}{t}</li>" for t in (
        "1 FREE gallon for every ~250 SF", "On natural wood orders over $750",
        "Open to all customers", "Cannot be combined with other promotions"))
    return f"""<section class="section" id="easy-oil" style="padding-top: 0">
  <div class="wrap">
    <div class="exclusive reveal">
      <div>
        <span class="flag flag--white">Miami exclusive</span>
        <h3 class="display">The bigger the wood order, <em>the more FREE Easy Oil.</em></h3>
        <p>Protect your new hardwood from day one. Order natural wood at our Miami HQ and we'll add Easy Oil hardwood finish to your order, on us.</p>
        <ul>{li}</ul>
        <a class="btn btn--lg" style="background:#fff;color:var(--ink)" href="#quote" data-product="easy-oil">Claim my free Easy Oil {I['arrow']}</a>
      </div>
      <div class="oil-calc" data-oil>
        <h4>How much do you get?</h4>
        <div class="oil-calc__out">
          <span class="oil-calc__num display" data-out="gal">2</span>
          <span class="oil-calc__unit">FREE gallons<span>for <b data-out="sf">500 SF</b> of natural wood</span></span>
        </div>
        <input type="range" min="250" max="5000" step="50" value="500" aria-label="Project size in square feet">
        <div class="scale"><span>250 SF</span><span>5,000 SF</span></div>
        <div class="cans" aria-hidden="true"></div>
      </div>
    </div>
  </div>
</section>
"""


def clearance(b):
    cards = ""
    for c in b["clearance"]:
        w1, w2 = c["wood"]
        prices = "".join(f"""<div class="price"><span class="price__name">{n}</span>
          <span><span class="price__now">{now}<small>{u}</small></span><span class="price__was">{was}</span></span></div>""" for n, now, u, was in c["prices"])
        notes = "".join(f"<li>{n}</li>" for n in c["notes"])
        flag_cls = "flag" if "only" in c["flag"] else "flag flag--outline"
        cards += f"""<article class="c-card reveal" id="{c['id']}">
      <div class="c-card__visual">
        <div class="wood {c['texture']}" style="--w1:{w1};--w2:{w2}"></div>
        <span class="{flag_cls}">{c['flag']}</span>
        <div class="c-card__pct"><div><b>{c['pct']}</b><small>{c['pct_small']}</small></div></div>
        <span class="c-card__species">{c['species']}</span>
      </div>
      <div class="c-card__body">
        <h3 class="c-card__title">{c['title']}</h3>
        <p class="c-card__tag">{c['tag']}</p>
        <div class="price-rows">{prices}</div>
        <ul>{notes}</ul>
        <a class="btn btn--ghost btn--block" href="#quote" data-product="{c['product']}">Reserve before it's gone</a>
      </div>
    </article>"""
    return f"""<section class="section" id="clearance" style="padding-top: 0">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Clearance · while local stock lasts</span>
      <h2 class="h2 display">Clearance prices. <em>Final sale.</em></h2>
      <p class="lead">Limited quantities at our {e(b['city'])} warehouse. When it's gone, it's gone.</p>
    </div>
    <div class="clearance-grid">{cards}</div>
  </div>
</section>
"""


def matrix(b):
    cls = {"dkt": "line--dkt", "pw": "line--pw", "clr": "line--clr", "exc": "line--exc"}
    rows = ""
    for k, line, name, spec, sku, deal, dsub, avail in b["matrix"]:
        rows += f"""<tr>
        <td data-label="Product"><span class="line {cls[k]}">{line}</span><span class="pname">{name}</span><span class="avail">{spec}</span></td>
        <td data-label="SKU / unit"><span class="sku">{sku}</span></td>
        <td data-label="Black Friday deal"><span class="deal">{deal}<small>{dsub}</small></span></td>
        <td data-label="Availability"><span class="avail">{avail}</span></td>
      </tr>"""
    return f"""<section class="section" id="products" style="padding-top: 0">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Product matrix · {e(b['name'])}</span>
      <h2 class="h2 display">Every deal. <em>One list.</em></h2>
      <p class="lead">Only products and promotions available at the {e(b['city'])} branch are shown.</p>
    </div>
    <div class="reveal">
      <table class="matrix">
        <thead><tr><th>Product</th><th>SKU / unit</th><th>Black Friday deal</th><th>Availability</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
  </div>
</section>
"""


def why():
    items = [("2,000+", "SKUs in stock", "Hardwoods, cladding, decking, hardware and finishes."),
             ("24h", "Quote to delivery", "Fast turnaround so your crew keeps building."),
             ("Direct", "Importer advantage", "Sourced at origin, priced without the middlemen."),
             ("3", "Warehouses + showrooms", "Miami · New Jersey · Los Angeles.")]
    html = "".join(f"""<div class="why__item reveal"><div class="why__num display">{n}</div><div class="why__label">{l}</div><div class="why__desc">{d}</div></div>""" for n, l, d in items)
    return f"""<section class="section" style="padding-top: 0">
  <div class="wrap"><div class="why">{html}</div></div>
</section>
"""


def showroom(b):
    q = f"{b['addr1']}, {b['addr2']}".replace(" ", "+")
    hours = "".join(f"<dt>{d}</dt><dd>{h}</dd>" for d, h in b["hours"])
    return f"""<section class="section" id="showroom" style="padding-top: 0">
  <div class="wrap">
    <div class="showroom reveal">
      <div class="showroom__map">
        <iframe title="Map: Brazilian Lumber {e(b['name'])}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
          src="https://maps.google.com/maps?q={q}&amp;z=15&amp;output=embed"></iframe>
      </div>
      <div class="showroom__info">
        <div>
          <span class="eyebrow">Showroom &amp; yard</span>
          <h3 class="display">Visit {e(b['name'])}</h3>
        </div>
        <div class="info-row">{I['pin']}<div><strong>Warehouse address</strong>{b['addr1']}<br>{b['addr2']}</div></div>
        <div class="info-row">{I['phone']}<div><strong>Direct line</strong><a class="big" href="tel:{b['tel']}">{b['phone']}</a></div></div>
        <div class="info-row">{I['clock']}<div><strong>Hours</strong><dl class="hours">{hours}</dl></div></div>
        <div class="showroom__ctas">
          <a class="btn" href="https://www.google.com/maps/dir/?api=1&amp;destination={q}" target="_blank" rel="noopener">{I['nav']} Get directions</a>
          <a class="btn btn--ghost" href="tel:{b['tel']}">{I['phone']} Call now</a>
        </div>
      </div>
    </div>
  </div>
</section>
"""


def final_cta(b):
    return f"""<section class="section final">
  <div class="final__bg"><img src="../assets/img/{b['slug']}-desktop.jpg" alt="" loading="lazy"></div>
  <div class="wrap reveal">
    <span class="eyebrow" data-countdown-label>Black Friday ends Dec 1 · 11:59 PM {b['tz']}</span>
    <h2 class="display">Build bigger.<em>Spend smarter.</em></h2>
    <div class="final__count">{countdown()}</div>
    <p>Lock in your Black Friday pricing at Brazilian Lumber {e(b['city'])} before the clock runs out.</p>
    <div class="final__ctas">
      <a class="btn btn--lg" href="#quote">Get my quote {I['arrow']}</a>
      <a class="btn btn--lg btn--ghost" href="tel:{b['tel']}">{I['phone']} {b['phone']}</a>
    </div>
  </div>
</section>
"""


def footer(b):
    return f"""<footer class="footer">
  <div class="wrap">
    <div class="footer__top">
      <img src="../assets/logos/brl-logo-white.svg" alt="Brazilian Lumber" width="128" height="40">
      <div class="footer__contact">
        <span>{b['addr1']}, {b['addr2']}</span>
        <a href="tel:{b['tel']}">{b['phone']}</a>
        <a href="https://{b['domain']}" target="_blank" rel="noopener">{b['domain']}</a>
      </div>
    </div>
    <div class="legal">
      <strong>Promotional terms</strong>
      <p>{LEGAL}</p>
    </div>
    <div class="copy">© 2026 Brazilian Lumber. All rights reserved.</div>
  </div>
</footer>
"""


def mbar(b):
    return f"""<div class="mbar">
  <a class="btn btn--ghost" href="tel:{b['tel']}">{I['phone']} Call</a>
  <a class="btn" href="#quote">Get quote</a>
</div>
"""


def page(b):
    title = f"Black Friday 2026 · Brazilian Lumber {b['city']} · Up to 20% OFF"
    desc = f"Build bigger, spend smarter. Black Friday at Brazilian Lumber {b['city']}: Nov 13 – Dec 1, 2026. Volume discounts on Deckotech and Platinum Woods plus clearance deals."
    return (head(b, e(title), e(desc))
            + f'<body data-branch="{b["slug"]}" data-deadline="{b["deadline"]}">\n'
            + topbar(b) + header() + "<main>\n" + hero(b) + ticker(b) + deals_index(b)
            + tiers_section(b) + easy_oil(b) + clearance(b) + matrix(b) + why()
            + showroom(b) + final_cta(b) + "</main>\n" + footer(b) + mbar(b)
            + '<script src="../assets/js/bf.js" defer></script>\n</body>\n</html>\n')


def thank_you(b):
    title = f"Thank you · Black Friday · Brazilian Lumber {b['city']}"
    return (head(b, e(title), "Your Black Friday quote request was received.")
            + f'<body data-branch="{b["slug"]}" data-deadline="{b["deadline"]}">\n'
            + "<!-- TRACKING (Manuel): fire Lead / conversion events on this page. -->\n"
            + topbar(b) + header()
            + f"""<main class="ty">
  <div class="ty__bg"><img src="../assets/img/{b['slug']}-desktop.jpg" alt=""></div>
  <div class="wrap ty__card">
    <div class="ty__check">{I['check']}</div>
    <span class="eyebrow">Request received · {e(b['name'])}</span>
    <h1 class="display">Thank you<span data-ty-name></span>. <em>Your Black Friday quote is on its way.</em></h1>
    <p>Our {e(b['city'])} team has your request and will reach out shortly. <!-- TBD: response-time promise --> Want it even faster? Give us a call.</p>
    <a class="ty__call" href="tel:{b['tel']}"><small>Call {e(b['name'])} for a faster quote</small><b>{b['phone']}</b></a>
    <div class="ty__addr">{I['pin']} {b['addr1']}, {b['addr2']} · <a href="https://www.google.com/maps/dir/?api=1&amp;destination={f"{b['addr1']}, {b['addr2']}".replace(' ', '+')}" target="_blank" rel="noopener">Directions</a></div>
    <a class="btn btn--ghost" href="index.html#deals">Back to Black Friday deals</a>
  </div>
</main>
"""
            + footer(b)
            + '<script src="../assets/js/bf.js" defer></script>\n</body>\n</html>\n')


if __name__ == "__main__":
    for b in BRANCHES:
        out = ROOT / b["slug"]
        out.mkdir(exist_ok=True)
        (out / "index.html").write_text(page(b), encoding="utf-8")
        (out / "thank-you.html").write_text(thank_you(b), encoding="utf-8")
        print("built", out)
