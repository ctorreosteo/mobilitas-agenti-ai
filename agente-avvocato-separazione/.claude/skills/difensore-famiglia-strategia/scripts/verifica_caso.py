#!/usr/bin/env python3
"""
Collaudo del FASCICOLO — il cancello sui fatti, prima che diventino un atto.

## Perche' esiste

Gli altri due cancelli guardano il prodotto: `verifica_atto.py` collauda l'atto
finito, `verifica_citazioni.py` collauda cosa si e' perso fra due riscritture.
Nessuno dei due guarda da dove vengono i fatti — e i fatti sono l'unico punto in
cui un modello linguistico inventa con la stessa disinvoltura con cui inventa il
numero di una sentenza.

`caso.json` nasce pieno di `null`, e la sua intestazione lo dice: «un agente che
li trova null deve chiederli, non riempirli». Finche' nessuno lo verificava,
quella frase era un'autodichiarazione. Un modello che deve scrivere un ricorso e
non trova il reddito dell'assistito non si ferma: scrive una cifra verosimile,
perche' la cifra verosimile e' cio' che sa produrre. E una cifra verosimile in un
atto e' peggio di una cifra mancante — la controparte deposita la busta paga e
l'atto perde credibilita' su tutto il resto, esattamente come con una sentenza
inesistente.

Questo script accerta tre cose, e nessuna richiede di capire il caso:

  1. **I campi che quel deliverable pretende ci sono.** Un ricorso senza reddito
     documentato non discute di mantenimento; senza il titolo sulla casa non
     vede arrivare l'art. 337-sexies c.c.
  2. **Il fascicolo non si contraddice.** Le date stanno in ordine, l'eta' del
     minore corrisponde alla data di nascita, i mesi di convivenza dopo il parto
     tornano con le due date che li delimitano.
  3. **Se l'atto e' gia' scritto, i valori che contiene hanno una fonte.** Un
     atto redatto su un fascicolo incompleto contiene numeri e date che non
     vengono da nessuna parte: e' il caso in cui l'invenzione e' gia' avvenuta.

## Cosa NON fa

Non decide se un reddito e' quello vero, se un obiettivo e' realistico, se una
data e' esatta. Verifica che ci siano, che si tengano fra loro e che l'atto non
sia partito prima. Il resto e' giudizio umano, e resta tale: cio' che non puo'
accertare esce come AVVISO, con scritto accanto che va guardato a mano.

Uso:
  verifica_caso.py caso.json [--tipo ricorso|comparsa|memoria|reclamo|istanza|
                                    accordo|penale|strategia]
                   [--atto ATTO.md] [--oggi AAAA-MM-GG]

Uscita: 0 se nessun bloccante, 1 se ce ne sono.
"""

import argparse
import json
import re
import sys
from datetime import date as _date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from riferimenti import date as date_nel_testo
from riferimenti import importi as importi_nel_testo

# ---------------------------------------------------------------------------
# 1. Cosa pretende ciascun deliverable
# ---------------------------------------------------------------------------
# Il percorso e' 'sezione.campo'. Accanto sta il PERCHE': un cancello che dice
# solo "manca un campo" viene aggirato riempiendo il campo con qualcosa.

COMUNI = {
    'assistito.nome': "l'atto va intestato a una persona, non a un ruolo",
    'assistito.residenza': "determina competenza, notifiche e domicilio",
    'controparte.nome': "senza il nome non si notifica",
    'controparte.residenza': "la notifica alla controparte si fa qui",
    'minore.nome': "il minore va identificato in ogni domanda",
    'minore.data_nascita': "l'eta' decide la partita: sotto i 3 anni cambia tutto",
    'relazione.data_cessazione_convivenza': "da qui decorrono i fatti rilevanti",
}

ECONOMICI = {
    'assistito.reddito_annuo_lordo': "senza reddito documentato non si discute di mantenimento",
    'assistito.fonte_reddito': "il rito pretende la documentazione, non l'affermazione",
    'casa.titolo': "proprieta' o locazione cambiano completamente il rischio",
    'casa.intestazione': "se e' sua ed e' stata casa familiare, l'art. 337-sexies c.c. la assegna",
    'casa.e_stata_casa_familiare': "e' il presupposto dell'assegnazione: si accerta prima",
    'casa.chi_la_occupa_oggi': "l'occupazione di fatto e' meta' della decisione",
}

