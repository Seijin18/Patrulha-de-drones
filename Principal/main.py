from djitellopy import Tello
import cv2
from controle import control
from detection import detect_objects

drone = Tello()

def main():
    drone.connect()
    drone.streamon()
    
    drone.takeoff()
    
    battery = drone.get_battery()
    print(f"battery is {battery}")
    
    while True and battery > 7:
        frame = drone.get_frame_read().frame
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # type: ignore
        cv2.imshow('frame', frame)
        
        filteredFrame, centers = detect_objects(frame)
        
        if centers != (None, None):
            filteredFrame = control(filteredFrame, centers, drone)
        cv2.imshow('filteredFrame', filteredFrame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    drone.land()
    drone.streamoff()
    cv2.destroyAllWindows()
    drone.end()
    
    
if __name__ == "__main__":
    main()