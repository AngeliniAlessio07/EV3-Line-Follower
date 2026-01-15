#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port
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

# 2. Definizioni Funzioni (Logica Pura)

def calcola_errore(s_sx, s_dx):
    """
    Calcola la differenza di luce riflessa tra i due sensori.
    Ritorna un valore positivo se il sinistro vede più luce (bianco) e il destro meno (nero).
    """
    # reflection() restituisce un valore da 0 (nero) a 100 (bianco)
    return s_sx.reflection() - s_dx.reflection()

def calcola_correzione(errore, kp):
    """
    Calcola il valore di correzione da applicare alla velocità.
    Correzione = Errore * Kp
    """
    return errore * kp

def calcola_velocita_motori(base_speed, correzione):
    """
    Calcola le velocità finali per i due motori.
    - Se correzione > 0 (Dobbiamo girare a destra): SX accelera, DX rallenta.
    - Se correzione < 0 (Dobbiamo girare a sinistra): SX rallenta, DX accelera.
    """
    v_sx = base_speed + correzione
    v_dx = base_speed - correzione
    return v_sx, v_dx

def applica_moto(m_sx, m_dx, v_sx, v_dx):
    """
    Comanda i motori con le velocità calcolate.
    """
    m_sx.run(v_sx)
    m_dx.run(v_dx)

# 3. Loop Principale
ev3.speaker.beep() # Segnale di avvio

while True:
    try:
        # A. Input
        errore_attuale = calcola_errore(sensore_sx, sensore_dx)
        
        # B. Elaborazione
        correzione_calc = calcola_correzione(errore_attuale, GUADAGNO_KP)
        vel_sx, vel_dx = calcola_velocita_motori(VELOCITA_BASE, correzione_calc)
        
        # C. Output
        applica_moto(motore_sx, motore_dx, vel_sx, vel_dx)
        
        # Piccola pausa per stabilità (opzionale, 10ms)
        wait(10)
        
    except Exception as e:
        # In caso di errore (es. sensore scollegato), ferma tutto
        motore_sx.stop()
        motore_dx.stop()
        print("Errore:", e)
        break
