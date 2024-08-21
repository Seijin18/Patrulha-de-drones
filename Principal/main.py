from typing import Final
from djitellopy import Tello
import cv2
from controle import control
from detection import detect_objects
from hud import stackImages
from arrows_detection import arrows_detection

TAKE_OFF: Final = False
VIEW_FRAME: Final = False

#drone = Tello()

def main():
    #drone.connect()
    
    if (TAKE_OFF):
        pass
        #drone.takeoff()
    
    if (VIEW_FRAME): 
        pass
        #drone.streamon()
        
    webcam = cv2.VideoCapture(0)
    
    #battery = drone.get_battery()
    #print(f"battery is {battery}")
    
    while True: #and battery > 7:
        #frame = drone.get_frame_read().frame
        _, frame = webcam.read()
        
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # type: ignore
        
        filteredFrame, centers = detect_objects(frame)
        
        if centers != (None, None):
            #filteredFrame = control(filteredFrame, centers, drone)
            
            arrow_img = arrows_detection(filteredFrame)
            #stackImages(0.9, ([filteredFrame, frame], [arrow_img, frame]))
            cv2.imshow("filteredFrame", filteredFrame)
        
        cv2.imshow("frame", frame)
        
        
        #hud de imagens e deteccao
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    if (TAKE_OFF):
        pass
        #drone.land()
        
    if (VIEW_FRAME):
        pass
        #drone.streamoff()
            
    cv2.destroyAllWindows()
    #drone.end()
    
    
if __name__ == "__main__":
    main()