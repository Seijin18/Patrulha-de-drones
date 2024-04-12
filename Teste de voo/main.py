from djitellopy import Tello
import cv2
import numpy as np

tello = Tello()

tello.connect()
tello.streamon()

while True:
    frame = tello.get_frame_read().frame

    # Apply color correction
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # type: ignore

    # Correct saturation
    frame = cv2.convertScaleAbs(frame, alpha=1.5, beta=0)

    '''# Pre-process the frame for better visualization
    frame = cv2.GaussianBlur(frame, (5, 5), 0)
    frame = cv2.medianBlur(frame, 5)

    # Improve contrast
    frame = cv2.convertScaleAbs(frame, alpha=1.2, beta=0)

    # Highlight only the red color
    mask = cv2.inRange(frame, (0, 0, 50), (50, 50, 255))

    # Apply filter
    filteredFrame = cv2.bitwise_and(frame, frame, mask=mask)'''

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Definir intervalo para a cor vermelha
    lower_red = np.array([160, 60, 60])
    upper_red = np.array([179, 255, 255])

    # Criar um filtro para a cor vermelha
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Aplicar o filtro na imagem
    filteredFrame = cv2.bitwise_and(frame, frame, mask=mask)

    # Find contours of red objects
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area
    min_contour_area = 1000  # Minimum contour area to consider
    large_contours = [contour for contour in contours if cv2.contourArea(contour) > min_contour_area]

    # Draw contours on filtered frame
    cv2.drawContours(filteredFrame, large_contours, -1, (0, 255, 0), 2)

    # Identify the center of the contours
    for contour in large_contours:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(filteredFrame, (cX, cY), 3, (255, 255, 255), -1)

    # Show frame with filter and without filter
    cv2.imshow('frame', frame)
    cv2.imshow('filteredFrame', filteredFrame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


