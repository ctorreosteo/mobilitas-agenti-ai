# Criticità GDPR — MobilitasHQ

> **Stato**: nessun audit ancora eseguito.
>
> Questo file viene compilato dal comando `/report` dopo `/sync` e `/audit`.
> Conterrà l'elenco delle non conformità e di **ciò che manca da implementare** nel gestionale.
> L'agente non modifica il codice: qui si segnala soltanto.

---

## Come leggere questo documento (una volta compilato)

| Severità | Significato |
|----------|-------------|
| **CRITICA** | violazione in atto su dati sanitari o esposizione concreta — intervenire subito |
| **ALTA** | obbligo GDPR non soddisfatto, senza esposizione immediata |
| **MEDIA** | obbligo soddisfatto in modo parziale o non dimostrabile |
| **BASSA** | buona prassi non adottata |
| **DA VERIFICARE** | non decidibile dal codice: serve un'informazione del Titolare |

Ogni criticità ha un **ID stabile** (`GDPR-001`, …) che resta invariato tra un audit e il
successivo, così da poterne seguire la chiusura nel tempo.

---

## Sezioni previste

1. **Sintesi** — conteggio per severità e aree principali
2. **Cosa è stato risolto in questa sessione** — documentazione aggiornata o creata
3. **Criticità aperte** — una scheda per voce, con evidenza `file:riga`
4. **Domande al Titolare** — informazioni necessarie per chiudere le voci *DA VERIFICARE*
5. **Metodo e limiti dell'audit** — cosa non è verificabile dal solo codice

---

*Documento tecnico da validare con DPO/consulente privacy. Non costituisce parere legale.*
