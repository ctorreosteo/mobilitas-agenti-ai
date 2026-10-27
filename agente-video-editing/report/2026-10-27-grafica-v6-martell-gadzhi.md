# Grafica v6: piano (27/10/2026) — livello Dan Martell / Iman Gadzhi

Richiesta di Carlos: «Prendi come esempio Dan Martell e Iman Gadzhi, sono dei geni delle
infografiche nei video YouTube. Voglio che il mio agente sappia editare a quel livello.»

## Cosa fanno loro che noi non facciamo ancora

La v5 ha già titoli dietro, dieci infografiche, scene a tutto schermo, sottotitoli cinetici.
Quello che manca è la **grammatica** dei due canali, non un altro tipo di card:

| firma | chi | cosa vuol dire per noi |
|---|---|---|
| **il framework che si costruisce** | Martell | il ragionamento ha una forma (passi, ciclo, matrice, piramide) e la forma si disegna pezzo per pezzo mentre lo dice |
| **il richiamo del framework** | Martell | più avanti nel video la stessa forma torna, piccola, con acceso il pezzo di cui sta parlando: lo spettatore sa sempre dove si trova |
| **la lavagna con la faccia** | Martell | lei in una finestra di lato, il framework sul resto del quadro: si vede il volto anche durante lo schema |
| **il ritaglio davanti alla grafica** | Gadzhi | lei esce dalla stanza: la sagoma resta in primo piano, spostata su un lato, con un filo di luce; la grafica sta dietro e accanto a lei |
| **la parola che sbatte** | entrambi | una parola chiave arriva grande accanto a lei, evidenziata a pennarello, con un colpo di camera |
| **i segni a mano** | Martell | cerchi, frecce, riquadri a pennarello che si disegnano sopra il girato e indicano una cosa nel set (il modello anatomico) |
| **la frusta** | Gadzhi | ingresso/uscita delle scene con uno strappo laterale sfocato invece della zoomata |
| **la pellicola** | Gadzhi | grana fine animata su tutto il video, tenuta bassa |

## Cosa entra nel motore (regia.json resta compatibile)

1. `scene[].lei`: `dietro` (com'è oggi), `finestra` (Martell), `davanti` (Gadzhi, usa le sagome).
2. Nuovi tipi di scena: `passi`, `ciclo`, `matrice`, `piramide`, `richiamo` (`di`: l'`id` della scena,
   `acceso`: la voce).
3. `segni`: `parola` (la parola che sbatte, dalla frase), `cerchio`, `freccia`, `riquadro`
   (`dove` in coordinate della sorgente 0-1: seguono il taglio di camera e la spinta).
4. `./mve griglia <slug> <m:ss>`: il fotogramma della sorgente con la griglia 0-1, per scegliere `dove`.
5. `finitura`: `grana` (default 0, consigliato 0,5) e `frusta` per le scene.
6. Suoni: pennarello che scrive, colpo della parola, strappo della frusta, scatto dei nodi.
7. `sagome` calcola anche le finestre delle scene `davanti`; `inquadra` tiene il largo durante i segni
   e mette la parola sul lato libero dal volto.
8. `scene`, `segni`, `finitura` entrano nell'impronta di `grafica.json` (prima `scene` mancava:
   cambiare una scena non segnava la grafica da rifare).

## Regole che restano

Parole sue, nessuna promessa, menta unico accento, il movimento finisce entro ~1,6 s.
Il pennarello è un **tratto**, non un font: la scritta resta Montserrat/Plex Mono.

## Come si verifica

Banco di prova `videos/YT_TOFU_02-v2`: regia con un framework + richiamo, una scena `davanti`,
segni e parole; `grafica`, `inquadra`, `sagome`, `anteprima`, fogli `movimento.jpg`,
`finale --limite` su un tratto, si guardano i fotogrammi.
