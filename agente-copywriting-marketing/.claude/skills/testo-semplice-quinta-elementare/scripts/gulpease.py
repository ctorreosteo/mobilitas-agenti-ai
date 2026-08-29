#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Misura la leggibilita di un testo italiano.

Uso:
    python3 gulpease.py testo.txt
    python3 gulpease.py pagina.html          # i tag HTML vengono rimossi
    cat testo.txt | python3 gulpease.py      # da stdin
    python3 gulpease.py a.txt b.txt          # confronto prima/dopo

Indice Gulpease (Lucisano e Piemontese, 1988), l'unico indice di leggibilita
costruito sull'italiano:  89 + (300 * frasi - 10 * lettere) / parole

  80-100  accessibile con la licenza elementare   <- bersaglio quinta elementare
  60-80   accessibile con la licenza media
  40-60   accessibile con un diploma superiore
  < 40    difficile per tutti
"""
import sys, re, io, unicodedata

SOGLIA_FRASE_LUNGA = 25       # parole
SOGLIA_SILLABE = 4            # sillabe stimate
SOGLIA_CARATTERI = 13         # caratteri

# Parole che segnalano registro burocratico, tecnico o astratto.
# Non sono errori: sono candidate alla sostituzione.
SPIE = set("""
effettuare effettuazione provvedere provvedimento usufruire avvalersi ottemperare
adempiere adempimento espletare espletamento recarsi pervenire trasmettere inoltrare
sussistere sussistenza decorrere decorrenza incorrere comportare consentire
qualora laddove ove allorche allorquando altresi nonche pertanto tuttavia ciononostante
conseguentemente successivamente precedentemente antecedentemente eventualmente
mediante tramite attraverso presso entro inerente inerenti relativo relativamente
concernente riguardante afferente attinente
suddetto suddetta predetto predetta summenzionato citato medesimo medesima
tale taluni codesto anzidetto sunnominato
ottimizzare ottimizzazione implementare implementazione efficientamento
massimizzare valorizzazione performante scalabile strutturato personalizzato
metodologia metodologico problematica problematiche criticita tematica tematiche
finalizzato finalita ambito contesto realta processo processi soluzione soluzioni
sinergia sinergie approccio percorso protocollo modalita tipologia
sintomatologia eziologia patologia patologico distretto rachide algia
cervicalgia lombalgia dorsalgia posturale posturali biomeccanico biomeccanica
propriocettivo miofasciale articolare articolarita mobilizzazione
""".split())

VOCALI = "aeiouàèéìòóùAEIOUÀÈÉÌÒÓÙ"


def togli_html(t):
    t = re.sub(r'<(script|style|head)[^>]*>.*?</\1>', ' ', t, flags=re.S | re.I)
    t = re.sub(r'<br\s*/?>', '\n', t, flags=re.I)
    t = re.sub(r'</(p|div|td|tr|h[1-6]|li|blockquote)>', '\n', t, flags=re.I)
    t = re.sub(r'<[^>]+>', ' ', t)
    for a, b in [('&nbsp;', ' '), ('&amp;', '&'), ('&quot;', '"'),
                 ('&lt;', '<'), ('&gt;', '>'), ('&#39;', "'")]:
        t = t.replace(a, b)
    return t


def sillabe(parola):
    """Stima le sillabe contando i gruppi di vocali. Approssimata, sufficiente."""
    n, prec = 0, False
    for c in parola:
        v = c in VOCALI
        if v and not prec:
            n += 1
        prec = v
    return max(n, 1)


def senza_accenti(p):
    return ''.join(c for c in unicodedata.normalize('NFD', p)
                   if unicodedata.category(c) != 'Mn')


def frasi(testo):
    """Una frase finisce con . ! ? ; oppure con un a capo (titoli, elenchi)."""
    pezzi = re.split(r'[.!?;]+|\n+', testo)
    return [p.strip() for p in pezzi if len(re.findall(r'\w+', p)) > 0]


def analizza(testo):
    fr = frasi(testo)
    parole = re.findall(r"[\w'àèéìòóùÀÈÉÌÒÓÙ]+", testo, re.UNICODE)
    lettere = sum(1 for c in testo if c.isalnum())
    n_f, n_p = len(fr), len(parole)
    if n_p == 0:
        return None
    g = 89 + (300 * n_f - 10 * lettere) / n_p

    lunghe = []
    for f in fr:
        w = re.findall(r"[\w'àèéìòóùÀÈÉÌÒÓÙ]+", f, re.UNICODE)
        if len(w) > SOGLIA_FRASE_LUNGA:
            lunghe.append((len(w), f))
    lunghe.sort(reverse=True, key=lambda x: x[0])

    diff = {}
    for p in parole:
        pl = p.lower()
        if pl.isdigit():
            continue
        if senza_accenti(pl) in SPIE or sillabe(p) >= SOGLIA_SILLABE or len(p) >= SOGLIA_CARATTERI:
            diff[pl] = diff.get(pl, 0) + 1

    return {
        'gulpease': g, 'frasi': n_f, 'parole': n_p, 'lettere': lettere,
        'media': n_p / n_f,
        'max': max((len(re.findall(r'\w+', f)) for f in fr), default=0),
        'lunghe': lunghe,
        'difficili': sorted(diff.items(), key=lambda x: (-x[1], x[0])),
    }


def livello(g):
    if g >= 80:  return "licenza elementare  <-- bersaglio quinta elementare RAGGIUNTO"
    if g >= 60:  return "licenza media       (sotto il bersaglio: servono ancora ~%d punti)" % (80 - g)
    if g >= 40:  return "diploma superiore   (molto sotto il bersaglio)"
    return "difficile per tutti"


def stampa(nome, a):
    print("=" * 66)
    print(nome)
    print("=" * 66)
    print("  Gulpease ............ %5.1f   %s" % (a['gulpease'], livello(a['gulpease'])))
    print("  Parole .............. %5d" % a['parole'])
    print("  Frasi ............... %5d" % a['frasi'])
    print("  Parole per frase .... %5.1f   (bersaglio 12-15)" % a['media'])
    print("  Frase piu lunga ..... %5d parole   (max consigliato %d)" % (a['max'], SOGLIA_FRASE_LUNGA))

    if a['lunghe']:
        print("\n  FRASI DA SPEZZARE (%d):" % len(a['lunghe']))
        for n, f in a['lunghe'][:8]:
            print("   [%3d parole] %s" % (n, (f[:100] + '...') if len(f) > 100 else f))
        if len(a['lunghe']) > 8:
            print("   ... e altre %d" % (len(a['lunghe']) - 8))

    if a['difficili']:
        print("\n  PAROLE CANDIDATE ALLA SOSTITUZIONE (%d diverse):" % len(a['difficili']))
        riga = []
        for p, n in a['difficili'][:30]:
            riga.append("%s%s" % (p, ("x%d" % n) if n > 1 else ""))
        print("   " + ", ".join(riga))
        if len(a['difficili']) > 30:
            print("   ... e altre %d" % (len(a['difficili']) - 30))
    print()


def leggi(percorso):
    t = io.open(percorso, encoding='utf-8', errors='replace').read()
    if percorso.lower().endswith(('.html', '.htm')) or '<html' in t[:2000].lower():
        t = togli_html(t)
    return t


def main():
    arg = sys.argv[1:]
    if not arg:
        stampa("stdin", analizza(sys.stdin.read()))
        return
    risultati = []
    for p in arg:
        a = analizza(leggi(p))
        if a is None:
            print("%s: nessun testo" % p); continue
        stampa(p, a)
        risultati.append((p, a))
    if len(risultati) == 2:
        (n1, a1), (n2, a2) = risultati
        print("=" * 66)
        print("CONFRONTO")
        print("=" * 66)
        print("  %-22s %10s %10s %10s" % ("", "prima", "dopo", "delta"))
        for et, ch, fmt in [("Gulpease", 'gulpease', "%.1f"),
                            ("Parole per frase", 'media', "%.1f"),
                            ("Frase piu lunga", 'max', "%.0f"),
                            ("Parole totali", 'parole', "%.0f")]:
            v1, v2 = a1[ch], a2[ch]
            print(("  %-22s " + fmt + "  " + fmt + "  %+.1f") % (et, v1, v2, v2 - v1))
        d = a2['parole'] - a1['parole']
        if d < -a1['parole'] * 0.05:
            print("\n  ATTENZIONE: il testo si e accorciato del %.0f%%." % (-100.0 * d / a1['parole']))
            print("  Semplificare non vuol dire accorciare: controlla di non aver tagliato informazioni.")
        print()


if __name__ == '__main__':
    main()
