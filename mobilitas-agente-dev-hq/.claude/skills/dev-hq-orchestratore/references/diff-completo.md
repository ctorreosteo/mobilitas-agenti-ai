# Costruire il diff che i revisori devono vedere

**`git diff` da solo mente.** È il modo più facile di far girare a vuoto un'intera Fase 4: i revisori ricevono meno di quello che hai scritto, approvano ciò che non hanno visto, e il 100% non vale niente.

Successo davvero, alla prima esecuzione dell'agente.

---

## I due buchi di `git diff`

`git diff` mostra **solo le modifiche non in staging a file già tracciati**. Restano fuori due categorie, e sono proprio quelle di un task di sviluppo:

| Cosa | Perché `git diff` non la vede | Come si presenta in `git status --porcelain` |
|------|-------------------------------|---------------------------------------------|
| **File nuovi** | git non li conosce ancora | `?? percorso` |
| **Modifiche in staging** | sono nell'indice, non nel working tree | `M `, `A `, `R ` (lettera in **prima** colonna) |

Il secondo è il più insidioso: basta che qualcuno abbia fatto `git add` — Carlos, un tool, un'abitudine — e `git diff` diventa **completamente vuoto** mentre il lavoro c'è tutto.

Misurato sul task 869cng430: `git diff` restituiva **0 righe**, `git diff HEAD` sei file fra cui la migrazione Flyway, cioè il file più importante del task.

---

## La ricetta corretta

Tre pezzi, tutti e tre obbligatori:

```bash
FE=/Users/carlitos/mobilitas-frontend
BE=/Users/carlitos/mobilitas-backend

for R in "$FE" "$BE"; do
  echo "########## $R ##########"

  # 1. il quadro completo: staged, non staged, non tracciati
  echo "--- STATO ---"
  git -C "$R" status --porcelain

  # 2. TUTTE le modifiche a file tracciati, staged o no
  echo "--- MODIFICHE (vs ultimo commit) ---"
  git -C "$R" diff HEAD

  # 3. i file NUOVI, che nessun diff mostra: contenuto per intero
  echo "--- FILE NUOVI ---"
  git -C "$R" status --porcelain | awk '$1=="??"{print $2}' | while read -r f; do
    echo "===== $f ====="
    cat "$R/$f"
  done
done
```

- **`git diff HEAD`** invece di `git diff`: prende staged **e** non staged.
- **I file nuovi si mostrano col contenuto**, perché non esistono in nessun diff.
- **`git -C <path>`** invece di `cd`: vedi sotto, non è un dettaglio.

## Verifica prima di consegnare ai revisori

Conta i file e confronta. Se il diff che stai per consegnare copre meno file di quelli che `git status` elenca, **fermati**: stai per far revisionare il vuoto.

```bash
git -C "$R" status --porcelain | wc -l          # quanti file toccati
git -C "$R" diff HEAD --stat | tail -1          # quanti nel diff
git -C "$R" status --porcelain | grep -c '^??'  # quanti nuovi (da mostrare a parte)
```

I primi devono tornare: `file toccati = file nel diff + file nuovi`.

---

## Usa `git -C`, mai `cd`

La working directory **persiste fra i comandi**, e con due repository è una trappola: un `cd` fatto tre comandi prima ti fa leggere il repo sbagliato senza nessun errore. Nella prima esecuzione dell'agente è successo **due volte**, e in un caso ha prodotto un elenco di file toccati completamente sbagliato — attribuiti al frontend mentre erano del backend.

Non è un problema estetico: significa dire a Carlos che hai modificato file che non hai toccato, o revisionare il repo sbagliato.

```bash
git -C /Users/carlitos/mobilitas-frontend status --porcelain   # sì
cd /Users/carlitos/mobilitas-frontend && git status             # no
```

Per i comandi che **non** accettano `-C` (`npm`, `./mvnw`), usa una subshell, così il `cd` muore con lei:

```bash
( cd /Users/carlitos/mobilitas-frontend && npm run typecheck )
( cd /Users/carlitos/mobilitas-backend  && ./mvnw -q -DskipTests compile )
```

---

## Il dossier — dove finisce tutto questo

**I revisori non possono eseguire questa ricetta:** hanno `tools: Read, Grep, Glob`, niente Bash. La esegui tu, una volta per giro, e ne scrivi il risultato su file.

```
/tmp/dev-hq-dossier/<task-id>-giro<n>.md
```

Non è solo comodità. Nove revisori che si ricostruivano il diff per conto loro erano **nove ricostruzioni diverse in nove momenti diversi**: il requisito «i nove hanno visto lo stesso stato del codice», da cui dipende il valore dell'approvazione al 100%, non era garantito da niente. Con un file solo, lo è.

### Le sei sezioni, in quest'ordine

| # | Sezione | Contenuto |
|---|---------|-----------|
| 1 | **Task** | id, titolo, url, descrizione integrale, commenti se ce ne sono |
| 2 | **Piano** | il percorso `/tmp/dev-hq-piani/<task-id>.md`, e il piano incollato per intero |
| 3 | **Stato** | `git -C "$R" status --porcelain`, per repo |
| 4 | **Diff** | `git -C "$R" diff HEAD`, per repo |
| 5 | **File nuovi** | percorso e **contenuto integrale** di ogni `??` |
| 6 | **Verifiche meccaniche** | typecheck: solo gli errori **nuovi** rispetto alla baseline · lint: il confronto per regola · backend: l'esito di `./mvnw -q -DskipTests compile` |

La sezione 6 è quella che i revisori non possono produrre da soli, ed è quella che rende inutile dargli Bash. Se la ometti, `revisore-logica-frontend` e `revisore-regressioni` non hanno i numeri su cui giudicare, e il referto che ti torna dirà — correttamente — che il dossier è incompleto. Il metodo per produrla sta in [verifiche.md](verifiche.md).

### Nel messaggio al subagent

Bastano tre cose, perché il resto è nel dossier:

1. **Il percorso del dossier.**
2. **L'elenco esplicito dei file nuovi** — sono quelli che si perdono, ripeterli costa una riga.
3. **Quale repo lo riguarda**, così chiude subito se non è materia sua.

**Non incollare il diff nel messaggio.** Se è nel file, tutti leggono lo stesso; se è nel messaggio, hai due copie che possono divergere. E un dossier grande non è un problema: il revisore lo apre a pezzi con gli strumenti che ha.
