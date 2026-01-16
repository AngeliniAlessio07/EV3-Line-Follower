
import time

# --- LOGICA DEL ROBOT (Copiata/Importata da main.py/verification_test.py) ---
# Copiamo le funzioni per assicurarci di testare ESATTAMENTE la stessa logica

def estrai_luminosita(rgb_tuple):
    r, g, b = rgb_tuple
    return (r + g + b) / 3

def is_green(rgb_tuple):
    r, g, b = rgb_tuple
    if g < 10: return False 
    if g > r * 1.5 and g > b * 1.5:
        return True
    return False

def calcola_errore(rgb_sx, rgb_dx):
    green_sx = is_green(rgb_sx)
    green_dx = is_green(rgb_dx)
    
    if green_sx or green_dx:
        return 0 # Fix: Ignora errore su verde
        
    lum_sx = estrai_luminosita(rgb_sx)
    lum_dx = estrai_luminosita(rgb_dx)
    return lum_sx - lum_dx

def calcola_correzione(errore, kp):
    return errore * kp

def calcola_velocita_motori(base_speed, correzione):
    v_sx = base_speed + correzione
    v_dx = base_speed - correzione
    return v_sx, v_dx

# --- DEFINIZIONE COLORI BASE ---
NERO  = (5, 5, 5)
GRIGIO = (50, 50, 50) # Sulla linea (bordo)
BIANCO = (90, 95, 90)
VERDE  = (10, 60, 10)

# --- DEFINIZIONE PERCORSO DIGITALE ---
# Ogni step è una tupla: (Descrizione, RGB_SX, RGB_DX)
PERCORSO = [
    ("START: Rettilineo Perfetto", GRIGIO, GRIGIO),
    ("Rettilineo: Leggera deriva a SX", (60, 60, 60), (40, 40, 40)),
    ("CURVA A DX: Inizio (SX vede Bianco)", BIANCO, GRIGIO),
    ("CURVA A DX: Centro (SX Bianco, DX Nero)", BIANCO, NERO),
    ("CURVA A DX: Uscita (Si raddrizza)", GRIGIO, GRIGIO),
    ("Rettilineo", GRIGIO, GRIGIO),
    ("CURVA A SX: Inizio (DX vede Bianco)", GRIGIO, BIANCO),
    ("CURVA A SX: Centro (SX Nero, DX Bianco)", NERO, BIANCO),
    ("CURVA A SX: Uscita", GRIGIO, GRIGIO),
    ("Rettilineo: Avvicinamento Verde", GRIGIO, GRIGIO),
    ("MARKER VERDE A SX!", VERDE, GRIGIO),
    ("Rettilineo Finale", GRIGIO, GRIGIO),
    ("STOP", GRIGIO, GRIGIO)
]

def simula_percorso():
    print("=== INIZIO SIMULAZIONE PERCORSO DIGITALE ===\n")
    print(f"{'STEP':<40} | {'SX_IN':<15} {'DX_IN':<15} | {'ERRORE':<8} | {'V_SX':<6} {'V_DX':<6} | {'AZIONI'}")
    print("-" * 130)

    kp = 1.2
    base_speed = 150

    for i, (desc, rgb_sx, rgb_dx) in enumerate(PERCORSO):
        # 1. Input
        errore = calcola_errore(rgb_sx, rgb_dx)
        
        # 2. Elaborazione Motori
        corr = calcola_correzione(errore, kp)
        v_sx, v_dx = calcola_velocita_motori(base_speed, corr)
        
        # 3. Analisi Azione Motoria
        azione_moto = "DRITTO"
        
        # Priority: Verde
        if is_green(rgb_sx):
            azione_moto = "*** SVOLTA 90 GRADI A SX ***"
            # In simulazione, idealmente lo step successivo cambierebbe contesto
        elif is_green(rgb_dx):
            azione_moto = "*** SVOLTA 90 GRADI A DX ***"
        elif v_sx > v_dx + 5: 
            azione_moto = "GIRA DX >>"
        elif v_dx > v_sx + 5: 
            azione_moto = "<< GIRA SX"
        
        output_str = f"{i+1}. {desc:<36} | {str(rgb_sx):<15} {str(rgb_dx):<15} | {errore:<8.1f} | {v_sx:<6.1f} {v_dx:<6.1f} | {azione_moto}"
        
        print(output_str)
        # time.sleep(0.5) # Decommentare per effetto "real time"

    print("\n=== FINE SIMULAZIONE ===")

if __name__ == "__main__":
    simula_percorso()
