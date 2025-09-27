import WebGUI
import HAL
import Frequency
import math
import random
import time

turn_start_time = None
forward_start_time = None
distance_start_time = None

def spiral(v):
    HAL.setV(v)
    HAL.setW(1)

def turn():
    HAL.setV(0)
    HAL.setW(0.6)

def main():
    global turn_start_time, forward_start_time, distance_start_time
    
    v = 0.05
    state = "SPIRAL"
    
    while True:
        
        if state == "SPIRAL":
            if HAL.getBumperData().state == 1:
                # ✅ Choque detectado: iniciar giro 90°
                state = "TURN"
                turn_start_time = time.time()
                print("Choque detectado → Girando 90°")
            else:
                spiral(v)
                v = v + 0.01
                
                if v > 2:
                    # ✅ Espiral completa: avanzar recto 1m
                    state = "FORWARD" 
                    forward_start_time = time.time()
                    v = 0.05  # Resetear velocidad para próxima espiral
                    print("Espiral completa → Avanzando 1m")

        elif state == "TURN":
            current_time = time.time()
            tiempo_giro = current_time - turn_start_time
            tiempo_giro_necesario = (math.pi/2) / 0.6  # ≈ 2.62s para 90°
            
            if tiempo_giro < tiempo_giro_necesario:
                turn()
                print(f"Girando... {tiempo_giro:.1f}s de {tiempo_giro_necesario:.1f}s")
            else:
                # ✅ Giro completado: avanzar 1m recto
                state = "FORWARD"
                forward_start_time = time.time()
                print("Giro 90° completado → Avanzando 1m")

        elif state == "FORWARD":
            current_time = time.time()
            tiempo_avance = current_time - forward_start_time
            
            # ✅ Verificar choque durante el avance
            if HAL.getBumperData().state == 1:
                state = "TURN"
                turn_start_time = time.time()
                print("Choque durante avance → Girando 90°")
            
            # ✅ Avanzar recto durante ~3.3s para 1m (a 0.3 m/s)
            elif tiempo_avance < 3.3:  # 1m / 0.3 m/s ≈ 3.3s
                HAL.setV(0.3)
                HAL.setW(0)
                print(f"Avanzando... {tiempo_avance:.1f}s")
            
            else:
                # ✅ 1m completado sin choques: volver a espiral
                state = "SPIRAL"
                v = 0.05  # Resetear velocidad de espiral
                print("1m avanzado → Volviendo a espiral")

        Frequency.tick()

main()