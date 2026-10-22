# Siti di riferimento analizzati con Taste: schede e sintesi

Analisi in quattro passi secondo `references/step1-4` della skill Taste, su catture fatte con il browser isolato dietro la guardia dei riferimenti (sola lettura). File Taste per sito: `{dominio}.md` e `{dominio}.json` in questa cartella. Usali come principi, mai come modelli da copiare.

**Limiti delle catture:**
- Heva copre la pagina con un popup email, a 1440 px subito e a 390 px dopo circa 4 s, e Taste non clicca.
- Oura mostra il banner dei cookie in basso.
- Antara rivela i testi allo scorrimento.

## Schede per sito (A–J)

### Heva Health
- A Struttura: nav fissa · hero a tutta finestra (titolo, valutazione, 2 CTA + link) · due percorsi di cura · health assessment · team clinico · 3 passi · testimonianze · prima/dopo · risultati clinici · FAQ · footer; popup sconto dopo pochi secondi.
- B Gerarchia: un titolo enorme e sottile contro un'interfaccia piccola; l'enfasi viene dalla scala e dall'inversione di fondo (oliva), non dal grassetto.
- C Tipografia: PP Editorial New 104/72/48/36/30 px, peso 300–400, tracking negativo; Inter 18 px corpo (576 px max), 14–16 UI, 11–12 etichette, fino a 9 px.
- D Fotografie: video muti in loop a tutta finestra al posto delle foto; persone reali nel servizio; ritratti 1:1 del team; su mobile foto a tutto schermo con velatura e testo sopra.
- E Spaziature: base 4 px, 90 px tra sezioni, griglia 2 × 584 px con gutter 32.
- F Distintivi: bicolore panna/oliva, serif sottile enorme, pill ovunque, percorsi paralleli.
- G CTA: tre livelli — pill piena chiara, pill a contorno, link sottolineato; ripetute; popup sconto.
- H Animazioni: transizioni CSS 0.15–0.5 s su colore e transform; video in loop; nessuna libreria; prefers-reduced-motion presente.
- I Per Mobilitas: (1) gerarchia d'azione a tre livelli: consulto pieno, prima visita a contorno, WhatsApp come link; (2) i due percorsi come scelta esplicita in prima schermata; (3) contrasto di scala con un peso leggero per i titoli.
- J Non copiare: popup email a tutto schermo; prima/dopo e statistiche da studi farmacologici; testo a 9–12 px e serif.

### Antara Spa & Wellness
- A Struttura: header a linee con wordmark distanziato · hero video con parola gigante e "Scroll" · capitoli "Past wisdom" / "Modern experiences" · menu (un paragrafo) + "Book a treatment" · sala a tutta finestra con card "Reach Us" inclinata · promozioni · Instagram · contatti WHATSAPP / CALL US giganti · barra info · loghi del gruppo.
- B Gerarchia: scala estrema (165 px contro 13.5 px), quasi nessun livello intermedio; una parola per schermata.
- C Tipografia: Fraunces peso 100 a 165/90/75/52/37 px; Manrope 13.5 px corpo; navigazione maiuscola.
- D Fotografie: video di sfondo velato; ambienti e materiali a tutta finestra senza cornici.
- E Spaziature: misure fluide, salti fino a 540 px; ritmo lento voluto.
- F Distintivi: wordmark distanziato, arco verde che emerge dal fondo, card terracotta ruotata, menu verticale flottante, audio, contatti come parole giganti.
- G CTA: nessun pulsante pieno; link testuali ("Book a treatment", "Explore"); contatti finali a pillola a contorno con orari.
- H Animazioni: GSAP + Lenis (smooth scroll), rivelazioni allo scorrimento (fino a 27 testi nascosti), carosello sedi, audio.
- I Per Mobilitas: (1) capitoli sintomo → causa → soluzione; (2) una parola chiave gigante per capitolo; (3) chiusura con doppio blocco Chiama / WhatsApp e orari.
- J Non copiare: smooth scroll e rivelazioni che nascondono il testo; audio; corpo a 13.5 px e trattamenti senza prezzi né durate.

### Oura
- A Struttura: barra promo · nav · hero foto a tutta larghezza con titolo a sinistra e una CTA blu · "capisci il tuo corpo" · carosello di 6 temi · statistica con nota · 3 testimonianze · funzione con avvertenza · notizie · stampa · pagamenti · newsletter · footer scuro.
- B Gerarchia: titolo serif sottile, un solo blu per agire, card tonali, blocchi scuri per la chiusura.
- C Tipografia: Editorial New 80/68 px peso 300–400, tracking fino a -4 px; AkkuratLL 40/20/16 px; etichette 12–13 px/600.
- D Fotografie: prodotto sul corpo in luce calda a tutta larghezza; persone nella vita quotidiana; ritratti tondi nelle testimonianze.
- E Spaziature: base 8 px, margini 64 px, griglia 28 colonne, sezioni separate dal cambio di tinta.
- F Distintivi: blu solo sulle CTA (0.2% della superficie), citazioni in serif con etichetta tematica, note a piè di pagina.
- G CTA: una pill blu piena nell'hero; secondarie più leggere; ripetizione moderata.
- H Animazioni: carosello, transizioni 0.15–0.7 s; nessun video.
- I Per Mobilitas: (1) un solo colore d'azione per fondo; (2) prove con la fonte accanto; (3) recensioni come citazioni grandi con l'etichetta del disturbo, solo se trascritte fedelmente.
- J Non copiare: serif; carosello che nasconde contenuto; barra promo, banner e logiche da e-commerce.

## Sintesi comparativa

**Comuni ai tre**
- Titoli a peso leggero e scala grande: Heva 300 a 104 px, Antara 100 a 165 px, Oura 300 a 80 px.
- Fondo naturale dominante con un solo inchiostro scuro.
- Un accento ristretto: Oura 0.2%, Heva 3 occorrenze, Antara sotto il 2%.
- Niente card con ombra.
- Immagine a tutta finestra nel primo schermo (video in due casi su tre).

**Davvero originali**
- Antara: parola-capitolo gigante, arco che emerge, card inclinata, contatti come tipografia.
- Heva: due percorsi in prima schermata, gerarchia d'azione a tre livelli.
- Oura: prove con nota a piè di pagina, citazioni tipografiche con etichetta tematica.

**Che differenzierebbero Mobilitas**
- Montserrat leggero a grande scala, con una parola in 800–900.
- I due percorsi consulto / prima visita resi visibili come scelta.
- Il racconto per capitoli.
- Le prove con la fonte.

**Compatibili con il brand**
- Peso leggero di Montserrat. Al momento dell'analisi il sito caricava solo i pesi 400–900: per il 300 in produzione va aggiunto (nei prototipi è servito in locale).
- Panna dominante con inchiostro blu, verde solo su blu, niente ombre.
- CTA a pillola: cambiamento minore rispetto agli angoli del design system, da approvare.

**Non compatibili:** serif, palette terra e oliva, audio.

**Rischiano di peggiorare la conversione**
- Popup a tutto schermo (Heva).
- Smooth scroll, rivelazioni e salti di 540 px che ritardano l'offerta e nascondono testo (Antara).
- CTA solo testuali (Antara).
- Caroselli (Oura).
- Corpo piccolo.
- Video pesanti su mobile.
- Titoli leggeri usati sotto i 36 px, dove perdono leggibilità.
