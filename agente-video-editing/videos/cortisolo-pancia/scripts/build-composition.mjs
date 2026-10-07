// Genera index.html dalla design spec + data/captions.json.
// Rigenerabile: `node scripts/build-composition.mjs`
import { readFileSync, writeFileSync } from "node:fs";

const caps = JSON.parse(readFileSync(new URL("../data/captions.json", import.meta.url), "utf8"));

// ---- EDL / timeline ----
const A = { start: 0, dur: 49.9, mediaStart: 2.8 };
const B = { start: 50.8, dur: 22.82, mediaStart: 64.48 };
const TOTAL = 77.7;
const SRC = "assets/source-4k.mp4";

// Elementi che richiedono dati di brand reali (nome in sovrimpressione, nome studio).
// false -> emessi con data-hidden: nascosti in preview E render, in modo reversibile.
// Per riattivarli: metti true, rigenera, e passa i valori con --variables.
const SHOW_BRAND = false;
const HIDE = SHOW_BRAND ? "" : " data-hidden";

const GRADE = JSON.stringify({
  adjust: { contrast: 0.06, shadows: 0.1, vibrance: 0.1, temperature: 0.03 },
  details: { vignette: 0.18, vignetteFeather: 0.7, grain: 0.04, grainSize: 0.3 },
});

const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

// ---- sottotitoli: una sub-composizione per sezione narrativa ----
// I 89 gruppi NON sono clip: sono wrapper non temporizzati dentro la finestra
// della sub-composizione, accesi e spenti via autoAlpha sulla timeline (l'unica
// eccezione di visibilità ammessa da determinism-rules per elementi non-clip).
const SPLITS = [22.6, 49.5];                       // confini di sezione (tempo composizione)
const SECTIONS = [
  { id: "caps-problema", label: "il problema" },
  { id: "caps-perche", label: "il perché" },
  { id: "caps-caso", label: "il caso clinico" },
];

SECTIONS.forEach((s) => (s.groups = []));
for (const g of caps) {
  SECTIONS[g.start < SPLITS[0] ? 0 : g.start < SPLITS[1] ? 1 : 2].groups.push(g);
}

// finestre contigue e non sovrapposte sulla stessa traccia
SECTIONS.forEach((c, i) => {
  c.start = i === 0 ? 0 : +(c.groups[0].start - 0.15).toFixed(3);
});
SECTIONS.forEach((c, i) => {
  c.end =
    i === SECTIONS.length - 1
      ? +(c.groups[c.groups.length - 1].end + 0.2).toFixed(3)
      : +(SECTIONS[i + 1].start - 0.001).toFixed(3);
});