INTRODUTTIVI = {
    **COMUNI, **ECONOMICI,
    'minore.residenza_anagrafica': "radica la competenza territoriale",
    'situazione_attuale.tribunale': "l'ufficio va indicato e la competenza verificata",
    'obiettivi_del_cliente.realistici': "un atto senza obiettivo realistico chiede tutto e ottiene niente",
    'obiettivi_del_cliente.irrinunciabili': "serve sapere cosa NON si baratta prima di trattare",
}

PENDENTI = {
    **COMUNI,
    'situazione_attuale.tribunale': "l'ufficio davanti al quale si deposita",
    'situazione_attuale.rg': "un atto in corso di causa senza numero di ruolo non si deposita",
    'situazione_attuale.fase': "decide quale finestra processuale e' ancora aperta",
}

RICHIESTI = {
    'ricorso': INTRODUTTIVI,
    'comparsa': INTRODUTTIVI,
    'memoria': PENDENTI,
    'istanza': PENDENTI,
    'reclamo': {
        **PENDENTI,
        'situazione_attuale.provvedimenti_gia_emessi':
            "si reclama un provvedimento: senza il provvedimento non c'e' oggetto",
    },
    'accordo': {
        **COMUNI, **ECONOMICI,
        'controparte.reddito_annuo_lordo':
            "una proposta si costruisce sui numeri di entrambi, non su meta'",
        'situazione_attuale.frequentazione_attuale':
            "la progressione si negozia a partire da cio' che c'e' oggi",
        'situazione_attuale.mantenimento_versato_oggi':
            "cio' che gia' si versa e' il pavimento di ogni trattativa",
    },
    'penale': {
        **COMUNI,
        'fronte_penale.denunce_ricevute':
            "la difesa penale ha per oggetto un procedimento: va identificato",
    },
    'strategia': COMUNI,
}

# Un campo puo' essere soddisfatto da un'alternativa: il reddito della madre che
# non lavora non esiste, ma la sua capacita' reddituale e' l'argomento centrale.
ALTERNATIVE = {
    'controparte.reddito_annuo_lordo': 'controparte.capacita_reddituale_potenziale',
}

# I valori che sembrano compilati e non lo sono.
SEGNAPOSTO = re.compile(
    r'^\s*(?:tbd|todo|n\.?/?a|da\s+compilare|da\s+definire|da\s+verificare|'
    r'xxx+|\.\.\.+|\?+|-+|_+)\s*$', re.IGNORECASE)

RE_ISO = re.compile(r'^(\d{4})-(\d{2})-(\d{2})$')
RE_IT = re.compile(r'^(\d{1,2})[/\-.](\d{1,2})[/\-.](\d{4})$')


def leggi_campo(dati, percorso):
    """Torna il valore a 'sezione.campo', o None se manca del tutto."""
    corrente = dati
    for pezzo in percorso.split('.'):
        if not isinstance(corrente, dict) or pezzo not in corrente:
            return None
        corrente = corrente[pezzo]
    return corrente


def vuoto(valore):
    """Un campo e' vuoto se e' null, una lista/stringa vuota o un segnaposto."""
    if valore is None:
        return True
    if isinstance(valore, str):
        return not valore.strip() or bool(SEGNAPOSTO.match(valore))
    if isinstance(valore, (list, dict)):
        return len(valore) == 0
    return False


def a_data(valore):
    """Accetta AAAA-MM-GG e GG/MM/AAAA. Torna None se non e' una data."""
    if not isinstance(valore, str):
        return None
    m = RE_ISO.match(valore.strip())
    if m:
        a, me, g = (int(x) for x in m.groups())
    else:
        m = RE_IT.match(valore.strip())
        if not m:
            return None
        g, me, a = (int(x) for x in m.groups())
    try:
        return _date(a, me, g)
    except ValueError:
        return None


