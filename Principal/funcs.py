from djitellopy import Tello
import cv2
import numpy as np

def detect_triangles(frame):
    # Correct saturation
    frame = cv2.convertScaleAbs(frame, alpha=1.5, beta=0)

    # Apply Gaussian blur to reduce noise
    frame = cv2.GaussianBlur(frame, (5, 5), 0)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define range for the color red
    lower_red = np.array([160, 60, 60])
    upper_red = np.array([179, 255, 255])

    # Create a filter for the color red
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Apply the filter to the image
    filteredFrame = cv2.bitwise_and(frame, frame, mask=mask)

    # Find contours of red objects
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area
    min_contour_area = 1000  # Minimum contour area to consider
    large_contours = [contour for contour in contours if cv2.contourArea(contour) > min_contour_area]

    for contour in large_contours:
        # Approximate the contour to a polygon
        epsilon = 0.022 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # If the polygon has 3 vertices, it is a triangle
        if len(approx) == 3:
            # Draw the contour
            cv2.drawContours(filteredFrame, [approx], -1, (0, 255, 0), 2)

            # Compute the center of the contour
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.circle(filteredFrame, (cX, cY), 3, (255, 255, 255), -1)

    return filteredFrame

def getWebCamImage(webcam_index):
    validacao, frame = webcam.read()
    if validacao:
        return frame
    else:
        print("Webcam not found")
        return None

# Select video source
source = input("Select video source webcam (1) or drone (2): ")

# Select the webcam to use
webcam_index = int(input("Select the webcam to use: "))
webcam = cv2.VideoCapture(webcam_index)

# # Connect to the Tello drone
if source == "2":
    tello = Tello()

    tello.connect()
    tello.streamon()

while True:
    if source == "1":
        frame = getWebCamImage(webcam_index)
    elif source == "2":
        frame = tello.get_frame_read().frame
    else:
        print("Invalid source")
        break

    # Apply color correction
    if source == "2":
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    filteredFrame = detect_triangles(frame)

    # Draw grid lines
    grid_spacing = 50  # Distance between grid lines
    height, width, _ = frame.shape

    # Draw horizontal lines
    for y in range(0, height, grid_spacing):
        cv2.line(filteredFrame, (0, y), (width, y), (255, 0, 0), 1)

    # Draw vertical lines
    for x in range(0, width, grid_spacing):
        cv2.line(filteredFrame, (x, 0), (x, height), (255, 0, 0), 1)

    # Show frame with filter and without filter
    cv2.imshow('frame', frame)
    cv2.imshow('filteredFrame', filteredFrame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()