#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Color
from pybricks.tools import wait

# 1. Configurazione / Setup
ev3 = EV3Brick()

# Configurazione Motori
# Assumiamo Motore Sinistro su Porta B, Destro su Porta C
motore_sx = Motor(Port.B)
motore_dx = Motor(Port.C)

# Configurazione Sensori
# Assumiamo Sensore Sinistro su Porta S1, Destro su Porta S4
sensore_sx = ColorSensor(Port.S1)
sensore_dx = ColorSensor(Port.S4)


# Costanti di Controllo
VELOCITA_BASE = 150       # Velocità di crociera (gradi al secondo)
GUADAGNO_KP = 1.2         # Costante Proporzionale (quanto forte sterzare)
VELOCITA_SVOLTA = 100     # Velocità durante la svolta a 90 gradi
GRADI_ROTAZIONE_90 = 230  # Gradi di rotazione motore per fare 90 gradi col robot (DA CALIBRARE)

# 2. Definizioni Funzioni (Logica Pura)

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
    # Soglie di sicurezza
    if g < 10: return False # Troppo scuro
    
    # Il verde deve essere significativamente più alto di rosso e blu
    if g > r * 1.5 and g > b * 1.5:
        return True
    return False

def calcola_errore(s_sx, s_dx):
    """
    Calcola la differenza di luminosità tra i due sensori usando RGB.
    Se un sensore vede verde, lo ignoriamo per il calcolo della guida (usiamo il valore dell'altro o neutro)
    per evitare che il robot sterzi bruscamente sul marker.
    """
    rgb_sx = s_sx.rgb()
    rgb_dx = s_dx.rgb()
    
    # Rilevamento Verde "Early" per decidere la strategia
    green_sx = is_green(rgb_sx)
    green_dx = is_green(rgb_dx)
    
    lum_sx = estrai_luminosita(rgb_sx)
    lum_dx = estrai_luminosita(rgb_dx)
    
    # Strategia Antigravità: Se vedo verde, "fingo" di essere perfettamente allineato su quel lato
    # per evitare scossoni mentre decido di svoltare nel loop principale.
    if green_sx or green_dx:
        return 0, rgb_sx, rgb_dx
        
    return lum_sx - lum_dx, rgb_sx, rgb_dx

def calcola_correzione(errore, kp):
    return errore * kp

def calcola_velocita_motori(base_speed, correzione):
    v_sx = base_speed + correzione
    v_dx = base_speed - correzione
    return v_sx, v_dx

def applica_moto(m_sx, m_dx, v_sx, v_dx):
    m_sx.run(v_sx)
    m_dx.run(v_dx)

def esegui_svolta_90(direzione, m_sx, m_dx):
    """
    Esegue una svolta di 90 gradi sul posto (Tank Turn).
    direzione: 'SX' o 'DX'
    """
    print(f"Eseguo svolta a {direzione}...")
    m_sx.stop()
    m_dx.stop()
    ev3.speaker.beep()
    
    # Calcolo angoli relativi
    # Per girare a DX: SX avanti, DX indietro
    # Per girare a SX: DX avanti, SX indietro
    if direzione == 'DX':
        m_sx.run_angle(VELOCITA_SVOLTA, GRADI_ROTAZIONE_90, wait=False)
        m_dx.run_angle(VELOCITA_SVOLTA, -GRADI_ROTAZIONE_90, wait=True)
    elif direzione == 'SX':
        m_sx.run_angle(VELOCITA_SVOLTA, -GRADI_ROTAZIONE_90, wait=False)
        m_dx.run_angle(VELOCITA_SVOLTA, GRADI_ROTAZIONE_90, wait=True)
        
    # Ripresa
    wait(100) # Breve pausa di assestamento

# 3. Loop Principale
ev3.speaker.beep() # Segnale di avvio

while True:
    try:
        # A. Input e Elaborazione Errore
        errore_attuale, rgb_now_sx, rgb_now_dx = calcola_errore(sensore_sx, sensore_dx)
        
        # B. Rilevamento Verde e Svolte
        # La priorità è al verde. Se rilevato, svoltiamo e saltiamo il resto del ciclo motore per questo tick.
        if is_green(rgb_now_sx):
            print("Verde a SINISTRA -> Svolta 90° SX")
            esegui_svolta_90('SX', motore_sx, motore_dx)
            # Dopo la svolta, puliamo lo stato o continuiamo, il prossimo loop rileggerà i sensori
            continue
            
        elif is_green(rgb_now_dx):
            print("Verde a DESTRA -> Svolta 90° DX")
            esegui_svolta_90('DX', motore_sx, motore_dx)
            continue
        
        # C. Guida Normale (Line Follower)
        # Se non stiamo svoltando, procediamo col PID
        correzione_calc = calcola_correzione(errore_attuale, GUADAGNO_KP)
        vel_sx, vel_dx = calcola_velocita_motori(VELOCITA_BASE, correzione_calc)
        applica_moto(motore_sx, motore_dx, vel_sx, vel_dx)
        
        wait(10)
        
    except Exception as e:
        motore_sx.stop()
        motore_dx.stop()
        print("Errore:", e)
        break


