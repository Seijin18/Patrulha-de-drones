from calendar import c
import os
import re

import cv2
from numpy import append

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
    read_frames = []
    corrected_lines = []
    while not end_flag:
        frames = [f for f in os.listdir(dir) if f.endswith('.png')]
        try:
            with open(dir + "alert_log.txt", "r") as f:
                lines = f.readlines()
                for line in lines:
                    line = line.split("\n")[0]
                    corrected_lines.append(line)
                    
                for frame in frames:
                    if frame not in corrected_lines:
                        read_frames.append(frame)
                        if detect_danger(frame):
                            send_alert(frame)
                
            with open(dir + "alert_log.txt", "a") as f:
                for frame in read_frames:
                    f.write(frame + "\n")
                read_frames = []
                    
        except:
            open(dir + "read_frames.txt", "w").close()
            
danger(False)
