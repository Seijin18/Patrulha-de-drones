from djitellopy import Tello
import cv2
import numpy as np



class Vision():
    def __init__(self, drone: Tello):
        self.drone = drone
        self.drone.streamon()
    
    def disconnect_cam(self):
        self.drone.streamoff()
        cv2.destroyAllWindows()

    def get_frame_cam(self):
        frame = self.drone.get_frame_read().frame
        
        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # type: ignore
            cv2.line(frame, (480, 0), (480, 720), (256, 256, 256), 1)
            cv2.line(frame, (0, 360), (960, 360), (256, 256, 256), 1)
            cv2.imshow('frame', frame)
            return frame
        else:
            print("Erro ao capturar frame.")
   
    def get_pixel_from_frame(self, frame):
        filteredFrame, center = self.detect_objects(frame)
        cv2.imshow('filteredFrame', filteredFrame)
        
        if any(center):
            print(center)
        
        return 0
   
    def get_distance(self, frame):
        pixel_height = self.get_pixel_from_frame(frame)
        return int(((2.718 ** (pixel_height/149.91)) / 7.18) * 100) 
    
    def distance_to_flag(self):
        frame = self.get_frame_cam()
        # Adicione a lógica para calcular a distância
        distance = self.get_distance(frame)
        return distance + 100
        #return 0