import os

import cv2

def detect_danger(file):
    return True

def send_alert(frame_name):
    print(f"Alert sent for frame {frame_name}")
    pass

def danger(end_flag):
    dir = os.getcwd()
    if not "images" in os.listdir(dir):
        os.mkdir("images")
    dir = os.path.join(dir, "images\\")
    while not end_flag:
        frames = [f for f in os.listdir(dir) if f.endswith('.png')]
        try:
            with open(dir + "read_frames.txt", "r") as f:
                for frame in frames:
                    if frame in f.read():
                        print(f.read())
                        pass
                    else:
                        detect_flag = detect_danger(frame)
                        with open(dir + "read_frames.txt", "a") as f:
                            f.write(frame + "\n")
                        if detect_flag:
                            frame_name = frame.split(".")[0]
                            send_alert(frame_name)
                            with open(dir + "alert_log.txt", "a") as log:
                                log.write(frame_name + "\n")
                        # Remove frames if more than 10 frames have been read
                        if len(f.readlines()) > 10:
                            files = f.readlines()
                        for file in files:
                            os.remove(os.path.join(dir, file))
                        f.seek(0)
                        f.truncate()
        except:
            open(dir + "read_frames.txt", "w").close()
            
            
danger(False)
