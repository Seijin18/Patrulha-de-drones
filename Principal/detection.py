import cv2
import numpy as np

# variaveis =
# Define range for the color red
lower_red = np.array([160, 60, 60])
upper_red = np.array([179, 255, 255])

# Define range for the color red
#lower_red = np.array([0, 160, 100])  # Lower bound for the color
#upper_red = np.array([50, 255, 255])  # Upper bound for the color

#lower_red = np.array([0, 120, 70])
#upper_red = np.array([10, 255, 255])

min_contour_area = 1000  # Minimum contour area to consider

# Função de detecção de objetos
def detect_objects(frame):
    # Correct saturation
    frame = cv2.convertScaleAbs(frame, alpha=1.5, beta=0)

    # Apply Gaussian blur to reduce noise
    frame = cv2.GaussianBlur(frame, (5, 5), 0)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a filter for the color red
    mask = cv2.inRange(hsv, lower_red, upper_red)
    
    mask = cv2.Canny(mask, 100, 200)

    # Apply the filter to the image
    filteredFrame = cv2.bitwise_and(frame, frame, mask=mask)

    # Find contours of red objects
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area
    #min_contour_area = 1000  # Minimum contour area to consider
    large_contours = [contour for contour in contours if cv2.contourArea(contour) > min_contour_area]

    area, centers = 0, (None, None)

    for contour in large_contours:
        
        # Draw the contour
        epsilon = 0.022 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        cv2.drawContours(filteredFrame, [approx], -1, (0, 255, 0), 2)
        
        '''
        # Criar uma nova imagem em branco com as mesmas dimensões da imagem original
        height, width = filteredFrame.shape[:2]
        blankImage = np.zeros((height, width, 3), np.uint8)
        
        # Calcular epsilon e aproximar o contorno
        epsilon = 0.022 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        # Desenhar o contorno na nova imagem em branco
        cv2.drawContours(blankImage, [approx], -1, (0, 255, 0), 2)
        '''
        
        
        # Compute the center of the contour
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(filteredFrame, (cX, cY), 3, (255, 255, 255), -1)
            if area < cv2.contourArea(contour):
                area = cv2.contourArea(contour)
                centers = (cX, cY)
        
        '''
        # Compute the center of the contour
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            #cv2.circle(blankImage, (cX, cY), 3, (255, 255, 255), -1)
            if area < cv2.contourArea(contour):
                area = cv2.contourArea(contour)
                centers = (cX, cY)
        
        return blankImage, centers
        '''
        
    return filteredFrame, large_contours