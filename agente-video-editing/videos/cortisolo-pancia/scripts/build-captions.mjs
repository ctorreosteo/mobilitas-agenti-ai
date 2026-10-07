// Compila transcript.srt (timing parola-per-parola, tempo SORGENTE)
// in data/captions.json (tempo COMPOSIZIONE), applicando l'EDL.
import { readFileSync, writeFileSync } from "node:fs";

// --- EDL: segmenti tenuti, in secondi sorgente ---
const EDL = [
  { srcIn: 2.8, srcOut: 52.7, compIn: 0.0 },      // apertura -> "E come?"
  { srcIn: 64.48, srcOut: 87.3, compIn: 50.8 },   // ripresa buona -> finale
];

const EMPHASIS = new Set([
  "cortisolo", "dormire", "pancia", "grasso", "viscerale", "sonno",
  "dieta", "silenziosa", "separati", "giorni", "volontà", "grammo",
  "addominale", "stress", "30",
]);

const MAX_WORDS = 3;
const MAX_CHARS = 22;
const TAIL = 0.09;      // coda dopo l'ultima parola del gruppo
const MIN_ON = 0.42;    // permanenza minima a schermo

const toSec = (t) => {
  const [h, m, rest] = t.split(":");
  const [s, ms] = rest.split(",");
  return +h * 3600 + +m * 60 + +s + +ms / 1000;
};

const norm = (w) => w.toLowerCase().replace(/[.,:;?!'"’]/g, "").trim();

// --- parse SRT ---
const raw = readFileSync(new URL("../data/transcript.srt", import.meta.url), "utf8");
const words = [];
for (const block of raw.trim().split(/\n\s*\n/)) {
  const lines = block.split("\n").map((l) => l.trim()).filter(Boolean);
  const tIdx = lines.findIndex((l) => l.includes("-->"));
  if (tIdx < 0) continue;
  const [a, b] = lines[tIdx].split("-->").map((x) => x.trim());
  const text = lines.slice(tIdx + 1).join(" ").trim();
  if (!text) continue;
  words.push({ text, srcStart: toSec(a), srcEnd: toSec(b) });
}

// --- mappa sorgente -> composizione, scarta i tagli ---
const mapped = [];
for (const w of words) {
  const seg = EDL.find((s) => w.srcStart >= s.srcIn - 1e-6 && w.srcStart < s.srcOut);
  if (!seg) continue; // parola dentro un taglio
  const start = w.srcStart - seg.srcIn + seg.compIn;
  const end = Math.min(w.srcEnd, seg.srcOut) - seg.srcIn + seg.compIn;
  mapped.push({ text: w.text, start, end: Math.max(end, start + 0.06), seg: EDL.indexOf(seg) });
}

// --- raggruppa in chunk da 2-3 parole ---
const groups = [];
let cur = [];
const flush = () => { if (cur.length) { groups.push(cur); cur = []; } };

for (let i = 0; i < mapped.length; i++) {
  const w = mapped[i];
  const prev = cur[cur.length - 1];
  // rompi se cambia segmento, se c'è uno stacco, o se il gruppo è pieno
  if (prev && (w.seg !== prev.seg || w.start - prev.end > 0.34)) flush();
  const projected = [...cur, w].map((x) => x.text).join(" ");
  if (cur.length >= MAX_WORDS || (cur.length && projected.length > MAX_CHARS)) flush();
  cur.push(w);
  // chiudi dopo punteggiatura forte
  if (/[.,:;?!]$/.test(w.text)) flush();
}
flush();

// --- costruisci le finestre a schermo ---
const out = groups.map((g, i) => {
  const start = g[0].start;
  let end = g[g.length - 1].end + TAIL;
  if (end - start < MIN_ON) end = start + MIN_ON;
  return {
    id: `cap${String(i).padStart(3, "0")}`,
    start: +start.toFixed(3),
    end: +end.toFixed(3),
    words: g.map((w) => ({
      t: w.text,
      s: +w.start.toFixed(3),
      e: +w.end.toFixed(3),
      hot: EMPHASIS.has(norm(w.text)),
    })),
  };
});

// evita sovrapposizioni: taglia la fine sul successivo
for (let i = 0; i < out.length - 1; i++) {
  if (out[i].end > out[i + 1].start) out[i].end = +(out[i + 1].start - 0.001).toFixed(3);
}

writeFileSync(new URL("../data/captions.json", import.meta.url), JSON.stringify(out, null, 0));

const dur = out[out.length - 1].end;
console.log(`gruppi: ${out.length}  parole: ${mapped.length}  ultima uscita: ${dur.toFixed(2)}s`);
console.log(`durata media gruppo: ${(out.reduce((a, g) => a + (g.end - g.start), 0) / out.length).toFixed(2)}s`);
const longest = out.reduce((a, g) => Math.max(a, g.words.map((w) => w.t).join(" ").length), 0);
console.log(`gruppo più lungo: ${longest} caratteri`);
console.log("primi 6:", out.slice(0, 6).map((g) => `[${g.start}] ${g.words.map((w) => w.t).join(" ")}`).join(" | "));
