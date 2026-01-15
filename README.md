# EV3 Proportional Line Follower 🤖

Questo progetto implementa un **Line Follower** (robot segui-linea) per LEGO Mindstorms EV3 utilizzando **MicroPython**.

La particolarità di questo codice è l'utilizzo di un **controllo proporzionale** basato su funzioni matematiche, evitando l'uso di lunghe catene di `if/else` per la gestione dei motori. Questo garantisce un movimento molto più fluido e preciso rispetto alla classica logica "a scatti" (line follower a stati discreti).

## 🚀 Caratteristiche
-   **Logica Proporzionale (P-Controller)**: La velocità di sterzata è calcolata in base alla differenza di luce letta dai sensori. Più il robot è fuori linea, più agisce correggendo la traiettoria.
-   **Guida Differenziale**: Modula la velocità dei singoli motori (accelera quello esterno, rallenta quello interno) per curve morbide.
-   **Codice Funzionale**: Strutturato in funzioni pure (`calcola_errore`, `calcola_velocita`) per massima chiarezza e manutenibilità.

## 🛠️ Hardware Richiesto
-   **LEGO Mindstorms EV3 Brick**
-   **2 Motori Grandi**:
    -   Sinistro: Porta **B**
    -   Destro: Porta **C**
-   **2 Sensori di Colore**:
    -   Sinistro: Porta **S1**
    -   Destro: Porta **S4**

## ⚙️ Come Funziona
Il nucleo del controllo risiede in questa formula:
```python
errore = luce_sinistra - luce_destra
correzione = errore * GUADAGNO_KP

velocita_sinistra = VELOCITA_BASE + correzione
velocita_destra   = VELOCITA_BASE - correzione
```
Se il sensore sinistro vede "più bianco" del destro, il robot sterza a destra proporzionalmente all'errore, mantenendosi centrato sulla linea.

## 📥 Installazione
1.  Clona questo repository.
2.  Apri la cartella con **VS Code** e l'estensione **LEGO EV3 MicroPython**.
3.  Collega il tuo EV3 al PC.
4.  Esegui il codice (`main.py`).

## 📊 Calibrazione
Puoi modificare le costanti in `main.py` per adattare il robot alla tua pista:
-   `VELOCITA_BASE`: Aumenta per andare più veloce (se la pista è semplice).
-   `GUADAGNO_KP`: Aumenta per curve più reattive, diminuisci se il robot oscilla troppo ("wobble").

---