def mesi_fra(prima, dopo):
    return (dopo.year - prima.year) * 12 + (dopo.month - prima.month) - (1 if dopo.day < prima.day else 0)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('caso')
    p.add_argument('--tipo', default='ricorso', choices=sorted(RICHIESTI))
    p.add_argument('--atto', help='se indicato, verifica che l atto non sia stato scritto prima dei fatti')
    p.add_argument('--oggi', help='AAAA-MM-GG, per il controllo dell eta (default: oggi)')
    a = p.parse_args()

    percorso = Path(a.caso)
    if not percorso.exists():
        print(f"ERRORE: {a.caso} non esiste.")
        return 1
    try:
        dati = json.loads(percorso.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e:
        print(f"ERRORE: {a.caso} non e' JSON valido — {e}")
        return 1

    oggi = a_data(a.oggi) if a.oggi else _date.today()
    if oggi is None:
        print(f"ERRORE: --oggi '{a.oggi}' non e' una data valida (AAAA-MM-GG).")
        return 1

    bloccanti, avvisi = [], []

    def blocca(codice, testo):
        bloccanti.append(f"[{codice}] {testo}")

    def avvisa(codice, testo):
        avvisi.append(f"[{codice}] {testo}")

    # --- 1. i campi che il deliverable pretende ------------------------------
    richiesti = RICHIESTI[a.tipo]
    mancanti = []
    for campo, perche in richiesti.items():
        if not vuoto(leggi_campo(dati, campo)):
            continue
        alt = ALTERNATIVE.get(campo)
        if alt and not vuoto(leggi_campo(dati, alt)):
            continue
        mancanti.append(campo)
        etichetta = f"{campo}" + (f" (ne' {alt})" if alt else '')
        blocca('CAMPO_MANCANTE', f"{etichetta} — {perche}")

    # --- 2. il fascicolo si contraddice? -------------------------------------
    nascita = a_data(leggi_campo(dati, 'minore.data_nascita'))
    nascita_rel = a_data(leggi_campo(dati, 'relazione.data_nascita_figlio'))
    inizio = a_data(leggi_campo(dati, 'relazione.inizio_convivenza'))
    fine = a_data(leggi_campo(dati, 'relazione.data_cessazione_convivenza'))

    if nascita and nascita_rel and nascita != nascita_rel:
        blocca('DATE_DISCORDANTI',
               f"minore.data_nascita ({nascita}) e relazione.data_nascita_figlio "
               f"({nascita_rel}) non coincidono. E' lo stesso bambino: due date diverse "
               f"nel fascicolo diventano due date diverse negli atti")

    if inizio and nascita and nascita < inizio:
        blocca('CRONOLOGIA_IMPOSSIBILE',
               f"il figlio ({nascita}) nasce prima dell'inizio della convivenza ({inizio})")

    if nascita and fine and fine < nascita:
        blocca('CRONOLOGIA_IMPOSSIBILE',
               f"la convivenza cessa ({fine}) prima della nascita del figlio ({nascita}). "
               f"Il caso e' costruito sui mesi fra le due date")

    if inizio and fine and fine < inizio:
        blocca('CRONOLOGIA_IMPOSSIBILE',
               f"la convivenza cessa ({fine}) prima di cominciare ({inizio})")

    if nascita and nascita > oggi:
        blocca('CRONOLOGIA_IMPOSSIBILE', f"il minore risulta nato nel futuro ({nascita})")

    # l'eta' dichiarata contro l'eta' vera: il fulcro del caso e' sotto i 3 anni,
    # e il campo va aggiornato a ogni sessione. Se non lo si aggiorna, si ragiona
    # su un bambino che non esiste piu'.
    eta_dich = leggi_campo(dati, 'minore.eta_mesi_attuale')
    if nascita and isinstance(eta_dich, (int, float)):
        eta_vera = mesi_fra(nascita, oggi)
        if abs(eta_vera - eta_dich) > 1:
            blocca('ETA_NON_AGGIORNATA',
                   f"minore.eta_mesi_attuale dice {eta_dich:.0f} mesi, la data di nascita "
                   f"({nascita}) ne dice {eta_vera}. Sotto i 3 anni la prassi sui pernottamenti "
                   f"cambia mese per mese: si ragiona sull'eta' vera")
        if eta_vera >= 36 > eta_dich:
            avvisa('SOGLIA_TRE_ANNI_SUPERATA',
                   f"il minore ha superato i 3 anni ({eta_vera} mesi): l'argomento principale "
                   f"del caso cambia. Rivedi la strategia sui pernottamenti")

    mesi_dich = leggi_campo(dati, 'relazione.mesi_di_convivenza_dopo_il_parto')
    if nascita and fine and isinstance(mesi_dich, (int, float)):
        mesi_veri = mesi_fra(nascita, fine)
        if abs(mesi_veri - mesi_dich) > 1:
            blocca('MESI_DOPO_IL_PARTO_INCOERENTI',
                   f"mesi_di_convivenza_dopo_il_parto dice {mesi_dich:.0f}, le date ne dicono "
                   f"{mesi_veri} ({nascita} → {fine}). E' il fatto su cui l'avversario costruisce "
                   f"la tesi dell'assenza di accudimento: il numero va difeso, non stimato")

    # --- 3. i rischi che il fascicolo rende gia' visibili --------------------
    intest = leggi_campo(dati, 'casa.intestazione')
    fam = leggi_campo(dati, 'casa.e_stata_casa_familiare')
    occupa = leggi_campo(dati, 'casa.chi_la_occupa_oggi')
    if isinstance(intest, str) and re.search(r'assistito|padre|cliente|lui', intest, re.I) \
            and fam is True:
        avvisa('RISCHIO_337_SEXIES',
               f"la casa risulta intestata all'assistito ed e' stata casa familiare"
               + (f", oggi occupata da: {occupa}" if isinstance(occupa, str) else '')
               + ". L'art. 337-sexies c.c. la assegna al genitore collocatario anche "
                 "senza matrimonio e anche se lui ne e' l'unico proprietario. Si presidia "
                 "prima, non dopo: vedi references/casa-familiare.md")

    modalita = leggi_campo(dati, 'situazione_attuale.modalita_versamento')
    if isinstance(modalita, str) and re.search(r'contant|brevi\s+manu|a\s+mano', modalita, re.I):
        blocca('MANTENIMENTO_IN_CONTANTI',
               f"modalita_versamento: «{modalita}». Il contante non e' mai stato pagato, in "
               f"giudizio. Va corretto adesso — bonifico con causale — e il briefing deve dirlo "
               f"prima della prossima mensilita'")

    versato = leggi_campo(dati, 'situazione_attuale.mantenimento_versato_oggi')
    if not vuoto(versato) and vuoto(modalita):
        avvisa('VERSAMENTO_SENZA_MODALITA',
               "risulta un mantenimento versato ma non come. Se non e' tracciato, in giudizio "
               "non risulta versato")

    # una voce del fronte penale senza i suoi campi e' una voce che non si difende
    for chiave in ('denunce_ricevute', 'denunce_sporte'):
        voci = leggi_campo(dati, f'fronte_penale.{chiave}')
        if not isinstance(voci, list):
            continue
        for i, voce in enumerate(voci, 1):
            if not isinstance(voce, dict):
                blocca('VOCE_PENALE_INCOMPLETA',
                       f"fronte_penale.{chiave}[{i}] non e' strutturata: servono data, reato "
                       f"ipotizzato, autorita', stato del procedimento, difensore nominato")
                continue
            persi = [c for c in ('data', 'reato', 'autorita', 'stato') if vuoto(voce.get(c))]
            if persi:
                blocca('VOCE_PENALE_INCOMPLETA',
                       f"fronte_penale.{chiave}[{i}]: mancano {', '.join(persi)}. "
                       f"Un procedimento senza stato e senza autorita' non ha termini calcolabili")

    if a.tipo == 'penale':
        ricevute = leggi_campo(dati, 'fronte_penale.denunce_ricevute') or []
        sporte = leggi_campo(dati, 'fronte_penale.denunce_sporte') or []
        if not ricevute and not sporte:
            blocca('NESSUN_PROCEDIMENTO_PENALE',
                   "il fronte penale e' vuoto in entrambe le direzioni: non c'e' oggetto di difesa")

    obiettivi = leggi_campo(dati, 'obiettivi_del_cliente.dichiarati')
    realistici = leggi_campo(dati, 'obiettivi_del_cliente.realistici')
    if not vuoto(obiettivi) and vuoto(realistici):
        avvisa('OBIETTIVI_NON_FILTRATI',
               "ci sono obiettivi dichiarati e nessun obiettivo realistico. La distanza fra i due "
               "e' il primo lavoro del difensore, e va fatta prima dell'atto, non dopo il rigetto")

    # --- 4. l'atto e' partito prima dei fatti? -------------------------------
    # E' il controllo che chiude il cerchio: se mancano campi obbligatori e l'atto
    # contiene comunque cifre e date, quelle cifre e quelle date non vengono dal
    # fascicolo. Non c'e' altro posto da cui possano venire.
    if a.atto:
        f_atto = Path(a.atto)
        if not f_atto.exists():
            print(f"ERRORE: {a.atto} non esiste.")
            return 1
        testo = f_atto.read_text(encoding='utf-8')
        if mancanti:
            trovati_imp = importi_nel_testo(testo)
            trovate_dat = date_nel_testo(testo)
            if trovati_imp or trovate_dat:
                blocca('ATTO_SCRITTO_SU_FASCICOLO_INCOMPLETO',
                       f"{len(mancanti)} campi obbligatori sono vuoti in caso.json, e l'atto "
                       f"contiene gia' {len(trovati_imp)} importi e {len(trovate_dat)} date. "
                       f"Quei valori non vengono dal fascicolo: o sono stati chiesti al cliente e "
                       f"non registrati — e allora vanno registrati — oppure sono stati dedotti, e "
                       f"un importo dedotto in un atto e' una busta paga in mano alla controparte. "
                       f"Campi vuoti: {', '.join(mancanti[:6])}"
                       + (f" e altri {len(mancanti) - 6}" if len(mancanti) > 6 else ''))
        else:
            noti = set()
            for chiave in ('assistito.reddito_annuo_lordo', 'controparte.reddito_annuo_lordo',
                           'casa.rata_mensile', 'situazione_attuale.mantenimento_versato_oggi'):
                v = leggi_campo(dati, chiave)
                if isinstance(v, (int, float)):
                    noti.add(f"{v:.2f}")
                elif isinstance(v, str):
                    noti |= importi_nel_testo(v)
            estranei = sorted(importi_nel_testo(testo) - noti)
            if estranei:
                avvisa('IMPORTI_NON_NEL_FASCICOLO',
                       f"{len(estranei)} importi nell'atto e non in caso.json: "
                       f"{', '.join(estranei[:8])}"
                       + (f" e altri {len(estranei) - 8}" if len(estranei) > 8 else '')
                       + ". Alcuni saranno somme calcolate o richieste, ed e' corretto; ognuno "
                         "deve pero' poter essere ricondotto a un documento del fascicolo")

    # --- rapporto ------------------------------------------------------------
    compilati = sum(1 for c in richiesti if not vuoto(leggi_campo(dati, c))
                    or (ALTERNATIVE.get(c) and not vuoto(leggi_campo(dati, ALTERNATIVE[c]))))
    print('=' * 78)
    print(f"COLLAUDO DEL FASCICOLO  {percorso.name}   (deliverable: {a.tipo})")
    print('=' * 78)
    print(f"Campi richiesti:  {compilati}/{len(richiesti)} compilati")
    if nascita:
        print(f"Minore:           nato il {nascita} — {mesi_fra(nascita, oggi)} mesi al {oggi}")
    if nascita and fine:
        print(f"Convivenza:       cessata il {fine} — {mesi_fra(nascita, fine)} mesi dopo il parto")
    print()

    if bloccanti:
        print(f"BLOCCANTI ({len(bloccanti)})")
        for b in bloccanti:
            print(f"  {b}")
        print()
    if avvisi:
        print(f"AVVISI ({len(avvisi)}) — da guardare a mano, non bloccano")
        for v in avvisi:
            print(f"  {v}")
        print()

    if bloccanti:
        print("ESITO: NON SI SCRIVE.")
        if mancanti:
            print("  I campi vuoti si chiedono al cliente e si registrano in caso.json — non si "
                  "riempiono con un valore verosimile.")
        if len(bloccanti) > len(mancanti):
            print("  Le incoerenze si risolvono sui documenti in fascicolo/prove/, decidendo "
                  "quale versione e' quella vera: un fascicolo che si contraddice produce atti "
                  "che si contraddicono, e la contraddizione la trova la controparte.")
        return 1
    print("ESITO: il fascicolo regge. I fatti ci sono e non si contraddicono; se siano quelli "
          "veri lo dicono i documenti in fascicolo/prove/, non questo script.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
