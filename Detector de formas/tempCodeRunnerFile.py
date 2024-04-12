for i in range(0, filteredImage.shape[0], 20):
    cv2.line(filteredImage, (0, i), (filteredImage.shape[1], i), (255, 255, 255, 25), 1, cv2.LINE_AA)
for i in range(0, filteredImage.shape[1], 20):
    cv2.line(filteredImage, (i, 0), (i, filteredImage.shape[0]), (255, 255, 255, 25), 1, cv2.LINE_AA)