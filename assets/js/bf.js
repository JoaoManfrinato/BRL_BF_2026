/* Brazilian Lumber · Black Friday 2026 · shared behaviour */
(function () {
  "use strict";
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var pad = function (n) { return String(n).padStart(2, "0"); };
  var money = function (n) { return "$" + Math.round(n).toLocaleString("en-US"); };

  /* ---------- Countdown ----------
     data-deadline is the UTC instant of Dec 1, 2026 11:59:59 PM local branch time
     (ET = UTC-5 in December, PT = UTC-8). */
  var deadlineAttr = document.body.getAttribute("data-deadline");
  if (deadlineAttr) {
    var deadline = new Date(deadlineAttr).getTime();
    var counters = $$("[data-countdown]");
    var tick = function () {
      var diff = Math.max(0, deadline - Date.now());
      var d = Math.floor(diff / 864e5),
          h = Math.floor(diff / 36e5) % 24,
          m = Math.floor(diff / 6e4) % 60,
          s = Math.floor(diff / 1e3) % 60;
      counters.forEach(function (el) {
        var set = function (k, v) { var n = el.querySelector('[data-u="' + k + '"]'); if (n) n.textContent = pad(v); };
        set("d", d); set("h", h); set("m", m); set("s", s);
      });
      if (diff === 0) {
        $$("[data-countdown-label]").forEach(function (l) { l.textContent = "Black Friday has ended"; });
        clearInterval(timer);
      }
    };
    var timer = setInterval(tick, 1000);
    tick();
  }

  /* ---------- Lead form ---------- */
  var form = $("#lead-form");
  if (form) {
    // Capture UTMs / click IDs for Salesforce · Flowsly attribution
    var params = new URLSearchParams(location.search);
    ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "gclid", "fbclid"].forEach(function (k) {
      var input = form.querySelector('input[name="' + k + '"]');
      if (input && params.get(k)) input.value = params.get(k);
    });
    var lp = form.querySelector('input[name="landing_page"]');
    if (lp) lp.value = location.href.split("?")[0];

    var validators = {
      full_name: function (v) { return v.trim().length >= 2; },
      phone: function (v) { return v.replace(/\D/g, "").length >= 10; },
      email: function (v) { return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()); },
      role: function (v) { return !!v; },
      approx_sf: function (v) { return Number(v) > 0; },
      product_interest: function (v) { return !!v; }
    };
    var check = function (field) {
      var fn = validators[field.name];
      if (!fn) return true;
      var ok = fn(field.value);
      field.closest(".field").classList.toggle("has-error", !ok);
      return ok;
    };
    $$("input, select", form).forEach(function (f) {
      f.addEventListener("blur", function () { if (f.value) check(f); });
      f.addEventListener("input", function () { if (f.closest(".field") && f.closest(".field").classList.contains("has-error")) check(f); });
    });

    // Phone mask (US)
    var phone = form.querySelector('input[name="phone"]');
    if (phone) phone.addEventListener("input", function () {
      var d = phone.value.replace(/\D/g, "").replace(/^1/, "").slice(0, 10);
      var out = d;
      if (d.length > 6) out = "(" + d.slice(0, 3) + ") " + d.slice(3, 6) + "-" + d.slice(6);
      else if (d.length > 3) out = "(" + d.slice(0, 3) + ") " + d.slice(3);
      phone.value = out;
    });

    form.addEventListener("submit", function (e) {
      var ok = true, first = null;
      $$("input, select", form).forEach(function (f) {
        if (!check(f)) { ok = false; first = first || f; }
      });
      if (!ok) { e.preventDefault(); first.focus(); return; }

      // DEV NOTE (Nicolas): replace form action with the Salesforce / Flowsly endpoint.
      // While action is "#", we simulate success and go to the thank-you page.
      if (form.getAttribute("action") === "#") {
        e.preventDefault();
        var btn = form.querySelector('button[type="submit"]');
        btn.disabled = true; btn.textContent = "Sending…";
        var name = (form.full_name.value.trim().split(" ")[0] || "");
        setTimeout(function () { location.href = "thank-you.html?name=" + encodeURIComponent(name); }, 600);
      }
    });
  }

  /* ---------- "Get quote" buttons preselect product ---------- */
  $$("[data-product]").forEach(function (a) {
    a.addEventListener("click", function () {
      var sel = $("#product_interest");
      if (sel) {
        sel.value = a.getAttribute("data-product");
        sel.dispatchEvent(new Event("change"));
      }
      setTimeout(function () { var n = $("#full_name"); if (n) n.focus({ preventScroll: true }); }, 650);
    });
  });

  /* ---------- Tier estimators (one per block, never mixed) ---------- */
  $$("[data-estimator]").forEach(function (block) {
    var tiers = JSON.parse(block.getAttribute("data-tiers")); // [[2000,10],[3000,15],[5000,20]]
    var range = $("input[type=range]", block);
    var outTotal = $("[data-out=total]", block);
    var outPct = $("[data-out=pct]", block);
    var outSave = $("[data-out=save]", block);
    var steps = $$(".step", block);
    var update = function () {
      var v = Number(range.value), pct = 0, idx = -1;
      tiers.forEach(function (t, i) { if (v >= t[0]) { pct = t[1]; idx = i; } });
      outTotal.textContent = money(v) + (v >= Number(range.max) ? "+" : "");
      outPct.textContent = pct ? pct + "% OFF" : "Add " + money(tiers[0][0] - v) + " to unlock " + tiers[0][1] + "%";
      outSave.textContent = pct ? "Save ~" + money(v * pct / 100) : "";
      steps.forEach(function (s, i) { s.classList.toggle("is-active", i === idx); });
    };
    range.addEventListener("input", update);
    update();
  });

  /* ---------- Easy Oil calculator (Miami) ---------- */
  var oil = $("[data-oil]");
  if (oil) {
    var r = $("input[type=range]", oil), num = $("[data-out=gal]", oil), sf = $("[data-out=sf]", oil), cans = $(".cans", oil);
    var draw = function () {
      var v = Number(r.value), g = Math.max(1, Math.floor(v / 250));
      num.textContent = g;
      sf.textContent = v.toLocaleString("en-US") + " SF";
      var have = cans.children.length;
      if (have < g) for (var i = have; i < g; i++) { var c = document.createElement("span"); c.className = "can"; cans.appendChild(c); }
      else while (cans.children.length > g) cans.removeChild(cans.lastChild);
    };
    r.addEventListener("input", draw);
    draw();
  }

  /* ---------- Mobile sticky CTA ---------- */
  var mbar = $(".mbar"), formCard = $(".form-card");
  if (mbar && formCard && "IntersectionObserver" in window) {
    var hero = $(".hero");
    new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { mbar.classList.toggle("is-visible", !en.isIntersecting); });
    }, { threshold: 0 }).observe(hero);
  }

  /* ---------- Reveal on scroll ---------- */
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    $$(".reveal").forEach(function (el) { io.observe(el); });
  } else {
    $$(".reveal").forEach(function (el) { el.classList.add("is-in"); });
  }

  /* ---------- Thank-you personalisation ---------- */
  var tyName = $("[data-ty-name]");
  if (tyName) {
    var n = new URLSearchParams(location.search).get("name");
    if (n) tyName.textContent = ", " + n.replace(/[<>]/g, "").slice(0, 30);
  }
})();
