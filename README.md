# Black Friday 2026 · Landing Pages (Brazilian Lumber)

Three geo-targeted LPs built from one template: same layout and structure, only branch data changes.
Brief: `[CMP] Web_Design_&_Paid_Media_Brief_Black_Friday_2026` (V5). Live window: Nov 13 – Dec 1, 2026.

## Files
```
miami/        index.html · thank-you.html
new-jersey/   index.html · thank-you.html
los-angeles/  index.html · thank-you.html
assets/       css/bf.css · js/bf.js · img/ (campaign banners) · logos/ · fonts/ (Archivo variable)
build.py      generator: edit branch data here, then run `python3 build.py`
```
Edit content in `build.py` (the BRANCHES list), not in the generated HTML, so the three pages stay in sync.

## Page structure (all three)
1. Sticky top bar: branch, countdown to Dec 1 11:59 PM local (ET for Miami/NJ, PT for LA), local phone
2. Hero: campaign banner (desktop 2:1 / mobile vertical) + lead form
3. Deal ticker + discount highlights (anchor tiles)
4. Tiered volume blocks, kept separate: Deckotech (10/15/20%) and Platinum Woods Cumaru & Garapa (5/7/10%), each with its own savings estimator
5. Miami only: FREE Easy Oil band with gallons calculator
6. Clearance cards (Cypress #2 Miami only · Ferretti · B-Grade Deck Tiles)
7. Branch product matrix (only that branch's products/SKUs)
8. Why BRL · Showroom & yard (map, address, phone, hours, directions) · Final CTA
9. Legal disclaimer footer (verbatim from brief)
10. Thank-you page: confirmation, branch phone + address, "call for a faster quote"

## Handoff
- **Luis (build):** relative paths; deploy each branch folder with `assets/` one level up, or adjust paths.
- **Nicolas (Salesforce / Flowsly):** form `#lead-form` has `action="#"` (demo: redirects to thank-you). Set the real endpoint. Fields: `full_name, phone, email, role, approx_sf, product_interest`, plus hidden `branch, campaign, landing_page, utm_*, gclid, fbclid` (auto-filled from the URL). Route leads by `branch`.
- **Manuel (tracking):** placeholders `<!-- TRACKING -->` in each `<head>`; fire the Lead conversion on `thank-you.html`.

## Open points for Laura's approval
- **Phone numbers:** the LPs use the brief's numbers (Miami 954.404.8011 · NJ (732) 708-6256 · LA (323) 289-2647). The company vault lists different ones: (954) 287-0816 · (908) 388-4434 · (323) 990-7871. Confirm which are the campaign numbers.
- **NJ Deckotech SKUs:** the brief lists SKUs only for Miami. NJ shows the same SKUs (1616DEASW, 1616DECLSLPRSG) for the same products. Confirm.
- **LA Deckotech:** the brief gives no SKUs, so the matrix shows stock counts (295 / 349 pcs).
- **Thank-you response time:** TBD in the brief; the copy currently says "will reach out shortly".
- **Product photos:** Platinum Woods, Cypress, Ferretti and Deck Tiles cards use CSS wood-texture placeholders. Swap in the photos from the campaign deck (the Google Slides deck wasn't accessible here).
- **Hours** come from the company vault (Miami Mon–Fri 8–5, Sat 8–1; NJ & LA Mon–Fri 8–5).
