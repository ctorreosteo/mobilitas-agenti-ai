# Casting, guardaroba, ambiente, camera, luce

I quattro punti in cui un prompt generico produce un'immagine da stock. Si aprono
mentre si scrive il T2I, non prima.

---

## Casting

Se il target non è specificato, deducilo **solo** quando è evidente dallo script.
Altrimenti resta sul pubblico dell'annuncio, senza inventare caratteristiche sensibili.

### L'età non è una preferenza: è un vincolo

**Il pubblico va dai 35 ai 60 anni. In scena si sta sempre fra i 40 e i 60.**

Non è una contraddizione: si rappresenta il **centro** del bersaglio, non il suo bordo più
giovane. Chi ha 38 anni si riconosce in una scena con una cinquantenne; chi ne ha 55 non si
riconosce in una scena con una trentacinquenne, e per di più legge il problema come roba da
giovani.

Non è un gusto estetico. È il pubblico che paga: chi convive con il problema da anni, ha un
lavoro, una famiglia e i soldi per un trattamento. Un protagonista di trent'anni sposta il
video su chi non prenota, e fa leggere il problema come passeggero — «passerà», che è
esattamente l'obiezione da disinnescare.

L'età si scrive **come numero** nel prompt (`a 52-year-old Italian woman`), non come
aggettivo: «middle-aged» produce trentacinquenni.

Il resto del casting, quando è coerente:

- aspetto europeo contemporaneo;
- curati, realistici;
- benestanti senza ostentazione;
- anatomia naturale, pelle vera con texture e imperfezioni, rughe d'espressione vere per l'età;
- nessun look da banca immagini.

**La pelle è il punto in cui si vede la differenza.** Chiedi sempre texture reale, pori
visibili, piccole asimmetrie: la pelle levigata è il marchio dell'immagine generata.

Quando più scene rappresentano la stessa persona nella stessa giornata, il personaggio
non cambia. La `descrizione_fissa` che arriva dalla regia si copia **alla lettera**, non
si riformula: due riformulazioni diverse producono due persone diverse.

### Quando è attivo un personaggio Soul ID

L'identità ha priorità assoluta. Apri il prompt con:

> Use the selected Higgsfield Character as the ONLY facial identity reference. Facial
> identity consistency has absolute priority over every other element. Do not redesign,
> reinterpret or generate a different face.

Preserva: proporzioni del volto, forma, occhi, sopracciglia, naso, labbra, mandibola,
orecchie, incarnato, texture della pelle, capelli, attaccatura, barba, età apparente,
asimmetrie naturali, stile dell'espressione.

Con il personaggio attivo, **non sovraccaricare il prompt di descrizioni fisiche
concorrenti**: ogni aggettivo sul viso tira l'identità da un'altra parte. Modifica solo
abbigliamento, posa, postura, ambiente, luce e angolo di camera.

---

## Guardaroba

Si descrive **sempre**: capo · colore · tessuto · pantaloni o gonna · cintura · scarpe ·
gioielli · orologio · accessori. Nessun logo, nessun marchio, nessuna scritta.

### Il registro è la via di mezzo, e ha due modi di sbagliare

Il bersaglio è **una persona curata in una giornata normale, che fra un'ora esce di casa.**

| Troppo giù | Il bersaglio | Troppo su |
|---|---|---|
| felpa, tuta, pantaloni morbidi da casa, ciabatte, capelli disfatti, viso spento | maglia di buon cotone o lana leggera, jeans scuri puliti o pantaloni di cotone, scarpe vere, capelli in ordine, un accessorio semplice | completo, camicia stirata, ufficio, look da catalogo |
| legge come **persona che si è arresa** | legge come **persona che proverà a risolvere** | legge come **pubblicità** |

L'errore da evitare per primo è quello di sinistra, ed è controintuitivo: sembra che
vestire male il protagonista renda la scena più vera. Fa il contrario. Nessuno si
riconosce volentieri in qualcuno più trasandato di come si vede, e soprattutto una persona
che si è lasciata andare non è credibile come qualcuno che prenoterà un trattamento.
L'identificazione la dà la **situazione**, non il degrado.

Il dolore si legge dalla postura, dal viso e dalla luce. Non dai vestiti.

Un esempio del livello giusto: *a soft merino crewneck in deep teal, slightly relaxed,
sleeves pushed to mid-forearm; dark clean straight-leg jeans; leather loafers; a thin
gold chain; small worn stud earrings; short unpolished nails; a plain watch with a
scuffed strap.*

Lo stesso in versione **sbagliata verso il basso**, da non scrivere mai: *heather grey
high-neck sweatshirt with stretched cuffs, soft charcoal loose lounge trousers, hair in a
ponytail that has already come loose.*

---