function subComposition(c) {
  const body = c.groups
    .map((g) => {
      const words = g.words
        .map((w, i) =>
          `<span class="w${w.hot ? " hot" : ""}" id="${g.id}w${i}" data-s="${(w.s - c.start).toFixed(3)}" data-e="${(w.e - c.start).toFixed(3)}">${esc(w.t)}</span>`)
        .join("");
      return `        <div class="cap" id="${g.id}" data-in="${(g.start - c.start).toFixed(3)}" data-out="${(g.end - c.start).toFixed(3)}"><div class="cap-in">${words}</div></div>`;
    })
    .join("\n");

  return `<!doctype html>
<html lang="it">
<head><meta charset="UTF-8" /><title>Sottotitoli — ${c.label}</title></head>
<body>
  <template>
    <style>
      /* la radice si stila sempre via #root: lo scoper CSS scarta una classe sulla radice */
      #root { position:absolute; inset:0; width:3840px; height:2160px;
        --mint:var(--accent, #72FB93); --paper:#EDF3F0; }
      .rail { position:absolute; left:5%; right:5%; bottom:224px; height:0; }
      .cap { position:absolute; left:0; right:0; bottom:0; display:flex;
        justify-content:center; opacity:0; visibility:hidden; }
      .cap-in { display:flex; align-items:baseline; gap:42px; max-width:100%;
        padding:30px 60px 40px; border-radius:30px; background:rgba(0,19,42,.66);
        box-shadow:0 22px 70px rgba(0,10,25,.46); }
      .w { display:inline-block; font-family:Montserrat, sans-serif; font-weight:900;
        font-size:132px; line-height:1; letter-spacing:-.03em; color:var(--paper);
        transform-origin:50% 72%; text-shadow:0 6px 24px rgba(0,12,28,.55); }
      .w.hot { color:var(--mint); font-size:148px; }
    </style>

    <div id="root" data-composition-id="${c.id}" data-width="3840" data-height="2160">
      <div class="rail">
${body}
      </div>
    </div>

    <script>
      (function () {
        var scope = document.querySelector('[data-composition-id="${c.id}"]');
        var MINT = "#72FB93", PAPER = "#EDF3F0", HOT_ON = "#C7FFDA";
        var tl = gsap.timeline({ paused: true });
        var groups = scope.querySelectorAll(".cap");
        for (var i = 0; i < groups.length; i++) {
          var g = groups[i];
          var gin = parseFloat(g.getAttribute("data-in"));
          var gout = parseFloat(g.getAttribute("data-out"));
          tl.fromTo("#" + g.id,
            { autoAlpha: 0, y: 26 },
            { autoAlpha: 1, y: 0, duration: 0.16, ease: "power2.out" }, gin);
          tl.set("#" + g.id, { autoAlpha: 0 }, gout);
          var ws = g.querySelectorAll(".w");
          for (var j = 0; j < ws.length; j++) {
            var w = ws[j], hot = w.classList.contains("hot");
            tl.to("#" + w.id, { color: hot ? HOT_ON : MINT, scale: hot ? 1.10 : 1.06,
              duration: 0.09, ease: "power1.out" }, parseFloat(w.getAttribute("data-s")));
            tl.to("#" + w.id, { color: hot ? MINT : PAPER, scale: 1,
              duration: 0.13, ease: "power1.inOut" }, parseFloat(w.getAttribute("data-e")));
          }
        }
        window.__timelines = window.__timelines || {};
        window.__timelines["${c.id}"] = tl;
      })();
    <\/script>
  </template>
</body>
</html>
`;
}

const capHosts = SECTIONS
  .map((c) => {
    writeFileSync(new URL(`../compositions/${c.id}.html`, import.meta.url), subComposition(c));
    return `    <div id="host-${c.id}" data-composition-id="${c.id}"
         data-composition-src="compositions/${c.id}.html"
         data-start="${c.start}" data-duration="${+(c.end - c.start).toFixed(3)}" data-track-index="6"
         data-width="3840" data-height="2160"></div>`;
  })
  .join("\n");

