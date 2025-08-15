import cv2
import numpy as np
import pyautogui




cap = cv2.VideoCapture(0)

prev_x, prev_y = None, None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)

    
    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        
        c = max(contours, key=cv2.contourArea)
        if cv2.contourArea(c) > 2000:  
            x, y, w, h = cv2.boundingRect(c)
            cx, cy = x + w // 2, y + h // 2  

            
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)

            
            if prev_x is not None and prev_y is not None:
                dx = cx - prev_x
                dy = cy - prev_y

                if abs(dx) > abs(dy):  
                    if dx > 30:
                        pyautogui.press('right')
                        print("Right")
                    elif dx < -30:
                        pyautogui.press('left')
                        print("Left")
                else:  
                    if dy < -30:
                        pyautogui.press('up')
                        print("Up")
                    elif dy > 30:
                        pyautogui.press('down')
                        print("Down")

            prev_x, prev_y = cx, cy

    cv2.imshow("Gesture Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
