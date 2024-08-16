from djitellopy import Tello
import cv2
import numpy as np
frameWidth = 1280
frameHeight = 720
deadZone=125

class Vision():
    def __init__(self, drone: Tello):
        self.drone = drone
        self.drone.streamoff()
        self.drone.streamon()

    def disconnect_cam(self):
        self.drone.streamoff()
        cv2.destroyAllWindows()

    def stackImages(self, scale, imgArray):
        rows = len(imgArray)
        cols = len(imgArray[0])
        rowsAvailable = isinstance(imgArray[0], list)
        width = imgArray[0][0].shape[1]
        height = imgArray[0][0].shape[0]
        if rowsAvailable:
            for x in range(0, rows):
                for y in range(0, cols):
                    if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                        imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                    else:
                        imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),None, scale, scale)
                    if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
            imageBlank = np.zeros((height, width, 3), np.uint8)
            hor = [imageBlank] * rows
            hor_con = [imageBlank] * rows
            for x in range(0, rows):
                hor[x] = np.hstack(imgArray[x])
            ver = np.vstack(hor)
        else:
            for x in range(0, rows):
                if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                    imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
                else:
                    imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale,scale)
                if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
            hor = np.hstack(imgArray)
            ver = hor
        return ver

    def getContours(self, img, imgcontour):

        contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            areaMin = cv2.getTrackbarPos("Area", "Parameters") / 5
            if area > areaMin:
                cv2.drawContours(imgcontour, cnt, -1, (255, 0, 255), 7)
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                print(len(approx))
                x, y, w, h = cv2.boundingRect(approx)
                cv2.rectangle(imgcontour, (x, y), (x + w, y + h), (0, 255, 0), 5)

                cv2.putText(imgcontour, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX,.7,(0, 255, 0), 2)
                cv2.putText(imgcontour, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,(0, 255, 0), 2)
                cv2.putText(imgcontour, " " + str(int(x)) + " " + str(int(y)), (x - 20, y - 45),cv2.FONT_HERSHEY_COMPLEX, 0.7,(0, 255, 0), 2)

                cx = int(x + (w / 2))
                cy = int(y + (h / 2))

                if (cx < int(frameWidth / 2) - deadZone):
                    cv2.putText(imgcontour, " GO LEFT ", (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)
                    cv2.rectangle(imgcontour, (0, int(frameHeight / 2 - deadZone)),(int(frameWidth / 2) - deadZone, int(frameHeight / 2) + deadZone), (0, 0, 255),cv2.FILLED)
                elif (cx > int(frameWidth / 2) + deadZone):
                    cv2.putText(imgcontour, " GO RIGHT ", (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)
                    cv2.rectangle(imgcontour, (int(frameWidth / 2 + deadZone), int(frameHeight / 2 - deadZone)),(frameWidth, int(frameHeight / 2) + deadZone), (0, 0, 255), cv2.FILLED)
                elif (cy < int(frameHeight / 2) - deadZone):
                    cv2.putText(imgContour, " GO UP ", (20, 50), cv2.FONT_HERSHEY_COMPLEX,1,(0, 0, 255), 3)
                    cv2.rectangle(imgContour,(int(frameWidth/2-deadZone),0),(int(frameWidth/2+deadZone),int(frameHeight/2)-deadZone),(0,0,255),cv2.FILLED)
                elif (cy > int(frameHeight / 2) + deadZone):
                    cv2.putText(imgContour, " GO DOWN ", (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1,(0, 0, 255), 3)
                    cv2.rectangle(imgContour,(int(frameWidth/2-deadZone),int(frameHeight/2)+deadZone),(int(frameWidth/2+deadZone),frameHeight),(0,0,255),cv2.FILLED)
                elif area < 10000:
                    cv2.putText(imgcontour, " MOVE FORWARD ", (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)
                elif area > 10000:
                    cv2.putText(imgcontour, " MOVE BACKWARD ", (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)

                cv2.line(imgcontour, (int(frameWidth / 2), int(frameHeight / 2)), (cx, cy),(0, 0, 255), 3)

    def display(self,img):
        cv2.line(img, (int(frameWidth / 2) - deadZone, 0), (int(frameWidth / 2) - deadZone, frameHeight), (255, 255, 0),3)
        cv2.line(img, (int(frameWidth / 2) + deadZone, 0), (int(frameWidth / 2) + deadZone, frameHeight), (255, 255, 0),3)
        cv2.circle(img, (int(frameWidth / 2), int(frameHeight / 2)), 5, (0, 0, 255), 5)
        cv2.line(img, (0, int(frameHeight / 2) - deadZone), (frameWidth, int(frameHeight / 2) - deadZone),(255, 255, 0), 3)
        cv2.line(img, (0, int(frameHeight / 2) + deadZone), (frameWidth, int(frameHeight / 2) + deadZone),(255, 255, 0), 3)

    def followFlag(self):
        def empty(a):
            pass
        cv2.namedWindow("HSV")
        cv2.resizeWindow("HSV", 640, 240)
        cv2.createTrackbar("HUE Min", "HSV", 19, 179, empty)
        cv2.createTrackbar("HUE Max", "HSV", 35, 179, empty)
        cv2.createTrackbar("SAT Min", "HSV", 107, 255, empty)
        cv2.createTrackbar("SAT Max", "HSV", 255, 255, empty)
        cv2.createTrackbar("VALUE Min", "HSV", 89, 255, empty)
        cv2.createTrackbar("VALUE Max", "HSV", 255, 255, empty)

        cv2.namedWindow("Parameters")
        cv2.resizeWindow("Parameters", 640, 240)
        cv2.createTrackbar("Threshold1", "Parameters", 166, 255, empty)
        cv2.createTrackbar("Threshold2", "Parameters", 171, 255, empty)
        cv2.createTrackbar("Area", "Parameters", 3750, 30000, empty)

        while True:
            frame_read = self.drone.get_frame_read()
            myframe = frame_read.frame
            frame_1 = cv2.cvtColor(myframe, cv2.COLOR_BGR2RGB)
            img = cv2.resize(frame_1, (frameWidth, frameHeight))
            img_contour = img.copy()
            img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            h_min = cv2.getTrackbarPos("HUE Min", "HSV")
            h_max = cv2.getTrackbarPos("HUE Max", "HSV")
            s_min = cv2.getTrackbarPos("SAT Min", "HSV")
            s_max = cv2.getTrackbarPos("SAT Max", "HSV")
            v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
            v_max = cv2.getTrackbarPos("VALUE Max", "HSV")

            lower = np.array([h_min, s_min, v_min])
            upper = np.array([h_max, s_max, v_max])
            mask = cv2.inRange(img_hsv, lower, upper)
            result = cv2.bitwise_and(img, img, mask=mask)
            mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

            imgBlur = cv2.GaussianBlur(result, (7, 7), 1)
            imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
            threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
            threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")
            imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
            kernel = np.ones((5, 5))
            imgDil = cv2.dilate(imgCanny, kernel, iterations=1)
            self.getContours(imgDil, img_contour)
            self.display(img_contour)
            stack = self.stackImages(0.7, ([img, result], [imgDil, img_contour]))
            cv2.imshow('Horizontal Stacking', stack)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.disconnect_cam()