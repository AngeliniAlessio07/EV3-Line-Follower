
# Script di Simulazione / Test Logica
# Questo script verifica che la matematica del Line Follower funzioni come previsto.

# --- 1. Copia delle Funzioni Logiche da main.py ---

def calcola_errore(val_sx, val_dx):
    # Simuliamo reflection() passando direttamente i valori interi
    return val_sx - val_dx

def calcola_correzione(errore, kp):
    return errore * kp

def calcola_velocita_motori(base_speed, correzione):
    v_sx = base_speed + correzione
    v_dx = base_speed - correzione
    return v_sx, v_dx

# --- 2. Test Cases ---

def esegui_test():
    print("=== INIZIO TEST SIMULATO ===")
    base_speed = 150
    kp = 1.2
    
    # CASO 1: RETTILINEO (Entrambi su Grigio/Bianco uguale)
    # SX: 50, DX: 50
    s_sx, s_dx = 50, 50
    errore = calcola_errore(s_sx, s_dx)
    corr = calcola_correzione(errore, kp)
    v_sx, v_dx = calcola_velocita_motori(base_speed, corr)
    
    print(f"\n[TEST 1] Rettilineo (Luce {s_sx}, {s_dx})")
    print(f"  Errore: {errore} (Atteso: 0)")
    print(f"  Velocità: SX={v_sx:.1f}, DX={v_dx:.1f}")
    if v_sx == v_dx == base_speed:
        print("  -> OK: Va dritto.")
    else:
        print("  -> FAIL: Dovrebbe andare dritto.")

    # CASO 2: CURVA A DESTRA (SX vede Bianco, DX vede Nero)
    # L'auto è troppo a sinistra, deve girare a destra.
    # SX: 90 (Bianco), DX: 10 (Nero)
    s_sx, s_dx = 90, 10
    errore = calcola_errore(s_sx, s_dx)
    corr = calcola_correzione(errore, kp)
    v_sx, v_dx = calcola_velocita_motori(base_speed, corr)
    
    print(f"\n[TEST 2] Curva a Destra (SX={s_sx}, DX={s_dx})")
    print(f"  Errore: {errore} (Atteso: Positivo)")
    print(f"  Velocità: SX={v_sx:.1f}, DX={v_dx:.1f}")
    
    if v_sx > v_dx:
        print("  -> OK: Motore SX più veloce, gira a destra.")
    else:
        print("  -> FAIL: Dovrebbe girare a destra.")

    # CASO 3: CURVA A SINISTRA (SX vede Nero, DX vede Bianco)
    # L'auto è troppo a destra, deve girare a sinistra.
    # SX: 10 (Nero), DX: 90 (Bianco)
    s_sx, s_dx = 10, 90
    errore = calcola_errore(s_sx, s_dx)
    corr = calcola_correzione(errore, kp)
    v_sx, v_dx = calcola_velocita_motori(base_speed, corr)
    
    print(f"\n[TEST 3] Curva a Sinistra (SX={s_sx}, DX={s_dx})")
    print(f"  Errore: {errore} (Atteso: Negativo)")
    print(f"  Velocità: SX={v_sx:.1f}, DX={v_dx:.1f}")
    
    if v_sx < v_dx:
        print("  -> OK: Motore DX più veloce, gira a sinistra.")
    else:
        print("  -> FAIL: Dovrebbe girare a sinistra.")

    print("\n=== FINE TEST ===")

if __name__ == "__main__":
    esegui_test()
