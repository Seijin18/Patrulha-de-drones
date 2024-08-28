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

deadZone = 100
min_consecutive_detections = 3000
consecutive_detections = 0
last_detection = False


def preprocess(img):
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])

    mask = cv2.inRange(imgHsv, lower_red1, upper_red1)

    img_blur = cv2.GaussianBlur(mask, (7, 7), 2)
    img_canny = cv2.Canny(img_blur, 100, 200)
    kernel = np.ones((3, 3))
    img_dilate = cv2.dilate(img_canny, kernel, iterations=2)
    img_erode = cv2.erode(img_dilate, kernel, iterations=1)
    return img_erode


def find_tip(points, convex_hull):
    length = len(points)
    indices = np.setdiff1d(range(length), convex_hull)

    for i in range(2):
        j = (indices[i] + 2) % length
        if np.all(points[j] == points[indices[i - 1] - 2]):
            return tuple(points[j])


def is_valid_arrow(approx, hull, area):
    sides = len(hull)

    bounding_rect = cv2.boundingRect(approx)
    aspect_ratio = float(bounding_rect[2]) / float(bounding_rect[3])

    return (
            6 > sides > 3 and
            sides + 2 == len(approx) and
            0.5 < aspect_ratio < 2.0
    )


def get_arrow_direction(arrow_tip, centroid):
    dx = arrow_tip[0] - centroid[0]
    dy = arrow_tip[1] - centroid[1]

    if abs(dx) > abs(dy):
        if dx > 0:
            return "direita"
        else:
            return "esquerda"
    else:
        if dy > 0:
            return "baixo"
        else:
            return "cima"


def getContours(img):
    global consecutive_detections, last_detection

    imgcontour = preprocess(img)
    contours, _ = cv2.findContours(imgcontour, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    min_area_threshold = 1500

    valid_arrow_detected = False

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > min_area_threshold:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.025 * peri, True)
            hull = cv2.convexHull(approx, returnPoints=False)

            if is_valid_arrow(approx, hull, area):
                arrow_tip = find_tip(approx[:, 0, :], hull.squeeze())

                if arrow_tip:
                    M = cv2.moments(cnt)
                    if M["m10"] != 0 and M["m00"] != 0:
                        centroid = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                        direction = get_arrow_direction(arrow_tip, centroid)

                        cv2.drawContours(img, [cnt], -1, (0, 255, 0), 3)
                        cv2.circle(img, arrow_tip, 3, (0, 0, 255), cv2.FILLED)

                        cv2.circle(img, centroid, 5, (255, 0, 0), cv2.FILLED)

                        cv2.putText(img, f"Direcao: {direction}", (centroid[0] + 20, centroid[1]),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                        valid_arrow_detected = True

    if valid_arrow_detected:
        if last_detection:
            consecutive_detections += 1
        else:
            consecutive_detections = 1
        last_detection = True
    else:
        last_detection = False
        consecutive_detections = 0

    if consecutive_detections >= min_consecutive_detections:
        return True
    else:
        return False


def main():
    while True:
        #_, myFrame = cap.read()
        # myFrame = frame_read.frame
        # framee = cv2.cvtColor(myFrame, cv2.COLOR_BGR2RGB)
        ret, myFrame = cap.read()
        if not ret:
            break

        img = cv2.resize(myFrame, (frameWidth, frameHeight))
        imgContour = img.copy()
        arrow_detected = getContours(imgContour)

        if arrow_detected:
            cv2.putText(imgContour, "Seta Detectada", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

        cv2.imshow("Image", imgContour)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()