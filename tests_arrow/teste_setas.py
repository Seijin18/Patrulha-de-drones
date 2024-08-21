import cv2
import numpy as np
# from djitellopy import Tello

# me = Tello()
# me.connect()
# print(me.get_battery())

frameWidth = 1280
frameHeight = 720
# me.streamoff()
# me.streamon()
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

deadZone=100
global imgContour


def preprocess(img):
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 120, 70])  # Intervalo inferior de vermelho
    upper_red = np.array([10, 255, 255])  # Intervalo superior de vermelho
    mask = cv2.inRange(imgHsv, lower_red, upper_red)

    img_gray = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    img_blur = cv2.GaussianBlur(img_gray, (5, 5), 1)
    img_canny = cv2.Canny(img_blur, 50, 50)
    kernel = np.ones((3, 3))
    img_dilate = cv2.dilate(img_canny, kernel, iterations=2)
    img_erode = cv2.erode(img_dilate, kernel, iterations=1)
    return img_erode

def find_tip(points, convex_hull):
    length = len(points)
    indices = np.setdiff1d(range(length), convex_hull)

    for i in range(2):
        j = indices[i] + 2
        if j > length - 1:
            j = length - j
        if np.all(points[j] == points[indices[i - 1] - 2]):
            return tuple(points[j])

def getContours(img):
    imgcontour = preprocess(img)
    contours, hierarchy = cv2.findContours(imgcontour, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    min_area_threshold = 1000

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > min_area_threshold:  # Defina um valor para min_area_threshold
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.025 * peri, True)
            hull = cv2.convexHull(approx, returnPoints=False)
            sides = len(hull)

            if 6 > sides > 3 and sides + 2 == len(approx):
                arrow_tip = find_tip(approx[:, 0, :], hull.squeeze())
                if arrow_tip:
                    cv2.drawContours(img, [cnt], -1, (0, 255, 0), 3)
                    cv2.circle(img, arrow_tip, 3, (0, 0, 255), cv2.FILLED)


while True:
    _, myFrame = cap.read()
    # myFrame = frame_read.frame
    # framee = cv2.cvtColor(myFrame, cv2.COLOR_BGR2RGB)
    img = cv2.resize(myFrame, (frameWidth, frameHeight))
    imgContour = img.copy()
    getContours(img)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
# cv2.destroyAllWindows()







