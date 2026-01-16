# EV3 Proportional Line Follower con Gestione Incroci 🤖

Questo progetto implementa un **Line Follower** avanzato per LEGO Mindstorms EV3 utilizzando **MicroPython**.

A differenza dei line follower classici, questo codice utilizza una **logica RGB unificata** per gestire contemporaneamente:
1.  **Guida Proporzionale (PID)** sulla linea.
2.  **Rilevamento Marker Verdi** per svolte automatiche agli incroci.

## 🚀 Caratteristiche
-   **Sensore RGB Unificato**: Utilizza la modalità `rgb()` per leggere colore e luminosità in un unico ciclo, eliminando la latenza del cambio modalità sensore.
-   **Guida Fluida**: Calcola la luminosità media `(R+G+B)/3` per un controllo proporzionale preciso.
-   **Gestione Incroci (Verde)**: Rileva marker verdi a destra o sinistra e **esegue automaticamente svolte a 90°**.
-   **Priorità di Azione**: Il rilevamento del verde ha priorità sulla guida, prevenendo errori di sterzata quando si passa sopra i marker colorati.

## 🛠️ Hardware Richiesto
-   **LEGO Mindstorms EV3 Brick**
-   **2 Motori Grandi**:
    -   Sinistro: Porta **B**
    -   Destro: Porta **C**
-   **2 Sensori di Colore**:
    -   Sinistro: Porta **S1**
    -   Destro: Porta **S4**

## ⚙️ Come Funziona
Il robot opera in un loop continuo che:
1.  Legge i valori **RGB** grezzi da entrambi i sensori.
2.  **Verifica Verde**: Se la componente Verde è dominante (`G > R*1.5` e `G > B*1.5`):
    -   Ferma i motori.
    -   Esegue una **svolta a 90°** nella direzione del sensore (Tank Turn).
    -   Riprende la guida.
3.  **Guida Linea**: Se non c'è verde, calcola l'errore di luminosità:
    ```python
    luminosita = (r + g + b) / 3
    errore = lum_sinistra - lum_destra
    ```
    E applica la correzione proporzionale ai motori.

## 📥 Installazione
1.  Clona questo repository.
2.  Apri la cartella con **VS Code** e l'estensione **LEGO EV3 MicroPython**.
3.  Collega il tuo EV3 al PC.
4.  Esegui il codice (`main.py`).

## 📊 Calibrazione
Puoi modificare le costanti in `main.py` per adattare il robot alla tua pista:

### Guida
-   `VELOCITA_BASE` (Default: 150): Velocità di crociera.
-   `GUADAGNO_KP` (Default: 1.2): Reattività dello sterzo. Se il robot "sculetta" (oscilla), abbassa questo valore.

### Svolte
-   `GRADI_ROTAZIONE_90` (Default: 230): **IMPORTANTE**. Questo valore determina di quanto devono girare le ruote per far ruotare il robot di 90° fisici.
    -   Se il robot gira **troppo** (oltre 90°), **diminuisci** questo valore (es. 210).
    -   Se il robot gira **poco** (meno di 90°), **aumenta** questo valore (es. 250).
