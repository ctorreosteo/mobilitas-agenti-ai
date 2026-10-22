> Analisi Taste di https://antaraspawellness.com/ (catturata il 2026-10-14). Smooth scroll e animazioni allo scorrimento: alcune schermate catturano testi non ancora comparsi.

# Design Map

## Spacing Scale
12 · 14.4 · 21.6 · 28.8 · 80 · 540 px (passo di circa 7.2 px; salto di 540px tra due sezioni)

## Font Hierarchy
- Parola di sezione: Fraunces 165px / 100
- Hero e wordmark: Fraunces 90px / 100, lettere distanziate
- H2: Fraunces 75px / 100 · H4 52.5px · H5 37.5px
- Corpo: Manrope 13.5px / 400, interlinea 18px · navigazione in maiuscolo

## Color Palette
- Terra #78694E (53.8%) · oliva #626548 (22.5%) · verde-nero #162015 (16.7%)
- Testo sabbia #C5BEB1
- Accenti: verde #425E40 (arco) · terracotta #9A5E39 (card)

## Image Ratios
- Video hero 1440x1313 a tutta larghezza con velatura scura
- Fotografie d'ambiente a tutta finestra, circa 16:10

## Component Tokens
- Raggi: arco 565px in alto · 90px · 61.5px · 45px · cerchi 50%
- Ombre: assenti (una sola al 2%, impercettibile)
- Griglia: tutta larghezza, 4 colonne, gutter 35px
- Menu verticale flottante a pillola · pulsante audio
- Movimento: GSAP + Lenis; transizioni 0.2–0.5s, ease-in-out
- :focus-visible presente · prefers-reduced-motion presente

---

# Taste DNA

### Peso 100 a scala monumentale
- **Trigger**: esprimere quiete senza immagini di relax stereotipate
- **Decision**: Fraunces a peso 100 fino a 165px invece di titoli medi in grassetto
- **Reason**: una lettera enorme e sottilissima rallenta la lettura e comunica calma prima delle parole
- **Evidence**: 132 elementi a peso 100; 165px su 34 elementi e 75px su 76; wordmark distanziato

### Il ritmo è lo scorrimento
- **Trigger**: presentare un'offerta poco differenziata
- **Decision**: capitoli rivelati scorrendo invece di un elenco di servizi
- **Reason**: il racconto fa entrare nello spazio prima di valutare i prezzi
- **Evidence**: GSAP e Lenis; fino a 27 testi nascosti durante lo scorrimento; salto di 540px; trattamenti in un solo paragrafo

### Forme che rompono la griglia
- **Trigger**: evitare l'aspetto da template di spa
- **Decision**: un arco verde che emerge dal fondo e una card terracotta inclinata invece di blocchi allineati
- **Reason**: poche forme fuori asse rendono la pagina riconoscibile senza aggiungere contenuto
- **Evidence**: radius 565px 565px 0 0; card ruotata; accenti sotto il 2% della superficie

### Nessun pulsante classico
- **Trigger**: chiedere il contatto
- **Decision**: parole giganti in corsivo dentro contorni a pillola invece di pulsanti pieni
- **Reason**: l'azione diventa tipografia e non un elemento estraneo
- **Evidence**: 0 elementi button; blocchi WHATSAPP e CALL US a metà larghezza; testo 75px
