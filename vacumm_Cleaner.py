import WebGUI
import HAL
import Frequency
import math
import time

turn_start_time = None
forward_start_time = None
spiral_start_time = None

def spiral_concentrica(tiempo_actual):
    
    radio_inicial = 0.3      # Radio inicial pequeño
    factor_crecimiento = 0.03  
    
    radio = radio_inicial + factor_crecimiento * tiempo_actual
    
    # Velocidad lineal constante
    v_lineal = 0.2
    
    # Velocidad angular = v_lineal / radio (para mantener círculo)
    if radio > 0.1:
        v_angular = v_lineal / radio
    else:
        v_angular = 2.0
    
    # Limitar velocidades
    v_angular = min(v_angular, 1.5)
    
    HAL.setV(v_lineal)
    HAL.setW(v_angular)
    
    return radio

def turn():
    #Giro de 90 grados
    HAL.setV(0)
    HAL.setW(0.6)

def main():
    global turn_start_time, forward_start_time, spiral_start_time
    
    state = "SPIRAL"
    spiral_start_time = time.time()
    
    while True:
        
        if state == "SPIRAL":
            current_time = time.time()
            tiempo_en_espiral = current_time - spiral_start_time
            
            # Ejecutar espiral
            radio_actual = spiral_concentrica(tiempo_en_espiral)
            
            if HAL.getBumperData().state == 1:
                state = "TURN"
                turn_start_time = time.time()
        
        elif state == "TURN":
            current_time = time.time()
            tiempo_giro = current_time - turn_start_time
            tiempo_giro_necesario = (math.pi/2) / 0.6  # ≈ 2.62s para 90 grados
            
            if tiempo_giro < tiempo_giro_necesario:
                turn()
            else:
                state = "FORWARD"
                forward_start_time = time.time()
        
        elif state == "FORWARD":
            current_time = time.time()
            tiempo_avance = current_time - forward_start_time
            tiempo_necesario = 1  
            
            if HAL.getBumperData().state == 1:
                state = "TURN"
                turn_start_time = time.time()
            
            elif tiempo_avance < tiempo_necesario:
                HAL.setV(0.5)
                HAL.setW(0)
            
            else:
                state = "SPIRAL"
                spiral_start_time = time.time()  # Reset timer

        Frequency.tick()

main()