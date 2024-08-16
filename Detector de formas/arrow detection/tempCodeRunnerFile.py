            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 5)
            cv2.putText(img, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(img, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
    return img

def getArrowDirection(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
            cv2.drawContours(img, [approx], -1, (255, 0, 0), 3)
            cv2.putText(img, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(img, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
            if len(approx) == 7:
                cv2.putText(img, "Arrow pointing right", (x + w + 20, y + 70), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
                print("Arrow pointing right")
            elif len(approx) == 8:
                cv2.putText(img, "Arrow pointing left", (x + w + 20, y + 70), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
                print("Arrow pointing left")
            elif len(approx) == 9:
                cv2.putText(img, "Arrow pointing up", (x + w + 20, y + 70), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
                print("Arrow pointing up")
            elif len(approx) == 10:
                cv2.putText(img, "Arrow pointing down", (x + w + 20, y + 70), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
                print("Arrow pointing down")
    return img

if __name__ == "__main__":
    dir = os.getcwd()