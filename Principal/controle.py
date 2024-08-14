import cv2
from djitellopy import Tello

# Funções de ação
def turn_left(drone: Tello, angle):
    drone.rotate_counter_clockwise(angle)

def turn_right(drone: Tello, angle):
    drone.rotate_clockwise(angle)

# Função de controle
def control(frame, object, drone: Tello):
    # Verificar se há um objeto detectado
    if len(object) == 0:
        return

    # Definir região central da imagem
    height, width, _ = frame.shape
    centro_x = width // 2
    centro_y = height // 2
    # Define a margem da região central
    margem = 50
    # Imprimir linhas de referência
    cv2.line(frame, (centro_x - margem, 0), (centro_x - margem, height), (255, 0, 0), 1)
    cv2.line(frame, (centro_x + margem, 0), (centro_x + margem, height), (255, 0, 0), 1)
    
    # Verificar se o objeto está na região central
    if object[0] < centro_x - margem:
        turn_left(drone, 10)
    elif object[0] > centro_x + margem:
        turn_right(drone, 10)
    else:
        turn_right(drone, 10)
        
    return frame