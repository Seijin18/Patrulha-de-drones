from djitellopy import Tello

# Função de controle
def is_centralize(frame_generation, height, width, object, drone: Tello):
    if frame_generation:
        # Verificar se há um objeto detectado
        if len(object) == 0:
            return
    
        centro_x = width // 2
        #centro_y = height // 2
        
        # Define a margem da região central
        margem = 50
        
        # Verificar se o objeto está na região central
        if object[0]//2 < centro_x - margem:
            print("mais para esquerda")
            drone.rotate_counter_clockwise(10)
            return False
        elif object[0]//2 > centro_x + margem:
            print("mais para direita")
            drone.rotate_clockwise(10)
            return False
        
    return True

def set_direction(frame_generation, direction, object_frame):
    if direction == "cima":
        object_frame.move_forward(30) if frame_generation else print("seguir para frente")
    elif direction == "direita":
        object_frame.rotate_clockwise(90) if frame_generation else  print("virar para a direita")
    elif direction == "esquerda":
        object_frame.rotate_counter_clockwise(90) if frame_generation else print("virar para esquerda")
    elif direction == "baixo":
        object_frame.move_back(20) if frame_generation else print("mover para trás")
