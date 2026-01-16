
# Script di Simulazione / Test Logica
# Questo script verifica che la matematica del Line Follower funzioni con input RGB.

# --- 1. Nuove Funzioni Logiche per RGB ---

def estrai_luminosita(rgb_tuple):
    """
    Converte una tupla (r, g, b) in un singolo valore di luminosità (0-100).
    Usiamo la media dei tre canali.
    """
    r, g, b = rgb_tuple
    return (r + g + b) / 3

def is_green(rgb_tuple):
    """
    Determina se la tupla RGB rappresenta il colore VERDE.
    Logica: Il canale Verde deve essere dominante.
    """
    r, g, b = rgb_tuple
    # Evitiamo divisioni per zero o valori troppo bassi (nero)
    if g < 10: 
        return False
        
    # Il verde deve essere significativamente più alto di rosso e blu
    # Esempio: G deve essere almeno il 20% in più di R e B
    if g > r * 1.5 and g > b * 1.5:
        return True
    return False

# --- 2. Copia delle Funzioni di Controllo (Adattate) ---

def calcola_errore(rgb_sx, rgb_dx):
    """
    Calcola l'errore basandosi sulla luminosità estratta dai valori RGB.
    """
    lum_sx = estrai_luminosita(rgb_sx)
    lum_dx = estrai_luminosita(rgb_dx)
    return lum_sx - lum_dx

def calcola_correzione(errore, kp):
    return errore * kp

def calcola_velocita_motori(base_speed, correzione):
    v_sx = base_speed + correzione
    v_dx = base_speed - correzione
    return v_sx, v_dx

# --- 3. Test Cases ---

def esegui_test():
    print("=== INIZIO TEST SIMULATO (RGB) ===")
    base_speed = 150
    kp = 1.2
    
    # Valori tipici simulati (R, G, B)
    BIANCO = (90, 95, 90)
    NERO = (5, 5, 5)
    VERDE = (10, 60, 10) # Verde brillante
    GRIGIO = (50, 50, 50)

    # CASO 1: RETTILINEO (Entrambi su Grigio/Mezzo)
    rgb_sx, rgb_dx = GRIGIO, GRIGIO
    errore = calcola_errore(rgb_sx, rgb_dx)
    corr = calcola_correzione(errore, kp)
    v_sx, v_dx = calcola_velocita_motori(base_speed, corr)
    
    print(f"\n[TEST 1] Rettilineo (SX={rgb_sx}, DX={rgb_dx})")
    print(f"  Luminosità: SX={estrai_luminosita(rgb_sx):.1f}, DX={estrai_luminosita(rgb_dx):.1f}")
    print(f"  Errore: {errore:.1f} (Atteso: 0)")
    if v_sx == v_dx:
        print("  -> OK: Va dritto.")
    else:
        print("  -> FAIL: Dovrebbe andare dritto.")

    # CASO 2: CURVA A DESTRA (SX su Bianco, DX su Nero)
    # L'auto è troppo a sinistra.
    rgb_sx, rgb_dx = BIANCO, NERO
    errore = calcola_errore(rgb_sx, rgb_dx)
    corr = calcola_correzione(errore, kp)
    v_sx, v_dx = calcola_velocita_motori(base_speed, corr)
    
    print(f"\n[TEST 2] Curva a Destra (SX={rgb_sx}, DX={rgb_dx})")
    print(f"  Luminosità: SX={estrai_luminosita(rgb_sx):.1f}, DX={estrai_luminosita(rgb_dx):.1f}")
    print(f"  Errore: {errore:.1f} (Atteso: Positivo)")
    if v_sx > v_dx:
        print("  -> OK: Sterza a destra.")
    else:
        print("  -> FAIL: Errore logica sterzata.")

    # CASO 3: CURVA A SINISTRA (SX su Nero, DX su Bianco)
    # L'auto è troppo a destra.
    rgb_sx, rgb_dx = NERO, BIANCO
    errore = calcola_errore(rgb_sx, rgb_dx)
    corr = calcola_correzione(errore, kp)
    v_sx, v_dx = calcola_velocita_motori(base_speed, corr)
    
    print(f"\n[TEST 3] Curva a Sinistra (SX={rgb_sx}, DX={rgb_dx})")
    print(f"  Luminosità: SX={estrai_luminosita(rgb_sx):.1f}, DX={estrai_luminosita(rgb_dx):.1f}")
    print(f"  Errore: {errore:.1f} (Atteso: Negativo)")
    if v_sx < v_dx:
        print("  -> OK: Sterza a sinistra.")
    else:
        print("  -> FAIL: Errore logica sterzata.")

    # CASO 4: RILEVAMENTO VERDE
    print(f"\n[TEST 4] Rilevamento Verde")
    # Test SX Verde
    if is_green(VERDE):
        print(f"  Verde perfetto {VERDE} -> Rilevato: SI (OK)")
    else:
        print(f"  Verde perfetto {VERDE} -> Rilevato: NO (FAIL)")

    # Test Falso Positivo (Bianco non deve essere verde)
    if is_green(BIANCO):
        print(f"  Bianco {BIANCO} -> Rilevato: SI (FAIL)")
    else:
        print(f"  Bianco {BIANCO} -> Rilevato: NO (OK)")
        
    print("\n=== FINE TEST ===")

if __name__ == "__main__":
    esegui_test()
