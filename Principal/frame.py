from djitellopy import Tello
from time import sleep
import cv2

def chose_frame_generation(frame_generation: int):
    
    if frame_generation:
        drone = Tello()
        drone.connect()
        drone.get_battery()

        print(f"Bateria: {drone.get_battery()}")

        if int(input("deseja que o drone levante vou? sim[1] não[0]: ")):
            drone.takeoff()

        sleep(2)
        drone.streamon()
        
        return drone
    else:
        webcam = cv2.VideoCapture(0)
        return webcam
    
def get_frame(frame_generation: int, object_frame):
    if frame_generation:
        frame = object_frame.get_frame_read().frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    else:
        _, frame = object_frame.read()
        
    return frame

def close_frame_generation(frame_generation: int, object_frame):
    if frame_generation:
        object_frame.streamoff()
        if object_frame.is_flying:
            object_frame.land()
    else:
        object_frame.release()
        
    cv2.destroyAllWindows()