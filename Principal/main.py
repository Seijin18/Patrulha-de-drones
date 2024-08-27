from djitellopy import Tello
import cv2
from controle import control
from detection import detect_objects
from hud import stackImages
from arrows_detection import arrows_detection
from teste_arrows_detection import get_arrow_info, get_filter_arrow_image, preprocess, get_arrow_direction
from frame import chose_frame_generation, get_frame, close_frame_generation


def main():
    COUNT_DIRECTION_MAX:int = 10
    count_direction: int = 0
    average_direction: int = [0, 0, 0, 0]
    #is_moving = False
    
    frame_generation = int(input("drone[1] webcam[0]: "))
    
    uav = chose_frame_generation(frame_generation)
    
    while True: 
        frame = get_frame(frame_generation, uav)
        
        filteredFrame, centers = detect_objects(frame)
        
        if centers != (None, None):
            thresh_image = preprocess(filteredFrame)
            
            control(filteredFrame, centers, uav)
            '''
            arrow_image = get_filter_arrow_image(thresh_image)
            if arrow_image is not None:
                cv2.imshow("arrow_image", arrow_image)
                #cv2.imwrite("arrow_image.png", arrow_image)
        
                arrow_info_image, angle = get_arrow_info(arrow_image)
                cv2.imshow("arrow_info_image", arrow_info_image)
                #cv2.imwrite("arrow_info_image.png", arrow_info_image)
                print(f"a seta esta apontada para {get_arrow_direction(angle)}")
            '''
            
            arrow_img, direction = arrows_detection(filteredFrame)
            
            if count_direction < COUNT_DIRECTION_MAX:
                average_direction[direction] += 1
                count_direction += 1
            else:
                indice = average_direction.index(max(average_direction))
                if indice == 0:
                    #uav.move_forward(20)
                    print("seguir para frente")
                elif indice == 1:
                    #uav.rotate_clockwise(40)
                    print("virar para a direita")
                elif indice == 2:
                    #uav.rotate_counter_clockwise(90)
                    print("virar para esquerda")
                else:
                    #uav.move_back(20)
                    print("mover para trás")
                
                count_direction = 0
                average_direction = [0, 0, 0, 0]
                    
        
        cv2.imshow("frame", frame)
        cv2.imshow("filteredFrame", filteredFrame)
        
        #hud de imagens e deteccao
        #stackImages(0.9, ([filteredFrame, frame], [arrow_img, frame]))
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    close_frame_generation(frame_generation, uav)
    
    
if __name__ == "__main__":
    main()