import cv2

def save_frame(frame, path):
    cv2.imwrite(path, frame)
    print(f"Frame saved at {path}")