// ---- freccia menta come SVG (niente glifi unicode non garantiti) ----
const arrowDown = `<svg class="arw" viewBox="0 0 40 64" aria-hidden="true"><path d="M20 0v46M20 62 4 40M20 62l16-22" fill="none" stroke="currentColor" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
const arrowUp = `<svg class="arw-in" viewBox="0 0 40 52" aria-hidden="true"><path d="M20 52V8M20 2 6 24M20 2l14 22" fill="none" stroke="currentColor" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/></svg>`;

const html = `<!doctype html>
<html lang="it" data-composition-variables='[
  {"id":"accent","type":"color","label":"Colore accento","default":"#72FB93"},
  {"id":"speakerName","type":"string","label":"Nome in sovrimpressione","default":"IL TUO NOME"},
  {"id":"speakerRole","type":"string","label":"Ruolo","default":"Osteopata D.O."},
  {"id":"brandName","type":"string","label":"Nome studio (closing)","default":"IL TUO STUDIO"},
  {"id":"ctaText","type":"string","label":"Call to action","default":"Iscriviti per il prossimo caso clinico"}
]'>
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=3840, height=2160" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"><\/script>
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  html, body { width:3840px; height:2160px; overflow:hidden; background:#001730; }
  body { font-family:Montserrat, sans-serif; }

  #root { position:relative; width:3840px; height:2160px; overflow:hidden;
    --navy:#002552; --navy-deep:#001730; --mint:var(--accent, #72FB93);
    --paper:#EDF3F0; --muted:#8FA8BE; }

  /* fondo pieno su un figlio full-bleed, mai sulla root */
  .bgfill { position:absolute; inset:0; background:var(--navy-deep); }

  /* ---- girato ---- */
  .stage { position:absolute; inset:0; overflow:hidden; }
  .stage video { width:100%; height:100%; object-fit:cover; display:block; }

  /* ---- decorativi ambientali ---- */
  .vignette { position:absolute; inset:0; pointer-events:none;
    background:radial-gradient(120% 88% at 42% 44%, rgba(0,12,28,0) 38%, rgba(0,12,28,0.30) 74%, rgba(0,12,28,0.62) 100%); }
  .btmscrim { position:absolute; left:0; right:0; bottom:0; height:760px; pointer-events:none;
    background:linear-gradient(to top, rgba(0,20,42,0.72) 0%, rgba(0,20,42,0.34) 42%, rgba(0,20,42,0) 100%); }
  .hairline { position:absolute; left:0; right:0; top:0; height:6px; background:var(--mint); opacity:.55; }

  /* ---- progress ---- */
  .progress { position:absolute; left:0; bottom:0; width:100%; height:12px;
    background:var(--mint); transform-origin:0% 50%; }
  .progress-bed { position:absolute; left:0; bottom:0; width:100%; height:12px; background:rgba(237,243,240,.16); }

  /* ---- card nel terzo destro ---- */
  .card { position:absolute; right:5%; top:340px; width:1280px; }
  .card-in { background:rgba(0,25,54,.90); border-radius:34px; padding:64px 68px 72px;
    box-shadow:0 34px 110px rgba(0,8,22,.55); }
  .eyebrow { font-family:"IBM Plex Mono", monospace; font-weight:700; font-size:34px;
    letter-spacing:.24em; color:var(--mint); }
  .eyerule { width:120px; height:6px; background:var(--mint); margin:22px 0 40px; border-radius:3px; }
  .c-line { font-weight:900; font-size:96px; line-height:1.02; letter-spacing:-.035em; color:var(--paper); }
  .c-line.hi { color:var(--mint); }
  .c-sub { font-weight:700; font-size:46px; line-height:1.24; letter-spacing:-.01em; color:var(--muted); margin-top:30px; }
  .arw { display:block; width:52px; height:82px; color:var(--mint); margin:26px 0 26px 6px; }
  .arw-in { display:inline-block; width:38px; height:50px; color:var(--mint); vertical-align:-4px; margin-left:14px; }

  .chips { display:flex; align-items:center; gap:30px; }
  .chip { flex:1; text-align:center; font-weight:900; font-size:72px; letter-spacing:-.03em;
    color:var(--paper); border:6px solid rgba(237,243,240,.28); border-radius:24px; padding:26px 10px; }
  .split { width:8px; height:120px; background:repeating-linear-gradient(to bottom, var(--mint) 0 16px, transparent 16px 32px); }

  .bignum { font-weight:900; font-size:210px; line-height:1.06; letter-spacing:-.05em; color:var(--mint); }
  .bigunit { font-weight:900; font-size:86px; line-height:1.14; letter-spacing:-.03em; color:var(--paper); margin-top:14px; }

  /* ---- lockup apertura ---- */
  .hook { position:absolute; right:5%; top:300px; width:1420px; text-align:right; }
  .hook .l { font-weight:900; font-size:118px; line-height:1.04; letter-spacing:-.04em; color:var(--paper);
    text-shadow:0 10px 40px rgba(0,10,25,.7); }
  .hook .l.hi { color:var(--mint); }
  .hook .eyebrow { margin-bottom:26px; }

  /* ---- chip identità ---- */
  .ident { position:absolute; left:5%; top:180px; }
  .ident-in { background:rgba(0,25,54,.90); border-radius:26px; padding:38px 54px 42px;
    box-shadow:0 26px 80px rgba(0,8,22,.5); }
  .ident .nm { font-weight:900; font-size:64px; letter-spacing:-.02em; color:var(--paper); }
  .ident .rl { font-family:"IBM Plex Mono", monospace; font-weight:700; font-size:34px;
    letter-spacing:.18em; color:var(--mint); margin-top:16px; }

  /* ---- schede a tutto schermo ---- */
  .full { position:absolute; inset:0; display:flex; flex-direction:column;
    align-items:center; justify-content:center; background:var(--navy); }
  .full .eyebrow { margin-bottom:34px; }
  .full .big { font-weight:900; font-size:300px; line-height:.94; letter-spacing:-.05em; color:var(--paper); }
  .outro-l { font-weight:900; font-size:104px; line-height:1.12; letter-spacing:-.03em;
    color:var(--paper); text-align:center; max-width:2600px; }
  .outro-l.hi { color:var(--mint); }
  .outro-brand { font-weight:900; font-size:132px; letter-spacing:-.03em; color:var(--paper); margin-top:96px; }
  .outro-cta { font-family:"IBM Plex Mono", monospace; font-weight:700; font-size:42px;
    letter-spacing:.2em; color:var(--mint); margin-top:30px; }
  .outro-rule { width:220px; height:8px; background:var(--mint); border-radius:4px; margin:54px 0 0; }
</style>
</head>
<body>
  <div id="root" data-composition-id="main" data-start="0" data-duration="${TOTAL}" data-width="3840" data-height="2160">
    <div class="bgfill"></div>

    <div class="stage" id="stage-a">
      <video id="vid-a" class="clip" src="${SRC}" data-start="${A.start}" data-duration="${A.dur}"
             data-media-start="${A.mediaStart}" data-track-index="0"
             data-color-grading='${GRADE}' muted playsinline></video>
    </div>
    <div class="stage" id="stage-b">
      <video id="vid-b" class="clip" src="${SRC}" data-start="${B.start}" data-duration="${B.dur}"
             data-media-start="${B.mediaStart}" data-track-index="1"
             data-color-grading='${GRADE}' muted playsinline></video>
    </div>

    <audio id="aud-a" src="${SRC}" data-start="${A.start}" data-duration="${A.dur}"
           data-media-start="${A.mediaStart}" data-track-index="10" data-volume="1"></audio>
    <audio id="aud-b" src="${SRC}" data-start="${B.start}" data-duration="${B.dur}"
           data-media-start="${B.mediaStart}" data-track-index="11" data-volume="1"></audio>

    <div class="vignette" id="vig"></div>
    <div class="btmscrim"></div>
    <div class="hairline" id="hair"></div>

    <!-- lockup apertura -->
    <div class="hook clip" id="hook" data-start="0.4" data-duration="4.2" data-track-index="3">
      <div class="hook-in" id="hook-in">
        <div class="eyebrow">DIVULGAZIONE CLINICA</div>
        <div class="l">NON È SOLO</div>
        <div class="l">LA DIETA.</div>
        <div class="l hi">È L'ORARIO</div>
        <div class="l hi">DEL SONNO.</div>
      </div>
    </div>

    <!-- chip identità -->
    <div class="ident clip" id="ident" data-start="6" data-duration="4.5" data-track-index="3"${HIDE}>
      <div class="ident-in" id="ident-in">
        <div class="nm" data-var-text="speakerName">IL TUO NOME</div>
        <div class="rl" data-var-text="speakerRole">Osteopata D.O.</div>
      </div>
    </div>

    <!-- card 1 : meccanismo -->
    <div class="card clip" id="card1" data-start="8.6" data-duration="4.8" data-track-index="4">
      <div class="card-in" id="card1-in">
        <div class="eyebrow">MECCANISMO</div>
        <div class="eyerule"></div>
        <div class="c-line">CORTISOLO${arrowUp}</div>
        ${arrowDown}
        <div class="c-line hi">GRASSO</div>
        <div class="c-line hi">VISCERALE</div>
      </div>
    </div>

    <!-- card 2 : l'errore classico -->
    <div class="card clip" id="card2" data-start="28.5" data-duration="4.6" data-track-index="4">
      <div class="card-in" id="card2-in">
        <div class="eyebrow">L'ERRORE CLASSICO</div>
        <div class="eyerule"></div>
        <div class="chips">
          <div class="chip">DIETA</div>
          <div class="split"></div>
          <div class="chip">CORTISOLO</div>
        </div>
        <div class="c-sub">Per anni trattati come due mondi separati. Non lo sono.</div>
      </div>
    </div>

    <!-- card 3 : caso clinico -->
    <div class="card clip" id="card3" data-start="53.2" data-duration="4.6" data-track-index="4">
      <div class="card-in" id="card3-in">
        <div class="eyebrow">CASO CLINICO</div>
        <div class="eyerule"></div>
        <div class="bignum">30</div>
        <div class="bigunit">GIORNI</div>
        <div class="c-sub">Un solo tassello cambiato: l'orario del sonno.</div>
      </div>
    </div>

${capHosts}

    <!-- stacco sul giunto -->
    <div class="full clip" id="bridge" data-start="49.55" data-duration="1.6" data-track-index="8">
      <div id="bridge-in" style="display:flex; flex-direction:column; align-items:center;">
        <div class="eyebrow">IL METODO</div>
        <div class="big">E COME?</div>
      </div>
    </div>

    <!-- closing -->
    <div class="full clip" id="outro" data-start="73.62" data-duration="4.08" data-track-index="8">
      <div id="outro-in" style="display:flex; flex-direction:column; align-items:center;">
        <div class="outro-l">Il tuo corpo può fare tutto giusto</div>
        <div class="outro-l hi">e remare contro di te.</div>
        <div class="outro-rule"></div>
        ${SHOW_BRAND ? '<div class="outro-brand" data-var-text="brandName">IL TUO STUDIO</div>' : ""}
        <div class="outro-cta" data-var-text="ctaText">Iscriviti per il prossimo caso clinico</div>
      </div>
    </div>


    <div class="progress-bed"></div>
    <div class="progress" id="prog"></div>
  </div>

<script>
  (function () {
    var TOTAL = ${TOTAL};
    var MINT = getComputedStyle(document.getElementById("root")).getPropertyValue("--mint").trim() || "#72FB93";
    var PAPER = "#EDF3F0";
    var HOT_ON = "#C7FFDA";

    var tl = gsap.timeline({ paused: true });

    /* progress bar lineare su tutta la durata */
    tl.fromTo("#prog", { scaleX: 0 }, { scaleX: 1, duration: TOTAL, ease: "none" }, 0);

    /* respiro della vignetta — cicli finiti, mai repeat:-1 */
    var CYCLE = 11;
    tl.fromTo("#vig",
      { opacity: 0.82 },
      { opacity: 1, duration: CYCLE, ease: "sine.inOut", yoyo: true,
        repeat: Math.max(0, Math.floor(TOTAL / CYCLE) - 1) }, 0);
    tl.fromTo("#hair",
      { opacity: 0.40 },
      { opacity: 0.72, duration: 6, ease: "sine.inOut", yoyo: true,
        repeat: Math.max(0, Math.floor(TOTAL / 6) - 1) }, 0);

    /* spinta d'apertura e stacco d'ingresso sulla ripresa buona */
    tl.fromTo("#stage-a", { scale: 1.06 }, { scale: 1, duration: 2.2, ease: "power2.out" }, 0);
    tl.fromTo("#stage-a", { opacity: 0 }, { opacity: 1, duration: 0.40, ease: "power2.out" }, 0);
    tl.fromTo("#stage-b", { scale: 1.12 }, { scale: 1, duration: 0.9, ease: "expo.out" }, ${B.start});

    /* --- schede grafiche --- */
    function panel(sel, at, dur, fromX) {
      tl.fromTo(sel, { opacity: 0, x: fromX, y: 34 },
        { opacity: 1, x: 0, y: 0, duration: 0.42, ease: "expo.out" }, at);
      tl.to(sel, { opacity: 0, y: -26, duration: 0.30, ease: "power2.in" }, at + dur - 0.30);
    }
    panel("#hook-in", 0.4, 4.2, 70);
    panel("#ident-in", 6.0, 4.5, -70);
    panel("#card1-in", 8.6, 4.8, 90);
    panel("#card2-in", 28.5, 4.6, 90);
    panel("#card3-in", 53.2, 4.6, 90);

    /* stacco: dentro secco, fuori secco — copre il giunto 49.90 -> 50.80 */
    tl.fromTo("#bridge", { opacity: 0 }, { opacity: 1, duration: 0.30, ease: "power2.out" }, 49.55);
    tl.fromTo("#bridge-in", { scale: 0.9 }, { scale: 1, duration: 0.55, ease: "expo.out" }, 49.55);
    tl.to("#bridge", { opacity: 0, duration: 0.22, ease: "power2.in" }, 50.8);

    /* closing */
    tl.fromTo("#outro", { opacity: 0 }, { opacity: 1, duration: 0.40, ease: "power2.out" }, 73.62);
    tl.fromTo("#outro-in", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.55, ease: "expo.out" }, 73.62);

    window.__timelines = window.__timelines || {};
    window.__timelines["main"] = tl;
  })();
<\/script>
</body>
</html>
`;

writeFileSync(new URL("../index.html", import.meta.url), html);
console.log(`index.html + ${SECTIONS.length} sub-composizioni — ${caps.length} gruppi (${SECTIONS.map((c) => c.groups.length).join("/")}), durata ${TOTAL}s`);
