import cv2
import numpy as np

# Funções de ação
def turn_left(frame):
    # iluminar de vermelho o lado esquerdo da imagem com 50% de transparência
    height, width, _ = frame.shape
    overlay = frame.copy()
    for y in range(0, height):
        for x in range(0, width//2):
            overlay[y, x] = [0, 0, 255]  # Red color
    alpha = 0.5  # Transparency factor
    frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)
    return frame

def turn_right(frame):
    # iluminar de vermelho o lado direito da imagem com 50% de transparência
    height, width, _ = frame.shape
    overlay = frame.copy()
    for y in range(0, height):
        for x in range(width//2, width):
            overlay[y, x] = [0, 0, 255]  # Red color
    alpha = 0.5  # Transparency factor
    frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)
    return frame

# Função de controle
def control(frame, object):
    # Verificar se há um objeto detectado
    if len(object) == 0:
        return

    # Definir região central da imagem
    height, width, _ = frame.shape
    centro_x = width // 2
    centro_y = height // 2
    # Define a margem da região central
    margem = 50
    # Imprimir linhas de referência
    cv2.line(frame, (centro_x - margem, 0), (centro_x - margem, height), (255, 0, 0), 1)
    cv2.line(frame, (centro_x + margem, 0), (centro_x + margem, height), (255, 0, 0), 1)

    # Verificar se o objeto está na região central
    if object[0] < centro_x - margem:
        frame = turn_left(frame)
    elif object[0] > centro_x + margem:
        frame = turn_right(frame)
    return frame

# Função de detecção de objetos
def detect_objects(frame):
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

    centers = []

    for contour in large_contours:
        # Draw the contour
        cv2.drawContours(filteredFrame, [contour], -1, (0, 255, 0), 2)

        # Compute the center of the contour
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(filteredFrame, (cX, cY), 3, (255, 255, 255), -1)
            filteredFrame = control(filteredFrame, (cX, cY))
            centers.append((cX, cY))

    return filteredFrame, centers


# Image capture
cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image")
        break
    cv2.imshow('frame', frame)

    filteredFrame, centers = detect_objects(frame)
    cv2.imshow('filteredFrame', filteredFrame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()