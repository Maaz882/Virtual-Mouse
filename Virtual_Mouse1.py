# AI Virtual Mouse Project
'''  Maaz Hasan 
     Btech CSE AI
     2021-350-019  '''

import mediapipe as mp
import cv2
import pyautogui
import tkinter as tk
from tkinter import ttk

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Environment variables
wCam, hCam = 1280, 720
screenX, screenY = pyautogui.size()
screenCenter = (screenX // 2, screenY // 2)
# Debug show resolution print(f"screen dimensions: {screenX}x{screenY}")
scrollThreshold = 0.1  # Threshold for finger scrolling gesture
scrollSpeed = 15  # Controls the speed of scrolling
clickThreshold = 0.05  # Threshold for finger clicking gesture
prevFingerPos = None  # Initialize prevFingerPos here
SMOOTHING = 0.2  # adjust between 0.1 (more smooth) to 1.0 (no smooth)


# cap = cv2.VideoCapture(0)

# cap.set(3, wCam)
# cap.set(4, hCam)

hands = mp_hands.Hands()

stopProgram = False

def start_program():
    global stopProgram
    global prevFingerPos  # Add this line to access prevFingerPos inside the function
    stopProgram = False
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    while not stopProgram:
        success, img = cap.read()
        # Display a window of the current webcam footage each frame
        img = cv2.flip(img, 1)
        h, w, _ = img.shape
        rgbFrame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(rgbFrame)

        margin_x = int(0.20 * wCam)
        margin_y = int(0.20 * hCam)
        rect_x_min, rect_x_max = margin_x, wCam - margin_x
        rect_y_min, rect_y_max = margin_y, hCam - margin_y

        # Draw that ROI so you can see it (yellow rectangle):
        cv2.rectangle(img,
                      (rect_x_min, rect_y_min),
                      (rect_x_max, rect_y_max),
                      (255, 255, 0), 2)

        if results.multi_hand_landmarks and results.multi_handedness:
            lm = results.multi_hand_landmarks[0]
            label = results.multi_handedness[0].classification[0].label
            # print(f"Detected hand: {label}")
            
            if label == 'Right':
                circle_color = (0, 255, 0)  # Green for right hand
            else:
                circle_color = (0, 0, 255)  # Red for left hand
            circle_center = (w - 40, 40)  # (x, y)
            radius = 20

            cv2.circle(img, circle_center, radius, circle_color, thickness=-1)

            font = cv2.FONT_HERSHEY_SIMPLEX
            text_pos = (circle_center[0] - 30, circle_center[1] + 40)
            cv2.putText(img, label, text_pos, font, 0.7, (0, 0, 0), 2)

            # Isolate index fingertip and middle fingertip
            ttip = lm.landmark[mp_hands.HandLandmark.THUMB_TIP]
            iftip = lm.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            mftip = lm.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            rftip = lm.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            ptip = lm.landmark[mp_hands.HandLandmark.PINKY_TIP]

            px = int(ptip.x * w)
            py = int(ptip.y * h)

            # Debug show fingertip coordinates relative position print(f"X: {iftip_x} | Y: {iftip_y} | Z: {iftip_z}")
            cv2.circle(img, (int(ptip.x * img.shape[1]), int(ptip.y * img.shape[0])), 5, (0, 255, 0), -1)
            cv2.circle(img, (int(iftip.x * img.shape[1]), int(iftip.y * img.shape[0])), 5, (255, 0, 0), -1)
            cv2.circle(img, (int(mftip.x * img.shape[1]), int(mftip.y * img.shape[0])), 5, (0, 0, 255), -1)
            cv2.circle(img, (int(ttip.x * img.shape[1]), int(ttip.y * img.shape[0])), 5, (255, 255, 255), -1)
            cv2.circle(img, (int(rftip.x * img.shape[1]), int(rftip.y * img.shape[0])), 5, (255, 165, 0), -1)

            cv2.line(img, (int(iftip.x * img.shape[1]), int(iftip.y * img.shape[0])),
                     (int(ttip.x * img.shape[1]), int(ttip.y * img.shape[0])), (0, 255, 0), 5)
            cv2.line(img, (int(mftip.x * img.shape[1]), int(mftip.y * img.shape[0])),
                     (int(ttip.x * img.shape[1]), int(ttip.y * img.shape[0])), (0, 255, 0), 5)
            cv2.line(img, (int(rftip.x * img.shape[1]), int(rftip.y * img.shape[0])),
                     (int(ttip.x * img.shape[1]), int(ttip.y * img.shape[0])), (0, 0, 255), 5)
            
            # === Step 3: clamp px/py into [rect_x_min..rect_x_max, rect_y_min..rect_y_max] ===
            px_clamped = max(rect_x_min, min(px, rect_x_max))
            py_clamped = max(rect_y_min, min(py, rect_y_max))

            # === Step 4: normalize within the ROI (0..1) ===
            norm_x = (px_clamped - rect_x_min) / (rect_x_max - rect_x_min)
            norm_y = (py_clamped - rect_y_min) / (rect_y_max - rect_y_min)

            # === Step 5: map to full screen resolution (0..screenX, 0..screenY) ===
            fingerX = int(norm_x * screenX)
            fingerY = int(norm_y * screenY)


            # Move mouse cursor to current fingertip position
            # fingerX = int(screenCenter[0] + screenX * (ptip.x - 0.5))
            # fingerY = int(screenCenter[1] + screenY * (ptip.y - 0.5))
            # # Pad mouse cursor to edges
            # screenUpper = screenY * 2
            # screenRight = screenX * 2

            fingerX = fingerX if fingerX > 3 else 3
            fingerY = fingerY if fingerY > 3 else 3
            fingerX = fingerX if fingerX < screenX - 3 else screenX - 3
            fingerY = fingerY if fingerY < screenY - 3 else screenY - 3

            # Debug show fingertip coordinates by screen resolution 
            # print(f"X: {fingerX} | Y: {fingerY}")
            if prevFingerPos is None:
                prevFingerPos = (fingerX, fingerY)

            # Smooth movement
            smoothedX = int(SMOOTHING * fingerX + (1 - SMOOTHING) * prevFingerPos[0])
            smoothedY = int(SMOOTHING * fingerY + (1 - SMOOTHING) * prevFingerPos[1])

            pyautogui.moveTo(smoothedX, smoothedY)
            prevFingerPos = (smoothedX, smoothedY)


            # Calculate distance from each finger to the thumb
            leftDistance = ((iftip.x - ttip.x) ** 2 + (iftip.y - ttip.y) ** 2) ** 0.5
            rightDistance = ((mftip.x - ttip.x) ** 2 + (mftip.y - ttip.y) ** 2) ** 0.5
            quitDistance = ((rftip.x - ttip.x) ** 2 + (rftip.y - ttip.y) ** 2) ** 0.5

            if label == "Right":
        
                # Scroll if finger is close to thumb
                if leftDistance < scrollThreshold:
                    pyautogui.scroll(scrollSpeed)
                elif rightDistance < scrollThreshold:
                    pyautogui.scroll(-scrollSpeed)
                # elif quitDistance < scrollThreshold:
                #     stopProgram = True

            elif label == "Left":
                # Scroll if finger is close to thumb
                if leftDistance < clickThreshold:
                    pyautogui.leftClick()
                elif rightDistance < clickThreshold:
                    pyautogui.rightClick()
                # elif quitDistance < scrollThreshold:
                #     stopProgram = True

        cv2.imshow("Virtual Mouse", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break



def stop_program():
    global stopProgram
    stopProgram = True


root = tk.Tk()
root.title("AI Virtual Mouse")

start_button = ttk.Button(root, text="Start", command=start_program)
start_button.pack(pady=10)

stop_button = ttk.Button(root, text="Stop", command=stop_program)
stop_button.pack(pady=10)

root.mainloop()


