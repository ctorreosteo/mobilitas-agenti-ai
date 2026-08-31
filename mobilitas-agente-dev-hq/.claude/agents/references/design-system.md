# Design system del gestionale

Fonte di verità: `/Users/carlitos/mobilitas-frontend/src/style/index.css` (1168 righe) e `docs/ui-and-components.md`. Questo file è il riassunto operativo per la revisione.

---

## Impianto

- **Tailwind CSS v4** (plugin Vite, niente `tailwind.config.js`)
- **shadcn/ui** stile New York, base color neutral, CSS variables
- Icone: **lucide-react** preferito; `react-icons` presente per casi storici
- Toast: **sonner**, sempre via il wrapper `@/lib/toast`
- Date: **react-day-picker** dietro `DatePickerInput`
- Grafici: **recharts**
- Merge classi: `cn()` da `@/lib/utils` (clsx + tailwind-merge)
- Varianti: **class-variance-authority**
- Font: Montserrat
- Tema a runtime: `ThemeProvider`, **default dark**

---

## I tre temi

Definiti in `src/style/index.css` come tre blocchi di variabili:

| Tema | Selettore | Sfondo | Identità |
|------|-----------|--------|----------|
| Chiaro | `:root` | bianco | Testi blu aziendale |
| **Dark** | `.dark` | `#002552` blu aziendale | **Default del prodotto** |
| **Silvia** | `.silvia` | `#000000` nero puro | Monocromatico, grigi eleganti |

Colori di marca, uguali nei tre: `--brand-blue #002552` · `--brand-green #72fa93` · `--brand-light-gray #F4F4F4`.

### La tabella che serve durante la revisione

| Token | Chiaro | Dark | Silvia |
|-------|--------|------|--------|
| `--background` | bianco | `#002552` | `#000000` |
| `--foreground` | brand-blue | `#ffffff` | `#ffffff` |
| `--heading-foreground` | brand-blue | **`#72fa93` verde** | `#ffffff` |
| `--card` | bianco | **`#002552` = sfondo** | `#1a1a1a` |
| `--popover` | bianco | **`#002552` = sfondo** | `#0a0a0a` |
| `--primary` | brand-blue | **`#002552` = sfondo** | `#1a1a1a` |
| `--secondary` | grigio chiaro | **`#002552` = sfondo** | `#1a1a1a` |
| `--muted` | grigio chiaro | **`#002552` = sfondo** | `#1a1a1a` |
| `--accent` | grigio chiaro | **`#002552` = sfondo** | `#2a2a2a` |
| `--muted-foreground` | grigio medio | `rgba(255,255,255,.7)` | `#a0a0a0` |
| `--border` | grigio chiaro | `rgba(255,255,255,.1)` | `#2a2a2a` |
| `--input` | grigio chiaro | `rgba(255,255,255,.15)` | `#1a1a1a` |
| `--ring` | grigio | `rgba(255,255,255,.3)` | `#4a4a4a` |

### La conseguenza da tenere in testa

**In dark, sette token di superficie sono lo stesso colore dello sfondo.** Card, popover, primary, secondary, muted, accent: tutti `#002552`.

Vuol dire che **in dark la profondità non esiste come colore** — esiste solo come **bordo** (`rgba(255,255,255,0.1)`).

Chi sviluppa in silvia o in chiaro vede le card staccarsi dal fondo e non si accorge di nulla. In dark — il tema di default, quello che vedono quasi tutti — lo stesso blocco è una superficie piatta.

Regola pratica: **separazione visiva = bordo, non fondo.**

Analogamente `--heading-foreground` è verde solo in dark: un titolo che usa quel token cambia identità fra i temi. È voluto, ma va saputo prima di scrivere `text-heading-foreground` accanto a un colore fisso.

---

## Le primitives — `src/components/ui/` (29)

| File | Uso |
|------|-----|
| `button.tsx` | Azioni |
| `input.tsx` · `textarea.tsx` · `label.tsx` · `checkbox.tsx` | Form |
| `select.tsx` | Scelta di un valore |
| `popover.tsx` · `dropdown-menu.tsx` · `context-menu.tsx` | Overlay e menu |
| `dialog.tsx` | Modale centrato — conferme corte |
| `sheet.tsx` | Pannello laterale — dettagli lunghi |
| `table.tsx` · `pagination.tsx` · `list.tsx` | Dati |
| `tabs.tsx` · `collapsible.tsx` · `separator.tsx` | Struttura |
| `card.tsx` | Layout dashboard/form |
| `badge.tsx` | Chip di stato |
| `skeleton.tsx` | Caricamento |
| `tooltip.tsx` · `breadcrumb.tsx` · `sidebar.tsx` | Navigazione e aiuto |
| `calendar.tsx` | Calendario day-picker |
| **`date-picker-input.tsx`** | **Campo data** — `DatePickerInput`, `DatePickerField`, `normalizeDateIsoValue` |
| `nazione-combobox` · `provincia-combobox` · `tag-dolore-combobox` · `fonte-lead-magnet-combobox` | Autocomplete di dominio |

Nelle primitives **non va logica di business**.

### Il caso date picker — il precedente da citare

`DatePickerInput` è la primitive canonica: `Popover` + `Calendar` + `Button`, `date-fns` con locale `it`, valore ISO `YYYY-MM-DD`, `normalizeDateIsoValue` per la validazione.

Stato reale del codebase: **13 file la usano, 20 file usano `<input type="date">` grezzo.**

Un `<input type="date">` prende l'aspetto dal sistema operativo: font diverso, altezza diversa, icona diversa, e un calendario nativo che non somiglia a `Calendar`. Messo accanto a un `DatePickerInput` la differenza si vede subito.

È esattamente il difetto che questo revisore deve fermare.

Un sintomo correlato, già nel CSS: le regole `!important` su `.silvia button[data-date-picker-range]` sono la pezza che serve quando i campi data non sono uno solo.

### Sheet e Dialog

23 file importano `Sheet` — il pannello laterale è **il** pattern di dettaglio del gestionale (visita, paziente, spesa, candidato, richiesta…). Un dettaglio nuovo che non è uno `Sheet` deve avere una ragione dichiarata.

`Dialog` è per le conferme corte, non per i dettagli lunghi.

---

## Convenzioni UX già scritte

Da `docs/ui-and-components.md` e `docs/conventions.md`:

- Esito successo/errore via **toast**, mai `alert()`
- Stati di caricamento espliciti sul salvataggio degli sheet
- Accessibilità: preferire i componenti Radix sotto shadcn
- Mobile: `use-mobile.ts` + sidebar collassabile
- Stringhe UI in **italiano** (label, colonne, empty state, toast, breadcrumb); identificatori in inglese
- **Non introdurre un design system parallelo**

---

## Debito noto — contesto, non alibi

| Cosa | Quanto |
|------|--------|
| Classi di palette Tailwind grezza in `.tsx` | ~5467 |
| `bg-white` / `text-black` e simili | ~1430 |
| Hex hardcoded `[#…]` | ~234 |
| Varianti `dark:` | ~2630 |
| Varianti `silvia:` | **~929** |
| `<input type="date">` grezzi | 20 |

Il divario 2630 / 929 è la misura del problema: **la maggior parte dei componenti che si adattano al dark non si adatta al silvia.**

Questi numeri servono a due cose: capire che il difetto è sistemico, e **non chiedere la bonifica del pregresso in una revisione di task.** Il mandato è che il diff non peggiori il conto.
