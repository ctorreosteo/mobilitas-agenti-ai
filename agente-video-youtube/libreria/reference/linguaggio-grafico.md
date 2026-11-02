# Il linguaggio grafico dei video

Copia leggibile di `motore/motore/brand.json` → `video.linguaggio` (la fonte è quella: se cambia lì, questo file si rigenera). Viene dallo studio delle reference elencate in `catalogo.md`, fatto in laboratorio: le reference fissano il **livello**, non si copiano.

> Riccardo, 28/10/2026 (fase 7b rivista), dallo studio di libreria/reference/ (14 clip, catalogo in libreria/reference/catalogo.md). Le reference fissano il livello, non si copiano: per ogni video si sceglie cosa serve al contenuto e si inventano grafiche nuove dello stesso livello.

## I due mondi

- **accanto a lui:** lui inquadrato con il lato libero ampio (punch-in o spostamento di camera all'arrivo dell'elemento); elementi accanto a lui, mai sul volto o sulle mani
- **scena scura:** a tutto schermo, fondo blu profondo -> blu notte con una texture sottile (grana fine e curve di livello panna al 4-6%, o luci sfocate); la camera si muove fra gli elementi: avanza lenta (circa 5% in 7 s) o scorre fra due punti in 0,8 s
- **passaggio:** taglio netto o lampo di luce panna/verde di 3-4 frame, mai una dissolvenza lunga; si alternano nel video, nessuno dei due per più di 2-3 momenti di fila

## Le famiglie di grafiche

- **frase parola per parola:** testo che arriva parola per parola sulla voce: ogni parola nasce panna al 35% e sfocata e in 2-3 frame diventa piena con il suo bagliore; la parola chiave in verde (solo sul blu) o in peso 900
- **lista voce per voce:** voci accanto a lui con un segno (punto verde luminoso o icona lineare), testo che si scrive da sinistra in 4-6 frame sulle parole dette; senza pannello, con ombra
- **etichette luminose:** pillole blu notte con bordo e bagliore verdi, testo panna 700; barrate da una riga che corre da sinistra in 3 frame sulla parola che le smonta
- **fumetti:** fumetti di chat panna a gradiente leggero con coda, ombra di contatto e luce interna, testo blu notte 700; nascono sfocati e scalati a 0,85, nitidi in 4 frame, quelli prima salgono
- **card con spessore:** card blu notte con bordo superiore chiaro (spessore), ombra di contatto + ombra morbida, texture fine; arrivano una ogni 0,25 s; icona o disegno Servier con luce verde
- **vetro:** pannello smerigliato che sfoca lo studio vero dietro, bordo panna sottile con riflesso, contenuto che arriva dopo il bordo
- **numeri:** cifre che scorrono come un contachilometri con sfocatura verticale e frenano sulla parola
- **anatomia:** disegno Servier in una card (modelli approvati: l'animazione del meccanismo a 1:21 e la card della colonna «spesso lavora di più» dell'anteprima 7b) o in una scena scura con la camera che va sulla parte nominata
- **oggetti veri:** telefoni, foto e interfacce credibili (iPhone realistico, foto vere con il viso tagliato fuori)

## Movimento

- **entrata s:** 0.25, 0.4
- 3-5 frame a 12 fps = 6-10 frame a 25 fps, con la sfocatura che si scioglie e power3.out; piccolo rimbalzo solo su fumetti e pillole (back.out <= 1.4)
- **parola frame 25:** 4, 6
- **sfasamento s:** 0.25
- **uscita:** con lo stacco o in 2-3 frame (4-6 a 25 fps)
- **camera:** nelle scene scure sempre in movimento; accanto a lui punch-in all'arrivo dell'elemento

## Luce

- **bagliore:** gli elementi sulle scene scure emettono luce: bagliore morbido dello stesso colore (verde #72FA93 o panna), 2 strati (stretto 8-12 px + largo 30-50 px)
- **scritte bianche sulla scena:** ombra morbida forte dietro ogni scritta bianca sopra il girato: 0 4px 14px blu profondo al 70% + 0 0 44px blu profondo al 55% (più di prima, regola del 28/10/2026)
- **sfondo:** quando arriva un elemento grande, lo sfondo si scurisce (-20/30%) e si sfoca in 3 frame

## Profondità

card con spessore e ombra, vetro che lascia vedere lo studio, testo dietro di lui con la sagoma di Vision, camera che si muove nello spazio delle scene scure

## Sincronia

nessun elemento arriva prima della sua parola; liste voce per voce, testo parola per parola, numeri che frenano sulla parola, barre che barrano sulla parola

## Colore

un solo accento forte per video: per Mobilitas il verde #72FA93, come luce e accento, solo sul blu; tutto il resto panna e blu

## Font

Montserrat; 800-900 per le parole grandi, 600-700 per fumetti ed etichette, 400 per il corpo dei pannelli
