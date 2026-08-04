# I Cinque Modelli Osteopatici — l'impalcatura di ogni procedura

Questo è il **telaio portante** di ogni procedura Mobilitas: i **cinque modelli osteopatici**, il linguaggio riconosciuto della professione. Sostituisce, come spina dorsale, il vecchio impianto "Piramide del Comando / Sistema Dominante" — che **non sparisce**, ma scende a fare il **Motore Clinico** (lo strato di ragionamento implicito, vedi `fase-0-piramide-del-comando.md`).

## Perché l'impalcatura sono i modelli e non il Sistema Dominante

La regola che governa questa inversione, e va capita prima di scrivere:

> **La procedura deve risolvere i problemi in studio. La scientificità non è il fine: è la corazza che impedisce a chi legge di attaccarla.**

- I **cinque modelli** sono il linguaggio **ufficiale** dell'osteopatia (formazione, benchmark internazionali), ognuno ancorato alla fisiologia e con un suo grado di evidenza. Come **struttura visibile** reggono il confronto con un medico o un fisioterapista: non danno appigli.
- Il **Sistema Dominante** (iceberg, lesione primaria, CC/CP di Stecco, road map) è il **motore clinico** che rende l'osteopata efficace in stanza — ma poggia su meccanismi non validati. Come *ragionamento interno* è prezioso e inattaccabile; come *spina dorsale pubblica* era il fianco scoperto. Per questo va **dentro**, non in vetrina.

Divisione dei ruoli, netta:

| | Cosa fa | Come si presenta |
| --- | --- | --- |
| **Cinque modelli** (impalcatura) | dicono **su cosa** lavori e **con quanta evidenza** | struttura visibile, Parte 0 |
| **Sistema Dominante** (Motore Clinico) | dice **come scegli** su quale modello agire per primo in *questo* paziente | ragionamento implicito, in coda alla Parte 0 |

**Il lucchetto della corazza:** l'unica cosa che fa "attaccare" un lettore critico è un **claim gonfiato** — affermare come provato ciò che provato non è. Se il Motore Clinico lo presenti come ragionamento (e non come prova) e dichiari onestamente l'evidenza di ogni modello, non lasci appigli. La corazza funziona **solo** se non resta fuori un claim gonfiato.

## I cinque modelli

Per ognuno, calato sulla condizione: **cosa governa**, gli **attori**, i **segnali che ti dicono che pesa** in questo paziente, e **l'evidenza / lo scope**.

1. **Biomeccanico-Strutturale** — postura, movimento, catene fasciali, disfunzione somatica muscolo-scheletrica; per le condizioni viscerali qui rientra anche la **meccanica dell'organo/della barriera** (mobilità, legamenti sospensori). *Nota di scope importante:* i cinque modelli **non prevedono un "modello viscerale" separato*; il lavoro viscerale si esprime dentro il biomeccanico (mobilità) e il neurologico (riflesso viscero-somatico). Tenerlo lì ci mantiene nel linguaggio riconosciuto.
2. **Respiratorio-Circolatorio** — diaframma come pompa e regolatore pressorio, dinamica dei fluidi, ritorno venoso-linfatico ("la legge dell'arteria"). Spesso il modello a evidenza migliore.
3. **Neurologico** — equilibrio autonomico, nocicezione, segmenti facilitati, riflessi viscero-somatici e somato-viscerali, nervo vago e frenico. Il meccanismo è spesso solido; l'effetto del **tocco** sull'autonomico va dichiarato plausibile, non dimostrato.
4. **Metabolico-Energetico** — economia energetica, nutrizione, peso, carico allostatico, sonno. Contiene le **leve di stile di vita** ad alta evidenza (peso, pasti, trigger): si **segnalano** e si **rinvia** a medico/dietista — non sono atto osteopatico.
5. **Comportamentale-Biopsicosociale** — fattori psicosociali, stress, credenze, aspettative, aderenza; asse intestino-cervello. Effetto di co-regolazione e counseling, non cura dimostrata.

Non tutti pesano per tutte le condizioni: dichiara l'evidenza **modello per modello**, e non gonfiare i deboli per far numero (l'onestà del modello debole rafforza la corazza, non la indebolisce).

La descrizione operativa dettagliata di ciascun modello vive anche in `direttore-osteopatico-modelli/references/cinque-modelli.md` (usata dal revisore `modelli`); **questo file è canonico per l'architettura** (impalcatura / motore / lucchetto), quello per il dettaglio d'uso dei singoli modelli. Se divergono, vince questo sull'architettura.

## La grammatica del lucchetto — come si dichiara l'evidenza

Ogni modello, nella Parte 0, **chiude con una riga `Evidenza:`** che usa una di queste etichette (coerenti col grading dei sottotipi di efficacia):

- **ALTA / BUONA** — RCT o revisioni sistematiche solide, con fonte citata.
- **MODERATA** — razionale forte + evidenza parziale o indiretta.
- **PLAUSIBILE (non dimostrata)** — meccanismo fisiologico coerente, nessuno studio diretto sul punto.
- **IPOTESI / RAGIONAMENTO** — cornice di ragionamento clinico (tipicamente il Motore Clinico: CC/CP, lesione primaria, effetto del tocco sull'autonomico). Si scrive come "si ipotizza / è coerente con", **mai** come fatto.

La regola è una sola: **un meccanismo non validato non si scrive mai come provato.** È questo il lucchetto — la corazza dei cinque modelli tiene solo se nessuna riga la fora con un claim gonfiato.

## Come struttura la procedura

- **Parte 0 = i cinque modelli applicati alla condizione** (impalcatura visibile). Per ciascuno: cosa governa, attori, segnali di dominanza, evidenza/scope.
- **In coda alla Parte 0 = il Motore Clinico** (`fase-0-piramide-del-comando.md`): il ragionamento del Sistema Dominante — iceberg, tre chiavi, road map, re-test, CC/CP — come strato **implicito**. *Implicito, in concreto, significa tre cose:* (a) sta **in coda** alla Parte 0, dopo i cinque modelli, non come sua apertura; (b) è introdotto col framing *"ecco come decido su quale modello agire per primo"*, **senza intestazioni-dottrina in vetrina** (niente "La Piramide del Comando", "La Bibbia", "La lesione primaria" come titoli-manifesto); (c) è scritto come **ragionamento/ipotesi**, mai come meccanismo dimostrato. Il ragionamento c'è tutto e guida le mani: semplicemente non è la struttura che il lettore esterno vede per prima.
- **Efficacia / sottotipi:** pattern di dominanza **di modello**, non etichette diagnostiche.
- **Parte IV:** l'approfondimento dei modelli (le vecchie sezioni "Sistema X" si mappano sui modelli; fornisci una mappa modello → sezione).
- **Piano di trattamento:** costruito attorno al **modello dominante**, dentro l'impalcatura dei cinque.

## Rapporto con il vecchio impianto (i sei sistemi)

I "sei sistemi" della vecchia Piramide si ridistribuiscono sui cinque modelli: Neurologico→Neurologico; Psico-Emotivo→Comportamentale; Respiratorio→Respiratorio-Circolatorio; Viscerale→Biomeccanico (meccanica) + Neurologico (riflesso); Fasciale/Posturale→Biomeccanico; Trauma→**non è un modello**, resta un *modificatore* da cercare nell'anamnesi (road map del Motore Clinico), non una sezione. Il Metabolico-Energetico, prima assente, entra a pieno titolo come quinto modello.
