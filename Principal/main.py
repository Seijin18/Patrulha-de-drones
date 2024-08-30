from djitellopy import Tello
import cv2
from control import is_centralize, set_direction
from detection import detect_objects
from hud import stackImages
from arrows_detection import get_direction, is_arrow_direction_deslocate
from frame import chose_frame_generation, get_frame, close_frame_generation

#from teste_arrows_detection import get_arrow_info, get_filter_arrow_image, preprocess, get_arrow_direction
#from teste_arrows_detection import getContours, get_direction

min_no_arrow = 30

def main():
    is_tracking = False
    consecutive_detections = 0
    last_detection = False
    tracking_direction: str = ""
    tracking_consecutive_detection = 0
    tracking_last_detection = False
    no_arrow_counter = 0
    
    frame_generation = int(input("drone[1] webcam[0]: "))
    
    uav = chose_frame_generation(frame_generation)
    
    frame = get_frame(frame_generation, uav)
    
    # Definir região central da imagem
    height, width, _ = frame.shape
    
    while True: 
        frame = get_frame(frame_generation, uav)
        
        filteredFrame, large_contours = detect_objects(frame)
        
        if large_contours:
            filteredFrame, direction, consecutive_detections, last_detection, centroid = get_direction(filteredFrame, large_contours, consecutive_detections, last_detection)
            
            if centroid != (None, None) and is_centralize(frame_generation, height, width, centroid, uav):
                no_arrow_counter = 0
                if is_tracking:
                    is_arrow_deslocate, tracking_consecutive_detection, tracking_last_detection = is_arrow_direction_deslocate(direction, tracking_direction, tracking_consecutive_detection, tracking_last_detection)
                    if is_arrow_deslocate:
                        set_direction(frame_generation, tracking_direction, uav)
                        is_tracking = False
                        tracking_consecutive_detection = 0
                        tracking_last_detection = False
                else:
                    if direction in ["direita", "esquerda"]:
                        is_tracking = True
                        tracking_direction = direction
                    else:
                        set_direction(frame_generation, direction, uav)
        else:
            if is_tracking:
                is_arrow_deslocate, tracking_consecutive_detection, tracking_last_detection = is_arrow_direction_deslocate("nd", tracking_direction, tracking_consecutive_detection, tracking_last_detection)
                if is_arrow_deslocate:
                    set_direction(frame_generation, tracking_direction, uav)
                    is_tracking = False
            elif no_arrow_counter >= min_no_arrow:
                uav.rotate_clockwise(10) if frame_generation else print("Não existe seta")
                no_arrow_counter = 0
            else:
                no_arrow_counter += 1
        
        #hud de imagens e deteccao
        stackImages(1, ([filteredFrame, frame]))
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    close_frame_generation(frame_generation, uav)
    
    
if __name__ == "__main__":
    main()