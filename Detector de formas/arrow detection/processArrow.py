import cv2
import numpy as np
import os

def processArrow(image):
    img_blur = cv2.GaussianBlur(image, (5, 5), 1)  # Apply Gaussian blur to the grayscale image
    hsv = cv2.cvtColor(img_blur, cv2.COLOR_BGR2HSV)  # Convert the original image to HSV
    cv2.imshow('hsv', img_blur)

    lower_red = np.array([160, 30, 30])
    upper_red = np.array([180, 255, 255])

    mask = cv2.inRange(hsv, lower_red, upper_red)  # Create a mask for the red color in the HSV image

    cv2.imshow('mask', mask)

    img_canny = cv2.Canny(mask, 100, 200)  # Apply Canny edge detection to the mask
    return img_canny

def skeletonize(image):
    
    size = np.size(image)
    skel = np.zeros(image.shape, np.uint8)
    ret, img = cv2.threshold(image, 127, 255, 0)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    done = False

    while not done:
        eroded = cv2.erode(img, element)
        temp = cv2.dilate(eroded, element)
        temp = cv2.subtract(img, temp)
        skel = cv2.bitwise_or(skel, temp)
        img = eroded.copy()

        zeros = size - cv2.countNonZero(img)
        if zeros == size:
            done = True

    return skel

def get_direction(corners, contour):
    # Get the center of the contour
    M = cv2.moments(contour)
    x_center = int(M["m10"] / M["m00"])
    y_center = int(M["m01"] / M["m00"])

    # Get the vector from the center to the maximum corner
    if np.mean(corners[:, 0, 0]) < x_center:
        direction = 'RIGHT'
    else:
        direction = 'LEFT'

    if np.mean(corners[:, 0, 1]) < y_center:
        direction = 'DOWN'
    else:
        direction = 'UP'

    return direction
    

def get_vertices(contour):
    # GoodfeaturestoTrack
    corners = cv2.goodFeaturesToTrack(contour, 7, 0.9, 50)

    for i in corners:
        x, y = i.ravel()
        x, y = int(x), int(y)  # Ensure x and y are integers
        cv2.circle(image, (x, y), 3, (0, 0, 0), -1)
        cv2.putText(image, f"{x}, {y}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)

    cv2.imshow('image', image)
    return corners


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
    get_vertices = get_vertices(processedImage)
    direction = get_direction(get_vertices, processedImage)
    print(f"Direction: {direction}")

    skeleton = skeletonize(image)
    cv2.imshow('skeleton', skeleton)
    cv2.imshow("Processed Image", processedImage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()