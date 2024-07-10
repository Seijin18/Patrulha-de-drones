from djitellopy import Tello
import cv2

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
            cv2.imshow('frame', frame)
        else:
            print("Erro ao capturar frame.")
    
    def distance_to_flag(self):
        self.get_frame_cam()
        # Adicione a lógica para calcular a distância
        return 0
