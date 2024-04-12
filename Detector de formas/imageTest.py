import cv2

# Load an image from a file
image = cv2.imread('ProjEcomp/Detector de formas/frame.png')

# Highlight the red color in the image
mask = cv2.inRange(image, (0, 0, 80), (80, 80, 255))

# Apply a filter to the image
filteredImage = cv2.bitwise_and(image, image, mask=mask)

# Add a grid to the filtered image
for i in range(0, filteredImage.shape[0], 20):
    cv2.line(filteredImage, (0, i), (filteredImage.shape[1], i), (255, 255, 255, 25), 1, cv2.LINE_AA)
for i in range(0, filteredImage.shape[1], 20):
    cv2.line(filteredImage, (i, 0), (i, filteredImage.shape[0]), (255, 255, 255, 25), 1, cv2.LINE_AA)

# Find the contours of the red color in the image
contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(filteredImage, contours, -1, (0, 255, 0), 2)

# Identify the center of the contours
for contour in contours:
    M = cv2.moments(contour)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.circle(filteredImage, (cX, cY), 3, (255, 255, 255), -1)




# Display the image with the filter applied
cv2.imshow('filtered image', filteredImage)

# Check if the image was loaded successfully
if image is None:
    print('Error loading image')
else:
    # Display the image in a window named 'image'
    cv2.imshow('image', image)

    # Wait for any key to be pressed and close the window
    cv2.waitKey(0)
    cv2.destroyAllWindows()