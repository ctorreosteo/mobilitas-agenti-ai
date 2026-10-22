> Analisi Taste di https://www.hevahealth.com/ (catturata il 2026-10-14). Limite: un popup di raccolta email a tutto schermo copre la pagina a 1440 px e, dopo circa 4 secondi, anche a 390 px. Taste non clicca: misure dal DOM completo e dalla schermata mobile presa prima del popup.

# Design Map

## Spacing Scale
4 · 8 · 12 · 16 · 24 · 32 · 40 · 64 · 90 px (base 4 px; 90 px tra sezioni)

## Font Hierarchy
- Hero: PP Editorial New 104px / 300, interlinea 106px, tracking -2.08px
- Display: 72px / 300 · 48px · 36px
- H3: PP Editorial New 30px / 400, tracking -0.96px
- Corpo: Inter 18px / 400, interlinea 29.25px, larghezza massima 576px
- Interfaccia: Inter 14–16px / 500 · etichette 11–12px (anche 9px)

## Color Palette
- Fondo #FDFDF1 (44.5%) · fondo alternato #E9EBDD (22.2%)
- Inchiostro e superficie scura #39442B (8.3%) · testo secondario #526343
- Evidenziatore #FAFE86 (3 occorrenze)

## Image Ratios
- Video a tutta finestra 1440x900 (5) · video 582x437 (2)
- Feature 1.9:1 e 16:9 · ritratti del team 1:1

## Component Tokens
- Raggi: 9999px (pulsanti, badge) · 30px · 16px · 12px
- Ombra: unica, tinta oliva rgba(57,68,43,0.07)
- Griglia: 2 colonne × 584px, gutter 32px
- Pulsanti: pill, 16px/500, padding 16×32 (principale) e 12×24
- Transizioni: 0.15–0.5s cubic-bezier(0.4,0,0.2,1) su colore e transform
- :focus-visible presente · prefers-reduced-motion presente

---

# Taste DNA

### Titolo sottile e grande, interfaccia piccola
- **Trigger**: dare autorevolezza medica senza il tono di un portale sanitario
- **Decision**: serif a peso 300 a 104px per i titoli e Inter 11–16px per il resto, invece di un sans pesante unico
- **Reason**: un titolo leggero ma enorme si legge come una promessa calma; la scala fa il lavoro del grassetto
- **Evidence**: h1 104px/300, tracking -2.08px; Inter su 707 elementi contro 40; dimensioni più frequenti 14px e 12px

### Due colori, nessun accento acceso
- **Trigger**: dare risalto a CTA e sezioni
- **Decision**: solo panna e oliva scuro con fondi alternati, invece di un accento saturo
- **Reason**: in un contesto clinico un colore squillante suona da promozione; l'inversione di fondo segnala importanza senza alzare la voce
- **Evidence**: #FDFDF1 44.5% + #E9EBDD 22.2%; #39442B 8.3% come fondo e testo; #FAFE86 in 3 punti

### Il video al posto della foto
- **Trigger**: mostrare un servizio che il visitatore non vede di persona
- **Decision**: video in loop muti a tutta finestra invece di fotografie statiche
- **Reason**: il movimento lento rende tangibile il servizio
- **Evidence**: 7 video autoplay muted loop, 5 a 1440x900; nessuna libreria di animazione

### Nessuna card con ombra
- **Trigger**: raggruppare percorsi, team e passi
- **Decision**: niente card con ombra; gruppi affidati a fondi alternati e pill
- **Reason**: superfici piatte mantengono calma una pagina lunga e densa di blocchi
- **Evidence**: 0 card rilevate da extract.js; ombra unica al 7%; raggio 9999px su 83 elementi
