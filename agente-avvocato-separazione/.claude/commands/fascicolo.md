---
description: Ricostruisce fatti, documenti e cronologia del caso. Nessuna strategia prima di questo.
argument-hint: "[pratica]"
---

Costruisci il fascicolo. **È il primo comando, sempre**: una strategia costruita prima di sapere
cosa si può provare è un esercizio letterario.

## Procedura

1. **Leggi `fascicolo/_dati/caso.json`.** Elenca i campi `null`: sono le domande da fare al
   cliente, e vanno fatte **in un solo giro**.

2. **Inventaria i documenti** presenti in `fascicolo/prove/`. Per ciascuno: cos'è, che data porta,
   quale fatto prova. **Aprili**: non fidarti del nome del file.

3. **Compila `fascicolo/_dati/timeline.md`** in append. Una riga per fatto: data, fatto, fonte,
   etichetta di prova. Nessun aggettivo — «ha urlato» non è un fatto, «messaggio vocale delle
   22:14, all. 12» lo è.

4. **Compila la sezione dei fatti sfavorevoli.** Quello che la controparte userà, scritto da noi
   prima che lo scriva lei, con la risposta accanto e la prova della risposta. Se questa sezione
   resta vuota, il fascicolo non è finito: **ogni caso ne ha**.

5. **Mappa i buchi.** Per ogni fatto importante che oggi è `ALLEGABILE` o `NON SOSTENIBILE`:
   quale documento lo renderebbe `PROVATO`, dove si trova, chi lo detiene, e **entro quando va
   acquisito**. È l'output più prezioso del comando.

6. **Verifica il fronte penale.** Denunce ricevute o sporte, indagini note, misure. Per ciascuna:
   data, reato ipotizzato, autorità, stato, difensore nominato.

## Chiusura

Riporta all'utente:

- **Cosa possiamo provare oggi**, con carta in mano.
- **Cosa dobbiamo procurarci**, con priorità e scadenza. Le voci che il tempo rende impossibili
  vanno per prime.
- **I tre fatti più sfavorevoli** e come li affrontiamo.
- **Le informazioni che solo il cliente può dare**, in elenco numerato.

Poi indica il comando successivo: `/strategia`.