## Ambiente

Non scrivere «modern office», «nice bedroom», «elegant restaurant». Sono le tre frasi
che producono la stessa immagine per chiunque.

Descrivi materiali, superfici, arredi, luce architettonica, attività sullo sfondo:

> warm oak flooring, floor-to-ceiling glazing with black aluminium frames, acoustic
> ceiling panels, integrated linear LEDs, a walnut workstation, indoor plants, glass
> meeting rooms blurred in the background

Ogni ambiente deve sembrare **progettato e vissuto**. Vissuto significa: una tazza usata,
una sedia non allineata, un cavo, una pila di carte. L'ordine perfetto è il secondo
marchio dell'immagine generata.

Preferisci ambienti europei e italiani quando è coerente, e prendi i dettagli dalla
città di riferimento invece di inventarli.

### La casa è il secondo costume

Un ambiente brutto o anonimo abbassa il ceto percepito esattamente quanto un capo
sbagliato, e lo fa senza che nessuno se ne accorga: si guarda il protagonista e si conclude
che quella è una persona a cui le cose non vanno bene.

Descrivi una casa **di cui si è orgogliosi**: non una casa da rivista, una casa bella e
vissuta. Materiali buoni, qualche pianta, luce, un quadro, tessuti veri. Poi sporcala con
i segni della vita, che è il contrario dell'ordine perfetto.

Vale in particolare per la **profondità**. Uno sfondo piatto — un muro, un
elettrodomestico, una porta chiusa — è il difetto più frequente e il più facile da
evitare: dietro il soggetto ci vuole qualcosa da guardare, a fuoco morbido.

### La finestra è dove entra la città

Quando la città di riferimento deve vedersi, **la finestra o la vetrata è quasi sempre il
posto giusto**, ed è l'unico che non costringe a spostare la scena fuori casa.

Come si scrive: lo sfondo urbano è **sfocato ma leggibile**, mai nitido e mai vuoto.
Tetti, facciate, alberi, una via che scende — il livello del *tessuto*, non i landmark.
Chi vive lì riconosce la sua città senza saper dire da cosa; chi non ci vive vede solo una
bella finestra.

Da evitare: la finestra bianca bruciata (il difetto tecnico più comune, e butta via metà
dell'ambientazione), il muro cieco dall'altra parte del vetro, e il monumento in campo —
massimo uno per video, e mai in una scena d'interni domestica.

### Gli oggetti: ognuno deve dimostrare qualcosa

Ogni oggetto in scena o **prova** la proposizione della scena, o esce dall'inquadratura.

Un oggetto che non c'entra con gli altri non è «vissuto», è disordine, e il disordine
incoerente è uno dei segnali più forti che l'immagine è generata: una tazzina di caffè
sporca accanto a un piatto di riso in bianco non racconta niente, perché nessuno beve un
caffè macchiato durante una dieta in bianco.

Prima di chiudere la lista degli oggetti, passali uno per uno e chiedi di ciascuno: **cosa
dimostra?** Se la risposta è «niente, riempie», va tolto. Tre oggetti coerenti battono
otto oggetti sparsi.

E devono essere **belli come sono davvero le cose di casa**: stoviglie vere e spaiate va
bene, stoviglie brutte no.

---

## Camera

Definisci sempre: inquadratura · angolo · altezza di camera · posizione del soggetto
nel quadro · estetica dell'obiettivo · profondità di campo.

- **50 mm** — lifestyle cinematografico, la resa più vicina all'occhio.
- **85 mm** — prodotto e dettaglio, compressione dello sfondo.
- **35 mm** — quando l'ambiente deve entrare e raccontare, tipico del 16:9.

Non usare la stessa inquadratura su due b-roll consecutivi: è il modo più rapido di far
sembrare una sequenza una serie di fotografie.

**La posizione nel quadro si descrive con la profondità, non con i terzi.** Elencare più
di un «third» nella stessa frase fa consegnare al modello un collage a bande orizzontali
invece di una scena: usa distanze in metri, piani e messa a fuoco (*twelve metres behind
her, thrown far out of focus*), che separano il soggetto dallo sfondo davvero.

---

## Luce

Descrivi sorgente, direzione, temperatura, interazione con l'ambiente, luce di schermo
quando c'è, luce naturale, luce architettonica.

La luce sostiene l'emozione e fa metà del lavoro che il volto non deve fare:

- **pain point** — più spenta, fredda, desaturata; sorgente unica; ombre presenti.
- **desiderio** — più calda, aperta, luminosa; più sorgenti; ombre morbide.

**Non trasformare il pain in horror.** Il buio drammatico su un mal di schiena non fa
identificare: fa cambiare video. La differenza fra le due palette deve essere di due
gradini, non di due mondi.
