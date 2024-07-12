import cv2
import time

while True:
    cap = cv2.VideoCapture(1)
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cap.release()
    time.sleep(1)