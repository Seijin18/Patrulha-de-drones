import cv2
import numpy as np
import os

def processArrow(image):
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (5, 5), 1)
    img_canny = cv2.Canny(img_blur, 50, 50)

    return img_canny

def find_tip(points, convex_hull):
    length = len(points)
    indices = np.setdiff1d(range(length), convex_hull)

    for i in range(2):
        j = indices[i] + 2
        if j > length - 1:
            j = length - j
        if np.all(points[j] == points[indices[i - 1] - 2]):
            return tuple(points[j])
        
def getContours(image):
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        peri = cv2.arcLength(contours[0], True)
        approx = cv2.approxPolyDP(contours[0], 0.02 * peri, True)
        hull = cv2.convexHull(approx, returnPoints=False)
        sides = len(hull)

        if sides < 3 and sides + 2 == len(approx):
            arrow_tip = find_tip(approx[:,0,:], hull)
            if arrow_tip:
                cv2.circle(image, arrow_tip, 3, (255, 255, 255), -1)
                cv2.putText(image, f"{arrow_tip}", arrow_tip, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                cv2.drawContours(image, [approx], -1, (0, 255, 0), 2)
    return image


if __name__ == "__main__":
    dir = os.getcwd()
    print(dir)
    os.chdir("Detector de formas")
    os.chdir("arrow detection")
    dir = os.getcwd()
    print(dir)
    image = cv2.imread("arrow2.jpg")
    cv2.imshow("Original Image", image)
    processedImage = processArrow(image)
    contoursImage = getContours(processedImage)
    cv2.imshow("Processed Image", processedImage)
    cv2.imshow("Contours Image", contoursImage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()